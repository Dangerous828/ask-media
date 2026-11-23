"""可插拔音频转录后端：优先 mlx-whisper（Apple Silicon，零新增重依赖），回退 SenseVoice。

原实现只支持 funasr/SenseVoice，需要 `pip install funasr modelscope torch torchaudio`
（约 2GB）。在 Apple Silicon 机器上 mlx-whisper 常有本地缓存，几十秒即可跑完一段音频，
故这里把后端选择收敛为数据驱动的探测顺序，而不是改每个平台脚本。

可用环境变量覆盖：
  CHUBBY_ASR_BACKEND = mlx_whisper | funasr   （指定单一后端，跳过探测）
  CHUBBY_MLX_MODEL   = 模型仓库名/本地路径     （默认 mlx-community/whisper-large-v3-mlx）
"""

import os
import shutil
import sys
import time

from chubby_common import deps

DEFAULT_MLX_MODEL = "mlx-community/whisper-large-v3-mlx"  # 本地有完整 2.9G 权重；turbo 是空壳

# 探测顺序：本机已有的轻量后端优先，重依赖后端兜底。
ORDER = ("mlx_whisper", "funasr")


def _forced():
    name = os.environ.get("CHUBBY_ASR_BACKEND", "").strip()
    return name or None


def _try(name):
    """返回 (可用?, 不可用原因)。"""
    if name == "mlx_whisper":
        import importlib.util

        if importlib.util.find_spec("mlx_whisper") is None:
            return False, "未安装 mlx-whisper（pip install mlx-whisper）"
        return True, ""
    if name == "funasr":
        import importlib.util

        if importlib.util.find_spec("funasr") is None:
            return False, "未安装 funasr"
        return True, ""
    return False, f"未知后端 {name}"


def pick_backend():
    """按探测顺序选出可用后端，返回 (后端名, 不可用提示)。"""
    forced = _forced()
    candidates = (forced,) if forced else ORDER
    notes = []
    for name in candidates:
        ok, why = _try(name)
        if ok:
            return name, ""
        notes.append(f"{name}: {why}")
    return None, " | ".join(notes)


def backend_label():
    """给 frontmatter 用的后端名，全不可用时返回占位名。"""
    name, _ = pick_backend()
    return {"mlx_whisper": "Whisper-large-v3-mlx (MLX)", "funasr": "SenseVoice-Small"}.get(
        name, "未知"
    )


def _ensure_ffmpeg_on_path():
    """mlx_whisper 内部用裸 'ffmpeg' 装载音频，会按 PATH 查找。

    Agent shell 的 PATH 常常没有 /opt/homebrew/bin，这里把 ffmpeg 所在目录补进
    PATH，避免「依赖检查通过了、内部调用却 FileNotFoundError」。
    """
    if shutil.which("ffmpeg"):
        return
    exe = deps.find_executable("ffmpeg")
    if not exe:
        return
    os.environ["PATH"] = os.path.dirname(exe) + os.pathsep + os.environ.get("PATH", "")


def _transcribe_mlx(audio_path: str, language: str) -> tuple:
    import mlx_whisper

    model = os.environ.get("CHUBBY_MLX_MODEL", "").strip() or DEFAULT_MLX_MODEL
    print(f"  🎙️  Loading MLX model: {model}...", file=sys.stderr)
    start = time.time()
    kwargs = {"language": None if language in ("", "auto") else language}
    result = mlx_whisper.transcribe(audio_path, path_or_hf_repo=model, verbose=False, **kwargs)
    elapsed = time.time() - start
    text = (result.get("text") or "").strip()
    print(f"  ✅ Done in {elapsed:.1f}s", file=sys.stderr)
    return text, elapsed


def _transcribe_funasr(audio_path: str, language: str) -> tuple:
    return funasr_transcribe(audio_path, language)


def funasr_transcribe(audio_path: str, language: str) -> tuple:
    from chubby_common import funasr

    return funasr.transcribe(audio_path, language=language)


def transcribe(audio_path: str, language: str = "auto") -> tuple:
    """转录音频，返回 (text, elapsed_seconds)。无可用后端时 exit 1。"""
    deps.ensure_ffmpeg()
    _ensure_ffmpeg_on_path()
    name, why = pick_backend()
    if name is None:
        print("❌ 没有可用的音频转录后端。", file=sys.stderr)
        print(f"   探测结果：{why}", file=sys.stderr)
        print("   任选其一安装：", file=sys.stderr)
        print("     Apple Silicon: pip install mlx-whisper   （推荐，无需 torch）", file=sys.stderr)
        print("     通用:          bash setup.sh video       （funasr+torch，约 2GB）", file=sys.stderr)
        raise SystemExit(1)

    print(f"  🎙️  ASR 后端：{name}", file=sys.stderr)
    if name == "mlx_whisper":
        return _transcribe_mlx(audio_path, language)
    return _transcribe_funasr(audio_path, language)
