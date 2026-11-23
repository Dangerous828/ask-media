"""依赖体检：在脚本入口和关键步骤前检查系统命令 / Python 包。

缺失时给出可执行的安装提示（指向 setup.sh 档位），而不是裸 traceback。
"""

import importlib.util
import os
import shutil
import sys


def check_command(name: str, hint: str) -> None:
    """检查系统命令是否存在，缺失时打印提示并以 exit 1 退出。"""
    if shutil.which(name) is None:
        print(f"❌ 未找到系统命令 `{name}`。", file=sys.stderr)
        print(f"   请安装：{hint}", file=sys.stderr)
        print("   装完后重新运行本脚本。", file=sys.stderr)
        raise SystemExit(1)


def check_python_module(name: str, hint: str) -> None:
    """检查 Python 包是否可导入，缺失时打印提示并以 exit 1 退出。"""
    try:
        spec = importlib.util.find_spec(name)
    except (ImportError, ValueError):
        spec = None
    if spec is None:
        print(f"❌ 缺少 Python 依赖 `{name}`。", file=sys.stderr)
        print(f"   请安装：{hint}", file=sys.stderr)
        print("   装完后重新运行本脚本。", file=sys.stderr)
        raise SystemExit(1)


def find_executable(name: str) -> str:
    """定位可执行文件：PATH 优先，再试常见安装位置。

    Agent 的 shell PATH 常不含 ~/.local/bin（uv tool）与 /opt/homebrew/bin（brew），
    直接 shutil.which 会误报「未安装」。返回 None 表示真的没装。
    """
    found = shutil.which(name)
    if found:
        return found
    candidates = [
        os.path.expanduser(f"~/.local/bin/{name}"),
        f"/opt/homebrew/bin/{name}",
        f"/usr/local/bin/{name}",
        os.path.expanduser(f"~/Library/Python/3.9/bin/{name}"),
    ]
    for c in candidates:
        if os.access(c, os.X_OK):
            return c
    return None


def yt_dlp_cmd() -> list:
    """yt-dlp 的调用前缀：找得到二进制就用二进制，否则退回 python -m yt_dlp。"""
    exe = find_executable("yt-dlp")
    if exe:
        return [exe]
    if importlib.util.find_spec("yt_dlp") is not None:
        return [sys.executable, "-m", "yt_dlp"]
    return None


def ensure_ytdlp() -> list:
    """转录流程前的 yt-dlp 检查，返回可用的调用前缀。"""
    cmd = yt_dlp_cmd()
    if cmd is None:
        print("❌ 未找到 `yt-dlp`。", file=sys.stderr)
        print("   请安装：bash setup.sh video 或 pip install -U yt-dlp", file=sys.stderr)
        print("   装完后重新运行本脚本。", file=sys.stderr)
        raise SystemExit(1)
    return cmd


def ensure_ffmpeg() -> str:
    """yt-dlp 转音频需要 ffmpeg。返回可执行文件绝对路径。"""
    exe = find_executable("ffmpeg")
    if exe is None:
        print("❌ 未找到系统命令 `ffmpeg`。", file=sys.stderr)
        print("   请安装：macOS: brew install ffmpeg  |  Ubuntu: sudo apt install ffmpeg",
              file=sys.stderr)
        print("   装完后重新运行本脚本。", file=sys.stderr)
        raise SystemExit(1)
    return exe


def ffprobe_cmd() -> str:
    exe = find_executable("ffprobe")
    if exe is None:
        raise SystemExit("❌ 未找到 `ffprobe`（macOS: brew install ffmpeg）")
    return exe


def ensure_funasr() -> None:
    """音频转录前的 funasr 检查（模型加载时仍会延迟 import）。"""
    check_python_module(
        "funasr",
        "bash setup.sh video 或 pip install funasr modelscope torch torchaudio",
    )
