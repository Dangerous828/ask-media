#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""逐镜运动曲线 / 切点连续性体检

用途：在判断"画面不连贯"的原因时，先量运动，再量色彩。
生成素材最常见的病是**头尾静止（起步-刹车）**，而不是色彩不接。

用法:
    python3 check_motion.py <目录或文件...> [--threshold 0.5] [--json out.json]

示例:
    python3 check_motion.py videos_v1/            # 目录下所有 mp4
    python3 check_motion.py s1.mp4 s2.mp4         # 指定文件
    python3 check_motion.py 成片.mp4 --cuts 5.88,10.33   # 检查成片切点

退出码：0 正常测完；2 输入错误（文件不存在/目录里没有 mp4/整段解不出帧）。
没有任何一段测成时绝不输出 0：0/0 镜的"全绿"是本工具最危险的输出。
"""

import sys, os, json, glob, argparse, subprocess

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("check_motion.py requires Python 3.9 or newer")

import numpy as np

SW, SH = 64, 112   # 分析降采样尺寸


def gray_seq(path):
    d = subprocess.run(["ffmpeg", "-v", "error", "-i", path,
                        "-vf", f"scale={SW}:{SH}", "-f", "rawvideo", "-pix_fmt", "gray", "-"],
                       capture_output=True).stdout
    n = len(d) // (SW * SH)
    if n < 2:
        return None
    return np.frombuffer(d[:n * SW * SH], np.uint8).reshape(n, SW * SH).astype(np.float32)


def motion_curve(frames):
    """相邻帧差 = 运动量"""
    return np.abs(np.diff(frames, axis=0)).mean(axis=1)


def shot_report(path, thr=0.5):
    fr = gray_seq(path)
    if fr is None:
        return None
    diff = motion_curve(fr)
    n = len(diff)
    head = float(diff[:7].mean()) if n >= 7 else float(diff.mean())
    mid = float(diff[n // 2 - 4:n // 2 + 4].mean()) if n >= 8 else float(diff.mean())
    tail = float(diff[-7:].mean()) if n >= 7 else float(diff.mean())
    hr = head / max(mid, 1e-3)
    tr = tail / max(mid, 1e-3)
    return dict(file=os.path.basename(path), frames=len(fr),
                head=head, mid=mid, tail=tail,
                head_ratio=round(hr, 2), tail_ratio=round(tr, 2),
                head_brake=hr < thr, tail_brake=tr < thr)


def cut_report(path, cuts, skip=0.30):
    """切点两侧运动量：跳过转场内部，比较前后窗口的平均运动"""
    fr = gray_seq(path)
    if fr is None:
        return []
    fps = 24.0
    d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=r_frame_rate",
                        "-of", "csv=p=0", path], capture_output=True, text=True).stdout.strip()
    d = d.splitlines()[0].strip() if d else ""
    if "/" in d:
        parts = d.split("/")
        if len(parts) == 2:
            a, b = parts
            try:
                if float(b) > 0:
                    fps = float(a) / float(b)
            except ValueError:
                pass
    diff = motion_curve(fr)
    rows = []
    w = int(0.25 * fps)
    for c in cuts:
        i = int(c * fps)
        a0, a1 = max(0, i - int(skip * fps) - w), max(1, i - int(skip * fps))
        b0, b1 = min(len(diff), i + int(skip * fps)), min(len(diff), i + int(skip * fps) + w)
        if a1 <= a0 or b1 <= b0:
            continue
        ma = float(diff[a0:a1].mean())
        mb = float(diff[b0:b1].mean())
        rows.append(dict(cut=round(c, 2), motion_before=round(ma, 3),
                         motion_after=round(mb, 3),
                         both_still=(ma < 0.5 and mb < 0.5),
                         ratio=round(mb / max(ma, 1e-3), 2)))
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--threshold", type=float, default=0.5)
    ap.add_argument("--cuts", type=str, default=None, help="逗号分隔的切点秒数（检查成片时用）")
    ap.add_argument("--json", type=str, default=None)
    args = ap.parse_args()

    files = []
    for p in args.paths:
        if os.path.isdir(p):
            files += sorted(glob.glob(os.path.join(p, "*.mp4")))
        else:
            files.append(p)

    # 输入错误必须显式失败：不存在的文件、空目录、目录下没有 mp4，
    # 以前全部落进"0/0 镜有头尾刹车"的 0 退出码，把没测读成全绿。
    missing = [p for p in files if not os.path.isfile(p)]
    if missing:
        print(f"NOT_EVALUATED: 文件不存在：" + "，".join(missing), file=sys.stderr)
        return 2
    if not files:
        print("NOT_EVALUATED: 目录下没有 mp4：" + "，".join(args.paths), file=sys.stderr)
        return 2

    result = {"shots": [], "cuts": []}

    if args.cuts:
        cuts = [float(x) for x in args.cuts.split(",") if x.strip()]
        rows = cut_report(files[0], cuts)
        if not rows:
            print(f"NOT_EVALUATED: {os.path.basename(files[0])} 解不出帧或全部切点越界，切点两侧运动未测",
                  file=sys.stderr)
            return 2
        result["cuts"] = rows
        print(f"=== 切点运动检查: {os.path.basename(files[0])}")
        print(f"{'切点':>7} {'前运动':>8} {'后运动':>8} {'比值':>6} 判定")
        for r in result["cuts"]:
            mark = "⚠️ 两侧都静止" if r["both_still"] else ("⚠️ 差 3 倍以上" if (r["ratio"] > 3 or r["ratio"] < 0.33) else "✓")
            print(f"{r['cut']:7.2f} {r['motion_before']:8.3f} {r['motion_after']:8.3f} {r['ratio']:6.2f} {mark}")
    else:
        unmeasured = []
        print(f"=== 逐镜运动曲线（阈值 {args.threshold}）")
        print(f"{'文件':>22} {'帧':>5} {'头':>6} {'中':>6} {'尾':>6} {'头/中':>6} {'尾/中':>6} 判定")
        for f in files:
            r = shot_report(f, args.threshold)
            if not r:
                unmeasured.append(os.path.basename(f))
                continue
            result["shots"].append(r)
            bad = []
            if r["head_brake"]:
                bad.append("头刹车")
            if r["tail_brake"]:
                bad.append("尾刹车")
            mark = "⚠️ " + "/".join(bad) if bad else "✓"
            print(f"{r['file']:>22} {r['frames']:5d} {r['head']:6.2f} {r['mid']:6.2f} {r['tail']:6.2f} "
                  f"{r['head_ratio']:6.2f} {r['tail_ratio']:6.2f} {mark}")
        if unmeasured:
            print(f"NOT_EVALUATED（解不出帧，未测）：" + "、".join(unmeasured), file=sys.stderr)
        nbad = sum(1 for r in result["shots"] if r["head_brake"] or r["tail_brake"])
        print(f"\n{nbad}/{len(result['shots'])} 镜有头尾刹车")
        if unmeasured:
            print(f"未测 {len(unmeasured)}/{len(files)} 段", file=sys.stderr)
        if not result["shots"]:
            # 一段都没测成：退出码 2，绝不输出 0/0 的全绿。
            return 2

    if args.json:
        json.dump(result, open(args.json, "w"), ensure_ascii=False, indent=2)
        print(f"\n已写入 {args.json}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
