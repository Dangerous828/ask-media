#!/usr/bin/env python3
"""example_h3q.py — 把角色C的 build_qwen_workflow 参数转成**队列**调用。

为什么需要这层
--------------
`smooth3d/tools/rerender_*.py` 直接 POST http://127.0.0.1:18199/prompt，
既指向已失效的端口，也绕过了「唯一提交入口是 h3q 队列」的纪律。

本文件此前调的是 `h3q_img.py`，**那同样是绕过队列**：h3q_img.py 自己的 docstring
写明「Called by h3q.py's worker, never by hand; run it directly only to debug one still」，
它直连 `127.0.0.1:8199/prompt`。手工调它 = 抢卡、不与队列互斥、无排队位次。
⇒ 现在改成调 `h3qc.py submit --kind image`，走 8200 唯一的 admission gate。

远端主机与目录全部来自环境变量，未配置直接报错，避免静默连错机器。

用法（替换原来的 submit_and_wait）：
    from example_h3q import render_via_h3q
    render_via_h3q(
        prompt_text=prompt,
        ref_images=["kf_s04_anime_sunlit.png", ...],   # ComfyUI input/ 里的文件名
        out_name="kf_s05_v2_surprised.png",
        seed=2040,
        steps=0,          # 0 = 走队列默认档；传 N>0 则显式 --steps N --cfg 3.5（线性 CFG 取值，与步数无关）
    )

命令行：
    python3 example_h3q.py --prompt-file p.txt --out o.png [--refs a.png,b.png] [--seed 42]
    python3 example_h3q.py ... --dry-run      # 只打印将执行的命令，不提交

本脚本不直接连 ComfyUI，只通过环境变量指定的渲染机上的 `h3qc.py` 提交队列。
"""
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

# 远端环境全部走环境变量。主名 H3Q_SSH_HOST / H3Q_REMOTE_PY（与 transcard、adapter 一致），
# 旧名 H3Q_HOST / H3Q_REMOTE_PYTHON / H3Q_PY 仍作兼容别名：
# python 读取顺序与 adapter 完全一致 H3Q_REMOTE_PY → H3Q_REMOTE_PYTHON → H3Q_PY（新名 → 旧名）。
# 未配置时在提交入口报错，不内置任何默认主机。
HOST = os.environ.get("H3Q_SSH_HOST") or os.environ.get("H3Q_HOST", "")
REMOTE_SCRIPTS = os.environ.get("H3Q_SCRIPTS", "")
REMOTE_PY = (os.environ.get("H3Q_REMOTE_PY") or os.environ.get("H3Q_REMOTE_PYTHON")
             or os.environ.get("H3Q_PY", ""))
REMOTE_TMP = os.environ.get("H3Q_TMP", "")
REMOTE_OUT_DIR = os.environ.get("H3Q_OUT", "")
# 本地产物目录：EXAMPLE_OUT 优先，GUGU_OUT 为改名前的兼容别名。
LOCAL_OUT_DIR = os.environ.get("EXAMPLE_OUT") or os.environ.get("GUGU_OUT", "./generated")


def _require_env() -> None:
    """检查远端环境变量。主名 H3Q_SSH_HOST/H3Q_REMOTE_PY，
    旧名 H3Q_HOST/H3Q_REMOTE_PYTHON/H3Q_PY 兼容。"""
    missing = [k for k, v in [
        ("H3Q_SSH_HOST/H3Q_HOST", HOST), ("H3Q_SCRIPTS", REMOTE_SCRIPTS),
        ("H3Q_REMOTE_PY/H3Q_REMOTE_PYTHON/H3Q_PY", REMOTE_PY), ("H3Q_TMP", REMOTE_TMP),
        ("H3Q_OUT", REMOTE_OUT_DIR),
    ] if not v]
    if missing:
        sys.exit(
            f"缺少远端环境变量: {', '.join(missing)}。\n"
            "请先设置渲染机的 SSH 主机与目录，例如:\n"
            "  export H3Q_SSH_HOST=<渲染主机>          # ssh 可达的渲染机（旧名 H3Q_HOST 仍兼容）\n"
            "  export H3Q_SCRIPTS=<渲染机脚本目录>   # 含 h3qc.py\n"
            "  export H3Q_REMOTE_PY=<渲染机 python 路径>  # 旧名 H3Q_REMOTE_PYTHON / H3Q_PY 仍兼容\n"
            "  export H3Q_TMP=<渲染机临时目录>\n"
            "  export H3Q_OUT=<渲染机产物目录>\n"
            "  export EXAMPLE_OUT=<本地产物目录>       # 可选，默认 ./generated（旧名 GUGU_OUT 仍兼容）"
        )


def _job_state_done(out: str) -> bool:
    """从 h3qc --wait 输出里取 job JSON 的 state 字段，精确判断是否 done。

    不用 '"state": "done"' 子串匹配：远程输出里出现同字串（日志/提示词）会误判；
    Out-String 还可能按控制台宽度折行，故先去掉 JSON 片段内的换行空白再解析。
    """
    for i, ch in enumerate(out):
        if ch != "{":
            continue
        depth = 0
        in_str = False
        esc = False
        for j in range(i, len(out)):
            c = out[j]
            if in_str:
                if esc:
                    esc = False
                elif c == "\\":
                    esc = True
                elif c == '"':
                    in_str = False
                continue
            if c == '"':
                in_str = True
            elif c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    frag = re.sub(r"\s+", " ", out[i:j + 1])
                    try:
                        obj = json.loads(frag)
                    except ValueError:
                        break
                    if isinstance(obj, dict) and obj.get("state") == "done":
                        return True
                    break
    return False


def _ssh(ps_body: str, timeout: int = 900) -> tuple[int, str]:
    """把 PowerShell 脚本上传到远端再执行。

    不用 -EncodedCommand：长脚本在 ssh 下会静默超时。
    不用 bash 单引号拼接：远端是 cmd.exe，中文与引号会碎。
    """
    with tempfile.TemporaryDirectory() as td:
        ps1 = Path(td) / "run.ps1"
        ps1.write_text(ps_body, encoding="utf-8-sig")
        remote_ps1 = f"{REMOTE_TMP}/h3q_run.ps1"
        subprocess.run(["scp", "-o", "ConnectTimeout=20", "-o", "StrictHostKeyChecking=accept-new",
                        str(ps1), f"{HOST}:{remote_ps1}"],
                       check=True, capture_output=True)
        cmd = f'powershell -ExecutionPolicy Bypass -File "{remote_ps1}"'
        p = subprocess.run(["ssh", "-o", "ConnectTimeout=20", "-o", "StrictHostKeyChecking=accept-new",
                            HOST, cmd],
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")


def _scp_up(local: Path) -> str:
    """上传到远端临时目录，返回远端路径。"""
    remote = f"{REMOTE_TMP}/{local.name}"
    subprocess.run(["scp", "-o", "ConnectTimeout=20", "-o", "StrictHostKeyChecking=accept-new",
                    str(local), f"{HOST}:{remote}"],
                   check=True, capture_output=True)
    return remote


def _scp_down(remote_name: str, local: Path) -> None:
    local.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["scp", "-o", "ConnectTimeout=20", "-o", "StrictHostKeyChecking=accept-new",
                    f"{HOST}:{REMOTE_OUT_DIR.replace(chr(92), '/').rstrip(chr(47))}/{remote_name}", str(local)],
                   check=True, capture_output=True)


# 默认画布与 label 沿用改名前的实测值（1376x768 / h3q/gugu），避免旧调用方
# 静默跑在新默认值上；显式传 --size/--label 可覆盖。
def render_via_h3q(prompt_text: str, ref_images: list[str], out_name: str,
                   seed: int = 42, steps: int = 0, size: str = "1376x768",
                   label: str = "h3q/gugu", timeout: int = 900,
                   dry_run: bool = False) -> dict:
    """通过 h3q **队列**出图。返回 {ok, out, raw}。

    steps：0 = 队列默认（档位现状以 h3qc/MCP 实读为准，实测快照见
           h3-queue/references/still-standard-tier-20261105.md）
           8 = 已退役 Turbo 档的遗留值：代码将其按默认档处理（不生成显式
           --steps/--cfg，实际走默认档步数），等效于不传
           >0 且 !=8 = 显式 --steps N --cfg 3.5（固定配线性 CFG 3.5，与步数无关；
           档位现状按 h3qc/MCP 实读，见 h3-queue/references/still-standard-tier-20261105.md）
    """
    if steps < 0:
        sys.exit("--steps 不能为负数: %d" % steps)
    _require_env()
    # 危险字符黑名单（PowerShell 拼接无转义体系，拒绝即阻止）：在**上传之前**检查，
    # 被拒的提交不产生任何远端副作用；--size 与 --out/--label/--refs 一并覆盖。
    import re as _re
    for _v in [out_name, label, size] + list(ref_images):
        if _re.search(r"[\\'\"`;&|<>]", str(_v)):
            raise ValueError(f"参数含命令拼接字符，拒绝提交: {str(_v)[:60]}")
    with tempfile.TemporaryDirectory() as td:
        pf = Path(td) / f"{Path(out_name).stem}.txt"
        pf.write_text(prompt_text, encoding="utf-8")
        remote_prompt = _scp_up(pf)
        refs = ",".join(ref_images) if ref_images else ""
        args = [
            "submit", "--kind image",
            f"--prompt-file '{remote_prompt}'",
            f"--out '{REMOTE_OUT_DIR}\\{out_name}'",
            f"--size {size}",
            f"--seed {int(seed)}",
            f"--label '{label}'",
            # idem-key 必须含 seed 与 out 名：同 prompt 换 seed 是不同活，
            # 只按 label 去重会静默吞掉后续提交（实测踩过）
            f"--idem-key 'example-{Path(out_name).stem}-s{int(seed)}'",
        ]
        if refs:
            args.append(f"--refs '{refs}'")
        if steps and steps != 8:
            args += [f"--steps {int(steps)}", "--cfg 3.5"]

        py_args = " ".join(args)
        ps = (
            f"Set-Location '{REMOTE_SCRIPTS}'; "
            f"& '{REMOTE_PY}' -X utf8 h3qc.py {py_args} --wait --interval 5 2>&1 | Out-String"
        )
        if dry_run:
            return {"ok": True, "dry_run": True, "command": ps,
                    "out": str(Path(LOCAL_OUT_DIR) / out_name)}
        rc, out = _ssh(ps, timeout=timeout)

    # 队列成功判据：h3qc --wait 返回 0 且 job JSON 的 state 字段精确等于 done
    ok = (rc == 0 and _job_state_done(out))
    result = {"ok": ok, "out": str(Path(LOCAL_OUT_DIR) / out_name), "raw": out.strip()}
    if ok:
        try:
            _scp_down(out_name, Path(LOCAL_OUT_DIR) / out_name)
            result["downloaded"] = True
        except subprocess.CalledProcessError as e:
            result["downloaded"] = False
            result["download_error"] = str(e)[:200]
    return result


def main() -> int:
    import argparse
    ap = argparse.ArgumentParser(description="角色C出图 → h3q 队列")
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--refs", default="")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--steps", type=int, default=0)
    ap.add_argument("--size", default="1376x768", help="采样画布；沿用改名前实测默认值")
    ap.add_argument("--label", default="h3q/gugu")
    ap.add_argument("--dry-run", action="store_true", help="只打印远端命令，不提交")
    args = ap.parse_args()

    text = Path(args.prompt_file).read_text(encoding="utf-8")
    refs = [x.strip() for x in args.refs.split(",") if x.strip()]
    r = render_via_h3q(text, refs, args.out, seed=args.seed, steps=args.steps,
                       size=args.size, label=args.label, dry_run=args.dry_run)
    print(json.dumps({k: v for k, v in r.items() if k != "raw"}, ensure_ascii=False, indent=1))
    if not r["ok"]:
        print(r.get("raw", ""), file=sys.stderr)
    return 0 if r["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
