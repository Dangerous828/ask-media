#!/usr/bin/env python3
"""Validate the executable cross-document contract of one creator-first episode."""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path, PurePosixPath
from collections.abc import Iterable
from typing import NamedTuple, Optional


MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit(
        "creator_markdown_check.py requires Python {}.{}, running {}.{}".format(
            *MINIMUM_PYTHON, sys.version_info.major, sys.version_info.minor
        )
    )


REQUIRED_DOCUMENTS = (
    "剧本.md",
    "视觉设定.md",
    "图片提示词.md",
    "分镜.md",
    "视频提示词.md",
)
SECTION_RE = re.compile(r"^## ((?:SHOT|MOTION)-[A-Z0-9-]+)\b", re.MULTILINE)
IMG_RE = re.compile(r"\b(IMG-[A-Z0-9-]+)《([^》]+)》（控制：([^）]+)）")
# 用途 is optional in the pattern on purpose: a declaration written before this
# field existed still parses, so the creator gets "REF 缺少用途" instead of the
# generic syntax error that gives no hint about what to add.
REF_RE = re.compile(
    r"(REF-[A-Z0-9-]+)（顺序：([1-9]\d*)）· "
    r"([^；\n]+?\.(?:png|jpe?g|webp))《([^》\n]+)》"
    r"（(?:用途：([^；）\n]+)；)?控制：([^；）]+)；不得控制：([^）]+)）",
    re.IGNORECASE,
)
# The same slot grammar, but the locator is a document entry instead of a file.
# A creator who generates in an external tool never has the file inside the
# project, and the copyable body only ever needed 顺序 and 用途 -- the path is a
# production input, not a prompt input. PLAN says "this picture does not exist
# here; attach it yourself in this order", which is a different claim from
# 「已有图片」 and from 「待补」.
PLAN_RE = re.compile(
    r"(PLAN-[A-Z0-9-]+)（顺序：([1-9]\d*)）· "
    r"((?:IMG-[A-Z0-9-]+|SHOT-[A-Z0-9-]+(?:#KF-[A-Z0-9-]+)?))《([^》\n]+)》"
    r"（(?:用途：([^；）\n]+)；)?控制：([^；）]+)；不得控制：([^）]+)）",
    re.IGNORECASE,
)
# One picture answers one question. 「同一张图承担两个作用时分开说明」 in
# references/reference-roles.md is what makes a slot translatable into a
# provider role, so the vocabulary is closed rather than free prose. The list
# lives in ``enums.py`` — the shared single source — and is re-exported here
# because the checker body and the tests read it off this module.


def _load_enums():
    path = Path(__file__).resolve().with_name("enums.py")
    spec = importlib.util.spec_from_file_location("creator_markdown_enums", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load the shared enums: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


REF_PURPOSES = _load_enums().REF_PURPOSES
_enums = _load_enums()
# A character's voice travels on its own line, `- 参考音频：`, never inside
# 输入参考图: the picture slots number `@图片N`/`<Picture N>`/`图N` and the audio
# slots number `@音频N`/`<Audio N>`/`音频N`, each from 1, so mixing them in one
# field would renumber every picture after the first voice.
AUDIO_SUFFIXES = ("wav", "mp3", "m4a", "aac", "flac")
AUDIO_REF_RE = re.compile(
    r"(REF-[A-Z0-9-]+)（顺序：([1-9]\d*)）· "
    r"([^；\n]+?\.(?:" + "|".join(AUDIO_SUFFIXES) + r"))《([^》\n]+)》"
    r"（用途：([^；）\n]+)；角色：([^；）\n]+)；控制：([^；）]+)；不得控制：([^）]+)）",
    re.IGNORECASE,
)
AUDIO_PURPOSE = "音色"
AUDIO_SYNTAX = (
    "REF-<槽位>（顺序：<n>）· <音频路径>《<中文名>》"
    "（用途：音色；角色：<人物名>；控制：<范围>；不得控制：<范围>）"
)
# An audio file or 用途：音色 in a picture field is a voice binding written in
# the wrong place; the generic "broken REF syntax" would not say where it goes.
AUDIO_IN_IMAGE_FIELD_RE = re.compile(
    r"\.(?:" + "|".join(AUDIO_SUFFIXES) + r"|opus)《|用途：音色", re.IGNORECASE
)
# Where 《视觉设定.md》 records a character's accepted voice reference: one
# line under that 人物 entry, path first.
VOICE_RECORD_RE = re.compile(
    r"^[ \t　]*[-*+][ \t　]*声音参考[：:](.*)$", re.MULTILINE
)
# Same filename rule as the binding's locator (`[^；\n]+?`), so any path a
# 参考音频 slot may name can also be the recorded one -- spaces included.
VOICE_RECORD_PATH_RE = re.compile(
    r"([^（；\n]+?\.(?:" + "|".join(AUDIO_SUFFIXES) + r"))(?=（|$)", re.IGNORECASE
)
# The screenplay's dialogue grammar, mirrored from the write skill's
# screenplay_index.py (DIALOGUE_RE, and TAG_RE + VOICE_TAG_BODY_RE for [VO] and
# [OS]). Each is matched against a whole paragraph, so a line that wraps onto
# the next physical line is still one line of dialogue.
SCREENPLAY_DIALOGUE_RE = re.compile(
    r"^(?P<speaker>[^\s：（）:\[\]#]{1,40})"
    r"(?:（[^（）\r\n]+）)?：(?P<text>\S[\s\S]*)$"
)
SCREENPLAY_VOICE_TAG_RE = re.compile(
    r"^\[(?:VO|OS)\]\s*(?P<speaker>[^\s：（）:\[\]#]{1,40})：(?P<text>\S[\s\S]*)$"
)
# A later line of a paragraph that starts another block (the index's
# ASCII_DIALOGUE_RE, ANY_TAG_RE and MALFORMED_TAG_RE): the paragraph is missing
# a separator and the index emits no dialogue for it.
SCREENPLAY_BLOCK_START_RE = re.compile(
    r"^[^\s：（）:\[\]#]{1,40}(?:（[^（）\r\n]+）)?:\s*\S"
    r"|^\[[^\]\r\n]+\]"
    r"|^\[(?:VO|OS|SFX|画面文字|连续性|转场)(?:\s|：|:)"
)
# Where the clause that introduces a quote begins.
CLAUSE_BREAK_RE = re.compile(r"[。！？；.!?;]")
# `EP001-SC001` is the documented shape, but a project that scopes ids by season
# writes `S01-EP001-SC001`. Both are one stable scene id, so the pattern takes
# any hyphenated prefix rather than exactly one segment.
SLOT_HEAD_RE = re.compile(
    r"(?:REF|PLAN)-[A-Za-z0-9][A-Za-z0-9-]*（顺序：", re.IGNORECASE
)
SCENE_ID_PATTERN = r"(?:[A-Za-z0-9]+-)+SC[0-9]+"
SCENE_HEADING_RE = re.compile(
    r"^## (" + SCENE_ID_PATTERN + r")\b", re.MULTILINE
)
SCENE_ID_RE = re.compile(SCENE_ID_PATTERN)
# A scene the storyboard decided not to film. SHT-01 has always allowed the
# omission and always required a reason; without a place to write it the
# omission and an oversight look identical in the finished document.
UNFILMED_LINE_RE = re.compile(
    r"^[ \t\u3000]*[-*+][ \t\u3000]*未拍场次[：:](.*)$", re.MULTILINE
)
UNFILMED_ENTRY_RE = re.compile(
    r"(" + SCENE_ID_PATTERN + r")（理由：([^）\n]+)）"
)
# Dialogue reaches the model as a quoted run, either inside the H3 `<d>` tag or
# inside quotation marks. Runs shorter than four Han characters are in-frame
# labels and interjections far more often than they are lines, so the check
# stays off them rather than inventing an escape hatch for signage.
SPOKEN_SPAN_RE = re.compile(r"<d>([^<]*)</d>|[\"“]([^\"”]*)[\"”]|「([^」]*)」")
SPOKEN_RUN_RE = re.compile(r"[\u3400-\u9fff]{4,}")
EXPLICIT_TEXT_TO_VIDEO = "无（创作者已明确选择文生视频）"
PENDING_REFERENCE_SUFFIX_RE = re.compile(r"；待补参考图：[^；。\n]+。?$")
VISUAL_CATEGORIES = ("人物", "造型", "地点", "道具")
# A malformed entry always tries to name something; a heading that is only the
# category word is a section divider ("## 人物"), and rejecting it left the
# document with no way to group entries at all.
VISUAL_SETTING_LINE_RE = re.compile(
    r"^#{2,4}[ \t　]*(?:"
    + "|".join(VISUAL_CATEGORIES)
    + r")(?![ \t　]*$)[^\n]*$",
    re.MULTILINE,
)
VISUAL_SETTING_HEADING_RE = re.compile(
    r"^## (" + "|".join(VISUAL_CATEGORIES) + r") · (.+?)[ \t　]*$", re.MULTILINE
)
# Any other `## <word> · <name>` heading, so a 视觉依据 entry that fails to
# resolve can say "the entry is there, the section word is not one of the four"
# instead of blaming the storyboard for a `视觉设定.md` problem.
OTHER_SETTING_HEADING_RE = re.compile(r"^## ([^\n·]+?) · (.+?)[ \t　]*$", re.MULTILINE)
# 画面代称 is the one field the coverage check depends on, so — like a
# continuity lock — anything that looks like it has to parse rather than
# silently drop out.
# Anchored at the start of the line so a sentence that merely mentions the
# field is prose, not a malformed declaration.
SCREEN_NAME_LINE_RE = re.compile(
    r"^[ \t　]*[-*+]?[ \t　]*画面代称[ \t　]*[：:][^\n]*$", re.MULTILINE
)
SCREEN_NAME_RE = re.compile(
    r"^[ \t　]*[-*+][ \t　]*画面代称[：:](.+)$", re.MULTILINE
)
VISUAL_BASIS_PREFIX = "《视觉设定.md》·"
VISUAL_BASIS_ENTRY_RE = re.compile(
    r"(" + "|".join(VISUAL_CATEGORIES) + r")「([^」\n]+)」（控制：([^）\n]+)）"
)
# A subject a keyframe names but does not show — an owner's abandoned bag, a
# name on a screen, a homonym of an entry name. SHT-22 excludes these from
# coverage, so the field needs a way to say so instead of forcing the creator
# to declare an absent subject as present.
OFFSCREEN_PREFIX = "；画外："
OFFSCREEN_ENTRY_RE = re.compile(
    r"(" + "|".join(VISUAL_CATEGORIES) + r")「([^」\n]+)」"
)
# Composition is a per-shot contract for every person declared visible in 视觉依据.
# The still-prompt gate later verifies that these decisions reach the actual English.
CAMERA_LOCK_LINE_RE = re.compile(r"^[-*+]\s*(?:\*\*)?机位锁(?:\*\*)?：([^\n]+)$", re.MULTILINE)
PERSON_COMPOSITION_LINE_RE = re.compile(
    r"^[-*+]\s*(?:\*\*)?人物构图(?:\*\*)?：([^｜\n]+)｜(.+)$", re.MULTILINE
)
NEGATIVE_GAZE_TARGET_RE = re.compile(
    r"不看|没看|不要看|禁止看|避免看|而非|而不是|not\s+looking|avoid\s+looking|away\s+from",
    re.IGNORECASE,
)
# 镜头静帧的七项取景字段，放在可复制正文外。历史正文首行格式兼容读取。
# 字段保留事实，不用词长或摄影名词表替代语义判断，也不反过来改分镜。
KEYFRAME_PROMPT_HEADINGS = (
    ("冻结关键帧提示词", r"冻结关键帧提示词"),
    ("核心参考画面", r"核心参考画面(?:（[^）]*）)?"),
    ("收尾关键帧提示词", r"收尾关键帧提示词"),
    ("起始帧提示词", r"起始帧提示词"),
)
KEYFRAME_POSE_HEADING = "关键姿势提示词"
CAMERA_LANGUAGE_PREFIX = "镜头语言："
CAMERA_LANGUAGE_SLOTS = (
    "景别",
    "水平角度",
    "机位高度",
    "焦段意图",
    "构图",
    "焦点",
    "帧相位",
)
CAMERA_LANGUAGE_FRAMINGS = (
    "大远景", "远景", "全景", "中全景", "中近景", "中景",
    "近景", "特写", "大特写", "插入特写",
)
CAMERA_LANGUAGE_ANGLES = ("正面", "斜侧", "正侧", "后斜侧", "背面", "轴线")
CAMERA_LANGUAGE_HEIGHTS = ("地平", "低", "仰", "平视", "高", "俯", "顶视")
CAMERA_LANGUAGE_FOCALS = ("广角", "标准", "长焦")
CAMERA_LANGUAGE_PHASES = ("起幅", "中段", "落幅", "固定单帧", "姿势瞬间")
# A declared lock must never become a no-op. Anything that *looks* like a lock
# line -- any list marker, any leading whitespace -- is captured here and then
# has to parse, so a creator who indents the bullet under 识别锚点 gets an error
# instead of silent non-enforcement.
LOCK_LINE_RE = re.compile(r"^[ \t\u3000]*[-*+][ \t\u3000]*连续性锁[：:].*$", re.MULTILINE)
LOCK_RE = re.compile(
    r"^[ \t\u3000]*[-*+][ \t\u3000]*连续性锁：(LOCK-[A-Z0-9-]+)《([^》\n]+)》"
    r"（镜头：([^；）\n]+)"
    r"(?:；图片提示词项：([^；）\n]+))?）"
    r"· 锁面：(.+)$"
)
# The surface has to name what is in the picture. A match glued to a negation
# ("no pale blue sweater") describes what must be absent, so it cannot be the
# evidence that the fact is present.
# Chinese runs without spaces, so the CJK markers cannot require a preceding
# boundary the way the English ones do. A bare 无 is deliberately not a marker:
# 无袖毛衣 describes the garment rather than excluding it.
NEGATION_RE = re.compile(
    r"(?:"
    r"(?:^|[\s,;:(\[/—-])(?:no|not|non|never|without|avoid|excludes?|excluding|"
    r"free\s+of|--?no)(?:\s+(?:a|an|the|any|some))?[\s-]*"
    r"|(?:不要|不得|不能|不应|不含|不出现|没有|未|避免|禁止|排除|去掉|移除)"
    r"(?:出现|包含|存在|带|有)?[\s]*"
    r")$",
    re.IGNORECASE,
)


def _sections(document: str, kind: str) -> dict[str, str]:
    matches = [
        match
        for match in SECTION_RE.finditer(document)
        if match.group(1).startswith(f"{kind}-")
    ]
    return {
        match.group(1): document[
            match.start() : matches[index + 1].start()
            if index + 1 < len(matches)
            else None
        ]
        for index, match in enumerate(matches)
    }


def _fields(section: str, *, owner: str, errors: list[str]) -> dict[str, str]:
    pairs = re.findall(r"^- ([^：\n]+)：(.+)$", section, re.MULTILINE)
    fields: dict[str, str] = {}
    for key, value in pairs:
        # `- **参考**：…` is ordinary Markdown and reads as the same field to a
        # human. Taking the emphasis literally turned it into a different key,
        # so the author got "缺少参考字段" while looking straight at 参考.
        key = re.sub(r"^(?:\*\*|__|\*|_)(.+?)(?:\*\*|__|\*|_)$", r"\1", key.strip())
        # 人物构图 is deliberately repeated once per visible person and is parsed
        # by _check_composition_locks, not as a scalar field.
        if key == "人物构图":
            continue
        if key in fields:
            errors.append(f"{owner}: 字段重复: {key}")
        fields[key] = value
    return fields


def _plain(value: str) -> str:
    return value.strip().rstrip("。")


def _contains_ref_token(value: str) -> bool:
    return "ref-" in value.casefold()


def _contains_plan_token(value: str) -> bool:
    return "plan-" in value.casefold()


def _contains_slot_token(value: str) -> bool:
    return _contains_ref_token(value) or _contains_plan_token(value)


def _is_none(value: str) -> bool:
    # `[^）]+` would stop at the first closing bracket, so a gap list that names
    # an entry in brackets -- 「角色A人物图（IMG-...）」 -- fell through to the REF
    # syntax error, whose obvious repair is deleting the gap record. That is the
    # silent downgrade this contract exists to prevent, so the note takes any
    # content as long as it is bracketed.
    return not _contains_slot_token(value) and bool(
        re.fullmatch(r"无(?:（.+）)?", _plain(value), re.DOTALL)
    )


def _is_explicit_text_to_video(value: str) -> bool:
    return _plain(value) == EXPLICIT_TEXT_TO_VIDEO


def _has_pending_references(value: str) -> bool:
    plain = _plain(value)
    return plain.startswith("无（待补参考图：") or bool(
        PENDING_REFERENCE_SUFFIX_RE.search(value.strip())
    )


def _is_no_external_reference(value: str) -> bool:
    return not _contains_slot_token(value) and bool(
        re.fullmatch(r"无(?:外部参考)?(?:；[^\n]*)?。?", value.strip())
    )


PROMPT_METADATA_RE = re.compile(r"^[-*+] (?:Frame|镜头语言)[：:]")


def _copyable_prompt(
    section: str, heading: str = r"可复制(?:通用)?提示词"
) -> Optional[str]:
    markers = list(re.finditer(rf"^### {heading}\s*$", section, re.MULTILINE))
    if len(markers) != 1:
        return None
    body = section[markers[0].end() :]
    following = re.search(r"^###\s+|^##\s+", body, re.MULTILINE)
    if following is not None:
        body = body[: following.start()]
    lines = [line for line in body.splitlines() if line.strip() and not PROMPT_METADATA_RE.match(line)]
    if not lines or any(not line.startswith(">") for line in lines):
        return None
    prompt = "\n".join(line[1:].lstrip() for line in lines).strip()
    return prompt or None


def _copyable_prompt_cause(
    section: str, heading: str = r"可复制(?:通用)?提示词"
) -> str:
    """Why `_copyable_prompt` returned None, as a suffix for the error.

    "缺少唯一且非空的可复制提示词" is true of four different documents and tells
    the author nothing about which one they wrote. The expensive case is a
    single stray line -- a separator, an HTML comment, a note -- inside an
    otherwise complete block: the prompt is visibly right there, so the message
    reads as a checker bug and the real line goes unlooked at.
    """

    # Name the heading the author actually has to write, not this one's default:
    # the keyframe caller passes a different one, and pointing at the wrong
    # heading is worse than saying nothing.
    label = "### " + re.sub(r"\(\?:([^)]*)\)\?", "", heading).replace("\\", "")
    markers = list(re.finditer(rf"^### {heading}\s*$", section, re.MULTILINE))
    if not markers:
        return f"：没有 `{label}` 小节标题"
    if len(markers) > 1:
        return f"：`{label}` 出现了 {len(markers)} 次，只能有一个"
    body = section[markers[0].end() :]
    following = re.search(r"^###\s+|^##\s+", body, re.MULTILINE)
    if following is not None:
        body = body[: following.start()]
    lines = [line for line in body.splitlines() if line.strip() and not PROMPT_METADATA_RE.match(line)]
    if not lines:
        return f"：`{label}` 下面是空的"
    intruders = [line for line in lines if not line.startswith(">")]
    if intruders:
        return (
            "：除引用块外的独立 `- Frame：...` / `- 镜头语言：...` 字段外，小节有不以 `>` 开头的行——"
            f"保留该字段在正文外，其余杂项移到小节外或删掉：{_excerpt(intruders[0])}"
        )
    return "：引用块里只有空白"


def _extract_quote_block(body: str) -> Optional[str]:
    """取一小节里连续的 `>` 引用行；有非引用行则说明该块不是可复制正文。"""
    lines = [line for line in body.splitlines() if line.strip() and not PROMPT_METADATA_RE.match(line)]
    if not lines or any(not line.startswith(">") for line in lines):
        return None
    prompt = "\n".join(line[1:].lstrip() for line in lines).strip()
    return prompt or None


def _camera_metadata(body: str) -> str:
    """仅供检查：读取引用块外独立字段，不把它拼回实际可复制正文。"""
    return "\n".join(re.findall(r"^[-*+] (镜头语言：[^\n]+)$", body, re.MULTILINE))


def _heading_camera_metadata(section: str, heading: str) -> str:
    marker = re.search(rf"^### {heading}\s*$", section, re.MULTILINE)
    if not marker:
        return ""
    body = section[marker.end():]
    stop = re.search(r"^###\s+|^##\s+", body, re.MULTILINE)
    if stop:
        body = body[:stop.start()]
    return _camera_metadata(body)


def _keyframe_prompt_blocks(shot_body: str) -> list[tuple[str, str]]:
    """列出本镜所有必须携带七项镜头语言锚点的关键帧正文。"""
    blocks: list[tuple[str, str]] = []
    for label, heading in KEYFRAME_PROMPT_HEADINGS:
        prompt = _copyable_prompt(shot_body, heading=heading)
        if prompt:
            metadata = _heading_camera_metadata(shot_body, heading)
            blocks.append((label, metadata + "\n" + prompt if metadata else prompt))
    # 关键姿势提示词下允许逐张 `#### KF-...`，每张各有自己的引用块。
    marker = re.search(
        rf"^### {KEYFRAME_POSE_HEADING}\s*$", shot_body, re.MULTILINE
    )
    if marker:
        body = shot_body[marker.end() :]
        following = re.search(r"^###\s+|^##\s+", body, re.MULTILINE)
        if following is not None:
            body = body[: following.start()]
        parts = re.split(r"^#### (.+)$", body, flags=re.MULTILINE)
        if len(parts) > 1:
            for index in range(1, len(parts), 2):
                title = parts[index].strip()
                content = parts[index + 1] if index + 1 < len(parts) else ""
                prompt = _extract_quote_block(content)
                if prompt:
                    metadata = _camera_metadata(content)
                    blocks.append((f"关键姿势提示词「{title}」", metadata + "\n" + prompt if metadata else prompt))
        else:
            prompt = _extract_quote_block(body)
            if prompt:
                metadata = _camera_metadata(body)
                blocks.append((KEYFRAME_POSE_HEADING, metadata + "\n" + prompt if metadata else prompt))
    return blocks


def _camera_language_parts(anchor: str) -> list[str]:
    return [part.strip() for part in anchor.split("｜")]


def _check_camera_language_anchor(
    prompt: str, shot_id: str, label: str, errors: list[str]
) -> None:
    """检查独立七项字段，兼容历史正文首行；不要求中文元数据进入模型。"""
    anchors = [line.strip() for line in prompt.splitlines() if line.strip().startswith(CAMERA_LANGUAGE_PREFIX)]
    if len(anchors) != 1:
        errors.append(f"{shot_id}: {label} 必须有唯一镜头语言字段（兼容历史正文第一行），实际{len(anchors)}条")
        return
    first = anchors[0]
    parts = _camera_language_parts(first[len(CAMERA_LANGUAGE_PREFIX) :].strip())
    if len(parts) != len(CAMERA_LANGUAGE_SLOTS):
        errors.append(
            f"{shot_id}: {label} 镜头语言必须正好七项（实际 {len(parts)} 项）"
        )
        return
    values: list[str] = []
    for index, (slot, part) in enumerate(zip(CAMERA_LANGUAGE_SLOTS, parts)):
        if index < 4:
            value = part
        else:
            prefix = f"{slot}："
            if not part.startswith(prefix):
                errors.append(f"{shot_id}: {label} 镜头语言第 {index + 1} 项缺少「{prefix}」")
                value = ""
            else:
                value = part[len(prefix) :].strip()
        if not value:
            errors.append(f"{shot_id}: {label} 镜头语言「{slot}」为空")
        values.append(value)
    if len(values) != len(CAMERA_LANGUAGE_SLOTS):
        return
    # 景别/机位/焦点的艺术与物理意义须审读，不按词长或固定名词配额判定。
    if NEGATIVE_GAZE_TARGET_RE.search(values[1]):
        errors.append(f"{shot_id}: {label} 水平角度混进了否定式视线写法；朝向与视线分别记录")


def _check_keyframe_camera_language(
    shot_body: str, shot_id: str, errors: list[str]
) -> None:
    blocks = _keyframe_prompt_blocks(shot_body)
    if not blocks:
        return
    for label, prompt in blocks:
        _check_camera_language_anchor(prompt, shot_id, label, errors)


def _portable_path(value: str) -> bool:
    if not value or "\\" in value or re.match(r"^[A-Za-z]:", value):
        return False
    parts = value.split("/")
    return not PurePosixPath(value).is_absolute() and not any(
        part in {"", ".", ".."} for part in parts
    )


def _inside(path: Path, root: Path) -> bool:
    resolved = path.resolve()
    root = root.resolve()
    return resolved == root or root in resolved.parents


class EntryIndex(NamedTuple):
    """The document entries a `PLAN-...` locator is allowed to name."""

    images: dict[str, str]
    shots: frozenset
    frames: dict[str, dict[str, str]]


def _planned_frame_roles(shots: dict[str, str]) -> dict[str, dict[str, str]]:
    """Index only the plan table; a SHOT shorthand never means composition=start."""
    indexed = {}
    for shot_id, body in shots.items():
        headings = list(re.finditer(r"^### 画面证明计划\s*$", body, re.MULTILINE))
        roles = {}
        if len(headings) == 1:
            plan = body[headings[0].end():]
            following = re.search(r"^###\s+|^##\s+", plan, re.MULTILINE)
            if following is not None:
                plan = plan[:following.start()]
            for frame_id, role in re.findall(
                r"^\|\s*(KF-[A-Z0-9-]+)\s*\|\s*(composition|start|pose_proof|end)\s*\|",
                plan,
                re.MULTILINE,
            ):
                roles[frame_id] = "duplicate" if frame_id in roles else role
        indexed[shot_id] = roles
    return indexed


def _slot_matches(value: str) -> list:
    """Every `REF-...` and `PLAN-...` slot in `value`, in written order.

    The two patterns cannot match the same span: a REF locator has to be an
    image path and a PLAN locator has to be an `IMG-`/`SHOT-` id.
    """
    found = []
    for kind, pattern in (("REF", REF_RE), ("PLAN", PLAN_RE)):
        for match in pattern.finditer(value):
            found.append((match.start(), match.end(), kind, match.groups()))
    found.sort(key=lambda item: item[0])
    return found


def _references(
    value: str,
    owner: str,
    project_root: Path,
    errors: list[str],
    entries: Optional[EntryIndex] = None,
) -> frozenset:
    """Validate one 输入参考图/参考 declaration; return the slot kinds it uses."""
    if _is_none(value):
        return frozenset()
    # Backticks are Markdown emphasis around a slot, not part of its grammar.
    # Accept both `REF-...` as a whole-cell wrapper and per-token wrapping.
    value = value.replace("`", "")
    if AUDIO_IN_IMAGE_FIELD_RE.search(value):
        errors.append(
            f"{owner}: 输入参考图只收图片；角色音色参考写在《视频提示词.md》"
            "该 MOTION 的「- 参考音频：」行"
        )
        return frozenset()
    reference_value = PENDING_REFERENCE_SUFFIX_RE.sub("", value.strip())
    matches = _slot_matches(reference_value)
    cursor = 0
    separators_are_valid = True
    for index, (start, end, _kind, _groups) in enumerate(matches):
        if reference_value[cursor:start] != ("" if index == 0 else "；"):
            separators_are_valid = False
        cursor = end
    trailing = reference_value[cursor:]
    # Counted as slot heads on the same text the slots were matched in. A bare
    # token count would read the `ref-` in a real path like
    # `输入/参考图/ref-角色A.png` as a second slot and reject a correct declaration.
    declared = len(SLOT_HEAD_RE.findall(reference_value))
    kinds = frozenset(item[2] for item in matches)
    if (
        len(matches) != declared
        or not matches
        or not separators_are_valid
        or trailing not in {"", "。"}
    ):
        # A gap list joined with ； reads as a fourth REF slot and would otherwise
        # be reported as broken REF syntax, whose obvious repair is deleting the
        # gap record -- the silent downgrade this contract exists to prevent.
        if "待补参考图" in value and not _has_pending_references(value):
            errors.append(
                f"{owner}: 待补参考图必须写在最后一个 REF 槽位之后，"
                "缺口之间只用、分隔"
            )
        elif _contains_plan_token(value) and not _contains_ref_token(value):
            errors.append(f"{owner}: 输入参考图必须使用完整 PLAN 语法")
        else:
            errors.append(f"{owner}: 输入参考图必须使用完整 REF 语法")
        return kinds
    groups = [item[3] for item in matches]
    slot_kinds = [item[2] for item in matches]
    slots = [group[0] for group in groups]
    orders = [int(group[1]) for group in groups]
    locators = [group[2] for group in groups]
    purposes = [(group[4] or "").strip() for group in groups]
    # A declaration made only of PLAN slots is not a REF declaration, so its
    # diagnostics must not send the creator looking for a REF line.
    noun = "PLAN" if kinds == frozenset({"PLAN"}) else "REF"
    if len(slots) != len(set(slots)):
        errors.append(f"{owner}: {noun} 槽位重复")
    if len(orders) != len(set(orders)) or sorted(orders) != list(
        range(1, len(orders) + 1)
    ):
        errors.append(f"{owner}: {noun} 顺序必须唯一且从 1 连续编号")
    locator_purposes = list(zip(locators, purposes))
    if len(locator_purposes) != len(set(locator_purposes)):
        errors.append(f"{owner}: {noun} 路径与用途完全重复")
    for slot, purpose in zip(slots, purposes):
        if not purpose:
            errors.append(
                f"{owner}: {noun} 缺少用途: {slot}；用途只能是"
                f"{'、'.join(REF_PURPOSES)}其中一个"
            )
        elif purpose not in REF_PURPOSES:
            errors.append(
                f"{owner}: {noun} 用途不在允许集合内: {slot}（{purpose}）；"
                f"只能是{'、'.join(REF_PURPOSES)}"
            )
    for role in ("起始帧", "结束帧"):
        if purposes.count(role) > 1:
            errors.append(f"{owner}: 同一条目只能有一张{role}参考图")
    if "结束帧" in purposes and "起始帧" not in purposes:
        errors.append(f"{owner}: 绑定结束帧参考图时必须同时绑定起始帧")
    for index, (kind, group) in enumerate(zip(slot_kinds, groups)):
        slot, raw_locator, label = group[0], group[2], group[3]
        may_control, must_not_control = group[5], group[6]
        if kind == "REF":
            _check_project_file(raw_locator, owner, project_root, errors)
        else:
            _plan_locator(
                raw_locator, label, owner, slot, purposes[index], entries, errors
            )
        if not re.search(r"[\u4e00-\u9fff]", label):
            errors.append(f"{owner}: {kind} 缺少中文名称: {slot}")
        if not may_control.strip() or not must_not_control.strip():
            errors.append(f"{owner}: {kind} 必须同时声明控制与不得控制: {slot}")
        allowed = {item.strip() for item in re.split(r"[、,，]", may_control)}
        prohibited = {item.strip() for item in re.split(r"[、,，]", must_not_control)}
        if "" in allowed or "" in prohibited or allowed & prohibited:
            errors.append(f"{owner}: {kind} 控制与不得控制范围冲突: {slot}")
    return kinds


def _check_project_file(
    locator: str, owner: str, project_root: Path, errors: list[str]
) -> None:
    """A REF locator names a readable file inside the project, or it is a defect."""
    if not _portable_path(locator):
        errors.append(f"{owner}: REF 路径不是安全的项目相对路径: {locator}")
        return
    reference_path = project_root / locator
    if not _inside(reference_path, project_root):
        errors.append(f"{owner}: REF 路径越出项目根目录: {locator}")
    elif not reference_path.is_file():
        errors.append(f"{owner}: REF 文件不存在: {locator}")


def _han_key(value: str) -> str:
    """Only the Han characters, so quoting and language tags do not decide identity."""
    return "".join(re.findall(r"[\u3400-\u9fff]+", value))


class SpokenLine(NamedTuple):
    """One dialogue paragraph of 剧本.md: its scene, speaker and Han text."""

    scene: Optional[str]
    speaker: str
    key: str


def _screenplay_dialogue(screenplay: str) -> list[SpokenLine]:
    """Every dialogue paragraph, read the way screenplay_index.py reads it.

    Mirrors `_parse_screenplay` block by block: a comment runs through the line
    that closes it, and an unclosed one ends the parse; a heading sets or clears
    the scene (scene ids use this checker's own SCENE_HEADING_RE, the one
    来源 resolves against); a paragraph runs until a blank line, a heading or a comment and
    counts only inside a scene; a later line that starts another block means a
    missing separator, so the paragraph is not dialogue. The one difference is
    the speaker list: the index takes it from the project, and here a speaker
    is only ever looked up by 人物 entry name.
    """
    found: list[SpokenLine] = []
    scene: Optional[str] = None
    lines = screenplay.splitlines()
    index = 0
    while index < len(lines):
        stripped = lines[index].strip()
        if not stripped:
            index += 1
            continue
        if stripped.startswith("<!--"):
            end = index
            while end < len(lines) and "-->" not in lines[end]:
                end += 1
            if end >= len(lines):
                break
            index = end + 1
            continue
        if stripped.startswith("#"):
            heading = SCENE_HEADING_RE.match(stripped)
            scene = heading.group(1) if heading else None
            index += 1
            continue
        end = index
        while end + 1 < len(lines):
            following = lines[end + 1].strip()
            if not following or following.startswith(("#", "<!--")):
                break
            end += 1
        paragraph = [line.strip() for line in lines[index : end + 1]]
        index = end + 1
        if scene is None or any(
            SCREENPLAY_DIALOGUE_RE.fullmatch(line) or SCREENPLAY_BLOCK_START_RE.match(line)
            for line in paragraph[1:]
        ):
            continue
        text = "\n".join(paragraph)
        match = SCREENPLAY_VOICE_TAG_RE.fullmatch(text) or SCREENPLAY_DIALOGUE_RE.fullmatch(
            text
        )
        if match is not None and _han_key(match.group("text")):
            found.append(
                SpokenLine(scene, match.group("speaker"), _han_key(match.group("text")))
            )
    return found


def _quote_speakers(
    prompt: Optional[str], lines: list[SpokenLine], names: dict[str, list[str]]
) -> list[tuple[str, frozenset]]:
    """Each quote in the copyable body with the speakers it can belong to.

    Dialogue reaches the body quoted and verbatim (VID-25), so the screenplay
    says whose line it is. A short quote such as 「是。」 has to match a whole
    line, or any one-character quote would count as anybody's. When two
    speakers share the line, the clause that introduces the quote decides it
    only if it names exactly one of them; otherwise the quote stays ambiguous.
    """
    if prompt is None:
        return []
    joined = prompt.replace("\n", "")
    result: list[tuple[str, frozenset]] = []
    previous_end = 0
    for match in SPOKEN_SPAN_RE.finditer(joined):
        span = next((group for group in match.groups() if group), "")
        key = _han_key(span) if len(span) <= 200 else ""
        candidates = frozenset(
            line.speaker
            for line in lines
            if key and (key == line.key or (len(key) >= 4 and key in line.key))
        )
        if len(candidates) > 1:
            lead = joined[previous_end : match.start()]
            breaks = list(CLAUSE_BREAK_RE.finditer(lead))
            clause = lead[breaks[-1].end() :] if breaks else lead
            named = frozenset(
                speaker
                for speaker in candidates
                if any(name in clause for name in names.get(speaker, [speaker]))
            )
            if len(named) == 1:
                candidates = named
        if candidates:
            result.append((span, candidates))
        previous_end = match.end()
    return result


def _voice_records(visual: str, errors: list[str]) -> dict[str, str]:
    """Each 人物 entry's `- 声音参考：` value, keyed by the entry name."""
    headings = list(re.finditer(r"^## [^\n]*$", visual, re.MULTILINE))
    records: dict[str, str] = {}
    for index, heading in enumerate(headings):
        entry = VISUAL_SETTING_HEADING_RE.match(heading.group(0))
        if entry is None or entry.group(1) != "人物":
            continue
        end = headings[index + 1].start() if index + 1 < len(headings) else None
        declared = VOICE_RECORD_RE.findall(visual[heading.end() : end])
        if len(declared) > 1:
            errors.append(f"视觉设定.md: 人物「{entry.group(2).strip()}」的声音参考重复，只能登记一条")
        elif declared:
            records[entry.group(2).strip()] = _plain(declared[0])
    return records


class VoiceContext(NamedTuple):
    """What a MOTION's 参考音频 line is checked against."""

    characters: frozenset
    records: dict[str, str]
    dialogue: list[SpokenLine]
    # Every name a clause may use for a 人物 entry: its name and 画面代称.
    names: dict[str, list[str]]


def _audio_references(
    value: str,
    owner: str,
    project_root: Path,
    errors: list[str],
    *,
    image_slots: list[str],
    prompt: Optional[str],
    voices: VoiceContext,
    scenes: list[str],
) -> None:
    """Validate one MOTION's 参考音频 line against the character it names."""
    if _is_none(value):
        return
    # A line said in another scene is not evidence for this shot.
    in_scope = [line for line in voices.dialogue if not scenes or line.scene in scenes]
    quotes = _quote_speakers(prompt, in_scope, voices.names)
    plain = value.strip()
    matches = list(AUDIO_REF_RE.finditer(plain))
    cursor = 0
    for index, match in enumerate(matches):
        if plain[cursor : match.start()] != ("" if index == 0 else "；"):
            matches = []
            break
        cursor = match.end()
    if not matches or plain[cursor:] not in {"", "。"}:
        errors.append(f"{owner}: 参考音频必须写成 {AUDIO_SYNTAX}，多条用；连接")
        return
    slots = [match.group(1) for match in matches]
    orders = sorted(int(match.group(2)) for match in matches)
    if len(set(slots)) != len(slots) or set(slots) & set(image_slots):
        errors.append(f"{owner}: 参考音频槽位重复，或与输入参考图的槽位重名")
    if orders != list(range(1, len(orders) + 1)):
        errors.append(f"{owner}: 参考音频顺序必须唯一且从 1 连续编号，与图片分开数")
    speakers = [match.group(6).strip() for match in matches]
    for name in sorted({name for name in speakers if speakers.count(name) > 1}):
        errors.append(f"{owner}: 人物「{name}」绑定了不止一条参考音频")
    for match in matches:
        slot, _, locator, label, purpose, _, may, must = match.groups()
        name = match.group(6).strip()
        _check_project_file(locator, owner, project_root, errors)
        if purpose.strip() != AUDIO_PURPOSE:
            errors.append(
                f"{owner}: 参考音频用途只能是{AUDIO_PURPOSE}: {slot}（{purpose.strip()}）"
            )
        if not re.search(r"[\u4e00-\u9fff]", label):
            errors.append(f"{owner}: REF 缺少中文名称: {slot}")
        allowed = {item.strip() for item in re.split(r"[、,，]", may)}
        prohibited = {item.strip() for item in re.split(r"[、,，]", must)}
        if "" in allowed or "" in prohibited or allowed & prohibited:
            errors.append(f"{owner}: REF 控制与不得控制范围冲突: {slot}")
        if not {"台词", "语气", "情绪"} <= prohibited:
            errors.append(f"{owner}: 参考音频不得控制至少包含台词、语气、情绪: {slot}")
        if name not in voices.characters:
            errors.append(
                f"{owner}: 参考音频的角色不是《视觉设定.md》里的人物条目: {name}"
            )
            continue
        shared = [span for span, speakers in quotes if name in speakers]
        if any(speakers == {name} for _, speakers in quotes):
            pass
        elif shared:
            others = sorted(
                {s for _, speakers in quotes if name in speakers for s in speakers} - {name}
            )
            errors.append(
                f"{owner}: 引文「{_excerpt(shared[0], 24)}」在《剧本.md》里也是"
                f"{'、'.join(others)}的台词，看不出是不是人物「{name}」在说；"
                "在引文前的分句里点名说话人，或引一句只属于他的台词"
            )
        else:
            errors.append(
                f"{owner}: 人物「{name}」在本镜可复制提示词里没有说出《剧本.md》记在其名下的台词；"
                "不说话的人物不绑定参考音频"
            )
        record = voices.records.get(name)
        recorded = VOICE_RECORD_PATH_RE.match(record.strip()) if record else None
        if record is None:
            errors.append(
                f"{owner}: 《视觉设定.md》人物「{name}」没有声音参考行；"
                "先在该人物条目下写「- 声音参考：<项目相对路径>（…）」"
            )
        elif recorded is None:
            errors.append(
                f"{owner}: 《视觉设定.md》人物「{name}」的声音参考还没有音频路径: "
                f"{_excerpt(record, 24)}"
            )
        elif recorded.group(1) != locator:
            errors.append(
                f"{owner}: 参考音频 {slot} 的路径 {locator} 与《视觉设定.md》"
                f"人物「{name}」登记的声音参考 {recorded.group(1)} 不一致"
            )


def _plan_locator(
    locator: str,
    label: str,
    owner: str,
    slot: str,
    purpose: str,
    entries: Optional[EntryIndex],
    errors: list[str],
) -> None:
    """A planned picture still has to name an entry that exists today.

    The picture itself is the creator's to supply, but what it depicts is
    already decided by an `IMG-...` board or a planned shot frame. A SHOT
    shorthand resolves its unique start/end role; it never aliases composition.
    """
    if entries is None:
        return
    if locator.startswith("IMG-"):
        if locator not in entries.images:
            errors.append(f"{owner}: PLAN 指向不存在的 IMG 条目: {locator}")
        elif label != entries.images[locator]:
            errors.append(f"{owner}: PLAN 中文名称与 IMG 标题不一致: {slot}")
    elif locator.startswith("SHOT-"):
        shot_id, _separator, frame_id = locator.partition("#")
        if shot_id not in entries.shots:
            errors.append(f"{owner}: PLAN 指向不存在的 SHOT 条目: {locator}")
            return
        expected_role = {"起始帧": "start", "结束帧": "end"}.get(purpose)
        roles = entries.frames.get(shot_id, {})
        if expected_role is not None:
            own = re.sub(r"^(?:SHOT|MOTION)-", "SHOT-", owner)
            if own.startswith("SHOT-") and shot_id != own:
                errors.append(f"{owner}: {purpose} PLAN 必须指向本镜: {locator}")
            if frame_id:
                if roles.get(frame_id) != expected_role:
                    errors.append(
                        f"{owner}: {purpose} PLAN 的 {frame_id} 必须在画面证明计划中"
                        f"登记为 {expected_role}: {locator}"
                    )
            elif list(roles.values()).count(expected_role) != 1:
                errors.append(
                    f"{owner}: {purpose} PLAN 简写要求本镜画面证明计划有唯一 "
                    f"{expected_role}，不得用冻结关键帧顶替: {locator}"
                )
        elif frame_id and frame_id not in roles:
            errors.append(f"{owner}: PLAN 指向未在画面证明计划登记的 KF: {locator}")
    else:
        errors.append(
            f"{owner}: PLAN 定位符只能是 IMG-...、SHOT-... 或 SHOT-...#KF-...: {locator}"
        )


def _excerpt(value: str, limit: int = 60) -> str:
    """A short, single-line quote of an offending line for a diagnostic."""
    collapsed = re.sub(r"\s+", " ", value).strip()
    return collapsed if len(collapsed) <= limit else collapsed[: limit - 1] + "…"


def _unique(values: "Iterable[str]") -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result


def _normalized(value: str) -> str:
    """Fold case and collapse whitespace so a hard-wrapped prompt still matches.

    A copyable prompt is one rendered paragraph; the line breaks the repo's
    Markdown style puts in it are not part of the text a creator wrote.
    """
    return re.sub(r"\s+", " ", value).strip().casefold()


def _wordish(character: str) -> bool:
    return bool(character) and character.isascii() and (
        character.isalnum() or character == "-"
    )


def _carries_surface(prompt: str, surface: str) -> bool:
    """Is this lock surface actually asserted by this prompt?

    Plain containment is not enough. `chipped white enamel mug` must not be
    satisfied by `unchipped ... mug`, and `no pale blue sweater` in a negative
    tail asserts the opposite of the fact the lock exists to hold.
    """
    haystack = _normalized(prompt)
    needle = _normalized(surface)
    if not needle:
        return False
    start = haystack.find(needle)
    while start != -1:
        end = start + len(needle)
        before = haystack[start - 1] if start else ""
        after = haystack[end] if end < len(haystack) else ""
        # Only ASCII words have boundaries to glue across. Chinese is written
        # without spaces, so treating an adjacent CJK character as "glued" would
        # make a Chinese surface impossible to satisfy.
        glued = (
            (_wordish(needle[:1]) and _wordish(before))
            or (_wordish(needle[-1:]) and _wordish(after))
        )
        if not glued and NEGATION_RE.search(haystack[:start]) is None:
            return True
        start = haystack.find(needle, start + 1)
    return False


class VisualEntry(NamedTuple):
    """One `视觉设定.md` entry plus every name a prompt body may call it by."""

    category: str
    name: str
    designators: list[str]

    @property
    def key(self) -> tuple[str, str]:
        return (self.category, self.name)


def _visual_entries(document: str, errors: list[str]) -> list[VisualEntry]:
    """Parse the 人物/造型/地点/道具 entries of one `视觉设定.md`.

    A heading that *looks* like an entry but does not parse would silently drop
    out of the coverage check and then reappear as "视觉依据 names an entry that
    does not exist", so it is rejected here where the cause is visible.
    """
    for line in VISUAL_SETTING_LINE_RE.findall(document):
        if VISUAL_SETTING_HEADING_RE.match(line) is None:
            errors.append(
                "视觉设定.md: 条目标题必须写成 `## <人物|造型|地点|道具> · <名称>`: "
                + _excerpt(line)
            )
    for line in SCREEN_NAME_LINE_RE.findall(document):
        if SCREEN_NAME_RE.match(line) is None:
            errors.append(
                "视觉设定.md: 画面代称必须写成 `- 画面代称：<正文里的拼写>`: "
                + _excerpt(line)
            )
    headings = list(VISUAL_SETTING_HEADING_RE.finditer(document))
    entries: list[VisualEntry] = []
    seen: set[tuple[str, str]] = set()
    for index, heading in enumerate(headings):
        end = (
            headings[index + 1].start()
            if index + 1 < len(headings)
            else len(document)
        )
        category, name = heading.group(1), heading.group(2).strip()
        if not name:
            errors.append(f"视觉设定.md: {category}条目缺少名称")
            continue
        if (category, name) in seen:
            errors.append(f"视觉设定.md: 条目重复: {category}「{name}」")
            continue
        seen.add((category, name))
        declared = SCREEN_NAME_RE.findall(document[heading.end() : end])
        if not declared:
            # No declaration: the entry's own name is the designator, which is
            # what a prompt body written in the project's own language calls it.
            designators = [name]
        elif all(_is_none(_plain(raw)) for raw in declared):
            # `画面代称：无` is the deliberate opt-out for a name too common to
            # match reliably in prose (道具「手机」 against 手机店). It removes the
            # derived name too, otherwise the opt-out would do nothing.
            designators = []
        else:
            designators = []
            for raw in declared:
                value = _plain(raw)
                if _is_none(value):
                    continue
                for item in re.split(r"[、,，]", value):
                    item = item.strip()
                    if item and item not in designators:
                        designators.append(item)
        # Only a *declared* designator earns this diagnostic: the creator chose a
        # spelling the matcher cannot honour and deserves to know. A one-character
        # entry name they never declared is simply not name-matched, the same as
        # any entry in a project whose prompt body is written in another language.
        if declared:
            for designator in designators:
                if len(designator.strip()) < 2:
                    errors.append(
                        f"视觉设定.md: {category}「{name}」的画面代称「{designator}」"
                        "过短，无法在正文中可靠识别；请写成至少两个字符，或写「画面代称：无」"
                    )
        entries.append(VisualEntry(category, name, designators))
    return entries


def _named_entries(
    prompt: str,
    entries: list[VisualEntry],
    *,
    fold_case: bool = False,
    by_entry_name: bool = False,
) -> set[tuple[str, str]]:
    """Which declared entries does this frozen keyframe actually call by name?

    Longer designators win: a keyframe that shows 「角色A手机」 names the prop, and
    the 人物「角色A」 substring inside it is not a second, unrelated claim.
    """
    haystack = re.sub(r"\s+", " ", prompt).strip()
    if fold_case:
        haystack = haystack.casefold()
    owners: dict[str, list[VisualEntry]] = {}
    for entry in entries:
        # 来源 quotes 剧本.md, which is written in the project's own language and
        # calls people by their entry names — not by the 画面代称 a prompt body
        # uses. Matching a Chinese screenplay quote against an English designator
        # would never fire, so that text is matched by entry name instead. An
        # entry that opted out with `画面代称：无` opted out of being found by
        # name at all, and stays out of both.
        needles = (
            [entry.name] if by_entry_name and entry.designators else entry.designators
        )
        for designator in needles:
            needle = re.sub(r"\s+", " ", designator).strip()
            if fold_case:
                needle = needle.casefold()
            # A one-character designator matches far too much prose to be
            # evidence; _visual_entries already reports it.
            if len(needle) < 2:
                continue
            owners.setdefault(needle, []).append(entry)
    named: set[tuple[str, str]] = set()
    # Spans of every occurrence of a longer designator, whether or not it was
    # credited. 「戒指盒」 occupies its characters even when the sentence is
    # 「没有戒指」, so 道具「戒指」 must not be read out of it.
    taken: list[tuple[int, int]] = []
    for needle in sorted(owners, key=len, reverse=True):
        occurrences: list[tuple[int, int]] = []
        start = haystack.find(needle)
        while start != -1:
            end = start + len(needle)
            occurrences.append((start, end))
            start = haystack.find(needle, start + 1)
        for start, end in occurrences:
            before = haystack[start - 1] if start else ""
            after = haystack[end] if end < len(haystack) else ""
            glued = (
                (_wordish(needle[:1]) and _wordish(before))
                or (_wordish(needle[-1:]) and _wordish(after))
            )
            # Strictly longer, so two entries sharing one designator are both
            # credited instead of the first in document order winning.
            inside_longer = any(
                taken_start <= start
                and end <= taken_end
                and taken_end - taken_start > end - start
                for taken_start, taken_end in taken
            )
            if (
                not glued
                and not inside_longer
                and NEGATION_RE.search(haystack[:start]) is None
            ):
                named.update(entry.key for entry in owners[needle])
        taken.extend(occurrences)
    return named


class VisualBasis(NamedTuple):
    """One shot's parsed 视觉依据: what it declares, and what it excludes."""

    parsed: bool
    declared: set[tuple[str, str]]
    offscreen: set[tuple[str, str]]

    @property
    def accounted(self) -> set[tuple[str, str]]:
        return self.declared | self.offscreen


def _resolve_entry(
    key: tuple[str, str],
    known: set[tuple[str, str]],
    other_headings: dict[str, str],
    owner: str,
    errors: list[str],
) -> None:
    if key in known:
        return
    category, name = key
    section = other_headings.get(name)
    if section is not None:
        errors.append(
            f"{owner}: 《视觉设定.md》里有「{name}」，但它的分节词是「{section}」；"
            "条目标题必须写成 `## <人物|造型|地点|道具> · <名称>`"
        )
    else:
        errors.append(
            f"{owner}: 视觉依据指向不存在的《视觉设定.md》条目: {category}「{name}」"
        )


def _check_named_coverage(
    prompt: str,
    owner: str,
    where: str,
    basis: "VisualBasis",
    entries: list[VisualEntry],
    errors: list[str],
    *,
    by_entry_name: bool = False,
) -> None:
    """Every entry this text calls by name is either in frame or declared 画外."""
    # Matching is case-sensitive so an ordinary English word never impersonates a
    # character called May or Will. A body that writes the name in another case
    # would otherwise fall out of the check silently, so it is reported here.
    named = _named_entries(prompt, entries, by_entry_name=by_entry_name)
    folded = _named_entries(
        prompt, entries, fold_case=True, by_entry_name=by_entry_name
    )
    for category, name in sorted(folded - named):
        errors.append(
            f"{owner}: {where}里的名字与画面代称大小写不一致: {category}「{name}」；"
            "同一个名字全集只用一个拼写"
        )
    for category, name in sorted(named):
        if (category, name) not in basis.accounted:
            errors.append(
                f"{owner}: {where}写到{category}「{name}」，视觉依据没有覆盖；"
                "本镜确实看不见时在视觉依据末尾加「；画外："
                f"{category}「{name}」」，正文里这个名字不可靠时在《视觉设定.md》"
                "写「画面代称：无」"
            )


def _visual_basis(
    value: str,
    owner: str,
    entries: list[VisualEntry],
    other_headings: dict[str, str],
    errors: list[str],
) -> VisualBasis:
    """Parse one shot's 视觉依据 and resolve it against `视觉设定.md`."""
    empty = VisualBasis(True, set(), set())
    if _is_none(value):
        return empty
    plain = _plain(value)
    offscreen_raw = ""
    if OFFSCREEN_PREFIX in plain:
        plain, _, offscreen_raw = plain.partition(OFFSCREEN_PREFIX)
    prefixed = plain.startswith(VISUAL_BASIS_PREFIX)
    body = plain[len(VISUAL_BASIS_PREFIX) :] if prefixed else ""
    matches = list(VISUAL_BASIS_ENTRY_RE.finditer(body)) if prefixed else []
    cursor = 0
    separators_are_valid = True
    for index, match in enumerate(matches):
        # Repeating 《视觉设定.md》· before each entry says the same thing and
        # reads naturally; rejecting it would cost a round trip over nothing.
        separator = body[cursor : match.start()]
        allowed = (
            {""}
            if index == 0
            else {"；", "；" + VISUAL_BASIS_PREFIX}
        )
        if separator not in allowed:
            separators_are_valid = False
        cursor = match.end()
    if not prefixed or not matches or not separators_are_valid or body[cursor:]:
        errors.append(
            f"{owner}: 视觉依据必须使用完整语法："
            "《视觉设定.md》·<人物|造型|地点|道具>「<名称>」（控制：<范围>），多项用；连接"
        )
        # Coverage is not reported on top of a parse failure: every entry would
        # be listed as uncovered and bury the one error that matters.
        return VisualBasis(False, set(), set())
    known = {entry.key for entry in entries}
    declared: set[tuple[str, str]] = set()
    for match in matches:
        key = (match.group(1), match.group(2).strip())
        if key in declared:
            errors.append(f"{owner}: 视觉依据条目重复: {key[0]}「{key[1]}」")
        declared.add(key)
        _resolve_entry(key, known, other_headings, owner, errors)
        if not match.group(3).strip():
            errors.append(f"{owner}: 视觉依据缺少控制范围: {key[0]}「{key[1]}」")
    offscreen: set[tuple[str, str]] = set()
    if offscreen_raw:
        offscreen_raw = offscreen_raw.replace(VISUAL_BASIS_PREFIX, "")
        remainder = OFFSCREEN_ENTRY_RE.sub("", offscreen_raw).strip("；、 ")
        offscreen_matches = list(OFFSCREEN_ENTRY_RE.finditer(offscreen_raw))
        if not offscreen_matches or remainder:
            errors.append(
                f"{owner}: 画外清单必须写成 `；画外：<人物|造型|地点|道具>「<名称>」`，多项用；连接"
            )
            return VisualBasis(False, set(), set())
        for match in offscreen_matches:
            key = (match.group(1), match.group(2).strip())
            if key in declared:
                errors.append(
                    f"{owner}: {key[0]}「{key[1]}」同时写进视觉依据和画外清单"
                )
            offscreen.add(key)
            _resolve_entry(key, known, other_headings, owner, errors)
    return VisualBasis(True, declared, offscreen)


class ContinuityLock(NamedTuple):
    """One declared cross-shot lock: the exact surface and where it applies."""

    lock_id: str
    surface: str
    shots: list[str]
    images: list[str]


def _continuity_locks(document: str, errors: list[str]) -> list[ContinuityLock]:
    """Parse the declared continuity locks of one 视觉设定.md."""
    locks: list[ContinuityLock] = []
    seen: set[str] = set()
    for line in LOCK_LINE_RE.findall(document):
        match = LOCK_RE.match(line)
        if match is None:
            errors.append(
                "视觉设定.md: 连续性锁必须使用完整语法: " + _excerpt(line)
            )
            continue
        lock_id, label, scope, image_scope, surface = match.groups()
        if lock_id in seen:
            errors.append(f"{lock_id}: 连续性锁 ID 重复")
            continue
        seen.add(lock_id)
        if not re.search(r"[\u3400-\u9fff]", label):
            errors.append(f"{lock_id}: 连续性锁缺少中文名称")
        surface = _plain(surface)
        if not surface:
            errors.append(f"{lock_id}: 连续性锁缺少锁面")
            continue
        shots = _unique(
            item.strip() for item in re.split(r"[、,，]", _plain(scope)) if item.strip()
        )
        if not shots:
            errors.append(f"{lock_id}: 连续性锁缺少镜头范围")
            continue
        if "全集" in shots and len(shots) != 1:
            errors.append(f"{lock_id}: 连续性锁的镜头范围不能把全集与具体镜头混写")
            continue
        images: list[str] = []
        if image_scope is not None and not _is_none(image_scope):
            images = _unique(
                item.strip()
                for item in re.split(r"[、,，]", _plain(image_scope))
                if item.strip()
            )
            if any(not item.startswith("IMG-") for item in images):
                errors.append(f"{lock_id}: 连续性锁的图片提示词项必须使用 IMG-  ID")
                continue
        locks.append(ContinuityLock(lock_id, surface, shots, images))
    return locks


def _prompt_language(project_root: Path) -> str:
    """The language a copyable prompt body is written in.

    Mirrors the skills' own routing: the project's declared prompt language,
    falling back to `en` when there is no `short-drama.json` -- which is what
    the storyboard skill tells the keyframe author to assume.
    """
    configuration = project_root / "short-drama.json"
    if not configuration.is_file():
        return "en"
    try:
        project = json.loads(configuration.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return "en"
    if not isinstance(project, dict):
        return "en"
    authority = project.get("creator_authority")
    profile = (
        authority.get("production_profile") if isinstance(authority, dict) else None
    )
    if isinstance(profile, dict) and profile.get("status") == "accepted":
        choices = profile.get("choices")
        if isinstance(choices, dict):
            declared = choices.get("video_prompt_language")
            if isinstance(declared, str) and declared:
                return declared
    formats = project.get("format")
    declared = formats.get("prompt_language") if isinstance(formats, dict) else None
    return declared if isinstance(declared, str) and declared else "en"


def _check_language_designators(
    project_root: Path, *, entries: list[VisualEntry], errors: list[str]
) -> None:
    """Every character must be nameable in the prompt body's language.

    Without this, omitting `画面代称` is a silent opt-out of the coverage check
    for exactly the projects that need it -- the keyframe body defaults to `en`
    while `视觉设定.md` is Chinese, which is the shape issue #94 reported.

    This deliberately does not wait until some shot's 视觉依据 references the
    entry. Gating on that made the two halves of the contract land in different
    rounds: a document missing 视觉依据 got one error, and only after fixing it
    did the missing 画面代称 appear.
    """
    if _prompt_language(project_root).casefold().startswith("zh"):
        return
    for entry in entries:
        if entry.category != "人物":
            continue
        if entry.designators == [entry.name]:
            errors.append(
                f"视觉设定.md: 人物「{entry.name}」缺少画面代称；"
                "提示词正文不是中文时，写「画面代称：<正文里的拼写>」，"
                "正文从不点名时写「画面代称：无」"
            )


def _declared_seconds(value: str) -> Optional[float]:
    """The number of seconds a 时长 field declares, however it is spelled.

    `4s`, `4 秒` and `4秒` are the same duration. Returning None for anything
    else keeps an unparseable value out of the comparison instead of turning a
    formatting difference into a false duration conflict.
    """
    match = re.search(r"(\d+(?:\.\d+)?)", value or "")
    return float(match.group(1)) if match else None


def _check_continuity_locks(
    locks: list[ContinuityLock],
    *,
    shots: dict[str, str],
    motion_by_shot: dict[str, tuple[str, str, Optional[str]]],
    image_prompts: dict[str, Optional[str]],
    errors: list[str],
) -> None:
    """Require every declared lock surface to be present where it was scoped."""
    for lock in locks:
        lock_id = lock.lock_id
        surface = lock.surface
        targets = sorted(shots) if lock.shots == ["全集"] else lock.shots
        for shot_id in targets:
            if shot_id not in shots:
                errors.append(f"{lock_id}: 连续性锁指向不存在的镜头: {shot_id}")
                continue
            keyframe = _copyable_prompt(shots[shot_id], heading=r"冻结关键帧提示词")
            if keyframe is None:
                errors.append(f"{lock_id}: {shot_id} 缺少可读的冻结关键帧提示词")
            elif not _carries_surface(keyframe, surface):
                errors.append(f"{lock_id}: {shot_id} 冻结关键帧提示词缺少锁面")
            motion = motion_by_shot.get(shot_id)
            if motion is None:
                continue
            motion_id, _, copyable_prompt = motion
            if copyable_prompt is not None and not _carries_surface(
                copyable_prompt, surface
            ):
                errors.append(f"{lock_id}: {motion_id} 可复制提示词缺少锁面")
        for image_id in lock.images:
            if image_id not in image_prompts:
                errors.append(f"{lock_id}: 连续性锁指向不存在的 IMG 条目: {image_id}")
                continue
            image_prompt = image_prompts[image_id]
            if image_prompt is not None and not _carries_surface(image_prompt, surface):
                errors.append(f"{lock_id}: {image_id} 可复制提示词缺少锁面")


def _storyboard_head(storyboard: str) -> str:
    """The part of 分镜.md that belongs to the episode rather than to a shot."""
    match = re.search(r"^## SHOT-", storyboard, re.MULTILINE)
    return storyboard if match is None else storyboard[: match.start()]


CARD_RE = re.compile(r"\b(CARD-[A-Z0-9-]+)\b")
CONTINUITY_FIELD = "场记"
CONTINUITY_RELATIVE = "设定集/场记.md"


def _continuity_cards(project_root: Path) -> dict[str, str] | None:
    """Return every ``CARD-...`` heading in the continuity ledger, or None.

    ``设定集/场记.md`` is one ledger for the whole production, so it is shared
    across episodes.  Absent file means the project has not adopted it yet: that
    is reported by the caller as a gap, never silently accepted.
    """
    ledger = project_root / CONTINUITY_RELATIVE
    if not ledger.is_file():
        return None
    text = ledger.read_text(encoding="utf-8")
    cards: dict[str, str] = {}
    for match in re.finditer(r"^#{2,4}\s+(CARD-[A-Z0-9-]+)\b", text, re.MULTILINE):
        cards[match.group(1)] = match.group(0)
    return cards


def _check_continuity_cards(
    shots: dict[str, str],
    project_root: Path,
    errors: list[str],
) -> None:
    """One shot, one card: ids must resolve and map one-to-one.

    This is the cross-file id correspondence class of check: a mistyped card id,
    a card nobody references, or one card cited by two shots are all invisible
    while reading, and each one silently breaks the ledger's authority.
    """
    cards = _continuity_cards(project_root)
    if cards is None:
        if any(CONTINUITY_FIELD in body for body in shots.values()):
            errors.append(
                f"分镜.md 写了「{CONTINUITY_FIELD}：」，但项目里没有 {CONTINUITY_RELATIVE}"
            )
        return

    cited: dict[str, str] = {}
    for shot_id, body in shots.items():
        fields = _fields(body, owner=shot_id, errors=[])
        value = _plain(fields.get(CONTINUITY_FIELD, "")).strip()
        if not value:
            errors.append(f"{shot_id}: 缺少「{CONTINUITY_FIELD}：CARD-...」")
            continue
        found = CARD_RE.findall(value)
        if not found:
            errors.append(f"{shot_id}: 「{CONTINUITY_FIELD}」里没有可解析的 CARD- 编号")
            continue
        if len(found) > 1:
            errors.append(
                f"{shot_id}: 引用了多张调度卡 {', '.join(found)}；一镜只能对一卡"
            )
        card = found[0]
        if card not in cards:
            errors.append(f"{shot_id}: 场记账里没有 {card}")
        if card in cited:
            errors.append(
                f"{shot_id}: {card} 已被 {cited[card]} 引用；一卡只能对一镜"
            )
        else:
            cited[card] = shot_id

    for card in sorted(set(cards) - set(cited)):
        errors.append(f"{CONTINUITY_RELATIVE}: {card} 没有被任何镜头引用")


def _shot_sources(
    value: str, owner: str, scenes: "frozenset", errors: list[str]
) -> list:
    """Resolve one shot's 来源 against the scene ids that exist in 剧本.md."""
    plain = _plain(value)
    if not plain:
        errors.append(f"{owner}: 缺少来源字段")
        return []
    # 《镜头手艺》 asks for the scene id plus a short quote of the source line,
    # and a quote contains commas of its own. So the ids are read out of the
    # field rather than by cutting it into pieces on punctuation.
    if SCENE_ID_RE.match(plain) is None:
        errors.append(
            f"{owner}: 来源必须以《剧本.md》的场景 ID 开头: {_excerpt(plain, 24)}"
        )
        return []
    resolved = []
    for scene_id in _unique(SCENE_ID_RE.findall(plain)):
        if scene_id not in scenes:
            errors.append(f"{owner}: 来源场景不在《剧本.md》中: {scene_id}")
        else:
            resolved.append(scene_id)
    return resolved


def _unfilmed_scenes(
    storyboard: str, scenes: "frozenset", errors: list[str]
) -> dict:
    """Scenes 分镜.md declares it deliberately does not film, with reasons."""
    head = _storyboard_head(storyboard)
    declared: dict = {}
    # The line belongs to the episode, not to a shot. Placed inside a SHOT
    # section it would be read as that shot's field and quietly do nothing,
    # which looks exactly like forgetting to write it.
    if len(UNFILMED_LINE_RE.findall(storyboard)) != len(
        UNFILMED_LINE_RE.findall(head)
    ):
        errors.append("分镜.md: 未拍场次要写在第一个 SHOT 之前的正文开头")
    for value in UNFILMED_LINE_RE.findall(head):
        value = value.strip()
        entries = UNFILMED_ENTRY_RE.findall(value)
        remainder = UNFILMED_ENTRY_RE.sub("", value).strip("；;。 ")
        if not entries or remainder:
            errors.append(
                "分镜.md: 未拍场次必须写成 <场景 ID>（理由：……），多项用；分隔"
            )
            continue
        for scene_id, reason in entries:
            if not reason.strip():
                errors.append(f"分镜.md: 未拍场次缺少理由: {scene_id}")
            elif scene_id not in scenes:
                errors.append(f"分镜.md: 未拍场次不在《剧本.md》中: {scene_id}")
            else:
                declared[scene_id] = reason.strip()
    return declared


def _spoken_key(value: str) -> str:
    """Drop punctuation and spacing so quoting choices do not decide identity."""
    return re.sub(r"[^\u3400-\u9fff0-9A-Za-z]", "", value)


def _quoted_speech(prompt: str) -> list:
    # The body is one prompt; a quote that happens to wrap across lines is the
    # same quote. Chinese does not separate words with spaces, so rejoining the
    # lines reconstructs the run exactly.
    joined = prompt.replace("\n", "")
    runs: list = []
    for match in SPOKEN_SPAN_RE.finditer(joined):
        span = next((group for group in match.groups() if group), "")
        # An unpaired quotation mark can pair with one much later and swallow
        # the narration between them. That span is not a quotation, so it is
        # not evidence of an invented line either.
        if len(span) > 200:
            continue
        runs.extend(SPOKEN_RUN_RE.findall(span))
    return runs


def _check_spoken_lines(
    prompt: str, owner: str, sources: "tuple", errors: list[str]
) -> None:
    """Quoted Chinese in a copyable body has to come from an upstream document.

    The video stage already owes the screenplay verbatim dialogue. Checking it
    here is what stops a prompt from writing the line the shot wishes the
    character had said. 视觉设定.md and 分镜.md count as sources too: a location
    or prop entry carries the exact text on a sign, and a shot's own fields
    carry the on-screen text and sound this shot was designed around. What no
    upstream document contains is a line the prompt made up.
    """
    for run in _quoted_speech(prompt):
        key = _spoken_key(run)
        if key and not any(key in source for source in sources):
            errors.append(
                f"{owner}: 可复制提示词的引文在《剧本.md》《视觉设定.md》《分镜.md》里都找不到: "
                f"{_excerpt(run, 24)}"
            )


def _director_v1_enabled(episode: Path, project_root: Path) -> bool:
    """New projects opt in explicitly; old projects opt in by writing 导演.md.

    The checker is also installed as part of the standalone short-drama skill.
    Import the director checker from the sibling checkout when available, but
    keep the legacy five-document surface usable when that skill is absent.
    """
    try:
        manifest = json.loads((project_root / "short-drama.json").read_text(encoding="utf-8"))
        if manifest.get("format", {}).get("director_contract") == "director-v1":
            return True
    except (OSError, UnicodeError, json.JSONDecodeError, AttributeError):
        pass
    return (episode / "导演.md").is_file()


def _validate_director_v1(episode: Path) -> list[str]:
    checker = Path(__file__).resolve().parents[2] / "short-drama-direct/scripts/director_check.py"
    if not checker.is_file():
        return [
            "director-v1 已启用，但未安装 short-drama-direct；"
            "请安装该技能以校验《导演.md》、reads 与画面证明计划"
        ]
    spec = importlib.util.spec_from_file_location("short_drama_direct_check", checker)
    if spec is None or spec.loader is None:
        return [f"无法加载导演契约校验器: {checker}"]
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.validate_episode(episode, enabled=True)


def _check_composition_locks(
    shot_body: str, shot_id: str, basis: VisualBasis, errors: list[str]
) -> None:
    """Every person declared visible must have body/head/gaze ownership."""
    expected = sorted(
        name for category, name in basis.declared if category == "人物"
    )
    if not expected:
        return
    cameras = CAMERA_LOCK_LINE_RE.findall(shot_body)
    if len(cameras) != 1 or _is_none(cameras[0]):
        errors.append(
            f"{shot_id}: 含人物镜头必须有唯一非空的机位锁；先确定视线对象，再写相机侧/距离/朝向"
        )
    declarations: dict[str, list[str]] = {}
    for match in PERSON_COMPOSITION_LINE_RE.finditer(shot_body):
        declarations.setdefault(match.group(1).strip(), []).append(match.group(2))
    for name in expected:
        rows = declarations.get(name, [])
        if len(rows) != 1:
            errors.append(
                f"{shot_id}: 可见人物「{name}」必须有唯一人物构图（身体/头部/视线目标）"
            )
            continue
        fields: dict[str, str] = {}
        for part in rows[0].split("｜"):
            if "：" not in part:
                errors.append(f"{shot_id}: 人物「{name}」构图字段缺少全角冒号")
                continue
            key, value = part.split("：", 1)
            fields[key.strip()] = value.strip()
        for key in ("身体", "头部", "视线目标"):
            if not fields.get(key):
                errors.append(f"{shot_id}: 人物「{name}」缺少{key}")
        target = fields.get("视线目标", "")
        if NEGATIVE_GAZE_TARGET_RE.search(target):
            errors.append(
                f"{shot_id}: 人物「{name}」视线目标只有否定/排除；必须写实际看向的唯一对象"
            )
        if "镜头" in target and "有意直视：" not in target:
            errors.append(
                f"{shot_id}: 人物「{name}」直视镜头必须写明（有意直视：<叙事理由>）"
            )
    for name in sorted(set(declarations) - set(expected)):
        errors.append(
            f"{shot_id}: 人物构图为「{name}」，但该人物未在视觉依据中声明为可见"
        )


def warn_asset_acceptance_scope(visual: str) -> list[str]:
    """Warn when an asset acceptance entry has no explicit scope dimensions.

    A bare '已认可' or 'creator_ack' with no dimension list means downstream
    consumers cannot tell whether geometry, lighting, materials, or spatial
    layout are individually accepted — any of them may silently be assumed.
    Each acceptance line must carry a '认可项:' clause listing what was
    actually reviewed and what still needs evidence.
    """
    warnings: list[str] = []
    for line in visual.splitlines():
        stripped = line.strip()
        # Match acceptance markers in bullet or field style
        if not re.search(r"已认可|creator_ack|已验收|accepted", stripped, re.IGNORECASE):
            continue
        # If the line already has an explicit scope marker it is fine
        if re.search(r"认可项[：:]|scope[：:]|维度[：:]|只认可|仅认可|仅.*认可", stripped, re.IGNORECASE):
            continue
        # Strip markdown list prefix for display
        display = re.sub(r"^[-*+]\s*", "", stripped)[:100]
        warnings.append(
            f"资产认可缺少维度声明：「{display}」— 请在同行或下一行用「认可项: 光色、材质…/ 待补证: 停车朝向…」标明认可范围，"
            "避免下游误当全维度通过。"
        )
    return warnings


def warn_scene_record_placeholders(episode: Path) -> list[str]:
    """Warn when 场记.md contains unfilled placeholder continuity entries.

    Empty CONT-* values mean the storyboard and video-prompts will inherit
    unknown anchor values; the warning names each empty entry so the agent
    can fill them before writing the storyboard.
    """
    warnings: list[str] = []
    record_path = episode / "设定集" / "场记.md"
    if not record_path.is_file():
        return warnings
    text = record_path.read_text(encoding="utf-8")
    # Match lines like: - CONT-V001 xxx：（空）or TBD or 待补 or 待定
    placeholder_re = re.compile(
        r"(CONT-[A-Z0-9-]+)[^\n]*[：:]\s*(待补|待定|TBD|？|\?|暂无|空|—|-{1,3})\s*$",
        re.IGNORECASE | re.MULTILINE,
    )
    for m in placeholder_re.finditer(text):
        warnings.append(
            f"场记占位符未填实：{m.group(1)} — 分镜.md 不得继承此空字段；"
            "请先填入具体连续性锚点，或在分镜中显式标注「连续性待补」。"
        )
    return warnings


def warn_intra_container_spatial_shift(video: str) -> list[str]:
    """Warn when adjacent [Shot N] blocks inside one MOTION container show a
    spatial position word that contradicts the previous shot without an explicit
    transition declaration.

    This is a text-level heuristic, not a video analysis. It catches the most
    common case: a left/right or near/far anchor that flips between shots inside
    the same generation without a stated reason.
    """
    warnings: list[str] = []
    # Regex to find MOTION sections
    motion_re = re.compile(r"^## (MOTION-[A-Z0-9-]+)\b[^\n]*\n(.*?)(?=^## |\Z)", re.M | re.S)
    shot_block_re = re.compile(r"\[Shot\s+\d+\](.*?)(?=\[Shot\s+\d+\]|\Z)", re.S)
    # Position indicators: horizontal (left/right/center) and depth (near/far)
    h_pos_re = re.compile(r"\b(left|right|画面左|画面右|左侧|右侧|左三分之|右三分之)\b", re.I)
    d_pos_re = re.compile(r"\b(foreground|background|前景|后景|远处|近处|前方|后方)\b", re.I)

    for m in motion_re.finditer(video):
        motion_id = m.group(1)
        body = m.group(2)
        shots = shot_block_re.findall(body)
        if len(shots) < 2:
            continue
        prev_h: set[str] = set()
        prev_d: set[str] = set()
        for i, shot_text in enumerate(shots):
            cur_h = {x.lower() for x in h_pos_re.findall(shot_text)}
            cur_d = {x.lower() for x in d_pos_re.findall(shot_text)}
            if i > 0 and prev_h and cur_h and not prev_h & cur_h:
                warnings.append(
                    f"{motion_id} [Shot {i}→{i+1}]: 水平位置词从 {sorted(prev_h)} 变为 {sorted(cur_h)}，"
                    "请确认是否有意切换或在 Shot 开头加「[Spatial: 同机位，人物位置未变]」声明。"
                )
            if i > 0 and prev_d and cur_d and not prev_d & cur_d:
                warnings.append(
                    f"{motion_id} [Shot {i}→{i+1}]: 景深位置词从 {sorted(prev_d)} 变为 {sorted(cur_d)}，"
                    "请确认是否有意切换。"
                )
            prev_h, prev_d = cur_h, cur_d
    return warnings


def warn_operated_props_missing(screenplay: str, visual: str) -> list[str]:
    """Warn when a prop that is handled in the screenplay has no asset entry.

    Operations: 递、接、拿、放、开、关、吃、穿、脱、破、湿、换手、打开、关上、掉、扔、举、拉、推、捡
    If a line of dialogue or action mentions such a verb immediately after or
    before a potential prop noun (any non-verb CJK word), and the visual
    design document has no matching prop or costume entry, raise a warning.
    """
    warnings: list[str] = []
    op_pattern = re.compile(
        r"(递|接过|拿起|拿出|放下|打开|关上|吃|穿上|脱下|破|湿|换手|掉落|扔|举起|拉开|推开|捡起)"
        r"([^，。\n]{1,10})"
    )
    # Collect prop entries from visual design
    prop_entry_re = re.compile(r"(?:道具|prop)[^\n]*[：:]\s*([^\n]+)", re.IGNORECASE)
    prop_names: set[str] = set()
    for m in prop_entry_re.finditer(visual):
        prop_names.add(m.group(1).strip()[:20])
    # Also collect from section headings that look like prop entries
    section_re = re.compile(r"^##\s+(?:IMG-[A-Z0-9-]+\s+·\s+)?(.+?)(?:\s*$)", re.MULTILINE)
    for m in section_re.finditer(visual):
        prop_names.add(m.group(1).strip()[:20])

    seen: set[str] = set()
    for m in op_pattern.finditer(screenplay):
        verb = m.group(1)
        obj = m.group(2).strip()
        if not obj or obj in seen:
            continue
        seen.add(obj)
        # 「递给他」「递给镜头」的宾语是接收者，不是道具。
        if verb == "递" and obj.startswith(("给", "到", "向")):
            continue
        # Check if any prop entry contains the object name
        matched = any(
            len(name) >= 2 and (obj in name or name in obj) for name in prop_names
        ) or any(
            len(name) >= 3 and name[-3:] in obj for name in prop_names
        )
        if not matched:
            warnings.append(
                f"剧本中「{verb}{obj}」涉及道具操作，但视觉设定中无对应道具板或条目 — "
                f"请在视觉设定里补充「{obj}」的道具板（IMG-...），"
                "或确认该道具可由场景卡地标承担并记录理由。"
            )
    return warnings


def episode_warnings(episode: Path, project_root: Optional[Path] = None) -> list[str]:
    """Collect all soft warnings for an episode directory.

    Unlike validate_episode (hard errors), these do not change the exit code.
    They surface incomplete but not yet wrong states: missing scope dimensions,
    unfilled continuity placeholders, operated props without asset entries.
    """
    episode = episode.resolve()
    warnings: list[str] = []
    missing = [name for name in REQUIRED_DOCUMENTS if not (episode / name).is_file()]
    if missing:
        return warnings  # hard errors will be reported by validate_episode
    visual = (episode / "视觉设定.md").read_text(encoding="utf-8")
    screenplay = (episode / "剧本.md").read_text(encoding="utf-8")
    storyboard = (episode / "分镜.md").read_text(encoding="utf-8")
    warnings.extend(warn_asset_acceptance_scope(visual))
    warnings.extend(warn_scene_record_placeholders(episode))
    warnings.extend(warn_operated_props_missing(screenplay, visual))
    warnings.extend(warn_intra_container_spatial_shift(
        (episode / "视频提示词.md").read_text(encoding="utf-8")
    ))
    warnings.extend(enum_warnings(storyboard))
    return warnings


def enum_warnings(storyboard: str) -> list[str]:
    """Warn-level 景别 conformance for a 分镜.md, per the review consensus.

    「景别/机位」 is creator prose — 「双人中近景，胸口高度」 is legal — so a
    value that names no known scale word is only a *warning*: the golden
    project's own accepted storyboard writes framings the word list does not
    carry, and blocking on the enum before the miss rate over real projects is
    known would trade a small catch for a certain false-positive rate. The
    count is the data that decides a later promotion to an error
    (kimi: 先 warn、后 hard-fail).

    Returns human-readable warning lines; callers count them (the dashboard
    and ``main`` print the count) so the false-positive rate is measurable.
    """

    warnings: list[str] = []
    for shot_id, body in _sections(storyboard, "SHOT").items():
        fields = _fields(body, owner=shot_id, errors=[])
        record = {"shot_id": shot_id, "framing": fields.get("景别/机位", "")}
        warnings.extend(
            finding["message"]
            for finding in _enums.check_enums([record])
        )
    return warnings


def validate_episode(episode: Path, project_root: Optional[Path] = None) -> list[str]:
    """Return all deterministic contract errors for ``episode``."""
    episode = episode.resolve()
    project_root = (project_root or episode.parent.parent).resolve()
    errors: list[str] = []
    missing = [name for name in REQUIRED_DOCUMENTS if not (episode / name).is_file()]
    if missing:
        return [f"缺少创作文档: {', '.join(missing)}"]

    images = (episode / "图片提示词.md").read_text(encoding="utf-8")
    storyboard = (episode / "分镜.md").read_text(encoding="utf-8")
    video = (episode / "视频提示词.md").read_text(encoding="utf-8")
    visual = (episode / "视觉设定.md").read_text(encoding="utf-8")
    screenplay = (episode / "剧本.md").read_text(encoding="utf-8")
    scene_headings = SCENE_HEADING_RE.findall(screenplay)
    scenes = frozenset(scene_headings)
    if not scenes:
        errors.append(
            "剧本.md: 没有可解析的场景标题；场景标题写成 ## <场景 ID> 内|外 · 地点 · 时间"
        )
    if len(scene_headings) != len(scenes):
        errors.append("剧本.md: 场景 ID 重复")
    spoken_sources = (
        _spoken_key(screenplay),
        _spoken_key(visual),
        _spoken_key(storyboard),
    )
    unfilmed = _unfilmed_scenes(storyboard, scenes, errors)
    claimed_scenes: set = set()
    locks = _continuity_locks(visual, errors)
    visual_entries = _visual_entries(visual, errors)
    voices = VoiceContext(
        characters=frozenset(
            entry.name for entry in visual_entries if entry.category == "人物"
        ),
        records=_voice_records(visual, errors),
        dialogue=_screenplay_dialogue(screenplay),
        names={
            entry.name: _unique([entry.name, *entry.designators])
            for entry in visual_entries
            if entry.category == "人物"
        },
    )
    other_headings = {
        match.group(2).strip(): match.group(1).strip()
        for match in OTHER_SETTING_HEADING_RE.finditer(visual)
        if match.group(1).strip() not in VISUAL_CATEGORIES
    }
    shots = _sections(storyboard, "SHOT")
    image_pairs = re.findall(r"^## (IMG-[A-Z0-9-]+) · (.+)$", images, re.MULTILINE)
    image_headings = dict(image_pairs)
    # A planned picture names the board or keyframe that already decides what it
    # depicts, so both indexes have to exist before any declaration is read.
    entries = EntryIndex(
        images=image_headings,
        shots=frozenset(shots),
        frames=_planned_frame_roles(shots),
    )
    all_image_headings = re.findall(r"^## (IMG-[A-Z0-9-]+)\b", images, re.MULTILINE)
    if len(image_pairs) != len(all_image_headings):
        errors.append("图片提示词.md: IMG 标题必须包含中文名称")
    if len(image_pairs) != len(image_headings):
        errors.append("图片提示词.md: IMG 标题 ID 重复")
    for image_id, label in image_pairs:
        if not re.search(r"[\u3400-\u9fff]", label):
            errors.append(f"{image_id}: IMG 标题缺少中文名称")
    image_matches = list(re.finditer(r"^## (IMG-[A-Z0-9-]+)\b", images, re.MULTILINE))
    image_prompts: dict[str, Optional[str]] = {}
    for index, match in enumerate(image_matches):
        body = images[
            match.start() : image_matches[index + 1].start()
            if index + 1 < len(image_matches)
            else None
        ]
        reference_value = _fields(body, owner=match.group(1), errors=errors).get(
            "参考", ""
        )
        if not reference_value:
            errors.append(f"{match.group(1)}: 缺少参考字段")
        elif _is_no_external_reference(reference_value):
            pass
        elif "REF-" in reference_value:
            _references(
                reference_value, match.group(1), project_root, errors, entries
            )
        else:
            errors.append(
                f"{match.group(1)}: 参考必须声明无外部参考或使用完整 REF 语法"
            )
        image_prompt = _copyable_prompt(body)
        image_prompts[match.group(1)] = image_prompt
        if image_prompt is None:
            errors.append(
                f"{match.group(1)}: 缺少唯一且非空的可复制提示词"
                + _copyable_prompt_cause(body)
            )

    motions = _sections(video, "MOTION")
    shot_ids = re.findall(r"^## (SHOT-[A-Z0-9-]+)\b", storyboard, re.MULTILINE)
    motion_ids = re.findall(r"^## (MOTION-[A-Z0-9-]+)\b", video, re.MULTILINE)
    if len(shot_ids) != len(set(shot_ids)):
        errors.append("分镜.md: SHOT 标题 ID 重复")
    if len(motion_ids) != len(set(motion_ids)):
        errors.append("视频提示词.md: MOTION 标题 ID 重复")
    named_shots = re.findall(
        r"^## (SHOT-[A-Z0-9-]+) · ([^\n]+)$", storyboard, re.MULTILINE
    )
    named_motions = re.findall(
        r"^## (MOTION-[A-Z0-9-]+) · ([^\n]+)$", video, re.MULTILINE
    )
    if len(named_shots) != len(shot_ids):
        errors.append("分镜.md: SHOT 标题必须包含中文名称")
    if len(named_motions) != len(motion_ids):
        errors.append("视频提示词.md: MOTION 标题必须包含中文名称")
    for shot_id, label in named_shots:
        if not re.search(r"[\u3400-\u9fff]", label):
            errors.append(f"{shot_id}: SHOT 标题缺少中文名称")
    for motion_id, label in named_motions:
        if not re.search(r"[\u3400-\u9fff]", label):
            errors.append(f"{motion_id}: MOTION 标题缺少中文名称")
    if not shots:
        errors.append("分镜.md: 没有 SHOT 条目")
    if not motions:
        errors.append("视频提示词.md: 没有 MOTION 条目")

    motion_by_shot: dict[str, tuple[str, str, Optional[str]]] = {}
    motion_duration: dict[str, str] = {}
    for motion_id, body in motions.items():
        fields = _fields(body, owner=motion_id, errors=errors)
        shot_id = _plain(fields.get("分镜", ""))
        motion_duration[shot_id] = _plain(fields.get("时长", ""))
        copyable_prompt = _copyable_prompt(body)
        if not shot_id:
            errors.append(f"{motion_id}: 缺少分镜字段")
        elif shot_id in motion_by_shot:
            errors.append(f"{motion_id}: 分镜 {shot_id} 被多个 MOTION 引用")
        else:
            motion_by_shot[shot_id] = (motion_id, body, copyable_prompt)
        if motion_id.removeprefix("MOTION-") != shot_id.removeprefix("SHOT-"):
            errors.append(f"{motion_id}: ID 必须与分镜 {shot_id} 一一对应")
        if copyable_prompt is None:
            errors.append(
                f"{motion_id}: 缺少唯一且非空的可复制提示词"
                + _copyable_prompt_cause(body)
            )

    if set(motion_by_shot) != set(shots):
        errors.append("分镜.md/视频提示词.md: SHOT 与 MOTION 未一一对应")

    for shot_id, shot_body in shots.items():
        fields = _fields(shot_body, owner=shot_id, errors=errors)
        source_value = fields.get("来源", "")
        shot_scenes = _shot_sources(source_value, shot_id, scenes, errors)
        claimed_scenes.update(shot_scenes)
        shot_seconds = _declared_seconds(_plain(fields.get("时长", "")))
        motion_seconds = _declared_seconds(motion_duration.get(shot_id, ""))
        if (
            shot_seconds is not None
            and motion_seconds is not None
            and shot_seconds != motion_seconds
        ):
            # 时长 is the value actually sent to the execution end and the term
            # VID-04/VID-13 arithmetic is built on. A downstream copy that drifts
            # from its accepted upstream is invisible in every other check.
            errors.append(
                f"{shot_id}: 分镜时长 {shot_seconds:g} 秒与视频提示词 "
                f"{motion_seconds:g} 秒不一致；视频提示词只能原样照抄已接受的镜头时长"
            )
        image_value = fields.get("图片提示词项", "")
        if not image_value:
            errors.append(f"{shot_id}: 缺少图片提示词项字段")
        image_refs = IMG_RE.findall(image_value)
        image_remainder = IMG_RE.sub("", image_value).strip("；。 ")
        if not _is_none(image_value) and (
            len(image_refs) != len(re.findall(r"\bIMG-[A-Z0-9-]+\b", image_value))
            or image_remainder
        ):
            errors.append(f"{shot_id}: 图片提示词项语法不完整")
        for image_id, label, _ in image_refs:
            if image_id not in image_headings:
                errors.append(f"{shot_id}: IMG 标题不存在: {image_id}")
            elif label != image_headings[image_id]:
                errors.append(f"{shot_id}: IMG 中文名称与标题不一致: {image_id}")

        shot_input = fields.get("输入参考图", "")
        if not shot_input:
            errors.append(f"{shot_id}: 缺少输入参考图字段")
        if "参考音频" in fields:
            errors.append(
                f"{shot_id}: 参考音频写在《视频提示词.md》的 MOTION 条目里，分镜不登记"
            )
        _references(shot_input, shot_id, project_root, errors, entries)

        basis_value = fields.get("视觉依据", "")
        if not basis_value:
            errors.append(f"{shot_id}: 缺少视觉依据字段")
            basis = VisualBasis(False, set(), set())
        else:
            basis = _visual_basis(
                basis_value, shot_id, visual_entries, other_headings, errors
            )
        if basis.parsed:
            _check_composition_locks(shot_body, shot_id, basis, errors)
        # 关键帧的七项镜头语言锚点是帧级取景的必填项；它不依赖视觉依据是否
        # 解析成功，所以独立于 basis.parsed 执行，避免人物镜以外的空镜漏检。
        _check_keyframe_camera_language(shot_body, shot_id, errors)
        # The keyframe is the only place the frame's contents exist as text, so a
        # shot without one would make the coverage check below vacuous.
        keyframe = _copyable_prompt(shot_body, heading=r"冻结关键帧提示词")
        if keyframe is None:
            errors.append(
                f"{shot_id}: 缺少唯一且非空的冻结关键帧提示词"
                + _copyable_prompt_cause(shot_body, heading=r"冻结关键帧提示词")
            )
        elif basis.parsed:
            _check_named_coverage(
                keyframe, shot_id, "冻结关键帧提示词", basis, visual_entries, errors
            )
        # start 只在需要端点正文时出现；出现后就必须是独立、非空、可复制的小节，
        # 不能拿冻结构图正文冒充0s，也不能让元数据污染实际提交正文。
        if re.search(r"^### 起始帧提示词\s*$", shot_body, re.MULTILINE):
            start = _copyable_prompt(shot_body, heading=r"起始帧提示词")
            if start is None:
                errors.append(
                    f"{shot_id}: 起始帧提示词不是唯一且非空的可复制正文"
                    + _copyable_prompt_cause(shot_body, heading=r"起始帧提示词")
                )
            elif basis.parsed:
                _check_named_coverage(
                    start, shot_id, "起始帧提示词", basis, visual_entries, errors
                )
        # The closing keyframe is optional — many shots end where they began —
        # but a heading that is present and malformed is a defect, not a shot
        # that quietly has no closing frame.
        if re.search(r"^### 收尾关键帧提示词\s*$", shot_body, re.MULTILINE):
            closing = _copyable_prompt(shot_body, heading=r"收尾关键帧提示词")
            if closing is None:
                errors.append(
                    f"{shot_id}: 收尾关键帧提示词不是唯一且非空的可复制正文"
                    + _copyable_prompt_cause(shot_body, heading=r"收尾关键帧提示词")
                )
            elif basis.parsed:
                _check_named_coverage(
                    closing, shot_id, "收尾关键帧提示词", basis, visual_entries, errors
                )
        if basis.parsed and source_value:
            # A shot's 来源 is its claim on the screenplay: whatever it quotes,
            # this shot is the one that films it. Quoting an action performed by
            # someone the frame never shows takes that action off everyone's
            # list — no other shot claims it, and nothing reports it missing, so
            # it simply never gets filmed. Same rule as the keyframe: in frame,
            # or declared 画外.
            _check_named_coverage(
                source_value,
                shot_id,
                "来源引文",
                basis,
                visual_entries,
                errors,
                by_entry_name=True,
            )

        motion = motion_by_shot.get(shot_id)
        if not motion:
            continue
        motion_id, motion_body, copyable_prompt = motion
        motion_fields = _fields(motion_body, owner=motion_id, errors=errors)
        if copyable_prompt is not None:
            _check_spoken_lines(
                copyable_prompt, motion_id, spoken_sources, errors
            )
        motion_input = motion_fields.get("输入参考图", "")
        _references(motion_input, motion_id, project_root, errors, entries)
        if _plain(motion_input) != _plain(shot_input):
            errors.append(f"{motion_id}: 输入参考图与 {shot_id} 不一致")
        if "参考音频" in motion_fields:
            _audio_references(
                motion_fields["参考音频"],
                motion_id,
                project_root,
                errors,
                image_slots=[
                    item[3][0]
                    for item in _slot_matches(
                        PENDING_REFERENCE_SUFFIX_RE.sub("", motion_input.strip())
                    )
                ],
                prompt=copyable_prompt,
                voices=voices,
                scenes=shot_scenes,
            )

        if _has_pending_references(shot_input):
            errors.append(f"{motion_id}: 仍有待补参考图，不能生成最终视频提示词")

        # A `PLAN-...` slot is not a file, but the prompt is still written for
        # image-conditioned generation: the creator attaches those pictures at
        # generation time. What decides 生成方式 is whether the shot sends
        # pictures at all, not whether this suite can read them.
        sends_pictures = not _is_none(shot_input)
        if sends_pictures:
            visible_persons = PERSON_COMPOSITION_LINE_RE.findall(shot_body)
            if visible_persons:
                slots = _slot_matches(motion_input)
                # 真·首帧接力只认真实文件：first_frame 与 reference_image 在 H3
                # 通道互斥，身份由上一段已验收真实末帧继承，不能再要求挂身份板。
                # PLAN 计划帧不是真实末帧（seam-transition §4.4.17），且起始帧
                # PLAN 被要求指向本镜，不能拿它豁免身份图。
                # 首帧接力：身份由上一段已验收的末帧继承，所以不需要身份板。
                # i2va/fl2va 下 identity 是禁止角色（provider 通道互斥），
                # 这两种 technique 的「首帧 + 可选尾帧」本身就是接力形态，
                # 不能再要求挂身份板，否则有可见人物的 i2va/fl2va 镜头永远修不好。
                purposes = {(item[3][4] or "").strip() for item in slots}
                is_first_frame_relay = (
                    len(slots) >= 1
                    and all(item[2] == "REF" for item in slots)
                    and "起始帧" in purposes
                    and purposes <= {"起始帧", "结束帧"}
                )
                has_identity_ref = is_first_frame_relay or "身份" in purposes
                if not has_identity_ref:
                    errors.append(
                        f"{motion_id}: 镜头有可见人物但无身份图参考，身份漂移概率高；"
                        "请绑定至少一张「身份」用途的 REF"
                    )
        expected_mode = "图生视频" if sends_pictures else "文生视频"
        if _plain(motion_fields.get("生成方式", "")) != expected_mode:
            errors.append(f"{motion_id}: 生成方式应为{expected_mode}")
        if not sends_pictures:
            if not _is_explicit_text_to_video(shot_input):
                errors.append(
                    f"{motion_id}: 无真实输入参考图时不能静默降级为文生视频；"
                    "请先绑定已有图片、列出待补图片，或记录创作者已明确选择文生视频"
                )
            anchor = _plain(motion_fields.get("静态视觉锚点", ""))
            if not anchor or anchor == "无":
                errors.append(f"{motion_id}: 文生视频缺少静态视觉锚点")
            if (
                copyable_prompt is not None
                and anchor
                and anchor != "无"
                and anchor not in copyable_prompt
            ):
                errors.append(f"{motion_id}: 可复制提示词没有包含静态视觉锚点")
            # In text-to-video the anchor carries the appearance the keyframe
            # would otherwise have carried, so it is the same claim about the
            # same frame and answers to the same visual basis. The rest of the
            # motion body is not checked: it may legitimately name an offscreen
            # speaker, which SHT-22 excludes.
            if anchor and anchor != "无" and basis.parsed:
                _check_named_coverage(
                    anchor, motion_id, "静态视觉锚点", basis, visual_entries, errors
                )

    for scene_id in scene_headings:
        if scene_id in claimed_scenes or scene_id in unfilmed:
            continue
        errors.append(
            f"分镜.md: 没有镜头承载场景 {scene_id}；"
            "拍它就写进某一镜的来源，不拍就写进未拍场次并给出理由"
        )
    for scene_id in sorted(set(unfilmed) & claimed_scenes):
        errors.append(f"分镜.md: 场景 {scene_id} 既被镜头承载又记为未拍")

    _check_language_designators(
        project_root, entries=visual_entries, errors=errors
    )
    _check_continuity_locks(
        locks,
        shots=shots,
        motion_by_shot=motion_by_shot,
        image_prompts=image_prompts,
        errors=errors,
    )
    _check_continuity_cards(shots, project_root, errors)
    if _director_v1_enabled(episode, project_root):
        errors.extend(_validate_director_v1(episode))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path, help="包含创作 Markdown 的剧集目录；director-v1 时为六份")
    parser.add_argument("--project-root", type=Path, help="用于解析 REF 项目相对路径")
    args = parser.parse_args()
    # 诊断与剧集路径都是中文。stdout 重定向时 Windows 用 ANSI 代码页，默认的
    # strict 处理器会在打印这一步抛错；stderr 早就是 backslashreplace，这里让
    # stdout 用同一个处理器：能编码就照常显示中文，不能编码才退成转义。
    reconfigure = getattr(sys.stdout, "reconfigure", None)
    if reconfigure is not None:
        reconfigure(errors="backslashreplace")
    errors = validate_episode(args.episode, args.project_root)
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    # Enum warnings never change the exit code (see enum_warnings): they are
    # the miss-rate data for a later promote-to-error decision, printed so a
    # creator sees them and CI can count them. The OK line stays first: the
    # dashboard and the tests read the verdict off stdout's first line.
    warnings: list[str] = []
    if (args.episode / "分镜.md").is_file():
        warnings = episode_warnings(args.episode, args.project_root)
    if warnings:
        print(f"OK: {args.episode}（{len(warnings)} 条枚举警告，不计入失败）")
    else:
        print(f"OK: {args.episode}")
    for warning in warnings:
        print(f"WARN: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
