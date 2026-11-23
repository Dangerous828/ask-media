#!/usr/bin/env python3
"""gugu_h3q.py — 把角色C的 build_qwen_workflow 参数转成**队列**调用。

为什么需要这层
--------------
`smooth3d/tools/rerender_*.py` 直接 POST http://127.0.0.1:18199/prompt，
既指向已失效的端口，也绕过了「唯一提交入口是 h3q 队列」的纪律。

本文件此前调的是 `h3q_img.py`，**那同样是绕过队列**：h3q_img.py 自己的 docstring
写明「Called by h3q.py's worker, never by hand; run it directly only to debug one still」，
它直连 `127.0.0.1:8199/prompt`。手工调它 = 抢卡、不与队列互斥、无排队位次。
⇒ 现在改成调 `h3qc.py submit --kind image`，走 8200 唯一的 admission gate。

同时修 SSH 路由：默认 `win-desktop-cf`。`win-desktop` / `uu-2222` 实测拒连
（只有 CF Tunnel 通），旧默认值会让人以为脚本坏了。

用法（替换原来的 submit_and_wait）：
    from gugu_h3q import render_via_h3q
    render_via_h3q(
        prompt_text=prompt,
        ref_images=["kf_s04_anime_sunlit.png", ...],   # ComfyUI input/ 里的文件名
        out_name="kf_s05_v2_surprised.png",
        seed=2040,
        steps=0,          # 0 = 队列默认（8步 + Turbo LoRA）；传 45 则显式 --steps 45 --cfg 4.0
    )

命令行：
    python3 gugu_h3q.py --prompt-file p.txt --out o.png [--refs a.png,b.png] [--seed 42]
    python3 gugu_h3q.py ... --dry-run      # 只打印将执行的命令，不提交

本脚本不直接连 ComfyUI，只调远端（`win-desktop-cf`）上的 `h3qc.py`。
"""
import json
import os
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

# 唯一可用路由：CF Tunnel（`win-desktop` / `uu-2222` 实测拒连，2026-10-22 复验）
HOST = os.environ.get("H3Q_HOST", "win-desktop-cf")
REMOTE_SCRIPTS = os.environ.get("H3Q_SCRIPTS", r"E:\H3-Studio\scripts")
REMOTE_PY = os.environ.get("H3Q_PY", r"E:\ComfyUI\ComfyUI_windows_portable\python_embeded\python.exe")
REMOTE_TMP = os.environ.get("H3Q_TMP", r"C:\Users\xc")
REMOTE_OUT_DIR = os.environ.get("H3Q_OUT", r"E:\H3-Studio\renders")
LOCAL_OUT_DIR = os.environ.get(
    "GUGU_OUT",
    "~/Code/kTool/example-project/smooth3d/assets/generated",
)


def _ssh(ps_body: str, timeout: int = 900) -> tuple[int, str]:
    """把 PowerShell 脚本上传到远端再执行。

    不用 -EncodedCommand：长脚本在 ssh 下会静默超时。
    不用 bash 单引号拼接：远端是 cmd.exe，中文与引号会碎。
    """
    with tempfile.TemporaryDirectory() as td:
        ps1 = Path(td) / "run.ps1"
        ps1.write_text(ps_body, encoding="utf-8-sig")
        remote_ps1 = f"{REMOTE_TMP}/h3q_run.ps1"
        subprocess.run(["scp", "-o", "ConnectTimeout=20", str(ps1), f"{HOST}:{remote_ps1}"],
                       check=True, capture_output=True)
        cmd = f'powershell -ExecutionPolicy Bypass -File "{remote_ps1}"'
        p = subprocess.run(["ssh", "-o", "ConnectTimeout=20", HOST, cmd],
                           capture_output=True, text=True, timeout=timeout)
        return p.returncode, (p.stdout or "") + (p.stderr or "")


def _scp_up(local: Path) -> str:
    """上传到远端临时目录，返回远端路径。"""
    remote = f"{REMOTE_TMP}/{local.name}"
    subprocess.run(["scp", "-o", "ConnectTimeout=20", str(local), f"{HOST}:{remote}"],
                   check=True, capture_output=True)
    return remote


def _scp_down(remote_name: str, local: Path) -> None:
    local.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["scp", "-o", "ConnectTimeout=20",
                    f"{HOST}:{REMOTE_OUT_DIR.replace(chr(92), '/').rstrip(chr(47))}/{remote_name}", str(local)],
                   check=True, capture_output=True)


def render_via_h3q(prompt_text: str, ref_images: list[str], out_name: str,
                   seed: int = 42, steps: int = 0, size: str = "1376x768",
                   label: str = "h3q/gugu", timeout: int = 900,
                   dry_run: bool = False) -> dict:
    """通过 h3q **队列**出图。返回 {ok, out, raw}。

    steps：0 = 队列默认（8 步 + Turbo LoRA）
           其他 = 显式 --steps N --cfg 4.0（对齐角色C原脚本的 45 步）
    """
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
            f"--idem-key 'gugu-{Path(out_name).stem}-s{int(seed)}'",
        ]
        if refs:
            args.append(f"--refs '{refs}'")
        if steps and steps != 8:
            args += [f"--steps {int(steps)}", "--cfg 4.0"]

        py_args = " ".join(args)
        ps = (
            f"Set-Location '{REMOTE_SCRIPTS}'; "
            f"& '{REMOTE_PY}' -X utf8 h3qc.py {py_args} --wait --interval 5 2>&1 | Out-String"
        )
        if dry_run:
            return {"ok": True, "dry_run": True, "command": ps,
                    "out": str(Path(LOCAL_OUT_DIR) / out_name)}
        rc, out = _ssh(ps, timeout=timeout)

    # 队列成功判据：h3qc --wait 返回 0 且 job 记录 state=done
    ok = (rc == 0 and '"state": "done"' in out)
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
    ap.add_argument("--size", default="1376x768")
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
