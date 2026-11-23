# -*- coding: utf-8 -*-
"""--keep-video 的离线参数与流程测试；所有下载、ASR、画面识别均 mock。"""
import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest import mock

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "understand.py"
SPEC = importlib.util.spec_from_file_location("understand_under_test", SCRIPT)
understand = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(understand)


class KeepVideoTests(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory(prefix="keep-video-test-")
        self.root = Path(self._tmp.name)
        self.keep = self.root / "项目" / "输入" / "原片"
        self.meta = {"title": "测试片", "author": "作者", "duration": 12.0}
        self.subtitle = {
            "text": "字幕证据", "lang": "zh", "timed": [], "file": "sub.ai-zh.srt",
        }

    def tearDown(self):
        self._tmp.cleanup()

    def test_bilibili_keep_video_uses_real_ydl_arguments_and_reuses_source_for_look(self):
        expected = self.keep / "source.mp4"

        def fake_ydl(cfg, args, timeout, capture):
            expected.parent.mkdir(parents=True, exist_ok=True)
            expected.write_bytes(b"local-video-evidence")
            return types.SimpleNamespace(stdout=str(expected) + "\n")

        with mock.patch.object(understand, "bilibili_info", return_value=self.meta), \
                mock.patch.object(understand, "bilibili_subtitles", return_value=self.subtitle), \
                mock.patch.object(understand.ytdlp, "run_ydl", side_effect=fake_ydl) as ydl, \
                mock.patch.object(understand, "_look", return_value=[]) as look:
            result = understand.run(
                "BV1offline", True, 6, None, 0, keep_video=str(self.keep),
            )

        self.assertEqual(result["video_path"], str(expected))
        self.assertTrue(expected.is_file(), "临时目录清理后原片仍须存在")
        self.assertEqual(look.call_args.args[0], str(expected))
        args = ydl.call_args.args[1]
        self.assertIn("bv*+ba/b", args)
        self.assertIn("after_move:filepath", args)
        self.assertIn("--no-playlist", args)
        self.assertIn("--merge-output-format", args)
        self.assertNotIn("--extract-audio", args)
        self.assertIn(str(self.keep / "source.%(ext)s"), args)
        self.assertIn("原片保留：" + str(expected), understand.to_markdown(result))

    def test_default_bilibili_does_not_download_or_emit_keep_path(self):
        with mock.patch.object(understand, "bilibili_info", return_value=self.meta), \
                mock.patch.object(understand, "bilibili_subtitles", return_value=self.subtitle), \
                mock.patch.object(understand.ytdlp, "run_ydl") as ydl, \
                mock.patch.object(understand, "_look", return_value=[]) as look:
            result = understand.run("BV1offline", True, 6, None, 0)

        ydl.assert_not_called()
        self.assertNotIn("video_path", result)
        self.assertEqual(look.call_args.args[0],
                         "https://www.bilibili.com/video/BV1offline/")

    def test_douyin_keep_video_calls_download_video_and_survives_temp_cleanup(self):
        expected = self.keep / "source.mp4"

        def fake_download(url, dst, notes):
            Path(dst).write_bytes(b"douyin-video-evidence")
            return {"title": "抖音测试"}

        def fake_extract(video, audio):
            self.assertTrue(Path(video).is_file())
            Path(audio).write_bytes(b"audio")
            return audio

        with mock.patch.object(understand.asr, "transcribe", return_value=("文字",)), \
                mock.patch.object(understand.asr, "backend_label", return_value="fake-asr"), \
                mock.patch("chubby_common.douyin.download_video", side_effect=fake_download) as download, \
                mock.patch("chubby_common.douyin.extract_audio", side_effect=fake_extract), \
                mock.patch("chubby_common.douyin.download_audio") as audio_download:
            result = understand.run(
                "https://www.douyin.com/video/123456", False, 6, None, 0,
                keep_video=str(self.keep),
            )

        audio_download.assert_not_called()
        self.assertEqual(download.call_args.args[1], str(expected))
        self.assertEqual(result["video_path"], str(expected))
        self.assertEqual(expected.read_bytes(), b"douyin-video-evidence")

    def test_douyin_default_audio_only_path_is_unchanged(self):
        audio = self.root / "audio.mp3"
        audio.write_bytes(b"audio")
        with mock.patch.object(understand.asr, "transcribe", return_value=("文字",)), \
                mock.patch.object(understand.asr, "backend_label", return_value="fake-asr"), \
                mock.patch("chubby_common.douyin.download_audio",
                           return_value=(str(audio), "抖音测试")) as audio_download, \
                mock.patch("chubby_common.douyin.download_video") as download:
            result = understand.run(
                "https://www.douyin.com/video/123456", False, 6, None, 0,
            )

        audio_download.assert_called_once()
        download.assert_not_called()
        self.assertNotIn("video_path", result)

    def test_main_passes_keep_video_argument(self):
        response = {
            "platform": "other", "source": "https://example.com/video",
            "title": "测试", "author": "", "duration": 0,
            "transcriber": "字幕:test", "text": "文字", "notes": [],
        }
        argv = ["understand.py", "https://example.com/video",
                "--keep-video", str(self.keep)]
        stdout = io.StringIO()
        with mock.patch.object(understand, "run", return_value=response) as run, \
                mock.patch.object(sys, "argv", argv), contextlib.redirect_stdout(stdout):
            code = understand.main()

        self.assertEqual(code, 0)
        self.assertEqual(run.call_args.args[-1], str(self.keep))
        self.assertEqual(json.loads(stdout.getvalue())["title"], "测试")

    def test_successful_ydl_without_real_file_is_an_error(self):
        with tempfile.TemporaryDirectory() as keep, \
                mock.patch.object(understand.ytdlp, "run_ydl",
                                  return_value=types.SimpleNamespace(stdout="")):
            with self.assertRaisesRegex(RuntimeError, "未报告有效的原片保留路径"):
                understand.download_kept_video(understand.BILI, "https://example.com", keep)

    def test_ydl_process_failure_has_clear_error(self):
        error = subprocess.CalledProcessError(1, ["yt-dlp"], stderr="HTTP 403")
        with tempfile.TemporaryDirectory() as keep, \
                mock.patch.object(understand.ytdlp, "run_ydl", side_effect=error):
            with self.assertRaisesRegex(RuntimeError, "原片下载失败.*403"):
                understand.download_kept_video(understand.BILI, "https://example.com", keep)


if __name__ == "__main__":
    unittest.main()
