"""Shared reference acceptance evidence used by produce, adapters and MCP."""
# SYNC NOTE: keep in sync with short-drama-produce/scripts/ref_gate.py;
# any behavior change must be applied to both copies.
from __future__ import annotations

import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Mapping

# cast_gate lives next to this file in both distributions (review and the
# standalone produce copy). Loading by __file__ keeps it available when the
# gate is imported by an MCP server that has no scripts/ on sys.path.
_CAST_PATH = Path(__file__).with_name("cast_gate.py")
_cast_spec = importlib.util.spec_from_file_location("cast_gate_shared", _CAST_PATH)
if _cast_spec is None or _cast_spec.loader is None:
    raise SystemExit(f"cast gate module missing: {_CAST_PATH}")
_cast_gate = importlib.util.module_from_spec(_cast_spec)
_cast_spec.loader.exec_module(_cast_gate)

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("ref_gate needs Python {}.{} or newer".format(*MINIMUM_PYTHON))

SCHEMA = "ref-gate/1"
GENERATED_MARKERS = (b"tEXtprompt", b"tEXtworkflow", b"iTXtprompt")
LOOK_LINE = re.compile(r"^-\s*LOOK-[A-Za-z0-9_-]+\s*[：:]\s*(.+?)《")
BASIS_LINE = re.compile(r"^-\s*认可依据\s*[：:]\s*\S")
VISUAL_SETTINGS = ("视觉设定.md", "剧集/*/视觉设定.md")

# 设计资产与镜头帧不是同一种东西，验收维度不同：
# 角色卡/场景卡/道具卡/分镜板验的是"身份与版面是否锁定"，镜头帧验的是"这一帧能不能用"。
# 设计资产没有剧情层，也没有 scene comparability 可比较，不该被镜头帧的判据挡住。
DESIGN_ASSETS = {"character-card", "scene-card", "prop-card", "storyboard"}

# 同场连续（multishot 两窗共享机位）声明的地理/构图锚与身份锚用途词表。
# 只看 reference_bindings 的 may_control / must_not_control，不猜文件名或 label。
SCENE_CONTROL_TERMS = (
    "场景", "构图", "取景", "地理", "环境", "空间", "机位", "布景", "陈设", "布局", "位置",
    "scene", "composition", "geography", "environment", "layout",
    "setting", "staging", "camera", "framing",
)
IDENTITY_CONTROL_TERMS = (
    "身份", "人物", "角色", "脸", "骨相", "造型", "服装", "发型", "体型",
    "identity", "character", "face", "likeness", "wardrobe", "costume", "hair",
)


class InputError(ValueError):
    pass


def relative_path(value: object) -> str:
    if not isinstance(value, str):
        raise InputError("project paths must be strings")
    pure = PurePosixPath(value.replace("\\", "/"))
    if (not value or pure.is_absolute()
            or any(part in {"", ".", ".."} for part in pure.parts)):
        raise InputError(f"unsafe project-relative path: {value}")
    return pure.as_posix()


def project_file(root: Path, relative: str) -> Path:
    target = root.joinpath(*PurePosixPath(relative).parts)
    resolved_root = root.resolve()
    if target.is_symlink() or not target.is_file():
        raise InputError(f"job input is not a regular file: {relative}")
    if not target.resolve().is_relative_to(resolved_root):
        raise InputError(f"job input escapes project root: {relative}")
    return target


def sha256_file(root: Path, relative: str) -> str:
    digest = hashlib.sha256()
    with project_file(root, relative).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def generated_path(relative: str) -> bool:
    parts = PurePosixPath(relative).parts
    return (
        len(parts) >= 4
        and parts[0] in {"剧集", "episodes"}
        and parts[2] in {"制作成果", "production"}
    ) or (len(parts) >= 2 and parts[0].casefold() == "production")


def produced_digests(root: Path) -> set[str]:
    digests: set[str] = set()
    runs = root / ".short-drama" / "production" / "runs"
    if not runs.is_dir():
        return digests
    for record in runs.glob("*/*.json"):
        try:
            document = json.loads(record.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        for output in document.get("outputs") or []:
            digest = output.get("sha256") if isinstance(output, dict) else None
            if isinstance(digest, str):
                digests.add(digest)
    return digests


def looks_generated(root: Path, relative: str, digest: str, produced: set[str]) -> bool:
    if generated_path(relative) or digest in produced:
        return True
    try:
        with project_file(root, relative).open("rb") as handle:
            head = handle.read(256 * 1024)
    except (OSError, InputError):
        return False
    return any(marker in head for marker in GENERATED_MARKERS)


def registered_baselines(root: Path) -> set[str]:
    found: set[str] = set()
    documents = sorted(root.glob("视觉设定.md")) + sorted(root.glob("剧集/*/视觉设定.md"))
    for document in documents:
        in_section, paths, basis = False, [], False
        for line in document.read_text(encoding="utf-8").splitlines() + ["## END"]:
            if line.startswith("## "):
                if in_section and basis:
                    found.update(paths)
                in_section = line.strip().startswith("## 画风基准")
                paths, basis = [], False
                continue
            if not in_section:
                continue
            match = LOOK_LINE.match(line.strip())
            if match:
                paths.append(PurePosixPath(match.group(1).strip()).as_posix())
            elif BASIS_LINE.match(line.strip()):
                basis = True
    return found


def latest_review(report: Mapping[str, Any]) -> Mapping[str, Any]:
    history = report.get("reviews")
    if isinstance(history, list) and history:
        last = history[-1]
        return last if isinstance(last, Mapping) else {}
    legacy = report.get("visual_review")
    return legacy if isinstance(legacy, Mapping) else {}


def look_report(root: Path, relative: str) -> Path:
    return root / "审查" / "look" / f"{relative}.look.json"


def reference_problem(root: Path, relative: str, digest: str,
                      asset_kind: str = "frame",
                      _ancestors: set[str] | None = None) -> str | None:
    try:
        report = json.loads(look_report(root, relative).read_text(encoding="utf-8"))
    except FileNotFoundError:
        return (
            "no look report — this image has never been through short-drama-review. "
            "Run: look_check.py assess <project> --media <path> --scope reference --reviewer <name>; "
            "then look_check.py review ... approve; only then can it be used as a reference."
        )
    except (OSError, json.JSONDecodeError):
        return "unreadable look_check report"
    if not isinstance(report, dict) or report.get("media") != relative:
        return "look_check report belongs to another file"
    if report.get("media_sha256") != digest:
        return "file changed after its look_check"
    review = latest_review(report)
    if ((report.get("mechanical") or {}).get("verdict") == "FAIL"
            and not (review.get("status") == "approved" and review.get("creator_ack")
                     and review.get("mechanical_override"))):
        return "look_check verdict is FAIL"
    # 两条来源都认：报告自己写了 kind=asset（look_check --kind asset 的产物），
    # 或调用方显式声明 asset_kind。都没有就按镜头帧审。
    design_asset = (report.get("kind") == "asset") or (asset_kind in DESIGN_ASSETS)
    if not design_asset and report.get("comparison", {}).get("status") == "unknown":
        return "scene comparability has not been reviewed"
    if (report.get("measurement_id") and review.get("measurement_id")
            and review["measurement_id"] != report["measurement_id"]):
        return "comparison evidence changed after approval"
    if review.get("status") != "approved":
        return f"latest review is {review.get('status') or 'pending'}, not approved"
    allowed_use = {"reference", "design"} if design_asset else {"reference"}
    if review.get("use") not in allowed_use:
        if design_asset:
            return (f"use is {review.get('use')}, expected reference or design "
                    f"for a {asset_kind} asset")
        return "approved for edit only, not for reuse as a reference"
    if not design_asset and not review.get("story_pass"):
        return "story layer was not passed"
    if review.get("self_review") and not review.get("creator_ack"):
        return "self-review needs the creator's --creator-ack before reuse"
    parent = report.get("derived_from")
    if isinstance(parent, str) and parent:
        problem = _derived_reference_problem(
            root, parent, relative, set(_ancestors or ()))
        if problem:
            return problem
    return None


def _derived_reference_problem(root: Path, parent: str, child_relative: str,
                               seen: set[str]) -> str | None:
    """An ancestor must currently qualify as a reference, not merely be approved.

    A derived frame (a relay tail frame, a crop, a re-encode) inherits its
    acceptance from the media it was taken from: that parent must still be the
    same bytes on disk, hold the current measurement, and carry an approved
    reference use with its story layer — the same standard the child itself
    just passed. The chain is walked recursively; cycles and unreadable
    ancestors fail closed instead of riding on an old approval.
    """
    if parent in seen or parent == child_relative:
        return f"derived_from chain cycles at {parent}"
    try:
        parent_digest = sha256_file(root, parent)
    except (InputError, OSError) as exc:
        return (f"derived from {parent}, whose current bytes cannot be read ({exc}); "
                f"the parent media must be present and unchanged")
    problem = reference_problem(root, parent, parent_digest, "frame", seen | {child_relative})
    if problem:
        return f"derived from {parent}: {problem}"
    return None


def result(allowed: bool, code: str, message: str,
           references: list[dict] | None = None, **extra: Any) -> dict:
    return {"schema": SCHEMA, "allowed": allowed, "code": code,
            "message": message, "references": references or [], **extra}


def _explicit_truth(value: object, label: str) -> bool:
    """Parse the explicit same-scene opt-in; anything else is a caller error."""
    if value in (None, ""):
        return False
    if value is True:
        return True
    if value is False:
        return False
    if isinstance(value, str):
        text = value.strip().lower()
        if text in ("true", "1", "yes"):
            return True
        if text in ("false", "0", "no"):
            return False
    raise InputError(f"{label} must be a boolean, got {value!r}")


def _binding_controls(binding: Mapping[str, Any], terms: tuple[str, ...]) -> bool:
    """The binding declares one of `terms` and does not deny it."""
    may = binding.get("may_control") or []
    must = binding.get("must_not_control") or []

    def hits(values: object) -> bool:
        folded = [str(item).casefold() for item in values] if isinstance(values, (list, tuple)) else []
        return any(term.casefold() in value for term in terms for value in folded)

    return hits(may) and not hits(must)


def _same_scene_contract(parameters: Mapping[str, Any],
                         bindings: list[Mapping[str, Any]]) -> None:
    """multishot 同场连续的可选合同。

    只在显式 same_scene_continuous=true 且 workflow=multishot 时生效：要求
    至少一张身份参考，并用明确的 scene_anchor_index 指向已准入的地理/构图锚。
    换场/硬切不声明该参数，行为完全不变；非 multishot 显式 true 直接拒绝。
    """
    explicit = _explicit_truth(parameters.get("same_scene_continuous"),
                               "same_scene_continuous")
    index = parameters.get("scene_anchor_index")
    if not explicit:
        if index not in (None, ""):
            raise InputError(
                "scene_anchor_index may only be used with same_scene_continuous=true")
        return
    workflow = str(parameters.get("workflow") or "").strip().lower()
    if workflow != "multishot":
        raise InputError(
            "same_scene_continuous only applies to workflow=multishot; "
            "a scene change or hard cut must not declare it")
    if not bindings:
        raise InputError(
            "same_scene_continuous=true requires explicit reference_bindings with "
            "may_control/must_not_control, so the scene anchor and identity reference "
            "can be verified")
    if parameters.get("scene_video"):
        # 场景锚也可以是上一镜成片的片段（reference_video / H3ReferenceVideo）。
        # 这条路不把场景图塞进人物参考：记忆采样器会把 reference_images 里的
        # 每张图声明成 <Subject N> 的照片，场景图会占掉一个人物名额。
        if index not in (None, ""):
            raise InputError(
                "scene_video and scene_anchor_index are mutually exclusive: use the "
                "clip as the scene anchor, or point at a reference image, not both")
        identity = any(
            isinstance(binding, Mapping)
            and binding.get("role") == "reference_image"
            and _binding_controls(binding, IDENTITY_CONTROL_TERMS)
            for binding in bindings
        )
        if not identity:
            raise InputError(
                "same_scene_continuous=true with scene_video still requires an identity "
                "reference: the clip carries room/framing/light, not who the character is")
        return
    if index in (None, ""):
        raise InputError(
            "same_scene_continuous=true requires scene_anchor_index: the 1-based "
            "position of the accepted scene/composition anchor in reference_bindings")
    if isinstance(index, bool) or not isinstance(index, int) or not 1 <= index <= len(bindings):
        raise InputError(
            "scene_anchor_index must be the 1-based position of a reference in "
            f"reference_bindings (got {index!r}, {len(bindings)} bindings)")
    anchor = bindings[index - 1]
    if (not isinstance(anchor, Mapping)
            or anchor.get("role") != "reference_image"
            or not _binding_controls(anchor, SCENE_CONTROL_TERMS)):
        raise InputError(
            "scene_anchor_index points at a reference that does not declare a "
            "scene/composition control scope (may_control); bind the accepted "
            "scene plate or start frame as reference_image and declare its 用途")
    identity = any(
        isinstance(binding, Mapping)
        and binding.get("role") == "reference_image"
        and _binding_controls(binding, IDENTITY_CONTROL_TERMS)
        for position, binding in enumerate(bindings, 1)
        if position != index
    )
    if not identity:
        raise InputError(
            "same_scene_continuous=true also requires an identity reference: another "
            "reference_image whose may_control names 身份/人物/脸/造型 (and does not "
            "deny it). A scene anchor alone cannot carry character consistency")


def check(root: Path, references: list[str], *, modality: str,
          parameters: Mapping[str, Any] | None = None,
          bindings: list[Mapping[str, Any]] | None = None) -> dict:
    parameters = parameters or {}
    if modality not in ("image", "video"):
        return result(True, "not_applicable", "look gate applies to image/video only")
    try:
        # A root that is not a directory can declare no baseline and read no
        # report; reporting `missing_look_baseline` for it used to name a
        # look-dev problem the caller cannot fix by registering one.
        if not root.is_dir():
            raise InputError(f"project root is not a directory: {root}")
        references = [relative_path(item) for item in references]
        _same_scene_contract(parameters, list(bindings or []))
        asset_kind = str(parameters.get("asset_kind") or "frame")
        # 设计资产本身就是"确立画风基准的东西"，不能反过来要求项目先有基准。
        design_declared = asset_kind in DESIGN_ASSETS
        baselines = registered_baselines(root)
        if not baselines and not parameters.get("no_look_baseline_ack") and not design_declared:
            return result(False, "missing_look_baseline",
                          "project has no creator-accepted look baseline with an 认可依据 line; "
                          "declaring asset_kind=character-card/scene-card/prop-card/storyboard "
                          "skips this requirement because design assets define the baseline")
        produced = produced_digests(root)
        checked = []
        for relative in references:
            if relative in baselines:
                checked.append({"path": relative, "status": "baseline"})
                continue
            digest = sha256_file(root, relative)
            if not looks_generated(root, relative, digest, produced):
                checked.append({"path": relative, "status": "creator_original"})
                continue
            problem = reference_problem(root, relative, digest,
                                        str(parameters.get("asset_kind") or "frame"))
            if problem:
                return result(False, "reference_not_accepted",
                              f"generated reference {relative} is not accepted for reuse ({problem})",
                              checked)
            checked.append({"path": relative, "status": "accepted", "sha256": digest})
        # 角色卡漏挂是"带齐了但带错"之外的另一类错：参考图逐张都合法，却整组
        # 没有一张身份板。设计资产本身就是在造身份板，lookdev 首跑也还没有
        # 可带的板，两者豁免；其余 image/video job 都过这道覆盖检查。
        cast_outcome = None
        if not design_declared and not parameters.get("no_look_baseline_ack"):
            exempt = parameters.get("cast_exempt")
            cast_outcome = _cast_gate.check(
                bindings or references,
                cast=parameters.get("cast"),
                cast_aliases=parameters.get("cast_aliases"),
                cast_required=bool(parameters.get("cast_required")),
                cast_exempt=exempt if isinstance(exempt, str) else None,
            )
            if cast_outcome["status"] in ("fail", "error"):
                return result(False, cast_outcome.get("code") or "cast_coverage_failed",
                              cast_outcome["message"], checked, cast=cast_outcome)
        return result(True, "accepted", "references accepted", checked,
                      cast=cast_outcome)
    except (InputError, OSError, UnicodeError) as exc:
        return result(False, "input_error", str(exc))


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Shared reference acceptance gate")
    sub = parser.add_subparsers(dest="command", required=True)
    check_parser = sub.add_parser("check")
    check_parser.add_argument("--project-root", required=True)
    check_parser.add_argument("--modality", required=True, choices=("image", "video", "tts", "music"))
    check_parser.add_argument("--references", nargs="*", default=[])
    check_parser.add_argument("--parameters", default="{}",
                              help="JSON object, e.g. no_look_baseline_ack for explicit lookdev")
    check_parser.add_argument("--bindings", default="[]",
                              help="JSON array of {path,label,may_control} bindings, "
                                   "so the cast gate can read identity control scope")
    args = parser.parse_args(argv)
    try:
        parameters = json.loads(args.parameters)
        bindings = json.loads(args.bindings)
        if not isinstance(parameters, dict):
            raise ValueError("parameters must be a JSON object")
        if not isinstance(bindings, list) or any(not isinstance(b, dict) for b in bindings):
            raise ValueError("bindings must be a JSON array of objects")
        outcome = check(Path(args.project_root), args.references,
                        modality=args.modality, parameters=parameters,
                        bindings=bindings or None)
    except (ValueError, json.JSONDecodeError) as exc:
        outcome = result(False, "input_error", str(exc))
    print(json.dumps(outcome, ensure_ascii=False, sort_keys=True))
    return 0 if outcome["allowed"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
