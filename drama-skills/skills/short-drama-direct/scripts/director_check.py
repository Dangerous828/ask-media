#!/usr/bin/env python3
"""Validate the director-v1 Markdown contract without judging artistic quality.

The checker proves only source linkage, field presence, table references and
arithmetic. It cannot decide whether a scene is well directed or a viewer will
understand it. It never writes project files or calls a model.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import NamedTuple, Optional

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("director_check.py requires Python 3.9 or newer")

SCENE_ID = r"(?:[A-Za-z0-9]+-)+SC[0-9]+"
SCENE_RE = re.compile(
    r"^## (" + SCENE_ID + r")(?:\s+(?:内|外|内外)\b|\s+·\s*)([^\n]*)$",
    re.MULTILINE,
)
SHOT_RE = re.compile(r"^## (SHOT-[A-Z0-9-]+)(?:\s+·\s*[^\n]+)?\s*$", re.MULTILINE)
FIELD_RE = re.compile(r"^- ([^：\n]+)：(.+)$", re.MULTILINE)
SECONDS_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*s$", re.IGNORECASE)
TIME_RE = re.compile(r"^(\d+(?:\.\d+)?)\s*(?:s|秒)?\s*$", re.IGNORECASE)
WINDOW_RE = re.compile(
    r"^(\d+(?:\.\d+)?)\s*(?:s|秒)?\s*[–—-]\s*(\d+(?:\.\d+)?)\s*(?:s|秒)?$",
    re.IGNORECASE,
)
DIRECTOR_FIELDS = ("戏剧行动", "转折与承受", "观众知情", "观看方案", "空间与声音")
ROLES = {"composition", "start", "pose_proof", "end"}


class Row(NamedTuple):
    values: list[str]


def _sections(text: str, pattern: re.Pattern[str]) -> dict[str, str]:
    matches = list(pattern.finditer(text))
    result: dict[str, str] = {}
    for index, match in enumerate(matches):
        key = match.group(1)
        body = text[match.start():matches[index + 1].start() if index + 1 < len(matches) else None]
        if key in result:
            raise ValueError(f"标题 ID 重复: {key}")
        result[key] = body
    return result


def _fields(text: str) -> dict[str, str]:
    return {key.strip(): value.strip() for key, value in FIELD_RE.findall(text)}


def _seconds(value: str) -> Optional[float]:
    match = SECONDS_RE.fullmatch(value.strip().rstrip("。"))
    return float(match.group(1)) if match else None


def _time(value: str) -> Optional[float]:
    match = TIME_RE.fullmatch(value.strip())
    return float(match.group(1)) if match else None


def _window(value: str) -> Optional[tuple[float, float]]:
    match = WINDOW_RE.fullmatch(value.strip())
    return (float(match.group(1)), float(match.group(2))) if match else None


def _close(left: float, right: float) -> bool:
    return abs(left - right) < 0.0001


def _tables(text: str, heading: str) -> list[Row]:
    match = re.search(r"^### " + re.escape(heading) + r"\s*$", text, re.MULTILINE)
    if not match:
        return []
    body = text[match.end():]
    next_heading = re.search(r"^#{1,3} ", body, re.MULTILINE)
    if next_heading:
        body = body[:next_heading.start()]
    rows: list[Row] = []
    for line in body.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if not cells or all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells):
            continue
        if cells[0] in {"Read", "Frame", "Shot"}:
            continue
        rows.append(Row(cells))
    return rows


def _shot_ids(text: str) -> set[str]:
    return set(re.findall(r"\bSHOT-[A-Z0-9-]+\b", text))


def _unfilmed_scenes(text: str) -> set[str]:
    """Return deliberate omissions that carry a reason, in either owner file."""
    found: set[str] = set()
    for match in re.finditer(r"^[ \t]*[-*+][ \t]*未拍场次[：:](.*)$", text, re.MULTILINE):
        for scene_id, reason in re.findall(r"(" + SCENE_ID + r")（理由：([^）\n]+)）", match.group(1)):
            if reason.strip():
                found.add(scene_id)
    return found


NECESSARY_LINE = re.compile(r"叙事必需[：:](.+?)(?:[;；]\s*允许偏差|$)", re.MULTILINE)
DEVIATION_LINE = re.compile(r"允许偏差[：:](.+?)(?:$)", re.MULTILINE)

# Plan-2 schema: 叙事必需 entries may carry a scene-local ID (N1=<fact>),
# optionally followed by an entity-anchor suffix ``[实体:<id,id>]`` (opus:
# structured anchors). The ID turns "was this fact carried by a shot" from a
# text-matching guess into reference integrity -- the checker proves the
# reference graph, not the prose. ID entries are separated by 、、， or ； --
# ； is safe as a separator because NECESSARY_LINE already ends the 叙事必需
# body at 允许偏差, so a ； inside the body can only be an entry boundary.
NEC_ID_MARK = re.compile(r"(?:^|[、，,；;]\s*)(N[0-9]{1,2})\s*[=＝]\s*")
NEC_ANCHOR_SUFFIX = re.compile(r"\s*[\[［]实体[：:][^\]］]*[\]］]\s*$")
CARRIES_TOKEN = re.compile(r"N[0-9]{1,2}")

# Plan-3 schema: the 入场状态 / 离场状态与交接 cells may end with a state
# ledger suffix ``[在场:<ids>; 持有:<id=prop>; 知情:观众=<fact>]``. Only a
# bracket whose first segment starts with one of the three ledger keys is
# parsed as a ledger, so prose brackets such as ``[注意：交接]`` never enter
# the diff. The ledger is opt-in per cell: legacy rows produce no findings.
LEDGER_CELL = re.compile(r"[\[［]([^\[］\]]*)[\]］]\s*$")
LEDGER_KEY_VALUE = re.compile(r"^(在场|持有|知情)\s*[：:]\s*(.*)$")


def _parse_necessary(value: str) -> list[tuple[Optional[str], str]]:
    """Split 叙事必需 into ``(N-ID or None, fact)`` entries.

    Legacy prose (no ID) keeps the comma-separated dialect. ID entries are
    cut at every ``N<digits>=`` boundary, so a fact may contain commas and the
    entries may be separated by 、，或；. An entity-anchor suffix is accepted
    and stripped; anchoring the carriers against it is left to the second
    wave, which reads the asset ledger too.
    """
    match = NECESSARY_LINE.search(value)
    if not match:
        return []
    body = match.group(1).strip()
    if not body or body in {"无", "待补", "同上"}:
        return []
    marks = list(NEC_ID_MARK.finditer(body))
    if not marks:
        return [
            (None, item.strip())
            for item in re.split(r"[、，,]", body)
            if item.strip()
        ]
    items: list[tuple[Optional[str], str]] = []
    head = body[: marks[0].start()].rstrip("、，,；;。 \t")
    for piece in re.split(r"[、，,]", head):
        if piece.strip():
            items.append((None, piece.strip()))
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(body)
        fact = body[mark.end():end].rstrip("。、，,；; \t")
        fact = NEC_ANCHOR_SUFFIX.sub("", fact).strip()
        if fact:
            items.append((mark.group(1), fact))
    return items


def _declared_necessary(value: str) -> list[str]:
    """Split a 叙事必需 clause into its individual facts.

    ID entries contribute their fact text, so the necessary-vs-deviation
    contradiction check keeps working unchanged for both dialects.
    """
    return [fact for _, fact in _parse_necessary(value)]


def _declared_necessary_ids(value: str) -> tuple[dict[str, str], list[str]]:
    """Return ``({N1: fact}, duplicate ids)`` for the ID-declared entries.

    A dict cannot carry a duplicate, so a scene-local ID bound to two facts
    is reported instead of silently keeping one binding.
    """
    ids: dict[str, str] = {}
    duplicates: list[str] = []
    for nid, fact in _parse_necessary(value):
        if nid is None:
            continue
        if nid in ids:
            duplicates.append(nid)
        else:
            ids[nid] = fact
    return ids, duplicates


def _ledger(cell: str) -> tuple[Optional[dict[str, set[str]]], list[str]]:
    """Parse the state-ledger suffix off an 入场/离场 cell.

    Returns ``(ledger or None, parse errors)``. A bracket that does not start
    with a ledger key is ordinary prose and yields ``(None, [])`` -- the
    ledger is opt-in per cell, so legacy rows never produce findings.
    """
    match = LEDGER_CELL.search(cell)
    if not match:
        return None, []
    body = match.group(1).strip()
    if not LEDGER_KEY_VALUE.match(body):
        return None, []
    ledger: dict[str, set[str]] = {}
    errors: list[str] = []
    for part in re.split(r"[;；]", body):
        part = part.strip()
        if not part:
            errors.append(
                "状态账本含空片段；片段用「;」分隔，形如 [在场:甲,乙; 持有:甲=牌; 知情:观众=事实]"
            )
            continue
        pair = LEDGER_KEY_VALUE.match(part)
        if not pair:
            errors.append(f"状态账本键只能是在场、持有、知情，不接受片段「{part}」")
            continue
        key, raw = pair.group(1), pair.group(2).strip()
        if not raw:
            errors.append(f"状态账本的 {key} 为空")
            continue
        items = {
            item.strip().replace("＝", "=")
            for item in re.split(r"[、，,]", raw)
            if item.strip()
        }
        for item in sorted(items):
            if key == "持有" and "=" not in item:
                errors.append(f"状态账本持有项必须形如 <人物>=<道具>，不接受「{item}」")
            if key == "知情" and not item.startswith("观众="):
                errors.append(
                    f"状态账本知情项暂只支持 观众=<事实>，不接受「{item}」"
                )
        ledger[key] = items
    return ledger, errors


def _fmt(items: set[str]) -> str:
    """Render a ledger set for diagnostics; an empty set reads as ∅."""
    return "、".join(sorted(items)) or "∅"


def _carried_ids(cell: str, shot_id: str, errors: list[str]) -> set[str]:
    """Parse the 承载 cell into a set of N-IDs.

    ``无`` is legal (this shot carries nothing). Legacy 5-column rows never
    reach this function. An ID is accepted only with the single-shot dialect
    (、-separated or bare); anything else in the cell is a defect, because a
    half-parsed carrier list would silently drop a declared necessity.
    """
    body = cell.strip()
    if not body or body in {"无", "同上", "待补"}:
        return set()
    ids = {item.strip() for item in re.split(r"[、，,]", body) if item.strip()}
    for item in sorted(ids):
        if not re.fullmatch(r"N[0-9]{1,2}", item):
            errors.append(
                f"导演.md/{shot_id}: 承载列只接受 N-ID（如 N1、N2）或「无」，"
                f"不接受「{item}」"
            )
            ids.discard(item)
    return ids


def _ledger_diff(
    scene_id: str,
    prev_shot: str,
    exit_ledger: dict[str, set[str]],
    shot_id: str,
    entry_ledger: dict[str, set[str]],
    errors: list[str],
) -> None:
    """Diff one shot's entry ledger against the previous shot's exit ledger.

    在场延续 and 持有延续 demand equality -- continuity must be re-declared,
    a prop changing hands must say so in both cells, and「牌绝不换手」becomes
    diffable arithmetic. 知情延续 also demands equality at the cut: growth is
    a change inside a shot, so a set that grows across a cut without either
    cell admitting it is a knowledge event that happened nowhere.
    """
    for key in ("在场", "持有"):
        exit_set = exit_ledger.get(key, set())
        entry_set = entry_ledger.get(key, set())
        if exit_set == entry_set:
            continue
        errors.append(
            f"导演.md/{scene_id}: {key}延续断裂（{prev_shot} 离场 → {shot_id} 入场）："
            f"{prev_shot} 离场为 {_fmt(exit_set)}，{shot_id} 入场为 {_fmt(entry_set)}；"
            f"相邻镜的{key}集合必须一致，道具换手或人物离场必须同时写进两侧"
        )
    exit_known = exit_ledger.get("知情", set())
    entry_known = entry_ledger.get("知情", set())
    if exit_known == entry_known:
        return
    vanished = exit_known - entry_known
    grew = entry_known - exit_known
    if vanished:
        errors.append(
            f"导演.md/{scene_id}: 知情在切点消失（{prev_shot} 离场 → {shot_id} 入场）："
            f"消失项 {_fmt(vanished)}；观众不会忘，删除某项知情不是本字段支持的语法"
        )
    if grew:
        errors.append(
            f"导演.md/{scene_id}: 知情在切点凭空出现（{prev_shot} 离场 → {shot_id} 入场）："
            f"新增项 {_fmt(grew)}；增长必须发生在某一镜内（该镜入场侧写旧集合、离场侧写新集合），"
            "不得在切点上无声出现"
        )


def _check_knowledge_monotonic_in_shot(
    shot_id: str,
    entry_known: set[str],
    exit_known: set[str],
    errors: list[str],
) -> None:
    """知情单调：a shot may only add audience knowledge, never remove it."""
    if entry_known - exit_known:
        errors.append(
            f"导演.md/{shot_id}: 知情单调被破坏：入场知情 {_fmt(entry_known)} "
            f"包含离场未再声明的 {_fmt(entry_known - exit_known)}；观众不会忘，"
            "知情集合在镜内只允许增长"
        )


def _ledger_reveal_hints(ledger: dict[str, set[str]]) -> list[str]:
    """Facts a shot revealed, for the warn-tier 知情先行 reads cross-check."""
    hints: list[str] = []
    for item in sorted(ledger.get("知情", set())):
        fact = item[len("观众="):] if item.startswith("观众=") else item
        if len(fact) >= 2:
            hints.append(fact)
    return hints


def _declared_deviation(value: str) -> list[str]:
    """Split a 允许偏差 clause into its individual facts."""
    match = DEVIATION_LINE.search(value)
    if not match:
        return []
    body = match.group(1).strip().rstrip("。")
    if not body or body in {"无", "待补", "同上"}:
        return []
    return [item.strip() for item in re.split(r"[、，,]", body) if item.strip()]


def check_director(director: str, screenplay: str, storyboard: str) -> list[str]:
    """Return hard errors for the contract; warn-tier findings go to
    ``check_director.warnings`` (reset on every call).

    The knowledge-reveal cross-check reads creator prose on one side, so it
    cannot be error-tier: a legitimate rewording would fail it. It lives on
    the warnings channel -- callers print the count, the same way the enum
    layer does, and a later promotion to hard-fail is a one-line change once
    the miss rate over real projects is known.
    """
    errors: list[str] = []
    knowledge_warnings: list[str] = []
    check_director.warnings = knowledge_warnings
    try:
        scenes = _sections(screenplay, SCENE_RE)
        plans = _sections(director, SCENE_RE)
        shots = _sections(storyboard, SHOT_RE)
    except ValueError as error:
        return [str(error)]

    if not scenes:
        errors.append("剧本.md: 没有可解析的场景标题")
    if not plans:
        errors.append("导演.md: 没有场景导演条目")
    unfilmed = _unfilmed_scenes(director) | _unfilmed_scenes(storyboard)

    for scene_id in scenes:
        if scene_id not in plans and scene_id not in unfilmed:
            errors.append(f"导演.md: 缺少场景导演条目 {scene_id}")
        if scene_id in plans and scene_id in unfilmed:
            errors.append(f"导演.md: 场景 {scene_id} 既有导演计划又被记为未拍")
    for scene_id in plans:
        if scene_id not in scenes:
            errors.append(f"导演.md: 场景不在剧本中 {scene_id}")

    planned_shots: set[str] = set()
    # Warn-tier reveal hints per shot: {shot_id: [revealed facts]}, used by
    # the cross-document 知情先行 check further down.
    reveal_hints: dict[str, list[str]] = {}
    for scene_id, body in plans.items():
        scene_fields = _fields(body)
        for field in DIRECTOR_FIELDS:
            value = scene_fields.get(field, "")
            if not value or value in {"无", "待补", "同上"}:
                errors.append(f"导演.md/{scene_id}: 缺少{field}")
        rows = _tables(body, "镜头计划")
        if not rows:
            errors.append(f"导演.md/{scene_id}: 缺少镜头计划表")
        for fact in _declared_necessary(scene_fields.get("空间与声音", "")):
            # 机械可核对的那一半：同一条事实不能既被声明为「观众看不到就会
            # 误读」、又被列进「允许偏差」。这是 DIR-08 的直接矛盾，下游会拿到
            # 两个相反的授权。至于某一镜是否真的兑现了它，属于内容判断，
            # 本脚本不做（见文件头「cannot decide whether a scene is well
            # directed」）。
            deviation = _declared_deviation(scene_fields.get("空间与声音", ""))
            if fact in deviation:
                errors.append(
                    f"导演.md/{scene_id}: 「{fact}」同时被声明为叙事必需与允许偏差；"
                    "叙事必需必须由下游兑现，允许偏差偏了不判失败，二者不能重叠"
                )
        necessary_ids, duplicate_ids = _declared_necessary_ids(
            scene_fields.get("空间与声音", "")
        )
        carried: dict[str, list[str]] = {}
        prev_exit_ledger: Optional[dict[str, set[str]]] = None
        prev_shot: Optional[str] = None
        for row in rows:
            if len(row.values) not in (5, 6):
                errors.append(f"导演.md/{scene_id}: 镜头计划必须为5列或6列（第6列为承载）")
                continue
            shot_id = row.values[0]
            if not re.fullmatch(r"SHOT-[A-Z0-9-]+", shot_id):
                errors.append(f"导演.md/{scene_id}: 无效镜头 ID {shot_id}")
                continue
            if shot_id in planned_shots:
                errors.append(f"导演.md: 计划镜头重复 {shot_id}")
            planned_shots.add(shot_id)
            if scene_id not in row.values[1]:
                errors.append(f"导演.md/{shot_id}: 镜头计划未引用本场 {scene_id}")
            if any(not cell or cell in {"同上", "待补"} for cell in row.values[1:5]):
                errors.append(f"导演.md/{shot_id}: 镜头计划有空泛或未决字段")
            if len(row.values) == 5:
                # Legacy row. When the scene declares no N-ID at all this is
                # the ordinary legacy dialect and passes; when the scene
                # declared IDs, a row that skipped the 承载 column would let
                # the LLM dodge the carrier graph -- carry nothing by writing
                # 承载「无」, not by omitting the column.
                if necessary_ids:
                    errors.append(
                        f"导演.md/{scene_id}/{shot_id}: 本场叙事必需已声明 N-ID，"
                        "每行镜头计划必须带承载列（不承载写「无」）"
                    )
            else:
                carries_cell = row.values[5].strip()
                if not necessary_ids and CARRIES_TOKEN.search(carries_cell):
                    errors.append(
                        f"导演.md/{scene_id}: 本场叙事必需未声明任何 N-ID，"
                        "镜头计划不得出现承载列；先在叙事必需中用 N1=<事实> 声明"
                    )
                    carries_cell = ""
                for nid in _carried_ids(carries_cell, shot_id, errors):
                    if nid not in necessary_ids:
                        errors.append(
                            f"导演.md/{scene_id}/{shot_id}: 承载列引用了未声明的 N-ID {nid}；"
                            f"引用前先在本场叙事必需中声明 {nid}=<事实>"
                        )
                    else:
                        carried.setdefault(nid, []).append(shot_id)
            entry_ledger, entry_errors = _ledger(row.values[2])
            exit_ledger, exit_errors = _ledger(row.values[4])
            for message in entry_errors + exit_errors:
                errors.append(f"导演.md/{shot_id}: {message}")
            if entry_ledger is not None and exit_ledger is not None:
                if prev_exit_ledger is not None and prev_shot is not None:
                    _ledger_diff(
                        scene_id, prev_shot, prev_exit_ledger, shot_id, entry_ledger, errors
                    )
                _check_knowledge_monotonic_in_shot(
                    shot_id,
                    entry_ledger.get("知情", set()),
                    exit_ledger.get("知情", set()),
                    errors,
                )
                grew = exit_ledger.get("知情", set()) - entry_ledger.get("知情", set())
                if grew:
                    reveal_hints.setdefault(shot_id, []).extend(
                        _ledger_reveal_hints({"知情": grew})
                    )
            elif entry_ledger is not None or exit_ledger is not None:
                errors.append(
                    f"导演.md/{shot_id}: 状态账本必须成对声明（入场与离场两侧都写），"
                    "只写一侧无法做延续 diff"
                )
            if exit_ledger is not None:
                prev_exit_ledger, prev_shot = exit_ledger, shot_id
        if necessary_ids:
            for nid in sorted(necessary_ids):
                # (b) every declared necessity must be carried by at least
                # one planned shot. This is the structurally-eliminated class
                # kimi named: 「完全没承载」这个最致命的错误 no longer has a
                # schema shape at all.
                if nid not in carried:
                    errors.append(
                        f"导演.md/{scene_id}: 叙事必需 {nid}（{necessary_ids[nid]}）"
                        "没有任何镜头承载；在承载列声明至少一镜，或删除该必需项"
                    )
            for nid in sorted(set(duplicate_ids)):
                errors.append(
                    f"导演.md/{scene_id}: 叙事必需 ID {nid} 重复声明；"
                    "每个 N-ID 在场内只能绑定一个事实"
                )

    for shot_id, body in shots.items():
        fields = _fields(body)
        if shot_id not in planned_shots:
            errors.append(f"分镜.md/{shot_id}: 未出现在导演镜头计划中")
        for scene_id in re.findall(SCENE_ID, fields.get("来源", "")):
            if scene_id not in plans:
                errors.append(f"分镜.md/{shot_id}: 来源场景没有导演方案 {scene_id}")

        duration = _seconds(fields.get("时长", ""))
        if duration is None or duration <= 0:
            errors.append(f"分镜.md/{shot_id}: 缺少合法的镜长，无法核对 reads")
        reads = _tables(body, "观众 reads")
        if not reads:
            errors.append(f"分镜.md/{shot_id}: 缺少观众 reads 表")
        read_ids: set[str] = set()
        read_windows: dict[str, tuple[float, float]] = {}
        cursor = 0.0
        for index, row in enumerate(reads, 1):
            if len(row.values) != 5:
                errors.append(f"分镜.md/{shot_id}: reads 必须为5列")
                continue
            read_id, raw_window, meaning, attention, landing = row.values
            if not re.fullmatch(r"R[1-9][0-9]*", read_id):
                errors.append(f"分镜.md/{shot_id}: 无效 read ID {read_id}")
            elif read_id != f"R{index}":
                errors.append(f"分镜.md/{shot_id}: reads 必须按 R1、R2…顺序排列")
            if read_id in read_ids:
                errors.append(f"分镜.md/{shot_id}: read 重复 {read_id}")
            read_ids.add(read_id)
            window = _window(raw_window)
            if window is None:
                errors.append(f"分镜.md/{shot_id}/{read_id}: 时间窗格式应为 0.0–1.0s")
            else:
                start, end = window
                read_windows[read_id] = window
                if not _close(start, cursor):
                    errors.append(f"分镜.md/{shot_id}/{read_id}: reads 必须无缺口无重叠地接续")
                if end <= start:
                    errors.append(f"分镜.md/{shot_id}/{read_id}: 时间窗必须 end > start")
                cursor = end
            if not all((meaning, attention, landing)) or any(
                value in {"同上", "待补"} for value in (meaning, attention, landing)
            ):
                errors.append(f"分镜.md/{shot_id}/{read_id}: 必须写理解内容、注意引导与停留/承接")
        if reads and duration is not None and not _close(cursor, duration):
            errors.append(
                f"分镜.md/{shot_id}: reads 结束于 {cursor:g}s，镜长为 {duration:g}s；应完整覆盖本镜"
            )
        # 知情先行（warn 级）：本镜揭示的每一项观众知情，应当能在这部镜头自
        # 己的 reads 里找到对应表述。导演侧的揭示声明（账本离场 − 入场）是
        # 事实，reads 的「观众要理解什么」是承诺；两边对不上的那一条，就是
        # 「观众知情与分镜相反」这条注入错误留下的指纹。判据取弱形式（子串
        # 命中任一 read），因为 reads 一侧是创作散文，换措辞是合法的（kimi:
        # 召回取向，允许它粗），所以它进 WARN 通道而不是 errors。
        hints = reveal_hints.get(shot_id)
        if hints:
            reads_text = " ".join(
                row.values[2] for row in reads if len(row.values) == 5
            )
            for fact in hints:
                if fact not in reads_text:
                    knowledge_warnings.append(
                        f"分镜.md/{shot_id}: 知情先行未在 reads 中兑现（warn）：导演账本"
                        f"声明本镜向观众揭示「{fact}」，但本镜观众 reads 的「观众要理解什么」"
                        "列没有出现这一表述；核对导演知情声明与分镜 reads 是否讲的是同一件事"
                    )

        frames = _tables(body, "画面证明计划")
        if not frames:
            errors.append(f"分镜.md/{shot_id}: 缺少画面证明计划表")
        frame_ids: set[str] = set()
        frame_roles: list[str] = []
        for row in frames:
            if len(row.values) != 6:
                errors.append(f"分镜.md/{shot_id}: 画面证明计划必须为6列")
                continue
            frame_id, role, read_id, raw_time, proof, production = row.values
            if not re.fullmatch(r"KF-[A-Z0-9-]+", frame_id):
                errors.append(f"分镜.md/{shot_id}: 无效关键帧 ID {frame_id}")
            if frame_id in frame_ids:
                errors.append(f"分镜.md/{shot_id}: 关键帧 ID 重复 {frame_id}")
            frame_ids.add(frame_id)
            if role not in ROLES:
                errors.append(f"分镜.md/{shot_id}/{frame_id}: role 只能是 composition、start、pose_proof 或 end")
            else:
                frame_roles.append(role)
            if read_id not in read_ids:
                errors.append(f"分镜.md/{shot_id}/{frame_id}: 引用不存在的 read {read_id}")
            instant = _time(raw_time)
            if instant is None:
                errors.append(f"分镜.md/{shot_id}/{frame_id}: 时刻格式应为秒数，如 0.0s")
            else:
                if duration is not None and not (0 <= instant <= duration):
                    errors.append(f"分镜.md/{shot_id}/{frame_id}: 时刻超出本镜")
                # A frame proves the read it cites, at the instant it names. If the
                # instant lies outside that read's window the plan contradicts
                # itself: a `start` frame at 0.0s that claims R3 (3.4–5.4s) is a
                # later-state picture wearing the opening-frame label, and every
                # downstream consumer (first_frame binding, video "opening
                # composition" wording) inherits the lie.
                cited = read_windows.get(read_id)
                if cited is not None and not (
                    cited[0] - 1e-6 <= instant <= cited[1] + 1e-6
                ):
                    errors.append(
                        f"分镜.md/{shot_id}/{frame_id}: 时刻 {instant:g}s 不在它引用的 "
                        f"{read_id} 时间窗 {cited[0]:g}–{cited[1]:g}s 内；"
                        "帧的内容、role 与 read 要指同一刻（start 在 0s 就引用覆盖 0s 的 read，"
                        "后段状态的帧改成 composition 并写它真实的时刻）"
                    )
                if role == "start" and not _close(instant, 0):
                    errors.append(f"分镜.md/{shot_id}/{frame_id}: start 必须在 0s")
                if role == "end" and duration is not None and not _close(instant, duration):
                    errors.append(f"分镜.md/{shot_id}/{frame_id}: end 必须在镜末")
                if role == "pose_proof" and duration is not None and (instant <= 0 or instant >= duration):
                    errors.append(f"分镜.md/{shot_id}/{frame_id}: 关键姿势必须在镜内，不得冒充首/尾帧")
            if not proof or proof in {"同上", "待补"}:
                errors.append(f"分镜.md/{shot_id}/{frame_id}: 缺少本帧证明责任")
            if not production or production in {"同上", "待补"}:
                errors.append(f"分镜.md/{shot_id}/{frame_id}: 缺少生产/审查用途")

        if not frame_roles.count("start"):
            errors.append(f"分镜.md/{shot_id}: 画面证明计划缺少 start")
        elif frame_roles.count("start") > 1:
            errors.append(f"分镜.md/{shot_id}: 画面证明计划最多有一个 start")
        if frame_roles.count("end") > 1:
            errors.append(f"分镜.md/{shot_id}: 画面证明计划最多有一个 end")
        if frame_roles.count("composition") > 1:
            errors.append(f"分镜.md/{shot_id}: 画面证明计划最多有一个 composition")
        pose_ids = {
            row.values[0] for row in frames if len(row.values) == 6 and row.values[1] == "pose_proof"
        }
        pose_headings = set(re.findall(r"^#### (KF-[A-Z0-9-]+)\s*$", body, re.MULTILINE))
        if pose_headings != pose_ids:
            errors.append(f"分镜.md/{shot_id}: 关键姿势标题与 pose_proof 计划不一致")
        has_end_heading = bool(re.search(r"^### 收尾关键帧提示词\s*$", body, re.MULTILINE))
        if ("end" in frame_roles) != has_end_heading:
            errors.append(f"分镜.md/{shot_id}: end 计划与收尾关键帧提示词必须一一对应")
        start_headings = re.findall(r"^### 起始帧提示词\s*$", body, re.MULTILINE)
        if len(start_headings) > 1:
            errors.append(f"分镜.md/{shot_id}: 起始帧提示词只能有一个")
        if start_headings and "start" not in frame_roles:
            errors.append(f"分镜.md/{shot_id}: 起始帧提示词必须绑定画面证明计划中的 start")
        if "composition" in frame_roles and not re.search(
            r"^### 冻结关键帧提示词\s*$", body, re.MULTILINE
        ):
            errors.append(f"分镜.md/{shot_id}: composition 计划缺少冻结关键帧提示词")
        if "pose_proof" in frame_roles and not re.search(
            r"^### 关键姿势提示词\s*$", body, re.MULTILINE
        ):
            errors.append(f"分镜.md/{shot_id}: 计划了关键姿势但缺少关键姿势提示词")
        if "pose_proof" not in frame_roles and re.search(
            r"^### 关键姿势提示词\s*$", body, re.MULTILINE
        ):
            errors.append(f"分镜.md/{shot_id}: 关键姿势提示词未在画面证明计划中声明")
    return errors


def validate_episode(episode: Path, *, enabled: Optional[bool] = None) -> list[str]:
    """Validate an episode only when its director-v1 contract is enabled.

    A missing episode directory is a caller error, never a pass. Returning an
    empty list there would let `produce`, the dashboard and CI read "checked and
    clean" when nothing was read at all, so the path is rejected explicitly.
    """
    episode = Path(episode)
    # Every early return below means check_director never ran, so its warn
    # channel must not still hold the previous episode's findings.
    check_director.warnings = []
    if not episode.is_dir():
        hint = "（传入的是文件，本参数要求集目录，如 剧集/EP001）" if episode.is_file() else ""
        return [f"director-v1 集目录不存在: {episode}{hint}"]
    if enabled is None:
        enabled = (episode / "导演.md").is_file()
    if not enabled:
        return []
    for name in ("导演.md", "剧本.md", "分镜.md"):
        if not (episode / name).is_file():
            return [f"director-v1 缺少文件: {name}"]
    return check_director(
        (episode / "导演.md").read_text(encoding="utf-8"),
        (episode / "剧本.md").read_text(encoding="utf-8"),
        (episode / "分镜.md").read_text(encoding="utf-8"),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("episode", type=Path, help="集目录，例如 剧集/EP001")
    parser.add_argument("--legacy", action="store_true", help="explicitly skip the director-v1 check")
    args = parser.parse_args()
    errors = validate_episode(args.episode, enabled=False if args.legacy else None)
    for error in errors:
        print(f"ERROR: {error}")
    for warning in check_director.warnings:
        print(f"WARN: {warning}")
    if check_director.warnings:
        print(f"NOTE: {len(check_director.warnings)} warn-level finding(s); they do not fail the check")
    if errors:
        return 1
    if args.legacy:
        # A skip is not a pass: the word OK here once let `--legacy` read as
        # "checked and clean" about a check that never ran.
        print("NOT_EVALUATED: director-v1 check skipped (--legacy); no reads, keyframes or boundaries were verified")
        return 0
    if not (args.episode / "导演.md").is_file():
        print("NOT_EVALUATED: director-v1 not enabled for this episode; the director contract was not checked")
        return 0
    print("OK: director-v1 contract valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
