#!/usr/bin/env python3
"""Run the exact frozen H3 checker and retain per-attempt evidence. No network."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
from datetime import datetime, timezone


def _sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def run_archived_gate(prompt: Path, checker: Path, destination: Path,
                      arguments: list[str], *, context: dict | None = None, runner=None):
    """A unique destination is mandatory; an earlier attempt is never overwritten.

    The checker is a standalone Python script. Freeze it and its optional series
    configuration before execution, and upload destination/prompt.txt afterwards.
    """
    prompt_bytes, checker_bytes = prompt.read_bytes(), checker.read_bytes()
    destination.mkdir(parents=True, exist_ok=False)
    frozen_prompt = destination / "prompt.txt"
    frozen_checker = destination / "h3_gate.py"
    frozen_prompt.write_bytes(prompt_bytes)
    frozen_checker.write_bytes(checker_bytes)
    args = list(arguments)
    files = {"prompt.txt": _sha(prompt_bytes), "h3_gate.py": _sha(checker_bytes)}
    if "--series-config" in args:
        index = args.index("--series-config") + 1
        series = Path(args[index]).read_bytes()
        frozen_series = destination / "series-config.json"
        frozen_series.write_bytes(series)
        files[frozen_series.name] = _sha(series)
        args[index] = str(frozen_series)
    command = [sys.executable, str(frozen_checker), str(frozen_prompt), *args]
    manifest = {"schema": "h3-gate-evidence/1", "created_at": datetime.now(timezone.utc).isoformat(),
                "files": files, "checker_source": str(checker.resolve()), "argv": command,
                "context": context or {}, "state": "checking"}
    manifest_path = destination / "manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    try:
        result = (runner(command, check=False) if runner else subprocess.run(
            command, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120))
    except Exception as exc:
        manifest.update(state="checker_error", error=type(exc).__name__)
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
        raise
    stdout, stderr = getattr(result, "stdout", "") or "", getattr(result, "stderr", "") or ""
    try:
        report = json.loads(stdout)
    except json.JSONDecodeError:
        report = {"invalid_json": True, "stdout": stdout}
    report_bytes = json.dumps(report, ensure_ascii=False, indent=2).encode()
    (destination / "gate-report.json").write_bytes(report_bytes)
    (destination / "gate-stderr.txt").write_text(stderr)
    files.update({"gate-report.json": _sha(report_bytes), "gate-stderr.txt": _sha(stderr.encode())})
    manifest.update(state="checked", exit_code=result.returncode)
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    return result
