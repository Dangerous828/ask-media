#!/usr/bin/env python3
"""segment_guard.py — 段内「黑框自溶」帧级检查（story_check 补不上的那一半）。

为什么需要这个脚本
------------------
`story_check.py` 只能在**文本层**查「同一次空间穿越被多镜重复承担」，
查不出真正的自溶——因为自溶发生在**渲染过程内部**，提示词里根本看不见。
EP01 的真事故形态：S02 写"推镜穿屏"、S03 只写"满幅"，两个文件各自都没错；
错在 S03 又穿了一遍，于是黑框在没有动机的情况下**在段内自己溶解**，
外环死黑 25.7%（文档头起始值；下表 ss03 用 p10 口径记 +31.8，两者统计口径不同，未复算）→ 17.3% → … → 0.0% 单调递减。这段视频在提示词层是"合格"的。

⇒ 只有帧级数据能证明。本脚本就是那个数据源。

判据（2026-10-22 在 EP01 实渲素材上实测标定；文档头写「25 条」，下表明细为 3+1+20=24 条，另 1 条未列入明细，未复算）
----------------------------------------------------------------------
取画面四周 6% 环带（与 qc_image 的 BORDER_RING_FRACTION 同一口径）的死黑占比，
沿时间轴画曲线。`drop = 首窗中位数 - 曲线低分位(p10，跳过尾部 10%)`：

| 素材                        | drop      | 判定     |
|-----------------------------|-----------|----------|
| ss03（真事故·自溶）         | **+31.8** | DECAY    |
| ss03（另一版）              | **+32.2** | DECAY    |
| s02_push（真事故·自溶）     | **+29.6** | DECAY    |
| ss02（推镜穿屏·正常）       | **-0.1**  | OK（递增）|
| 其余 20 条正常镜            | **≤0.5**  | OK       |

**关键：只有「递减」才是自溶。** 外环死黑**递增**是合法的「边框被推入画」，
ss02/s02_push 的设计就是推镜进屏幕，drop 不涨反跌，绝不能拦。
把「有变化」当门控会误杀正常推镜——这是本篇最容易写错的地方。

为什么用低分位而不是「尾窗」：初版用尾窗中位数，在「真事故 + 尾部淡出到黑」
的合成反例上 drop 变成 -68.3（尾部 100% 黑把 tail 抬高），**假阴性漏判**。
改取曲线 p10 并跳过尾部 10%，该样本回到 +27.0（正确报警），
正常镜最大仍只有 0.5 —— 分离度从 9 倍提到 54 倍。

阈值取 `DECAY_MIN = 8.0%`。另加「单调性」判据：真事故外环曲线下跌帧数远超上涨帧数
（45 down / 12 up），用来把「单帧闪黑（黑场转场/瞬间遮挡）」与「持续溶解」区分开。

### 第二条判据：必须是「只有环带在变」（fade-in 误报的修法）

单靠 drop 会把**淡入**判成自溶。实测合成反例 `fade=t=in:d=1.5`：

| 素材            | 外环 drop | 内区 drop | 判定              |
|-----------------|-----------|-----------|-------------------|
| 合成 fade-in    | **+53.4** | **+51.8** | 整帧都在变 → 放行 |
| ss03（真自溶）  | **+31.8** | **+2.1**  | 只有环带在变 → 拦 |

淡入时整帧从黑起亮，外环与内区**同步**下降；黑框自溶是**局部几何**事件，
内区亮度基本不动。故加 `RING_OVER_INNER_MIN = 8.0`：
要求 `外环 drop - 内区 drop >= 8`。

正常镜该差值实测最大 2.7（ss07），事故为 29.7 / 30.3，仍有 3.5 倍余量。

已知边界（别当成完备门控）
--------------------------
- 只查**外环**。内区自溶（满幅画面中物体自己消失）不在本判据内。
- 环带比例固定 6%，与 qc_image 一致；画面本身就是「窗口套窗口」时，
  外环可能始终有遮挡，此时 head/tail 都高，drop 小 → 不告警（这是对的，不是漏判）。
- 判的是**几何占位**，不是「这个溶解是否有动机」。创意上真要黑框慢慢出画
  （例如合法地从屏内**拉出**去），用 `--allow-decay` 显式放行，并在项目文档写明理由。
  ⇒ 本判据**无法**区分「非法自溶」与「合法地把黑框拉出画面」，二者几何同形。
  这是不可消除的边界，靠 allow-decay 与人工复核承担。
- 成片（多镜拼接）也能跑，但镜间接缝处的死黑跳变会污染曲线；
  只在逐段（单段一条文件）模式下结论可信。

用法
----
    # 单段
    python3 segment_guard.py seg.mp4
    # 整目录（每条独立判）
    python3 segment_guard.py <视频目录>
    # 创意上允许黑框自己出画（只豁免 DECAY；帧数不足的 NOTCHK 仍阻断）
    python3 segment_guard.py seg.mp4 --allow-decay
    python3 segment_guard.py <目录> --json

退出码
------
    0  无自溶
    1  检出自溶（DECAY）
    2  参数错误 / 读不到视频 / NOTCHK（帧数不足或解码为空，--allow-decay 不豁免）
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

# 与 qc_image.BORDER_RING_FRACTION 保持同一口径
BORDER_RING_FRACTION = 0.06
# 死黑亮度阈值，与 qc_image 一致（gray < 16）
DEAD_THR = 16
# 解码尺寸：只需几何占比，320x180 足够且快
DECODE_W, DECODE_H = 320, 180

# 判定阈值（实测标定，见模块 docstring 的表）
DECAY_MIN = 8.0            # 外环 head - p10 超过它才算「溶解」（事故 27.0+ / 正常 ≤0.5）
RING_OVER_INNER_MIN = 8.0  # 外环 drop 相对内区 drop 的超额（过滤整帧淡入淡出）
HEAD_TAIL_FRAMES = 10      # 首窗取多少帧的中位数
LOW_PCTL = 10.0            # 低分位：替代尾窗，避免尾部淡出把 tail 抬高造成假阴性
TAIL_SKIP_FRACTION = 0.10  # 算低分位时跳过尾部比例（淡出/黑场常落在这里）
MONO_DOWN_MIN = 2.0        # 下跌帧数 / 上涨帧数 下限（事故 3.75–3.93 / 正常 ≈1）
MIN_FRAMES = 12            # 帧数太少的段不做结论


def _frames(path: Path):
    """解成灰度小图序列。fps_mode passthrough 防 vaapi 补帧导致序号偏移。"""
    cmd = ["ffmpeg", "-v", "error", "-i", str(path),
           "-vf", "scale=%d:%d" % (DECODE_W, DECODE_H),
           "-fps_mode", "passthrough",
           "-f", "rawvideo", "-pix_fmt", "gray", "-"]
    raw = subprocess.run(cmd, capture_output=True, check=True).stdout
    n = len(raw) // (DECODE_W * DECODE_H)
    if n == 0:
        return None
    return np.frombuffer(raw[:n * DECODE_W * DECODE_H],
                         dtype=np.uint8).reshape(n, DECODE_H, DECODE_W)


def _ring_mask(h: int, w: int, frac: float = BORDER_RING_FRACTION):
    m = np.zeros((h, w), dtype=bool)
    band = max(1, int(min(h, w) * frac))
    m[:band, :] = True
    m[-band:, :] = True
    m[:, :band] = True
    m[:, -band:] = True
    return m


def analyse(path: Path) -> dict:
    fr = _frames(path)
    if fr is None or fr.shape[0] < MIN_FRAMES:
        return {"path": str(path), "ok": False, "skip": "帧数不足或解码为空",
                "frames": 0 if fr is None else int(fr.shape[0])}

    n = fr.shape[0]
    flat = fr.reshape(n, -1)
    ring = _ring_mask(*fr.shape[1:]).ravel()
    dead = flat < DEAD_THR
    # 外环与内区各画一条死黑曲线。判自溶要两条一起看（见 docstring 第二条判据）。
    curve = dead[:, ring].mean(axis=1) * 100.0
    inner = dead[:, ~ring].mean(axis=1) * 100.0

    k = min(HEAD_TAIL_FRAMES, max(3, n // 6))
    # 首窗中位数 vs 低分位。不用尾窗：尾部淡出到黑会把 tail 抬到 100%，
    # 使真事故的 drop 变负而漏判（合成反例 decay_fadeout 实测 -68.3）。
    body_end = max(k, int(n * (1.0 - TAIL_SKIP_FRACTION)))
    head = float(np.median(curve[:k]))
    low = float(np.percentile(curve[:body_end], LOW_PCTL))
    i_head = float(np.median(inner[:k]))
    i_low = float(np.percentile(inner[:body_end], LOW_PCTL))
    drop = head - low
    inner_drop = i_head - i_low
    excess = drop - inner_drop
    d = np.diff(curve)
    down = int((d < -0.05).sum())
    up = int((d > 0.05).sum())
    mono = (down / float(up)) if up else float(down)

    decay = (drop >= DECAY_MIN and mono >= MONO_DOWN_MIN
             and excess >= RING_OVER_INNER_MIN)
    # 只下结论不解释原因，原因留给报告层拼（便于 --json 消费）
    reason = ""
    if drop >= DECAY_MIN and mono >= MONO_DOWN_MIN and excess < RING_OVER_INNER_MIN:
        reason = "整帧同步变暗（疑似淡入淡出，非局部自溶）"
    return {
        "path": str(path),
        "frames": n,
        "ring_head": round(head, 2),
        "ring_low": round(low, 2),
        "ring_max": round(float(curve.max()), 2),
        "ring_min": round(float(curve.min()), 2),
        "inner_head": round(i_head, 2),
        "inner_low": round(i_low, 2),
        "drop": round(drop, 2),
        "inner_drop": round(inner_drop, 2),
        "excess": round(excess, 2),
        "mono_down": round(mono, 2),
        "down_frames": down,
        "up_frames": up,
        "decay": bool(decay),
        "note": reason,
        "ok": True,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="段内黑框自溶帧级检查")
    ap.add_argument("targets", nargs="+", help="视频文件或目录")
    ap.add_argument("--allow-decay", action="store_true",
                    help="创意上允许黑框在段内自己出画：只豁免 DECAY，NOTCHK（帧数不足/解码为空）仍阻断")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    args = ap.parse_args()

    files = []
    for t in args.targets:
        p = Path(t)
        if p.is_dir():
            files += sorted(p.glob("*.mp4")) + sorted(p.glob("*.mov")) + sorted(p.glob("*.mkv"))
        elif p.is_file():
            files.append(p)
        else:
            print("ERROR: 找不到 %s" % t, file=sys.stderr)
            return 2
    if not files:
        print("ERROR: 没有可查的视频", file=sys.stderr)
        return 2

    reports = []
    bad = []
    notchecked = []   # 帧数不足/解不出：与 preflight 的 NOTCHK 哲学一致，未查成不能当通过
    for f in files:
        try:
            r = analyse(f)
        except subprocess.CalledProcessError as e:
            print("ERROR: ffmpeg 解不了 %s: %s" % (f, e), file=sys.stderr)
            return 2
        reports.append(r)
        if not r.get("ok"):
            notchecked.append(r["path"])
        if r.get("ok") and r["decay"]:
            bad.append(r)

    if args.json:
        print(json.dumps({"reports": reports,
                          "decay": [r["path"] for r in bad],
                          "notchecked": notchecked,
                          "allow_decay": args.allow_decay},
                         ensure_ascii=False, indent=1))
    else:
        print("=" * 84)
        print("段内黑框自溶检查（外环 %.0f%% 带 · 死黑 < %d）"
              % (BORDER_RING_FRACTION * 100, DEAD_THR))
        print("判据：外环 drop >= %.1f%% 且 下跌帧/上涨帧 >= %.1f 且 (外环-内区) drop >= %.1f%%"
              % (DECAY_MIN, MONO_DOWN_MIN, RING_OVER_INNER_MIN))
        print("=" * 84)
        print("%-40s %5s %7s %7s %7s %7s %6s  %s"
              % ("file", "n", "ring_h", "ring_lo", "drop", "excess", "mono", "verdict"))
        for r in reports:
            if not r.get("ok"):
                print("%-40s  SKIP  %s" % (Path(r["path"]).name[:40], r.get("skip")))
                continue
            tag = "DECAY" if r["decay"] else "ok"
            if r.get("note"):
                tag = "ok(淡入淡出)"
            print("%-40s %5d %7.2f %7.2f %7.2f %7.2f %6.2f  %s"
                  % (Path(r["path"]).name[:40], r["frames"], r["ring_head"],
                     r["ring_low"], r["drop"], r["excess"], r["mono_down"], tag))
        print("-" * 84)
        if bad:
            print("检出段内黑框自溶 %d 条：" % len(bad))
            for r in bad:
                print("  · %s  外环死黑 %.1f%% → %.1f%%（内区仅 %.1f%% → %.1f%%，"
                      "只有环带在变）"
                      % (Path(r["path"]).name, r["ring_head"], r["ring_low"],
                         r["inner_head"], r["inner_low"]))
            print("  含义：黑框在段内无动机地自己消失 —— 常见根因是"
                  "「同一次空间穿越被相邻两镜重复承担」。")
            print("  注意：本判据无法区分「非法自溶」与「合法地把黑框拉出画面」，"
                  "二者几何同形。")
            if args.allow_decay:
                print("  --allow-decay 已开启：仅报告，不阻断。")
        else:
            print("未检出段内黑框自溶。")
        if notchecked:
            print("NOTCHK %d 条未查成（帧数不足/解码为空）：%s"
                  % (len(notchecked), ", ".join(Path(p).name for p in notchecked)))

    # --allow-decay 只豁免「衰减类」检查：创意上允许黑框自己出画。
    # NOTCHK（帧数不足/解码为空）是「没查成」，不能当通过，任何 flag 下都阻断（exit 2）。
    if bad and not args.allow_decay:
        return 1
    if notchecked:
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
