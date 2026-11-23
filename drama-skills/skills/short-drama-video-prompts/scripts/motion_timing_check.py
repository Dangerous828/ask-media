#!/usr/bin/env python3
"""Check explicit motion segment timing against accepted shot duration (`VID-04`).

`VID-04` is arithmetic, and it is violated in two directions that fail
differently:

* **Overflow** — segments extend past the accepted duration. Whatever falls
  outside is truncated, taking the closing action, the verbatim dialogue tail
  and the end pose with it.
* **Shortfall** — segments stop short. The execution end may not stop or
  hold at the last written mark; in a small H3 sample it stretched the written
  action to fill the shot, so the written seconds landed later than planned and
  the plan no longer described the output.

Both are the same rule, so both are reported under the same ID with distinct
diagnostic codes. Relative timing plans are out of scope by contract: only a
plan that declares itself `explicit` makes a checkable arithmetic claim.

The script reads accepted creator files and writes nothing.
"""

from __future__ import annotations

import argparse
import json
import math
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
# Seconds are authored by hand, so compare with a tolerance rather than by
# equality: 0.1 + 0.2 != 0.3 in binary floating point, and a rule that fires on
# that would be noise. A millisecond is far below anything a shot can express.
TOLERANCE_SECONDS = 1e-6
# An interval reads `0.0-1.5`. Accept the en dash and the CJK wave dash too:
# creators type these on Chinese input methods and the distinction carries no
# meaning here.
INTERVAL_RE = re.compile(
    r"^\s*(?P<start>\d+(?:\.\d+)?)\s*[-–—~～]\s*(?P<end>\d+(?:\.\d+)?)\s*(?:s|秒)?\s*$"
)


class CheckError(ValueError):
    """The inputs cannot be checked at all, as opposed to failing a check."""


def _reject_json_constant(value: str) -> None:
    raise CheckError(f"non-finite JSON number is not allowed: {value}")


def _finite_number(value: Any) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    number = float(value)
    return number if math.isfinite(number) else None


def _load_jsonl(path: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise CheckError(f"cannot read {path}: {error}") from error
    for number, line in enumerate(text.splitlines(), start=1):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        try:
            record = json.loads(stripped, parse_constant=_reject_json_constant)
        except json.JSONDecodeError as error:
            raise CheckError(f"{path.name} line {number} is not valid JSON: {error}") from error
        if not isinstance(record, dict):
            raise CheckError(f"{path.name} line {number} is not a JSON object")
        records.append(record)
    if records and records[0].get("record_type") == SOURCES_RECORD_TYPE:
        del records[0]
    return records


def _finding(code: str, motion_id: str, message: str, **extra: Any) -> dict[str, Any]:
    return {
        "code": code,
        "rule": "VID-04",
        "severity": "error",
        "motion_id": motion_id,
        "message": message,
        **extra,
    }


def _parse_interval(value: Any) -> tuple[float, float] | None:
    """Return an explicit ``(start, end)`` window, or None when unparseable."""

    if isinstance(value, dict):
        start = _finite_number(value.get("start_seconds"))
        end = _finite_number(value.get("end_seconds"))
        if start is not None and end is not None:
            return start, end
        return None
    if isinstance(value, str):
        match = INTERVAL_RE.match(value)
        if match:
            return float(match.group("start")), float(match.group("end"))
    return None


def _union_length(windows: list[tuple[float, float]]) -> float:
    """Total time occupied by ``windows``, counting overlap once."""

    total = 0.0
    cursor: float | None = None
    span_end = 0.0
    for start, end in sorted(windows):
        if cursor is None or start > span_end:
            if cursor is not None:
                total += span_end - cursor
            cursor, span_end = start, end
        else:
            span_end = max(span_end, end)
    if cursor is not None:
        total += span_end - cursor
    return total


def _accepted_duration(
    spec: dict[str, Any], shots_by_id: dict[str, dict[str, Any]]
) -> tuple[float | None, str | None]:
    """Resolve the accepted shot duration and any conflict with the projection.

    ``boundary_refs.duration.value_seconds`` is a read-only projection of the
    shot record. When both are present and disagree, the projection is stale and
    the arithmetic below would be checked against a number the storyboard never
    accepted, so that is reported instead of silently preferring one.
    """

    boundary = spec.get("boundary_refs")
    duration_ref = boundary.get("duration") if isinstance(boundary, dict) else None
    projected: float | None = None
    record_id: str | None = None
    if isinstance(duration_ref, dict):
        projected = _finite_number(duration_ref.get("value_seconds"))
        if isinstance(duration_ref.get("record_id"), str):
            record_id = duration_ref["record_id"]

    shot_ref = spec.get("shot_ref")
    if record_id is None and isinstance(shot_ref, dict):
        if isinstance(shot_ref.get("record_id"), str):
            record_id = shot_ref["record_id"]

    authoritative: float | None = None
    if record_id is not None:
        shot = shots_by_id.get(record_id)
        if isinstance(shot, dict):
            authoritative = _finite_number(shot.get("duration_seconds"))
        elif projected is not None:
            # A reference naming no shot used to fall through to
            # `resolved = projected`, so the arithmetic was then checked against
            # the spec's own self-declared number and the staleness guard never
            # ran -- one mistyped character switched off VID-04. Only reported
            # when a projection exists: with neither a shot nor a projection
            # there is nothing to be wrong about, and `unmeasured` stays the
            # honest answer.
            return None, (
                f"duration reference {record_id} resolves to no shot, so the "
                f"projected {projected}s is checked against nothing"
            )

    if projected is not None and authoritative is not None:
        if abs(projected - authoritative) > TOLERANCE_SECONDS:
            return None, (
                f"projected duration {projected}s does not match accepted "
                f"{record_id} duration {authoritative}s"
            )
        return authoritative, None
    resolved = authoritative if authoritative is not None else projected
    return resolved, None


def _generation_duration_problem(
    spec: dict[str, Any],
    duration: float | None,
    bounds: dict[str, float] | None,
    motion_id: str,
) -> tuple[dict[str, Any] | None, str | None]:
    """Check a declared generation duration against the shot and the model band.

    The storyboard accepts a narrative shot length, which may be fractional; the
    execution end only accepts its own legal steps. Submitting the narrative
    length verbatim violates the model, and rewriting it silently violates the
    storyboard, so a spec that submits must declare which seconds it actually
    sent. This is optional: a spec that has not been submitted yet says nothing,
    and inventing a number for it would be worse than reporting nothing.

    Returns (finding, skip_reason). A skip reason means the claim cannot be
    judged here and must not be counted as a pass.
    """
    raw = spec.get("generation_duration_seconds")
    if raw is None:
        return None, "not_submitted"
    declared = _finite_number(raw)
    if declared is None or declared <= 0:
        return (
            _finding(
                "VID_GENERATION_DURATION_INVALID",
                motion_id,
                f"generation_duration_seconds is {raw!r}, not a positive duration",
            ),
            None,
        )
    if duration is not None and declared < duration - TOLERANCE_SECONDS:
        return (
            _finding(
                "VID_GENERATION_SHORTER_THAN_SHOT",
                motion_id,
                f"generation_duration_seconds is {declared}s but the accepted shot "
                f"is {duration}s; the closing action and end pose would be cut off. "
                f"Raise the generation duration to a legal step at or above the shot "
                f"length, or send the shot back to the storyboard for a split",
            ),
            None,
        )
    if bounds is None:
        return None, "model_band_undeclared"
    minimum = bounds.get("min")
    maximum = bounds.get("max")
    if minimum is not None and declared < minimum - TOLERANCE_SECONDS:
        return (
            _finding(
                "VID_GENERATION_OUTSIDE_MODEL_BAND",
                motion_id,
                f"generation_duration_seconds is {declared}s, below the model's "
                f"{minimum}s minimum",
            ),
            None,
        )
    if maximum is not None and declared > maximum + TOLERANCE_SECONDS:
        return (
            _finding(
                "VID_GENERATION_OUTSIDE_MODEL_BAND",
                motion_id,
                f"generation_duration_seconds is {declared}s, above the model's "
                f"{maximum}s maximum; the shot has to be split in the storyboard",
            ),
            None,
        )
    if spec.get("integer_duration_only") and abs(declared - round(declared)) > TOLERANCE_SECONDS:
        return (
            _finding(
                "VID_GENERATION_NOT_INTEGER",
                motion_id,
                f"generation_duration_seconds is {declared}s but this model only "
                f"accepts whole seconds",
            ),
            None,
        )
    return None, None


def check(
    specs: list[dict[str, Any]],
    shots: list[dict[str, Any]],
    duration_bounds: dict[str, float] | None = None,
) -> dict[str, Any]:
    # A file with no motion specs verified nothing: without this guard an empty
    # (or sources-only) file reported `status: pass` over zero rows, which is
    # the "checked and clean" illusion this script exists to remove.
    if not specs:
        raise CheckError("motion spec file carries no motion records")
    shots_by_id = {
        shot["shot_id"]: shot
        for shot in shots
        if isinstance(shot.get("shot_id"), str)
    }
    findings: list[dict[str, Any]] = []
    checked = 0
    # Reported, not a finding: a relative plan makes no arithmetic claim, so it
    # is out of scope rather than passing. Keeping the count visible stops a
    # file of entirely relative plans from reading as a clean explicit check.
    relative: list[str] = []
    unmeasured: list[str] = []
    # Generation duration is a separate claim from the narrative shot length, so
    # it is counted separately: a run that declares no generation durations has
    # verified nothing about the model band and must not read as if it had.
    generation_checked = 0
    generation_skipped: list[str] = []

    for index, spec in enumerate(specs):
        motion_id = spec.get("motion_id")
        if not isinstance(motion_id, str) or not motion_id:
            raise CheckError(f"motion spec {index} has no motion_id")

        plan = spec.get("timing_plan")
        mode = plan.get("mode") if isinstance(plan, dict) else None
        segments = [
            entry.get("timing")
            for entry in spec.get("ordered_subject_motion") or []
            if isinstance(entry, dict)
        ]
        explicit_segments = [
            timing
            for timing in segments
            if isinstance(timing, dict) and timing.get("mode") == "explicit"
        ]
        # Whether the projection matches the shot is a fact about the data, not
        # about the timing mode, so it is checked before the mode gate below.
        # Gated behind `explicit` it never ran on a file of relative plans --
        # which is every spec in the recorded run -- and a projection authored
        # wrong from the start was carried downstream unchallenged.
        duration, conflict = _accepted_duration(spec, shots_by_id)

        # The generation duration is its own claim and does not depend on the
        # timing mode or on the projection being fresh, so it runs before the
        # `continue` below. A stale projection says the shot length moved; the
        # submitted seconds can still be wrong for the model on their own.
        generation_finding, generation_skip = _generation_duration_problem(
            spec, duration, duration_bounds, motion_id
        )
        if generation_finding is not None:
            findings.append(generation_finding)
        elif generation_skip is None:
            generation_checked += 1
        else:
            generation_skipped.append(f"{motion_id}:{generation_skip}")

        if conflict is not None:
            findings.append(_finding("VID_DURATION_PROJECTION_STALE", motion_id, conflict))
            continue

        if mode != "explicit":
            # A relative plan makes no arithmetic claim, so it is out of scope
            # by contract rather than passing. Explicit segments underneath one
            # are a contradiction the creator has to resolve — silently doing
            # the arithmetic anyway would judge a plan the docs promise not to.
            if explicit_segments:
                findings.append(
                    _finding(
                        "VID_TIMING_MODE_INCONSISTENT",
                        motion_id,
                        f"timing_plan mode is {mode!r} but "
                        f"{len(explicit_segments)} segment(s) declare explicit timing",
                    )
                )
            else:
                relative.append(motion_id)
            continue

        if duration is None:
            # Cannot be judged either way, and staying silent here is the
            # failure mode this script exists to remove.
            unmeasured.append(motion_id)
            continue

        windows: list[tuple[float, float]] = []
        unparseable: list[Any] = []
        for timing in explicit_segments:
            interval = _parse_interval(timing.get("value"))
            if interval is None:
                unparseable.append(timing.get("value"))
            else:
                windows.append(interval)
        if unparseable:
            findings.append(
                _finding(
                    "VID_EXPLICIT_TIMING_UNPARSEABLE",
                    motion_id,
                    "explicit segment timing is not a readable seconds interval",
                    values=unparseable,
                )
            )
            continue
        if not windows:
            findings.append(
                _finding(
                    "VID_EXPLICIT_TIMING_UNPARSEABLE",
                    motion_id,
                    "timing_plan declares explicit mode but no segment carries an interval",
                )
            )
            continue

        inverted = [
            f"{start}-{end}"
            for start, end in windows
            if start < 0 or end < 0 or end < start
        ]
        if inverted:
            findings.append(
                _finding(
                    "VID_EXPLICIT_TIMING_UNPARSEABLE",
                    motion_id,
                    "explicit segment ends before it starts",
                    values=inverted,
                )
            )
            continue

        checked += 1
        ordered = sorted(windows)
        declared_overlap = bool(
            isinstance(plan, dict) and plan.get("declares_overlap") is True
        )
        overlaps = [
            f"{ordered[position - 1][0]}-{ordered[position - 1][1]} / {start}-{end}"
            for position, (start, end) in enumerate(ordered)
            if position and start < ordered[position - 1][1] - TOLERANCE_SECONDS
        ]
        if overlaps and not declared_overlap:
            findings.append(
                _finding(
                    "VID_EXPLICIT_TIMING_UNDECLARED_OVERLAP",
                    motion_id,
                    "segments overlap without an explicit overlap declaration",
                    values=overlaps,
                )
            )
            continue

        # The two failure directions are measured from different quantities on
        # purpose. Comparing one total against the duration hides the plan that
        # commits both at once: 0.0-2.0 plus 3.0-5.0 covers exactly 4.0s of a
        # 4.0s shot, so the totals match — while a segment runs a second past
        # the end (truncated) and the 2-3s window sits unallocated (the written
        # action stretches over it). Overflow is therefore read off the endpoint, and
        # shortfall off the union clipped to the shot.
        covered = _union_length(ordered)
        # max(), not ordered[-1][1]: sorting (start, end) tuples orders by
        # start, so the last element is the latest-starting segment, whose end
        # can sit well inside an earlier segment that encloses it. A sustained
        # motion spanning the shot with beats inside it — exactly what
        # motion-recipe.md tells creators to mark `declares_overlap` — would
        # otherwise have its overrun read off one of the inner beats.
        last_end = max((end for _, end in ordered), default=0.0)
        inside = _union_length(
            [
                (max(start, 0.0), min(end, duration))
                for start, end in ordered
                if min(end, duration) > max(start, 0.0)
            ]
        )

        if last_end - duration > TOLERANCE_SECONDS:
            findings.append(
                _finding(
                    "VID_EXPLICIT_TIMING_OVERFLOW",
                    motion_id,
                    f"explicit timing runs to {last_end}s on an accepted {duration}s shot; "
                    "everything past the end is truncated",
                    accepted_duration_seconds=duration,
                    endpoint_seconds=round(last_end, 6),
                    overflow_seconds=round(last_end - duration, 6),
                )
            )
        unallocated = duration - inside
        if unallocated > TOLERANCE_SECONDS:
            findings.append(
                _finding(
                    "VID_EXPLICIT_TIMING_SHORTFALL",
                    motion_id,
                    f"explicit timing leaves {round(unallocated, 6)}s of an accepted "
                    f"{duration}s shot unallocated; the written action may be stretched "
                    "to fill it, so the written seconds may not be where it lands",
                    accepted_duration_seconds=duration,
                    allocated_seconds=round(inside, 6),
                    unallocated_seconds=round(unallocated, 6),
                )
            )

        declared_total = (
            plan.get("declared_total_or_endpoint_seconds") if isinstance(plan, dict) else None
        )
        # The field is named `declared_total_or_endpoint_seconds`, so both
        # readings are legitimate and they differ whenever overlap is declared.
        # Matching either is a pass; insisting on one would make a correct plan
        # fail under the other spelling.
        declared_number = _finite_number(declared_total)
        if declared_total is not None and declared_number is None:
            findings.append(
                _finding(
                    "VID_DECLARED_TOTAL_MISMATCH",
                    motion_id,
                    "timing_plan declared total must be a finite non-negative number",
                )
            )
        elif declared_number is not None and declared_number < 0:
            findings.append(
                _finding(
                    "VID_DECLARED_TOTAL_MISMATCH",
                    motion_id,
                    "timing_plan declared total must be a finite non-negative number",
                    declared_seconds=declared_number,
                )
            )
        elif declared_number is not None and not any(
            abs(declared_number - candidate) <= TOLERANCE_SECONDS
            for candidate in (covered, last_end)
        ):
            findings.append(
                _finding(
                    "VID_DECLARED_TOTAL_MISMATCH",
                    motion_id,
                    f"timing_plan declares {declared_total}s, which is neither the "
                    f"{round(covered, 6)}s its segments occupy nor their "
                    f"{round(last_end, 6)}s endpoint",
                    declared_seconds=declared_number,
                    covered_seconds=round(covered, 6),
                    endpoint_seconds=round(last_end, 6),
                )
            )

    return {
        "schema_version": SCHEMA_VERSION,
        "motion_specs": len(specs),
        "explicit_checked": checked,
        "generation_durations_checked": generation_checked,
        "generation_durations_skipped": generation_skipped,
        "relative_plans": relative,
        "unmeasured_specs": unmeasured,
        "findings": findings,
        "status": "pass" if not findings else "fail",
    }


def _duration_bounds(profile_path: Path | None) -> dict[str, float] | None:
    """Read `native_duration_seconds` from the project profile, if one was given.

    Without it the model band is unknown, and an undeclared band is reported as
    skipped rather than assumed: guessing 4-15 for a model that accepts 2-30
    would fail legal shots, and guessing wider than the model allows would pass
    illegal ones.
    """
    if profile_path is None:
        return None
    try:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise CheckError(f"cannot read {profile_path}: {error}") from error
    choices = (
        profile.get("creator_authority", {}).get("production_profile", {}).get("choices", {})
        if isinstance(profile, dict)
        else {}
    )
    band = choices.get("native_duration_seconds") if isinstance(choices, dict) else None
    if not isinstance(band, dict):
        return None
    bounds: dict[str, float] = {}
    for key in ("min", "max"):
        value = _finite_number(band.get(key))
        if value is not None:
            bounds[key] = value
    return bounds or None


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Check explicit motion timing against accepted shot duration (VID-04)."
    )
    parser.add_argument("motion_specs", type=Path, help="the episode motion specs JSONL")
    parser.add_argument("--shots", type=Path, required=True)
    parser.add_argument(
        "--profile",
        type=Path,
        help="short-drama.json, read for native_duration_seconds; without it a "
        "declared generation duration is reported as skipped, not passed",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = check(
            _load_jsonl(args.motion_specs),
            _load_jsonl(args.shots),
            _duration_bounds(args.profile),
        )
    except CheckError as error:
        print(f"{type(error).__name__}: {error}", file=sys.stderr)
        return 2
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, allow_nan=False))
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
