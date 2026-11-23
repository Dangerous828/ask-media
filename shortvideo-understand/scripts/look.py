#!/usr/bin/env python3
"""短视频画面理解：抽帧 + 多模态模型描述，输出「画面层」事实，交给 Agent 合成最终回答。

为什么需要它：短视频的关键信息常常只在画面里（游戏账号数值、商品参数、代码、地图、
字幕之外的 UI 文字）。只转录音频会丢掉这一层。本脚本把画面转成文字证据，
「看懂」的最终合成由调用它的 Agent 完成——脚本本身不调文本大模型。

用法：
    python3 scripts/look.py <本地视频文件>                    # 默认均匀 8 帧
    python3 scripts/look.py <本地视频文件> --frames 12
    python3 scripts/look.py <本地视频文件> --timestamps 0,15,48
    python3 scripts/look.py --video-url <平台链接> --frames 8   # 自行下载再抽帧
    python3 scripts/look.py <视频> -o out.md                   # 落 Markdown

依赖：ffmpeg/ffprobe（必需）+ 一个 OpenAI 兼容多模态端点。
视觉端点走环境变量，不硬编码密钥：
    CHUBBY_VISION_BASE      默认 http://127.0.0.1:8321/v1（本机 sensenova 网关）
    CHUBBY_VISION_MODEL     默认 sensenova-6.8-flash-lite
    CHUBBY_VISION_API_KEY   本地网关可留空；远端必填
"""

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.error
import urllib.request

DEFAULT_BASE = os.environ.get("CHUBBY_VISION_BASE", "http://127.0.0.1:8321/v1")
DEFAULT_MODEL = os.environ.get("CHUBBY_VISION_MODEL", "sensenova-6.8-flash-lite")
FRAME_WIDTH = 720          # 识图输入宽度：再大对 OCR 无收益、更慢
MAX_BYTES_PER_FRAME = 220_000

# 技能仓根目录：安装包里就是上一级，仓库内是上两级（chubby_common 所在处）。
_HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = _HERE if os.path.isdir(os.path.join(_HERE, "chubby_common")) else os.path.dirname(_HERE)
for _p in (os.path.join(_HERE, "lib"), ROOT):
    if _p not in sys.path and os.path.isdir(_p):
        sys.path.insert(0, _p)

PROMPT = (
    "这是一条短视频中的一帧。请用中文按下面三段输出，只写画面里确实存在的信息，不要推测：\n"
    "【画面】主体、人物、场景与动作，一句话。\n"
    "【文字】逐字抄出屏幕上的所有可见文字与数字：烧录字幕、标题、UI 标签、"
    "账号/ID/战力等数值、价格、代码、地名。没有就写「无」。\n"
    "【镜头】分开描述景别与可见介质观感（实拍观感/半写实CG/3D动画/2D动画/录屏/图文/PPT）。"
    "介质不确定时明确写「介质不确定」，不要仅因皮肤逼真就断言实拍，不推断实际制作技术或软件。\n"
    "总字数 150 以内。"
)


def ff(name: str) -> str:
    """ffmpeg/ffprobe 路径：Agent shell 的 PATH 常不含 /opt/homebrew/bin。"""
    exe = shutil.which(name)
    for c in (f"/opt/homebrew/bin/{name}", f"/usr/local/bin/{name}"):
        if exe is None and os.access(c, os.X_OK):
            exe = c
    if exe is None:
        raise SystemExit(f"❌ 缺少 {name}（macOS: brew install ffmpeg）")
    return exe


def probe_duration(path: str) -> float:
    r = subprocess.run(
        [ff("ffprobe"), "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", path],
        capture_output=True, text=True, timeout=30,
    )
    try:
        return float(r.stdout.strip())
    except ValueError:
        return 0.0


def encode_frame(src: str) -> str:
    """缩到 FRAME_WIDTH 并以 q=75 压 JPEG，返回 data URL（超大时继续降质）。"""
    out = src + ".v.jpg"
    quality = "75"
    for _ in range(3):
        subprocess.run(
            [ff("ffmpeg"), "-y", "-v", "error", "-i", src,
             "-vf", f"scale={FRAME_WIDTH}:-2", "-q:v", quality, out],
            capture_output=True, timeout=60, check=True,
        )
        if os.path.getsize(out) <= MAX_BYTES_PER_FRAME:
            break
        quality = str(max(2, int(quality) - 2))  # mjpeg q 越小越狠
    with open(out, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()
    os.remove(out)
    return "data:image/jpeg;base64," + b64


def extract_frames(path: str, tmpdir: str, times) -> list:
    frames = []
    for i, t in enumerate(times):
        dst = os.path.join(tmpdir, f"f{i:02d}.jpg")
        # -ss 放 -i 前为快速定位，对本用途精度足够
        r = subprocess.run(
            [ff("ffmpeg"), "-y", "-v", "error", "-ss", f"{t:.2f}", "-i", path,
             "-frames:v", "1", "-q:v", "2", dst],
            capture_output=True, text=True, timeout=120,
        )
        if r.returncode == 0 and os.path.isfile(dst) and os.path.getsize(dst) > 0:
            frames.append((t, dst))
        else:
            print(f"  ⚠️  t={t:.1f}s 抽帧失败：{r.stderr.strip()[:80]}", file=sys.stderr)
    return frames


def uniform_times(duration: float, n: int) -> list:
    if duration <= 0:
        return [0.0]
    if n == 1:
        return [duration / 2]
    pad = min(0.5, duration * 0.02)
    span = duration - 2 * pad
    return [pad + span * i / (n - 1) for i in range(n)]


# 本地图像描述网关会强制思考：thinking:disabled / reasoning_effort:none 对
# 127.0.0.1:8321 实测均不生效，reasoning 约吃掉 350-600 token。预算低于 ~1200 时
# content 会被截空，只剩 reasoning 草稿。阶梯：1600 常规 → 2500 兜底。
MAX_TOKEN_LADDER = (1600, 2500, 2500)

# 思考草稿兜底时的截断长度（字）：实测草稿常 1000+ 字且前段信息密度最高。
REASONING_CLIP = 400


def describe(data_url: str, base: str, model: str, key: str, timeout: int) -> str:
    url = base.rstrip("/") + "/chat/completions"
    last = None
    diag = ""
    fallback_reasoning = ""
    for attempt, max_tokens in enumerate(MAX_TOKEN_LADDER):
        body = {
            "model": model,
            "temperature": 0.2,
            # 保留禁用参数：远端网关可能生效（见 sensenova-image 实测）。
            "thinking": {"type": "disabled"},
            "reasoning_effort": "none",
            "max_tokens": max_tokens,
            "messages": [{"role": "user", "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": data_url}},
            ]}],
        }
        req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                    headers={"Content-Type": "application/json"})
        if key:
            req.add_header("Authorization", "Bearer " + key)
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                d = json.loads(resp.read().decode("utf-8"))
            choices = d.get("choices") or []
            if not choices:
                diag = (f"无 choices；响应键={sorted(d)[:6]} "
                        f"error={str(d.get('error'))[:120]}")
                raise KeyError("choices")
            msg = choices[0].get("message") or {}
            content = (msg.get("content") or "").strip()
            if content:
                return content
            # content 空 → 记下 reasoning 作末位兜底，继续加预算重试
            fallback_reasoning = (msg.get("reasoning") or "").strip()
            diag = (f"max_tokens={max_tokens} 时 content 为空；"
                    f"finish_reason={choices[0].get('finish_reason')} "
                    f"reasoning_len={len(fallback_reasoning)}")
            raise KeyError("content")
        except (urllib.error.URLError, KeyError, json.JSONDecodeError, TimeoutError) as exc:
            last = exc
            if attempt < len(MAX_TOKEN_LADDER) - 1:
                import time

                time.sleep(2 * (attempt + 1))
    if fallback_reasoning:
        # 思考草稿未按三段格式且冗长（实测 1000+ 字），信息密度最高的部分在前段；
        # 截断后显式标注降级，避免淹没调用方上下文。需要完整内容时按该时间点重跑。
        clip = fallback_reasoning[:REASONING_CLIP]
        tail = "…" if len(fallback_reasoning) > REASONING_CLIP else ""
        return f"（格式降级：思考草稿截断，可用 --timestamps 单独重跑该帧）{clip}{tail}"
    return f"（识别失败：{type(last).__name__}{('；' + diag) if diag else ''}：{str(last)[:80]}）"


def fetch_video(url: str, tmpdir: str, height: int = 480) -> tuple:
    """下载一份视频用于抽帧，返回 (路径, 标题)。

    抖音走 chubby_common.douyin 分享页直链（yt-dlp 对 douyin.com 稳定 403），
    其余平台走 yt-dlp。cookie 自动探测本机登录过的浏览器，无需配置。
    """
    from chubby_common import ytdlp
    from chubby_common.config import PlatformConfig

    dst = os.path.join(tmpdir, "source.mp4")

    if "douyin.com" in url:
        # 抖音走分享页直链：yt-dlp 对 douyin.com 稳定 403
        from chubby_common import douyin

        info = douyin.download_video(url, dst)
        return dst, info["title"]

    # 按链接域名声明 cookie 域，交给 chubby_common.cookies 自动探测登录过的浏览器
    domain = "bilibili.com" if "bilibili.com" in url or "b23.tv" in url else ""
    cfg = PlatformConfig(id="look", name="画面理解", tag="视频",
                         default_title="视频", cookie_domain=domain,
                         referer=("https://www.bilibili.com" if domain else ""))
    title = (ytdlp.get_title(cfg, url) or "视频").strip() or "视频"
    # 画面层不需要音频：只下视频轨。实测 B 站「视频+音频合并下载」比纯视频轨慢一个
    # 数量级（同片 1491s：纯 360p 视频轨 8.7s，合并 480p 曾超时 293s）。
    h = max(180, min(int(height or 480), 1080))
    ytdlp.run_ydl(
        cfg,
        ["-f", f"bv*[height<={h}]/bv/b[height<={h}]/b",
         "--retries", "4", "--fragment-retries", "4", "--socket-timeout", "30",
         "--no-playlist", "-o", dst, url],
        timeout=900, capture=True,
    )
    return dst, title


def main():
    ap = argparse.ArgumentParser(description="短视频画面理解（抽帧 + 识图）")
    ap.add_argument("video", nargs="?", help="本地视频文件")
    ap.add_argument("--video-url", help="平台链接（自行下载再抽帧）")
    ap.add_argument("--frames", type=int, default=8, help="均匀抽帧数量（默认 8）")
    ap.add_argument("--timestamps", help="逗号分隔秒数，如 0,15,48（优先于 --frames）")
    ap.add_argument("--output", "-o", help="Markdown 输出路径（默认打印到 stdout）")
    ap.add_argument("--base", default=DEFAULT_BASE)
    ap.add_argument("--model", default=DEFAULT_MODEL)
    ap.add_argument("--timeout", type=int, default=90)
    ap.add_argument("--json", action="store_true", help="输出 JSON 而非 Markdown")
    ap.add_argument("--height", type=int, default=int(os.environ.get("CHUBBY_LOOK_HEIGHT", 480)),
                    help="下载视频轨最大高度（默认 480；小字/OCR 密集可提到 720）")
    args = ap.parse_args()

    if not args.video and not args.video_url:
        ap.error("需要本地视频路径或 --video-url")
    ff("ffmpeg"); ff("ffprobe")  # 入口即检查，缺失时早失败

    key = os.environ.get("CHUBBY_VISION_API_KEY", "").strip()
    tmpdir = tempfile.mkdtemp(prefix="look-")
    try:
        if args.video:
            path, title = args.video, os.path.splitext(os.path.basename(args.video))[0]
        else:
            print("  ⬇️  下载视频...", file=sys.stderr)
            path, title = fetch_video(args.video_url, tmpdir, args.height)

        duration = probe_duration(path)
        times = ([float(x) for x in args.timestamps.split(",")] if args.timestamps
                 else uniform_times(duration, max(1, args.frames)))
        print(f"  🎬 {title} | {duration:.0f}s | 抽 {len(times)} 帧", file=sys.stderr)

        frames = extract_frames(path, tmpdir, times)
        if not frames:
            print("❌ 一帧都没抽出来（文件损坏或 codec 不支持）", file=sys.stderr)
            return 1

        shots, ok = [], 0
        for t, f in frames:
            print(f"  👁️  t={t:.1f}s 识别中...", file=sys.stderr)
            desc = describe(encode_frame(f), args.base, args.model, key, args.timeout)
            good = not desc.startswith("（识别失败")
            ok += good
            shots.append({"t": round(t, 1), "description": desc, "ok": good})
        print(f"  ✅ {ok}/{len(shots)} 帧识别成功", file=sys.stderr)

        payload = {"title": title, "duration": round(duration, 1),
                   "source": args.video_url or os.path.abspath(path),
                   "model": args.model, "shots": shots}

        if args.json:
            out = json.dumps(payload, ensure_ascii=False, indent=2)
        else:
            lines = [f"# 画面理解：{title}", "",
                     f"- 时长：{duration:.0f}s | 帧数：{len(shots)}（成功 {ok}）",
                     f"- 来源：{payload['source']}", f"- 视觉模型：{args.model}", ""]
            for s in shots:
                lines += [f"### [{s['t']:.1f}s]", "", s["description"], ""]
            out = "\n".join(lines)
        if args.output:
            os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(out + "\n")
            print(args.output)
        else:
            print(out)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
