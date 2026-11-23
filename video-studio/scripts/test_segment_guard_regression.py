#!/usr/bin/env python3
"""segment_guard --allow-decay 只豁免衰减、NOTCHK 仍阻断的回归测试（issue #32-2）。"""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import segment_guard


SEGMENT_GUARD = Path(__file__).resolve().parent / "segment_guard.py"


class SegmentGuardRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.video = Path(self.tmp.name) / "short.mp4"
        self.video.write_bytes(b"")

    def tearDown(self):
        self.tmp.cleanup()

    def run_guard(self, *extra):
        return subprocess.run(
            [sys.executable, str(SEGMENT_GUARD), str(self.video), *extra],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def _cli_with_analyse(self, analyse_result, argv):
        """以受控 analyse 结果驱动 main()，验证退出码。"""
        with patch.object(segment_guard, "analyse", return_value=analyse_result), \
             patch.object(sys, "argv", ["segment_guard.py", str(self.video), *argv]):
            return segment_guard.main()

    def test_allow_decay_does_not_exempt_notchk_frames_short(self):
        """开 --allow-decay + 帧数不足：仍阻断（exit 2），不得 exit 0。"""
        notchk = {"path": str(self.video), "ok": False,
                  "skip": "帧数不足或解码为空", "frames": 3}
        rc = self._cli_with_analyse(notchk, ["--allow-decay"])
        self.assertNotEqual(rc, 0, "--allow-decay 不得放过帧数不足的 NOTCHK")
        self.assertEqual(rc, 2)

    def test_notchk_blocks_without_flag(self):
        notchk = {"path": str(self.video), "ok": False,
                  "skip": "帧数不足或解码为空", "frames": 3}
        self.assertEqual(self._cli_with_analyse(notchk, []), 2)

    def test_allow_decay_still_exempts_real_decay(self):
        """--allow-decay 对本职的衰减类仍豁免（exit 0）。"""
        decay = {"path": str(self.video), "ok": True, "decay": True,
                 "frames": 100, "ring_head": 40.0, "ring_low": 5.0,
                 "inner_head": 2.0, "inner_low": 1.0,
                 "drop": 35.0, "excess": 34.0, "mono_down": 4.0, "note": ""}
        self.assertEqual(self._cli_with_analyse(decay, ["--allow-decay"]), 0)

    def test_decay_blocks_without_flag(self):
        decay = {"path": str(self.video), "ok": True, "decay": True,
                 "frames": 100, "ring_head": 40.0, "ring_low": 5.0,
                 "inner_head": 2.0, "inner_low": 1.0,
                 "drop": 35.0, "excess": 34.0, "mono_down": 4.0, "note": ""}
        self.assertEqual(self._cli_with_analyse(decay, []), 1)


if __name__ == "__main__":
    unittest.main()
