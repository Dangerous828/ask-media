#!/usr/bin/env python3
"""ref_guard first_frame 闸门与兼容字段的回归测试（issue #32-1）。"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np

import ref_guard


class RefGuardRegressionTests(unittest.TestCase):
    def test_multi_subject_panel_blocks_on_first_frame(self):
        """首帧多主体面板必须 BLOCK（闸门；放宽=放行废片）。"""
        with tempfile.TemporaryDirectory() as td:
            img = Path(td) / "panel.png"
            # 无需真实图片：直接给 check() 喂一块假 gray，patch 掉读取与面板检测。
            img.write_bytes(b"")
            panel = {"n": 3, "cv": 0.05, "sum_pct": 55.0, "panel": True}
            with patch.object(ref_guard, "_load", return_value=np.zeros((100, 100, 3), dtype=np.uint8)), \
                 patch.object(ref_guard, "multi_subject_panels", return_value=panel):
                result = ref_guard.check(img, chain="first_frame", prompt_text="one continuous frame")
        self.assertFalse(result["pass"], "first_frame 多主体面板必须判负")
        self.assertTrue(any("首帧/尾帧" in x for x in result["issues"]), result["issues"])

    def test_multi_subject_panel_only_warns_on_still(self):
        """静帧链仍只告警，不改变原有行为（防过度放宽/收紧）。"""
        with tempfile.TemporaryDirectory() as td:
            img = Path(td) / "panel.png"
            img.write_bytes(b"")
            panel = {"n": 3, "cv": 0.05, "sum_pct": 55.0, "panel": True}
            with patch.object(ref_guard, "_load", return_value=np.zeros((100, 100, 3), dtype=np.uint8)), \
                 patch.object(ref_guard, "multi_subject_panels", return_value=panel):
                result = ref_guard.check(img, chain="still", prompt_text="one continuous frame")
        self.assertTrue(result["pass"])
        self.assertTrue(any("大小相近" in x for x in result["warns"]), result["warns"])

    def test_span_lines_key_is_always_present(self):
        """span_lines 对外字段必须存在（调用方读取不得 KeyError），恒为 0。"""
        with tempfile.TemporaryDirectory() as td:
            img = Path(td) / "single.png"
            img.write_bytes(b"")
            with patch.object(ref_guard, "_load", return_value=np.zeros((100, 100, 3), dtype=np.uint8)), \
                 patch.object(ref_guard, "multi_subject_panels", return_value={"n": 1}):
                result = ref_guard.check(img, chain="still", prompt_text="one continuous frame")
        self.assertIn("span_lines", result)
        self.assertEqual(result["span_lines"], 0)


if __name__ == "__main__":
    unittest.main()
