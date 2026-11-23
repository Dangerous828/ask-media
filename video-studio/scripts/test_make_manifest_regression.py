#!/usr/bin/env python3
"""make_manifest 存在性检查必须在 sha256 之前的回归（issue #33-2）。"""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

SPEC = importlib.util.spec_from_file_location(
    "make_manifest", Path(__file__).with_name("make_manifest.py"))
make_manifest = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(make_manifest)


class MakeManifestMissingFileTests(unittest.TestCase):
    def test_missing_prompt_clean_error_no_traceback(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "manifest.json"
            missing = root / "does_not_exist.txt"
            with mock.patch.object(
                    make_manifest.sys, "argv",
                    ["make_manifest.py", "--out", str(out),
                     "--profile", "3d_anime", "--prompt", str(missing)]):
                rc = make_manifest.main()
            self.assertEqual(rc, 2)
            self.assertFalse(out.exists(), "缺失文件不应生成 manifest")

    def test_missing_image_clean_error_no_traceback(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "manifest.json"
            missing = root / "no_such_image.png"
            with mock.patch.object(
                    make_manifest.sys, "argv",
                    ["make_manifest.py", "--out", str(out),
                     "--profile", "3d_anime", "--image", str(missing)]):
                rc = make_manifest.main()
            self.assertEqual(rc, 2)
            self.assertFalse(out.exists())

    def test_existing_files_still_append_manifest(self):
        """正常路径不受存在性检查影响。"""
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            out = root / "manifest.json"
            prompt = root / "p.txt"
            image = root / "i.png"
            prompt.write_text("a woman", encoding="utf-8")
            image.write_bytes(b"png")
            with mock.patch.object(
                    make_manifest.sys, "argv",
                    ["make_manifest.py", "--out", str(out),
                     "--profile", "3d_anime", "--prompt", str(prompt),
                     "--image", str(image)]):
                rc = make_manifest.main()
            self.assertEqual(rc, 0)
            data = json.loads(out.read_text(encoding="utf-8"))
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]["profile"], "3d_anime")


if __name__ == "__main__":
    unittest.main()
