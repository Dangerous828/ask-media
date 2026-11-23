#!/usr/bin/env python3
"""Reconcile an episode's delivery containers against its shot set (`VID-15`).

Every container can be correct on its own while the episode is wrong: a shot
packed into two containers bills its seconds twice, and a shot packed into none
disappears although its dialogue, bindings, and keyframe prompts are already
done. Neither error is visible from inside a single container, so the check is
a set comparison at episode scope.

The script reads accepted creator files and writes nothing.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# Creators run these scripts on whatever interpreter their machine provides, so
# an unsupported version must say so instead of failing inside an import.
MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit(
        "short-drama needs Python {}.{} or newer; this interpreter is {}.{}".format(
            *MINIMUM_PYTHON, sys.version_info.major, sys.version_info.minor
        )
    )

SCHEMA_VERSION = "1.0.0"
# A .jsonl file opens with a header record declaring the upstream snapshots its
# references name. The header is a declaration, not one of the file's records.
SOURCES_RECORD_TYPE = "sources"
# H3 multi-shot container bodies mark each cut as `[Shot 2] At 00:03.000, ...`.
# The first shot carries no timestamp, so shot 1 has no mark by contract and
# shot k (k >= 2) must carry exactly the accumulated start time of the members
# before it. That value is a pure function of the member durations, so it is
# recomputed here rather than trusted from the body text.
CUT_MARK_RE = re.compile(
    r"\[Shot (?P<shot>[1-9][0-9]*)\] At (?P<time>\d{2}:\d{2}\.\d{3})"
)


class CheckError(ValueError):
    """The inputs cannot be checked at all, as opposed to failing a check."""


def h3_cut_time(seconds: float) -> str:
    """Render container-relative seconds as H3's ``00:03.500`` clock.

    Single source for both the recomputed expectation and any generator: a cut
    mark is a projection of the member durations, never an authored value.
    """
    total_ms = int(round(seconds * 1000))
    minutes, remainder = divmod(total_ms, 60_000)
    return "{:02d}:{:02d}.{:03d}".format(minutes, remainder // 1000, remainder % 1000)


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise CheckError(f"unreadable JSONL: {path}") from error
    for number, line in enumerate(text.splitlines(), start=1):
        if not line.strip():
            continue
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise CheckError(f"invalid JSONL at {path.name}:{number}") from error
        if not isinstance(record, dict):
            raise CheckError(f"JSONL needs one object per line: {path.name}:{number}")
        records.append(record)
    if records and records[0].get("record_type") == SOURCES_RECORD_TYPE:
        del records[0]
    return records


def _finding(code: str, message: str, **detail: Any) -> dict[str, Any]:
    return {"code": code, "message": message, **detail}


def _seconds(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    return float(value)


# The three conclusions `delivery-container.jsonl.md` requires a container to
# state about why its members belong together.
MEMBERSHIP_BASIS_KEYS = (
    "source_order_contiguous",
    "binding_chain_equal",
    "scene_boundary_not_crossed",
)


def _member_shot_id(member: Any) -> str | None:
    if not isinstance(member, dict):
        return None
    ref = member.get("shot_ref")
    if isinstance(ref, dict) and isinstance(ref.get("record_id"), str):
        return ref["record_id"]
    return None


def _member_motion_id(member: Any) -> str | None:
    if not isinstance(member, dict):
        return None
    ref = member.get("motion_ref")
    if isinstance(ref, dict) and isinstance(ref.get("record_id"), str):
        return ref["record_id"]
    return None


def _motion_body(specs: list[dict[str, Any]]) -> dict[str, str]:
    """Map each motion_id to the copyable prompt body its spec carries."""

    bodies: dict[str, str] = {}
    for spec in specs:
        motion_id = spec.get("motion_id")
        body = spec.get("generic_prompt")
        if isinstance(motion_id, str) and isinstance(body, str):
            bodies[motion_id] = body
    return bodies


def check_cut_marks(
    containers: list[dict[str, Any]],
    packed_members: dict[str, list[tuple[str, float]]],
    motion_bodies: dict[str, str],
) -> tuple[list[dict[str, Any]], int, list[str]]:
    """Recompute every `[Shot k] At ...` cut mark from the member durations.

    The cut time of shot k is the sum of the durations of members 1..k-1, so it
    is a projection, never an authored value. The recomputation runs both
    directions: a mark the body writes but the durations contradict is a
    finding, and a member whose body carries no mark at all is a finding too --
    a missing mark used to leave the cut to the model's guess, which is exactly
    the failure this reconciliation exists to make visible. Single-member
    containers need no marks (the dialect gives shot 1 no timestamp).

    Returns (findings, checked_container_count, containers_skipped_no_dialect).
    Bodies outside the H3 dialect (`[Shot ...]` never mentioned) claim no cut
    times at all; they are skipped and named, never counted as checked.
    """

    findings: list[dict[str, Any]] = []
    checked = 0
    skipped_no_dialect: list[str] = []
    for container in containers:
        container_id = container.get("container_id")
        if not isinstance(container_id, str):
            continue
        members = packed_members.get(container_id) or []
        # Nothing can be recomputed without every member duration; the missing
        # durations are already reported by VID15_MEMBER_SHOT_HAS_NO_DURATION.
        if not members:
            continue
        bodies = [
            motion_bodies.get(_member_motion_id(member) or "")
            for member in container.get("members") or []
            if isinstance(member, dict)
        ]
        # The per-member bodies are only meaningful for this reconciliation
        # when one container body carries the whole pack. H3 container bodies
        # are written once per container, so the check reads the body of the
        # first member that has one.
        body = next((b for b in bodies if b), None)
        if body is None:
            continue
        marks = {
            int(match.group("shot")): match.group("time")
            for match in CUT_MARK_RE.finditer(body)
        }
        # Cut marks are a claim of the H3 multi-shot dialect: its bodies address
        # shots as `[Shot k]` and timestamp the cuts. A prose body that never
        # mentions `[Shot` makes no such claim -- generic Chinese bodies have
        # no marks to check, and demanding them there would fail every project
        # that never opted into the dialect. Those bodies are counted as
        # skipped, never as passed.
        if not marks and "[Shot" not in body:
            skipped_no_dialect.append(container_id)
            continue
        checked += 1
        # Shot 1 carries no timestamp by contract; a mark on it is a defect.
        if 1 in marks:
            findings.append(
                _finding(
                    "VID13_SHOT1_CARRIES_A_TIMESTAMP",
                    "the dialect gives [Shot 1] no cut timestamp; remove the mark",
                    container_id=container_id,
                )
            )
        expected: dict[int, str] = {}
        cursor = 0.0
        for position, (_shot_id, seconds) in enumerate(members, start=1):
            if position >= 2:
                expected[position] = h3_cut_time(cursor)
            cursor += seconds
        if len(members) > 1:
            missing = sorted(set(expected) - set(marks))
            if missing:
                findings.append(
                    _finding(
                        "VID13_CUT_MARK_MISSING",
                        "a multi-shot container body must timestamp every cut; the "
                        "cut time is the accumulated duration of the members before it",
                        container_id=container_id,
                        missing_shots=missing,
                        expected_times={str(k): v for k, v in sorted(expected.items())},
                    )
                )
        extra = sorted(set(marks) - set(expected) - {1})
        if extra:
            findings.append(
                _finding(
                    "VID13_CUT_MARK_HAS_NO_MEMBER",
                    "the body timestamps a shot the container does not pack",
                    container_id=container_id,
                    shots=extra,
                )
            )
        for shot_number, expected_time in sorted(expected.items()):
            written = marks.get(shot_number)
            if written is not None and written != expected_time:
                findings.append(
                    _finding(
                        "VID13_CUT_MARK_IS_NOT_THE_ACCUMULATED_SUM",
                        "the cut mark disagrees with the accumulated member durations",
                        container_id=container_id,
                        shot=shot_number,
                        written=written,
                        computed=expected_time,
                    )
                )
    return findings, checked, skipped_no_dialect


def reconcile(
    containers: list[dict[str, Any]],
    shots: list[dict[str, Any]],
    motion_specs: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    # An empty containers file and an empty shots file both verified nothing,
    # yet both used to report `status: pass` over zero rows. A project that
    # genuinely ships no containers records them as loose shots against a real
    # shot file; a zero-row run is an unreadable episode, not a clean one.
    if not containers:
        raise CheckError("container file carries no container records")
    if not shots:
        raise CheckError("shot file carries no shot records")
    findings: list[dict[str, Any]] = []
    durations = {
        shot["shot_id"]: _seconds(shot.get("duration_seconds"))
        for shot in shots
        if isinstance(shot.get("shot_id"), str)
    }
    episode_shots = set(durations)

    owner_of: dict[str, str] = {}
    packed: set[str] = set()
    container_total = 0.0
    # Per container: the ordered (shot_id, duration) of members whose duration
    # is known, kept so the cut-mark reconciliation can recompute the expected
    # `[Shot k] At ...` clock from the same numbers the total is summed from.
    packed_members: dict[str, list[tuple[str, float]]] = {}
    for container in containers:
        container_id = container.get("container_id")
        if not isinstance(container_id, str):
            findings.append(
                _finding("VID15_CONTAINER_HAS_NO_ID", "a container record has no id")
            )
            continue
        members = container.get("members")
        if not isinstance(members, list) or not members:
            findings.append(
                _finding(
                    "VID15_CONTAINER_HAS_NO_MEMBERS",
                    "a container carries no members",
                    container_id=container_id,
                )
            )
            continue
        # Checkpoint 1: `order` unique, contiguous and ascending. A delivery
        # package is assembled in this order, so a repeated or skipped number is
        # an ambiguous cut list, not a cosmetic flaw.
        orders = [
            member.get("order") for member in members if isinstance(member, dict)
        ]
        if not all(
            isinstance(value, int) and not isinstance(value, bool) for value in orders
        ) or orders != list(range(1, len(members) + 1)):
            findings.append(
                _finding(
                    "VID15_MEMBER_ORDER_IS_NOT_A_SEQUENCE",
                    "members must carry order 1..n, ascending and without gaps",
                    container_id=container_id,
                    orders=orders,
                )
            )

        # Checkpoint 7: the three membership_basis conclusions. Each is a claim
        # about why these shots belong in one container; leaving one blank makes
        # the container's own justification unreadable.
        basis = container.get("membership_basis")
        if not isinstance(basis, dict):
            findings.append(
                _finding(
                    "VID15_MEMBERSHIP_BASIS_MISSING",
                    "a container must record why its members belong together",
                    container_id=container_id,
                )
            )
        else:
            blank = sorted(
                key
                for key in MEMBERSHIP_BASIS_KEYS
                if not str(basis.get(key) or "").strip()
            )
            if blank:
                findings.append(
                    _finding(
                        "VID15_MEMBERSHIP_BASIS_INCOMPLETE",
                        "every membership_basis conclusion must be stated",
                        container_id=container_id,
                        missing=blank,
                    )
                )

        member_total = 0.0
        for member in members:
            shot_id = _member_shot_id(member)
            if shot_id is None:
                findings.append(
                    _finding(
                        "VID15_MEMBER_HAS_NO_SHOT_REF",
                        "a member does not name the shot it packs",
                        container_id=container_id,
                    )
                )
                continue
            if shot_id not in episode_shots:
                findings.append(
                    _finding(
                        "VID15_MEMBER_IS_NOT_AN_EPISODE_SHOT",
                        "a container packs a shot that is not in this episode",
                        container_id=container_id,
                        shot_id=shot_id,
                    )
                )
                continue
            previous = owner_of.get(shot_id)
            if previous is not None:
                findings.append(
                    _finding(
                        "VID15_SHOT_PACKED_TWICE",
                        "a shot belongs to more than one container",
                        shot_id=shot_id,
                        container_ids=sorted({previous, container_id}),
                    )
                )
                continue
            owner_of[shot_id] = container_id
            packed.add(shot_id)
            seconds = durations.get(shot_id)
            if seconds is None:
                findings.append(
                    _finding(
                        "VID15_MEMBER_SHOT_HAS_NO_DURATION",
                        "a packed shot carries no numeric duration",
                        container_id=container_id,
                        shot_id=shot_id,
                    )
                )
                continue
            packed_members.setdefault(container_id, []).append((shot_id, seconds))

            # Checkpoint 3: the member's own `accepted_duration` against the
            # shot it projects. This field was never read: the total was summed
            # straight from `shots.jsonl`, so a member could claim 12.0s for a
            # 6.3s shot and pass, and the execution end would be handed the 12.0.
            # `motion_timing_check` guards exactly this staleness class; this
            # file had no equivalent.
            claimed = _seconds(member.get("accepted_duration"))
            if claimed is None:
                findings.append(
                    _finding(
                        "VID15_MEMBER_HAS_NO_ACCEPTED_DURATION",
                        "a member must project the duration it packs",
                        container_id=container_id,
                        shot_id=shot_id,
                    )
                )
            elif abs(claimed - seconds) > 1e-6:
                findings.append(
                    _finding(
                        "VID15_MEMBER_DURATION_IS_STALE",
                        "a member's accepted_duration does not match its shot",
                        container_id=container_id,
                        shot_id=shot_id,
                        claimed=claimed,
                        accepted=seconds,
                    )
                )
            member_total += seconds
        stated = _seconds(container.get("container_duration"))
        if stated is None:
            findings.append(
                _finding(
                    "VID15_CONTAINER_DURATION_MISSING",
                    "container_duration must be present and a number of seconds",
                    container_id=container_id,
                )
            )
        elif abs(stated - member_total) > 1e-6:
            findings.append(
                _finding(
                    "VID15_CONTAINER_DURATION_IS_NOT_THE_SUM",
                    "container_duration does not equal its members' durations",
                    container_id=container_id,
                    stated=stated,
                    computed=round(member_total, 6),
                )
            )
        container_total += member_total

    loose = sorted(episode_shots - packed)
    # A shot whose duration is still open is a legal state upstream, so it is
    # held out of the arithmetic instead of being reported as an error. Only a
    # shot packed into a container must already have one, because the
    # container's own duration claim depends on it.
    unmeasured = sorted(
        shot_id for shot_id in episode_shots if durations.get(shot_id) is None
    )
    loose_total = sum(
        durations[shot_id] or 0.0 for shot_id in loose if durations.get(shot_id) is not None
    )

    episode_total = sum(value for value in durations.values() if value is not None)
    if abs((container_total + loose_total) - episode_total) > 1e-6:
        findings.append(
            _finding(
                "VID15_EPISODE_TOTAL_DOES_NOT_RECONCILE",
                "containers plus loose shots do not add up to the episode total",
                packed_seconds=round(container_total, 6),
                loose_seconds=round(loose_total, 6),
                episode_seconds=round(episode_total, 6),
            )
        )

    # Cut-mark reconciliation is a separate claim (VID-13) from the set
    # arithmetic (VID-15), so it is reported under its own rule and counted
    # separately. Without motion specs there is nothing to read, and the
    # omission is named rather than silent: a pass that never saw the bodies
    # would certify cut times it never checked.
    cut_marks_checked = 0
    cut_marks_skipped_no_dialect: list[str] = []
    if motion_specs is not None:
        cut_findings, cut_marks_checked, cut_marks_skipped_no_dialect = check_cut_marks(
            containers, packed_members, _motion_body(motion_specs)
        )
        findings.extend(cut_findings)

    result = {
        "schema_version": SCHEMA_VERSION,
        "containers": len(containers),
        "episode_shots": len(episode_shots),
        "packed_shots": len(packed),
        # Loose shots are legal: containers need not cover everything. They are
        # reported so the count is a decision rather than an oversight.
        "loose_shots": loose,
        # Reported, not a finding: these shots are excluded from every total
        # above, so a caller can tell an incomplete episode from a wrong one.
        "unmeasured_shots": unmeasured,
        "packed_seconds": round(container_total, 6),
        "loose_seconds": round(loose_total, 6),
        "episode_seconds": round(episode_total, 6),
        # Cut marks (VID-13) are recomputed from member durations whenever
        # motion specs are supplied. With no specs the count is null -- the
        # check did not run -- which is never the same as zero checked.
        "cut_marks_checked": None if motion_specs is None else cut_marks_checked,
        # Containers whose bodies are outside the H3 cut-mark dialect: named
        # rather than folded into "checked", so a caller can tell "no cut times
        # claimed" from "cut times verified".
        "cut_marks_skipped_no_dialect": (
            None if motion_specs is None else cut_marks_skipped_no_dialect
        ),
        "findings": findings,
        "status": "pass" if not findings else "fail",
    }
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Reconcile delivery containers with the episode's shot set."
    )
    parser.add_argument("containers", type=Path, help="the episode containers JSONL")
    parser.add_argument("--shots", type=Path, required=True)
    parser.add_argument(
        "--motion-specs",
        type=Path,
        help="motion-specs.jsonl; with it every multi-shot container body's "
        "`[Shot k] At ...` cut marks are recomputed from the member durations "
        "(VID-13) instead of trusted as written. Without it that check does "
        "not run and the report says so via cut_marks_checked: null",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        motion_specs = (
            _load_jsonl(args.motion_specs) if args.motion_specs is not None else None
        )
        result = reconcile(
            _load_jsonl(args.containers), _load_jsonl(args.shots), motion_specs
        )
    except CheckError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
