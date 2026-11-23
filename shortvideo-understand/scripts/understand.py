#!/usr/bin/env python3
"""短视频链接 → 结构化「可读证据」：元信息 + 文字稿（+可选画面层）。

设计边界：本脚本**不做总结**。它把视频变成 Agent 可直接阅读的文字证据，
「看懂并回答」由调用它的 Agent 完成——Agent 本身就是语言模型，再调一次外部
LLM 既多花钱又丢掉了对话上下文。

用法：
    python3 scripts/understand.py "https://www.bilibili.com/video/BVxxxx/"
    python3 scripts/understand.py "https://v.douyin.com/xxxx/"
    python3 scripts/understand.py BV1xxxxxxxxx              # 裸 BV 号
    python3 scripts/understand.py <URL> --look              # 加画面层（抽帧识图）
    python3 scripts/understand.py <URL> --look --frames 12
    python3 scripts/understand.py <URL> --timestamps 0,45,90 --look
    python3 scripts/understand.py <URL> -o note.md          # 落 Markdown
    python3 scripts/understand.py <URL> --audio-only        # 只要文字稿

输出（stdout，JSON）：
    {platform,title,author,duration,source,transcriber,text,shots,notes}
`text` 是完整文字稿；`shots` 仅在 --look 时出现；`notes` 记录降级与坑。

零配置：cookie 自动从本机已登录的浏览器探测（B 站 AI 字幕、抖音分享页都依赖它），
无需设置任何环境变量。
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LIB = os.path.join(HERE, "lib")
for p in (LIB, HERE):
    if p not in sys.path:
        sys.path.insert(0, p)

from chubby_common import asr, cookies, deps, vtt, ytdlp  # noqa: E402
from chubby_common.config import PlatformConfig  # noqa: E402

SUB_LANGS = "zh-Hans,zh-CN,zh,zh-Hant,ai-zh,en,en-US"
SUB_PRIORITY = ("zh-hans", "zh-cn", "zh", "zh-hant", "ai-zh", "en")

BILI = PlatformConfig(
    id="bilibili", name="Bilibili", tag="B站", default_title="B站视频",
    language="zh", referer="https://www.bilibili.com", cookie_domain="bilibili.com",
)

# ---------------------------------------------------------------- 平台判定

def detect(url: str) -> str:
    if re.search(r"(BV[\w]+)", url) or "bilibili.com" in url or "b23.tv" in url:
        return "bilibili"
    if "douyin.com" in url or "iesdouyin" in url:
        return "douyin"
    return "other"


def normalize(url: str, platform: str) -> str:
    if platform == "bilibili":
        m = re.search(r"(BV[\w]+)", url)
        if m:
            return f"https://www.bilibili.com/video/{m.group(1)}/"
    return url


def expand_bilibili_short_url(url: str) -> str:
    """把 b23.tv 短链展开成含 BV 号的正式地址，供后续统一解析。"""
    request = urllib.request.Request(
        url, headers={"User-Agent": "Mozilla/5.0"}, method="GET"
    )
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            expanded = response.geturl()
    except OSError as exc:
        raise RuntimeError(f"B 站短链展开失败：{exc}") from exc
    if not re.search(r"(BV[\w]+)", expanded):
        raise RuntimeError("B 站短链展开后未找到 BV 号，请改用完整视频页链接")
    return expanded


# ---------------------------------------------------------------- 元信息

def bilibili_info(url: str, bvid: str) -> dict:
    try:
        r = ytdlp.run_ydl(
            BILI, ["--print", "%(title)s|||%(uploader)s|||%(duration)s",
                   "--skip-download", url], timeout=45, capture=True)
        line = r.stdout.strip().split("\n")[0]
        title, _, rest = line.partition("|||")
        uploader, _, dur = rest.partition("|||")
        if uploader.strip() in ("NA", "None"):
            uploader = ""
        return {"title": title.strip() or bvid, "author": uploader.strip(),
                "duration": float(dur) if dur.strip() not in ("", "NA") else 0.0}
    except Exception:
        return {"title": bvid, "author": "", "duration": 0.0}


def download_kept_video(cfg, url: str, keep_dir: str) -> str:
    """显式保留最高可用画质的完整音视频；返回 yt-dlp 报出的实际落盘路径。"""
    os.makedirs(keep_dir, exist_ok=True)
    template = os.path.join(keep_dir, "source.%(ext)s")
    try:
        r = ytdlp.run_ydl(
            cfg,
            ["-f", "bv*+ba/b", "--merge-output-format", "mp4/mkv",
             "--retries", "4", "--fragment-retries", "4", "--socket-timeout", "30",
             "--no-playlist", "--print", "after_move:filepath",
             "-o", template, url],
            timeout=1800, capture=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("原片下载失败：" +
                           (exc.stderr or str(exc)).strip()[-300:]) from exc
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("原片下载超时（1800s）；请检查链接与网络后重试") from exc
    paths = [os.path.abspath(line.strip()) for line in (r.stdout or "").splitlines()
             if line.strip() and os.path.isfile(line.strip())]
    if not paths or os.path.getsize(paths[-1]) == 0:
        raise RuntimeError("yt-dlp 未报告有效的原片保留路径：" +
                           (r.stdout or "").strip()[-200:])
    return paths[-1]


def audio_from_video(video_path: str, tmpdir: str) -> str:
    """已有保留原片时复用它提取转录音频，避免再下一遍音频。"""
    audio_path = os.path.join(tmpdir, "audio.mp3")
    try:
        subprocess.run(
            [deps.ensure_ffmpeg(), "-y", "-v", "error", "-i", video_path,
             "-vn", "-acodec", "libmp3lame", "-ab", "128k", audio_path],
            capture_output=True, text=True, timeout=600, check=True,
        )
    except subprocess.CalledProcessError as exc:
        raise RuntimeError("从保留原片提取音频失败：" +
                           (exc.stderr or "").strip()[-200:]) from exc
    return audio_path


# ---------------------------------------------------------------- 字幕层

def bilibili_subtitles(url: str, tmpdir: str, notes: list):
    """字幕优先：秒级、免 GPU。返回 (text, lang, timed) 或 None。

    B 站 AI 字幕只提供 srt（指定 vtt 也仍落盘 .srt），且需登录 cookie 才可见。
    """
    try:
        ytdlp.run_ydl(
            BILI,
            ["--skip-download", "--write-subs", "--write-auto-subs",
             "--sub-langs", SUB_LANGS, "--sub-format", "srt/vtt/best",
             "-o", os.path.join(tmpdir, "sub.%(ext)s"), url],
            timeout=150, capture=True,
        )
    except Exception as exc:
        notes.append(f"字幕抓取异常：{str(exc)[:120]}")
        return None
    files = vtt.find_subtitle_files(tmpdir)
    if not files:
        notes.append("无字幕：本机浏览器未登录 B 站，或该视频确实无 AI/CC 字幕。"
                     f"（cookie 探测：{cookies.describe('bilibili.com')}）")
        return None
    chosen = vtt.pick_subtitle(files, SUB_PRIORITY)
    text = vtt.parse_vtt(chosen)
    if len(text) < 50:
        notes.append(f"字幕过短（{len(text)} 字），按无字幕处理")
        return None
    lang = "zh" if re.search(r"[一-鿿]", text) else "en"
    return {"text": text, "lang": lang, "timed": vtt.parse_subtitle_timed(chosen),
            "file": os.path.basename(chosen)}


# ---------------------------------------------------------------- 主流程# ---------------------------------------------------------------- 主流程

def run(url: str, want_look: bool, frames, timestamps, max_minutes,
        no_subtitle: bool = False, look_height: int = 480,
        keep_video: str = None) -> dict:
    notes = []
    platform = detect(url)
    keep_dir = os.path.abspath(keep_video) if keep_video else None
    if keep_dir:
        os.makedirs(keep_dir, exist_ok=True)
    kept_video_path = None
    tmpdir = tempfile.mkdtemp(prefix="svu-")
    try:
        if platform == "bilibili":
            if "b23.tv" in url and not re.search(r"(BV[\w]+)", url):
                url = expand_bilibili_short_url(url)
            bvid = re.search(r"(BV[\w]+)", url).group(1)
            canon = normalize(url, platform)
            meta = bilibili_info(canon, bvid)
            if keep_dir:
                kept_video_path = download_kept_video(BILI, canon, keep_dir)
            text, lang, timed, transcriber = None, "zh", None, None

            if not no_subtitle:
                sub = bilibili_subtitles(canon, tmpdir, notes)
                if sub:
                    text, lang, timed = sub["text"], sub["lang"], sub["timed"]
                    transcriber = f"字幕:{sub['file']}"

            if text is None:
                audio = (audio_from_video(kept_video_path, tmpdir) if kept_video_path else
                         ytdlp.download_audio(BILI, canon, tmpdir, filename="audio.mp3"))
                text = asr.transcribe(audio, language="zh")[0]
                transcriber = asr.backend_label()

            result = {"platform": "bilibili", "source": canon, "bvid": bvid,
                      "title": meta["title"], "author": meta["author"],
                      "duration": meta["duration"], "language": lang,
                      "transcriber": transcriber, "text": text}
            if timed:
                result["timed"] = [[t, s] for t, s in timed[:400]]
            source_url = kept_video_path or canon

        elif platform == "douyin":
            from chubby_common import douyin

            # 抖音的 mp4 自带音轨：要画面层或保留原片时下一次就够，避免二次拉 CDN
            local_video = None
            if want_look or keep_dir:
                local_video = os.path.join(keep_dir or tmpdir, "source.mp4")
                info = douyin.download_video(url, local_video, notes)
                audio = douyin.extract_audio(local_video, os.path.join(tmpdir, "audio.mp3"))
                title = info["title"]
                if keep_dir:
                    kept_video_path = os.path.abspath(local_video)
            else:
                audio, title = douyin.download_audio(url, tmpdir, notes)
            text = asr.transcribe(audio, language="zh")[0]
            result = {"platform": "douyin", "source": url, "title": title,
                      "author": "", "duration": 0.0, "language": "zh",
                      "transcriber": asr.backend_label(), "text": text}
            source_url = local_video or url
        else:
            cfg = PlatformConfig(id="generic", name="通用", tag="视频",
                                 default_title="视频", cookie_domain=_domain_of(url))
            meta_t = ytdlp.get_title(cfg, url)
            if keep_dir:
                kept_video_path = download_kept_video(cfg, url, keep_dir)
            audio = (audio_from_video(kept_video_path, tmpdir) if kept_video_path else
                     ytdlp.download_audio(cfg, url, tmpdir, filename="audio.mp3"))
            text = asr.transcribe(audio, language="auto")[0]
            result = {"platform": "other", "source": url, "title": meta_t,
                      "author": "", "duration": 0.0, "language": "auto",
                      "transcriber": asr.backend_label(), "text": text}
            source_url = kept_video_path or url

        if kept_video_path:
            result["video_path"] = kept_video_path
            print("  ✅ 原片保留：%s" % kept_video_path, file=sys.stderr)
        if max_minutes and result.get("duration", 0) > max_minutes * 60:
            notes.append(f"视频 {result['duration']/60:.1f} 分钟超过 --max-minutes="
                         f"{max_minutes}，文字稿仍为全量，画面层帧数已按上限压缩")

        if want_look:
            shots = _look(source_url, tmpdir, frames, timestamps, notes, look_height)
            if shots:
                result["shots"] = shots
        result["notes"] = notes
        return result
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


def _domain_of(url: str) -> str:
    m = re.search(r"https?://(?:[\w-]+\.)*([\w-]+\.[\w.]+)", url)
    return m.group(1) if m else ""


def _look(url, tmpdir, frames, timestamps, notes, height=480) -> list:
    """调用同目录的 look.py 做抽帧+识图，失败只记 notes 不影响文字稿。"""
    look = os.path.join(HERE, "scripts", "look.py")
    if os.path.isfile(url):
        # 已是本地文件（抖音 --look 复用同一次下载）：直接抽帧，不再拉 CDN
        cmd = [sys.executable, look, url, "--json"]
    else:
        cmd = [sys.executable, look, "--video-url", url, "--json", "--height", str(height)]
    if frames:
        cmd += ["--frames", str(frames)]
    if timestamps:
        cmd += ["--timestamps", timestamps]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=1800)
    if r.returncode != 0:
        notes.append(f"画面层失败：{(r.stderr or '').strip()[-200:]}")
        return []
    try:
        d = json.loads(r.stdout[r.stdout.index("{"):])
        return d.get("shots", [])
    except (ValueError, json.JSONDecodeError):
        notes.append("画面层输出解析失败")
        return []


def to_markdown(res: dict) -> str:
    lines = [f"# {res.get('title') or res.get('source')}", "",
             f"- 平台：{res.get('platform')}｜来源：{res.get('source')}",
             f"- 作者：{res.get('author') or '未知'}｜时长：{res.get('duration', 0):.0f}s",
             f"- 文本来源：{res.get('transcriber')}"]
    if res.get("video_path"):
        lines.append(f"- 原片保留：{res['video_path']}")
    lines.append("")
    if res.get("notes"):
        lines += ["## 处理说明", ""] + [f"- {n}" for n in res["notes"]] + [""]
    lines += ["## 文字稿", "", res.get("text", "").strip(), ""]
    if res.get("timed"):
        lines += ["## 带时间轴逐句稿", "", "```"]
        lines += [f"[{t}] {s}" for t, s in res["timed"]]
        lines += ["```", ""]
    if res.get("shots"):
        lines += ["## 画面层（抽帧识别）", ""]
        for s in res["shots"]:
            lines += [f"### [{s['t']:.1f}s]", "", s["description"], ""]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="短视频链接 → 结构化可读证据")
    ap.add_argument("url", help="B站/抖音链接、BV 号，或任意 yt-dlp 支持的视频链接")
    ap.add_argument("--look", action="store_true", help="附加画面层（抽帧 + 多模态识图）")
    ap.add_argument("--frames", type=int, default=6, help="画面层均匀抽帧数（默认 6）")
    ap.add_argument("--timestamps", help="画面层指定秒数，逗号分隔，如 0,45,90")
    ap.add_argument("--height", type=int, default=480,
                    help="画面层下载视频轨最大高度（默认 480；小字/OCR 密集提到 720）")
    ap.add_argument("--keep-video", metavar="DIR",
                    help="可选：下载最高可用画质的完整音视频并保留到 DIR，输出实际路径")
    ap.add_argument("--no-subtitle", action="store_true", help="跳过字幕，强制音频转录")
    ap.add_argument("--max-minutes", type=float, default=0,
                    help="仅用于提示：超过该时长的视频建议只看前半段")
    ap.add_argument("--output", "-o", help="把 Markdown 写到该路径")
    ap.add_argument("--markdown", action="store_true", help="stdout 输出 Markdown 而非 JSON")
    args = ap.parse_args()

    try:
        res = run(args.url, args.look, args.frames, args.timestamps,
                  args.max_minutes, args.no_subtitle, args.height, args.keep_video)
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
        # 失败也要给 Agent 可执行的处置，而不是裸 traceback。
        print(f"❌ 处理失败：{exc}", file=sys.stderr)
        print(_advice(args.url, str(exc)), file=sys.stderr)
        return 2
    body = to_markdown(res)
    if args.output:
        os.makedirs(os.path.dirname(os.path.abspath(args.output)), exist_ok=True)
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(body + "\n")
        print(os.path.abspath(args.output))
    elif args.markdown:
        print(body)
    else:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


def _advice(url: str, err: str) -> str:
    """按平台与错误串给出下一步建议。判断顺序：链接形态 → 平台 → 认证/风控。"""
    if "is not a valid URL" in err or "无法从输入中提取" in err or "video id" in err:
        if "v.douyin" in url or "douyin" in url:
            return ("   处置：抖音 v.douyin.com 短链会过期。请重新在 App 里「分享 → 复制链接」"
                    "取新链接；仍失败则贴 https://www.douyin.com/video/<id> 完整链接。")
        return ("   处置：这不是可解析的视频链接。请贴完整的 https:// 视频页地址"
                "（B 站也可只给 BV 号）。")
    if "bilibili" in url or "b23.tv" in url or re.search(r"BV\w+", url):
        return ("   处置：确认 BV 号有效（稿件被删除/仅自己可见会取不到）；"
                "合集链接请指到具体分 P。b23.tv 短链可先在浏览器打开换成完整链接。")
    if "Fresh cookies" in err or "403" in err or "蜘蛛壳" in err or "cookie" in err.lower():
        return ("   处置：用本机浏览器打开一次该平台首页（抖音建议登录），"
                "让 cookie 变新鲜后重试；浏览器从未访问过该平台时无法解锁 B 站 AI 字幕。")
    return "   处置：检查链接是否有效、网络是否可达；必要时重跑并保留 stderr 排障。"


if __name__ == "__main__":
    sys.exit(main())
