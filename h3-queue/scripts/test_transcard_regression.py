#!/usr/bin/env python3
"""transcard 的提交前校验：17k+5 必须拦住，短帧只告警不拦。"""
import pathlib
import subprocess
import sys
import tempfile
import unittest

HERE = pathlib.Path(__file__).resolve().parent
SCRIPT = HERE / "transcard.py"


def run(frames, before, after, prompt):
    return subprocess.run(
        [sys.executable, str(SCRIPT),
         "--before", str(before), "--after", str(after),
         "--prompt-file", str(prompt), "--frames", str(frames),
         "--width", "576", "--height", "992",
         "--out-dir", tempfile.mkdtemp(), "--dry-run"],
        capture_output=True, text=True,
    )


class TranscardFrameBoundsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        root = pathlib.Path(self.tmp.name)
        self.before = root / "a.mp4"
        self.after = root / "b.mp4"
        self.prompt = root / "p.txt"
        self.before.write_bytes(b"")
        self.after.write_bytes(b"")
        self.prompt.write_text("A quiet room at dusk, a woman waits by the door.", encoding="utf-8")

    def test_below_recommendation_warns_but_passes_frame_checks(self):
        """39f/56f 是合法取值：只告警说明动作容量，不再当错误拦下。

        2026-11-27 实测 22f/39f 转场卡两端 MAD 都 <10，107f 只是推荐值。
        （后续 ffmpeg 读空文件失败属另一回事，这里只判帧数校验。）
        """
        for frames in (39, 56):
            with self.subTest(frames=frames):
                res = run(frames, self.before, self.after, self.prompt)
                text = res.stderr + res.stdout
                self.assertNotIn("不是 17k+5", text)
                self.assertIn("短于常用的 107f", text)

    def test_off_grid_is_rejected(self):
        res = run(110, self.before, self.after, self.prompt)
        self.assertNotEqual(res.returncode, 0)
        self.assertIn("不是 17k+5", res.stderr + res.stdout)

    def test_107_is_quiet(self):
        """107f 是推荐值本身：既不告警也不因网格被拦。"""
        res = run(107, self.before, self.after, self.prompt)
        text = res.stderr + res.stdout
        self.assertNotIn("短于常用的 107f", text)
        self.assertNotIn("不是 17k+5", text)


if __name__ == "__main__":
    unittest.main()
