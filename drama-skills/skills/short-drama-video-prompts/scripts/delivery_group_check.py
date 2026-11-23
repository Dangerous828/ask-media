#!/usr/bin/env python3
"""Check delivery grouping and seam contracts in a video-prompt document.

This is the Markdown-side counterpart of container_check.py.  The existing
container checker only reconciles structured JSONL delivery containers.  A
creator-first project writes `剧集/<EP>/视频提示词.md`, where every MOTION was
historically allowed to become its own generation job even when several
adjacent MOTIONs belonged to one continuous scene.

This checker enforces three structural invariants:

1. A same-scene, time-continuous run of shot-only MOTIONs must be declared as a
   delivery group.  A run of two or more adjacent MOTIONs with no group
   declaration and no explicit split reason fails.
2. Every delivery group lists its members, member durations, container duration,
   contiguity/binding-chain/one-scene basis, container mode (多镜容器), and at
   least one seam reason.  Container mode lives in the group row, not in the
   creator document's closed `生成方式` field.
3. Every adjacent pair in a group has a seam contract: previous end state, next
   start state, connection kind (sight/sound/action/reaction), new information,
   and what would be lost without the cut.
4. A multishot group that explicitly declares same-scene continuity must carry
   both an identity reference and a geographic/composition anchor among its
   members' declared `用途`, as two different bindings. The declaration is
   opt-in: a group that says nothing, or a scene change / hard cut, is checked
   exactly as before.

Groups are opt-in only when the episode genuinely has one shot.  A multi-shot
episode without either a group table or an explicit per-MOTION split reason is
reported, because "one MOTION = one job" is not a neutral default.

The script reads documents and writes nothing.

Usage:
    python3 delivery_group_check.py <剧集/EP001> [--json]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("requires Python 3.9 or newer")

MOTION_RE = re.compile(r"^## (MOTION-[A-Z0-9-]+) · ([^\n]+)$", re.MULTILINE)
DURATION_RE = re.compile(r"^- 时长：\s*(?P<value>\d+(?:\.\d+)?)\s*[sS秒]?\s*$", re.MULTILINE)
SEAM_RE = re.compile(
    r"^\|\s*(?P<from>MOTION-[A-Z0-9-]+)\s*→\s*(?P<to>MOTION-[A-Z0-9-]+)\s*\|"
    r"\s*(?P<prev>[^|]*)\|\s*(?P<next>[^|]*)\|\s*(?P<kind>[^|]*)\|"
    r"\s*(?P<newinfo>[^|]*)\|\s*(?P<lost>[^|]*)\|",
    re.MULTILINE,
)
GROUP_RE = re.compile(
    r"^\|\s*(?P<group>G-[A-Z0-9-]+)\s*\|\s*(?P<members>[^|]+)\|"
    r"\s*(?P<duration>[^|]*)\|\s*(?P<basis>[^|]*)\|\s*(?P<mode>[^|]*)\|"
    r"\s*(?P<seam>[^|]*)\|",
    re.MULTILINE,
)
SPLIT_REASON_RE = re.compile(
    r"^- 拆分理由：\s*(?P<reason>\S.+)$", re.MULTILINE
)
GENERATION_MODE_RE = re.compile(r"^- 生成方式：\s*(?P<mode>[^\n]+)$", re.MULTILINE)
REFERENCE_RE = re.compile(r"(REF-[A-Z0-9-]+)")
REVIEW_SECTION_RE = re.compile(r"^## (?:接缝评审|Seam Review)\s*$", re.MULTILINE)
CONNECTIONS = ("视线", "声音", "动作", "反应")
EMPTY = {"", "—", "-", "待定", "TBD", "tbd", "无"}
REVIEW_STATUS = ("APPROVE", "REVISE", "UNVERIFIED")
REVIEW_REQUIRED = ("reviewer", "input_digest", "status", "independence")
# Opt-in same-scene declaration on a multishot group row.  A denied form
# (非同场连续 / 不是同场连续 / 换场后不再同场连续) must not turn the check on,
# hence both the immediate lookbehind and the wider denial pattern.
SAME_SCENE_RE = re.compile(r"同场连续")
SAME_SCENE_DENIAL_RE = re.compile(r"(?:不|非|无|未|没)[^，,。；;、|\s]{0,6}同场连续")
# 用途 values (closed set from the storyboard skill) that carry each duty.
IDENTITY_PURPOSES = ("身份", "造型状态")
SCENE_PURPOSES = ("地理", "构图")
REFERENCE_LINE_RE = re.compile(r"^- 输入参考图：\s*(?P<refs>.*)$", re.MULTILINE)
PURPOSE_RE = re.compile(r"用途：\s*([^；;）)]+)")


def _sections(text: str) -> dict[str, str]:
    matches = list(MOTION_RE.finditer(text))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        result[match.group(1)] = text[match.end():end]
    return result


def _ordering(text: str) -> list[str]:
    return [match.group(1) for match in MOTION_RE.finditer(text)]


def _duration(body: str) -> float | None:
    match = DURATION_RE.search(body)
    return float(match.group("value")) if match else None


def _group_section(text: str) -> str | None:
    match = re.search(r"^## 交付分组\s*$", text, re.MULTILINE)
    if not match:
        return None
    rest = text[match.end():]
    nxt = re.search(r"^## ", rest, re.MULTILINE)
    return rest[:nxt.start()] if nxt else rest


def _seam_section(text: str) -> str | None:
    match = re.search(r"^## (?:接缝契约|切点契约)\s*$", text, re.MULTILINE)
    if not match:
        return None
    rest = text[match.end():]
    nxt = re.search(r"^## ", rest, re.MULTILINE)
    return rest[:nxt.start()] if nxt else rest


def _review_section(text: str) -> str | None:
    match = REVIEW_SECTION_RE.search(text)
    if not match:
        return None
    rest = text[match.end():]
    nxt = re.search(r"^## ", rest, re.MULTILINE)
    return rest[:nxt.start()] if nxt else rest


def _generation_mode(body: str) -> str:
    match = GENERATION_MODE_RE.search(body)
    return match.group("mode").strip() if match else ""


def _reference_set(body: str) -> set[str]:
    match = re.search(r"^- 输入参考图：\s*(.*)$", body, re.MULTILINE)
    if not match:
        return set()
    return set(REFERENCE_RE.findall(match.group(1)))


def _is_single_shot_mode(mode: str) -> bool:
    """A multi-member group cannot declare a single-shot execution mode."""
    compact = mode.replace(" ", "")
    return "单镜" in compact or "single" in compact.lower()


def _declares_same_scene(basis: str) -> bool:
    """True only for a positive same-scene declaration.

    The declaration is opt-in.  A denied form (非同场连续 / 不是同场连续) or a
    group that simply omits the phrase switches the group-level reference-duty
    check off, leaving the historical behavior untouched.
    """
    if not SAME_SCENE_RE.search(basis):
        return False
    return not SAME_SCENE_DENIAL_RE.search(basis)


def _reference_duties(body: str) -> dict[str, set[str]]:
    """Map each declared reference to the `用途：...` duties it carries.

    Duties are read per reference, not per MOTION: the adapter requires the
    scene anchor and the identity reference to be two different bindings, so a
    single picture claiming both roles must stay visible as one reference here.
    """
    duties: dict[str, set[str]] = {}
    line = REFERENCE_LINE_RE.search(body)
    if not line:
        return duties
    for chunk in re.split(r"[；;\n]", line.group("refs")):
        reference = REFERENCE_RE.search(chunk)
        if not reference:
            continue
        bucket = duties.setdefault(reference.group(1), set())
        for match in PURPOSE_RE.finditer(chunk):
            for part in re.split(r"[、,，/|]", match.group(1)):
                token = part.strip()
                if token:
                    bucket.add(token)
    return duties


def _digest(paths: list[Path]) -> str:
    """Digest the reviewed inputs, excluding the review section itself.

    The review is stored in 视频提示词.md, so hashing the whole file would make
    the reviewer's digest impossible to satisfy: writing it changes the bytes it
    must cover.  Exclude the review section; everything the reviewer judges
    (motions, groups, seams, storyboard) stays in the digest.
    """
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.name.encode("utf-8"))
        digest.update(b"\0")
        try:
            content = path.read_bytes()
        except OSError:
            digest.update(b"<missing>")
            content = b""
        if path.name == "视频提示词.md":
            text = content.decode("utf-8", "replace")
            match = REVIEW_SECTION_RE.search(text)
            if match:
                rest = text[match.end():]
                nxt = re.search(r"^## ", rest, re.MULTILINE)
                if nxt:
                    text = text[:match.start()] + rest[nxt.start():]
                else:
                    text = text[:match.start()]
            content = text.encode("utf-8")
        digest.update(content)
        digest.update(b"\0")
    return digest.hexdigest()


def _parse_review(section: str) -> dict[str, str]:
    fields: dict[str, str] = {}
    for line in section.splitlines():
        match = re.match(r"^-\s*(?P<key>[A-Za-z_]+)：\s*(?P<value>.+)$", line.strip())
        if match:
            fields[match.group("key")] = match.group("value").strip()
    return fields


def check_review(episode: Path, inputs: list[Path], errors: list[str]) -> None:
    """A seam review is an independent subagent result, not a table of prose.

    The mechanical layer can only prove that the review exists, names a
    reviewer, binds the current input bytes and says APPROVE.  Whether the seam
    is genuinely continuous remains the reviewer's judgement; this check exists
    so a missing, stale or self-authored review cannot be presented as approval.
    """
    text = (episode / "视频提示词.md").read_text(encoding="utf-8")
    section = _review_section(text)
    if section is None:
        errors.append(
            "缺少「## 接缝评审」：必须由独立 subagent 评审接缝，"
            "不能只靠机械检查或作者自审"
        )
        return
    fields = _parse_review(section)
    for key in REVIEW_REQUIRED:
        if not fields.get(key) or fields[key] in EMPTY:
            errors.append(f"接缝评审缺少「{key}」")
    status = fields.get("status", "").upper()
    if status not in REVIEW_STATUS:
        errors.append(f"接缝评审 status 必须是 {'/'.join(REVIEW_STATUS)}（实得：{status or '空'}）")
    elif status != "APPROVE":
        errors.append(f"接缝评审未通过：{status}；未 APPROVE 不许进入视频生产")
    independence = fields.get("independence", "")
    if independence and not any(word in independence for word in ("独立", "isolated", "fresh")):
        errors.append("接缝评审必须由未参与写词/生产的独立 subagent 执行，independence 要写明")
    expected = _digest(inputs)
    actual = fields.get("input_digest", "")
    if actual != expected:
        errors.append(
            "接缝评审 input_digest 与当前文档字节不一致："
            "修改分镜或视频提示词后必须重新开独立 subagent 复评"
        )


def check_episode(episode: Path) -> tuple[list[str], list[str]]:
    """Return (errors, warnings) for one episode directory."""
    video = episode / "视频提示词.md"
    errors: list[str] = []
    warnings: list[str] = []
    if not video.is_file():
        return [f"缺少 {video}"], warnings
    text = video.read_text(encoding="utf-8")
    motions = _sections(text)
    order = _ordering(text)
    if not motions:
        return ["视频提示词.md: 没有 MOTION 条目"], warnings

    group_section = _group_section(text)
    seam_section = _seam_section(text)
    groups = list(GROUP_RE.finditer(group_section or ""))
    seams = [match.groupdict() for match in SEAM_RE.finditer(seam_section or "")]

    # Every explicit group must be internally consistent.
    grouped: set[str] = set()
    for match in groups:
        group = match.group("group")
        members = [item.strip() for item in re.split(r"[、,，\s]+", match.group("members")) if item.strip()]
        if not members:
            errors.append(f"{group}: 交付分组没有成员")
            continue
        unknown = [member for member in members if member not in motions]
        if unknown:
            errors.append(f"{group}: 成员未在文中定义: {', '.join(unknown)}")
        duplicate = [member for member in members if member in grouped]
        if duplicate:
            errors.append(f"{group}: 成员重复出现在其他分组: {', '.join(duplicate)}")
        grouped.update(members)
        if members[0] in order:
            start = order.index(members[0])
            expected = order[start:start + len(members)]
            if members != expected:
                errors.append(f"{group}: 成员顺序必须与正文 MOTION 顺序一致")
        total = sum(_duration(motions[member]) or 0 for member in members if member in motions)
        declared = match.group("duration")
        number = re.search(r"\d+(?:\.\d+)?", declared)
        if not number:
            errors.append(f"{group}: 容器时长读不出数字（实得：{declared.strip()}）")
        elif abs(float(number.group(0)) - total) > 1e-6:
            errors.append(
                f"{group}: 容器时长 {number.group(0)}s 不等于成员时长之和 {total:g}s"
            )
        for label in ("basis", "mode", "seam"):
            if match.group(label).strip() in EMPTY:
                errors.append(f"{group}: {label} 栏为空")
        if len(members) > 1:
            # `- 生成方式：` is a creator-document field with a closed
            # vocabulary (图生视频/文生视频).  Container granularity belongs to
            # the delivery-group row instead, so the two checks cannot
            # contradict each other.
            mode = match.group("mode").replace(" ", "")
            is_multishot = "多镜" in mode or "容器" in mode or "multi" in mode.lower()
            if not is_multishot:
                errors.append(
                    f"{group}: 容器模式是「{match.group('mode').strip() or '空'}」，"
                    "多成员分组必须在分组表声明「多镜容器」"
                )
            # Members may need different reference slots; the binding chain is
            # shared when each member's references are a subset of the group's
            # union.  Requiring identical sets would reject legitimate
            # references that only some members need (e.g. a state image).
            reference_sets = {member: _reference_set(motions.get(member, "")) for member in members}
            union = set().union(*reference_sets.values())
            if not union:
                errors.append(f"{group}: 组内没有任何参考图，「共享同一绑定链」不成立")
            for member, refs in reference_sets.items():
                if not refs:
                    errors.append(f"{group}: {member} 没有参考图，不能与有参考的成员共用同一绑定链")
            # Opt-in group-level duty check.  A multishot group that declares
            # same-scene continuity must carry both an identity duty and a
            # geographic/composition duty somewhere in the group, mirroring the
            # adapter's identity + scene-anchor requirement.  Undeclared
            # groups, scene changes and hard cuts are checked as before.
            if is_multishot and _declares_same_scene(match.group("basis")):
                duties: dict[str, set[str]] = {}
                for member in members:
                    for reference, carried in _reference_duties(motions.get(member, "")).items():
                        duties.setdefault(reference, set()).update(carried)
                identity_refs = {
                    reference for reference, carried in duties.items()
                    if carried & set(IDENTITY_PURPOSES)
                }
                scene_refs = {
                    reference for reference, carried in duties.items()
                    if carried & set(SCENE_PURPOSES)
                }
                if not identity_refs:
                    errors.append(
                        f"{group}: 声明同场连续，但组内没有任何参考图承担身份职责"
                        f"（用途需含 {'/'.join(IDENTITY_PURPOSES)}）"
                    )
                if not scene_refs:
                    errors.append(
                        f"{group}: 声明同场连续，但组内没有任何参考图承担地理/构图职责"
                        f"（用途需含 {'/'.join(SCENE_PURPOSES)}，并明确锚点）"
                    )
                if identity_refs and scene_refs and not any(
                    identity != scene for identity in identity_refs for scene in scene_refs
                ):
                    errors.append(
                        f"{group}: 声明同场连续，但身份与地理/构图职责落在同一张参考上；"
                        "adapter 要求场景锚之外另有一张身份参考，请拆成两条绑定"
                    )
        if len(members) == 1:
            errors.append(f"{group}: 单成员分组没有意义；一镜直接生成并写明拆分理由")
        for left, right in zip(members, members[1:]):
            if not any(s["from"] == left and s["to"] == right for s in seams):
                errors.append(f"{group}: 缺少 {left} → {right} 的接缝契约")
        grouped.update(members)

    # Adjacent same-scene MOTIONs that were not grouped need an explicit reason.
    ungrouped = [motion for motion in order if motion not in grouped]
    if len(order) > 1 and len(groups) == 0:
        for motion in ungrouped:
            body = motions[motion]
            reason = SPLIT_REASON_RE.search(body)
            if not reason:
                errors.append(
                    f"{motion}: 多镜项目必须进入交付分组；若确需单独生成，"
                    "必须在条目内写「- 拆分理由：…」并说明为什么不能与相邻镜同容器"
                )
            elif len(reason.group("reason").strip()) < 12:
                errors.append(
                    f"{motion}: 拆分理由太短，必须写明具体差异"
                    "（换场次/换地点/独立返修/超出时长上限）"
                )
            elif not any(word in reason.group("reason")
                         for word in ("换场次", "换地点", "场次", "地点", "返修", "时长", "上限")):
                errors.append(
                    f"{motion}: 拆分理由没有落到可核对的原因；"
                    "必须属于换场次、换地点、独立返修或超出模型时长上限"
                )

    # Seam rows: no empty cells, connection kind must be one of the four.
    for seam in seams:
        pair = f"{seam['from']} → {seam['to']}"
        for label in ("prev", "next", "kind", "newinfo", "lost"):
            if seam[label].strip() in EMPTY:
                errors.append(f"{pair}: 接缝契约「{label}」为空")
        if not any(word in seam["kind"] for word in CONNECTIONS):
            errors.append(
                f"{pair}: 接缝连接方式必须是 视线接/声音接/动作接/反应接 之一"
                f"（实得：{seam['kind'].strip()}）"
            )

    # Group members must collectively explain all adjacent pairs in the group.
    if groups and seam_section is None:
        errors.append("存在交付分组，但缺少「## 接缝契约」章节")
    if len(order) > 1 and not groups:
        warnings.append("只有一个 MOTION 以外的多镜项目却没有交付分组；请确认每镜确实独立生成")

    # Detect a table header that promises seams but has no data rows.
    if seam_section is not None and not seams:
        errors.append("「## 接缝契约」章节存在但没有数据行")

    # A seam is a judgement, not a table.  A multi-shot document must carry an
    # independent reviewer's binding result for the exact current bytes.
    if len(order) > 1:
        inputs = [video]
        storyboard = episode / "分镜.md"
        if storyboard.is_file():
            inputs.append(storyboard)
        check_review(episode, inputs, errors)

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path, help="包含视频提示词.md 的剧集目录")
    parser.add_argument("--json", action="store_true", help="输出 JSON")
    args = parser.parse_args()
    errors, warnings = check_episode(args.episode)
    if args.json:
        print(json.dumps({"ok": not errors, "errors": errors, "warnings": warnings},
                         ensure_ascii=False, indent=2))
    else:
        for error in errors:
            print(f"FAIL  {error}")
        for warning in warnings:
            print(f"WARN  {warning}")
        print("PASS  交付分组与接缝契约齐全" if not errors else
              f"\n共 {len(errors)} 个 FAIL：不许提交视频生产")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
