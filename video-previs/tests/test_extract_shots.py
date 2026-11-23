# -*- coding: utf-8 -*-
"""extract_shots 的离线 synthetic 验证；不联网、不调用 GPU。"""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

import cv2

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "extract_shots.py"
SPEC = importlib.util.spec_from_file_location("extract_shots_under_test", SCRIPT)
extract_shots = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(extract_shots)


def executable(name):
    found = shutil.which(name)
    for candidate in ("/opt/homebrew/bin/" + name, "/usr/local/bin/" + name):
        if found is None and os.access(candidate, os.X_OK):
            found = candidate
    return found


class ExtractShotsSyntheticTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.ffmpeg = executable("ffmpeg")
        cls.ffprobe = executable("ffprobe")
        if not cls.ffmpeg or not cls.ffprobe:
            raise unittest.SkipTest("synthetic 验证需要本机 ffmpeg 与 ffprobe")
        cls._class_tmp = tempfile.TemporaryDirectory(prefix="extract-shots-suite-")
        cls.source = Path(cls._class_tmp.name) / "source.mp4"
        # 两个纯色镜头，320x180 用于区分代表帧与 222x120 接触印片。
        cmd = [
            cls.ffmpeg, "-y", "-v", "error",
            "-f", "lavfi", "-i", "color=c=red:size=320x180:rate=12:duration=2",
            "-f", "lavfi", "-i", "color=c=blue:size=320x180:rate=12:duration=2",
            "-filter_complex", "[0:v][1:v]concat=n=2:v=1:a=0,format=yuv420p[v]",
            "-map", "[v]", "-c:v", "mpeg4", "-q:v", "2", str(cls.source),
        ]
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, "_class_tmp"):
            cls._class_tmp.cleanup()

    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="extract-shots-case-")
        self.root = Path(self._tmp.name)
        self.video = self.root / "source.mp4"
        shutil.copyfile(self.source, self.video)

    def tearDown(self):
        self._tmp.cleanup()

    def run_cli(self, *args):
        return subprocess.run(
            [sys.executable, str(SCRIPT), str(self.video)] + list(args),
            capture_output=True, text=True, timeout=120,
        )

    def image_size(self, path):
        result = subprocess.run(
            [self.ffprobe, "-v", "error", "-select_streams", "v:0",
             "-show_entries", "stream=width,height", "-of", "json", str(path)],
            check=True, capture_output=True, text=True, timeout=30,
        )
        stream = json.loads(result.stdout)["streams"][0]
        return stream["width"], stream["height"]

    def test_default_outputs_remain_contact_sheet_and_cuts_only(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        out = self.root / "frames_source"
        self.assertTrue((out / "contact_0.jpg").is_file())
        self.assertTrue((out / "cuts.txt").is_file())
        self.assertEqual(list(self.root.rglob("SRC-*.jpg")), [])
        self.assertEqual(list(self.root.rglob("shots.json")), [])
        self.assertEqual(list(self.root.rglob("原片拆解.md")), [])

    def test_rep_frames_manifest_dimensions_names_and_skeleton(self):
        rep = self.root / "输入" / "原片" / "frames"
        result = self.run_cli("--rep-frames", str(rep), "--prefix", "SRC-")
        self.assertEqual(result.returncode, 0, result.stderr)

        manifest_path = rep / "shots.json"
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        shots = manifest["shots"]
        self.assertEqual(len(shots), 2, result.stdout)
        self.assertEqual([s["id"] for s in shots], ["SRC-01", "SRC-02"])
        self.assertEqual([Path(s["frame_path"]).name for s in shots],
                         ["SRC-01.jpg", "SRC-02.jpg"])
        self.assertAlmostEqual(shots[0]["start"], 0.0, delta=0.05)
        self.assertAlmostEqual(shots[0]["end"], 2.0, delta=0.15)
        self.assertAlmostEqual(shots[1]["end"], 4.0, delta=0.15)
        for shot in shots:
            frame = Path(shot["frame_path"])
            self.assertTrue(frame.is_file())
            self.assertGreater(frame.stat().st_size, 0)
            self.assertEqual(self.image_size(frame), (320, 180))
            b, g, r = cv2.imread(str(frame)).mean(axis=(0, 1))
            if shot["id"] == "SRC-01":
                self.assertGreater(r, b, "第一镜中点必须仍在红色段")
            else:
                self.assertGreater(b, r, "第二镜中点必须仍在蓝色段")
            self.assertAlmostEqual(shot["midpoint"],
                                   (shot["start"] + shot["end"]) / 2, places=5)

        skeleton = (rep / "原片拆解.md").read_text(encoding="utf-8")
        self.assertIn("## SRC-01\n", skeleton)
        self.assertIn("## SRC-02\n", skeleton)
        for field in ("入点（秒）", "出点（秒）", "代表帧路径", "景别与机位",
                      "画面人物", "说话人与台词（逐字）", "关键道具与状态", "运镜"):
            self.assertIn(field, skeleton)
        self.assertIn("./SRC-01.jpg", skeleton)
        self.assertIn("待填", skeleton)
        self.assertIn(str(manifest_path), result.stdout)

    def test_no_valid_shots_is_an_error_without_manifest(self):
        self.video.write_bytes(b"")
        rep = self.root / "rep"
        result = self.run_cli("--rep-frames", str(rep))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("没有可抽取代表帧的有效镜头", result.stderr)
        self.assertFalse((rep / "shots.json").exists())
        self.assertFalse((rep / "原片拆解.md").exists())

    def test_missing_ffmpeg_is_explicit(self):
        with mock.patch.object(extract_shots.shutil, "which", return_value=None), \
                mock.patch.object(extract_shots.os, "access", return_value=False):
            with self.assertRaisesRegex(RuntimeError, "找不到 ffmpeg"):
                extract_shots.find_ffmpeg()


if __name__ == "__main__":
    unittest.main()
