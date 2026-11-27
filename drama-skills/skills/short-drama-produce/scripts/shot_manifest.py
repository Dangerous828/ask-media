#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""shot_manifest.py -- validate and plan a short-drama production manifest.

The manifest is a build file: assets -> prompt labels -> channel slots ->
submission parameters. It never carries story, dialogue or prompt prose.

Commands:
    validate <project> --manifest <yaml|json> [--json] [--allow-missing-hash]
    plan     <project> --manifest <yaml|json> --shot <id> [--json]

Exit codes:
    0  no errors (warnings allowed)
    1  validation errors
    2  usage / IO / parse errors
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:  # YAML input needs PyYAML; JSON works without it.
    yaml = None

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit(
        "shot_manifest.py requires Python %s.%s+" % MINIMUM_PYTHON
    )

TECHNIQUES = {"ref2va", "frame_ref2va", "i2va", "fl2va", "multishot",
              "motion_drive", "t2va"}
ROLES = {
    "identity", "scene", "prop", "style",
    "first_frame", "last_frame", "scene_video", "action_video", "audio",
}
ASSET_KINDS = {"identity", "scene", "prop", "style", "action", "audio", "clip",
               "keyframe"}
ADMISSION_STATUSES = {"accepted", "creator_original", "reviewed", "unset"}
SHOT_STATUSES = {"active", "archived"}
PLAN_STATUSES = {"active", "archived"}
SEAM_KINDS = {"inner", "inter"}
SEAM_JOINS = {"continuous", "hard_cut", "interval", "j_cut", "l_cut"}
SEAM_REASONS = {"none", "scene_change", "time_jump", "action_bridge",
                "sound_bridge", "identity_bridge", "coverage_cut"}
DECISION_REASON_CODES = {"creator_alignment", "creator_pending", "source_priority",
                         "continuity", "look_approved", "scope_boundary", "other"}
DECISION_STATUSES = {"accepted", "pending", "rejected"}
CONFLICT_STATUSES = {"unresolved", "resolved", "accepted"}
DRIFT_KINDS = {"prompt_body", "keyframe", "keyframe_lens", "state", "seam"}
DRIFT_STATUSES = {"unresolved", "resolved", "accepted"}
QC_CHECK_STATUSES = {"pass", "fail", "pending", "unverified"}
SEAM_PROSE_KEYS = {"camera_side", "occlusion_light", "first_frame_source",
                   "cost_tier", "new_info", "if_not_cut"}
KEYFRAME_ROLES = {"start", "composition", "pose_proof", "end"}
MEDIA_STATES = {"accepted", "not_generated", "stale", "rejected"}
AUDIT_LEVELS = {"core", "optional"}
KEYFRAME_USES = {"start_check", "composition_ref", "pose_proof", "end_check",
                 "not_generated"}
GROUP_MODES = {"single", "continuous", "interval", "hard_cut", "j_cut", "l_cut"}
QC_STATUSES = {"pass", "fail", "pending"}
LEDGER_ID_RE = re.compile(r"^[A-Z][A-Z0-9-]*$")
SCENE_ID_RE = re.compile(r"^EP\d+-SC\d+$")
WORKFLOWS = {"ref2va", "pdd_lu", "fl2va", "multishot", "motion_drive"}
DEFAULT_WORKFLOW = {
    "ref2va": "ref2va",
    "frame_ref2va": "ref2va",
    "i2va": "ref2va",
    "fl2va": "fl2va",
    "multishot": "multishot",
    "motion_drive": "motion_drive",
    "t2va": "ref2va",
}
ALLOWED_WORKFLOWS = {
    "ref2va": {"ref2va", "pdd_lu"},
    "frame_ref2va": {"ref2va", "pdd_lu"},
    "i2va": {"ref2va"},
    "fl2va": {"fl2va"},
    "multishot": {"multishot"},
    "motion_drive": {"motion_drive"},
    "t2va": {"ref2va"},
}
REQUIRED_ROLES = {
    "ref2va": {},
    "frame_ref2va": {"identity": 1},
    "i2va": {"first_frame": 1},
    "fl2va": {"first_frame": 1, "last_frame": 1},
    "multishot": {"identity": 1},
    "motion_drive": {"identity": 1, "action_video": 1},
    "t2va": {},
}
FORBIDDEN_ROLES = {
    "ref2va": {"first_frame", "last_frame", "scene_video", "action_video", "audio"},
    "frame_ref2va": {"first_frame", "last_frame", "scene_video", "action_video", "audio"},
    "i2va": {"last_frame", "scene_video", "action_video", "audio",
             "identity", "scene", "prop", "style"},
    "fl2va": {"scene_video", "action_video", "audio",
              "identity", "scene", "prop", "style"},
    "multishot": {"first_frame", "last_frame", "action_video"},
    "motion_drive": {"first_frame", "last_frame", "scene_video"},
    "t2va": ROLES,
}
LABEL_RE = re.compile(r"<(Picture|Subject|Video|Audio)\s+(\d+)>")
LABEL_VALUE_RE = re.compile(r"^<(Picture|Subject|Video|Audio)\s+(\d+)>$")
SHA_RE = re.compile(r"^(?:sha256:)?([0-9a-fA-F]{64})$")

ERROR = "error"
WARNING = "warning"


class Problems:
    def __init__(self) -> None:
        self.items: list[dict[str, str]] = []

    def add(self, level: str, code: str, message: str,
            shot: str | None = None, field: str | None = None) -> None:
        item = {"level": level, "code": code, "message": message}
        if shot:
            item["shot"] = shot
        if field:
            item["field"] = field
        self.items.append(item)

    def error(self, code: str, message: str, shot: str | None = None,
              field: str | None = None) -> None:
        self.add(ERROR, code, message, shot, field)

    def warn(self, code: str, message: str, shot: str | None = None,
             field: str | None = None) -> None:
        self.add(WARNING, code, message, shot, field)

    @property
    def errors(self) -> list[dict[str, str]]:
        return [item for item in self.items if item["level"] == ERROR]

    @property
    def warnings(self) -> list[dict[str, str]]:
        return [item for item in self.items if item["level"] == WARNING]


def load_document(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".yaml", ".yml"}:
        if yaml is None:
            raise SystemExit("shot_manifest: PyYAML is required for YAML input")
        return yaml.safe_load(text)
    return json.loads(text)


def project_path(root: Path, value: str) -> Path:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = root / candidate
    candidate = candidate.resolve()
    try:
        candidate.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError("path escapes project root: %s" % value) from exc
    return candidate


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_sha(value: Any) -> str | None:
    if value is None:
        return None
    match = SHA_RE.match(str(value).strip())
    return match.group(1).lower() if match else None


def normalize_label(value: Any) -> str | None:
    if value is None:
        return None
    match = LABEL_VALUE_RE.match(str(value).strip())
    if not match:
        return None
    return "<%s %s>" % (match.group(1), match.group(2))


def labels_in_text(text: str) -> set[str]:
    return {"<%s %s>" % (kind, number) for kind, number in LABEL_RE.findall(text)}


def asset_versions(asset_id: str, raw: Any, problems: Problems) -> list[dict[str, Any]]:
    if not isinstance(raw, dict):
        problems.error("ASSET001", "asset %s must be a mapping" % asset_id, field=asset_id)
        return []
    versions = raw.get("versions")
    if versions is None:
        versions = [{
            "version": 1,
            "path": raw.get("path"),
            "sha256": raw.get("sha256"),
            "previous_path": raw.get("previous_path"),
        }]
    if not isinstance(versions, list) or not versions:
        problems.error("ASSET002", "asset %s has no versions" % asset_id, field=asset_id)
        return []
    result: list[dict[str, Any]] = []
    seen: set[int] = set()
    for item in versions:
        if not isinstance(item, dict):
            problems.error("ASSET003", "asset %s version must be a mapping" % asset_id,
                           field=asset_id)
            continue
        try:
            number = int(item.get("version", 0))
        except (TypeError, ValueError):
            number = 0
        if number < 1:
            problems.error("ASSET004", "asset %s version must be a positive integer" % asset_id,
                           field=asset_id)
            continue
        if number in seen:
            problems.error("ASSET005", "asset %s duplicate version %s" % (asset_id, number),
                           field=asset_id)
            continue
        seen.add(number)
        if not item.get("path"):
            problems.error("ASSET006", "asset %s v%s has no path" % (asset_id, number),
                           field=asset_id)
            continue
        result.append({**item, "version": number})
    return sorted(result, key=lambda item: item["version"])


def resolve_asset(assets: dict[str, Any], ref: str,
                  problems: Problems) -> tuple[str, dict[str, Any]] | None:
    asset_id, _, version_text = str(ref).partition("@")
    raw = assets.get(asset_id)
    if raw is None:
        problems.error("BIND001", "binding references unknown asset %r" % ref)
        return None
    versions = asset_versions(asset_id, raw, problems)
    if not versions:
        return None
    if version_text:
        try:
            wanted = int(version_text)
        except ValueError:
            problems.error("BIND002", "asset version must be an integer: %r" % ref)
            return None
        for item in versions:
            if item["version"] == wanted:
                return asset_id, item
        problems.error("BIND003", "asset %s has no version %s" % (asset_id, wanted))
        return None
    return asset_id, versions[-1]


def used_asset_ids(doc: dict[str, Any]) -> set[str]:
    used: set[str] = set()
    shots = doc.get("shots")
    if not isinstance(shots, list):
        return used
    for shot in shots:
        if not isinstance(shot, dict):
            continue
        if str(shot.get("status") or "active").strip().lower() == "archived":
            continue
        for binding in shot.get("bindings") or []:
            if isinstance(binding, dict) and binding.get("asset"):
                used.add(str(binding["asset"]).split("@")[0])
    return used


def check_asset_files(root: Path, assets: dict[str, Any],
                      problems: Problems, allow_missing_hash: bool,
                      allow_unadmitted: bool = False,
                      used_ids: set[str] | None = None) -> None:
    for asset_id, raw in assets.items():
        kind = str(raw.get("kind") or "").strip().lower()
        if not kind:
            problems.error("ASSET011", "asset %s has no kind" % asset_id, field=asset_id)
        elif kind not in ASSET_KINDS:
            problems.error("ASSET011", "asset %s has unknown kind %r (allowed: %s)"
                           % (asset_id, kind, ", ".join(sorted(ASSET_KINDS))),
                           field=asset_id)
        admission = raw.get("admission") or {}
        status = str(admission.get("status") or "unset").strip().lower()
        is_used = used_ids is None or asset_id in used_ids
        if status not in ADMISSION_STATUSES:
            if is_used:
                problems.error("ASSET012", "asset %s has unknown admission.status %r"
                               % (asset_id, status), field=asset_id)
        elif is_used and status == "unset":
            if allow_unadmitted:
                problems.warn("ASSET013", "asset %s is not admitted (unset)" % asset_id,
                              field=asset_id)
            else:
                problems.error("ASSET013", "asset %s is not admitted (unset)" % asset_id,
                               field=asset_id)
        elif is_used and status == "reviewed":
            problems.warn("ASSET014", "asset %s is reviewed but not accepted" % asset_id,
                          field=asset_id)
        versions = asset_versions(asset_id, raw, problems)
        for item in versions:
            try:
                path = project_path(root, str(item["path"]))
            except ValueError as exc:
                problems.error("ASSET007", str(exc), field=asset_id)
                continue
            if not path.is_file():
                problems.error("ASSET008", "asset file missing: %s" % item["path"],
                               field=asset_id)
                continue
            expected = normalize_sha(item.get("sha256"))
            if expected is None:
                if not allow_missing_hash:
                    problems.error("ASSET009", "asset %s v%s has no sha256"
                                   % (asset_id, item["version"]), field=asset_id)
                continue
            actual = sha256_file(path)
            if actual != expected:
                problems.error("ASSET010", "asset %s v%s sha256 mismatch: %s != %s"
                               % (asset_id, item["version"], actual[:12], expected[:12]),
                               field=asset_id)


def binding_role(binding: dict[str, Any]) -> str:
    return str(binding.get("role") or "").strip().lower()


def binding_labels(binding: dict[str, Any]) -> list[str]:
    labels: list[str] = []
    for key in ("prompt_label", "subject_label", "video_label", "audio_label"):
        value = binding.get(key)
        if value in (None, ""):
            continue
        normalized = normalize_label(value)
        if normalized is None:
            labels.append(str(value))
        else:
            labels.append(normalized)
    return labels


def check_bindings(root: Path, shot: dict[str, Any], assets: dict[str, Any],
                   problems: Problems) -> list[dict[str, Any]]:
    shot_id = str(shot.get("id") or "?")
    technique = str(shot.get("technique") or "").strip().lower()
    bindings = shot.get("bindings") or []
    if not isinstance(bindings, list):
        problems.error("SHOT001", "bindings must be a list", shot=shot_id)
        return []
    normalized: list[dict[str, Any]] = []
    seen_labels: dict[str, int] = {}
    refs: list[dict[str, Any]] = []
    for index, raw in enumerate(bindings):
        if not isinstance(raw, dict):
            problems.error("BIND004", "binding must be a mapping", shot=shot_id,
                           field="bindings[%s]" % index)
            continue
        binding = dict(raw)
        asset_ref = binding.get("asset")
        if not asset_ref:
            problems.error("BIND005", "binding has no asset", shot=shot_id,
                           field="bindings[%s]" % index)
            continue
        resolved = resolve_asset(assets, str(asset_ref), problems)
        if resolved is None:
            continue
        asset_id, version = resolved
        binding["asset_id"] = asset_id
        binding["asset_version"] = version
        role = binding_role(binding)
        if role not in ROLES:
            problems.error("BIND006", "unknown role %r (allowed: %s)"
                           % (role, ", ".join(sorted(ROLES))), shot=shot_id,
                           field="bindings[%s].role" % index)
            continue
        if role in FORBIDDEN_ROLES.get(technique, set()):
            problems.error("BIND007", "role %r is not allowed for technique %r"
                           % (role, technique), shot=shot_id,
                           field="bindings[%s].role" % index)
        semantic = str(binding.get("semantic") or "").strip().lower()
        if semantic and semantic not in {"first_frame", "last_frame", "composition",
                                         "start", "pose_proof", "end"}:
            problems.error("BIND019", "unknown semantic %r" % semantic, shot=shot_id,
                           field="bindings[%s].semantic" % index)
        if semantic == "first_frame" and role not in {"identity", "scene", "prop", "style"}:
            problems.error("BIND020",
                           "semantic first_frame requires a reference role "
                           "(identity/scene/prop/style)", shot=shot_id,
                           field="bindings[%s].role" % index)
        if (role in {"identity", "scene", "prop", "style"}
                and technique in {"ref2va", "frame_ref2va", "i2va", "fl2va", "multishot"}
                and "ref_slot" not in binding):
            problems.error("BIND014", "role %s needs ref_slot for technique %s"
                           % (role, technique), shot=shot_id,
                           field="bindings[%s].ref_slot" % index)
        if role in {"identity", "scene", "prop", "style"}:
            if technique == "frame_ref2va":
                if not binding.get("prompt_label"):
                    problems.error("BIND015", "role %s needs prompt_label for frame_ref2va"
                                   % role, shot=shot_id)
                if semantic != "first_frame" and not binding.get("subject_label"):
                    problems.error("BIND016", "role %s needs subject_label for frame_ref2va"
                                   % role, shot=shot_id)
            elif technique in {"ref2va", "i2va", "fl2va"}:
                if not binding.get("prompt_label"):
                    problems.error("BIND015", "role %s needs prompt_label for technique %s"
                                   % (role, technique), shot=shot_id)
                if not binding.get("subject_label"):
                    problems.error("BIND016", "role %s needs subject_label for technique %s"
                                   % (role, technique), shot=shot_id)
            elif technique == "multishot" and not binding.get("subject_label"):
                problems.error("BIND017", "role %s needs subject_label for multishot" % role,
                               shot=shot_id)
        if role in {"first_frame", "last_frame"} and not binding.get("prompt_label"):
            problems.error("BIND018", "role %s needs prompt_label" % role, shot=shot_id)
        for label in binding_labels(binding):
            if normalize_label(label) is None:
                problems.error("BIND008", "invalid label %r (expected <Picture N> etc.)"
                               % label, shot=shot_id, field="bindings[%s]" % index)
                continue
            if label in seen_labels:
                problems.error("BIND009", "label %s bound twice (bindings %s and %s)"
                               % (label, seen_labels[label], index), shot=shot_id)
            seen_labels[label] = index
        if "ref_slot" in binding:
            try:
                slot = int(binding["ref_slot"])
            except (TypeError, ValueError):
                slot = 0
            if slot < 1:
                problems.error("BIND010", "ref_slot must be a positive integer",
                               shot=shot_id, field="bindings[%s].ref_slot" % index)
            else:
                binding["ref_slot"] = slot
                refs.append(binding)
        if role == "scene_video":
            if binding.get("start") is not None:
                try:
                    binding["start"] = float(binding["start"])
                except (TypeError, ValueError):
                    problems.error("BIND011", "scene_video.start must be a number",
                                   shot=shot_id, field="bindings[%s].start" % index)
            if binding.get("seconds") is not None:
                try:
                    binding["seconds"] = float(binding["seconds"])
                except (TypeError, ValueError):
                    problems.error("BIND012", "scene_video.seconds must be a number",
                                   shot=shot_id, field="bindings[%s].seconds" % index)
        normalized.append(binding)
    refs.sort(key=lambda item: item["ref_slot"])
    if refs:
        slots = [item["ref_slot"] for item in refs]
        if slots != list(range(1, len(slots) + 1)):
            problems.error("BIND013", "ref_slot must be contiguous from 1: %s" % slots,
                           shot=shot_id)
    return normalized


def check_technique(shot: dict[str, Any], bindings: list[dict[str, Any]],
                    problems: Problems) -> None:
    shot_id = str(shot.get("id") or "?")
    technique = str(shot.get("technique") or "").strip().lower()
    if technique not in TECHNIQUES:
        problems.error("SHOT002", "unknown technique %r (allowed: %s)"
                       % (technique, ", ".join(sorted(TECHNIQUES))), shot=shot_id,
                       field="technique")
        return
    counts: dict[str, int] = {}
    for binding in bindings:
        role = binding_role(binding)
        counts[role] = counts.get(role, 0) + 1
    for role, minimum in REQUIRED_ROLES[technique].items():
        if counts.get(role, 0) < minimum:
            problems.error("SHOT003", "technique %r requires at least %s %s binding(s)"
                           % (technique, minimum, role), shot=shot_id)
    if technique == "ref2va" and not any(
            counts.get(role, 0) for role in ("identity", "scene", "prop", "style")):
        problems.error("SHOT012", "ref2va requires at least one reference binding",
                       shot=shot_id)
    if technique == "frame_ref2va":
        frame_bindings = [b for b in bindings
                          if str(b.get("semantic") or "").strip().lower() == "first_frame"]
        if len(frame_bindings) != 1:
            problems.error("SHOT013", "frame_ref2va requires exactly one semantic first_frame",
                           shot=shot_id)
    if technique == "i2va" and counts.get("first_frame", 0) != 1:
        problems.error("SHOT004", "i2va requires exactly one first_frame", shot=shot_id)
    if technique == "fl2va":
        if counts.get("first_frame", 0) != 1 or counts.get("last_frame", 0) != 1:
            problems.error("SHOT005", "fl2va requires exactly one first_frame and one last_frame",
                           shot=shot_id)
    if technique in {"multishot", "motion_drive"} and any(
            b.get("prompt_label") for b in bindings):
        problems.error("SHOT011", "technique %r does not use prompt_label (<Picture N>)"
                       % technique, shot=shot_id)
    if technique == "multishot":
        scene_videos = [b for b in bindings if binding_role(b) == "scene_video"]
        if len(scene_videos) > 1:
            problems.error("SHOT006", "multishot allows at most one scene_video",
                           shot=shot_id)
        if any(binding_role(b) not in {"identity", "scene_video", "audio"}
               for b in bindings):
            problems.error("SHOT007", "multishot bindings allow only identity/scene_video/audio",
                           shot=shot_id)
    if technique == "motion_drive":
        if any(binding_labels(b) for b in bindings):
            problems.error("SHOT008", "motion_drive does not use H3 prompt labels",
                           shot=shot_id)
    if technique == "t2va" and bindings:
        problems.error("SHOT009", "t2va takes no bindings", shot=shot_id)


def check_prompt(root: Path, shot: dict[str, Any], bindings: list[dict[str, Any]],
                 problems: Problems) -> None:
    shot_id = str(shot.get("id") or "?")
    technique = str(shot.get("technique") or "").strip().lower()
    prompt_value = shot.get("prompt")
    if not prompt_value:
        problems.error("PROMPT001", "shot has no prompt path", shot=shot_id)
        return
    try:
        prompt_path = project_path(root, str(prompt_value))
    except ValueError as exc:
        problems.error("PROMPT002", str(exc), shot=shot_id)
        return
    if not prompt_path.is_file():
        problems.error("PROMPT003", "prompt file missing: %s" % prompt_value, shot=shot_id)
        return
    if technique == "motion_drive":
        return
    prompt_labels = labels_in_text(prompt_path.read_text(encoding="utf-8", errors="replace"))
    bound_labels: set[str] = set()
    for binding in bindings:
        for label in binding_labels(binding):
            normalized = normalize_label(label)
            if normalized:
                bound_labels.add(normalized)
    if technique == "multishot":
        pictures = {label for label in prompt_labels if label.startswith("<Picture")}
        if pictures:
            problems.error("PROMPT004", "multishot prompt must not use <Picture N>: %s"
                           % ", ".join(sorted(pictures)), shot=shot_id)
    missing = prompt_labels - bound_labels
    extra = bound_labels - prompt_labels
    if missing:
        problems.error("PROMPT005", "prompt labels not bound: %s"
                       % ", ".join(sorted(missing)), shot=shot_id)
    if extra:
        problems.error("PROMPT006", "binding labels not in prompt: %s"
                       % ", ".join(sorted(extra)), shot=shot_id)


def positive_int(value: Any) -> int | None:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return None
    return number if number > 0 else None


def check_submit(shot: dict[str, Any], bindings: list[dict[str, Any]],
                 problems: Problems) -> None:
    shot_id = str(shot.get("id") or "?")
    technique = str(shot.get("technique") or "").strip().lower()
    submit = shot.get("submit") or {}
    if not isinstance(submit, dict):
        problems.error("SUBMIT001", "submit must be a mapping", shot=shot_id)
        return
    workflow = str(submit.get("workflow") or DEFAULT_WORKFLOW.get(technique, "")).strip().lower()
    if workflow not in WORKFLOWS:
        problems.error("SUBMIT002", "unknown workflow %r (allowed: %s)"
                       % (workflow, ", ".join(sorted(WORKFLOWS))), shot=shot_id,
                       field="submit.workflow")
        return
    if workflow not in ALLOWED_WORKFLOWS.get(technique, set()):
        problems.error("SUBMIT003", "workflow %r is not allowed for technique %r"
                       % (workflow, technique), shot=shot_id, field="submit.workflow")
    width = positive_int(submit.get("width"))
    height = positive_int(submit.get("height"))
    if width is None or height is None:
        problems.error("SUBMIT004", "width/height must be positive integers", shot=shot_id)
    else:
        if width % 32 or height % 32:
            problems.error("SUBMIT005", "width/height must be multiples of 32: %sx%s"
                           % (width, height), shot=shot_id)
    frames = positive_int(shot.get("frames"))
    if submit.get("seed") is not None and positive_int(submit.get("seed")) is None:
        problems.error("SUBMIT020", "seed must be a positive integer", shot=shot_id)
    if technique == "multishot":
        per = positive_int(submit.get("frames_per_shot"))
        count = positive_int(submit.get("shot_count"))
        if per is None or count is None:
            problems.error("SUBMIT006", "multishot requires frames_per_shot and shot_count",
                           shot=shot_id)
        elif count < 2:
            problems.error("SUBMIT007", "shot_count must be >=2; a single window uses ref2va",
                           shot=shot_id)
        elif per < 5 or (per - 5) % 17:
            problems.error("SUBMIT021", "frames_per_shot must be 17k+5 (e.g. 345), got %s" % per,
                           shot=shot_id)
        elif frames is not None and frames != per * count - (count - 1):
            problems.error("SUBMIT008", "shot.frames %s != per*count-(count-1) %s"
                           % (frames, per * count - (count - 1)), shot=shot_id)
    else:
        if frames is None:
            problems.error("SUBMIT009", "frames must be a positive integer", shot=shot_id)
        if submit.get("frames_per_shot") is not None or submit.get("shot_count") is not None:
            problems.error("SUBMIT010", "frames_per_shot/shot_count are multishot-only",
                           shot=shot_id)
    refs = sorted([b for b in bindings if "ref_slot" in b], key=lambda b: b["ref_slot"])
    refs_order = submit.get("refs_order")
    if refs:
        if not isinstance(refs_order, list) or len(refs_order) != len(refs):
            problems.error("SUBMIT011", "refs_order must list every ref_slot asset",
                           shot=shot_id, field="submit.refs_order")
        else:
            expected = [str(item["asset_id"]) for item in refs]
            actual = [str(item).split("@")[0] for item in refs_order]
            if actual != expected:
                problems.error("SUBMIT012", "refs_order %s != ref_slot order %s"
                               % (actual, expected), shot=shot_id)
    elif refs_order:
        problems.error("SUBMIT013", "refs_order given but no ref_slot bindings", shot=shot_id)
    if technique == "multishot":
        subjects = submit.get("reference_subjects")
        if refs and not subjects:
            problems.error("SUBMIT014", "multishot with refs requires reference_subjects",
                           shot=shot_id)
        if subjects:
            parts = [part.strip() for part in str(subjects).split(",") if part.strip()]
            if len(parts) != len(refs):
                problems.error("SUBMIT015", "reference_subjects has %s entries, refs has %s"
                               % (len(parts), len(refs)), shot=shot_id)
            for part in parts:
                if not part.isdigit() or int(part) < 1:
                    problems.error("SUBMIT016", "reference_subjects must be positive integers: %r"
                                   % subjects, shot=shot_id)
                    break
        scene_videos = [b for b in bindings if binding_role(b) == "scene_video"]
        if submit.get("scene_video") and not scene_videos:
            problems.error("SUBMIT017", "submit.scene_video given but no scene_video binding",
                           shot=shot_id)
        if submit.get("scene_video") and scene_videos:
            binding = scene_videos[0]
            if str(submit["scene_video"]) != str(binding["asset_version"]["path"]):
                problems.error("SUBMIT018", "submit.scene_video path must match the binding",
                               shot=shot_id)
    else:
        for key in ("scene_video", "scene_video_start", "scene_video_seconds",
                    "reference_subjects", "reference_image_size", "auto_chunk_ffn",
                    "voice_ref", "voice_ref_2"):
            if submit.get(key) is not None:
                problems.error("SUBMIT019", "%s is multishot-only" % key, shot=shot_id)


def check_plan_origin(doc: dict[str, Any], shot: dict[str, Any],
                      problems: Problems) -> None:
    plan = doc.get("plan") or {}
    current = str(plan.get("id") or "").strip()
    origin = str(shot.get("origin_plan") or "").strip()
    if current and origin and origin != current:
        problems.warn("PLAN001", "shot reuses old plan %r; re-check its bindings against %r"
                      % (origin, current), shot=str(shot.get("id") or "?"))


def check_seams(doc: dict[str, Any], shots_by_id: dict[str, dict[str, Any]],
                problems: Problems) -> None:
    seams = doc.get("seams")
    if seams is None:
        return
    if not isinstance(seams, list):
        problems.error("SEAM001", "seams must be a list")
        return
    seen: set[str] = set()
    for index, raw in enumerate(seams):
        if not isinstance(raw, dict):
            problems.error("SEAM002", "seam must be a mapping")
            continue
        kind = str(raw.get("kind") or "").strip().lower()
        join = str(raw.get("join") or "").strip().lower()
        if kind not in SEAM_KINDS:
            problems.error("SEAM003", "seam kind must be inner or inter")
            continue
        if join not in SEAM_JOINS:
            problems.error("SEAM004", "seam join must be one of %s"
                           % ", ".join(sorted(SEAM_JOINS)))
            continue
        reason = str(raw.get("reason") or "").strip().lower()
        if reason and reason not in SEAM_REASONS:
            problems.error("SEAM019", "seam reason must be one of %s"
                           % ", ".join(sorted(SEAM_REASONS)))
        for key in SEAM_PROSE_KEYS:
            if key in raw:
                problems.error("SEAM020", "seam.%s is prose; use note_ref" % key)
        seam_id = str(raw.get("id") or "").strip()
        if seam_id:
            if seam_id in seen:
                problems.error("SEAM005", "duplicate seam id %s" % seam_id)
            seen.add(seam_id)
        if kind == "inner":
            if raw.get("from") is not None or raw.get("to") is not None:
                problems.error("SEAM006", "inner seam uses shot, not from/to")
            shot_id = str(raw.get("shot") or "").strip()
            shot = shots_by_id.get(shot_id)
            if shot is None:
                problems.error("SEAM007", "seam references unknown shot %r" % shot_id)
                continue
            if str(shot.get("technique") or "").strip().lower() != "multishot":
                problems.error("SEAM008", "inner seam is only valid for multishot")
                continue
            at_frame = positive_int(raw.get("at_frame"))
            per = positive_int((shot.get("submit") or {}).get("frames_per_shot"))
            if at_frame is None:
                problems.error("SEAM009", "inner seam needs a positive at_frame")
            elif per is not None and at_frame != per:
                problems.error("SEAM010", "inner at_frame must equal frames_per_shot (%s)"
                               % per)
            if join != "continuous":
                problems.error("SEAM011", "inner seam join must be continuous")
            if raw.get("gap_seconds") is not None:
                problems.error("SEAM012", "inner seam does not take gap_seconds")
        else:
            from_id = str(raw.get("from") or "").strip()
            to_id = str(raw.get("to") or "").strip()
            if not from_id or not to_id:
                problems.error("SEAM013", "inter seam needs from and to")
                continue
            if from_id == to_id:
                problems.error("SEAM014", "inter seam from and to must differ")
                continue
            if from_id not in shots_by_id or to_id not in shots_by_id:
                problems.error("SEAM007", "seam references unknown shot")
                continue
            if join == "continuous":
                problems.error("SEAM015", "inter seam cannot be continuous")
            gap = raw.get("gap_seconds")
            if gap is not None:
                try:
                    gapf = float(gap)
                except (TypeError, ValueError):
                    problems.error("SEAM016", "gap_seconds must be a number")
                else:
                    if gapf < 0:
                        problems.error("SEAM016", "gap_seconds must be >= 0")
            if join == "interval" and gap is None:
                problems.error("SEAM017", "interval seam needs gap_seconds")
            if join == "hard_cut" and reason in ("", "none"):
                from_scene = str((shots_by_id[from_id].get("group") or {}).get("scene") or "")
                to_scene = str((shots_by_id[to_id].get("group") or {}).get("scene") or "")
                if from_scene and from_scene == to_scene:
                    problems.error(
                        "SEAM021",
                        "同一场（%s）里的硬切必须写明理由：刻意分镜覆盖写 coverage_cut，"
                        "有时间跳跃写 time_jump，有动作/声音/身份承接写对应的 *_bridge。"
                        "接缝阶梯第 1 步是「能连续就连续」，硬切不是同场的默认。"
                        % from_scene)
            for sid in (from_id, to_id):
                if str(shots_by_id[sid].get("status") or "active").strip().lower() == "archived":
                    problems.warn("SEAM018", "seam touches archived shot %s" % sid)


def _as_number(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def check_ref_path(root: Path, value: Any, problems: Problems,
                   feature: str, shot: str | None = None,
                   allow_anchor: bool = True) -> None:
    if value in (None, ""):
        return
    path_text, _, anchor = str(value).partition("#")
    try:
        path = project_path(root, path_text)
    except ValueError as exc:
        problems.error(feature, str(exc), shot=shot)
        return
    if not path.is_file():
        problems.error(feature, "referenced file missing: %s" % path_text, shot=shot)
        return
    if allow_anchor and anchor and anchor not in path.read_text(
            encoding="utf-8", errors="replace"):
        problems.error(feature, "anchor %r not found in %s" % (anchor, path_text),
                       shot=shot)


def check_ledger_keyframe(root: Path, shot_id: str, kf: Any, assets: dict[str, Any],
                          timecode: Any, problems: Problems) -> str | None:
    if not isinstance(kf, dict):
        problems.error("LEDGER030", "keyframe must be a mapping", shot=shot_id)
        return None
    kf_id = str(kf.get("id") or "").strip()
    if not kf_id:
        problems.error("LEDGER030", "keyframe.id is required", shot=shot_id)
    elif not LEDGER_ID_RE.match(kf_id):
        problems.error("LEDGER031", "keyframe.id has invalid format: %r" % kf_id,
                       shot=shot_id)
    img_id = kf.get("img_id")
    if img_id is not None and not LEDGER_ID_RE.match(str(img_id)):
        problems.error("LEDGER031", "keyframe.img_id has invalid format: %r" % img_id,
                       shot=shot_id)
    role = str(kf.get("role") or "").strip().lower()
    if role not in KEYFRAME_ROLES:
        problems.error("LEDGER032", "keyframe.role must be one of %s"
                       % ", ".join(sorted(KEYFRAME_ROLES)), shot=shot_id)
    at_s = _as_number(kf.get("at_s"))
    if at_s is None:
        problems.error("LEDGER033", "keyframe.at_s must be a number", shot=shot_id)
    elif at_s < 0:
        problems.error("LEDGER033", "keyframe.at_s must not be negative", shot=shot_id)
    elif isinstance(timecode, dict):
        # `at_s` is the instant inside its own shot: the same clock the shot's
        # `### 观众 reads` windows use. Comparing it against the episode-level
        # `timecode` would reject a legal frame whose shot simply starts later.
        start = _as_number(timecode.get("in_s"))
        end_v = _as_number(timecode.get("out_s"))
        if start is not None and end_v is not None and at_s > (end_v - start):
            problems.error(
                "LEDGER033",
                "keyframe.at_s %.3f is past the end of its shot (%.3fs long)"
                % (at_s, end_v - start),
                shot=shot_id,
            )
    asset_ref = kf.get("asset")
    if asset_ref not in (None, ""):
        resolve_asset(assets, str(asset_ref), problems)
    media_state = str(kf.get("media_state") or "").strip().lower()
    if media_state and media_state not in MEDIA_STATES:
        problems.error("LEDGER034", "keyframe.media_state must be one of %s"
                       % ", ".join(sorted(MEDIA_STATES)), shot=shot_id)
    audit = str(kf.get("audit") or "").strip().lower()
    if audit and audit not in AUDIT_LEVELS:
        problems.error("LEDGER034", "keyframe.audit must be core or optional", shot=shot_id)
    use = str(kf.get("use") or "").strip().lower()
    if use and use not in KEYFRAME_USES:
        problems.error("LEDGER035", "keyframe.use must be one of %s"
                       % ", ".join(sorted(KEYFRAME_USES)), shot=shot_id)
    check_ref_path(root, kf.get("prompt_ref"), problems, "LEDGER036", shot_id)
    basis_refs = kf.get("basis_refs")
    if basis_refs is not None:
        if not isinstance(basis_refs, list):
            problems.error("LEDGER037", "basis_refs must be a list", shot=shot_id)
        else:
            for ref in basis_refs:
                text = str(ref)
                if text.split("@")[0].startswith(("ASSET-", "ASSET_")):
                    resolve_asset(assets, text, problems)
                elif not text.startswith(("LOCK-", "VF-", "CARD-")):
                    problems.error("LEDGER037",
                                   "basis_refs must be ASSET-*/LOCK-*/VF-*/CARD-*: %r"
                                   % text, shot=shot_id)
    check_ref_path(root, kf.get("basis_note_ref"), problems, "LEDGER038", shot_id)
    check_ref_path(root, kf.get("control_ref"), problems, "LEDGER039", shot_id)
    proves_reads = kf.get("proves_reads")
    if proves_reads is not None:
        if not isinstance(proves_reads, list):
            problems.error("LEDGER040", "proves_reads must be a list", shot=shot_id)
        else:
            for read_id in proves_reads:
                if not re.match(r"^R\d+$", str(read_id)):
                    problems.error("LEDGER040", "proves_reads entry must be R<n>: %r"
                                   % read_id, shot=shot_id)
    evidence_refs = kf.get("evidence_refs")
    if evidence_refs is not None:
        if not isinstance(evidence_refs, list):
            problems.error("LEDGER041", "evidence_refs must be a list", shot=shot_id)
        else:
            for ref in evidence_refs:
                check_ref_path(root, ref, problems, "LEDGER041", shot_id)
    anchor = kf.get("anchor")
    if anchor is not None and not isinstance(anchor, bool):
        problems.error("LEDGER042", "keyframe.anchor must be a boolean", shot=shot_id)
    decision_refs = kf.get("decision_refs")
    if decision_refs is not None:
        if not isinstance(decision_refs, list):
            problems.error("LEDGER043", "decision_refs must be a list", shot=shot_id)
        else:
            for ref in decision_refs:
                check_ref_path(root, ref, problems, "LEDGER043", shot_id, False)
    for prose_key in ("basis", "controls", "note"):
        if isinstance(kf.get(prose_key), str):
            problems.error("LEDGER002",
                           "keyframe.%s is prose; use basis_note_ref/control_ref/evidence_refs"
                           % prose_key, shot=shot_id)
    return kf_id or None


def check_ledger(root: Path, doc: dict[str, Any],
                 shots_by_id: dict[str, dict[str, Any]], assets: dict[str, Any],
                 problems: Problems) -> None:
    active: list[dict[str, Any]] = []
    seen_kf: set[str] = set()
    seen_img: set[str] = set()
    seen_motion: set[str] = set()
    for raw in doc.get("shots") or []:
        if not isinstance(raw, dict):
            continue
        if str(raw.get("status") or "active").strip().lower() == "archived":
            continue
        active.append(raw)
        shot_id = str(raw.get("id") or "?")
        check_ref_path(root, raw.get("doc_path"), problems, "LEDGER003", shot_id, False)
        for field in ("doc_id", "img_doc", "motion_doc"):
            check_ref_path(root, raw.get(field), problems, "LEDGER045", shot_id,
                           field == "doc_id")
        timecode = raw.get("timecode")
        if timecode is not None:
            if not isinstance(timecode, dict):
                problems.error("LEDGER004", "timecode must be a mapping", shot=shot_id)
            else:
                start = _as_number(timecode.get("in_s"))
                end_v = _as_number(timecode.get("out_s"))
                if start is None or end_v is None:
                    problems.error("LEDGER004", "timecode.in_s/out_s must be numbers",
                                   shot=shot_id)
                elif end_v <= start:
                    problems.error("LEDGER004", "timecode.out_s must be > in_s",
                                   shot=shot_id)
                if "note" in timecode:
                    problems.error("LEDGER002", "timecode.note is prose; move it to 审查/",
                                   shot=shot_id)
        group = raw.get("group")
        if group is not None:
            if not isinstance(group, dict):
                problems.error("LEDGER005", "group must be a mapping", shot=shot_id)
            else:
                scene = str(group.get("scene") or "").strip()
                if scene and not SCENE_ID_RE.match(scene):
                    problems.error("LEDGER005", "group.scene must be EPxxx-SCxxx: %r"
                                   % scene, shot=shot_id)
                mode = str(group.get("mode") or "").strip().lower()
                if mode and mode not in GROUP_MODES:
                    problems.error("LEDGER005", "group.mode must be one of %s"
                                   % ", ".join(sorted(GROUP_MODES)), shot=shot_id)
                reason = str(group.get("seam_reason") or "").strip().lower()
                if reason and reason not in SEAM_REASONS:
                    problems.error("LEDGER005", "group.seam_reason must be one of %s"
                                   % ", ".join(sorted(SEAM_REASONS)), shot=shot_id)
                check_ref_path(root, group.get("note_ref"), problems, "LEDGER005",
                               shot_id)
        if "reference_note" in raw:
            problems.error("LEDGER002",
                           "reference_note is prose; use reference_assets", shot=shot_id)
        reference_assets = raw.get("reference_assets")
        if reference_assets is not None:
            if not isinstance(reference_assets, list):
                problems.error("LEDGER006", "reference_assets must be a list", shot=shot_id)
            else:
                for ref in reference_assets:
                    resolve_asset(assets, str(ref), problems)
        motion_id = raw.get("motion_id")
        if motion_id:
            text = str(motion_id)
            if not LEDGER_ID_RE.match(text):
                problems.error("LEDGER007", "motion_id has invalid format: %r" % text,
                               shot=shot_id)
            elif text in seen_motion:
                problems.error("LEDGER007", "duplicate motion_id %s" % text, shot=shot_id)
            seen_motion.add(text)
        for field in ("img_ids", "kf_ids"):
            values = raw.get(field)
            if values is None:
                continue
            if not isinstance(values, list):
                problems.error("LEDGER007", "%s must be a list" % field, shot=shot_id)
                continue
            for item in values:
                text = str(item)
                if not LEDGER_ID_RE.match(text):
                    problems.error("LEDGER007", "%s has invalid id: %r" % (field, text),
                                   shot=shot_id)
                elif field == "img_ids" and text in seen_img:
                    problems.error("LEDGER007", "duplicate img_id %s" % text, shot=shot_id)
                elif field == "kf_ids" and text in seen_kf:
                    problems.error("LEDGER007", "duplicate kf_id %s" % text, shot=shot_id)
                if field == "img_ids":
                    seen_img.add(text)
                else:
                    seen_kf.add(text)
        keyframes = raw.get("keyframes")
        if keyframes is not None:
            if not isinstance(keyframes, list):
                problems.error("LEDGER030", "keyframes must be a list", shot=shot_id)
            else:
                local_ids: set[str] = set()
                for kf in keyframes:
                    kf_id = check_ledger_keyframe(root, shot_id, kf, assets, timecode,
                                                 problems)
                    if kf_id:
                        if kf_id in local_ids:
                            problems.error("LEDGER031", "duplicate keyframe id %s" % kf_id,
                                           shot=shot_id)
                        local_ids.add(kf_id)
        for prose_key in ("basis", "proves", "controls", "note"):
            if isinstance(raw.get(prose_key), str):
                problems.error("LEDGER002",
                               "shot.%s is prose; use keyframes/decisions", shot=shot_id)

    for item in doc.get("decisions") or []:
        if not isinstance(item, dict):
            problems.error("LEDGER046", "decision must be a mapping")
            continue
        did = str(item.get("id") or "").strip()
        if not did or not LEDGER_ID_RE.match(did):
            problems.error("LEDGER046", "decision id invalid: %r" % did)
        for key in ("subject", "field", "value"):
            if not isinstance(item.get(key), str) or not str(item.get(key)).strip():
                problems.error("LEDGER046", "decision.%s is required" % key)
        alternatives = item.get("alternatives")
        if alternatives is not None:
            if not isinstance(alternatives, list):
                problems.error("LEDGER046", "decision.alternatives must be a list")
            else:
                for alt in alternatives:
                    if not isinstance(alt, str):
                        problems.error("LEDGER046",
                                       "decision.alternatives entries must be strings")
        reason = str(item.get("reason_code") or "").strip().lower()
        if reason not in DECISION_REASON_CODES:
            problems.error("LEDGER046", "decision.reason_code must be one of %s"
                           % ", ".join(sorted(DECISION_REASON_CODES)))
        status = str(item.get("status") or "").strip().lower()
        if status not in DECISION_STATUSES:
            problems.error("LEDGER046", "decision.status must be accepted/pending/rejected")
        refs = item.get("refs")
        if refs is not None:
            if not isinstance(refs, list):
                problems.error("LEDGER046", "decision.refs must be a list")
            else:
                for ref in refs:
                    check_ref_path(root, ref, problems, "LEDGER046")

    for item in doc.get("conflicts") or []:
        if not isinstance(item, dict):
            problems.error("LEDGER047", "conflict must be a mapping")
            continue
        cid = str(item.get("id") or "").strip()
        if not cid or not LEDGER_ID_RE.match(cid):
            problems.error("LEDGER047", "conflict id invalid: %r" % cid)
        shot_id = str(item.get("shot") or "").strip()
        if shot_id and shot_id not in shots_by_id:
            problems.error("LEDGER047", "conflict references unknown shot %r" % shot_id)
        field = item.get("field")
        if not isinstance(field, str) or not field.strip():
            problems.error("LEDGER047", "conflict.field is required")
        values = item.get("values")
        if not isinstance(values, list) or not values:
            problems.error("LEDGER047", "conflict.values must be a non-empty list")
        else:
            for value in values:
                if not isinstance(value, str):
                    problems.error("LEDGER047", "conflict.values entries must be strings")
        status = str(item.get("status") or "").strip().lower()
        if status not in CONFLICT_STATUSES:
            problems.error("LEDGER047", "conflict.status must be unresolved/resolved/accepted")
        refs = item.get("refs")
        if refs is not None:
            if not isinstance(refs, list):
                problems.error("LEDGER047", "conflict.refs must be a list")
            else:
                for ref in refs:
                    check_ref_path(root, ref, problems, "LEDGER047")

    for item in doc.get("drift") or []:
        if not isinstance(item, dict):
            problems.error("LEDGER048", "drift must be a mapping")
            continue
        did = str(item.get("id") or "").strip()
        if not did or not LEDGER_ID_RE.match(did):
            problems.error("LEDGER048", "drift id invalid: %r" % did)
        kind = str(item.get("kind") or "").strip().lower()
        if kind not in DRIFT_KINDS:
            problems.error("LEDGER048", "drift.kind must be one of %s"
                           % ", ".join(sorted(DRIFT_KINDS)))
        status = str(item.get("status") or "").strip().lower()
        if status not in DRIFT_STATUSES:
            problems.error("LEDGER048", "drift.status must be unresolved/resolved/accepted")
        refs = item.get("refs")
        if not isinstance(refs, list) or len(refs) < 2:
            problems.error("LEDGER048", "drift.refs must list at least two paths")
        else:
            for ref in refs:
                check_ref_path(root, ref, problems, "LEDGER048")

    for seam in doc.get("seams") or []:
        if not isinstance(seam, dict):
            continue
        check_ref_path(root, seam.get("note_ref"), problems, "LEDGER049")
        check_ref_path(root, seam.get("reason_detail_ref"), problems, "LEDGER049")

    qc = doc.get("qc")
    if qc is not None:
        if not isinstance(qc, dict):
            problems.error("LEDGER011", "qc must be a mapping")
        else:
            status = str(qc.get("status") or "").strip().lower()
            if status and status not in QC_STATUSES:
                problems.error("LEDGER011", "qc.status must be pass/fail/pending")
            checks = qc.get("checks")
            if not isinstance(checks, list) or not checks:
                problems.error("LEDGER012", "qc.checks must be a non-empty list")
            else:
                for check in checks:
                    if not isinstance(check, dict):
                        problems.error("LEDGER012", "qc.checks entries must be mappings")
                        continue
                    cid = str(check.get("id") or "").strip()
                    if not cid or not LEDGER_ID_RE.match(cid):
                        problems.error("LEDGER012", "qc.checks id invalid: %r" % cid)
                    cstatus = str(check.get("status") or "").strip().lower()
                    if cstatus not in QC_CHECK_STATUSES:
                        problems.error("LEDGER012",
                                       "qc.checks status must be pass/fail/pending/unverified")
                    evidence = check.get("evidence_ref")
                    if evidence:
                        check_ref_path(root, evidence, problems, "LEDGER012")
                    elif cstatus == "pass":
                        problems.error("LEDGER012",
                                       "qc.checks %s is pass but has no evidence_ref" % cid)
            ref = qc.get("ref")
            if ref:
                check_ref_path(root, ref, problems, "LEDGER011")


def validate_manifest(root: Path, doc: dict[str, Any],
                      allow_missing_hash: bool = False,
                      allow_unadmitted: bool = False) -> Problems:
    problems = Problems()
    if not isinstance(doc, dict):
        problems.error("DOC001", "manifest must be a mapping")
        return problems
    if doc.get("schema") not in {"shot-manifest/v1", "shot_manifest/v1"}:
        problems.error("DOC002", "schema must be shot-manifest/v1")
    plan = doc.get("plan")
    if not isinstance(plan, dict) or not plan.get("id"):
        problems.error("DOC003", "plan.id is required")
    else:
        plan_status = str(plan.get("status") or "active").strip().lower()
        if plan_status not in PLAN_STATUSES:
            problems.error("DOC013", "plan.status must be active or archived")
        elif plan_status == "archived":
            problems.warn("PLAN002", "plan is archived; plan commands will refuse it")
    project = doc.get("project")
    if not isinstance(project, dict) or not project.get("id"):
        problems.error("DOC004", "project.id is required")
    canvas = doc.get("canvas")
    if not isinstance(canvas, dict):
        problems.error("DOC005", "canvas is required")
    else:
        width = positive_int(canvas.get("width"))
        height = positive_int(canvas.get("height"))
        if width is None or height is None:
            problems.error("DOC006", "canvas.width/height must be positive integers")
        else:
            if width % 32 or height % 32:
                problems.error("DOC007", "canvas.width/height must be multiples of 32")
            aspect = str(canvas.get("declared_aspect") or "").strip()
            if aspect:
                try:
                    [int(part) for part in aspect.split(":")]
                except ValueError:
                    problems.error("DOC008", "canvas.declared_aspect must be W:H")
    assets = doc.get("assets")
    if not isinstance(assets, dict):
        problems.error("DOC010", "assets must be a mapping")
        assets = {}
    check_asset_files(root, assets, problems, allow_missing_hash, allow_unadmitted,
                      used_asset_ids(doc))
    shots = doc.get("shots")
    if not isinstance(shots, list) or not shots:
        problems.error("DOC011", "shots must be a non-empty list")
        return problems
    seen_ids: set[str] = set()
    shots_by_id: dict[str, dict[str, Any]] = {}
    for raw in shots:
        if not isinstance(raw, dict):
            problems.error("DOC012", "shot must be a mapping")
            continue
        shot_id = str(raw.get("id") or "?")
        if shot_id in seen_ids:
            problems.error("SHOT010", "duplicate shot id %s" % shot_id, shot=shot_id)
        seen_ids.add(shot_id)
        shots_by_id[shot_id] = raw
        status = str(raw.get("status") or "active").strip().lower()
        if status not in SHOT_STATUSES:
            problems.error("SHOT014", "shot.status must be active or archived",
                           shot=shot_id, field="status")
            continue
        if status == "archived":
            problems.warn("SHOT015", "archived shot skipped", shot=shot_id)
            continue
        technique = str(raw.get("technique") or "").strip().lower()
        if technique not in TECHNIQUES:
            problems.error("SHOT011", "unknown technique %r" % technique, shot=shot_id,
                           field="technique")
            continue
        bindings = check_bindings(root, raw, assets, problems)
        check_technique(raw, bindings, problems)
        check_prompt(root, raw, bindings, problems)
        check_submit(raw, bindings, problems)
        check_plan_origin(doc, raw, problems)
    check_seams(doc, shots_by_id, problems)
    check_ledger(root, doc, shots_by_id, assets, problems)
    return problems


def build_plan(root: Path, doc: dict[str, Any], shot_id: str) -> dict[str, Any]:
    shots = {str(shot.get("id")): shot for shot in doc.get("shots") or []
             if isinstance(shot, dict)}
    shot = shots.get(shot_id)
    if shot is None:
        raise SystemExit("shot_manifest: unknown shot %r" % shot_id)
    if str(shot.get("status") or "active").strip().lower() == "archived":
        raise SystemExit("shot_manifest: shot %r is archived" % shot_id)
    plan_status = str((doc.get("plan") or {}).get("status") or "active").strip().lower()
    if plan_status == "archived":
        raise SystemExit("shot_manifest: plan is archived")
    technique = str(shot.get("technique") or "").strip().lower()
    problems = Problems()
    bindings = check_bindings(root, shot, doc.get("assets") or {}, problems)
    if problems.errors:
        render_problems(problems, False)
        raise SystemExit(1)
    submit = shot.get("submit") or {}
    workflow = str(submit.get("workflow") or DEFAULT_WORKFLOW.get(technique, "")).strip().lower()
    width = positive_int(submit.get("width")) or 0
    height = positive_int(submit.get("height")) or 0
    frames = positive_int(shot.get("frames"))
    prompt = str(shot.get("prompt") or "")
    labels = [label for binding in bindings for label in binding_labels(binding)]
    prompt_labels = [label for label in labels if label.startswith("<Picture")]
    refs = sorted([b for b in bindings if "ref_slot" in b], key=lambda b: b["ref_slot"])
    ref_names = [str(b["asset_id"]) for b in refs]
    scene_videos = [b for b in bindings if binding_role(b) == "scene_video"]
    gate: list[str] | None = None
    if technique != "motion_drive":
        mode = "multishot" if technique == "multishot" else (
            "base" if technique in {"i2va", "fl2va", "t2va"} else "ref")
        gate = [
            "python3",
            str(Path(__file__).resolve().parents[4] / "h3-video-gate/scripts/h3_gate.py"),
            prompt,
            "--mode", mode,
        ]
        if technique == "multishot":
            shot_count = positive_int(submit.get("shot_count"))
            frames_per_shot = positive_int(submit.get("frames_per_shot"))
            if shot_count:
                gate += ["--shot-count", str(shot_count)]
            if frames_per_shot:
                gate += ["--frames", str(frames_per_shot)]
            gate += ["--refs", str(len(refs))]
        else:
            if frames:
                gate += ["--frames", str(frames)]
            gate += ["--refs", str(len(prompt_labels))]
        if submit.get("gate_rate") is not None:
            gate += ["--rate", str(submit["gate_rate"])]
    notes: list[str] = []
    submit_argv: list[str] | None = None
    remote_prompt = submit.get("remote_prompt") or "<REMOTE_PROMPT:%s>" % prompt
    remote_refs = submit.get("remote_refs") or {}
    if technique == "motion_drive":
        notes.append("motion_drive 不走 h3q；按 h3-queue/references/video-motion-drive.md 直投 ComfyUI。")
    else:
        submit_argv = ["h3qc", "submit", "--kind", "video", "--prompt-file", str(remote_prompt),
                       "--width", str(width), "--height", str(height)]
        if workflow == "multishot":
            shot_count = positive_int(submit.get("shot_count")) or 0
            frames_per_shot = positive_int(submit.get("frames_per_shot")) or 0
            submit_argv += ["--workflow", "multishot",
                            "--shot-count", str(shot_count),
                            "--frames-per-shot", str(frames_per_shot),
                            "--reference-subjects", str(submit.get("reference_subjects") or "")]
            if submit.get("reference_image_size") is not None:
                submit_argv += ["--reference-image-size", str(submit["reference_image_size"])]
            if submit.get("auto_chunk_ffn") is not None:
                submit_argv += ["--auto-chunk-ffn", str(submit.get("auto_chunk_ffn"))]
            if refs:
                names = [remote_refs.get(name, "<REMOTE_REF:%s>" % name) for name in ref_names]
                submit_argv += ["--refs", ",".join(names)]
            if scene_videos:
                binding = scene_videos[0]
                scene_path = remote_refs.get(binding["asset_id"], "<REMOTE_CLIP:%s>" % binding["asset_id"])
                submit_argv += ["--scene-video", str(scene_path)]
                if binding.get("start") is not None:
                    submit_argv += ["--scene-video-start", str(binding["start"])]
                if binding.get("seconds") is not None:
                    submit_argv += ["--scene-video-seconds", str(binding["seconds"])]
            for key, flag in (("voice_ref", "--voice-ref"), ("voice_ref_2", "--voice-ref-2")):
                if submit.get(key):
                    submit_argv += [flag, str(submit[key])]
        elif workflow == "pdd_lu":
            submit_argv += ["--workflow", "pdd_lu", "--no-upscale"]
            if frames:
                submit_argv += ["--frames", str(frames)]
            if ref_names:
                names = [remote_refs.get(name, "<REMOTE_REF:%s>" % name) for name in ref_names]
                submit_argv += ["--refs", ",".join(names)]
        elif technique == "fl2va":
            first = next((b for b in bindings if binding_role(b) == "first_frame"), None)
            last = next((b for b in bindings if binding_role(b) == "last_frame"), None)
            if first:
                submit_argv += ["--first-frame", str(remote_refs.get(first["asset_id"], "<REMOTE_REF:%s>" % first["asset_id"]))]
            if last:
                submit_argv += ["--last-frame", str(remote_refs.get(last["asset_id"], "<REMOTE_REF:%s>" % last["asset_id"]))]
            if frames:
                submit_argv += ["--frames", str(frames)]
        elif technique == "i2va":
            first = next((b for b in bindings if binding_role(b) == "first_frame"), None)
            if first:
                submit_argv += ["--first-frame", str(remote_refs.get(first["asset_id"], "<REMOTE_REF:%s>" % first["asset_id"]))]
            if frames:
                submit_argv += ["--frames", str(frames)]
        else:
            if frames:
                submit_argv += ["--frames", str(frames)]
            if ref_names:
                names = [remote_refs.get(name, "<REMOTE_REF:%s>" % name) for name in ref_names]
                submit_argv += ["--refs", ",".join(names)]
        if submit.get("idem_key"):
            submit_argv += ["--idem-key", str(submit["idem_key"])]
        if submit.get("seed") is not None:
            submit_argv += ["--seed", str(submit["seed"])]
        if technique == "frame_ref2va":
            notes.append("frame_ref2va 的 semantic first_frame 是词稿语义，不传 --first-frame；provider 仍按 --refs 送图。")
        if "<REMOTE_" in " ".join(submit_argv):
            notes.append("提交命令里的 <REMOTE_...> 是远端占位符；按投递单把 Windows 侧 ASCII 路径填进去。")
    return {
        "shot": shot_id,
        "technique": technique,
        "workflow": workflow,
        "gate": gate,
        "submit": submit_argv,
        "notes": notes,
    }


def render_problems(problems: Problems, as_json: bool) -> None:
    if as_json:
        print(json.dumps({"errors": problems.errors, "warnings": problems.warnings},
                         ensure_ascii=False, indent=2))
        return
    for item in problems.errors:
        location = "shot %s" % item.get("shot") if item.get("shot") else ""
        field = " field %s" % item.get("field") if item.get("field") else ""
        print("[ERROR] %s %s%s: %s" % (item["code"], location, field, item["message"]))
    for item in problems.warnings:
        location = "shot %s" % item.get("shot") if item.get("shot") else ""
        field = " field %s" % item.get("field") if item.get("field") else ""
        print("[WARN]  %s %s%s: %s" % (item["code"], location, field, item["message"]))
    print("summary: %s error(s), %s warning(s)" % (len(problems.errors), len(problems.warnings)))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="shot_manifest.py")
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a shot manifest")
    validate.add_argument("project")
    validate.add_argument("--manifest", required=True)
    validate.add_argument("--json", action="store_true")
    validate.add_argument("--allow-missing-hash", action="store_true")
    validate.add_argument("--allow-unadmitted", action="store_true")

    plan = sub.add_parser("plan", help="print gate/submit commands for one shot")
    plan.add_argument("project")
    plan.add_argument("--manifest", required=True)
    plan.add_argument("--shot", required=True)
    plan.add_argument("--json", action="store_true")
    plan.add_argument("--allow-unadmitted", action="store_true")

    args = parser.parse_args(argv)
    root = Path(args.project).resolve()
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = root / manifest
    if not manifest.is_file():
        print("shot_manifest: manifest not found: %s" % manifest, file=sys.stderr)
        return 2
    try:
        doc = load_document(manifest)
    except (OSError, json.JSONDecodeError) as exc:
        print("shot_manifest: cannot read manifest: %s" % exc, file=sys.stderr)
        return 2
    except SystemExit:
        raise
    if args.command == "validate":
        problems = validate_manifest(root, doc, args.allow_missing_hash,
                                     args.allow_unadmitted)
        render_problems(problems, args.json)
        return 1 if problems.errors else 0
    problems = validate_manifest(root, doc, False, args.allow_unadmitted)
    if problems.errors:
        render_problems(problems, args.json)
        return 1
    result = build_plan(root, doc, args.shot)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print("shot: %s  technique: %s  workflow: %s" % (result["shot"], result["technique"], result["workflow"]))
        if result["gate"]:
            print("gate: " + " ".join(result["gate"]))
        if result["submit"]:
            print("submit: " + " ".join(result["submit"]))
        for note in result["notes"]:
            print("note: " + note)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
