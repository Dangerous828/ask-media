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

    def test_p0_1_undefined_picture_reference_blocks(self):
        text = "[Shot 1] A woman stands beside <Picture 4> and looks out the window."
        issues = h3_lint.check_picture_definitions(text)
        self.assertTrue(any("P0-1" in x and "Picture 4" in x for x in issues), issues)
        path = self.write_prompt(text)
        result = h3_lint.lint(path)
        self.assertTrue(any("P0-1" in x for x in result["p0"]), result["p0"])
        self.assertEqual(result["status"], "BLOCK")
        self.assertFalse(result["pass"])

    def test_p0_3_physical_hint_is_warn_not_block(self):
        text = ("[Shot 1] A woman is holding hands with a child while "
                "waving to the camera with her free hand.")
        hints = h3_lint.check_physical_heuristic(text)
        self.assertTrue(any("P0-3" in x for x in hints), hints)
        path = self.write_prompt(text)
        result = h3_lint.lint(path)
        self.assertEqual(result["p0"], [], result["p0"])
        self.assertTrue(any("P0-3" in x for x in result["p1"]), result["p1"])
        self.assertEqual(result["status"], "WARN")
        self.assertTrue(result["pass"])

    def test_p0_4_official_single_shot_is_allowed(self):
        # 官方 base-en.txt :201-203：双帧都写成 (from Shot 1)，单个 [Shot 1] 连续插值。
        text = (
            "How the reference pictures align with the target video — "
            "Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; "
            "Picture 2 (from Shot 1) aligns with the 8.00-second mark of the target video.\n"
            "integrated_multimodal_description: [Shot 1] A cyclist begins in the framing of "
            "Picture 1 and settles into the pose of Picture 2 at the end of the shot."
        )
        path = self.write_prompt(text)
        self.assertEqual(h3_lint.check_fl2va_single_shot(text), [])
        self.assertNotIn("P0-4", " ".join(h3_lint.lint(path)["p0"]))

    def test_p0_4_three_shots_without_declared_cut_is_blocked(self):
        text = (
            "How the reference pictures align — <Picture 1> (from [Shot 1]) aligns with 0.00s; "
            "<Picture 2> (from [Shot 3]) aligns with 8.00s.\n"
            "[Shot 1] <Picture 1> is the opening. A woman stands by the window.\n"
            "[Shot 2] She lifts her gaze toward the lights.\n"
            "[Shot 3] She folds the letter into the pose of <Picture 2>."
        )
        path = self.write_prompt(text)
        issues = h3_lint.check_fl2va_single_shot(text)
        self.assertTrue(any("P0-4" in x for x in issues), issues)
        self.assertTrue(any("P0-4" in x for x in h3_lint.lint(path)["p0"]))

    def test_p0_4_three_shots_with_declared_hard_cut_is_allowed(self):
        text = (
            "How the reference pictures align — <Picture 1> (from [Shot 1]) aligns with 0.00s; "
            "<Picture 2> (from [Shot 3]) aligns with 8.00s.\n"
            "[Shot 1] <Picture 1> is the opening. A woman stands by the window.\n"
            "[Shot 2] At 00:03.000, the camera cuts to a close-up of the letter.\n"
            "[Shot 3] She folds the letter into the pose of <Picture 2>."
        )
        path = self.write_prompt(text)
        self.assertEqual(h3_lint.check_fl2va_single_shot(text), [])
        self.assertNotIn("P0-4", " ".join(h3_lint.lint(path)["p0"]))

    def test_p0_4_official_bare_picture_labels_are_recognized(self):
        # 裸 `Picture N (from Shot N)` 不带尖括号，也必须被识别为双帧 FL2VA。
        text = (
            "Picture 1 is the first frame and Picture 2 is the ending.\n"
            "[Shot 1] A woman begins at Picture 1 and ends at Picture 2 in one take.\n"
            "[Shot 2] She keeps walking."
        )
        self.assertTrue(h3_lint.check_fl2va_single_shot(text),
                        "裸标签双帧被漏判为并非 FL2VA")

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

    def test_p0_2_cross_line_subject_binding_is_allowed(self):
        """合法跨行 Subject 定义不应被误判为 P0-2（issue #32-3）。"""
        text = (
            "<Subject 2> is the woman in a blue coat, "
            "introduced here and carrying the same face\n"
            "in <Picture 3>. She stands beside the bench.\n"
            "[Shot 1] <Subject 2> waits for the train."
        )
        self.assertEqual(h3_lint.check_reference_loaded(text), [])

    def test_p0_2_same_line_subject_binding_is_allowed(self):
        """同行官方写法仍应通过（防回归，保留原行为）。"""
        text = (
            "<Subject 1> is the traveler in <Picture 1>, with short brown hair.\n"
            "[Shot 1] <Subject 1> waits beside the bench."
        )
        self.assertEqual(h3_lint.check_reference_loaded(text), [])

    def test_p0_2_subject_with_no_picture_is_still_blocked(self):
        """非法 Subject（无任何 Picture 绑定）仍必须判 P0-2。"""
        text = (
            "<Picture 1> is the opening composition of the station.\n"
            "[Shot 1] <Subject 7> smiles at the camera."
        )
        issues = h3_lint.check_reference_loaded(text)
        self.assertTrue(any("P0-2" in x and "Subject 7" in x for x in issues), issues)


if __name__ == "__main__":
    unittest.main()
