#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""生成视频的技术层检查（媒体验收第 2 层）：只测可测量的，不判剧情。

逐条视频报告：
- frames / duration：帧数与时长；给了 --expect-seconds 时核对 24fps 17k+5 吸附后的帧数；
- size：分辨率，给了 --expect-size 时必须一致；
- audio：是否有音频流（画音同轨模型必须有）、整段是否近乎静音；
- black：黑场占比（blackdetect）；
- cuts：段内硬切（相邻帧差远高于本条中位数的突变），单镜视频出现即 FAIL；
- brake：头尾刹车（首/尾 0.5 秒运动量相对中段的比值，低于 0.5 记 WARN）。

阈值都是相对本条视频自身（中位数比），不是跨项目绝对值。

用法:
    python3 video_check.py <project> --media <视频...> [--expect-seconds 6] \
        [--expect-size 1024x576] [--multi-shot] [--json]

退出码：0 全部 PASS；1 有 WARN；2 有 FAIL；3 输入错误或缺 ffmpeg。
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("video_check.py requires Python 3.9 or newer")

import numpy as np

FPS = 24
SW, SH = 64, 36
CUT_RATIO = 6.0          # 相邻帧差 / 中位帧差 超过此值视为硬切
CUT_FLOOR = 18.0         # 且绝对帧差至少这么大，避免近静止镜的噪声误报
BRAKE_RATIO = 0.5        # 头/尾运动量 / 中段 低于此值记头尾刹车
BLACK_FAIL = 0.10        # 黑场占比超过 10% 判 FAIL
SILENT_DB = -50.0        # 平均音量低于此值视为静音
SEMANTIC_UNVERIFIED = (
    "identity_costume",
    "hand_limb_contact",
    "action_spatial_continuity",
    "dialogue_lip_sync",
    "audio_voice",
)
ASR_LIMIT = "ASR 只辅助定位，不能证明精确台词、口型或声线。"


def _result(path: Path, items: dict, verdict: str) -> dict:
    return {
        "media": str(path),
        "items": items,
        "verdict": verdict,
        "semantic_review": {name: "UNVERIFIED" for name in SEMANTIC_UNVERIFIED},
        "asr_limit": ASR_LIMIT,
    }


def snapped_frames(seconds: float) -> int:
    requested = round(seconds * FPS)
    return 17 * ((requested - 5 + 16) // 17) + 5


def _probe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-count_packets", "-show_entries",
         "stream=codec_type,width,height,nb_read_packets:format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def _gray_frames(path: Path) -> np.ndarray:
    data = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"scale={SW}:{SH}",
         "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True, check=True).stdout
    n = len(data) // (SW * SH)
    return np.frombuffer(data[: n * SW * SH], np.uint8).reshape(n, SW * SH).astype(np.float32)


def _black_ratio(path: Path, duration: float) -> float:
    err = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-vf", "blackdetect=d=0.1:pix_th=0.10",
         "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    total = 0.0
    for token in err.split():
        if token.startswith("black_duration:"):
            total += float(token.split(":", 1)[1])
    return total / duration if duration > 0 else 0.0


def _mean_volume(path: Path) -> float | None:
    err = subprocess.run(
        ["ffmpeg", "-v", "info", "-i", str(path), "-vn", "-af", "volumedetect", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    for line in err.splitlines():
        if "mean_volume:" in line:
            return float(line.split("mean_volume:")[1].split("dB")[0])
    return None


def check(path: Path, expect_seconds: float | None, expect_size: tuple[int, int] | None,
          multi_shot: bool) -> dict:
    info = _probe(path)
    streams = info.get("streams") or []
    video = next((s for s in streams if s.get("codec_type") == "video"), None)
    audio = any(s.get("codec_type") == "audio" for s in streams)
    duration = float((info.get("format") or {}).get("duration") or 0.0)
    items: dict[str, dict] = {}

    def put(name, grade, detail):
        items[name] = {"grade": grade, "detail": detail}

    if video is None:
        put("video", "FAIL", "没有视频流")
        return _result(path, items, "FAIL")
    frames = int(video.get("nb_read_packets") or 0)
    if expect_seconds is not None:
        want = snapped_frames(expect_seconds)
        put("frames", "PASS" if abs(frames - want) <= 1 else "FAIL",
            f"{frames} 帧，期望 {want}（{expect_seconds}s 吸附 17k+5）")
    else:
        put("frames", "PASS" if frames > 0 else "FAIL", f"{frames} 帧，{duration:.2f}s")
    size = (int(video.get("width") or 0), int(video.get("height") or 0))
    if expect_size:
        put("size", "PASS" if size == expect_size else "FAIL", f"{size[0]}×{size[1]}")
    if not audio:
        put("audio", "FAIL", "没有音频流（画音同轨模型应有）")
    else:
        volume = _mean_volume(path)
        put("audio", "FAIL" if volume is not None and volume < SILENT_DB else "PASS",
            f"平均音量 {volume} dB" if volume is not None else "有音频流")
    black = _black_ratio(path, duration)
    put("black", "FAIL" if black > BLACK_FAIL else "PASS", f"黑场占比 {black:.1%}")

    gray = _gray_frames(path)
    if len(gray) >= 4:
        diff = np.abs(np.diff(gray, axis=0)).mean(axis=1)
        median = float(np.median(diff)) or 1e-6
        cuts = [round((i + 1) / FPS, 2) for i, d in enumerate(diff)
                if d > CUT_RATIO * median and d > CUT_FLOOR]
        if cuts and not multi_shot:
            put("cuts", "FAIL", f"单镜视频内检出硬切于 {cuts} 秒（段内藏切）")
        else:
            put("cuts", "PASS", f"切点 {cuts}" if cuts else "未检出硬切")
        edge = max(1, int(0.5 * FPS))
        if len(diff) > 3 * edge:
            middle = float(np.median(diff[edge:-edge])) or 1e-6
            head = float(np.median(diff[:edge])) / middle
            tail = float(np.median(diff[-edge:])) / middle
            braking = [n for n, r in (("头", head), ("尾", tail)) if r < BRAKE_RATIO]
            put("brake", "WARN" if braking else "PASS",
                f"头/中 {head:.2f}，尾/中 {tail:.2f}" + (f"（{'、'.join(braking)}部刹车）" if braking else ""))
        else:
            # 片段太短时刹车无从测起；显式 NOT_EVALUATED，不得静默缺项读成通过。
            put("brake", "NOT_EVALUATED", "片段过短，头尾刹车未测")
    else:
        put("cuts", "NOT_EVALUATED", f"可解码帧仅 {len(gray)} 帧（<4），段内硬切未测")
        put("brake", "NOT_EVALUATED", f"可解码帧仅 {len(gray)} 帧（<4），头尾刹车未测")
    # NOT_EVALUATED 与 WARN 同档：未测不等于失败，但整体结论也不得读成纯 PASS。
    order = {"PASS": 0, "WARN": 1, "NOT_EVALUATED": 1, "FAIL": 2}
    verdict = max((v["grade"] for v in items.values()), key=order.get)
    if verdict == "NOT_EVALUATED":
        verdict = "WARN"
    return _result(path, items, verdict)


# Seam thresholds (same scale as internal cut detection: 64×36 gray pixels)
SEAM_WARN_MAD = 28.0   # structural MAD above this → spatial discontinuity warn
SEAM_FAIL_MAD = 55.0   # above this → likely scene-break (not just drift)


def _last_frame(path: Path) -> np.ndarray | None:
    """Extract the last frame of a video as a 64×36 gray array."""
    try:
        data = subprocess.run(
            ["ffmpeg", "-v", "error", "-sseof", "-0.5", "-i", str(path),
             "-vframes", "1", "-vf", f"scale={SW}:{SH}",
             "-f", "rawvideo", "-pix_fmt", "gray", "-"],
            capture_output=True, check=True).stdout
        if len(data) < SW * SH:
            return None
        return np.frombuffer(data[:SW * SH], np.uint8).astype(np.float32)
    except subprocess.CalledProcessError:
        return None


def _first_frame(path: Path) -> np.ndarray | None:
    """Extract the first frame of a video as a 64×36 gray array."""
    try:
        data = subprocess.run(
            ["ffmpeg", "-v", "error", "-i", str(path),
             "-vframes", "1", "-vf", f"scale={SW}:{SH}",
             "-f", "rawvideo", "-pix_fmt", "gray", "-"],
            capture_output=True, check=True).stdout
        if len(data) < SW * SH:
            return None
        return np.frombuffer(data[:SW * SH], np.uint8).astype(np.float32)
    except subprocess.CalledProcessError:
        return None


def check_seam(before: Path, after: Path) -> dict:
    """Measure structural similarity at the boundary between two video segments.

    Compares the last frame of `before` with the first frame of `after`.
    A high MAD means the two segments look spatially discontinuous at the cut,
    which is the most common symptom of identity/space drift between shots.

    This is a geometric signal, not a semantic one: it cannot tell *why* the
    frames differ (new scene vs same scene with different composition), but it
    reliably flags cases where the agent should look carefully at the seam.
    """
    tail = _last_frame(before)
    head = _first_frame(after)
    if tail is None or head is None:
        return {
            "before": str(before), "after": str(after),
            "grade": "NOT_EVALUATED",
            "detail": "无法提取接缝帧（ffmpeg 错误）",
            "mad": None,
        }
    mad = float(np.abs(tail - head).mean())
    if mad >= SEAM_FAIL_MAD:
        grade = "FAIL"
        note = "接缝处结构突变，可能是场景切换或严重漂移"
    elif mad >= SEAM_WARN_MAD:
        grade = "WARN"
        note = "接缝处结构差异明显，建议实看人物位置与空间连续性"
    else:
        grade = "PASS"
        note = "接缝结构差异在正常范围内"
    return {
        "before": str(before), "after": str(after),
        "grade": grade,
        "detail": f"MAD {mad:.1f}（阈值 warn≥{SEAM_WARN_MAD} / fail≥{SEAM_FAIL_MAD}）— {note}",
        "mad": round(mad, 2),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="生成视频技术层检查")
    parser.add_argument("project")
    parser.add_argument("--media", nargs="+", required=True)
    parser.add_argument("--expect-seconds", type=float, default=None)
    parser.add_argument("--expect-size", default=None, help="如 1024x576")
    parser.add_argument("--multi-shot", action="store_true", help="本条有意包含多个剪辑镜头")
    parser.add_argument("--seam", action="store_true",
                        help="额外检查相邻 --media 之间的接缝空间连续性（按传入顺序两两比较）")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        print("需要 ffmpeg / ffprobe；未测不等于通过。", file=sys.stderr)
        return 3
    size = None
    if args.expect_size:
        w, h = args.expect_size.lower().split("x")
        size = (int(w), int(h))
    order = {"PASS": 0, "WARN": 1, "FAIL": 2}
    worst = 0
    results = []
    paths = []
    for raw in args.media:
        path = Path(raw)
        if not path.is_absolute():
            path = Path(args.project) / raw
        if not path.is_file():
            print(f"文件不存在：{raw}", file=sys.stderr)
            return 3
        paths.append(path)
        try:
            result = check(path, args.expect_seconds, size, args.multi_shot)
        except subprocess.CalledProcessError as exc:
            print(f"无法解码：{raw}（{exc}）", file=sys.stderr)
            return 3
        results.append(result)
        worst = max(worst, order[result["verdict"]])
    seam_results = []
    if args.seam and len(paths) >= 2:
        for i in range(len(paths) - 1):
            sr = check_seam(paths[i], paths[i + 1])
            seam_results.append(sr)
            worst = max(worst, order.get(sr["grade"], 0))
    if args.json:
        if seam_results:
            output = {"segments": results, "seams": seam_results}
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            # Preserve the original list format when --seam is not used,
            # so existing callers that index into json.loads(output)[N] keep working.
            print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        for result in results:
            print(f"{result['verdict']}  {result['media']}")
            for name, item in result["items"].items():
                print(f"  {item['grade']:4}  {name}: {item['detail']}")
            for name, grade in result["semantic_review"].items():
                print(f"  {grade}  {name}: 技术脚本未审；由独立 reviewer 实读媒体后判定")
            print(f"  NOTE {result['asr_limit']}")
        if seam_results:
            print("\n── 接缝空间连续性 ──")
            for sr in seam_results:
                print(f"  {sr['grade']:4}  {Path(sr['before']).name} → {Path(sr['after']).name}: {sr['detail']}")
    return worst


if __name__ == "__main__":
    raise SystemExit(main())
