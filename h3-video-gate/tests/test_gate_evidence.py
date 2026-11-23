import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import hashlib

SCRIPT = Path(__file__).resolve().parents[1] / "scripts/gate_evidence.py"
spec = importlib.util.spec_from_file_location("gate_evidence", SCRIPT)
evidence = importlib.util.module_from_spec(spec)
spec.loader.exec_module(evidence)


class GateEvidenceTests(unittest.TestCase):
    def test_freezes_executed_checker_and_prompt_even_when_original_changes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt, checker, dest = root / "source.txt", root / "checker.py", root / "run-1"
            prompt.write_text("actual submitted prompt")
            original = 'import json; print(json.dumps({"version": "a", "summary": {"errors": 0}}))'
            checker.write_text(original)
            def racing_runner(command, check=False):
                checker.write_text('raise SystemExit(9)')
                prompt.write_text("later edit")
                return subprocess.run(command, capture_output=True, text=True)
            result = evidence.run_archived_gate(prompt, checker, dest, ["--json"], runner=racing_runner)
            self.assertEqual(result.returncode, 0)
            self.assertEqual(json.loads((dest / "gate-report.json").read_text())["version"], "a")
            self.assertEqual((dest / "prompt.txt").read_text(), "actual submitted prompt")
            manifest = json.loads((dest / "manifest.json").read_text())
            self.assertEqual(manifest["files"]["h3_gate.py"], hashlib.sha256(original.encode()).hexdigest())
            with self.assertRaises(FileExistsError):
                evidence.run_archived_gate(prompt, checker, dest, ["--json"])
            self.assertEqual(json.loads((dest / "gate-report.json").read_text())["version"], "a")

    def test_failed_gate_and_series_config_remain_available(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            prompt, checker, series = root / "source.txt", root / "checker.py", root / "series.json"
            prompt.write_text("bad input")
            checker.write_text('import json; print(json.dumps({"findings": [{"rule": "G30"}]})); raise SystemExit(1)')
            series.write_text('{"character": "fixed"}')
            dest = root / "attempt"
            result = evidence.run_archived_gate(prompt, checker, dest, ["--json", "--series-config", str(series)])
            self.assertEqual(result.returncode, 1)
            self.assertEqual(json.loads((dest / "manifest.json").read_text())["exit_code"], 1)
            self.assertEqual((dest / "series-config.json").read_bytes(), series.read_bytes())
            self.assertEqual(json.loads((dest / "gate-report.json").read_text())["findings"][0]["rule"], "G30")


if __name__ == "__main__":
    unittest.main()
