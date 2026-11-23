#!/usr/bin/env python3
"""h3_lint 时间戳与台词时长检查的回归测试。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import h3_lint


H3_LINT = Path(__file__).resolve().parent / "h3_lint.py"


class H3LintRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_prompt(self, text):
        path = self.root / "prompt.txt"
        path.write_text(text, encoding="utf-8")
        return path

    def test_at_night_is_not_a_timestamp(self):
        text = "[Shot 1] At night, the room is quiet."
        self.assertEqual(h3_lint.check_shot_timing(text), [])
        path = self.write_prompt(text)
        self.assertEqual(h3_lint.lint(path)["status"], "PASS")

    def test_real_shot_one_timestamp_is_rejected(self):
        issues = h3_lint.check_shot_timing("[Shot 1] At 00:00.000, the room is quiet.")
        self.assertTrue(any("P1-2" in issue and "Shot 1" in issue for issue in issues))

    def test_dialogue_duration_can_come_from_next_shot_timestamp(self):
        text = (
            "[Shot 1] The speaker talks: <d>[Chinese] " + "字" * 22 + "</d> "
            "and waits. [Shot 2] At 00:03.000, the camera cuts to a silent room."
        )

        results = h3_lint.check_dialogue_overload(text)

        self.assertTrue(any(item.startswith("P1-3 台词超载") for item in results), results)
        self.assertFalse(any("NOTCHK" in item for item in results), results)

    def test_explicit_duration_uses_unified_4_1_chars_per_second(self):
        text = "duration: 7s\n[Shot 1] <d>[Chinese] " + "字" * 22 + "</d>"

        results = h3_lint.check_dialogue_overload(text)

        self.assertEqual(h3_lint.CHARS_PER_SECOND, 4.1)
        self.assertTrue(any(item.startswith("P1-3 台词超载") for item in results), results)
        self.assertFalse(any("NOTCHK" in item for item in results), results)

    def test_determinable_duration_within_limit_is_checked(self):
        text = (
            "[Shot 1] The speaker says <d>[Chinese] 你好吗</d> and listens. "
            "[Shot 2] At 00:03.000, the camera cuts to a silent room."
        )
        path = self.write_prompt(text)

        result = h3_lint.lint(path)

        self.assertEqual(result["status"], "PASS")
        self.assertEqual(result["notchecked"], [])

    def test_undeterminable_dialogue_duration_is_explicit_notchk(self):
        path = self.write_prompt("[Shot 1] The speaker says <d>[Chinese] 你好吗</d>.")

        result = h3_lint.lint(path)
        completed = subprocess.run(
            [sys.executable, str(H3_LINT), str(path), "--json"],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )
        payload = json.loads(completed.stdout)[0]

        self.assertEqual(result["status"], "NOTCHK")
        self.assertTrue(result["notchecked"])
        self.assertIn("无法确定", result["notchecked"][0])
        self.assertFalse(result["pass"])
        self.assertEqual(completed.returncode, 2, completed.stdout + completed.stderr)
        self.assertEqual(payload["status"], "NOTCHK")
        self.assertTrue(payload["notchecked"])

        human = subprocess.run(
            [sys.executable, str(H3_LINT), str(path)],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )
        self.assertEqual(human.returncode, 2)
        self.assertIn("NOTCHK", human.stdout)
        self.assertNotIn("PASS  prompt.txt", human.stdout)


if __name__ == "__main__":
    unittest.main()
