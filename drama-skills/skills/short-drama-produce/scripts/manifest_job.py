#!/usr/bin/env python3
"""Build a production_tool job JSON from a shot-manifest/v1 entry.

This is the bridge between the 2026-11-25 one-file contract and the existing
prepare/confirm/run tool.  It only reads the manifest and the prompt file; it
does not submit anything.  Run ``production_tool.py prepare`` on the output.

    python3 manifest_job.py <project> --manifest <制作清单.yaml> --shot <id> \
        [--job-id <id>] [--output <job.json>]
    python3 manifest_job.py <project> --manifest <制作清单.yaml> --keyframe <KF-id> \
        [--job-id <id>] [--output <job.json>]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any

try:
    import yaml
except Exception as exc:  # pragma: no cover
    raise SystemExit(f"manifest_job.py needs PyYAML: {exc}")


MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit(
        "manifest_job.py requires Python {}.{}, running {}.{}".format(
            *MINIMUM_PYTHON, sys.version_info.major, sys.version_info.minor
        )
    )

JOB_ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,79}$")
MULTISHOT = "multishot"


def relative_path(value: object) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("path must be a non-empty string")
    pure = PurePosixPath(value.replace("\\", "/"))
    if pure.is_absolute() or any(part in {"", ".", ".."} for part in pure.parts):
        raise ValueError(f"unsafe project path: {value}")
    return pure.as_posix()


def load_manifest(path: Path) -> dict[str, Any]:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        raise ValueError("manifest top level must be a mapping")
    if document.get("schema") != "shot-manifest/v1":
        raise ValueError("manifest schema must be shot-manifest/v1")
    return document


def asset_paths(manifest: dict[str, Any]) -> dict[str, str]:
    """Resolve asset id (with or without @version) to a project-relative path."""
    result: dict[str, str] = {}
    assets = manifest.get("assets") or {}
    if not isinstance(assets, dict):
        raise ValueError("manifest assets must be a mapping")
    for asset_id, asset in assets.items():
        if not isinstance(asset, dict):
            continue
        versions = asset.get("versions")
        if versions is None and asset.get("path"):
            versions = [asset]
        if not isinstance(versions, list) or not versions:
            continue
        by_version = {}
        latest = None
        for version in versions:
            if not isinstance(version, dict) or not version.get("path"):
                continue
            path = relative_path(version["path"])
            number = version.get("version")
            if isinstance(number, int):
                by_version[number] = path
            latest = path
        if latest is None:
            continue
        result[str(asset_id)] = latest
        for number, path in by_version.items():
            result[f"{asset_id}@{number}"] = path
    return result


def binding_role(binding: dict[str, Any]) -> str:
    role = str(binding.get("role") or "").strip().lower()
    if role in {"identity", "scene", "prop"}:
        return "reference_image"
    if role in {"first_frame", "last_frame"}:
        return role
    semantic = str(binding.get("semantic") or "").strip().lower()
    if semantic == "first_frame":
        return "first_frame"
    if semantic == "last_frame":
        return "last_frame"
    if role:
        return role
    return "reference_image"


def asset_kinds(manifest: dict[str, Any]) -> dict[str, str]:
    result: dict[str, str] = {}
    for asset_id, asset in (manifest.get("assets") or {}).items():
        if isinstance(asset, dict):
            result[str(asset_id)] = str(asset.get("kind") or "").strip().lower()
    return result


def asset_labels(manifest: dict[str, Any]) -> dict[str, str]:
    labels: dict[str, str] = {}
    for asset_id, asset in (manifest.get("assets") or {}).items():
        if not isinstance(asset, dict):
            continue
        label = asset.get("label") or asset.get("roles_hint") or asset.get("note") or "参考"
        labels[str(asset_id)] = str(label)
    return labels


def default_controls(kind: str) -> list[str]:
    return {
        "identity": ["identity", "face", "character"],
        "scene": ["scene_layout", "lighting"],
        "prop": ["prop_shape"],
        "style": ["style"],
    }.get(kind, ["reference_image"])


def default_must_not_control(kind: str) -> list[str]:
    return {
        "identity": ["composition", "lighting"],
        "scene": ["identity"],
        "prop": ["composition"],
        "style": ["composition"],
    }.get(kind, ["composition"])


def find_keyframe(
    manifest: dict[str, Any], keyframe_id: str
) -> tuple[dict[str, Any], dict[str, Any], str]:
    for shot in manifest.get("shots") or []:
        if not isinstance(shot, dict):
            continue
        if str(shot.get("status") or "active").strip().lower() == "archived":
            continue
        for keyframe in shot.get("keyframes") or []:
            if isinstance(keyframe, dict) and str(keyframe.get("id")) == keyframe_id:
                return shot, keyframe, str(shot.get("shot_id") or shot.get("id") or "")
    raise ValueError(f"keyframe not found: {keyframe_id}")


def build_image_job(
    manifest: dict[str, Any],
    keyframe_id: str,
    job_id: str | None = None,
    project: Path | None = None,
) -> dict[str, Any]:
    shot, keyframe, stable_shot = find_keyframe(manifest, keyframe_id)
    prompt_path = relative_path(keyframe.get("prompt_ref"))
    prompt_file = (project or Path.cwd()) / prompt_path
    if not prompt_file.is_file():
        raise ValueError(f"prompt file does not exist: {prompt_path}")
    prompt = prompt_file.read_text(encoding="utf-8")
    if not prompt.strip():
        raise ValueError(f"prompt file is empty: {prompt_path}")

    paths = asset_paths(manifest)
    kinds = asset_kinds(manifest)
    labels = asset_labels(manifest)
    references: list[str] = []
    reference_bindings: list[dict[str, Any]] = []
    for index, asset_id in enumerate(keyframe.get("basis_refs") or [], 1):
        asset_id = str(asset_id)
        path = paths.get(asset_id)
        if path is None:
            continue
        kind = kinds.get(asset_id.split("@", 1)[0], "")
        slot = re.sub(r"[^A-Za-z0-9-]+", "-", asset_id.split("@", 1)[0]).strip("-").upper()
        reference_bindings.append({
            "slot_id": f"REF-{slot}",
            "order": index,
            "path": path,
            "label": labels.get(asset_id.split("@", 1)[0], "参考"),
            "role": "reference_image",
            "may_control": default_controls(kind),
            "must_not_control": default_must_not_control(kind),
        })
        references.append(path)
    if not references:
        raise ValueError(f"keyframe {keyframe_id} has no resolvable basis_refs")

    submit = shot.get("submit") or {}
    width = submit.get("width") or manifest.get("canvas", {}).get("width")
    height = submit.get("height") or manifest.get("canvas", {}).get("height")
    if not isinstance(width, int) or width <= 0 or not isinstance(height, int) or height <= 0:
        raise ValueError("manifest/shot needs positive width and height")
    parameters: dict[str, Any] = {"width": width, "height": height}
    if submit.get("seed") is not None:
        parameters["seed"] = submit["seed"]

    output = None
    if keyframe.get("asset"):
        output = paths.get(str(keyframe["asset"]))
    if not output:
        episode = str((manifest.get("project") or {}).get("episode") or "").strip()
        if not episode:
            raise ValueError("keyframe has no asset path and project.episode is missing")
        output = f"剧集/{episode}/制作成果/起始帧/{keyframe_id}.png"
    output = relative_path(output)
    project_id = str((manifest.get("project") or {}).get("id") or "project")
    identifier = job_id or f"{project_id}-{keyframe_id}-image"
    identifier = re.sub(r"[^A-Za-z0-9._-]+", "-", identifier).strip("-")
    if JOB_ID_RE.fullmatch(identifier) is None:
        raise ValueError(f"invalid job id: {identifier!r}")
    return {
        "schema_version": "1.0",
        "job_id": identifier,
        "modality": "image",
        "adapter": "local-h3q-image",
        "prompt": prompt,
        "source": prompt_path,
        "references": references,
        "reference_bindings": reference_bindings,
        "outputs": [output],
        "parameters": parameters,
        "overwrite": False,
    }


def build_job(
    manifest: dict[str, Any],
    shot_id: str,
    job_id: str | None = None,
    project: Path | None = None,
) -> dict[str, Any]:
    shots = manifest.get("shots") or []
    if not isinstance(shots, list):
        raise ValueError("manifest shots must be a list")
    shot = next(
        (item for item in shots if isinstance(item, dict) and str(item.get("id")) == shot_id),
        None,
    )
    if shot is None:
        raise ValueError(f"shot not found: {shot_id}")
    if str(shot.get("status") or "active").strip().lower() == "archived":
        raise ValueError(f"shot is archived: {shot_id}")

    prompt_path = relative_path(shot.get("prompt"))
    prompt_file = (project or Path.cwd()) / prompt_path
    if not prompt_file.is_file():
        raise ValueError(f"prompt file does not exist: {prompt_path}")
    prompt = prompt_file.read_text(encoding="utf-8")
    if not prompt.strip():
        raise ValueError(f"prompt file is empty: {prompt_path}")

    technique = str(shot.get("technique") or "").strip().lower()
    if technique == "motion_drive":
        raise ValueError(
            "motion_drive does not go through production_tool/h3q; "
            "use h3-queue/references/video-motion-drive.md"
        )
    submit = shot.get("submit") or {}
    if not isinstance(submit, dict):
        raise ValueError("shot.submit must be a mapping")
    workflow = str(submit.get("workflow") or ("multishot" if technique == MULTISHOT else "ref2va"))
    # adapter 的 VIDEO_WORKFLOWS 是 ref2va / multishot / fl2va 三种。
    # 早期这里只放行前两种，导致首尾帧镜头在建 job 阶段就被挡住，
    # 而 adapter 本身能跑——清单合法、通道支持、中间层拒绝。
    if workflow not in {"ref2va", "multishot", "fl2va"}:
        raise ValueError(
            f"production_tool adapter supports ref2va/multishot/fl2va, got {workflow!r}"
        )

    paths = asset_paths(manifest)
    bindings = shot.get("bindings") or []
    if not isinstance(bindings, list):
        raise ValueError("shot.bindings must be a list")
    references: list[str] = []
    reference_bindings: list[dict[str, Any]] = []
    ordered = sorted(
        (b for b in bindings if isinstance(b, dict) and b.get("ref_slot") is not None),
        key=lambda b: int(b["ref_slot"]),
    )
    for binding in ordered:
        asset_id = str(binding.get("asset") or "")
        path = paths.get(asset_id)
        if path is None:
            raise ValueError(f"binding asset has no file path: {asset_id}")
        role = binding_role(binding)
        if role not in {"reference_image", "first_frame", "last_frame"}:
            raise ValueError(
                f"binding role {role!r} is not accepted by the local h3q adapter; "
                "use h3qc direct for scene_video/audio"
            )
        slot = re.sub(r"[^A-Za-z0-9-]+", "-", asset_id.split("@", 1)[0]).strip("-").upper()
        reference_bindings.append({
            "slot_id": f"REF-{slot}",
            "order": int(binding["ref_slot"]),
            "path": path,
            "label": str(binding.get("label") or asset_id),
            "role": role,
            "may_control": list(binding.get("may_control") or ["identity"]),
            "must_not_control": list(binding.get("must_not_control") or []),
        })
        references.append(path)

    width = submit.get("width") or manifest.get("canvas", {}).get("width")
    height = submit.get("height") or manifest.get("canvas", {}).get("height")
    if not isinstance(width, int) or width <= 0 or not isinstance(height, int) or height <= 0:
        raise ValueError("manifest/submit needs positive width and height")

    parameters: dict[str, Any] = {
        "workflow": workflow,
        "width": width,
        "height": height,
        "engine": str(submit.get("engine") or "pdd"),
        "tier": str(submit.get("tier") or "draft"),
    }
    if workflow == MULTISHOT:
        per = submit.get("frames_per_shot")
        count = submit.get("shot_count")
        if not isinstance(per, int) or per <= 0:
            raise ValueError("multishot needs frames_per_shot")
        if per < 5 or (per - 5) % 17:
            raise ValueError("multishot frames_per_shot must be 17k+5 (e.g. 345), got %s" % per)
        if not isinstance(count, int) or count < 2:
            raise ValueError("multishot needs shot_count >= 2")
        parameters["frames_per_shot"] = per
        parameters["shot_count"] = count
        parameters["reference_subjects"] = str(submit.get("reference_subjects") or "1")
        parameters["reference_image_size"] = str(submit.get("reference_image_size") or "match")
        if submit.get("auto_chunk_ffn") is not None:
            parameters["auto_chunk_ffn"] = submit["auto_chunk_ffn"]
        # local-h3q-video 通道要求 duration 显式给出（它把 frames 换成秒），
        # 多窗分支之前漏了这一步，prepare 会拒「duration must explicitly match」。
        # 多窗总时长是 shot 的 frames / fps，不是单窗时长。
        total = shot.get("frames")
        if isinstance(total, int) and total > 0:
            parameters["duration"] = round(total / 24.0, 6)
    else:
        frames = shot.get("frames")
        if not isinstance(frames, int) or frames <= 0:
            raise ValueError("single-shot job needs positive frames")
        parameters["frames"] = frames
        parameters["duration"] = round(frames / 24.0, 6)
    for key in ("seed", "voice_ref", "voice_ref_2", "same_scene_continuous", "scene_anchor_index"):
        if key in submit:
            parameters[key] = submit[key]

    output = submit.get("output")
    if not output:
        episode = str((manifest.get("project") or {}).get("episode") or "").strip()
        if not episode:
            raise ValueError("submit.output is missing and project.episode cannot name a default")
        stable_id = str(shot.get("shot_id") or shot.get("id") or shot_id).strip()
        output = f"剧集/{episode}/制作成果/{stable_id}.mp4"
    output = relative_path(output)
    identifier = job_id or str(submit.get("idem_key") or f"{manifest.get('project', {}).get('id', 'project')}-{shot_id}")
    identifier = re.sub(r"[^A-Za-z0-9._-]+", "-", identifier).strip("-")
    if JOB_ID_RE.fullmatch(identifier) is None:
        raise ValueError(f"invalid job id: {identifier!r}")
    return {
        "schema_version": "1.0",
        "job_id": identifier,
        "modality": "video",
        "adapter": "local-h3q-video",
        "prompt": prompt,
        "source": prompt_path,
        "references": references,
        "reference_bindings": reference_bindings,
        "outputs": [output],
        "parameters": parameters,
        "overwrite": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    selector = parser.add_mutually_exclusive_group(required=True)
    selector.add_argument("--shot")
    selector.add_argument("--keyframe")
    parser.add_argument("--job-id")
    parser.add_argument("--output", type=Path, help="write job JSON here; default stdout")
    args = parser.parse_args()
    project = args.project.resolve()
    manifest_path = args.manifest if args.manifest.is_absolute() else project / args.manifest
    try:
        manifest = load_manifest(manifest_path)
        if args.keyframe:
            job = build_image_job(manifest, args.keyframe, args.job_id, project)
        else:
            job = build_job(manifest, args.shot, args.job_id, project)
    except (OSError, ValueError, KeyError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    payload = json.dumps(job, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(payload, encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        sys.stdout.write(payload)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
