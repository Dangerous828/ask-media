"""VTT 字幕解析与语言优先级挑选（B 站 / YouTube 共用）。"""

import glob
import os
import re


def parse_vtt(path: str) -> str:
    """把 vtt 字幕解析成纯文本：去时间轴、去标签、去连续重复行。"""
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = f.read().splitlines()
    out = []
    for line in lines:
        line = line.strip()
        if not line or line == "WEBVTT" or "-->" in line:
            continue
        if line.isdigit() or line.startswith(("Kind:", "Language:", "NOTE")):
            continue
        line = re.sub(r"<[^>]+>", "", line).replace("&nbsp;", " ").strip()
        if not line or (out and out[-1] == line):
            continue
        out.append(line)
    return "\n".join(out)


def pick_subtitle(files, priority: tuple) -> str:
    """按语言优先级从 vtt 文件列表中挑选最合适的。"""
    def rank(path):
        name = os.path.basename(path).lower()
        for index, tag in enumerate(priority):
            if tag in name:
                return index
        return 99

    return sorted(files, key=rank)[0]


def find_vtt_files(tmpdir: str) -> list:
    return glob.glob(os.path.join(tmpdir, "*.vtt"))


def find_subtitle_files(tmpdir: str) -> list:
    """字幕落盘扩展名因平台而异：B 站 AI 字幕即使指定 --sub-format vtt 也会存成 .srt。

    只扫 *.vtt 会让「字幕优先」在 B 站必然落空并回退音频转录，故一并扫 .srt。
    """
    found = []
    for ext in ("*.vtt", "*.srt"):
        found.extend(glob.glob(os.path.join(tmpdir, ext)))
    return found


def parse_subtitle_timed(path: str) -> list:
    """把 vtt/srt 解析成 [(HH:MM:SS, text), ...]，供带时间轴的审计稿使用。"""
    with open(path, encoding="utf-8", errors="replace") as f:
        lines = [l.strip() for l in f.read().splitlines()]
    stamp = re.compile(r"(\d{2}:\d{2}:\d{2})[.,]\d{3}\s*-->")
    out = []
    for i, line in enumerate(lines):
        m = stamp.search(line)
        if not m:
            continue
        body = []
        for nxt in lines[i + 1:]:
            if not nxt or "-->" in nxt or nxt.isdigit():
                break
            body.append(re.sub(r"<[^>]+>", "", nxt).replace("&nbsp;", " ").strip())
        text = " ".join(b for b in body if b)
        if text:
            out.append((m.group(1), text))
    return out
