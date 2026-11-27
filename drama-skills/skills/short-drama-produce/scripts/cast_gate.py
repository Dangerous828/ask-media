"""Cast coverage gate: a multi-reference generation must carry identity plates.

A job that binds a scene plate, a composition frame and a prop, but forgets the
character cards, passes every check that only asks "is each attached image
approved?". This module answers the different question: "is at least one
identity plate attached, and — when the caller declares a cast — is each
on-screen character represented?"

Three tiers, in order:

1. **exempt** — the caller supplied ``cast_exempt`` with a reason. The reason is
   echoed in the result so it stays visible in the job preview; silent skipping
   is never allowed.
2. **weak (default, zero input)** — with two or more references, at least one
   must be recognisable as an identity plate. This catches the common failure
   ("I forgot the character cards entirely") without needing anybody to
   remember to declare anything.
3. **strong (opt-in)** — when ``cast`` is supplied *and* ``cast_required`` is
   true, every named character must be represented. Spellings come from
   ``cast_aliases`` (prepare derives them from 视觉设定.md's ``- 画面代称：``).

Design assets (character/scene/prop/storyboard cards) define the identity
plates; they are not shots and are exempt at the caller's discretion via
``cast_exempt``. Look-development first runs are likewise exempt.

Matching is deliberately lexical and conservative. It never decides *which*
image is the identity plate for a character; a wrong-but-present attachment is
a job for look acceptance and the agent's own viewing. A missing attachment is
unambiguous and fail-closed.

No filesystem access: the caller owns the project documents.

SYNC NOTE: keep this file in sync with short-drama-review/scripts/cast_gate.py;
any behavior change must be applied to both copies.
"""
from __future__ import annotations

import json
import re
import sys
from typing import Any, Iterable, Mapping, Sequence

SCHEMA = "cast-gate/1"
MINIMUM_PYTHON = (3, 9)

# 身份板在路径、中文名或控制范围里稳定出现的词。角色卡命名跨项目一直是这一族。
IDENTITY_MARKERS = (
    "角色卡", "角色板", "身份板", "身份图", "三视图", "设定图",
    "character-card", "character-sheet", "character sheet", "charactercard",
    "identity", "char_", "-sheet", "_sheet", "turnaround",
)
# reference_bindings 的「控制」字段里，声明这张图捐身份时的用词
IDENTITY_CONTROL = ("身份", "脸型", "五官", "identity", "face")

# 分镜.md 的逐人调度行：`- 人物构图：角色A｜身体：…｜头部：…｜视线目标：…`
CAST_LINE = re.compile(r"^-\s*人物构图[：:]\s*([^｜|：:\n]+)", re.MULTILINE)
# 视觉设定.md 的人物条目与其画面代称
CHARACTER_HEADING = re.compile(r"^##\s*人物\s*[·・]\s*(.+?)\s*$", re.MULTILINE)
ALIAS_LINE = re.compile(r"^-\s*画面代称[：:]\s*(.+?)\s*$", re.MULTILINE)

MIN_REFERENCES = 2


def _normalize(value: str) -> str:
    """Case-folded, whitespace-free form used for both Chinese and Latin names."""
    return re.sub(r"\s+", "", value).casefold()


def _fields(item: Any) -> tuple[str, str, str]:
    """(path, label, may_control) as plain text, from a path or a binding dict."""
    if isinstance(item, str):
        return item, "", ""
    if isinstance(item, Mapping):
        control = item.get("may_control") or item.get("控制") or ""
        if isinstance(control, (list, tuple, set)):
            control = " ".join(str(part) for part in control)
        return (str(item.get("path") or ""), str(item.get("label") or ""),
                str(control))
    return "", "", ""


def _identity_evidence(item: Any) -> str:
    path, label, control = _fields(item)
    return _normalize(" ".join((path, label, control)))


def _is_identity_plate(item: Any, cast_tokens: Iterable[str]) -> bool:
    text = _identity_evidence(item)
    if any(_normalize(marker) in text for marker in IDENTITY_MARKERS):
        return True
    if any(_normalize(marker) in text for marker in IDENTITY_CONTROL):
        return True
    return any(token in text for token in cast_tokens)


def _tokens(character: str, aliases: Mapping[str, Any] | None) -> list[str]:
    """All spellings that may identify this character in a path or label."""
    values: list[str] = [character]
    extra = (aliases or {}).get(character)
    if isinstance(extra, str):
        values.append(extra)
    elif isinstance(extra, (list, tuple, set)):
        values.extend(str(item) for item in extra)
    tokens = []
    for value in values:
        normalized = _normalize(value)
        if normalized and normalized not in tokens:
            tokens.append(normalized)
    return tokens


def shot_cast(document: str) -> list[str]:
    """Characters declared by 人物构图 lines, in document order."""
    found: list[str] = []
    for name in CAST_LINE.findall(document):
        name = name.strip()
        if name and name not in found:
            found.append(name)
    return found


def project_aliases(document: str) -> dict[str, list[str]]:
    """Visual-setting 人物 → 画面代称 map, for projects that keep that section."""
    result: dict[str, list[str]] = {}
    chunks = list(CHARACTER_HEADING.finditer(document))
    for index, match in enumerate(chunks):
        name = match.group(1).strip()
        end = chunks[index + 1].start() if index + 1 < len(chunks) else len(document)
        section = document[match.end():end]
        values = [_normalize(v) for v in ALIAS_LINE.findall(section)]
        values = [v for v in values if v and v != _normalize(name)]
        if name:
            result[name] = sorted(set(values))
    return result


def check(
    references: Sequence[Any],
    *,
    cast: Sequence[str] | None = None,
    cast_aliases: Mapping[str, Any] | None = None,
    cast_required: bool = False,
    cast_exempt: str | None = None,
) -> dict[str, Any]:
    """Return a cast-coverage verdict. Pure; no filesystem access."""
    base: dict[str, Any] = {"schema": SCHEMA, "cast": list(cast or []),
                            "missing": [], "matched": {}, "identity_plates": []}
    if cast_exempt:
        reason = cast_exempt.strip()
        if len(reason) < 8:
            return {**base, "status": "error",
                    "message": "cast_exempt 需要写清具体理由（≥8 个字符），不接受空豁免"}
        return {**base, "status": "exempt", "exempt_reason": reason,
                "message": "cast coverage exempted by explicit reason: " + reason}

    if len(references) < MIN_REFERENCES:
        return {**base, "status": "not_applicable",
                "message": f"fewer than {MIN_REFERENCES} references; the multi-reference "
                           "identity-plate rule does not apply (single first frame / text-only)"}

    # 首尾帧接力（i2va/fl2va）：身份由首帧那一格继承，而 shot-manifest 明确禁止
    # i2va/fl2va 挂 identity 角色——两处都要求会让这两种 technique 永远过不去。
    # 只认「全部参考都是首帧/结束帧」的形态，混了别的参考照常要求身份板。
    def _endpoint_role(item: Any) -> str:
        if not isinstance(item, Mapping):
            return ""
        purpose = str(item.get("purpose") or item.get("用途") or "").strip()
        if purpose:
            return purpose
        return str(item.get("role") or "").strip()

    endpoint_only = all(
        _endpoint_role(item) in {"起始帧", "结束帧", "first_frame", "last_frame"}
        for item in references
    ) and any(
        _endpoint_role(item) in {"起始帧", "first_frame"} for item in references
    )
    if endpoint_only:
        return {**base, "status": "not_applicable",
                "message": "first/last-frame relay: identity is inherited from the first "
                           "frame, so the multi-reference identity-plate rule does not apply"}

    all_tokens: list[str] = []
    for character in cast or []:
        all_tokens.extend(_tokens(character, cast_aliases))
    plates = [item for item in references
              if _is_identity_plate(item, all_tokens)]
    base["identity_plates"] = [(_fields(item)[0] or _fields(item)[1]) for item in plates]
    if not plates:
        attached = [(_fields(item)[0] or _fields(item)[1]) for item in references]
        return {**base, "status": "fail",
                "code": "cast_identity_plate_missing",
                "message": "多参考生成没有挂任何身份板/角色卡。已挂参考："
                           + "、".join(attached)
                           + "。改法：给本镜每个出场角色带上已验收的角色卡（或 scene/"
                             "composition 之外的 identity 席位）；确属无身份可辨的镜头，"
                             "在 parameters.cast_exempt 写明具体理由。"}

    if cast_required and cast:
        matched: dict[str, list[str]] = {}
        missing: list[str] = []
        haystacks = [(_identity_evidence(item),
                      _fields(item)[0] or _fields(item)[1]) for item in references]
        for character in cast:
            tokens = _tokens(character, cast_aliases)
            hits = [display for text, display in haystacks
                    if any(token in text for token in tokens)]
            if hits:
                matched[character] = hits
            else:
                missing.append(character)
        if missing:
            return {**base, "status": "fail", "matched": matched, "missing": missing,
                    "code": "cast_identity_reference_missing",
                    "message": "出场角色缺身份参考图：" + "、".join(missing)
                               + "；逐角色核对需在 parameters.cast_aliases 补齐画面代称/简称"}
        return {**base, "status": "pass", "matched": matched,
                "message": "identity plate present and every declared character "
                           "has an identity reference"}

    return {**base, "status": "pass",
            "message": "identity plate present; per-character check not requested "
                       "(set parameters.cast + cast_required to enable)"}


def main(argv: list[str] | None = None) -> int:
    import argparse
    from pathlib import Path
    parser = argparse.ArgumentParser(description="Check cast identity coverage")
    parser.add_argument("--references", nargs="*", default=[],
                        help="attached reference paths")
    parser.add_argument("--bindings", default="[]",
                        help="JSON array of {path,label,may_control} bindings")
    parser.add_argument("--cast", nargs="*", default=[],
                        help="characters appearing in this shot")
    parser.add_argument("--aliases", default="{}", help="JSON object of name -> aliases")
    parser.add_argument("--cast-required", action="store_true")
    parser.add_argument("--cast-exempt", default="", help="explicit reason for exemption")
    parser.add_argument("--shot-file", default="", help="分镜.md / shot table for cast")
    parser.add_argument("--visual-file", default="", help="视觉设定.md for 画面代称")
    args = parser.parse_args(argv)
    try:
        bindings = json.loads(args.bindings)
        if not isinstance(bindings, list):
            raise ValueError("bindings must be a JSON array")
        aliases = json.loads(args.aliases)
        if not isinstance(aliases, dict):
            raise ValueError("aliases must be a JSON object")
        shot_text = Path(args.shot_file).read_text(encoding="utf-8") if args.shot_file else ""
        visual_text = Path(args.visual_file).read_text(encoding="utf-8") if args.visual_file else ""
        cast = list(args.cast) or shot_cast(shot_text)
        merged = {**project_aliases(visual_text), **aliases}
        outcome = check(bindings or args.references, cast=cast, cast_aliases=merged,
                        cast_required=args.cast_required, cast_exempt=args.cast_exempt or None)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError) as exc:
        outcome = {"schema": SCHEMA, "status": "error", "missing": [], "matched": {},
                   "identity_plates": [], "message": str(exc)}
    print(json.dumps(outcome, ensure_ascii=False, sort_keys=True))
    return 0 if outcome["status"] in ("pass", "not_applicable", "exempt") else 2


if __name__ == "__main__":
    raise SystemExit(main())
