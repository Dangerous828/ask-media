#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""接缝取证：把相邻两段的真实末帧与真实首帧并排摆出来，并量出差异在哪里。

这个脚本**不下判断**。它只做三件人做不到的事：

1. 从视频里取到**真实末帧**（不是倒数第二帧、不是首帧）；末帧取错，整套比对就是假的；
2. 把前段末帧与后段首帧拼成一张可直接打开看的并排图；
3. 输出几个能把「哪里变了」定位到画面区域的数字，让人带着坐标去看，而不是盯着整帧猜。

为什么不能只看一个总分：整帧平均差会把「桌面换了木色」和「吊灯挪了位置」平均成一个数，
两个都不像；而真正要判断的是**同一个人、同一空间、同一造型、同一道具**这四件事各自有没有变。
所以这里给的是分区域、分频段的数字，判断仍然由人做完。

用法:

    # 两段相邻视频（最常用）
    python3 seam_check.py --before <a.mp4> --after <b.mp4> --out 审查/seam/<标签>

    # 也可直接给两张已取好的帧
    python3 seam_check.py --before <末帧.png> --after <首帧.png> --out ...

    # 只想取帧、自己拼
    python3 seam_check.py --extract <video> --frame last --out <png>

产物（全部写进 --out 目录，不覆盖已有文件）：

    <label>-before-end.png     前段真实末帧
    <label>-after-start.png    后段真实首帧
    <label>-side-by-side.jpg   并排图，左上角标注文件名与帧号
    <label>-grid.jpg           4x3 网格热图，标出差异落在哪些区域
    <label>-seam.json          全部指标与取帧来源，供写进《视频提示词.md》的接缝契约

退出码：0 = 取证完成；2 = 参数/文件/ffmpeg 问题（**不代表接缝不合格**）。

读数字的方法见 `references/seam-transition.md` 的「量差异」一节；本脚本不替你做取舍。
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit(
        "seam_check.py requires Python {}.{} or newer; this interpreter is {}.{}".format(
            *MINIMUM_PYTHON, sys.version_info.major, sys.version_info.minor
        )
    )

try:
    import numpy as np
    from PIL import Image, ImageDraw
except ImportError as error:  # pragma: no cover - depends on the host interpreter
    raise SystemExit(
        "seam_check.py needs numpy and Pillow ({error}). Install them or run the "
        "same comparison with ffmpeg + an image viewer.".format(error=error)
    )

SCHEMA = "seam-check/1"

# Analysis width for the pixel comparisons. 384 is wide enough that a plate rim
# or a pendant lamp keeps its shape and narrow enough that a 4K take is still
# cheap. Every metric below is computed at this width, so numbers from two runs
# are comparable.
ANALYSIS_WIDTH = 384

# A low-pass pass at this width keeps room layout, lamp positions and large
# colour fields while discarding grain, flyaway hair and micro-texture. That is
# exactly the band that carries "same space / same lighting"; texture noise is
# what makes an unprocessed pixel diff useless across two separate generations.
STRUCTURE_WIDTH = 12

# Region grid, rows x columns. Three rows separate ceiling light from table
# top; four columns separate the left window from the right of frame.
GRID_ROWS, GRID_COLS = 3, 4


class SeamError(ValueError):
    """The inputs cannot be measured at all, as opposed to showing a difference."""


# ---------------------------------------------------------------------------
# 取帧
# ---------------------------------------------------------------------------

def _which(tool: str) -> str:
    found = shutil.which(tool)
    if not found:
        raise SeamError(
            "需要 {tool}，当前 PATH 里没有。装好 ffmpeg 再跑；未测不等于接缝合格。".format(tool=tool)
        )
    return found


def probe(path: Path) -> dict[str, Any]:
    """读视频的帧数、时长、尺寸。拿不到 nb_frames 时返回 None，由调用方走回退路径。"""
    ffprobe = _which("ffprobe")
    argv = [
        ffprobe, "-v", "error",
        "-select_streams", "v:0",
        "-show_entries", "stream=width,height,r_frame_rate,nb_frames,duration",
        "-of", "json", str(path),
    ]
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode != 0:
        raise SeamError("ffprobe 读不了这个文件：{path}".format(path=path))
    try:
        streams = json.loads(result.stdout).get("streams") or []
    except json.JSONDecodeError as error:
        raise SeamError("ffprobe 输出无法解析：{path}".format(path=path)) from error
    if not streams:
        raise SeamError("文件里没有视频流：{path}".format(path=path))
    stream = streams[0]
    frames = stream.get("nb_frames")
    try:
        frame_count = int(frames) if frames not in (None, "N/A") else None
    except (TypeError, ValueError):
        frame_count = None
    duration = stream.get("duration")
    try:
        duration_seconds = float(duration) if duration not in (None, "N/A") else None
    except (TypeError, ValueError):
        duration_seconds = None
    # 有没有音轨单独问一次：视频流查询不会带出 audio stream。
    has_audio = False
    audio_probe = subprocess.run(
        [
            _which("ffprobe"), "-v", "error",
            "-select_streams", "a:0",
            "-show_entries", "stream=codec_type",
            "-of", "csv=p=0", str(path),
        ],
        capture_output=True, text=True,
    )
    if audio_probe.returncode == 0 and audio_probe.stdout.strip():
        has_audio = True
    return {
        "width": stream.get("width"),
        "height": stream.get("height"),
        "r_frame_rate": stream.get("r_frame_rate"),
        "frame_count": frame_count,
        "duration_seconds": duration_seconds,
        "has_audio": has_audio,
    }


def _run_ffmpeg(argv: list[str]) -> None:
    result = subprocess.run(argv, capture_output=True, text=True)
    if result.returncode != 0:
        raise SeamError(
            "ffmpeg 取帧失败：{err}".format(err=(result.stderr or "").strip()[-400:])
        )


def extract_frame(video: Path, edge: str, target: Path) -> dict[str, Any]:
    """取**真实**首帧或真实末帧，并返回这次是怎么取到的。

    末帧有两种常见错法，两种都会让整套比对失效：
      * `-sseof -1` 配 `-frames:v 1` 取到的是末段窗口里的**第一帧**，不是最后一帧；
      * 按 `duration - 1/fps` 定位，在 17k+5 帧网格上会落到倒数第二帧。
    所以这里优先按帧号取（`select=eq(n,count-1)`），只有拿不到 nb_frames 时才回退
    `-sseof` + `-update 1`（后者靠"每帧覆盖同一输出文件"留下最后一张）。
    """
    ffmpeg = _which("ffmpeg")
    info = probe(video)
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        raise SeamError("不覆盖已有文件：{target}".format(target=target))

    method: str
    index: int | None = None
    if info.get("frame_count"):
        index = 0 if edge == "first" else int(info["frame_count"]) - 1
        argv = [
            ffmpeg, "-v", "error", "-i", str(video),
            "-vf", "select=eq(n\\,{index})".format(index=index),
            "-fps_mode", "passthrough", "-frames:v", "1", "-y", str(target),
        ]
        method = "select frame index"
    else:
        if edge == "first":
            argv = [ffmpeg, "-v", "error", "-i", str(video), "-frames:v", "1", "-y", str(target)]
            method = "first frame"
        else:
            # `-update 1` rewrites the same path per frame; the survivor is the last one.
            argv = [
                ffmpeg, "-v", "error", "-sseof", "-1", "-i", str(video),
                "-update", "1", "-q:v", "2", "-y", str(target),
            ]
            method = "sseof -1 with -update 1 (frame count unknown)"
    _run_ffmpeg(argv)
    if not target.is_file():
        raise SeamError("ffmpeg 没有写出帧：{target}".format(target=target))
    return {
        "source": str(video),
        "role": edge,
        "frame_index": index,
        "method": method,
        "probe": info,
        "path": str(target),
    }


def resolve_frame(spec: str, role: str, target: Path) -> dict[str, Any]:
    """一个输入既可以是视频也可以是已经取好的帧图。

    前段要末帧、后段要首帧——这是这套比对唯一有意义的取法，所以由 role 决定取哪一端，
    不给调用方选错的机会。
    """
    path = Path(spec)
    if not path.is_file():
        raise SeamError("找不到文件：{path}".format(path=path))
    suffix = path.suffix.lower()
    if suffix in {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}:
        return {
            "source": str(path),
            "role": role,
            "frame_index": None,
            "method": "supplied still image",
            "probe": None,
            "path": str(path),
        }
    edge = "first" if role == "after_start" else "last"
    return extract_frame(path, edge, target)


# ---------------------------------------------------------------------------
# 量差异
# ---------------------------------------------------------------------------

def _load(path: Path) -> Image.Image:
    try:
        return Image.open(path).convert("RGB")
    except (OSError, ValueError) as error:
        raise SeamError("读不了图片：{path}".format(path=path)) from error


def _resized(image: Image.Image, width: int) -> np.ndarray:
    height = max(1, int(round(width * image.size[1] / image.size[0])))
    return np.asarray(image.resize((width, height), Image.LANCZOS), dtype=np.float32)


def _gradients(pixels: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    gray = pixels.mean(axis=2)
    gx = np.zeros_like(gray)
    gy = np.zeros_like(gray)
    gx[:, 1:-1] = gray[:, 2:] - gray[:, :-2]
    gy[1:-1, :] = gray[2:, :] - gray[:-2, :]
    return gx, gy


def edge_agreement(before: np.ndarray, after: np.ndarray) -> float:
    """两张图的边缘方向是否指向同一处：+1 同向，0 无关，-1 反向。

    这是判断「同一个空间」最直接的一个数：家具、灯、窗框的边界会落在同一位置、
    同一朝向。两段独立生成换了整个空间时，这个数会掉到 0 附近。
    镜头本身在剧烈运动（推、甩、环绕）时它也会自然下降，所以要和本段的段内值比。
    """
    ax, ay = _gradients(before)
    bx, by = _gradients(after)
    magnitude_a = np.hypot(ax, ay)
    magnitude_b = np.hypot(bx, by)
    weight = np.minimum(magnitude_a, magnitude_b)
    if float(weight.sum()) <= 1e-6:
        return 0.0
    cosine = (ax * bx + ay * by) / (magnitude_a * magnitude_b + 1e-6)
    return float((cosine * weight).sum() / weight.sum())


def histogram_distance(before: np.ndarray, after: np.ndarray, bins: int = 32) -> float:
    """三通道直方图的 Bhattacharyya 距离，0 = 分布相同，1 = 完全不重叠。

    它只看「色和影调的分布」，不看位置，所以能分开两类问题：
    分布差大而边缘对得上 → 布光或调色变了；两者都差 → 换了地方。
    """
    total = 0.0
    for channel in range(3):
        ha, _ = np.histogram(before[:, :, channel], bins=bins, range=(0, 255))
        hb, _ = np.histogram(after[:, :, channel], bins=bins, range=(0, 255))
        ha = ha / max(ha.sum(), 1)
        hb = hb / max(hb.sum(), 1)
        total += float(np.sqrt(ha * hb).sum())
    return 1.0 - total / 3.0


def region_table(before: Image.Image, after: Image.Image) -> list[dict[str, Any]]:
    """把画面切成 3x4 格，每格给自己那一小块的平均差。

    整帧一个数字看不出「只有桌面的木色变了」；分格之后能直接说「第 3 行第 2 格」。
    格子名用画面方位（上/中/下 × 左/中左/中右/右），写进接缝契约时不用换算坐标。
    """
    row_names = ["top", "middle", "bottom"]
    col_names = ["left", "centre-left", "centre-right", "right"]
    width, height = before.size
    out: list[dict[str, Any]] = []
    for row in range(GRID_ROWS):
        for col in range(GRID_COLS):
            box = (
                col * width // GRID_COLS,
                row * height // GRID_ROWS,
                (col + 1) * width // GRID_COLS,
                (row + 1) * height // GRID_ROWS,
            )
            a = np.asarray(before.crop(box), dtype=np.float32)
            b = np.asarray(after.crop(box), dtype=np.float32)
            if a.shape != b.shape:
                b = np.asarray(
                    Image.fromarray(b.astype(np.uint8)).resize(
                        (a.shape[1], a.shape[0]), Image.LANCZOS
                    ),
                    dtype=np.float32,
                )
            out.append({
                "row": row_names[row],
                "column": col_names[col],
                "mean_abs_diff": round(float(np.abs(a - b).mean()), 2),
            })
    return out


def luma_mean(pixels: np.ndarray) -> float:
    """Rec.601 luma mean of an RGB array (0-255).

    `luminance_mean` elsewhere in this report is the plain RGB average and
    under-reads brightness changes on warm frames, where the green channel
    carries most of the perceived brightness (midnight-cream-veil START-A to
    SEG-A: -5.1% by RGB average, -6.3% by luma).
    """
    # Explicit channel sum, not a matmul: the macOS Accelerate build of numpy
    # emits divide-by-zero/overflow RuntimeWarnings (and can return garbage) for
    # float32 matmul on large frames.
    rgb = pixels.astype(np.float64)
    return float((0.299 * rgb[..., 0] + 0.587 * rgb[..., 1] + 0.114 * rgb[..., 2]).mean())


def audio_level(video: Path, start: float, duration: float) -> dict[str, Any]:
    """量一个时间窗内的平均电平（dBFS）。用于看切点两侧的声音接不接得上。

    画面接缝能靠并排图看，声音不行——听要反复倒带，而且笔记本喇叭常听不出来。
    这里只报数：切点前 0.3 秒 vs 切点后 0.3 秒，两个数差多少。
    人耳约 3 dB 可察觉、10 dB 明显变响；两个数差很多时，观众听到的是"突然大了一截"。
    """
    ffmpeg = _which("ffmpeg")
    if ffmpeg is None:
        return {"note": "没有 ffmpeg，跳过音频"}
    if not probe(video).get("has_audio"):
        return {"note": "这段没有音轨"}
    with tempfile.TemporaryDirectory(prefix="seam-check-audio-") as scratch:
        out = Path(scratch) / "w.wav"
        _run_ffmpeg([
            ffmpeg, "-y", "-v", "error",
            "-ss", "%.3f" % max(start, 0.0), "-t", "%.3f" % duration,
            "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(out),
        ])
        if not out.exists() or out.stat().st_size < 64:
            return {"note": "取样窗内没有音频数据"}
        try:
            import wave, struct, math
            with wave.open(str(out)) as handle:
                raw = handle.readframes(handle.getnframes())
            if len(raw) < 2:
                return {"note": "取样窗太短"}
            samples = struct.unpack("<%dh" % (len(raw) // 2), raw)
            rms = math.sqrt(sum(float(x) * x for x in samples) / len(samples))
            db = 20.0 * math.log10(max(rms, 1.0) / 32768.0)
            return {"dbfs": round(db, 1), "window_s": round(duration, 2)}
        except Exception as error:  # noqa: BLE001 - 取证失败不该让整次检查挂掉
            return {"note": "读不到 PCM：%s" % error}


def audio_onset(video: Path, scan: float = 1.5, window: float = 0.05) -> dict[str, Any]:
    """看这一段**自己的开场**有没有爆一下。

    每段独立生成时，声音的起点不继承上一段：模型常在最开头甩一个短促的冲击
    （撞击/气音/"啊"一声），然后才进入正常底噪。观众听到的是"一开场吓一跳"，
    和画面接不接得上无关——所以这个检查对单段也成立，不需要相邻两段。

    2026-11-07 EP002 实测：16 段里 4 段在开场 1.5 秒内超过 -12 dBFS，
    最狠的两段直接从近乎静音跳到 0.0 dBFS（满刻度），0.25 秒后掉到 -45 dBFS。
    """
    ffmpeg = _which("ffmpeg")
    if ffmpeg is None:
        return {"note": "没有 ffmpeg，跳过"}
    if not probe(video).get("has_audio"):
        return {"note": "这段没有音轨"}
    with tempfile.TemporaryDirectory(prefix="seam-check-onset-") as scratch:
        out = Path(scratch) / "w.wav"
        _run_ffmpeg([
            ffmpeg, "-y", "-v", "error", "-t", "%.2f" % scan,
            "-i", str(video), "-vn", "-ac", "1", "-ar", "16000", str(out),
        ])
        if not out.exists() or out.stat().st_size < 64:
            return {"note": "取不到开场音频"}
        try:
            import wave, struct, math
            with wave.open(str(out)) as handle:
                raw = handle.readframes(handle.getnframes())
            if len(raw) < 2:
                return {"note": "开场音频太短"}
            samples = struct.unpack("<%dh" % (len(raw) // 2), raw)
            step = max(int(16000 * window), 1)
            envelope = []
            for i in range(0, len(samples) - step, step):
                chunk = samples[i:i + step]
                rms = math.sqrt(sum(float(x) * x for x in chunk) / len(chunk))
                envelope.append(round(20.0 * math.log10(max(rms, 1.0) / 32768.0), 1))
        except Exception as error:  # noqa: BLE001
            return {"note": "读不到 PCM：%s" % error}
    if not envelope:
        return {"note": "开场音频太短"}
    peak = max(envelope)
    at = round(envelope.index(peak) * window, 2)
    head = envelope[0]
    # 开场是不是"一上来就在响"。这是观众真正听成"啊一声"的那种：
    # 第 0 秒就在高峰值，几百毫秒内又掉下去，然后真正的戏才开始。
    opening_loud = head > -12
    # 从第 0 秒到峰值后 0.3 秒的落差
    later_index = min(envelope.index(peak) + int(0.3 / window), len(envelope) - 1)
    drop = round(peak - envelope[later_index], 1)
    # 掉下去之后又回升：说明开场的响是独立的，不属于戏里的声音
    tail_max = max(envelope[later_index:]) if envelope[later_index:] else peak
    rebound = round(tail_max - envelope[later_index], 1)
    record: dict[str, Any] = {
        "head_dbfs": head,
        "peak_dbfs": peak,
        "peak_at_s": at,
        "drop_after_peak_db": drop,
        "rebound_after_drop_db": rebound,
        "envelope_dbfs": envelope,
    }
    # 009/014 的形态：第 0 秒就在 -6 dB，0.3 秒后掉到 -45，1.0 秒又回来。
    # 用「峰值后 0.3 秒」做窗口会漏掉它（峰值恰在第 0 秒、恰好 0.3 秒才掉完）。
    # 所以真正要问的是：开场这段响，之后有没有掉下去过（随后又回升不算事）。
    after_head_index = min(int(0.35 / window), len(envelope) - 1)
    trough_after_head = min(envelope[after_head_index:]) if envelope[after_head_index:] else head
    fall_from_head = round(head - trough_after_head, 1)
    record["fall_from_head_db"] = fall_from_head
    if opening_loud and fall_from_head > 15:
        record["verdict"] = "opening_pop"
        record["hint"] = (
            "第 0 秒就在响，随后掉下去——这就是观众听到的'一开场突然啊一声'。"
            "这段的戏其实在掉下去之后才开始。"
            "处理：剪辑层从冲击之后起用，或段首 0.2–0.4 秒淡入；"
            "写词时把开场第一声写成持续音（底噪/雨声/引擎怠速），不要用动作音起手。"
        )
    elif peak > -12 and drop > 15:
        record["verdict"] = "transient_pop"
        record["hint"] = (
            "段内有个短促冲击（不一定在第 0 秒），峰值高、很快掉下去。"
            "处理：剪辑层避开或淡入；写词时把这一声写成持续音。"
        )
    elif opening_loud:
        record["verdict"] = "loud_onset"
        record["hint"] = "开场偏响但没有立刻掉下去。建议段首淡入 0.2 秒。"
    else:
        record["verdict"] = "ok"
        record["hint"] = "开场电平正常，没有冲击。"
    return record


def audio_seam(before: Path, after: Path, window: float = 0.3) -> dict[str, Any]:
    """切点前后的电平差。差得大说明声音在切点处跳了。"""
    info_b = probe(before)
    duration = info_b.get("duration_seconds") or 0.0
    tail = audio_level(before, max(duration - window, 0.0), window)
    head = audio_level(after, 0.0, window)
    record: dict[str, Any] = {"before_tail": tail, "after_head": head, "window_s": window}
    if "dbfs" in tail and "dbfs" in head:
        delta = round(abs(tail["dbfs"] - head["dbfs"]), 1)
        record["delta_db"] = delta
        if delta < 3:
            record["hint"] = "两侧电平接近，切点听不出音量跳变。"
        elif delta < 10:
            record["hint"] = "有明显电平差但不算突兀，可用 0.3 秒声音交叉淡化处理。"
        else:
            record["hint"] = (
                "切点电平差很大，观众会听到声音突然变大或变小。"
                "先查是不是一段带对白、另一段是环境声；"
                "这一刀若本来要连续，应在写词时用 <scenetrans> 加官方四个连续性短语"
                "（continues seamlessly across the cut / continues uninterrupted into the next shot / "
                "carries over from the previous shot / remains audible across the transition），"
                "并在剪辑层做声音桥。"
            )
    else:
        record["hint"] = "至少一侧取不到电平（无音轨或静音），只能靠听。"
    return record


def within_shot_envelope(video: Path, sample_limit: int = 240) -> dict[str, Any]:
    """量这一段**自己内部**的相邻帧差，作为「这一段的运动量基线」。

    绝对阈值没有意义：一段固定机位的对话戏，段内相邻帧差只有约 1；一段推镜加甩镜
    的段落可以到 5 以上。接缝差只有和**它前后两段各自的段内差**比，才知道大不大。
    这里只取前 sample_limit 帧，够看运动量级，不追求全片统计。
    """
    ffmpeg = _which("ffmpeg")
    info = probe(video)
    total = info.get("frame_count")
    limit = min(int(total), sample_limit) if total else sample_limit
    frames: list[np.ndarray] = []
    # Write frames to a scratch directory instead of a pipe: PNG frames read back
    # from a pipe silently repeat the first image in some Pillow builds, which
    # would report a motionless shot and make a real jump look acceptable.
    with tempfile.TemporaryDirectory(prefix="seam-check-envelope-") as scratch:
        pattern = str(Path(scratch) / "frame_%05d.png")
        argv = [
            ffmpeg, "-v", "error", "-i", str(video),
            "-vf", "select=lt(n\\,{limit}),scale={width}:-2".format(
                limit=limit, width=ANALYSIS_WIDTH
            ),
            "-fps_mode", "passthrough", "-y", pattern,
        ]
        result = subprocess.run(argv, capture_output=True, text=True)
        if result.returncode != 0:
            raise SeamError(
                "段内基线取样失败：{err}".format(
                    err=(result.stderr or "").strip()[-300:]
                )
            )
        for path in sorted(Path(scratch).glob("frame_*.png"))[:limit]:
            frames.append(np.asarray(Image.open(path).convert("RGB"), dtype=np.float32))
    if len(frames) < 2:
        return {"frames_sampled": len(frames), "note": "段内可比的帧少于两帧，段内基线不可用"}
    structure = np.array([
        float(np.abs(_resized_array(frames[i], STRUCTURE_WIDTH)
                     - _resized_array(frames[i + 1], STRUCTURE_WIDTH)).mean())
        for i in range(len(frames) - 1)
    ])
    edges = np.array([
        edge_agreement(frames[i], frames[i + 1]) for i in range(len(frames) - 1)
    ])
    lumas = [luma_mean(frame) for frame in frames]
    return {
        "frames_sampled": len(frames),
        "luma_first": round(lumas[0], 1),
        "luma_last_sampled": round(lumas[-1], 1),
        "luma_min": round(min(lumas), 1),
        "luma_max": round(max(lumas), 1),
        "luma_note": "段内取样走 scale 滤镜（BT.601 矩阵），与 luma_mean 相差约 1；luma_* 只在这一段内部比较起伏，不要与 luma_mean 相减。",
        "structure_mad_median": round(float(np.median(structure)), 2),
        "structure_mad_p95": round(float(np.percentile(structure, 95)), 2),
        # The denominator for a seam. A seam is a single frame-to-frame step, so
        # the honest comparison is the largest single step this shot already
        # makes — not how far the shot drifts from its own first frame. A slow
        # push can drift 47 while never stepping more than 1.4, and using drift
        # as the denominator turns a real hard cut into a sub-1x ratio.
        "structure_mad_max_step": round(float(structure.max()), 2),
        "edge_agreement_min": round(float(edges.min()), 3),
        "edge_agreement_median": round(float(np.median(edges)), 3),
        "note": (
            "这是这一段自己内部的相邻帧差。接缝的 structure_mad 要和 structure_mad_max_step 比："
            "接缝本身就是一个单帧阶跃，天然应当落在段内单帧阶跃的量级附近。"
            "不要用首末漂移当分母——持续推镜的段首末能差很多，会把真接缝除成 1 倍以下。"
        ),
    }


def _resized_array(pixels: np.ndarray, width: int) -> np.ndarray:
    image = Image.fromarray(pixels.astype(np.uint8))
    return _resized(image, width)


# ---------------------------------------------------------------------------
# 出图
# ---------------------------------------------------------------------------

def side_by_side(before: Image.Image, after: Image.Image, labels: tuple[str, str],
                 target: Path) -> None:
    """并排图，两幅同高、带标签。判断「同一个人」只能靠这张图。"""
    height = 960
    widths = [max(1, int(round(height * image.size[0] / image.size[1]))) for image in (before, after)]
    gap = 16
    header = 34
    canvas = Image.new("RGB", (sum(widths) + gap, height + header), (10, 10, 10))
    canvas.paste(before.resize((widths[0], height), Image.LANCZOS), (0, header))
    canvas.paste(after.resize((widths[1], height), Image.LANCZOS), (widths[0] + gap, header))
    draw = ImageDraw.Draw(canvas)
    draw.text((6, 10), labels[0], fill=(255, 255, 255))
    draw.text((widths[0] + gap + 6, 10), labels[1], fill=(255, 255, 255))
    target.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(target, quality=92)


def grid_image(before: Image.Image, after: Image.Image, regions: list[dict[str, Any]],
               target: Path) -> None:
    """把每格的平均差涂成热图叠在后段首帧上，让「哪里变了」有坐标。

    每一格同时给三样东西：数值、方位名（`top-left` 等，写进接缝契约时不用换算坐标）、
    以及按深浅着色的覆盖层。热图做成两张并排：左是后段首帧（叠了格线与数值），
    右是纯色阶版的差异图。深色夜景里半透明红盖几乎看不出来，只给叠图会让人误以为两帧一致。
    """
    peak = max([region["mean_abs_diff"] for region in regions] + [1.0])
    overlay = after.convert("RGB").copy()
    draw = ImageDraw.Draw(overlay, "RGBA")
    width, height = overlay.size
    heat = Image.new("RGB", after.size, (0, 0, 0))
    heat_draw = ImageDraw.Draw(heat)
    for region in regions:
        row = ["top", "middle", "bottom"].index(region["row"])
        col = ["left", "centre-left", "centre-right", "right"].index(region["column"])
        box = (
            col * width // GRID_COLS,
            row * height // GRID_ROWS,
            (col + 1) * width // GRID_COLS,
            (row + 1) * height // GRID_ROWS,
        )
        strength = min(1.0, region["mean_abs_diff"] / peak)
        # Enough tint to read on a 30-luma night frame, light enough that the
        # frame underneath is still identifiable — the point is "this region
        # changed", and the eye has to be able to say what changed.
        draw.rectangle(box, fill=(255, 64, 32, int(40 + 80 * strength)))
        draw.rectangle(box, outline=(255, 255, 255, 200), width=3)
        draw.text(
            (box[0] + 10, box[1] + 10),
            "{value:.0f}".format(value=region["mean_abs_diff"]),
            fill=(255, 255, 255, 255),
        )
        draw.text(
            (box[0] + 10, box[1] + 30),
            "{row}-{col}".format(row=region["row"], col=region["column"]),
            fill=(255, 255, 255, 230),
        )
        level = int(255 * strength)
        heat_draw.rectangle(box, fill=(level, level // 3, 0))
        heat_draw.rectangle(box, outline=(255, 255, 255), width=2)
        heat_draw.text(
            (box[0] + 10, box[1] + 10),
            "{row}-{col}  {value:.0f}".format(
                row=region["row"], col=region["column"], value=region["mean_abs_diff"]
            ),
            fill=(255, 255, 255),
        )

    gap = 16
    header = 34
    combined = Image.new("RGB", (width * 2 + gap, height + header), (10, 10, 10))
    combined.paste(overlay, (0, header))
    combined.paste(heat, (width + gap, header))
    title = ImageDraw.Draw(combined)
    title.text((6, 10), "after-frame with diff grid", fill=(255, 255, 255))
    title.text((width + gap + 6, 10), "diff level (bright = more change)", fill=(255, 255, 255))
    target.parent.mkdir(parents=True, exist_ok=True)
    combined.save(target, quality=92)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="seam_check.py",
        description=(
            "并排前段真实末帧与后段真实首帧，并量出差异落在哪些区域。"
            "只出证据，不下接缝合格与否的判断。"
        ),
    )
    parser.add_argument("--before", help="前段：视频或已取好的末帧图")
    parser.add_argument("--after", help="后段：视频或已取好的首帧图")
    parser.add_argument("--out", help="输出目录；省略时写在两文件所在目录下")
    parser.add_argument("--label", help="产物文件名前缀，省略时按输入文件名生成")
    parser.add_argument(
        "--extract", help="只取帧：给一个视频，把真实首帧或末帧写到 --to"
    )
    parser.add_argument("--frame", choices=["first", "last"], default="last",
                        help="配合 --extract 使用，默认末帧")
    parser.add_argument("--to", help="配合 --extract 使用的输出图片路径")
    parser.add_argument("--no-envelope", action="store_true",
                        help="跳过段内运动量基线（视频很大时省时间）")
    parser.add_argument("--no-audio", action="store_true",
                        help="跳过切点两侧的电平比对（无音轨的项目可省这一步）")
    return parser


def _safe_label(text: str) -> str:
    keep = [character if (character.isalnum() or character in "-_") else "-" for character in text]
    slug = "".join(keep).strip("-")
    return slug or "seam"


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.extract:
        if not args.to:
            parser.error("--extract 需要配合 --to <输出图片路径>")
        record = extract_frame(Path(args.extract), args.frame, Path(args.to))
        print(json.dumps(record, ensure_ascii=False, indent=1))
        return 0

    if not (args.before and args.after):
        parser.error("需要同时给 --before 与 --after，或用 --extract/--to 只取帧")

    before_source = Path(args.before)
    after_source = Path(args.after)
    out_dir = Path(args.out) if args.out else before_source.parent / "seam"
    label = _safe_label(args.label) if args.label else _safe_label(
        "{a}-to-{b}".format(a=before_source.stem, b=after_source.stem)
    )

    try:
        before_record = resolve_frame(
            args.before, "before_end", out_dir / "{label}-before-end.png".format(label=label)
        )
        after_record = resolve_frame(
            args.after, "after_start", out_dir / "{label}-after-start.png".format(label=label)
        )
        before_image = _load(Path(before_record["path"]))
        after_image = _load(Path(after_record["path"]))

        if before_image.size != after_image.size:
            after_compared = after_image.resize(before_image.size, Image.LANCZOS)
            size_note = (
                "两帧尺寸不同（{a} vs {b}），按前段尺寸缩放过再比较；尺寸差本身也是接缝问题。"
                .format(a=before_image.size, b=after_image.size)
            )
        else:
            after_compared = after_image
            size_note = None

        before_pixels = _resized(before_image, ANALYSIS_WIDTH)
        after_pixels = _resized(after_compared, ANALYSIS_WIDTH)
        before_structure = _resized(before_image, STRUCTURE_WIDTH)
        after_structure = _resized(after_compared, STRUCTURE_WIDTH)

        regions = region_table(before_image, after_compared)
        measurements: dict[str, Any] = {
            "mean_abs_diff": round(float(np.abs(before_pixels - after_pixels).mean()), 2),
            "structure_mad": round(float(np.abs(before_structure - after_structure).mean()), 2),
            "edge_agreement": round(edge_agreement(before_pixels, after_pixels), 3),
            "histogram_distance": round(histogram_distance(before_pixels, after_pixels), 4),
            "luminance_mean": {
                "before": round(float(before_pixels.mean()), 1),
                "after": round(float(after_pixels.mean()), 1),
            },
            "luma_mean": {
                "before": round(luma_mean(before_pixels), 1),
                "after": round(luma_mean(after_pixels), 1),
                "change_pct": round(
                    100.0 * (luma_mean(after_pixels) - luma_mean(before_pixels))
                    / max(luma_mean(before_pixels), 1e-6), 1
                ),
                "note": (
                    "Rec.601 亮度；change_pct 为相对 before 的均值变化百分比。"
                    "核对第 0 秒时 --before 给送进去的首帧、--after 给本段视频。"
                    "前后须使用同一解码与色彩转换路径，并核对尺寸、构图和可比区域；"
                    "全幅均值变化也可能伴随画面内容变化，读数本身不判定合格与否或变化原因。"
                ),
            },
            "rgb_mean": {
                "before": [round(float(value), 1) for value in before_pixels.reshape(-1, 3).mean(axis=0)],
                "after": [round(float(value), 1) for value in after_pixels.reshape(-1, 3).mean(axis=0)],
            },
            "regions": regions,
        }

        envelope: dict[str, Any] = {}
        if not args.no_envelope:
            for key, record in (("before", before_record), ("after", after_record)):
                source = Path(record["source"])
                if record["probe"] is None:
                    envelope[key] = {"note": "输入是静帧，没有段内基线"}
                    continue
                try:
                    envelope[key] = within_shot_envelope(source)
                except SeamError as error:
                    envelope[key] = {"note": str(error)}
        measurements["within_shot_envelope"] = envelope

        # 声音这一侧：画面接缝能并排看，声音必须报数才能比。
        if not args.no_audio and before_record["probe"] and after_record["probe"]:
            try:
                measurements["audio_seam"] = audio_seam(
                    Path(before_record["source"]), Path(after_record["source"]))
                measurements["audio_onset"] = {
                    "before": audio_onset(Path(before_record["source"])),
                    "after": audio_onset(Path(after_record["source"])),
                }
            except SeamError as error:
                measurements["audio_seam"] = {"note": str(error)}
        else:
            measurements["audio_seam"] = {"note": "输入是静帧或已跳过"}

        # The one derived number worth printing: the seam as a multiple of the
        # largest single step either shot already takes. Reported, never judged.
        steps = [
            envelope[key].get("structure_mad_max_step")
            for key in ("before", "after")
            if isinstance(envelope.get(key), dict)
            and isinstance(envelope[key].get("structure_mad_max_step"), (int, float))
        ]
        if steps:
            denominator = max(steps)
            value = round(measurements["structure_mad"] / max(denominator, 1e-6), 1)
            # 分档只用来递一句话给写契约的人，不拦任何东西。档位背后是实测：
            # 2026-11-07 EP002 七处接缝里，真接上的四处在 0.5–0.9，两处断的分别在
            # 22.6 与 41 左右（机位换到了人物另一侧）。所以 10 倍以上几乎总是
            # 「换空间/换机位」，1–3 倍才是正常接缝的常见区间。
            # 实测区分度：真接上的四处 vs_median 落在 1.0–2.5，断开的在两处
            # 67.7 / 73.7，中间隔着 20 倍以上。所以分档优先用 vs_median，
            # value 只在 vs_median 缺失时兜底。
            # 分母用「段内最大单帧阶跃」在某些段会被一次快速运镜抬得很高，
            # 把真断开的接缝压成中等比值（2026-11-07 C8：structure_mad 62.96，
            # 但段内有一帧 10.93 的运镜阶跃，比值只剩 5.8）。再给一个以中位数
            # 为分母的读数：中位数代表这段的常态运动，接缝相对常态放大多少更直观。
            medians = [
                envelope[key].get("structure_mad_median")
                for key in ("before", "after")
                if isinstance(envelope.get(key), dict)
                and isinstance(envelope[key].get("structure_mad_median"), (int, float))
            ]
            median_ratio = None
            if medians:
                median_ratio = round(
                    measurements["structure_mad"] / max(max(medians), 1e-6), 1)
            basis = median_ratio if median_ratio is not None else value
            if basis < 5:
                band = "normal"
                hint = ("接缝与段内单帧阶跃同量级，这类接缝通常靠剪辑即可，"
                        "不必额外加遮挡。仍要打开并排图确认四要素。")
            elif basis < 20:
                band = "raised"
                hint = ("接缝比段内单帧阶跃明显，常见原因是曝光/色温漂移或轻微位移。"
                        "先用声音桥或动作掩护处理；若并排图里物体位置对不上，按换空间处理。")
            else:
                band = "space_change"
                hint = ("接缝高出段内两个数量级，通常意味着换了空间或机位。"
                        "先打开并排图确认：若这一刀本来就是换场/换机位（剧情需要），"
                        "就按硬切写进契约，不要试图用叠化掩盖；"
                        "若本来该是连续镜头，那是机位写反了，只能改机位重出。")
            measurements["seam_step_ratio"] = {
                "value": value,
                "vs_median_step": median_ratio,
                "band": band,
                "hint": hint,
                "denominator": denominator,
                "denominator_basis": "max single-frame step in either shot",
                "reading": (
                    "接缝是一个单帧阶跃，应当和段内单帧阶跃同量级。"
                    "1–2 倍是正常接缝；高出两个数量级时先打开并排图确认换没换空间。"
                    "这不是通过阈值：本项目不在判断类问题上设机械闸门。"
                    "与 vs_median_step 各自的用法：value 会被段内一次快速运镜抬高分母，"
                    "vs_median_step 用段内常态运动当基准；两者差距很大（例如 value<10 但 "
                    "vs_median_step>50）时，说明这段本身运动剧烈，以 vs_median_step 与并排图为准。"
                ),
            }
        else:
            measurements["seam_step_ratio"] = {
                "value": None,
                "note": "输入是静帧或段内基线不可用，没有分母；只看并排图。",
            }

        side_by_side(
            before_image, after_image,
            (
                "{name} · last frame".format(name=before_source.name),
                "{name} · first frame".format(name=after_source.name),
            ),
            out_dir / "{label}-side-by-side.jpg".format(label=label),
        )
        grid_image(
            before_image, after_compared, regions,
            out_dir / "{label}-grid.jpg".format(label=label),
        )

        report: dict[str, Any] = {
            "schema": SCHEMA,
            "label": label,
            "before": before_record,
            "after": after_record,
            "comparison": measurements,
            "outputs": {
                "side_by_side": str(out_dir / "{label}-side-by-side.jpg".format(label=label)),
                "grid": str(out_dir / "{label}-grid.jpg".format(label=label)),
            },
            "caveat": (
                "本文件只提供证据，不判定接缝是否成立。判断要打开 side-by-side 与 grid，"
                "按《视频提示词.md》接缝契约逐项看：同一个人、同一空间、同一造型、同一道具状态。"
            ),
        }
        if size_note:
            report["size_note"] = size_note
        report_path = out_dir / "{label}-seam.json".format(label=label)
        out_dir.mkdir(parents=True, exist_ok=True)
        if not report_path.exists():
            report_path.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
        else:
            # Keep every run: a repaired seam has two measurements and the later
            # one only means something next to the earlier one.
            stem = report_path.with_suffix("")
            index = 2
            while True:
                candidate = Path("{stem}-{index}.json".format(stem=stem, index=index))
                if not candidate.exists():
                    candidate.write_text(
                        json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8"
                    )
                    report_path = candidate
                    break
                index += 1
        report["report_path"] = str(report_path)
        print(json.dumps(report, ensure_ascii=False, indent=1))
        return 0
    except SeamError as error:
        print("[ERROR] {error}".format(error=error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
