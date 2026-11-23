#!/usr/bin/env python3
"""Offline self-test for confirmation-gated production and provider profiles."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

from production_tool import (
    ConfirmationRequiredError,
    _markdown_reference_bindings,
    _read_job,
    _validate_stored_job,
    audit_project,
    job_status,
    confirm_job,
    prepare_job,
    run_job,
)
from provider_adapters import (
    compile_gpt_image_2_payload,
    compile_minimax_music_payload,
    compile_seedance_payload,
)

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("selftest.py requires Python 3.9 or newer")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def check_creator_image_roundtrips(project: Path, config: Path) -> None:
    episode = project / "剧集/EP001"
    episode.mkdir(parents=True, exist_ok=True)
    cases = (
        ("分镜.md", "SHOT-SELFTEST-001", "SHOT-SELFTEST-001#KF-SELFTEST-001-START", "起始帧提示词", "输入参考图", "IMG-WRONG"),
        ("图片提示词.md", "IMG-SELFTEST-001", "IMG-SELFTEST-001", "可复制提示词", "参考", "SHOT-WRONG"),
    )
    for filename, entry, selector, heading, reference_field, wrong_entry in cases:
        source = episode / filename
        frame_plan = ""
        if filename == "分镜.md":
            frame_plan = (
                "### 画面证明计划\n\n| Frame | role | read | 时刻 | 证明责任 | 生产/审查用途 |\n"
                "|---|---|---|---|---|---|\n"
                "| KF-SELFTEST-001-START | start | R1 | 0.0s | 起态 | 首帧生产 |\n\n"
            )
        source.write_text(
            f"# Test\n\n## {entry} · Test\n- {reference_field}：无。\n\n"
            f"{frame_plan}### {heading}\n> An original test frame.\n",
            encoding="utf-8",
        )
        job = {
            "job_id": f"SELFTEST-{entry}", "modality": "image", "adapter": "fixture",
            "prompt": "An original test frame.",
            "source": source.relative_to(project).as_posix(), "source_entry": selector,
            "reference_bindings": [], "references": [],
            "outputs": [f"剧集/EP001/制作成果/images/{entry}.png"],
            "parameters": {}, "overwrite": False,
        }
        job_path = project / f"{entry}.json"
        job_path.write_text(json.dumps(job), encoding="utf-8")
        preview = prepare_job(project, job_path)
        confirm_job(project, job_id=job["job_id"], confirmation=preview["confirmation"])
        run_job(project, job_id=job["job_id"], adapter_config=config)
        require(job_status(project, job_id=job["job_id"])["state"] == "succeeded",
                f"{filename} image job did not round-trip through stored validation")
        stored = _read_job(project, job["job_id"])
        try:
            _validate_stored_job(project, {**stored, "source_entry": wrong_entry})
        except ValueError as exc:
            require("wrong modality" in str(exc), "wrong source entry failed at an unrelated check")
        else:
            raise AssertionError(f"{filename} accepted the wrong source-entry prefix")
    require(audit_project(project)["status"] == "pass", "creator image fixture audit failed")

    # A valid creator selector must not weaken the confirmed-input snapshot check.
    stale = dict(job)
    stale.update(job_id="SELFTEST-STALE-IMAGE", outputs=["剧集/EP001/制作成果/images/stale.png"])
    stale_path = project / "stale-image.json"
    stale_path.write_text(json.dumps(stale), encoding="utf-8")
    preview = prepare_job(project, stale_path)
    confirm_job(project, job_id=stale["job_id"], confirmation=preview["confirmation"])
    source.write_text(source.read_text(encoding="utf-8") + "\nChanged source.\n", encoding="utf-8")
    try:
        run_job(project, job_id=stale["job_id"], adapter_config=config)
    except ConfirmationRequiredError as exc:
        require("job inputs changed" in str(exc), "stale input failed at an unrelated check")
    else:
        raise AssertionError("changed confirmed source reached the fixture adapter")
    require(not (project / stale["outputs"][0]).exists(), "stale input produced an output")


def main() -> int:
    with tempfile.TemporaryDirectory() as directory:
        base = Path(directory)
        project = base / "project"
        project.mkdir()
        (project / "short-drama.json").write_text("{}\n", encoding="utf-8")
        (project / "输入").mkdir()
        (project / "输入/look-baseline.png").write_bytes(b"baseline")
        (project / "视觉设定.md").write_text(
            "# 项目视觉设定\n\n## 画风基准\n\n- LOOK-SELFTEST：输入/look-baseline.png《自测基准》\n"
            "- 认可依据：自测夹具。\n",
            encoding="utf-8",
        )
        job_path = project / "music-job.json"
        job: dict[str, Any] = {
            "job_id": "SELFTEST-MUSIC-001",
            "modality": "music",
            "adapter": "fixture",
            "prompt": "restrained instrumental tension",
            "references": [],
            "outputs": ["剧集/EP001/制作成果/music/cue.wav"],
            "parameters": {"is_instrumental": True},
            "overwrite": False,
        }
        job_path.write_text(json.dumps(job), encoding="utf-8")
        config = base / "adapters.json"
        fixture = Path(__file__).with_name("fixture_adapter.py")
        config.write_text(
            json.dumps(
                {
                    "adapters": {
                        "fixture": {
                            "command": [sys.executable, str(fixture)],
                            "timeout_seconds": 30,
                        }
                    }
                }
            ),
            encoding="utf-8",
        )

        preview = prepare_job(project, job_path)
        try:
            confirm_job(project, job_id=job["job_id"], confirmation="CONFIRM wrong")
        except ConfirmationRequiredError:
            pass
        else:
            raise AssertionError("a mismatched production confirmation was accepted")
        confirm_job(
            project,
            job_id=job["job_id"],
            confirmation=preview["confirmation"],
        )
        result = run_job(project, job_id=job["job_id"], adapter_config=config)
        require(result["state"] == "succeeded", "fixture production did not succeed")
        require(
            (project / job["outputs"][0]).read_bytes().startswith(b"RIFF"),
            "fixture production did not write WAV media",
        )
        check_creator_image_roundtrips(project, config)

    require(
        compile_gpt_image_2_payload(
        {
            "modality": "image",
            "prompt": "portrait",
            "references": [],
            "outputs": ["制作成果/portrait.png"],
            "parameters": {"size": "1024x1024"},
        }
        )["model"]
        == "gpt-image-2",
        "GPT Image 2 profile compiled the wrong model",
    )
    seedance = compile_seedance_payload(
        {
            "modality": "video",
            "prompt": "slow push in",
            "references": [],
            "outputs": ["制作成果/shot.mp4"],
            "parameters": {"duration": 5, "ratio": "9:16"},
        },
        model="configured-endpoint",
        allowed_ratios={"9:16"},
        duration_range=(5, 10),
    )
    require(
        seedance.get("ratio") == "9:16" and seedance.get("duration") == 5,
        "Seedance profile did not compile explicit API parameters",
    )
    require(
        compile_minimax_music_payload(
        {
            "modality": "music",
            "prompt": "restrained score",
            "references": [],
            "outputs": ["制作成果/cue.mp3"],
            "parameters": {"is_instrumental": True},
        }
        )["model"]
        == "music-3.0",
        "MiniMax Music profile compiled the wrong model",
    )

    section = "- 输入参考图：REF-CHAR（顺序：1）· 输入/char.png《角色》（用途：身份；控制：脸型；不得控制：构图）；待补参考图：本镜起始帧"
    declared = _markdown_reference_bindings(section, field_name="输入参考图", pending_ok=True)
    require(len(declared) == 1 and declared[0]["slot_id"] == "REF-CHAR",
            "keyframe pending-start declaration was rejected")
    try:
        _markdown_reference_bindings(section, field_name="输入参考图", pending_ok=False)
    except ValueError:
        pass
    else:
        raise AssertionError("pending references leaked into a non-keyframe job")

    print("16 self-tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
