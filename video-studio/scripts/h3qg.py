#!/usr/bin/env python3
"""h3qg.py -- h3qc 的闸门包装（Gate wrapper）：提交前自动跑 preflight。

为什么要有这一层
----------------
`preflight.py` 已经能做 5 项检查，但它**不在提交路径上**：
要靠人记得手动跑，而「最容易跳过」的恰好是代价最高的两项
（参考图拼版 → 71.9% 废片；剧本事件丢失 → 整镜白烧）。

本包装把闸门挂到**唯一提交入口**的前面：任何 `submit` 都要先过闸。

为什么包装 h3qc 而不是改 h3q.py
------------------------------
h3q.py 是常驻服务，改它必须重启 —— 而重启会打断正在跑的渲染。
h3qc.py 是客户端，每次提交都是新进程，**改完立刻生效、零中断**。
闸门必须在客户端侧，服务端只负责排队与显存，职责也更干净。

闸门规则（按 kind 分流，只跑了能跑的那几项）
------------------------------------------
| kind  | 闸门 |
|-------|------|
| image | `--refs` / `--first-frame` / `--last-frame` 非空 → `ref_guard.py`（静帧链：拦拼版垫图） |
| video | `--refs` → `ref_guard.py`（Ref2VA 链：多视图身份卡合法）；`--first-frame` / `--last-frame` → `ref_guard.py`（首尾帧链：必须单画面）；`--prompt-file` → `h3_lint.py`（H3 结构一致性） |

**`--refs` 与 `--first-frame` 都为空就不跑 ref_guard**（没有输入可查）。
**`story_check` / `segment_guard` 不在本包装里**：它们需要剧本与成片目录，
属于「批次级」检查，由 `preflight.py` 在批次层面跑；单次提交没有这些上下文。

用法
----
    # 和 h3qc 完全一样，只是多一层闸门
    python h3qg.py submit --kind image --prompt-file p.txt --out o.png --size 1344x768
    python h3qg.py queue / health / show / ls / stats / cancel   # 直接透传

    # 明知故犯（会在日志里留痕）
    python h3qg.py submit ... --gate-off
    # 只跑闸门、不提交
    python h3qg.py submit ... --gate-only

环境
----
    H3QG_SKILL   video-studio scripts 目录（默认按本仓库内的相对位置）

退出码
------
    0 提交成功（或 --gate-only 闸门通过）
    1 闸门拦截（不提交）
    2 参数错误
    3 队列不可达
    其他 = h3qc 的原始退出码

已知边界
--------
- 本包装**不复制**闸门逻辑，只调用 video-studio 的脚本；判据更新只改一处。
- `h3_lint.py` 的退出码非 0 只作 **warn**（不阻断），因为 H3 提示词的写法
  以项目已验收的写法为准，lint 会误报（见 video-studio `结论-提示词体系适用性.md`）。
  `ref_guard` 拦截**才**阻断 —— 它的误报代价远低于放过一张拼版的代价。
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

# Windows 控制台默认 GBK，中文/emoji 会 UnicodeEncodeError 直接崩进程。
# 闸门是拦截逻辑，绝不能因为「打印」失败而放行或误拦 —— 先把 stdout 钉成 UTF-8。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

HERE = Path(__file__).resolve().parent
# 闸门「找不到脚本就静默跳过」是最危险的失效模式：它会让人以为查过了。
# 所以多探几个候选；一个都没有时 gate() 直接报错拒提交，不假装通过。
def _skill_dir():
    cands = []
    env = os.environ.get("H3QG_SKILL")
    if env:
        cands.append(Path(env))
    cands += [HERE, HERE / "vgate",
              Path.home() / ".skills" / "hub" / "video-studio" / "scripts"]
    for p in cands:
        if (p / "ref_guard.py").exists():
            return p
    return cands[0] if cands else HERE


SKILL = _skill_dir()
PY = os.environ.get("H3QG_PY", sys.executable)


def _run(path: Path, args: list) -> tuple:
    """跑一个闸门脚本，返回 (ok, out)。脚本不存在按通过处理并说明。

    子进程强制 UTF-8：Windows 下默认按 GBK 解码，闸门脚本的中文输出会
    直接 UnicodeDecodeError —— 那时 `ok=False` 会被误判成「闸门拦截」。
    """
    if not path.exists():
        return True, "(闸门脚本不存在，跳过: %s)" % path
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([PY, "-X", "utf8", str(path)] + [str(a) for a in args],
                       capture_output=True, text=True,
                       encoding="utf-8", errors="replace", env=env)
    return p.returncode == 0, ((p.stdout or "") + (p.stderr or "")).strip()


def split_refs(raw: str) -> list:
    """--refs 是逗号分隔的 input/ 文件名；相对名要拼成绝对路径才能查。"""
    out = []
    for name in (raw or "").split(","):
        name = name.strip()
        if not name:
            continue
        p = Path(name)
        if not p.is_absolute():
            # ComfyUI 的 input 目录；只用于读取判据，不改原图
            p = Path(os.environ.get(
                "H3QG_INPUT", "ComfyUI/input")) / name
        out.append(p)
    return out


def gate(a) -> int:
    """跑闸门。返回 0=放行，1=拦截。

    「无法校验」一律**拦截**而不是放行：闸门静默失效比误拦危险得多——
    前者会让人以为查过了。真不想查请用 --gate-off（会留痕）。
    """
    kind = getattr(a, "kind", "video") or "video"
    blocks, warns = [], []

    refs = split_refs(getattr(a, "refs", "") or "")
    # FL2VA 的尾帧和首帧走同一条「必须是单画面」判据；漏掉它，首尾帧任务
    # 只查了一半。图片模式的 --refs 是静帧垫图，不是 Ref2VA 多槽参考。
    refs_chain = "still" if kind == "image" else "ref2va"
    ff_refs = split_refs(getattr(a, "first_frame", "") or "")
    ff_refs += split_refs(getattr(a, "last_frame", "") or "")
    if refs or ff_refs:
        if not (SKILL / "ref_guard.py").exists():
            blocks.append("闸门脚本缺失：找不到 %s\n"
                          "   ⇒ 无法校验参考图。把 ref_guard.py 与 h3qg.py 放同目录，"
                          "或设 H3QG_SKILL 指过去。" % (SKILL / "ref_guard.py"))
        else:
            missing = [str(r) for r in refs + ff_refs if not Path(r).exists()]
            if missing:
                # 闸门必须与参考图**同机**：h3qg 在 Mac 上跑、refs 却是
                # Windows 的 ComfyUI input 文件名时，读不到图就等于没查。
                blocks.append("参考图在本机不存在，无法校验：%s\n"
                              "   ⇒ 闸门要和 h3qc 在同一台机器上跑（Windows 提交侧），"
                              "或把 --refs 换成本机可读路径。" % missing)
            else:
                print("提醒：参考图只能是原始资产、画风基准或经 look_check 以 --use reference 批准的生成物；"
                      "拼贴/修图/未验收视频抽帧不得提交（h3-queue「参考图来源纪律」）。")
                # 链路决定判据（2026-10-30）：帧锚（首帧/尾帧）按「必须单画面」判据，
                # 其余按垫图链路判据——视频多槽是 Ref2VA（身份卡合法），图片垫图是
                # 静帧链（拼版当构图模板的风险位）。分批跑，不能混用一个闸。
                pf0 = getattr(a, "prompt_file", "") or ""
                extra = ["--prompt", pf0] if (pf0 and Path(pf0).exists()) else []
                ok_all, out_all = True, []
                for batch, chain in (
                    (refs, refs_chain),
                    (ff_refs, "first_frame"),
                ):
                    if not batch:
                        continue
                    ok, out = _run(SKILL / "ref_guard.py", list(batch) + ["--chain", chain] + extra)
                    out_all.append("[%s 链路]\n%s" % (chain, out))
                    if not ok:
                        ok_all = False
                out = "\n".join(out_all)
                if not ok_all:
                    blocks.append("ref_guard 拦下参考图：\n" + out)
                elif out:
                    warns.append(out)

    if kind == "video":
        pf = getattr(a, "prompt_file", "") or ""
        lint = SKILL / "h3_lint.py"
        if pf and Path(pf).exists():
            if lint.exists():
                ok, out = _run(lint, [pf])
                if not ok:
                    # 只 warn：H3 写法以项目已验收为准，lint 会误报
                    warns.append("h3_lint 有告警（不阻断）：\n" + out)
            else:
                warns.append("h3_lint.py 不在 %s，本条视频结构检查未做" % SKILL)

    if blocks:
        print("=" * 66)
        print("❌ 提交前闸门拦截（未入队）")
        print("=" * 66)
        for b in blocks:
            print(b)
        print("\n确认无误后可用 --gate-off 跳过（会留痕）。")
        return 1
    if warns:
        print("闸门告警（不阻断）：")
        for w in warns:
            print("  " + w.replace("\n", "\n  "))
    return 0


def main() -> int:
    # 先解析本层关心的几个开关，其余原样透传给 h3qc
    argv = sys.argv[1:]
    gate_off = "--gate-off" in argv
    gate_only = "--gate-only" in argv
    argv = [x for x in argv if x not in ("--gate-off", "--gate-only")]

    if not argv:
        print(__doc__)
        return 2

    # 只在 submit 子命令上做闸门
    if argv[0] == "submit":
        pa = argparse.ArgumentParser(add_help=False)
        pa.add_argument("--kind", default="video")
        pa.add_argument("--refs", default="")
        pa.add_argument("--first-frame", default="")
        pa.add_argument("--last-frame", default="")
        pa.add_argument("--prompt-file", default="")
        known, _ = pa.parse_known_args(argv[1:])
        skipped = False
        if gate_off:
            print("⚠️  --gate-off：跳过提交前闸门（本次不查参考图 / H3 结构）")
            skipped = True
        else:
            rc = gate(known)
            if rc != 0:
                return 1
        if gate_only:
            # 不能对「闸门被跳过」也报「闸门通过」——那是假凭证
            print("--gate-only：闸门**已跳过**（--gate-off），未校验，也未提交。"
                  if skipped else "--gate-only：闸门通过，未提交。")
            return 0

    # 透传给 h3qc
    h3qc = HERE / "h3qc.py"
    if not h3qc.exists():
        print("ERROR: 找不到 h3qc.py（应在 %s）" % HERE, file=sys.stderr)
        return 2
    p = subprocess.run([PY, "-X", "utf8", str(h3qc)] + argv,
                       env=dict(os.environ, PYTHONIOENCODING="utf-8"))
    return p.returncode


if __name__ == "__main__":
    sys.exit(main())
