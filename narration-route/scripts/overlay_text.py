#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""旁白艺术字叠层 · 通用版

用法:
    python3 overlay_text.py <输入视频> <输出视频> <配置JSON>
    python3 overlay_text.py in.mp4 out.mp4 narration.json --preview 12.5

配置 JSON（时间用成片输出时间线的秒数）:
[
  {
    "text": "小时候的我一直不明白",
    "start": 10.55,
    "end": 14.45,
    "mode": "v-right",      // v-right | v-left | h-top | h-bottom
    "fsize": 64,            // 可选，默认 64
    "color": "#FFFAEB",     // 可选
    "glow":  "#FFE196",     // 可选
    "edge":  "#19140F"      // 可选
  }
]

排版规则见 references/layout.md：竖排按可用高度自动分列并垂直居中，
横排按可用宽度自动折行；不会出画。
"""
import sys
import os
import json
import random
import argparse
import subprocess

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

FONT_CANDIDATES = [
    ("/System/Library/Fonts/Songti.ttc", 0),        # Songti SC Black
    ("/System/Library/Fonts/STHeiti Medium.ttc", 0),
    ("/System/Library/Fonts/Hiragino Sans GB.ttc", 0),
]

DEFAULTS = dict(fsize=64, color="#FFFAEB", glow="#FFE196", edge="#19140F",
                fade_in=0.50, fade_out=0.60, jitter=1, seed=20251020)


def hex2bgr(h):
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (b, g, r)


def load_font(fsize):
    for path, idx in FONT_CANDIDATES:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, fsize, index=idx)
            except Exception:
                continue
    raise RuntimeError("找不到可用中文字体，请安装 Songti 或 Heiti")


def split_columns(text, per_col):
    """按标点切语义段，逐段灌列；超长段硬切。返回列列表。"""
    import re
    raw = text.replace(" ", "")
    segs = [x for x in re.split(r"(?<=[，。：；、！？])", raw) if x]
    cols, cur = [], ""
    for seg in segs:
        while len(seg) > per_col:
            room = per_col - len(cur)
            if room > 0:
                cur += seg[:room]
                seg = seg[room:]
            if cur:
                cols.append(cur)
                cur = ""
            if len(seg) <= per_col:
                break
        if len(cur) + len(seg) <= per_col:
            cur += seg
        else:
            if cur:
                cols.append(cur)
            cur = seg
    if cur:
        cols.append(cur)
    return cols or [raw]


def render_layer(spec, W, H, rng):
    """渲染一条旁白为全画幅 RGBA。返回 np.float32 (H,W,4)。"""
    text = spec["text"]
    mode = spec.get("mode", "v-right")
    fsize = int(spec.get("fsize", DEFAULTS["fsize"]))
    color = hex2bgr(spec.get("color", DEFAULTS["color"]))
    glow = hex2bgr(spec.get("glow", DEFAULTS["glow"]))
    edge = hex2bgr(spec.get("edge", DEFAULTS["edge"]))
    jitter = int(spec.get("jitter", DEFAULTS["jitter"]))

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    if mode.startswith("v"):
        # 竖排：自动缩字号保证不出画
        for _ in range(5):
            font = load_font(fsize)
            line_gap = int(fsize * 1.16)
            gap = int(fsize * 0.20)
            per_col = max(1, int((H - 240) // line_gap))
            cols = split_columns(text, per_col)
            need_w = len(cols) * (fsize + gap) - gap
            need_h = max(len(c) for c in cols) * line_gap
            if need_w <= W - 100 and need_h <= H - 200:
                break
            fsize = max(34, int(fsize * 0.92))
        total_w = need_w
        x_start = (W - 78 - total_w) if mode == "v-right" else 26
        x_start = max(16, x_start)
        y_start = max(60, (H - need_h) // 2)
        for ci, col in enumerate(cols):
            cx = x_start + ci * (fsize + gap)
            for ri, ch in enumerate(col):
                bb = d.textbbox((0, 0), ch, font=font)
                cw = bb[2] - bb[0]
                x = cx + (fsize - cw) // 2 + (rng.randint(-jitter, jitter) if jitter else 0)
                y = y_start + ri * line_gap + (rng.randint(-jitter, jitter) if jitter else 0)
                d.text((x, y), ch, font=font, fill=(255, 255, 255, 255))
    else:
        # 横排：按宽度自动折行
        font = load_font(fsize)
        line_gap = int(fsize * 1.42)
        avail_w = W - 120
        lines, cur = [], ""
        for ch in text:
            if font.getlength(cur + ch) <= avail_w:
                cur += ch
            else:
                lines.append(cur)
                cur = ch
        if cur:
            lines.append(cur)
        block_h = len(lines) * line_gap
        if mode == "h-bottom":
            y = max(70, H - 240 - block_h)
        else:
            y = 72
        for ln in lines:
            tw = font.getlength(ln)
            d.text(((W - tw) / 2, y), ln, font=font, fill=(255, 255, 255, 255))
            y += line_gap

    alpha = img.split()[3]
    e = ImageChops.subtract(alpha.filter(ImageFilter.MaxFilter(9)), alpha)
    edge_col = Image.new("RGBA", (W, H), edge + (255,))
    edge_col.putalpha(e.point(lambda v: int(v * 0.88)))
    g = alpha.filter(ImageFilter.GaussianBlur(11))
    glow_layer = Image.new("RGBA", (W, H), glow + (255,))
    glow_layer.putalpha(g.point(lambda v: int(v * 0.58)))
    body = Image.new("RGBA", (W, H), color + (255,))
    body.putalpha(alpha)
    out = Image.alpha_composite(edge_col, glow_layer)
    out = Image.alpha_composite(out, body)
    return np.array(out).astype(np.float32)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("config")
    ap.add_argument("--preview", type=float, default=None,
                    help="只导出该时刻单帧 PNG（用于定位置，避免整片重渲染）")
    ap.add_argument("--seed", type=int, default=DEFAULTS["seed"])
    args = ap.parse_args()

    specs = json.load(open(args.config, encoding="utf-8"))
    for s in specs:
        s.setdefault("mode", "v-right")

    cap = cv2.VideoCapture(args.src)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24.0
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"src {n}f {W}x{H} @{fps:.3f}")

    # 预渲染所有图层（抖动种子固定，避免逐帧跳动）
    layers = []
    for i, s in enumerate(specs):
        rng = random.Random(args.seed + i)
        arr = render_layer(s, W, H, rng)
        layers.append(arr)
        print(f"  layer[{i}] {s['text'][:14]}... {s['start']:.2f}-{s['end']:.2f} {s['mode']}")

    if args.preview is not None:
        t = args.preview
        cap.set(cv2.CAP_PROP_POS_FRAMES, int(t * fps))
        ok, fr = cap.read()
        cap.release()
        if not ok:
            raise SystemExit("预览取帧失败")
        out = fr.astype(np.float32)
        for arr, s in zip(layers, specs):
            if s["start"] <= t < s["end"]:
                a = arr[:, :, 3:4] / 255.0
                out = out * (1 - a) + arr[:, :, :3] * a
        cv2.imwrite(args.dst, out.astype(np.uint8))
        print("preview ->", args.dst)
        return

    tmp = "/tmp/_overlay_text_tmp.mp4"
    proc = cv2.VideoWriter(tmp, cv2.VideoWriter_fourcc(*"mp4v"), fps, (W, H))
    for i in range(n):
        ok, fr = cap.read()
        if not ok:
            break
        t = i / fps
        out = fr.astype(np.float32)
        for arr, s in zip(layers, specs):
            st, en = s["start"], s["end"]
            if not (st <= t < en):
                continue
            dur = max(1e-3, en - st)
            fin = s.get("fade_in", DEFAULTS["fade_in"])
            fout = s.get("fade_out", DEFAULTS["fade_out"])
            a = min(1.0, (t - st) / fin) * min(1.0, (en - t) / fout)
            if a <= 0:
                continue
            la = arr[:, :, 3:4] / 255.0 * a
            out = out * (1 - la) + arr[:, :, :3] * la
        proc.write(out.astype(np.uint8))
        if i % 200 == 0:
            print(f"  {i}/{n}")
    cap.release()
    proc.release()

    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-i", args.src,
                    "-map", "0:v", "-map", "1:a?", "-c:v", "libx264", "-crf", "17",
                    "-preset", "slow", "-pix_fmt", "yuv420p", "-c:a", "copy", args.dst],
                   check=True)
    print("DONE ->", args.dst)


if __name__ == "__main__":
    main()
