#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
h3_gate.py —— MiniMax H3「视频提示词」交稿前机械闸门。

只用 Python 3.9+ 标准库,不联网。Mac 的 python3 与 Windows Python 3.12 均可运行。

用法:
    python3 h3_gate.py FILE [FILE...] [--mode auto|ref|base|multishot]
                       [--frames N | --seconds S] [--refs N] [--rate R]
                       [--series-config FILE.json] [--json] [--strict] [-v]

退出码:
    0 = 没有 error
    1 = 有 error(--strict 时 warn 也算失败)
    2 = 用法错误 / 文件读取错误 / 配置错误

规则 ID 与阈值见本仓库 `h3-video-gate/SKILL.md` §4 规则表(G01–G26,G08b,S01–S04;G23–G26 依据官方 ref-en/base-en 补充)。
多文件时,命令行顺序即镜序 S1..Sn,并额外运行 series 检查。
"""
from __future__ import annotations

import argparse
import difflib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Callable, Dict, List, Optional, Sequence, Set, Tuple

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

FPS = 24
NODE_MAX_FRAMES = 3600                       # MiniMaxH3ReferenceToVideo.length 节点硬上限(实测 object_info max=3600,step17)
NODE_MAX_SECONDS = NODE_MAX_FRAMES / FPS     # 150.0
LOCAL_SAFE_SECONDS = 15                      # 本地 16G 容量/官方训练范围 124-362f 的安全上限,非节点能力上限
# lib_workflow.seconds_to_frames: round(seconds * 24), then snap up to 17k+5.
# 15s -> 360 requested frames -> 362 physical frames (15.083333s), not 365.
LOCAL_MAX_FRAMES = 17 * ((LOCAL_SAFE_SECONDS * FPS - 5 + 16) // 17) + 5
TIME_TOL = 0.5 / FPS
DIALOGUE_OVERRUN_ERR_S = 0.6  # G18:估算结束时间超出总时长多少秒才算 error(语速是经验估计,成人更快,小幅超出只 warn)
OVERLAP_WARN_S = 0.3          # G18:不同说话人台词重叠超过该秒数即 warn
NEG_WINDOW = 12               # G22/S01/S03:否定词回看字符数
LIPS_WINDOW = 350             # G17:<d> 前后查找 off-screen / lips / closed 的窗口
SPEAKER_WINDOW = 120          # S04:(Sx) 前查找角色关键词的窗口
WORDS_MIN, WORDS_MAX = 150, 600

REF_ORDER = [
    "subject_definitions",
    "summary",
    "retention_analysis",
    "detailed_description",
    "overall_soundscape",
    "non_diegetic_music",
]
BASE_ORDER = [
    "integrated_multimodal_description",
    "overall_soundscape",
    "non_diegetic_music",
]
ALL_SECTIONS = sorted(set(REF_ORDER) | set(BASE_ORDER), key=len, reverse=True)
NA_OK = {"overall_soundscape", "non_diegetic_music"}

VISUAL_MARKERS = {"fully_preserved", "partially_preserved", "attribute_transfer", "weak_reference"}
AUDIO_MARKERS = {"fully_copy", "partially_copy", "reference", "weak_reference"}

_NAMES = "|".join(ALL_SECTIONS)
HEADER_RE = re.compile(r"(?m)^(%s)[ \t]*:" % _NAMES)
INDENTED_HEADER_RE = re.compile(r"(?m)^[ \t]+(%s)[ \t]*:" % _NAMES)
NOCOLON_HEADER_RE = re.compile(r"(?m)^(%s)[ \t]*$" % _NAMES)

LABEL_RE = re.compile(r"<(Subject|Picture|Video|Audio) (\d+)>")
# 官方 FL2VA/L2VA 的对齐句写作 'Picture 1 (from Shot 1)'，不带尖括号
# （base-en.txt §3.2 与 Case 3 / Case 4 示例原文即如此，L2VA 示例则带尖括号）。
# G08/G08b 若只认 <Picture N>，会把「首尾帧已正确标注」的合规提示词
# 误判成「上传了未标注的参考图」。此宽松形式仅用于 G08 的计数，
# 不影响 G06/G07 等依赖严格标签起始的规则。
LABEL_RE_ANY = re.compile(
    r"<(Subject|Picture|Video|Audio) (\d+)>"
    r"|(?<![<\w])(Subject|Picture|Video|Audio) (\d+)(?![>\w])")
LABEL_START = r"<(?:Subject|Picture|Video|Audio) \d+>"
DEF_START_RE = re.compile(r"^<(Subject|Picture|Video|Audio) (\d+)>\s+is\b")
TS_RE = re.compile(r"(?<![\d:])(\d{2}):(\d{2})\.(\d{3})(?!\d)")
RANGE_RE = re.compile(r"(\d{2}:\d{2}\.\d{3})\s*(?:and|to|-|–|—)\s*(\d{2}:\d{2}\.\d{3})")
START_RE = re.compile(r"\b(?:At|at|Between|between|From|from)\s+(\d{2}:\d{2}\.\d{3})")
SHOT_RE = re.compile(r"\[Shot (\d+)\]")
SPK_RE = re.compile(r"\(S(\d+)(?:\s*,\s*S\d+)*\)")
D_TAG_RE = re.compile(r"<(/?)d>")
D_CONTENT_RE = re.compile(r"\s*\[([A-Za-z][A-Za-z \-]*)\]\s*(\S[\s\S]*?)\s*$")
HAN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
CJK_RE = re.compile(r"[\u3000-\u303f\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff00-\uffef]+")
NEG_RE = re.compile(r"\b(?:no|never|not|without)\b", re.I)
EN_WORD_RE = re.compile(r"[A-Za-z]+(?:['’\-][A-Za-z]+)*")
OFFSCREEN_RE = re.compile(r"off[- ]?screen", re.I)
LIPS_RE = re.compile(r"\blips?\b", re.I)
CLOSED_RE = re.compile(r"\bclosed\b", re.I)
QUOTE_RE = re.compile(r"[\"“「『]([^\"”」』\n]{1,80})[\"”」』]")
# G15: 必须有明确的画内文字载体/义务，不能只凭 read/characters 等泛词放行。
VISIBLE_CARRIER = (r"(?:sign|signs|signage|banner|banners|label|labels|caption|subtitle|subtitles|title|inscription|poster|"
                   r"screen|display|packaging|package|neon(?:\s+(?:sign|text|lettering))?|menu|placard|plaque|"
                   r"billboard|storefront|lettering|graffiti)")
VISIBLE_RE = re.compile(
    r"\b%s\b(?:[^.!?\n\"“「『]{0,80}\b(?:reads?|reading|displays?|displaying|shows?|showing|"
    r"written|writes?|printed|labeled|labelled|stencill?ed|painted|engraved|etched|carved|"
    r"scrawled|displayed|glows?)|[^.!?\n\"“「『]{0,80}\bwith\s+the\s+words?)?\s*$"
    % VISIBLE_CARRIER,
    re.I,
)
VISIBLE_OBLIGATION_RE = re.compile(
    r"\b(?:exact[_-]readable|(?:only\s+)?(?:allowed|permitted|required)\s+"
    r"(?:visible|on[- ]screen|in[- ]scene)\s+(?:text|characters))\b[^.!?\n\"“「『]{0,80}$",
    re.I,
)
# 引号在前、动词在后的写法：A faded "禁止吸烟" is stencilled on the wall
VISIBLE_SUFFIX_RE = re.compile(
    r"^\s*(?:is|are|was|were)\s+(?:\w+\s+)?(?:stencill?ed|painted|printed|written|engraved|etched|carved|"
    r"scrawled|displayed|embroidered|lit|projected)\b", re.I)
HAN_RUN_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")
LEGACY_SUBJECT_SOURCE_RE = re.compile(r"\bfrom\s+(?:the\s+)?character\s+reference\s+images?\b", re.I)
VOICE_SUBJECT_RE = re.compile(
    r"\b(?:off[- ]screen|voiceover|voice[- ]only|audio[- ]only|narrator|narration|"
    r"disembodied\s+voice|heard\s+only)\b",
    re.I,
)
FIRST_FRAME_RE = re.compile(
    r"<Picture (\d+)>\s+(?:is|serves\s+as|acts\s+as)\s+(?:the\s+)?(?:first|opening)\s+(?:frame|composition)\b"
    r"|\b(?:begins?|starts?|opens?)\s+(?:from|on|with)\s+<Picture (\d+)>",
    re.I,
)
ANCHOR_RE = re.compile(
    r"(?:\bbegins?|\bstarts?|\bopens?|\bends?|\bending|\bcloses?|\bclosing|\blands?|\bholds?|"
    r"\bmatch(?:es|ing)?|\bcorresponds? to|\baligns? with|\bcomposition of|\bpose of|"
    r"\bframe of|\bframing of|\bas in)\b[^<.\n]{0,30}<(Picture|Video) (\d+)>",
    re.I,
)
APPEARS_RE = re.compile(r"^appears in \[Shot \d+\](?:\s*(?:,|and|, and)\s*\[Shot \d+\])*$")
ENTRY_RE = re.compile(
    r"^<(Subject|Picture|Video|Audio) (\d+)>\s*(?:\((?P<paren>[^)]*)\))?\s*:\s*"
    r"(?P<marker>[A-Za-z_]+)\s*[-–—]\s*(?P<desc>.*)$",
    re.S,
)
ALIGN_RE = re.compile(
    r"at\s+\d+(?:\.\d+)?\s+seconds?\s+into\s+the\s+target\s+video,?\s*<Picture \d+>"
    r"|how\s+the\s+reference\s+pictures\s+align\s+with\s+the\s+target\s+video\s*[—–-]+\s*<?Picture \d+>?",
    re.I,
)
SOUND_SPEECH_RE = re.compile(
    r"\b(?:says?|said|speaks?|speaking|spoke|talks?|talking|shouts?|shouting|whispers?|"
    r"whispering|dialogue|conversation)\b",
    re.I,
)
SPEAKER_GENERIC = {"voice", "narrator", "someone", "speaker", "person", "off", "screen", "on"}
TRIGGER_STOP = {"the", "and", "with", "young", "old", "little", "small", "big", "a", "an"}


# ---------------------------------------------------------------------------
# 数据结构
# ---------------------------------------------------------------------------

@dataclass
class Finding:
    level: str          # "error" | "warn" | "ok"
    rule: str
    file: str
    line: Optional[int]
    message: str

    def as_dict(self) -> dict:
        return {
            "level": self.level,
            "rule": self.rule,
            "file": self.file,
            "line": self.line,
            "message": self.message,
        }


@dataclass
class Section:
    name: str
    hpos: int       # 段名在全文中的起点
    cstart: int     # 内容起点(冒号之后)
    cend: int       # 内容终点(下一段名之前)
    text: str


@dataclass
class Dialogue:
    open_pos: int
    close_end: int
    lang: Optional[str]
    content: str
    han: int
    shot_start: int
    speaker: Optional[str] = None
    speaker_pos: Optional[int] = None
    inherited: bool = False
    start: Optional[float] = None


# ---------------------------------------------------------------------------
# 工具函数
# ---------------------------------------------------------------------------

def ts(s: str) -> float:
    mm, rest = s.split(":")
    return int(mm) * 60 + float(rest)


def fmt_ts(t: float) -> str:
    return "%02d:%06.3f" % (int(t // 60), t - 60 * int(t // 60))


def is_negated(text: str, idx: int, window: int = NEG_WINDOW) -> bool:
    """idx 处的词之前 window 个字符内是否有 no/never/not/without。"""
    start = max(0, idx - window)
    chunk = text[start:idx]
    if start > 0 and text[start - 1].isalnum():
        # 窗口切在单词中间,丢掉第一个残词,避免 "piano" 被当成 "no"
        m = re.match(r"\w*", chunk)
        chunk = chunk[m.end():] if m else chunk
    return bool(NEG_RE.search(chunk))


def word_pattern(word: str) -> re.Pattern:
    w = re.escape(word.lower())
    if word.lower() == "night":
        return re.compile(r"\bnight(?:s|time|fall|-time)?\b", re.I)
    return re.compile(r"(?<![A-Za-z])%s(?![A-Za-z])" % w, re.I)


def mask_spans(text: str, spans: Sequence[Tuple[int, int]]) -> str:
    chars = list(text)
    for a, b in spans:
        for i in range(a, b):
            if chars[i] != "\n":
                chars[i] = " "
    return "".join(chars)


def parse_sections(text: str) -> List[Section]:
    heads = list(HEADER_RE.finditer(text))
    out: List[Section] = []
    for i, m in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        out.append(Section(m.group(1), m.start(), m.end(), end, text[m.end():end]))
    return out


def pair_d_tags(text: str) -> Tuple[List[Tuple[int, int, int, int]], List[Tuple[int, str]]]:
    """返回 (<d> 配对列表 (open_start, open_end, close_start, close_end), 配对错误)。"""
    pairs: List[Tuple[int, int, int, int]] = []
    errors: List[Tuple[int, str]] = []
    open_tok = None
    for t in D_TAG_RE.finditer(text):
        if t.group(1) == "":
            if open_tok is not None:
                errors.append((open_tok.start(), "这个 <d> 在下一个 <d> 之前没有闭合。改法:在台词末尾补 </d>。"))
            open_tok = t
        else:
            if open_tok is None:
                errors.append((t.start(), "多余的 </d>,前面没有对应的 <d>。改法:删掉它或补上开头的 <d>[Language]。"))
            else:
                pairs.append((open_tok.start(), open_tok.end(), t.start(), t.end()))
                open_tok = None
    if open_tok is not None:
        errors.append((open_tok.start(), "这个 <d> 一直到文件末尾都没有闭合。改法:在台词末尾补 </d>。"))
    return pairs, errors


def detect_mode(text: str, forced: str) -> Optional[str]:
    if forced in ("ref", "base", "multishot"):
        return forced
    if "subject_definitions:" in text or re.search(r"subject_definitions\s*:", text):
        return "ref"
    if "integrated_multimodal_description:" in text or re.search(r"integrated_multimodal_description\s*:", text):
        return "base"
    # 多窗脚本没有段名，只有 `---` 分隔的裸窗口。自动判定只在确实分段时成立，
    # 避免把普通单段正文误判成多窗。
    if len(split_multishot_windows(text)) > 1:
        return "multishot"
    return None


def split_multishot_windows(text: str) -> List[str]:
    """多窗脚本 = 若干段裸正文，窗口之间单独一行 `---`。

    这不是单镜正文的「三段/六段」结构，所以不能按段名判定模式。
    """
    return [w.strip() for w in re.split(r"(?m)^---\s*$", text or "") if w.strip()]


def word_diff(a: str, b: str, limit: int = 12) -> List[str]:
    aw, bw = a.split(), b.split()
    out: List[str] = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, aw, bw).get_opcodes():
        if tag == "equal":
            continue
        if i1 < i2:
            out.append("-" + " ".join(aw[i1:i2]))
        if j1 < j2:
            out.append("+" + " ".join(bw[j1:j2]))
    return out[:limit]


def trigger_keywords(trigger: str) -> List[str]:
    return [w for w in re.findall(r"[a-z]+", trigger.lower()) if len(w) >= 3 and w not in TRIGGER_STOP]


# ---------------------------------------------------------------------------
# 文档对象
# ---------------------------------------------------------------------------

class Doc:
    def __init__(self, path: str, text: str, args: argparse.Namespace, config: Optional[dict]):
        self.path = path
        self.text = text
        self.args = args
        self.config = config
        self.rate: float = args.rate
        self.refs: Optional[int] = args.refs
        self.findings: List[Finding] = []
        self.frames, self.duration, self.dur_source, self.frames_fractional = self._resolve_duration()
        self.sections = parse_sections(text)
        self.sec: Dict[str, Section] = {}
        for s in self.sections:
            self.sec.setdefault(s.name, s)
        self.d_pairs, self.d_errors = pair_d_tags(text)
        self.masked = mask_spans(text, [(a, d) for a, _b, _c, d in self.d_pairs])
        self.mode = detect_mode(text, args.mode)
        self._dialogues: Optional[List[Dialogue]] = None

    # -- 基础 ---------------------------------------------------------------
    def _resolve_duration(self):
        a = self.args
        if a.frames is not None:
            return a.frames, a.frames / FPS, "--frames", False
        if a.seconds is not None:
            f = a.seconds * FPS
            if abs(f - round(f)) < 1e-6:
                return int(round(f)), a.seconds, "--seconds", False
            return None, a.seconds, "--seconds", True
        ms = re.findall(r"_(\d+)f", os.path.basename(self.path))
        if ms:
            fr = int(ms[-1])
            return fr, fr / FPS, "文件名", False
        return None, None, None, False

    @property
    def main(self) -> Optional[Section]:
        if self.mode == "ref":
            return self.sec.get("detailed_description")
        if self.mode == "base":
            return self.sec.get("integrated_multimodal_description")
        return None

    @property
    def main_name(self) -> str:
        return "detailed_description" if self.mode == "ref" else "integrated_multimodal_description"

    @property
    def multishot_windows(self) -> List[str]:
        if self.mode != "multishot":
            return []
        return split_multishot_windows(self.text)

    def line_of(self, pos: Optional[int]) -> Optional[int]:
        if pos is None:
            return None
        return self.text.count("\n", 0, pos) + 1

    def add(self, level: str, rule: str, pos: Optional[int], msg: str) -> None:
        self.findings.append(Finding(level, rule, self.path, self.line_of(pos), msg))

    def mtext(self, s: Section) -> str:
        return self.masked[s.cstart:s.cend]

    # -- 条目切分 -----------------------------------------------------------
    def split_entries(self, sec: Section, start_pat: str) -> List[Tuple[int, str]]:
        """按行切分;同一行内若以 '. <Label N> ...' 串写多个条目,也拆开。"""
        splitter = re.compile(r"(?<=[.;])[ \t]+(?=%s)" % start_pat)
        out: List[Tuple[int, str]] = []
        pos = sec.cstart
        for line in sec.text.split("\n"):
            cuts = [0] + [m.end() for m in splitter.finditer(line)]
            for i, c in enumerate(cuts):
                e = cuts[i + 1] if i + 1 < len(cuts) else len(line)
                piece = line[c:e]
                stripped = piece.strip()
                if stripped:
                    out.append((pos + c + (len(piece) - len(piece.lstrip())), stripped))
            pos += len(line) + 1
        return out

    def def_entries(self) -> List[Tuple[int, str]]:
        sd = self.sec.get("subject_definitions")
        if not sd:
            return []
        return self.split_entries(sd, LABEL_START + r"\s+is\b")

    def standalone_labels(self) -> Dict[Tuple[str, int], Tuple[int, str]]:
        out: Dict[Tuple[str, int], Tuple[int, str]] = {}
        for pos, entry in self.def_entries():
            m = DEF_START_RE.match(entry)
            if m:
                out.setdefault((m.group(1), int(m.group(2))), (pos, entry))
        return out

    def retention_entries(self) -> List[Tuple[int, str]]:
        ra = self.sec.get("retention_analysis")
        if not ra:
            return []
        return self.split_entries(ra, LABEL_START + r"\s*[(:]")

    def retention_labels(self) -> Dict[Tuple[str, int], int]:
        out: Dict[Tuple[str, int], int] = {}
        for pos, entry in self.retention_entries():
            m = re.match(r"^<(Subject|Picture|Video|Audio) (\d+)>", entry)
            if m:
                out.setdefault((m.group(1), int(m.group(2))), pos)
        return out

    # -- 对白 ---------------------------------------------------------------
    def dialogues(self) -> List[Dialogue]:
        if self._dialogues is not None:
            return self._dialogues
        res: List[Dialogue] = []
        main = self.main
        if main is None:
            self._dialogues = res
            return res
        shots = [m.start() for m in SHOT_RE.finditer(self.masked, main.cstart, main.cend)]
        prev: Optional[Dialogue] = None
        for a, b, c, d in self.d_pairs:
            if not (main.cstart <= a < main.cend):
                continue
            inner = self.text[b:c]
            m = D_CONTENT_RE.match(inner)
            lang = m.group(1) if m else None
            content = m.group(2) if m else inner.strip()
            shot_start = max([s for s in shots if s <= a], default=main.cstart)
            seg_start = max(shot_start, prev.close_end if prev else main.cstart)
            dl = Dialogue(a, d, lang, content, len(HAN_RE.findall(content)), shot_start)
            spks = list(SPK_RE.finditer(self.masked, seg_start, a))
            if spks:
                dl.speaker = "S" + spks[-1].group(1)
                dl.speaker_pos = spks[-1].start()
            elif (prev is not None and prev.shot_start == shot_start and prev.speaker
                  and len(self.masked[seg_start:a].strip()) <= 120):
                # 同一说话人紧接着的第二句台词,沿用上一句的说话人
                dl.speaker = prev.speaker
                dl.speaker_pos = prev.speaker_pos
                dl.inherited = True
            starts = list(START_RE.finditer(self.masked, main.cstart, a))
            if starts:
                dl.start = ts(starts[-1].group(1))
            res.append(dl)
            prev = dl
        self._dialogues = res
        return res


# ---------------------------------------------------------------------------
# 规则:每条一个函数
# ---------------------------------------------------------------------------

def rule_g02(doc: Doc) -> None:
    order = REF_ORDER if doc.mode == "ref" else BASE_ORDER
    for m in INDENTED_HEADER_RE.finditer(doc.text):
        if m.group(1) in order:
            doc.add("error", "G02", m.start(),
                    "段名 %s 前面有空白,不算段名。改法:把 '%s:' 顶格写在行首。" % (m.group(1), m.group(1)))
    for m in NOCOLON_HEADER_RE.finditer(doc.text):
        if m.group(1) in order:
            doc.add("error", "G02", m.start(),
                    "段名 %s 后缺冒号。改法:写成 '%s:'。" % (m.group(1), m.group(1)))
    seen: Dict[str, int] = {}
    for s in doc.sections:
        if s.name not in order:
            continue
        if s.name in seen:
            doc.add("error", "G02", s.hpos,
                    "段 %s 重复出现。改法:合并为一段,每段只出现一次。" % s.name)
        else:
            seen[s.name] = s.hpos
    for name in order:
        if name not in seen:
            doc.add("error", "G02", None,
                    "缺少段 %s。改法:按顺序 %s 补齐,每段名顶格并以冒号结尾。" % (name, " → ".join(order)))
    present = sorted(seen, key=lambda n: seen[n])
    expected = [n for n in order if n in seen]
    if present != expected:
        doc.add("error", "G02", None,
                "段落顺序不对:实际 %s;应为 %s。" % (" → ".join(present), " → ".join(expected)))
    for name in order:
        s = doc.sec.get(name)
        if s is None:
            continue
        body = s.text.strip()
        if not body:
            hint = "无配乐/无内容时写 N/A" if name in NA_OK else "写入该段正文"
            doc.add("error", "G02", s.hpos, "段 %s 内容为空。改法:%s。" % (name, hint))
        elif body.upper() in ("N/A", "NA") and name not in NA_OK:
            doc.add("error", "G02", s.hpos,
                    "段 %s 不允许写 N/A(只有 overall_soundscape / non_diegetic_music 可以)。改法:写入实际内容。" % name)


def rule_g03(doc: Doc) -> None:
    if doc.mode == "ref":
        for m in re.finditer(r"\bintegrated_multimodal_description\b", doc.text):
            doc.add("error", "G03", m.start(),
                    "ref(六段)文件里出现了 integrated_multimodal_description。官方 Ref2VA 只有六段,"
                    "该字段只属于基础模式。改法:删除该段,把内容并入 detailed_description。")
            break
    elif doc.mode == "base":
        for name in ("detailed_description", "subject_definitions"):
            m = re.search(r"\b%s\b" % name, doc.text)
            if m:
                doc.add("error", "G03", m.start(),
                        "base(三段)文件里出现了 %s。改法:要用参考标签就整体改成 ref 六段;"
                        "否则删掉它,正文写进 integrated_multimodal_description。" % name)


def rule_g04(doc: Doc) -> None:
    dd = doc.sec.get("detailed_description")
    if dd is None:
        return
    m = re.search(r"\[Shot 1\]", dd.text)
    if not m:
        return
    pre = doc.masked[dd.cstart:dd.cstart + m.start()].strip()
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", pre) if len(EN_WORD_RE.findall(s)) >= 3]
    if not sentences:
        doc.add("error", "G04", dd.hpos,
                "detailed_description 在 [Shot 1] 之前缺少 1–2 句英文风格开场(ref-en.txt §5.2)。"
                "改法:在 [Shot 1] 前加一句,如 'The target video is a vertical 3D CG animated shot in the "
                "style of a modern animated feature: soft global illumination, warm filmic grade.'")


def rule_g05(doc: Doc) -> None:
    sd = doc.sec.get("subject_definitions")
    defined: Set[Tuple[str, int]] = set()
    if sd:
        defined = {(m.group(1), int(m.group(2))) for m in LABEL_RE.finditer(sd.text)}
    reported: Set[Tuple[str, int]] = set()
    scan: List[Tuple[str, Section]] = []
    # 第一个段名之前的文本（改词单说明、注释等）同样会被模型读到。
    if doc.sections and doc.sections[0].hpos > 0:
        pre = doc.text[:doc.sections[0].hpos]
        scan.append(("文件开头(第一个段名之前)", Section("preamble", 0, 0, len(pre), pre)))
    for name in ("summary", "retention_analysis", "detailed_description",
                 "overall_soundscape", "non_diegetic_music"):
        if doc.sec.get(name) is not None:
            scan.append((name, doc.sec[name]))
    for name, s in scan:
        for m in LABEL_RE.finditer(s.text):
            key = (m.group(1), int(m.group(2)))
            if key in defined or key in reported:
                continue
            reported.add(key)
            doc.add("error", "G05", s.cstart + m.start(),
                    "%s 里的 %s 没有在 subject_definitions 中定义。改法:在 subject_definitions 加一行 "
                    "'%s is ...',或改用已定义的标签。" % (name, m.group(0), m.group(0)))


def rule_g06(doc: Doc) -> None:
    standalone = doc.standalone_labels()
    # 官方 ref-en.txt:37/:68 允许（并要求）把只作素材来源的图写进 <Subject N> 定义里引用，
    # 不建独立行。这类图在正文用 <Subject N> 指代、在 retention 里可能单独列一条，
    # 但缺独立定义行是合规的 —— 不算 G06。
    sd = doc.sec.get("subject_definitions")
    cited_in_subject = set()
    if sd is not None:
        # 一条 Subject 定义可以吃多张图/多段视频（官方 ref-en.txt:48/:57/:312）：
        # '<Subject 2> is the Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>'
        # 每条定义按句号切段，段内所有 Picture/Video 都算已引用。
        for entry in re.split(r"(?<=[.;])\s+(?=<Subject\s+\d+>\s+is\b)", sd.text):
            if not re.match(r"<Subject\s+\d+>\s+is\b", entry.strip()):
                continue
            # 段内每个标签各自看它后面到下一个标签之间的小段，判断它是素材来源还是帧锚。
            # 官方 ref-en.txt:62 要求帧锚/构图锚建独立 Picture 行，不能顺带豁免。
            marks = list(re.finditer(r"<(Picture|Video)\s+(\d+)>", entry))
            for idx, m in enumerate(marks):
                stop = marks[idx + 1].start() if idx + 1 < len(marks) else len(entry)
                tail = entry[m.end():stop]
                if PICTURE_FRAME_ROLE_RE.search(tail):
                    continue
                cited_in_subject.add((m.group(1), int(m.group(2))))
    required: Dict[Tuple[str, int], Tuple[int, str]] = {}
    for key, pos in doc.retention_labels().items():
        required.setdefault(key, (pos, "在 retention_analysis 里有独立条目"))
    dd = doc.sec.get("detailed_description")
    if dd is not None:
        for m in ANCHOR_RE.finditer(doc.masked, dd.cstart, dd.cend):
            key = (m.group(1), int(m.group(2)))
            required.setdefault(key, (m.start(), "在 detailed_description 里被当作画面锚点引用"))
    for key in sorted(required, key=lambda k: required[k][0]):
        if key in standalone:
            continue
        if key in cited_in_subject:
            # 素材图已按官方写法并进 Subject 定义，不再要求独立行。
            continue
        pos, why = required[key]
        label = "<%s %d>" % key
        if key[0] == "Picture":
            example = "%s is the composition anchor for [Shot 1], showing ..." % label
        elif key[0] == "Video":
            example = "%s is the source video for ..." % label
        else:
            example = "%s is ..." % label
        doc.add("error", "G06", pos,
                "%s %s,但 subject_definitions 里没有以 '%s is' 开头的独立定义行(ref-en.txt §2.2/§2.3)。"
                "改法:在 subject_definitions 单独加一行,如 '%s'。" % (label, why, label, example))


def rule_g07(doc: Doc) -> None:
    ret = doc.retention_labels()
    for key, (pos, _entry) in sorted(doc.standalone_labels().items(), key=lambda kv: kv[1][0]):
        if key not in ret:
            label = "<%s %d>" % key
            doc.add("warn", "G07", pos,
                    "%s 有独立定义,但 retention_analysis 没有它的条目(官方要求每个标签一行)。"
                    "改法:在 retention_analysis 加一行 '%s (appears in [Shot 1]): fully_preserved - ...'。"
                    % (label, label))


def rule_g08(doc: Doc) -> None:
    # 官方 ref-en.txt:110 只规定「同类内独立编号」,没有连续性要求:
    # <Subject 1>/<Picture 2>/<Subject 3> 只要同类之间不撞号就合法。
    # 编号表达的是「这一类里第几个」,不是张数对等或时间顺序。
    # 正文里同一标签反复出现是正常引用(一个 Subject 被提多次),不是重复定义;
    # 真正的错只有一种:subject_definitions 里同一个编号定义了两个不同实体。
    by_type: Dict[str, Dict[int, int]] = {}
    for m in LABEL_RE_ANY.finditer(doc.text):
        typ = m.group(1) or m.group(3)
        num = m.group(2) or m.group(4)
        by_type.setdefault(typ, {}).setdefault(int(num), m.start())
    # 判「重复定义」按行算，不按句算：同一行里再写一次 '<Subject 1> is wearing …'
    # 是对同一实体的补充说明（官方 ref-en.txt:110 允许同一标签跨句保持同一含义），
    # 只有另起一行重新定义同一编号，才是两个实体撞号。
    seen_def: Dict[Tuple[str, int], int] = {}
    sd = doc.sec.get("subject_definitions")
    if sd is not None:
        offset = 0
        for line in sd.text.split("\n"):
            m = DEF_START_RE.match(line.strip())
            if m:
                key = (m.group(1), int(m.group(2)))
                if key in seen_def:
                    doc.add("error", "G08", sd.cstart + offset,
                            "<%s %d> 在 subject_definitions 里被独立定义了两次:同一个标签只能对应一个实体。"
                            "改法:同一实体只定义一次,后续段落直接引用该标签;不同实体改用不同编号。"
                            % key)
                else:
                    seen_def[key] = sd.cstart + offset
            offset += len(line) + 1
    if doc.refs is not None:
        pics = by_type.get("Picture", {})
        kmax = max(pics) if pics else 0
        if kmax > doc.refs:
            doc.add("error", "G08", pics[kmax],
                    "出现 <Picture %d>,但 --refs 说只上传了 %d 张参考图。改法:补传图片,或把编号改到 1..%d 之内。"
                    % (kmax, doc.refs, doc.refs))
        if doc.refs > len(pics):
            doc.add("warn", "G08b", None,
                    "上传了 %d 张参考图,但提示词只标注了 %d 张 <Picture N>:上传了未标注的参考图,模型不知道它们的角色。"
                    "改法:按上传顺序给每张图写 <Picture N>,并在 subject_definitions 说明它的用途"
                    "(身份图写进 <Subject N> 的定义里,如 '<Subject 1> is the boy in <Picture 2>, ...')。"
                    % (doc.refs, len(pics)))
        # G08c: subject_definitions 里引用的 Picture 编号必须真的上传过。
        # 编号不要求连续(官方 ref-en.txt:110 只有类内独立编号),所以这里不查连续性,
        # 只查「引用了一个超出 --refs 张数的编号」——那种引用模型无从解析。
        sd_section = doc.sec.get("subject_definitions")
        sd_text = sd_section.text if sd_section is not None else ""
        if sd_text:
            for m in re.finditer(r"<Picture\s+(\d+)>", sd_text):
                num = int(m.group(1))
                if num > doc.refs:
                    doc.add("warn", "G08c", m.start(),
                            "subject_definitions 引用了 <Picture %d>,但 --refs 只有 %d 张。"
                            "改法:改成实际存在的编号,或补传这张参考图。"
                            % (num, doc.refs))


def rule_g09(doc: Doc) -> None:
    ra = doc.sec.get("retention_analysis")
    if ra is None:
        return
    for pos, entry in doc.retention_entries():
        if not re.match(LABEL_START, entry):
            doc.add("error", "G09", pos,
                    "retention_analysis 这一行不是以标签开头的条目:'%s'。改法:每行写成 "
                    "'<Subject N> (appears in [Shot 1]): fully_preserved - ...'。" % entry[:60])
            continue
        m = ENTRY_RE.match(entry)
        if not m:
            doc.add("error", "G09", pos,
                    "retention_analysis 条目格式不对:'%s'。改法:'<Label N> (appears in [Shot a], [Shot b]): "
                    "marker - 说明'(Audio 可写 '<Audio N>: marker - ...')。" % entry[:60])
            continue
        typ, num = m.group(1), int(m.group(2))
        paren = (m.group("paren") or "").strip()
        marker = m.group("marker")
        label = "<%s %d>" % (typ, num)
        if typ == "Subject" and not APPEARS_RE.match(paren):
            doc.add("error", "G09", pos,
                    "%s 的括号应为 '(appears in [Shot 1], [Shot 2])',实际为 '(%s)'。改法:按该格式写出现镜次。"
                    % (label, paren))
        elif typ == "Picture" and not (APPEARS_RE.match(paren) or re.search(r"\[Shot \d+\]", paren)):
            doc.add("error", "G09", pos,
                    "%s 的括号应写出它锚定的镜头与用途,如 '([Shot 1] composition anchor)',实际为 '(%s)'。"
                    % (label, paren))
        elif typ == "Video" and not paren:
            doc.add("error", "G09", pos,
                    "%s 缺少括号说明,如 '(cut and pacing structure)' 或 '(appears in [Shot 1])'。" % label)
        allowed = AUDIO_MARKERS if typ == "Audio" else VISUAL_MARKERS
        if marker not in allowed:
            doc.add("error", "G09", pos,
                    "%s 的 marker '%s' 不在枚举内。改法:改为 %s 之一。" % (label, marker, " | ".join(sorted(allowed))))
        if not (m.group("desc") or "").strip():
            doc.add("error", "G09", pos, "%s 的 '-' 后缺少说明。改法:写清保留了什么、改变了什么。" % label)


def section_shots(doc: Doc, start: int, end: int):
    """正文里的镜头段标记；排除 `(from [Shot N])` 这类引用。

    官方 base 规范两种写法都有：`<Picture 1> (from [Shot 1]) is fully
    referenced`（带方括号）与 `Picture 1 (from Shot 1) aligns with ...`
    （不带）。带方括号的那句是引用同一镜，不是开第二镜——按段判定时不能算，
    否则照官方写反而报 G10。
    """
    out = []
    for m in SHOT_RE.finditer(doc.masked, start, end):
        pre = doc.masked[max(start, m.start() - 8):m.start()]
        if re.search(r"\(from\s*$", pre):
            continue
        out.append(m)
    return out


def rule_g10(doc: Doc) -> None:
    main = doc.main
    if main is None:
        return
    shots = section_shots(doc, main.cstart, main.cend)
    if not shots:
        doc.add("error", "G10", main.hpos,
                "%s 里没有 [Shot 1]。改法:单镜也要以 '[Shot 1]' 开始镜头描述。" % doc.main_name)
        return
    nums = [int(m.group(1)) for m in shots]
    if nums != list(range(1, len(nums) + 1)):
        doc.add("error", "G10", shots[0].start(),
                "镜头编号应为 [Shot 1], [Shot 2], ... 依次递增,实际为 %s。" % nums)
    prev_t = 0.0
    for m in shots:
        after = doc.masked[m.end():m.end() + 40]
        tm = re.match(r"\s*,?\s*At (\d{2}:\d{2}\.\d{3})", after)
        n = int(m.group(1))
        if n == 1:
            if tm:
                doc.add("error", "G10", m.start(),
                        "[Shot 1] 不能带时间戳。改法:删掉紧跟其后的 'At %s,',直接写画面。" % tm.group(1))
            continue
        if not tm:
            doc.add("error", "G10", m.start(),
                    "[Shot %d] 后缺少切镜时间。改法:写成 '[Shot %d] At MM:SS.mmm, ...'。" % (n, n))
            continue
        t = ts(tm.group(1))
        if t <= prev_t:
            doc.add("error", "G10", m.start(),
                    "[Shot %d] 的切镜时间 %s 没有严格晚于上一镜(%s)。改法:切镜时间必须递增。"
                    % (n, tm.group(1), fmt_ts(prev_t)))
        if doc.duration is not None and t >= doc.duration:
            doc.add("error", "G10", m.start(),
                    "[Shot %d] 的切镜时间 %s 不小于总时长 %s。改法:提前切点或拆成下一次生成。"
                    % (n, tm.group(1), fmt_ts(doc.duration)))
        prev_t = t


def rule_g11(doc: Doc) -> None:
    main = doc.main
    if main is None:
        return
    shots = [m.start() for m in section_shots(doc, main.cstart, main.cend)]
    bounds = sorted(set([main.cstart] + shots + [main.cend]))
    for i in range(len(bounds) - 1):
        prev = None
        for m in TS_RE.finditer(doc.masked, bounds[i], bounds[i + 1]):
            t = ts(m.group(0))
            if doc.duration is not None and t > doc.duration + TIME_TOL:
                doc.add("error", "G11", m.start(),
                        "时间戳 %s 超过总时长 %s(%s)。改法:把动作/台词收在 %s 之前。"
                        % (m.group(0), fmt_ts(doc.duration), doc.dur_source, fmt_ts(doc.duration)))
            if prev is not None and t < prev - 1e-9:
                doc.add("warn", "G11", m.start(),
                        "同一镜内时间戳倒退:%s 出现在 %s 之后。改法:按播放顺序写时间段,避免区间互相覆盖。"
                        % (m.group(0), fmt_ts(prev)))
            prev = t
    for m in RANGE_RE.finditer(doc.masked, main.cstart, main.cend):
        a, b = ts(m.group(1)), ts(m.group(2))
        if a > b + 1e-9:
            doc.add("error", "G11", m.start(),
                    "时间区间起点 %s 晚于终点 %s。改法:交换或改正这两个时间。" % (m.group(1), m.group(2)))
    # 声景/配乐/retention 的时间码同样受总时长约束：声景里写 at 00:47.000 落在一个
    # 5.9 秒的镜头里，是硬错（官方 base-en.txt:154 要求声景用 1-4 句英文描述整段，
    # 不是逐事件时间轴）。
    # 但 subject_definitions 与 summary 例外：官方 ref-en.txt:80-85/:136-137 的
    # video-editing / continuation 任务本来就要说明「用了源素材的哪一段」，
    # 那里的时间码属于源片，不受目标片时长约束。
    if doc.duration is not None:
        for name in ("overall_soundscape", "non_diegetic_music", "retention_analysis"):
            sec = doc.sec.get(name)
            if sec is None:
                continue
            for m in TS_RE.finditer(doc.masked, sec.cstart, sec.cend):
                t = ts(m.group(0))
                if t > doc.duration + TIME_TOL:
                    doc.add("error", "G11", m.start(),
                            "%s 里的时间戳 %s 超过目标片总时长 %s(%s)。"
                            "改法:声景/配乐段只描述整段持续声音,不写逐事件时间码;"
                            "retention 段只声明保留程度,不复述源素材时段。"
                            % (name, m.group(0), fmt_ts(doc.duration), doc.dur_source))


def rule_g12(doc: Doc) -> None:
    if doc.duration is None:
        doc.add("warn", "G12", None,
                "无法得知时长(未给 --frames/--seconds,文件名也没有 _NNNf),已跳过时长上限相关检查。"
                "改法:加 --frames 141 或把文件命名为 xxx_141f.txt。")
        return
    if doc.frames_fractional:
        doc.add("warn", "G12", None,
                "--seconds %.3f × 24 不是整数帧。改法:改用 --frames,或按整帧时长规划。" % doc.duration)
        return
    f = doc.frames
    if f is not None and (f - 5) % 17 != 0:
        k = max(0, (f - 5) // 17)
        lo, hi = 17 * k + 5, 17 * (k + 1) + 5
        doc.add("warn", "G12", None,
                "帧数 %d 不满足 17k+5(H3-Studio 实测会自动对齐)。改法:按目标帧数规划,最近可用值为 %d(%.3fs)或 %d(%.3fs)。"
                % (f, lo, lo / FPS, hi, hi / FPS))


def rule_g13(doc: Doc) -> None:
    for pos, msg in doc.d_errors:
        doc.add("error", "G13", pos, msg)
    for a, b, c, _d in doc.d_pairs:
        inner = doc.text[b:c]
        if not D_CONTENT_RE.match(inner):
            doc.add("error", "G13", a,
                    "对白格式不对:'<d>%s</d>'。改法:写成 '<d>[Chinese] 逐字台词</d>',语言标签放方括号内,后面紧跟台词。"
                    % inner.strip()[:30])


def rule_g14(doc: Doc) -> None:
    main = doc.main
    if main is None:
        return
    for dl in doc.dialogues():
        if dl.speaker is None:
            # 官方 ref-en §5.4:直接复用的 BGM/完整音轨里的歌词线索,以 <Audio N> 为发声源,不另编 (Sx)。
            ctx = doc.masked[max(main.cstart, dl.open_pos - 160):dl.open_pos]
            ctx = ctx[max(ctx.rfind(ch) for ch in ".!?;") + 1:] if any(ch in ctx for ch in ".!?;") else ctx
            if re.search(r"<Audio \d+>", ctx):
                continue
            doc.add("error", "G14", dl.open_pos,
                    "这句 <d> 前找不到说话人 ID (Sx)。改法:ref 模式写 '<Subject N> (S1) says, <d>...';"
                    "非已定义主体写 'A warm adult female voice, off-screen (S2), says: <d>...'。")
    firsts: List[Tuple[int, int]] = []
    seen: Set[int] = set()
    for m in SPK_RE.finditer(doc.masked, main.cstart, main.cend):
        n = int(m.group(1))
        if n not in seen:
            seen.add(n)
            firsts.append((n, m.start()))
    for i, (n, pos) in enumerate(firsts):
        if n != i + 1:
            doc.add("error", "G14", pos,
                    "说话人编号应按目标视频里首次发声的先后为 S1, S2, ...;这里第 %d 个首次出现的说话人是 (S%d)。"
                    "改法:按发声先后重新编号(ref-en.txt §5.4)。" % (i + 1, n))
            break
    ra = doc.sec.get("retention_analysis")
    if ra is not None:
        for m in SPK_RE.finditer(ra.text):
            doc.add("error", "G14", ra.cstart + m.start(),
                    "retention_analysis 里不得出现说话人 ID %s。改法:删掉 (Sx),只保留标签。" % m.group(0))
    if doc.mode == "ref":
        _g14_subject_speaker(doc, main)


def _g14_subject_speaker(doc: Doc, main: Section) -> None:
    """说话人是已定义主体却没写 <Subject N> (Sx) —— 启发式,只 warn。"""
    subj_defs = [e.lower() for _p, e in doc.def_entries() if e.startswith("<Subject")]
    if not subj_defs:
        return
    warned: Set[str] = set()
    for m in SPK_RE.finditer(doc.masked, main.cstart, main.cend):
        sx = m.group(0)
        if sx in warned:
            continue
        back = doc.masked[max(main.cstart, m.start() - 80):m.start()]
        cut = max([back.rfind(ch) for ch in ".!?:;]"] + [-1])
        phrase = back[cut + 1:]
        phrase = re.sub(r"\bAt \d{2}:\d{2}\.\d{3},?", " ", phrase)
        if re.search(r"<Subject \d+>\s*,?\s*$", phrase) or "<Subject" in phrase:
            continue
        phrase = OFFSCREEN_RE.sub(" ", phrase)
        phrase = re.sub(r"on[- ]screen", " ", phrase, flags=re.I)
        words = [w.lower() for w in re.findall(r"[A-Za-z]+", phrase)]
        if not words:
            continue
        head = words[-1]
        if len(head) < 3 or head in SPEAKER_GENERIC:
            continue
        if any(re.search(r"\b%s\b" % re.escape(head), d) for d in subj_defs):
            warned.add(sx)
            doc.add("warn", "G14", m.start(),
                    "说话人 '%s %s' 看起来是已定义的主体,但没写成 '<Subject N> %s'。改法:写成 '<Subject N> %s, the %s, ...'"
                    "(ref-en.txt §5.4)。" % (head, sx, sx, sx, head))


def _configured_visible_text(doc: Doc) -> Set[str]:
    """系列配置可精确放行画内文字；未知/畸形配置不放行，保持 fail closed。"""
    cfg = doc.config or {}
    out: Set[str] = set()
    for key in ("visible_text", "allowed_visible_text"):
        raw = cfg.get(key, [])
        if isinstance(raw, dict):
            raw = raw.get("allow", [])
        if isinstance(raw, list):
            out.update(x for x in raw if isinstance(x, str) and x)
    return out


def rule_g15(doc: Doc) -> None:
    configured = _configured_visible_text(doc)
    for s in doc.sections:
        body = doc.mtext(s)
        allowed: List[Tuple[int, int]] = []
        for q in QUOTE_RE.finditer(body):
            prefix = body[max(0, q.start() - 120):q.start()]
            if (q.group(1) in configured or VISIBLE_RE.search(prefix)
                    or VISIBLE_OBLIGATION_RE.search(prefix)
                    or VISIBLE_SUFFIX_RE.match(body[q.end():q.end() + 60])):
                allowed.append((q.start(), q.end()))
        hits = [m for m in CJK_RE.finditer(body)
                if not any(a <= m.start() < b for a, b in allowed)]
        for m in hits[:5]:
            doc.add("error", "G15", s.cstart + m.start(),
                    "%s 里在 <d> 之外出现中文/全角字符 '%s'。改法:台词放进 '<d>[Chinese] ...</d>';描述改写成英文"
                    "(如发音说明写 'the word wai-mai');画内文字须用明确载体/义务(如 'the sign reads \"...\"'),"
                    "或在系列配置 visible_text 中精确允许。" % (s.name, m.group(0)[:20]))
        if len(hits) > 5:
            doc.add("error", "G15", s.cstart + hits[5].start(),
                    "%s 里另有 %d 处 <d> 外的中文/全角字符未逐条列出。" % (s.name, len(hits) - 5))


def rule_g16(doc: Doc) -> None:
    dls = doc.dialogues()
    seen: Dict[str, int] = {}
    for dl in dls:
        key = re.sub(r"\s+", "", dl.content)
        if not key:
            continue
        if key in seen:
            doc.add("error", "G16", dl.open_pos,
                    "同一句台词 '<d>%s</d>' 在 %s 里出现了不止一次(首次在第 %d 行)。改法:只在实际发声处写一次。"
                    % (dl.content[:30], doc.main_name, doc.line_of(seen[key]) or 0))
        else:
            seen[key] = dl.open_pos
    for name in ("overall_soundscape", "non_diegetic_music", "summary", "retention_analysis"):
        s = doc.sec.get(name)
        if s is None:
            continue
        for m in D_TAG_RE.finditer(s.text):
            doc.add("error", "G16", s.cstart + m.start(),
                    "%s 里出现了 <d> 对白标签。改法:对白只写在 %s 对应镜头里,这里只写%s。"
                    % (name, doc.main_name, "环境声/配乐" if name.endswith(("soundscape", "music")) else "对本片的说明"))
            break
        if name not in ("overall_soundscape", "non_diegetic_music"):
            continue
        for dl in dls:
            han = "".join(HAN_RE.findall(dl.content))
            if len(han) >= 2 and han in "".join(HAN_RE.findall(s.text)):
                doc.add("error", "G16", s.cstart,
                        "%s 里重复了台词原文 '%s'。改法:删掉,台词只保留在 %s 的 <d> 里。" % (name, dl.content[:20], doc.main_name))


def rule_g17(doc: Doc) -> None:
    main = doc.main
    if main is None:
        return
    for dl in doc.dialogues():
        win = doc.masked[max(main.cstart, dl.open_pos - LIPS_WINDOW):min(main.cend, dl.close_end + LIPS_WINDOW)]
        if OFFSCREEN_RE.search(win) and not (LIPS_RE.search(win) and CLOSED_RE.search(win)):
            doc.add("warn", "G17", dl.open_pos,
                    "台词附近有 off-screen 说话人,但没写画内人物闭嘴。模型会把口型放到画面最显眼的正脸上"
                    "(方言实测 3 次中 2 次)。改法:在台词后补一句 '<Subject N> does not speak; his lips remain completely closed.'")


def rule_g18(doc: Doc) -> None:
    prev: Optional[Tuple[Dialogue, float]] = None
    for dl in doc.dialogues():
        if dl.han == 0:
            continue
        if dl.start is None:
            doc.add("warn", "G18", dl.open_pos,
                    "这句台词前找不到 'At/Between/From MM:SS.mmm' 起点,跳过台词时长估算。改法:在台词所在动作句前写明开口时间。")
            continue
        end = dl.start + dl.han / doc.rate
        if doc.duration is not None and end > doc.duration + TIME_TOL:
            over = end - doc.duration
            level = "error" if over > DIALOGUE_OVERRUN_ERR_S else "warn"
            doc.add(level, "G18", dl.open_pos,
                    "台词 %d 字,从 %s 起按 %.1f 字/秒约到 %s,超出总时长 %s 约 %.2fs,可能被截断。"
                    "改法:提前开口、删减台词,或加长镜头(按 17k+5 帧);成人语速偏快时可用 --rate 调高再复核。"
                    % (dl.han, fmt_ts(dl.start), doc.rate, fmt_ts(end), fmt_ts(doc.duration), over))
        if prev is not None:
            pdl, pend = prev
            overlap = pend - dl.start
            if pdl.speaker and dl.speaker and pdl.speaker != dl.speaker and overlap > OVERLAP_WARN_S:
                doc.add("warn", "G18", dl.open_pos,
                        "两句台词叠在一起,口型会串:%s 的台词约到 %s 才说完,%s 却在 %s 开口(重叠 %.2fs)。"
                        "改法:把后一句推迟到 %s 之后,或缩短前一句。"
                        % (pdl.speaker, fmt_ts(pend), dl.speaker, fmt_ts(dl.start), overlap, fmt_ts(pend)))
        prev = (dl, end)


def rule_g19(doc: Doc) -> None:
    s = doc.sec.get("overall_soundscape")
    if s is not None:
        m = SOUND_SPEECH_RE.search(s.text)
        if m:
            doc.add("warn", "G19", s.cstart + m.start(),
                    "overall_soundscape 里写了说话(%s)。改法:说话事件写进 %s 对应镜头,这里只汇总环境声与物理音效。"
                    % (m.group(0), doc.main_name))
        elif QUOTE_RE.search(s.text):
            doc.add("warn", "G19", s.cstart,
                    "overall_soundscape 里出现引号内容,疑似台词。改法:台词只写在 <d> 里。")
    mu = doc.sec.get("non_diegetic_music")
    if mu is not None and not mu.text.strip():
        doc.add("warn", "G19", mu.hpos,
                "non_diegetic_music 为空串。改法:无配乐写 'N/A'(方言实测:留空会被模型补乐)。")


def rule_g20(doc: Doc) -> None:
    main = doc.main
    if main is None:
        return
    n = len(EN_WORD_RE.findall(doc.mtext(main)))
    if n < WORDS_MIN or n > WORDS_MAX:
        doc.add("warn", "G20", main.hpos,
                "%s 英文词数 %d,不在本闸门阈值 [%d, %d]。判据是这个阈值;官方常态 350–500 只是写作参考,"
                "对白密集的稿子低于 350 但在阈值内不报。改法:%s。" % (doc.main_name, n, WORDS_MIN, WORDS_MAX,
                             "补充构图、光线、动作与声音细节" if n < WORDS_MIN else "删去重复描述"))


def rule_g21(doc: Doc) -> None:
    # 触发条件必须同时认裸标签：官方 FL2VA 对齐句与正文里的帧号常写成 `Picture 1`
    # （不带尖括号，base-en.txt:25/:201 原文即如此，项目 S01–S08 也全用裸写法）。
    # 原先只认 `<Picture N>`，导致「裸标签 + 缺对齐首行」整份漏检：
    # 2026-10-22 实测同一内容裸标签版 exit=0、换成尖括号版才报 G21。
    if not LABEL_RE_ANY.search(doc.text):
        return
    first_head = doc.sections[0].hpos if doc.sections else len(doc.text)
    region = doc.text[:first_head]
    main = doc.main
    if main is not None:
        m = re.search(r"\[Shot 1\]", main.text)
        region += "\n" + main.text[:m.start() if m else len(main.text)]
    if not ALIGN_RE.search(region):
        doc.add("error", "G21", main.hpos if main else None,
                "base 模式(I2VA/FL2VA)用了 Picture 参考图,但缺少对齐首行(base-en.txt §3)。改法:在 "
                "integrated_multimodal_description 开头写 'For the target video, at 0.00 seconds into the target "
                "video, <Picture 1> (from [Shot 1]) is fully referenced.'(首尾帧再补尾帧那一句)，"
                "或官方 FL2VA 范例的 'Picture 1 (from Shot 1) aligns with the 0.00-second mark ...' 写法。")


def _g22_words(doc: Doc) -> List[str]:
    """只有系列配置明确给出禁用时间词时才启用；无配置不代表白天。"""
    tod = (doc.config or {}).get("time_of_day") or {}
    words = tod.get("forbid_any")
    return list(words) if isinstance(words, list) and words else []


def rule_g22(doc: Doc) -> None:
    for w in _g22_words(doc):
        for m in word_pattern(w).finditer(doc.masked):
            if is_negated(doc.masked, m.start()):
                continue
            doc.add("warn", "G22", m.start(),
                    "出现未被否定的 '%s',与系列时间设定可能冲突。改法:删掉或按设定写成 'never %s'/'no %s'。"
                    % (m.group(0), w, w))
            break


SUMMARY_TYPES = ("keyframe completion", "reference generation", "video editing",
                 "video continuation", "audio reuse", "audio reference")


def rule_g23(doc: Doc) -> None:
    """官方 ref-en §3:summary 开头必须带 [任务类型],多类型用 ' + ' 连接且不重复。"""
    sm = doc.sec.get("summary")
    if sm is None:
        return
    head = doc.mtext(sm).lstrip()
    m = re.match(r"\[([^\]]+)\]", head)
    if not m:
        doc.add("warn", "G23", sm.cstart,
                "summary 开头缺任务类型前缀。改法:写成 '[reference generation] The target video ...'"
                "(可选 %s,多类型用 ' + ' 连接)。" % " / ".join(SUMMARY_TYPES))
        return
    parts = [x.strip() for x in m.group(1).split("+")]
    bad = [x for x in parts if x not in SUMMARY_TYPES]
    if bad:
        doc.add("error", "G23", sm.cstart,
                "summary 任务类型 %s 不是官方枚举。改法:只用 %s。" % (bad, " / ".join(SUMMARY_TYPES)))
    if len(set(parts)) != len(parts):
        doc.add("error", "G23", sm.cstart, "summary 任务类型重复。改法:同一类型只写一次,用 ' + ' 连接不同类型。")


def rule_g24(doc: Doc) -> None:
    """官方 base-en §4.x:跨切台词用 <scenetrans>,片尾被截断用 <cutoff>;不认识的尖括号标签要报。"""
    known = {"d", "scenetrans", "cutoff", "Subject", "Picture", "Video", "Audio"}
    for m in re.finditer(r"</?([A-Za-z][A-Za-z_]*)(?:\s+\d+)?>", doc.text):
        name = m.group(1)
        if name in known:
            continue
        near = [k for k in ("scenetrans", "cutoff", "d") if name.lower().startswith(k[:4])]
        doc.add("warn", "G24", m.start(),
                "出现未知标签 <%s>。官方只有 <d> / <scenetrans> / <cutoff> 和 Subject/Picture/Video/Audio 标签。%s"
                % (name, ("疑似拼写错误,是否想写 <%s>?" % near[0]) if near else ""))
    n_st = len(re.findall(r"<scenetrans>", doc.text))
    if n_st % 2:
        doc.add("warn", "G24", None,
                "<scenetrans> 出现 %d 次,官方要求跨切台词在前后两段连接点各写一次(成对)。" % n_st)


def rule_g25(doc: Doc) -> None:
    """本地容量 4-15s(362f);节点硬顶 3600f;--allow-long-video 只豁免长端。"""
    if doc.duration is None:
        return
    # --seconds is a requested duration even if it resolves to an integer frame
    # count. Only --frames / filename carry an explicit physical grid count;
    # do not enlarge TIME_TOL or grant a blanket 362/24-second request limit.
    # 1) 节点硬顶:任何通道都不能超,不受豁免 flag 影响。
    if doc.frames is not None and doc.frames > NODE_MAX_FRAMES:
        doc.add("error", "G25", None,
                "总帧数 %d 超过 MiniMaxH3ReferenceToVideo 节点 length 上限 %d 帧(约 %.0fs)。改法:拆分镜头。"
                % (doc.frames, NODE_MAX_FRAMES, NODE_MAX_SECONDS))
        return
    local_max_grid = (doc.dur_source in ("--frames", "文件名")
                      and doc.frames == LOCAL_MAX_FRAMES)
    # 2) 超出本地容量安全档(15s/362f):默认 error;直投通道显式豁免则降 warn。
    if doc.duration > LOCAL_SAFE_SECONDS + TIME_TOL and not local_max_grid:
        # 豁免只认显式帧数来源(--frames/文件名);--seconds 是 h3q 常规路径的请求时长,不共享豁免。
        if (getattr(doc.args, "allow_long_video", False)
                and doc.dur_source in ("--frames", "文件名")):
            doc.add("warn", "G25", None,
                    "总时长 %.3fs 超出本地 16G 容量/训练范围 4-15s(--allow-long-video 豁免)。"
                    "这是手搓长视频直投通道,需人工确认分辨率与显存余量(512x896/447f 峰值余量约 0.37GiB)。"
                    % doc.duration)
        else:
            doc.add("error", "G25", None,
                    "总时长 %.3fs 超出本地 16G 容量/官方训练范围 4-15s。改法:拆成两次生成,或请求时长 ≤ 15s;"
                    "h3q 常规路径用 --allow-long-video 无效。本地帧数输入的最大合法 17k+5 网格为 %d 帧。"
                    "手搓直投通道可显式加 --allow-long-video 豁免为 warn(需自担显存风险)。"
                    % (doc.duration, LOCAL_MAX_FRAMES))
    elif doc.duration < 4 - TIME_TOL:
        doc.add("warn", "G25", None,
                "总时长 %.3fs 低于建议下限 4s。改法:延长到 ≥ 4s 或确认这是刻意的短镜。"
                % doc.duration)


MULTISHOT_SECTION_NAMES = (
    "subject_definitions", "summary", "retention_analysis",
    "detailed_description", "overall_soundscape", "non_diegetic_music",
    "integrated_multimodal_description",
)


def rule_g39(doc: Doc) -> None:
    """多窗脚本自身的格式：窗口数、窗口开头、单镜段名混入。

    2026-11-19 EP004 v5 006/007 实证：窗口正文以 `[Shot 1]` 开头，
    H3MultishotMemorySampler 用 `text.startswith("[")` 判定成 JSON 数组，
    解析失败 → 9.6 秒后 node 30 execution_error，白占一次 GPU 窗口。
    这条规则让同样的错误在上传前就失败，而不是等 ComfyUI 跑到一半。
    """
    windows = doc.multishot_windows
    if not windows:
        doc.add("error", "G39", None,
                "多窗脚本没有任何窗口。改法:每个窗口写一段正文，窗口之间单独一行 `---`。")
        return
    want = getattr(doc.args, "shot_count", None)
    if want is not None and len(windows) != want:
        doc.add("error", "G39", None,
                "多窗脚本有 %d 个窗口，但 shot_count=%d。改法:补齐/删掉窗口，"
                "或把 shot_count 改成 %d。" % (len(windows), want, len(windows)))
    for i, w in enumerate(windows, 1):
        if w[0] in "[{":
            doc.add("error", "G39", None,
                    "第 %d 个窗口以 %r 开头，H3 会整份脚本当 JSON 解析并失败。"
                    "改法:窗口正文直接从场景/人物写起，不要带 [Shot 1] 这类标记。"
                    % (i, w[0]))
        head = w.split("\n", 1)[0]
        for name in MULTISHOT_SECTION_NAMES:
            if re.match(r"(?i)^%s\s*:" % name, head):
                doc.add("error", "G39", None,
                        "第 %d 个窗口写了单镜段名 '%s:'。多窗每个窗口只写正文，"
                        "段名只属于单镜 ref/base 正文。" % (i, name))
                break


def rule_g40(doc: Doc) -> None:
    """多窗内容规则：逐窗查 `<d>` 格式、`<d>` 外中文、以及每窗自己的时长上限。

    单镜规则依赖段名（doc.sections / doc.main），多窗没有段名，所以同样的事实
    必须按窗口重新查一遍——否则「整块豁免」等于什么都没查。
    """
    windows = doc.multishot_windows
    if not windows:
        return
    # 每窗帧数：--frames 在多窗里是「每窗帧数」，整片时长是窗口之和。
    per = doc.frames
    if per is not None:
        if (per - 5) % 17 != 0:
            doc.add("warn", "G40", None,
                    "每窗帧数 %d 不满足 17k+5，H3 会自动吸附。" % per)
        if per / FPS > LOCAL_SAFE_SECONDS + TIME_TOL:
            doc.add("error", "G40", None,
                    "每窗 %.2fs 超过单镜 15s 上限。改法:减少每窗帧数或增加窗数。"
                    % (per / FPS))
        elif per / FPS < 4 - TIME_TOL:
            doc.add("warn", "G40", None,
                    "每窗 %.2fs 低于 4s 建议下限。" % (per / FPS))
    for i, window in enumerate(windows, 1):
        pairs, errors = pair_d_tags(window)
        for pos, msg in errors:
            doc.add("error", "G40", None, "第 %d 窗：%s" % (i, msg))
        for a, b, c, _d in pairs:
            inner = window[b:c]
            if not D_CONTENT_RE.match(inner):
                doc.add("error", "G40", None,
                        "第 %d 窗对白格式不对:'<d>%s</d>'。改法:写成 '<d>[Chinese] 逐字台词</d>'。"
                        % (i, inner.strip()[:30]))
        masked = mask_spans(window, [(a, d) for a, _b, _c, d in pairs])
        configured = _configured_visible_text(doc)
        for m in CJK_RE.finditer(masked):
            prefix = masked[max(0, m.start() - 120):m.start()]
            if VISIBLE_RE.search(prefix) or VISIBLE_OBLIGATION_RE.search(prefix):
                continue
            if any(q.group(1) in configured for q in QUOTE_RE.finditer(prefix)):
                continue
            doc.add("error", "G40", None,
                    "第 %d 窗在 <d> 之外出现中文 '%s'。改法:台词放进 '<d>[Chinese] ...</d>'，"
                    "描述改写英文。" % (i, m.group(0)[:20]))
            break
        # 单镜的 G13/G14/G18 依赖段名，多窗没有段名，同样的对白事实必须按窗补查一遍。
        # 说话人判定要跟 G14 同一套口径，否则同一份稿在两个模式下给相反结论：
        #   ①先按句号截断到本句（不跨句找），②本句无 (Sx) 且上一句同窗有说话人、
        #   中间字符数 ≤120 就沿用，③<Audio N> 作发声源时官方不要求 (Sx)。
        # 先扫全窗，得到「每句对白之前最近的 (Sx)」序列，再逐句判断。
        # 直接边循环边找会漏掉「本句没写 (Sx)、上一句写了」的承接情形。
        # 判定与 G14 完全同构：从本窗起点到 <d> 之间找最近的 (Sx)（含更早的句子）；
        # 找不到时，只有「上一句对白之后到本句之间」≤120 字符才允许沿用上一句的说话人。
        prev_spk = None
        prev_end = 0
        for a, b, c, d in pairs:
            lead = window[prev_end:a] if prev_end else window[:a]
            spk = list(re.finditer(r"\(S\d+\)", lead))
            if spk:
                prev_spk = spk[-1].group(0)
            elif prev_spk is not None and len(lead.strip()) <= 120:
                pass                      # 沿用上一句的说话人
            elif re.search(r"<Audio \d+>", lead):
                prev_spk = None
                prev_end = d
                continue                  # 官方 ref-en.txt:270：复用音轨歌词不编 (Sx)
            else:
                doc.add("warn", "G40", None,
                        "第 %d 窗这句对白找不到说话人 ID：'<d>%s</d>'。"
                        "从本窗开头到这句之间没有 (S1)/(S2)，也无法从上一句承接。"
                        "多人同场时模型分不清谁在说。"
                        "改法:在引出台词的那句里写 '<Subject 1> (S1) says'。"
                        % (i, window[b:c].strip()[:30]))
            prev_end = d
        for a, b, c, d in pairs:
            inner = window[b:c]
            # 台词超时长：语速与 G18 同一口径（--rate，默认 4.1 字/秒），
            # 否则同一句话在单镜报 error、在多窗报通过。
            per_win = per / FPS if per else None
            if per_win:
                rate = getattr(doc.args, "rate", 4.1) or 4.1
                han = len(HAN_RE.findall(inner))
                if han:
                    need = han / rate
                    if need > per_win + 0.4:
                        doc.add("warn", "G40", None,
                                "第 %d 窗台词 %d 个汉字，按 %.1f 字/秒约需 %.1fs，"
                                "超过本窗 %.2fs，念不完。改法:删减台词或加长窗口。"
                                % (i, han, rate, need, per_win))
                else:
                    words = len(re.findall(r"[A-Za-z']+", inner))
                    if words:
                        # 英文按同一条语速折算：中文 4.1 字/秒 ≈ 英文 3.2 词/秒
                        need = words / (rate * 0.78)
                        if need > per_win + 0.4:
                            doc.add("warn", "G40", None,
                                    "第 %d 窗台词 %d 个英文词，按 %.1f 词/秒约需 %.1fs，"
                                    "超过本窗 %.2fs，念不完。改法:删减台词或加长窗口。"
                                    % (i, words, rate * 0.78, need, per_win))
        # G11/G17 在单镜靠段名取主段，多窗没有段名，按窗补查同一事实。
        if per is not None:
            win_dur = per / FPS
            for tm in TS_RE.finditer(masked):
                t = ts(tm.group(0))
                if t > win_dur + TIME_TOL:
                    doc.add("error", "G40", None,
                            "第 %d 窗时间戳 %s 超过本窗时长 %s。改法:把动作/台词收在 %s 之前;"
                            "多窗每个窗口的时间轴从 00:00.000 重新开始。"
                            % (i, tm.group(0), fmt_ts(win_dur), fmt_ts(win_dur)))
                    break
        for a, b, c, d in pairs:
            ctx = window[max(0, a - LIPS_WINDOW):min(len(window), d + LIPS_WINDOW)]
            if (OFFSCREEN_RE.search(ctx)
                    and not (LIPS_RE.search(window) and CLOSED_RE.search(window))):
                doc.add("warn", "G40", None,
                        "第 %d 窗台词附近有 off-screen 说话人,但没写画内人物闭嘴:'<d>%s</d>'。"
                        "改法:补一句画内人物 does not speak, lips remain completely closed。"
                        % (i, window[b:c].strip()[:24]))
        # 台词重复：同一句在多窗重复出现，模型会当成两次发声。
        # 中英都要比：只比汉字串会让整段英文台词漏检（英文 <d> 里没有汉字）。
        def _norm_dialogue(text):
            said = " ".join(text[b:c] for _a, b, c, _d in pair_d_tags(text)[0])
            said = re.sub(r"\[[A-Za-z][A-Za-z \-]*\]", " ", said)
            return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", said.lower())

        win_said = _norm_dialogue(window)
        # 官方 base-en.txt:142 要求跨切点的同一句台词在两侧各写一次 <scenetrans> 并复述，
        # 那种重复是合规的；只有「没有 <scenetrans> 声明却重复」才是模型会念两遍的错。
        win_has_trans = "<scenetrans>" in window
        if len(win_said) >= 8:
            for prev_i, prev_win in enumerate(windows[:i - 1], 1):
                prev_said = _norm_dialogue(prev_win)
                if not prev_said:
                    continue
                dup = (win_said == prev_said
                       or (len(win_said) > 12 and win_said in prev_said)
                       or (len(prev_said) > 12 and prev_said in win_said))
                if not dup:
                    continue
                if win_has_trans and "<scenetrans>" in prev_win:
                    continue          # 跨切点声明过的复述，合规
                doc.add("warn", "G40", None,
                        "第 %d 窗的台词与第 %d 窗重复出现且没有 <scenetrans> 声明：模型会当成两次发声。"
                        "改法:一句台词只在一个窗口里出现,后续窗口用动作/反应承接;"
                        "确实要跨切点延续同一句时,两侧都写 <scenetrans>。"
                        % (i, prev_i))
                break


def rule_g28(doc: Doc) -> None:
    """官方 base-en.txt:62:FL2VA favors a single shot;多段只在显式声明时才允许。

    实测(2026-10-22《示例项目》EP01 v4):把 FL2VA 提示词写成
    `[Shot 1]/[Shot 2] At 00:01.200/[Shot 3] At 00:02.800` 三段式后,
    H3 在帧 66(= 2.75s,正好对上 `At 00:02.800`)产生真硬切:
    相邻帧亮度差 106.5/255、直方图距离 0.64,机位与光照瞬时全换。
    同批另 5 段同写法却没触发 => 概率性诱发,不能拿「这次没炸」当通过。

    与 video-studio 的 h3_lint P0-4 同判据,两条闸门必须一致:
    漏一条就等于没有闸门(此前 h3_gate 完全没有这条检查,三段式反而 exit=0)。
    """
    if doc.mode != "base":
        return
    shots = sorted({int(m.group(1)) for m in SHOT_RE.finditer(doc.masked)})
    if len(shots) < 2:
        return
    # 帧号两种写法都要认:官方对齐句与项目正文都是裸 `Picture 1`(base-en.txt:25/:201)
    pics = {int(m.group(2) or m.group(4)) for m in LABEL_RE_ANY.finditer(doc.text)
            if (m.group(1) or m.group(3)) == "Picture"}
    if not (1 in pics and 2 in pics):
        return  # 只加载一张帧的是 I2VA / L2VA,不受单段约束(官方 Case 4 L2VA 即单张尾帧)
    low = doc.masked.lower()
    declared = any(k in low for k in (
        "the camera cuts to", "the shot cuts to", "the shot transitions to",
        "the shot changes to", "the shot switches to", "cross-dissolve",
        "hard cut", "smash cut", "jump cut", "match cut", "cuts directly to", "cuts back to",
        "the scene cuts to", "the camera switches to"))
    if declared:
        return  # 官方 base-en.txt:62 允许显式声明的多段
    doc.add("error", "G28", None,
            "FL2VA 同时加载了 Picture 1 与 Picture 2(首尾帧插值),却写了 %d 个 [Shot N] 且未声明硬切。"
            "官方要求 FL2VA 单段(base-en.txt:62)。实测分段会在该时间码处抽出真硬切。"
            "改法:合并为 [Shot 1]、删掉所有 `At MM:SS.mmm`,用一条连续运镜串完,"
            "结尾写 `decelerates into the exact ... of Picture 2 at the end of the shot`。"
            % len(shots))


NEG_FIELD_RE = re.compile(r"^[ \t]*(?:negative|negative_prompt|neg)\s*[:=]", re.I | re.M)


def rule_g29(doc: Doc) -> None:
    """H3 在 cfg 1 没有负向分支,提示词里出现 `negative:` 字段形态必为死配置。

    官方依据:minimax-h3-prompt-guide.md:39 —— "No negatives: BasicGuider runs at
    cfg 1 with no negative branch." 源码亦证:comfy/samplers.py:610 在 cfg≈1.0 时
    把 uncond 置 None,_calc_cond_batch:240 直接跳过,负面条件根本不进模型。

    判据只认「字段名形态」(行首 `negative:` / `negative_prompt:` / `neg=`),
    不认正文里的 no/not/never —— 校准实测:官方 base-en.txt 含 12 处、ref-en.txt 含
    34 处 no/not/never/without,官方 3D 动画 skill 更自带 6 连「不要…」风格锁。
    按数量或按词面拦正文否定会误伤官方原文,所以本条一律放行;
    `do not show` 这类正文单句否定同理不拦。
    """
    for m in NEG_FIELD_RE.finditer(doc.masked):
        doc.add("error", "G29", m.start(),
                "用了 `negative:` 字段形态。H3 在 cfg 1 无负向分支(官方 guide §8),"
                "这一段不参与采样,等于没写。改法:① 写应然(state what should appear);"
                "② Ref2VA 用 retention 字段划保留边界(fully_preserved / partially_preserved);"
                "③ 要让某物不出现,就别描述它(见 failure-modes 出场治理三件套)。"
                "正文里的单句否定不必删,那是官方用法。")


def rule_g30(doc: Doc) -> None:
    """每个可见 Subject 都要有可核对的素材来源；不做违反官方多对多关系的数量相等检查。"""
    for (typ, num), (pos, entry) in sorted(doc.standalone_labels().items(), key=lambda kv: kv[1][0]):
        if typ != "Subject":
            continue
        label = "<Subject %d>" % num
        refs = [(m.group(1), int(m.group(2)), m.start()) for m in LABEL_RE.finditer(entry)]
        pictures = [(n, p) for t, n, p in refs if t == "Picture"]
        if doc.refs is not None:
            for pic_num, rel_pos in pictures:
                if pic_num > doc.refs:
                    doc.add("error", "G30", pos + rel_pos,
                            "%s 的定义引用了 <Picture %d>,但 --refs 只有 %d 张图。改法:绑定实际上传的身份图,"
                            "或修正 --refs/上传顺序。" % (label, pic_num, doc.refs))
        # 官方允许 in/from、多图共享，也允许 Subject 来自 Video；Audio/纯画外声音是合法例外。
        if pictures or any(t in ("Video", "Audio") for t, _n, _p in refs):
            continue
        if VOICE_SUBJECT_RE.search(entry):
            continue
        if LEGACY_SUBJECT_SOURCE_RE.search(entry):
            if doc.refs is not None:
                level = "error" if doc.refs == 0 else "warn"
                doc.add(level, "G30", pos,
                        "%s 仍使用未编号的 character reference image,无法逐 Subject 核对身份图。"
                        "改法:改成 '%s is ... in <Picture k>' 并核对实际上传顺序。" % (label, label))
            continue
        doc.add("error", "G30", pos,
                "%s 的 subject_definitions 没有可核对的参考来源。改法:写明 '%s is ... in <Picture k>';"
                "官方 Video/Audio 来源或纯画外声音主体也可保留。" % (label, label))


def rule_g31(doc: Doc) -> None:
    """首帧措辞只提醒人工核对，不禁止确实以冻结首帧开场的合法稿。"""
    declared: Set[Tuple[int, int]] = set()
    for pos, entry in doc.retention_entries():
        parsed = ENTRY_RE.fullmatch(doc.masked[pos:pos + len(entry)])
        if (not parsed or parsed.group(1) != "Picture"
                or parsed.group("marker") not in VISUAL_MARKERS or not parsed.group("desc").strip()):
            continue
        role = re.fullmatch(r"\[Shot (\d+)\]\s+first\s+frame", parsed.group("paren") or "", re.I)
        if role:
            declared.add((int(parsed.group(2)), int(role.group(1))))

    seen: Set[Tuple[int, Optional[int]]] = set()
    main = doc.main
    for m in FIRST_FRAME_RE.finditer(doc.masked):
        num = int(m.group(1) or m.group(2))
        # 定义句用显式镜号，正文用当前 [Shot k]；缺号或句内跨镜引用不推猜。
        explicit = {int(n) for n in SHOT_RE.findall(_sentence_around(doc.masked, m.start()))}
        shot = next(iter(explicit)) if len(explicit) == 1 else None
        if main and main.cstart <= m.start() < main.cend:
            preceding = list(SHOT_RE.finditer(doc.masked, main.cstart, m.start()))
            current = int(preceding[-1].group(1)) if preceding else None
            shot = current if not explicit or explicit == {current} else None
        key = (num, shot)
        if key in seen:
            continue
        seen.add(key)
        # 只有正确 retention 条目里同图、同镜的首帧声明能豁免；无法判镜号时保留提醒。
        if shot is not None and (num, shot) in declared:
            continue
        doc.add("warn", "G31", m.start(),
                "<Picture %d> 被写成首帧/开场锚点('%s')。请核对该图是否确为本镜真实起始帧(第 0 秒的画面);"
                "若它是 `用途：构图` 的核心参考画面、或只是身份板/结果态,改成 `<Picture %d> is the composition anchor for "
                "[Shot 1] … shows the arrangement reached around 00:0X.X`,正文在对应时刻写 `Around 00:0X.000 the arrangement "
                "corresponds to <Picture %d>`。真实起始帧无需删除此写法。"
                % (num, m.group(0), num, num))


def _dialogue_role_names(doc: Doc) -> Dict[str, str]:
    """只收集已定义 Subject/系列角色的中文名与别名，不把任意中文词当说话人。"""
    names: Dict[str, str] = {}

    def collect(value: str, owner: str) -> None:
        for name in HAN_RUN_RE.findall(value):
            if 2 <= len(name) <= 20:
                names.setdefault(name, owner)

    for _pos, entry in doc.def_entries():
        m = DEF_START_RE.match(entry)
        if m and m.group(1) == "Subject":
            collect(entry, "<Subject %s>" % m.group(2))
    for ch in (doc.config or {}).get("characters", []):
        owner = "角色 %s" % ch.get("id", "?")
        for key in ("trigger", "name", "id"):
            value = ch.get(key)
            if isinstance(value, str):
                collect(value, owner)
        aliases = ch.get("aliases", [])
        if isinstance(aliases, str):
            aliases = [aliases]
        if isinstance(aliases, list):
            for alias in aliases:
                if isinstance(alias, str):
                    collect(alias, owner)
    return names


def rule_g32(doc: Doc) -> None:
    names = _dialogue_role_names(doc)
    if not names:
        return
    for dl in doc.dialogues():
        for name in sorted(names, key=len, reverse=True):
            prefix = re.compile(r"^\s*(?:[【\[]\s*)?%s\s*(?:[】\]]\s*)?[:：]" % re.escape(name))
            if not prefix.match(dl.content):
                continue
            doc.add("error", "G32", dl.open_pos,
                    "<d> 台词以已定义的%s '%s' 加冒号开头,疑似把说话人标签写进台词正文。"
                    "改法:删掉台词内的 '%s:'/'%s：',说话人保留在 <d> 前的 Subject (Sx) 或稳定声音描述。"
                    % (names[name], name, name, name))
            break
            break


def rule_g33(doc: Doc) -> None:
    """G33 切点对账:给了 --storyboard 秒数表时,每个 [Shot k] (k>=2) 的 At 时刻必须等于
    前面各镜秒数的累计(内部语料来源 cutStarts 逐字对账规则的移植)。能由代码推导的值,不允许
    LLM 手写后无人对账。未给 --storyboard 时本规则不跑,与 G22 无时间约束不跑同语义。"""
    seconds_list = getattr(doc.args, "storyboard_seconds", None)
    if not seconds_list:
        return
    main = doc.main
    if main is None:
        return
    shots = section_shots(doc, main.cstart, main.cend)
    if not shots:
        return  # G10 已经报过"没有 [Shot 1]",这里不重复
    # 期望切点:第 k 镜(0 基)的切点 = 前 k 镜秒数之和
    expected: Dict[int, float] = {}
    acc = 0.0
    for idx, sec in enumerate(seconds_list):
        if idx + 1 < len(seconds_list):
            acc += sec
            expected[idx + 2] = acc  # [Shot idx+2] 开始于前 idx+1 镜累计
    n_written = len(seconds_list)
    for m in shots:
        n = int(m.group(1))
        if n == 1:
            continue
        after = doc.masked[m.end():m.end() + 40]
        tm = re.match(r"\s*,?\s*At (\d{2}:\d{2}\.\d{3})", after)
        if n > n_written:
            if tm:
                doc.add("error", "G33", m.start(),
                        "[Shot %d] 在 --storyboard 只声明了 %d 镜,没有第 %d 镜的秒数可对账。"
                        "改法:补全秒数表或删除多余的镜头标记。" % (n, n_written, n))
            continue
        want = expected.get(n)
        if want is None:
            continue  # 最后一镜没有后续切点
        if not tm:
            doc.add("error", "G33", m.start(),
                    "[Shot %d] 缺少切镜时间。按 --storyboard 应为 'At %s,'。"
                    % (n, fmt_ts(want)))
            continue
        got = ts(tm.group(1))
        if abs(got - want) > 0.0005:
            doc.add("error", "G33", m.start(),
                    "[Shot %d] 切镜时间写 %s,但 --storyboard 各镜秒数累计应为 %s。"
                    "改法:按分镜秒数改写,或修正分镜时长。" % (n, tm.group(1), fmt_ts(want)))


def rule_g26(doc: Doc) -> None:
    """官方 Ref2VA 输入配额:图 ≤ 9、视频 ≤ 3、音频 ≤ 3、总文件 ≤ 12(来自 CS-H3 导演台说明与节点定义 max)。"""
    counts = {}
    for typ in ("Picture", "Video", "Audio"):
        nums = {int(m.group(2)) for m in LABEL_RE.finditer(doc.text) if m.group(1) == typ}
        counts[typ] = len(nums)
    lim = {"Picture": 9, "Video": 3, "Audio": 3}
    for typ, n in counts.items():
        if n > lim[typ]:
            doc.add("error", "G26", None,
                    "<%s N> 共 %d 个,超过 Ref2VA 输入上限 %d。改法:合并或删减参考素材。" % (typ, n, lim[typ]))
    if sum(counts.values()) > 12:
        doc.add("error", "G26", None, "参考素材总数 %d 超过 12。改法:删减到 ≤ 12。" % sum(counts.values()))


def rule_g27(doc: Doc) -> None:
    """官方 3d-animation-short-generator STEP 7:分镜双绑定标签 [char:…][scene:…][shot:…][dur:…][hook:…]
    是分镜专用参考标记,不得进入最终视频提示词(会被模型当成画面内容)。"""
    pat = re.compile(r"\[(char|scene|shot|dur|hook)\s*:", re.I)
    hits = [(m.start(), m.group(1).lower()) for m in pat.finditer(doc.text)]
    if hits:
        first = hits[0]
        doc.add("error", "G27", first[0],
                "发现分镜双绑定标签 [%s:…](共 %d 处)。官方 STEP 7 要求渲染前剥离 "
                "[char:…][scene:…][shot:…][dur:…][hook:…],它们是分镜交叉引用标记,不是画面内容。"
                "改法:删掉这些标签,保留其中的实质信息(角色/场景/时长/hook 已由提示词其他段落承担)。"
                % (first[1], len(hits)))


# G34: EP001 vehicle-motion case reminder. Lateral motion may be intentional;
# these lexical matches cannot determine camera geometry or model capability.
VEHICLE_CTX_RE = re.compile(
    r"\b(?:car|sedan|saloon|vehicle|truck|van|bus|dashboard|windscreen|windshield|steering wheel|"
    r"driver'?s seat|passenger seat|cabin)\b", re.I)
_LATERAL = (r"(?:across (?:the )?frame|across the (?:shot|picture|screen)|sideways|laterally|horizontally|"
            r"from (?:the )?left to (?:the )?right|from (?:the )?right to (?:the )?left)")
# 背景/景物横向流过:车内镜头里的错误"前进感"
BACKGROUND_LATERAL_RE = re.compile(
    r"\b(?:slid(?:e|es|ing)|stream(?:s|ing)?|flow(?:s|ing)?|sweep(?:s|ing)?|drift(?:s|ing)?|"
    r"roll(?:s|ing)?|glid(?:e|es|ing)|scroll(?:s|ing)?|run(?:s|ning)?)\b[^.;\n]{0,80}?\b" + _LATERAL, re.I)
# 车本身横穿画面,或摄影机与车平行横移
VEHICLE_CROSSING_RE = re.compile(
    r"\b(?:car|sedan|saloon|vehicle|truck|van|bus)(?:'s)?\b(?:\s+[\w,'-]+){0,2}?\s+"
    r"(?:driv(?:e|es|ing)|drove|mov(?:e|es|ing)|travel(?:s|ling|ing)?|pass(?:es|ing)?|cross(?:es|ing)?|"
    r"roll(?:s|ing)?|glid(?:e|es|ing)|slid(?:e|es|ing)|go(?:es|ing)?|run(?:s|ning)?)\b[^.;\n]{0,40}?"
    r"\b" + _LATERAL, re.I)
CAMERA_SIDE_TRACK_RE = re.compile(
    r"\b(?:trucks?|trucking|tracks?|tracking|dolly|dollies|dollying)\s+(?:sideways|laterally|to the (?:left|right))\b",
    re.I)
# Negated mentions remain visible as advisory matches: the rule does not parse
# sentence intent, so both exclusions and intentional motion need human context.


def rule_g34(doc: Doc) -> None:
    text = doc.masked
    if not VEHICLE_CTX_RE.search(text):
        return
    seen = set()
    for rx, level, what, fix in (
        (BACKGROUND_LATERAL_RE, "warn", "景物横向流过画面",
         "在既有车内案例条件下观察到横滑;核对机位、路沿和相对运动是否符合本镜。"
         "正向行驶可用消失点与近景透视后退,侧向取景仍可合法横移。词匹配不证明方向错误。"),
        (VEHICLE_CROSSING_RE, "warn", "车横穿画面",
         "核对车头朝向、路径与摄影机关系。固定侧视的合法横穿可以保留;本提醒不要求改成车尾纵深。"),
        (CAMERA_SIDE_TRACK_RE, "warn", "摄影机横移",
         "核对摄影机是否真与车辆同动,还是场景仅有停靠车辆。保留已确认的跟拍选择,实看方向和空间。"),
    ):
        for m in rx.finditer(text):
            key = (level, m.start() // 20)
            if key in seen:
                continue
            seen.add(key)
            doc.add(level, "G34", m.start(),
                    "%s:'%s'。%s" % (what, " ".join(m.group(0).split())[:90], fix))
            break  # 每类只报第一处,避免同一问题刷屏


# G35: 设备屏幕朝镜头。看屏幕应该把机位绕到人背后(越肩),而不是让角色把设备递给镜头
# (2026-11-01 EP001 002A:模型把手机转向镜头)。
DEVICE_RE = r"(?:phone|smartphone|mobile|screen|tablet|laptop|device)"
SCREEN_TO_CAMERA_RE = re.compile(
    r"\b" + DEVICE_RE + r"\b[^.;\n]{0,40}?\b(?:toward|towards|facing|turned to|turns to|angled to|held out to|holds? out to|"
    r"shown to|shows? to|presented to|handed to|hands? to)\s+(?:the\s+)?(?:camera|lens|viewer|audience)\b"
    r"|\b(?:holds?|raises?|lifts?|turns?|tilts?|shows?|presents?)\s+(?:up\s+)?(?:the\s+|his\s+|her\s+)?" + DEVICE_RE +
    r"\b[^.;\n]{0,30}?\b(?:to|toward|towards|at)\s+(?:the\s+)?(?:camera|lens|viewer)\b",
    re.I)


def rule_g35(doc: Doc) -> None:
    text = doc.masked
    for m in SCREEN_TO_CAMERA_RE.finditer(text):
        if re.search(r"\b(?:back|rear|shell|casing|away)\b", m.group(0), re.I):
            continue  # 背壳朝镜头 = 屏幕背向镜头,正是想要的机位(EP001 030/S20)
        doc.add("warn", "G35", m.start(),
                "设备屏幕朝向镜头:'%s'。核对是否是本镜已确认的展示动作;若意图是人物自己读屏,"
                "可用越肩机位。提醒不裁决合法展示或否定句,也不授权新增机位。"
                % " ".join(m.group(0).split())[:90])
        break


# G36: List body negations for semantic review. Absence of a separate negative
# conditioning branch does not imply failure to understand linguistic negation.
# A warning is not a quality verdict or a requirement to remove every exclusion.
NEGATION_RE = re.compile(
    r"\b(?:no|not|never|nobody|nothing|none|without|neither|nor|cannot|can't|isn't|aren't|"
    r"doesn't|don't|didn't|won't)\b", re.I)
G36_SHOW = 4


def rule_g36(doc: Doc) -> None:
    text = doc.masked
    hits = [m for m in NEGATION_RE.finditer(text) if text[m.end():m.end() + 4].strip().upper() != "N/A"]
    if not hits:
        return
    examples = []
    last = -999
    for m in hits:
        if len(examples) >= G36_SHOW:
            break
        if m.start() - last < 45:
            continue  # 同一个短语里的连续否定只展示一次
        last = m.start()
        a = max(0, m.start() - 6)
        b = min(len(text), m.end() + 28)
        examples.append("'%s'" % " ".join(text[a:b].split()))
    doc.add("warn", "G36", hits[0].start(),
            "正文含 %d 处否定(%s%s)。回读与本镜状态/时间线是否相容;优先正向可见状态,"
            "必要的行为、空间或发声边界可以保留。无独立负向条件分支不证明正文否定失效;"
            "本项只提示语义核对,不以否定词数量放行或拒绝。"
            % (len(hits), "、".join(examples), "…" if len(hits) > G36_SHOW else ""))


# G38: 绝对保持词。"全程 / for the entire shot / in every frame / the whole time" 声明一件事整段不变,
# 与时间线里会动的同一对象互相打架时,模型两头听(example-project:先写左手平放桌沿,后写
# "左腕全程贴着下巴")。只列出来让人逐个对照时间线,不判断是否真矛盾。
ABSOLUTE_HOLD_RE = re.compile(
    r"\b(?:throughout(?:\s+(?:the\s+)?(?:(?:whole|entire)\s+)?"
    r"(?:shot|video|clip|scene|sequence|time|duration)|(?=\s*[,.;:!?]|\s*$))|"
    r"the\s+(?:whole|entire)\s+(?:time|shot|video|clip)|"
    r"for\s+the\s+(?:entire|whole)\s+(?:shot|video|clip|time|duration)|in\s+every\s+frame|"
    r"from\s+the\s+first\s+frame\s+to\s+the\s+last|all\s+the\s+way\s+through)\b", re.I)
G38_SHOW = 4


def _sentence_around(text: str, pos: int) -> str:
    # 小数点（包括 MM:SS.mmm）后接数字，不是句界；句末标点与换行才分句。
    a, b = 0, len(text)
    for boundary in re.finditer(r"[.!?](?=\s|$)|\n", text):
        if boundary.end() <= pos:
            a = boundary.end()
        elif boundary.start() >= pos:
            b = boundary.end()
            break
    return " ".join(text[a:b].split())


def rule_g38(doc: Doc) -> None:
    main = doc.main
    if main is None:
        return
    text = doc.masked
    shot_count = len(list(SHOT_RE.finditer(text, main.cstart, main.cend)))
    hits = []
    for m in ABSOLUTE_HOLD_RE.finditer(text, main.cstart, main.cend):
        sentence = _sentence_around(text, m.start())
        # 单镜只豁免主语和保持对象均为摄影机自身的锁定句；演员朝向 camera 不构成豁免。
        camera_lock = re.fullmatch(
            r"(?:\[Shot \d+\]\s*)?(?:At\s+\d+:\d+\.\d+\s*,\s*)?(?:The\s+)?camera\s+"
            r"(?:holds?\s+(?:its\s+(?:distance|position|height|framing)|"
            r"(?:a\s+)?locked[- ]off\s+(?:(?:medium|wide|close|low|high)[- ]?){0,3}shot)|"
            r"(?:is|remains?|stays?)\s+(?:locked[- ]off|fixed|stationary))\s+"
            + ABSOLUTE_HOLD_RE.pattern + r"[.!]?", sentence, re.I)
        if shot_count < 2 and camera_lock:
            continue
        if any(sentence == prior for _m, prior in hits):
            continue  # 同一句里的多个绝对词只算一处
        hits.append((m, sentence))
    if not hits:
        return
    shown = ["'%s'" % (s if len(s) <= 110 else s[:107] + "...") for _m, s in hits[:G38_SHOW]]
    doc.add("warn", "G38", hits[0][0].start(),
            "正文含 %d 处绝对保持词(%s%s)。这些词声明\"整段不变\";请逐个对照时间线,确认同一对象(手、袖口、道具、机位)"
            "在别处没有被写成会动或换位。会动的东西改成按时刻写(`<部位或物件> <状态> until <时刻>, then <变化>`);"
            "多镜容器里的\"摄影机全程保持\"会覆盖各 [Shot N] 自己的取景,应删掉。"
            % (len(hits), "、".join(shown), "…" if len(hits) > G38_SHOW else ""))


# G42: 身份靠图锁，正文不逐句复述外貌（ref-subject-picture.md §3b）。
# 判据：同一个 <Subject N> 的外貌描述里，同一串 >=4 词的短语在主段里出现 >=3 次。
# 看「同一串话重复」而不是看词性：写不同动作、每次带一个新外貌细节是正常的，
# §3b 反例的病是把同一串「dark chestnut ... worn loose and down ... falling freely」逐句抄。
G42_MIN_REPEAT = 3
G42_NGRAM = 5
G42_STATIC_RE = re.compile(
    r"\b(?:hair|ponytail|bangs|fringe|braids?|complexion|jawline|face\s+shape|cheekbones|"
    r"skin\s+tone|eye\s+colou?r|beak|scarf|jumpsuit|hat|backpack)\b", re.I)


def rule_g42(doc: Doc) -> None:
    main = doc.main
    if main is None:
        return
    body = doc.masked[main.cstart:main.cend]
    sentences = [x for x in re.split(r"(?<=[.!?])\s+|\n", body) if x.strip()]
    for sm in sorted({int(m.group(1)) for m in re.finditer(r"<Subject (\d+)>", body)}):
        tag = "<Subject %d>" % sm
        counts: Dict[Tuple[str, ...], List[str]] = {}
        for sent in sentences:
            if tag not in sent and not re.match(r"\s*(?:Her|His|Their)\b", sent):
                continue
            words = [w.lower() for w in EN_WORD_RE.findall(sent)]
            seen_here: Set[Tuple[str, ...]] = set()
            for k in range(len(words) - G42_NGRAM + 1):
                gram = tuple(words[k:k + G42_NGRAM])
                if gram in seen_here or not G42_STATIC_RE.search(" ".join(gram)):
                    continue
                seen_here.add(gram)
                counts.setdefault(gram, []).append(sent.strip())
        rep = [(g, ss) for g, ss in counts.items() if len(ss) >= G42_MIN_REPEAT]
        if rep:
            g, ss = max(rep, key=lambda kv: len(kv[1]))
            doc.add("warn", "G42", None,
                    "%s 的外貌短语 '%s' 在正文里重复了 %d 句。身份已由参考图锁定,"
                    "官方 ref-en.txt:246 要求首次清晰出现时提一次,之后只用标签(ref-subject-picture.md §3b)。"
                    "改法:保留首次出现的一句,其余改为只写位置与动作。" % (tag, " ".join(g), len(ss)))


# G01 在建档时判定;其余规则表驱动
RuleFn = Callable[[Doc], None]
# 身份/场景/风格类素材的症状词（官方 ref-en.txt:68：这类图不得建独立 Picture 条目）
IDENTITY_SHEET_RE = re.compile(
    r"\b(?:character\s+(?:sheet|board|reference(?:\s+image)?|design)|three[- ]view|multi[- ]view|"
    r"turnaround|model\s+sheet|identity\s+(?:sheet|board|reference)|"
    r"reference\s+(?:sheet|board)|costume\s+sheet|style\s+(?:sheet|board|reference)|"
    r"scene\s+(?:sheet|board|plate)|location\s+(?:sheet|board))\b", re.I)
# 这些用途词说明该 Picture 确实当画面本体用，允许独立存在
PICTURE_FRAME_ROLE_RE = re.compile(
    r"\b(?:first\s+frame|opening\s+frame|last\s+frame|final\s+frame|"
    r"key\s?frame|edited\s+key\s?frame|composition\s+anchor|"
    r"storyboard(?:\s+reference)?|shot[- ]planning)\b", re.I)
# 官方四类标签之外的自造引用写法（如 "character reference image 2"、"图2"）
BARE_REF_RE = re.compile(
    r"(?:\b(?:character|identity|style|scene|costume)\s+reference\s+(?:image|photo|picture)\s+\d+"
    r"|\breference\s+(?:image|photo)\s+\d+\b"
    r"|(?<![<\w])\b(?:image|photo)\s+\d+\b(?!\s*(?:seconds?|secs?|s\b|frames?|times?|minutes?|%))"
    r"|\bthe\s+(?:second|third|fourth|fifth)\s+(?:image|photo|reference\s+(?:image|photo|picture))(?:\s+in\s+refs)?)", re.I)


def rule_g41(doc: Doc) -> None:
    """G41 身份/场景/风格参考图不得建成独立 <Picture N>（官方 ref-en.txt:68 反规则）。

    两类症状都拦：
    (a) 素材图被建成独立 Picture（旧错法）：定义行含角色板/三视图/风格图等词，
        却没有首帧/关键帧/尾帧/构图锚/分镜板等帧用途词。
    (b) 素材图改用自造裸描述引用（新错法）：出现 "character reference image 2"
        "the second image in refs" 这类官方四类标签之外的写法 —— 模型不认，
        且不同段落无法交叉引用同一实体。
    """
    sd = doc.sec.get("subject_definitions")
    if sd is None:
        return
    # 不锚行首：同一行里跟在 Subject 定义后面的 <Picture N> is ... 同样要查。
    # 取到下一个标签或换行为止（不按句号截断）：豁免词常常写在第二句
    # （'<Picture 2> is the identity reference for <Subject 1>. It is also the first frame of [Shot 1].'），
    # 按句号切会把 'first frame' 切掉，反而误判成身份板。
    # 边界只认「标签 + is」（下一条定义的起点）；像 '<Picture 2> is the identity reference
    # for <Subject 1>. It is also the first frame of [Shot 1].' 里的 <Subject 1> 只是引用，
    # 不能当边界，否则第二句的 'first frame' 会被切掉。
    for m in re.finditer(
            r"<(Picture) (\d+)>\s+is\b((?:(?!<(?:Picture|Subject|Video|Audio)\s+\d+>\s+is\b)[^\n])*)",
            sd.text):
        num, body = int(m.group(2)), m.group(3)
        if not IDENTITY_SHEET_RE.search(body):
            continue
        if PICTURE_FRAME_ROLE_RE.search(body):
            continue
        doc.add("error", "G41", sd.cstart + m.start(),
                "<Picture %d> 是身份/场景/风格参考图（%r），却建成独立 Picture 条目。"
                "官方 ref-en.txt:68：图若只用来定义角色、场景、服装或风格，不得建独立 Picture，"
                "应写进对应 <Subject N> 定义里引用。改法：删掉这条定义行，"
                "把这张图作为来源写进 Subject，如 '<Subject 1> is the woman in <Picture %d>, with ...'。"
                % (num, body.strip()[:60], num))
    # 裸引用要扫全文：正文才是模型真正读的地方，只在 subject_definitions 里查等于漏掉主战场。
    for m in BARE_REF_RE.finditer(doc.text):
        doc.add("error", "G41b", m.start(),
                "用了官方四类标签之外的引用写法 %r。模型只认 <Subject N>/<Picture N>/"
                "<Video N>/<Audio N>；裸描述无法跨段引用同一实体，也会被当成画面内容。"
                "改法：该素材若是可见内容来源，写进对应 <Subject N> 定义"
                "（'<Subject 1> is the woman in <Picture 2>, with ...'），"
                "正文一律用 <Subject 1> 指代，不要用 'character reference image 2'。"
                % m.group(0))


RULES: List[Tuple[str, Tuple[str, ...], RuleFn, str]] = [
    ("G02", ("ref", "base"), rule_g02, "段落齐全且顺序正确"),
    ("G03", ("ref", "base"), rule_g03, "模式不混用"),
    ("G04", ("ref",), rule_g04, "[Shot 1] 前有英文风格开场"),
    ("G05", ("ref",), rule_g05, "标签均已定义"),
    ("G06", ("ref",), rule_g06, "需要独立定义的标签有独立行"),
    ("G07", ("ref",), rule_g07, "独立标签都有 retention 条目"),
    ("G08", ("ref", "base"), rule_g08, "标签编号连续,与上传张数一致"),
    ("G09", ("ref",), rule_g09, "retention_analysis 条目格式与 marker"),
    ("G10", ("ref", "base"), rule_g10, "镜头标记与切镜时间"),
    ("G11", ("ref", "base"), rule_g11, "时间戳不越界、不倒退"),
    ("G12", ("ref", "base"), rule_g12, "帧数满足 17k+5"),
    ("G13", ("ref", "base"), rule_g13, "<d>[Language] ...</d> 格式"),
    ("G14", ("ref", "base"), rule_g14, "说话人 ID"),
    ("G15", ("ref", "base"), rule_g15, "中文只在 <d> 内"),
    ("G16", ("ref", "base"), rule_g16, "对白不进音频段、不重复"),
    ("G17", ("ref", "base"), rule_g17, "画外说话时写明画内闭嘴"),
    ("G18", ("ref", "base"), rule_g18, "台词时长与叠词"),
    ("G19", ("ref", "base"), rule_g19, "音频段写法"),
    ("G20", ("ref", "base"), rule_g20, "正文英文词数"),
    ("G21", ("base",), rule_g21, "base 模式参考图对齐首行"),
    ("G22", ("ref", "base"), rule_g22, "白天/夜晚冲突"),
    ("G23", ("ref",), rule_g23, "summary 任务类型前缀(官方枚举)"),
    ("G24", ("ref", "base"), rule_g24, "<scenetrans>/<cutoff> 标签"),
    ("G25", ("ref", "base"), rule_g25, "时长 4-15s(本地容量);节点硬顶3600f;--allow-long-video 豁免长端"),
    ("G26", ("ref",), rule_g26, "参考素材输入配额"),
    ("G27", ("ref", "base"), rule_g27, "无分镜双绑定标签泄漏"),
    ("G28", ("base",), rule_g28, "FL2VA 首尾帧必须单段(官方 base-en.txt:62)"),
    ("G29", ("ref", "base"), rule_g29, "无 `negative:` 字段形态(cfg1 无负向分支)"),
    ("G30", ("ref",), rule_g30, "Subject 均有可核对且不越界的参考来源"),
    ("G31", ("ref",), rule_g31, "首帧措辞已提示人工核对"),
    ("G32", ("ref", "base"), rule_g32, "台词正文无角色名/说话人标签泄漏"),
    ("G33", ("ref", "base"), rule_g33, "切点时刻与 --storyboard 秒数累计对账"),
    ("G34", ("ref", "base"), rule_g34, "车辆运动方向(不横穿画面、不让景物横向流过)"),
    ("G35", ("ref", "base"), rule_g35, "设备屏幕不朝向镜头(越肩看屏幕)"),
    ("G36", ("ref", "base"), rule_g36, "正文否定句提醒(H3 无负向通道)"),
    ("G38", ("ref", "base"), rule_g38, "绝对保持词提醒(与时间线互相打架)"),
    ("G39", ("multishot",), rule_g39, "多窗脚本格式(窗口数/窗口开头/不混单镜段名)"),
    ("G40", ("multishot",), rule_g40, "多窗逐窗内容(对白格式/<d>外中文/每窗时长)"),
    ("G42", ("ref",), rule_g42, "正文不逐句复述身份外貌(身份靠图锁)"),
    ("G41", ("ref",), rule_g41, "身份/场景/风格参考图不得建成独立 <Picture N>"),
]


def run_rules(doc: Doc) -> List[str]:
    """运行单文件规则;返回实际运行过的规则 ID。"""
    if doc.mode is None:
        doc.add("error", "G01", None,
                "无法判定模式:文件里既没有 'subject_definitions:'(ref 六段)也没有 "
                "'integrated_multimodal_description:'(base 三段)。改法:按 ref-en.txt 或 base-en.txt 补齐段落,或用 --mode 指定。")
        return ["G01"]
    ran = ["G01"]
    for rid, modes, fn, _desc in RULES:
        if doc.mode in modes:
            if rid == "G22" and not _g22_words(doc):
                continue  # NOTCHK:未配置时间约束,不能在 verbose 里冒充检查通过
            fn(doc)
            ran.append(rid)
    return ran


# ---------------------------------------------------------------------------
# series 规则
# ---------------------------------------------------------------------------

def _identity_line(doc: Doc, trigger: str) -> Optional[Tuple[int, str]]:
    sd = doc.sec.get("subject_definitions")
    if sd is None:
        return None
    pos = sd.cstart
    for line in sd.text.split("\n"):
        if trigger.lower() in line.lower():
            return pos, line.strip()
        pos += len(line) + 1
    return None


def rule_s01(docs: List[Doc], cfg: dict) -> None:
    for doc in docs:
        low = doc.masked.lower()
        sd = doc.sec.get("subject_definitions")
        sd_low = (doc.mtext(sd) if sd else (doc.mtext(doc.main) if doc.main else "")).lower()
        for ch in cfg.get("characters", []):
            trig = ch["trigger"].lower()
            if trig not in low:
                continue
            missing = [w for w in ch.get("must_include", []) if w.lower() not in sd_low]
            if missing:
                doc.add("error", "S01", sd.hpos if sd else None,
                        "角色 %s('%s')的 subject_definitions 缺少设定词:%s。改法:把这些服装/特征词写进该角色的定义行。"
                        % (ch.get("id", "?"), ch["trigger"], ", ".join(missing)))
            for w in ch.get("forbid", []):
                for m in word_pattern(w).finditer(doc.masked):
                    if is_negated(doc.masked, m.start()):
                        continue
                    doc.add("error", "S01", m.start(),
                            "角色 %s 出现禁用描述 '%s'(与设定冲突)。改法:改为设定里的写法(%s)。"
                            % (ch.get("id", "?"), m.group(0), ", ".join(ch.get("must_include", [])) or "见设定"))
                    break


def rule_s02(docs: List[Doc], cfg: dict) -> None:
    for ch in cfg.get("characters", []):
        first: Optional[Tuple[Doc, str]] = None
        for doc in docs:
            hit = _identity_line(doc, ch["trigger"])
            if hit is None:
                continue
            pos, line = hit
            if first is None:
                first = (doc, line)
                continue
            if line != first[1]:
                diff = word_diff(first[1], line)
                doc.add("warn", "S02", pos,
                        "角色 %s 的身份定义句与 %s 不逐字相同,差异:%s。改法:跨镜直接复制同一句身份定义。"
                        % (ch.get("id", "?"), os.path.basename(first[0].path), "; ".join(diff) or "(空白差异)"))


def rule_s03(docs: List[Doc], cfg: dict) -> None:
    tod = cfg.get("time_of_day")
    if not tod:
        return
    req = tod.get("require_any", [])
    forbid = tod.get("forbid_any", [])
    for doc in docs:
        if req and not any(word_pattern(w).search(doc.masked) for w in req):
            doc.add("warn", "S03", None,
                    "全文没有任何时间设定词(%s)。改法:在风格开场或环境定义里写明,如 'bright afternoon daylight'。"
                    % ", ".join(req))
        for w in forbid:
            for m in word_pattern(w).finditer(doc.masked):
                if is_negated(doc.masked, m.start()):
                    continue
                doc.add("warn", "S03", m.start(),
                        "出现与系列时间设定冲突的 '%s'。改法:删掉,或写成否定 'never %s'。" % (m.group(0), w))
                break


def rule_s04(docs: List[Doc], cfg: dict) -> None:
    smap = cfg.get("speaker_map") or {}
    if not smap:
        return
    chars = cfg.get("characters", [])
    kws = {ch["id"]: trigger_keywords(ch["trigger"]) for ch in chars if "id" in ch}
    for doc in docs:
        main = doc.main
        if main is None:
            continue
        subj_to_char: Dict[str, str] = {}
        for _p, entry in doc.def_entries():
            m = DEF_START_RE.match(entry)
            if not m or m.group(1) != "Subject":
                continue
            for ch in chars:
                if ch["trigger"].lower() in entry.lower():
                    subj_to_char["<Subject %s>" % m.group(2)] = ch["id"]
        done: Set[str] = set()
        for m in SPK_RE.finditer(doc.masked, main.cstart, main.cend):
            sx = "S" + m.group(1)
            if sx in done:
                continue
            ws = max(main.cstart, m.start() - SPEAKER_WINDOW)
            win = doc.masked[ws:m.start()].lower()
            best: Optional[Tuple[int, str]] = None
            for cid, words in kws.items():
                for w in words:
                    for km in re.finditer(r"\b%s\b" % re.escape(w), win):
                        if best is None or km.end() > best[0]:
                            best = (km.end(), cid)
            for lm in LABEL_RE.finditer(doc.masked[ws:m.start()]):
                cid = subj_to_char.get(lm.group(0))
                if cid and (best is None or lm.end() > best[0]):
                    best = (lm.end(), cid)
            if best is None:
                continue
            done.add(sx)
            expected = smap.get(best[1])
            if expected and expected != sx:
                doc.add("warn", "S04", m.start(),
                        "(%s) 前的说话人看起来是 %s,而 speaker_map 约定 %s=%s。官方 Sx 按单次视频内发声先后编号,"
                        "跨镜一致性靠音色参考不靠编号,所以只提示;若想统一,调整台词顺序或在提交时绑定同一音色参考。"
                        % (sx, best[1], best[1], expected))


SERIES_RULES = [("S01", rule_s01), ("S02", rule_s02), ("S03", rule_s03), ("S04", rule_s04)]


def run_series(docs: List[Doc], cfg: Optional[dict]) -> List[str]:
    if not cfg:
        return []
    live = [d for d in docs if d.mode is not None]
    ran = []
    for rid, fn in SERIES_RULES:
        fn(live, cfg)
        ran.append(rid)
    return ran


# ---------------------------------------------------------------------------
# 命令行
# ---------------------------------------------------------------------------

class UsageError(Exception):
    pass


def load_config(path: str) -> dict:
    try:
        with open(path, "r", encoding="utf-8-sig") as fh:
            cfg = json.load(fh)
    except OSError as e:
        raise UsageError("无法读取 --series-config %s:%s" % (path, e))
    except json.JSONDecodeError as e:
        raise UsageError("--series-config %s 不是合法 JSON:%s" % (path, e))
    if not isinstance(cfg, dict):
        raise UsageError("--series-config 顶层必须是 JSON 对象")
    chars = cfg.get("characters", [])
    if not isinstance(chars, list):
        raise UsageError("--series-config 的 characters 必须是数组")
    for i, ch in enumerate(chars):
        if not isinstance(ch, dict) or not isinstance(ch.get("trigger"), str) or not ch["trigger"].strip():
            raise UsageError("--series-config characters[%d] 缺少字符串 trigger" % i)
        ch.setdefault("id", "char%d" % (i + 1))
        for k in ("must_include", "forbid"):
            v = ch.setdefault(k, [])
            if not isinstance(v, list) or not all(isinstance(x, str) for x in v):
                raise UsageError("--series-config characters[%d].%s 必须是字符串数组" % (i, k))
    tod = cfg.get("time_of_day")
    if tod is not None and not isinstance(tod, dict):
        raise UsageError("--series-config 的 time_of_day 必须是对象")
    sm = cfg.get("speaker_map")
    if sm is not None and not isinstance(sm, dict):
        raise UsageError("--series-config 的 speaker_map 必须是对象")
    return cfg


def read_text(path: str) -> str:
    try:
        with open(path, "r", encoding="utf-8-sig") as fh:
            return fh.read().replace("\r\n", "\n").replace("\r", "\n")
    except FileNotFoundError:
        raise UsageError("文件不存在:%s" % path)
    except UnicodeDecodeError:
        raise UsageError("文件不是 UTF-8 编码:%s(请另存为 UTF-8)" % path)
    except OSError as e:
        raise UsageError("无法读取文件 %s:%s" % (path, e))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="h3_gate.py",
        description="MiniMax H3 视频提示词交稿前闸门(ref 六段 / base 三段)。多文件时顺序即镜序。",
    )
    p.add_argument("files", nargs="+", metavar="FILE", help="提示词文件;多个文件按镜序排列")
    p.add_argument("--mode", choices=["auto", "ref", "base", "multishot"], default="auto",
                   help="默认 auto 自动判定；multishot = 多窗脚本（窗口用单独一行 --- 分隔）")
    p.add_argument("--shot-count", type=int, default=None, dest="shot_count",
                   help="multishot: 期望窗口数；给定则核对窗口数，并检查每个窗口都以正文开头")
    g = p.add_mutually_exclusive_group()
    g.add_argument("--frames", type=int, help="总帧数(24fps)")
    g.add_argument("--seconds", type=float, help="总秒数")
    p.add_argument("--refs", type=int, help="本次实际上传的参考图张数")
    p.add_argument("--allow-long-video", action="store_true", dest="allow_long_video",
                   help="豁免 G25 长视频 error 降为 warn(仅供不经 h3q 的手搓直投通道;节点 3600f 硬顶不受豁免)")
    p.add_argument("--rate", type=float, default=4.1, help="中文台词语速 字/秒,默认 4.1")
    p.add_argument("--series-config", dest="series_config", help="跨镜一致性配置 JSON")
    p.add_argument("--storyboard", help="分镜秒数表 JSON(数组,按镜序,如 [3.0, 2.5, 4.0]);给定则启用 G33 切点对账")
    p.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    p.add_argument("--strict", action="store_true", help="warn 也算失败")
    p.add_argument("-v", "--verbose", action="store_true", help="同时列出通过的规则")
    return p


def _setup_stdout() -> None:
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")  # type: ignore[attr-defined]
        except (AttributeError, ValueError):
            pass


def main(argv: Optional[Sequence[str]] = None) -> int:
    _setup_stdout()
    args = build_parser().parse_args(argv)
    try:
        if args.rate <= 0:
            raise UsageError("--rate 必须大于 0")
        if args.frames is not None and args.frames <= 0:
            raise UsageError("--frames 必须是正整数")
        if args.seconds is not None and args.seconds <= 0:
            raise UsageError("--seconds 必须大于 0")
        if args.refs is not None and args.refs < 0:
            raise UsageError("--refs 不能为负数")
        config = load_config(args.series_config) if args.series_config else None
        if args.storyboard:
            sb = json.loads(read_text(args.storyboard))
            if isinstance(sb, dict):
                # {"shots": [{"seconds": 3.0}, ...]} 或 {"seconds": [3.0, ...]} 都收
                sb = sb.get("shots") or sb.get("seconds")
            if isinstance(sb, list):
                cleaned = []
                for item in sb:
                    if isinstance(item, dict):
                        item = item.get("seconds", item.get("duration_seconds"))
                    if not isinstance(item, (int, float)) or item <= 0:
                        raise UsageError("--storyboard 秒数必须是正数,收到: %r" % (item,))
                    cleaned.append(float(item))
                args.storyboard_seconds = cleaned
            else:
                raise UsageError("--storyboard 应为秒数数组 JSON,收到: %r" % (sb,))
        else:
            args.storyboard_seconds = None
        docs = [Doc(p, read_text(p), args, config) for p in args.files]
    except UsageError as e:
        if args.json:
            print(json.dumps({"error": str(e), "exit_code": 2}, ensure_ascii=False))
        else:
            print("[ERROR] 用法/文件错误:%s" % e, file=sys.stderr)
        return 2

    ran: Dict[str, List[str]] = {}
    for d in docs:
        ran[d.path] = run_rules(d)
    series_ran: List[str] = []
    series_note = None
    if len(docs) > 1 or config:
        series_ran = run_series(docs, config)
        if not config:
            series_note = "多文件但未提供 --series-config,已跳过 S01–S04。"

    findings: List[Finding] = []
    order = {d.path: i for i, d in enumerate(docs)}
    for d in docs:
        findings.extend(d.findings)
    findings.sort(key=lambda f: (order.get(f.file, 0), f.line or 0, f.rule))
    n_err = sum(1 for f in findings if f.level == "error")
    n_warn = sum(1 for f in findings if f.level == "warn")
    code = 1 if n_err or (args.strict and n_warn) else 0

    if args.json:
        out = {
            "files": [
                {
                    "file": d.path,
                    "mode": d.mode,
                    "frames": d.frames,
                    "duration_seconds": d.duration,
                    "duration_source": d.dur_source,
                    "errors": sum(1 for f in d.findings if f.level == "error"),
                    "warnings": sum(1 for f in d.findings if f.level == "warn"),
                }
                for d in docs
            ],
            "findings": [f.as_dict() for f in findings],
            "series_rules": series_ran,
            "summary": {
                "files": len(docs),
                "errors": n_err,
                "warnings": n_warn,
                "strict": args.strict,
                "exit_code": code,
            },
        }
        if series_note:
            out["note"] = series_note
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return code

    desc = {rid: d for rid, _m, _f, d in RULES}
    desc["G01"] = "模式可判定"
    for d in docs:
        mine = [f for f in findings if f.file == d.path]
        for f in mine:
            loc = "%s:L%d" % (f.file, f.line) if f.line else f.file
            print("[%s] %s %s %s" % (f.level.upper(), f.rule, loc, f.message))
        if args.verbose:
            hit = {f.rule for f in mine} | {"G08" for f in mine if f.rule == "G08b"}
            for rid in ran[d.path]:
                if rid not in hit:
                    print("[OK] %s %s %s" % (rid, d.path, desc.get(rid, "")))
        if not mine:
            print("[OK] ALL %s 全部检查通过(mode=%s)" % (d.path, d.mode))
    if series_note:
        print("注:" + series_note)
    verdict = "通过" if code == 0 else "未通过"
    print("汇总:%d 个文件,%d error,%d warn%s → %s(exit %d)"
          % (len(docs), n_err, n_warn, ",--strict 生效" if args.strict else "", verdict, code))
    return code


if __name__ == "__main__":
    sys.exit(main())
