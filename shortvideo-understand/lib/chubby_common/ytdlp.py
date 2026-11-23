"""yt-dlp 统一封装：带平台 UA / Referer / 附加参数、依赖体检、重试和友好错误。

各平台脚本不再自己拼 yt-dlp 命令，避免「同一处修复要改 N 份拷贝」。
"""

import os
import subprocess
import sys
import time

from chubby_common import cookies, deps


def _browser_for(cfg):
    """本次调用该用哪个浏览器的 cookie：显式环境变量 > 平台 cookie_domain 自动探测。"""
    forced = os.environ.get("YTDLP_COOKIES_FROM_BROWSER", "").strip()
    if forced:
        return forced
    domain = getattr(cfg, "cookie_domain", "") or ""
    return cookies.resolve(domain) if domain else None


def run_ydl(cfg, args, timeout, capture=True):
    """统一的 yt-dlp 调用，自动带上平台的 UA / Referer / 额外参数。

    环境变量：
    - YTDLP_COOKIES_FROM_BROWSER：如 chrome / safari，传递给 --cookies-from-browser，
      用于平台把出口 IP 标记为机器人时的登录态证明。未设置时，若平台声明了
      cookie_domain，会用 chubby_common.cookies 自动探测本机登录过的浏览器。
    - YTDLP_REMOTE_COMPONENTS：如 ejs:github，YouTube JS challenge 求解组件。
    """
    deps.ensure_ytdlp()
    cmd = deps.yt_dlp_cmd() + ["--no-check-certificates", "--user-agent", cfg.ua]
    # yt-dlp 内部按 PATH 找 ffmpeg，Agent shell 常不含 /opt/homebrew/bin，显式给位置。
    ffmpeg = deps.find_executable("ffmpeg")
    if ffmpeg:
        cmd += ["--ffmpeg-location", os.path.dirname(ffmpeg)]
    browser = _browser_for(cfg)
    if browser:
        cmd += ["--cookies-from-browser", browser]
    components = os.environ.get("YTDLP_REMOTE_COMPONENTS", "").strip()
    if components:
        cmd += ["--remote-components", components]
    if cfg.referer:
        cmd += ["--referer", cfg.referer]
    cmd += list(cfg.extra_ydl_args) + list(args)
    return subprocess.run(
        cmd, capture_output=capture, text=True, timeout=timeout, check=True
    )


def get_title(cfg, url: str) -> str:
    """获取视频标题，失败回退到平台默认标题。"""
    try:
        result = run_ydl(cfg, ["--get-title", url], timeout=cfg.info_timeout, capture=True)
        return result.stdout.strip() or cfg.default_title
    except Exception:
        return cfg.default_title


def download_audio(cfg, url: str, output_dir: str, filename: str = "audio.mp3") -> str:
    """下载音频为 mp3，失败自动重试，全部失败时抛可读 RuntimeError。"""
    audio_path = os.path.join(output_dir, filename)
    last_err = None
    for attempt in range(1, cfg.max_retry + 1):
        try:
            print(
                f"  ⬇️  Downloading (attempt {attempt}/{cfg.max_retry})...",
                file=sys.stderr,
            )
            run_ydl(
                cfg,
                [
                    "--extract-audio",
                    "--audio-format",
                    "mp3",
                    "--audio-quality",
                    "128K",
                    "-o",
                    audio_path,
                    url,
                ],
                timeout=cfg.download_timeout,
            )
            if not os.path.exists(audio_path):
                raise RuntimeError(
                    f"yt-dlp 退出成功但未产出音频文件：{audio_path}，链接可能已失效"
                )
            size_mb = os.path.getsize(audio_path) / (1024 * 1024)
            print(f"  ✅ Audio: {size_mb:.1f} MB", file=sys.stderr)
            return audio_path
        except subprocess.CalledProcessError as exc:
            last_err = f"yt-dlp 退出码 {exc.returncode}"
            if exc.stderr and exc.stderr.strip():
                last_err += f"：{exc.stderr.strip()}"
            print(f"  ⚠️  下载失败，{2 * attempt}s 后重试...", file=sys.stderr)
            time.sleep(2 * attempt)
        except subprocess.TimeoutExpired as exc:
            last_err = exc
            print("  ⚠️  下载超时，重试...", file=sys.stderr)
    hint = "可能原因：链接失效、需要登录 cookie、或平台限制。"
    if "403" in str(last_err) or "Forbidden" in str(last_err):
        # Measured 2026-10-05: a YouTube subtitle/download attempt 403s without
        # this, and succeeds with it. Naming the actual lever beats a generic
        # "platform restriction".
        hint += (
            "\n   403 多见于 YouTube 反爬：先设 YTDLP_REMOTE_COMPONENTS=ejs:github"
            "（JS 挑战求解组件），仍失败再加 YTDLP_COOKIES_FROM_BROWSER=<浏览器名>。"
        )
    raise RuntimeError(
        f"{cfg.name} 下载失败（已重试 {cfg.max_retry} 次）。{hint}原始错误：{last_err}"
    )
