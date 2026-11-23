"""抖音取流公共模块：分享页解析 + 无水印直链 + cookie 拼装。

下沉理由：transcribe 与画面层（look）都需要「拿到抖音的视频文件/标题」，
上游把它们写在 douyin-transcribe/scripts/download_douyin_audio.py 里，第二个调用方
只能靠 sys.path 硬引，改一处要改两份。这里作为唯一实现。

关键实测结论（2026-10-24）：
- yt-dlp 对 douyin.com 稳定 `HTTP 403 / Fresh cookies needed`，不要走 yt-dlp 下载。
- 必须走 `https://www.iesdouyin.com/share/video/<id>` + iPhone UA，解析
  `window._ROUTER_DATA`，取 `play_addr.url_list[0]` 并把 `playwm` 换成 `play` 去水印。
- 无 cookie 时分享页返回蜘蛛壳（loaderData 里没有 videoInfoRes）。
- cookie 不能交给 `curl -b <netscape 文件>`：浏览器里存的是 `.douyin.com`，
  按域匹配不覆盖 `iesdouyin.com`（两者可注册域不同），实测等于没带 cookie。
  必须把条目显式拼成 `Cookie:` 头发送。
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

from chubby_common import cookies, deps

MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1"
)

# 载体 URL 只为让 yt-dlp 走完「浏览器 cookie 解密 + 导出」，其自身报错不影响导出结果。
_PROBE_URL = "https://example.com/"


def extract_video_id(url: str) -> str:
    """从抖音完整链接或 v.douyin.com 短链取 video id。"""
    m = re.search(r"/video/(\d+)", url)
    if m:
        return m.group(1)
    m = re.search(r"modal_id=(\d+)", url)
    if m:
        return m.group(1)
    if "v.douyin.com" in url:
        r = subprocess.run(
            ["curl", "-sI", "-L", "-H", f"User-Agent: {MOBILE_UA}", url],
            capture_output=True, text=True, timeout=20,
        )
        m = re.search(r"/video/(\d+)", r.stdout)
        if m:
            return m.group(1)
    raise ValueError(f"无法从抖音链接提取 video id：{url}")


def parse_share_page(html: str):
    """解析分享页 → {title, video_url}；蜘蛛壳/结构变化返回 None。"""
    m = re.search(r"window\._ROUTER_DATA\s*=\s*(.*?)</script>", html, re.DOTALL)
    if not m:
        return None
    try:
        data = json.loads(m.group(1).strip())
        item = data["loaderData"]["video_(id)/page"]["videoInfoRes"]["item_list"][0]
        url_list = item["video"]["play_addr"]["url_list"]
        return {
            "title": item.get("desc") or "抖音视频",
            "video_url": url_list[0].replace("playwm", "play"),
        }
    except (KeyError, IndexError, TypeError, ValueError):
        return None


def cookie_header(notes: list = None):
    """返回可直接放进 `Cookie:` 头的字符串；拿不到返回 None。

    优先级：DOUYIN_COOKIES > DOUYIN_COOKIE_FILE/YTDLP_COOKIES_FILE >
    YTDLP_COOKIES_FROM_BROWSER > 自动探测本机登录过的浏览器。
    浏览器导出只写进临时目录，读完立即删除，凭据不长期留盘。
    """
    notes = notes if notes is not None else []
    raw = os.environ.get("DOUYIN_COOKIES", "").strip()
    if raw:
        return raw

    path, owned = "", None
    for var in ("DOUYIN_COOKIE_FILE", "YTDLP_COOKIES_FILE"):
        p = os.environ.get(var, "").strip()
        if p and os.path.isfile(p):
            path = p
            break
    if not path:
        browser = os.environ.get("YTDLP_COOKIES_FROM_BROWSER", "").strip() or cookies.resolve(
            "douyin.com"
        )
        if not browser:
            notes.append(f"无抖音 cookie：{cookies.describe('douyin.com')}")
            return None
        owned = tempfile.mkdtemp(prefix="dyck-")
        path = os.path.join(owned, "cookies.txt")
        try:
            subprocess.run(
                deps.yt_dlp_cmd() + ["--cookies-from-browser", browser, "--cookies", path,
                                     "--skip-download", "--simulate", _PROBE_URL],
                capture_output=True, text=True, timeout=180,
            )
        except Exception as exc:
            notes.append(f"浏览器 cookie 导出失败：{str(exc)[:100]}")

    pairs = []
    try:
        with open(path, encoding="utf-8", errors="replace") as f:
            for line in f:
                if line.startswith("#") or not line.strip():
                    continue
                p = line.rstrip("\n").split("\t")
                if len(p) >= 7 and "douyin" in p[0] and p[5]:
                    pairs.append(f"{p[5]}={p[6]}")
    except OSError:
        notes.append("cookie 文件读取失败")
    if owned:
        shutil.rmtree(owned, ignore_errors=True)
    if not pairs:
        notes.append("cookie 文件里没有 douyin 条目")
        return None
    return "; ".join(pairs)


def fetch_info(url: str, notes: list = None) -> dict:
    """取 {video_id, title, video_url}。被风控时抛 RuntimeError 并给出可执行处置。"""
    notes = notes if notes is not None else []
    vid = extract_video_id(url)
    cmd = ["curl", "-s", "-L", "-H", f"User-Agent: {MOBILE_UA}"]
    ck = cookie_header(notes)
    if ck:
        cmd += ["-H", f"Cookie: {ck}"]
    cmd += [f"https://www.iesdouyin.com/share/video/{vid}"]
    try:
        html = subprocess.run(cmd, capture_output=True, text=True, timeout=40).stdout
    except subprocess.TimeoutExpired:
        raise RuntimeError("抖音分享页请求超时（40s），稍后重试或改用 App 内分享短链")
    info = parse_share_page(html)
    if info is None:
        notes.append(
            "分享页返回蜘蛛壳（风控）。处置：用本机浏览器打开一次 "
            "https://www.douyin.com 后重试；或改用 App 里「复制链接」得到的 v.douyin.com 短链。"
        )
        raise RuntimeError(f"抖音分享页无视频数据（video_id={vid}），需要新鲜浏览器 cookie")
    info["video_id"] = vid
    return info


def download_video(url: str, dst: str, notes: list = None) -> dict:
    """下载抖音视频到 dst，返回 fetch_info 的结果。"""
    info = fetch_info(url, notes)
    subprocess.run(
        ["curl", "-s", "-L", "-o", dst, "-H", f"User-Agent: {MOBILE_UA}",
         "-H", "Referer: https://www.douyin.com/", info["video_url"]],
        timeout=600, check=True,
    )
    if not os.path.isfile(dst) or os.path.getsize(dst) < 1024:
        raise RuntimeError(f"抖音视频下载结果为空/过小：{dst}（链接可能已失效）")
    return info


def extract_audio(video_path: str, audio_path: str) -> str:
    """mp4 → mp3（128k）。用绝对 ffmpeg 路径，Agent 的最小 PATH 常不含 brew。"""
    subprocess.run(
        [deps.ensure_ffmpeg(), "-y", "-i", video_path, "-vn",
         "-acodec", "libmp3lame", "-ab", "128k", audio_path],
        capture_output=True, timeout=600, check=True,
    )
    return audio_path


def download_audio(url: str, output_dir: str = None, notes: list = None) -> tuple:
    """抖音 → (mp3 路径, 标题)。上游脚本入口，保持原返回契约。"""
    deps.ensure_ffmpeg()
    if output_dir is None:
        output_dir = tempfile.mkdtemp(prefix="dyt-")
    info = fetch_info(url, notes)
    vid = info["video_id"]
    video_path = os.path.join(output_dir, f"{vid}.mp4")
    print(f"Downloading: {info['title'][:60]}...", file=sys.stderr)
    subprocess.run(
        ["curl", "-s", "-L", "-o", video_path, "-H", f"User-Agent: {MOBILE_UA}",
         "-H", "Referer: https://www.douyin.com/", info["video_url"]],
        timeout=600, check=True,
    )
    print(f"  Video: {os.path.getsize(video_path) / 1048576:.1f} MB", file=sys.stderr)
    audio_path = extract_audio(video_path, os.path.join(output_dir, f"{vid}.mp3"))
    os.remove(video_path)
    print(f"  Audio: {os.path.getsize(audio_path) / 1048576:.1f} MB", file=sys.stderr)
    return audio_path, info["title"]
