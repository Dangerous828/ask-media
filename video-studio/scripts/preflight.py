#!/usr/bin/env python3
"""preflight.py — 提交前一次跑完全部检查（5 项检查串成一条流水线）。

为什么要有它
------------
分散跑这五项检查容易漏跑，尤其「剧本对账」和「参考图检查」这两个最容易被跳过——
而它们恰好拦的是代价最高的两类事故：
  · 整镜丢失 / 事件降级成静态（story_check）
  · 拼版参考图导致废片："拼版被当构图模板"（ref_guard；小样本实测观察（样本与复现命令未随公开版发布））

本流水线按「越早发现越省钱」排序：
    1. ref_guard     参考图 —— 拦在**生成之前**（最省，不烧 GPU）
    2. story_check   剧本对账 —— 拦在**交稿之前**（不烧 GPU）
    3. segment_guard 段内自溶 —— 拦在**出片之后、接成片之前**（帧级，唯一能查自溶的）
    4. qc_image      关键帧四带 —— 拦在**出图之后**（已烧过图，但拦在出视频前）
    5. qc_signals    介质告警 —— 只告警，不阻断

为什么第 3 项不是 story_check 的一部分：文本层查不出"同镜内黑框自溶"
（EP01 事故里 S02 写"推镜穿屏"、S03 只写"满幅"，两个文件各自都对，
自溶发生在渲染内部），只有帧级外环死黑曲线能证。两者是互补的两半。

用法
----
    # 最完整：五项全跑
    python3 preflight.py \
        --refs <参考图目录或文件> --target-aspect 16:9 \
        --script <剧本.md> --shots <提示词目录> \
        --clips <成片段目录> \
        --frames <关键帧目录> --profile <档> --baseline <本片基准目录>

    # 只跑其中几项：不给对应参数即跳过
    python3 preflight.py --refs refs/ --script 剧本.md --shots prompts/
    python3 preflight.py --clips video/          # 只查段内自溶

退出码
------
    0  全部通过（可提交）
    1  有阻断项（禁止提交）
    2  参数错误 / 必要参数缺失
"""
import argparse
import os
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
# 子检查超时：某个子脚本挂住不能让整个 preflight 无限等。默认 3600s，可用
# H3Q_PREFLIGHT_TIMEOUT 覆盖；超时记作 rc=2（NOTCHECKED，禁止提交但措辞不是「被拦」）。
SUBCHECK_TIMEOUT = int(os.environ.get("H3Q_PREFLIGHT_TIMEOUT", "3600"))


def run(name, cmd):
    """跑一个子检查，返回 (ok, exit_code, stdout)。"""
    print(f"\n{'='*66}\n[{name}] {' '.join(str(c) for c in cmd[1:])}\n{'='*66}")
    try:
        p = subprocess.run([sys.executable] + [str(c) for c in cmd],
                           capture_output=True, text=True, timeout=SUBCHECK_TIMEOUT)
    except subprocess.TimeoutExpired as e:
        out = ((e.stdout or b"") + (e.stderr or b"")).decode("utf-8", "replace") \
            if isinstance(e.stdout, bytes) else ((e.stdout or "") + (e.stderr or ""))
        print(out.rstrip())
        print(f"ERROR: 子检查超时（{SUBCHECK_TIMEOUT}s）：{name}", file=sys.stderr)
        return False, 2, out + f"\nTIMEOUT after {SUBCHECK_TIMEOUT}s"
    out = (p.stdout or "") + (p.stderr or "")
    print(out.rstrip())
    return p.returncode == 0, p.returncode, out


def main() -> int:
    ap = argparse.ArgumentParser(description="提交前流水线（5 项检查）")
    ap.add_argument("--refs", nargs="*", default=None, help="参考图（文件或目录）")
    ap.add_argument("--target-aspect", default=None, help="目标画幅，如 16:9")
    ap.add_argument("--script", default=None, help="剧本 .md")
    ap.add_argument("--shots", default=None, help="H3 提示词目录")
    ap.add_argument("--clips", default=None, help="成片段目录或文件（段内自溶帧级检查）")
    ap.add_argument("--frames", default=None, help="关键帧目录")
    ap.add_argument("--profile", default=None, help="qc_image 档位（与 --baseline 二选一）")
    ap.add_argument("--baseline", default=None, help="qc_image 基准目录（推荐，走混合判据）")
    ap.add_argument("--allow-decay", action="store_true",
                    help="创意上允许黑框在段内自己出画：segment_guard 只报告不阻断")
    ap.add_argument("--skip-signals", action="store_true", help="跳过介质告警")
    args = ap.parse_args()

    # 至少要有内容可查
    if not any([args.refs, args.script, args.clips, args.frames]):
        print("ERROR: 至少要给 --refs / --script / --clips / --frames 之一", file=sys.stderr)
        return 2

    blockers = []
    results = []

    def add(name, cmd, block_label, nocheck_label, allow_flag=None):
        """跑一项并**按退出码分三态**记录。

        0=PASS；1=BLOCK（闸门真的判了不合格）；
        2=NOTCHECKED（参数/路径错，一项都没查成）。
        后两者都禁止提交，但**措辞必须分开**：把 exit 2 报成「被拦」，
        会让人以为闸门抓到了一张坏图，而实际上根本没看到图。
        """
        ok, rc, _ = run(name, cmd)
        # name 形如 "1/5 ref_guard 参考图" → 取第二段作为脚本名
        results.append((name.split()[1], ok, rc))
        if rc == 0:
            return
        blockers.append(nocheck_label if rc == 2 else block_label)

    # 1) 参考图（最先，不烧 GPU）
    if args.refs:
        cmd = [SCRIPTS / "ref_guard.py"] + list(args.refs)
        if args.target_aspect:
            cmd += ["--target-aspect", args.target_aspect]
        add("1/5 ref_guard 参考图", cmd,
            "ref_guard（参考图被拦）",
            "ref_guard 参数/路径错误，**未能校验**参考图（看上面 ERROR 行）")

    # 2) 剧本对账（不烧 GPU）
    if args.script:
        if not args.shots:
            print("ERROR: 给了 --script 就必须给 --shots", file=sys.stderr)
            return 2
        add("2/5 story_check 剧本对账",
            [SCRIPTS / "story_check.py", "--script", args.script,
             "--shots", args.shots],
            "story_check（剧本对账有 error）",
            "story_check 参数/路径错误，**未能对账**（看上面 ERROR 行）")

    # 3) 段内黑框自溶（帧级，文本层查不出的那一半）
    if args.clips:
        cmd = [SCRIPTS / "segment_guard.py", args.clips]
        if args.allow_decay:
            cmd.append("--allow-decay")
        add("3/5 segment_guard 段内自溶", cmd,
            "segment_guard（段内黑框自溶）",
            "segment_guard 读不到视频，**未能校验**（看上面 ERROR 行）")

    # 4) 关键帧四带
    if args.frames:
        if not (args.profile or args.baseline):
            print("ERROR: 给了 --frames 就必须给 --profile 或 --baseline", file=sys.stderr)
            return 2
        cmd = [SCRIPTS / "qc_image.py", args.frames]
        if args.baseline:
            cmd += ["--baseline", args.baseline]
        if args.profile:
            cmd += ["--qc-profile", args.profile]
        add("4/5 qc_image 关键帧四带", cmd,
            "qc_image（关键帧四带不过）",
            "qc_image 参数/路径错误，**未能测量**（看上面 ERROR 行）")

    # 5) 介质信号（只告警，不阻断）
    if args.frames and not args.skip_signals:
        # qc_signals.py 要求必须给 --baseline；不给就拿被测图自己当基准，比值恒在 1
        # 附近、告警失效。无 --baseline 时明确记 NOTCHK，不用待测目录自比。
        if args.baseline:
            if Path(args.baseline).exists():
                ok, rc, _ = run("5/5 qc_signals 介质告警（不阻断）",
                                [SCRIPTS / "qc_signals.py", args.frames,
                                 "--baseline", args.baseline])
                results.append(("qc_signals", True, rc))   # 永不阻断
            else:
                results.append(("qc_signals（基准路径不存在）", True, 2))
        else:
            results.append(("qc_signals（未给 --baseline，NOTCHK）", True, 2))

    # ---- 汇总 ----
    print(f"\n{'='*66}\nPREFLIGHT 汇总\n{'='*66}")
    for name, ok, rc in results:
        tag = "PASS" if rc == 0 else ("NOTCHK" if rc == 2 else "BLOCK")
        print(f"  [{tag:6s}] {name}  (exit {rc})")
    if blockers:
        print(f"\n❌ 禁止提交，阻断项：")
        for b in blockers:
            print(f"     - {b}")
        return 1
    print(f"\n✅ 全部通过，可以提交（退出码 0）")
    return 0


if __name__ == "__main__":
    sys.exit(main())