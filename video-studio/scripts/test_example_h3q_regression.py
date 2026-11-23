#!/usr/bin/env python3
"""example_h3q 改名的兼容别名与默认值核对回归（issue #33-1 / #28-4）。

不连渲染机：dry_run 路径在上传提示词前会走 _require_env / _scp_up，
因此这里直接核对模块常量、函数签名与 steps 语义对应的参数拼装。
"""
import importlib.util
import inspect
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "example_h3q", Path(__file__).with_name("example_h3q.py"))
example_h3q = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(example_h3q)


class ExampleH3QDefaultsTests(unittest.TestCase):
    def test_canvas_and_label_match_pre_rename_defaults(self):
        """默认画布/label 与改名前的实测值一致，避免静默跑在新默认上。"""
        sig = inspect.signature(example_h3q.render_via_h3q)
        self.assertEqual(sig.parameters["size"].default, "1376x768")
        self.assertEqual(sig.parameters["label"].default, "h3q/gugu")

    def test_gugu_out_alias_is_read_when_example_out_absent(self):
        """旧环境变量 GUGU_OUT 需作兜底别名。"""
        with tempfile.TemporaryDirectory() as td:
            env = {"GUGU_OUT": td}
            env.pop("EXAMPLE_OUT", None)
            with patch.dict(os.environ, env, clear=True):
                # 重新加载以让模块级常量按新环境求值。
                fresh = importlib.util.module_from_spec(SPEC)
                SPEC.loader.exec_module(fresh)
            self.assertEqual(fresh.LOCAL_OUT_DIR, td)

    def test_example_out_takes_priority_over_gugu_out(self):
        """EXAMPLE_OUT 优先，GUGU_OUT 兜底。"""
        with tempfile.TemporaryDirectory() as td_new, tempfile.TemporaryDirectory() as td_old:
            with patch.dict(os.environ, {"EXAMPLE_OUT": td_new, "GUGU_OUT": td_old}, clear=True):
                fresh = importlib.util.module_from_spec(SPEC)
                SPEC.loader.exec_module(fresh)
            self.assertEqual(fresh.LOCAL_OUT_DIR, td_new)

    def test_steps_eight_emits_no_explicit_steps_flag(self):
        """steps=8 与队列默认同档，等效不传（docstring 与实现一致）。"""
        captured = {}

        def fake_ssh(ps_body, timeout=900):
            captured["ps"] = ps_body
            return 0, '{"state": "done"}'

        with patch.object(example_h3q, "_require_env"), \
                patch.object(example_h3q, "_scp_up", return_value="remote_prompt.txt"), \
                patch.object(example_h3q, "_ssh", side_effect=fake_ssh), \
                patch.object(example_h3q, "_scp_down"):
            example_h3q.render_via_h3q(
                "a woman standing", [], "out.png", steps=8, dry_run=False)

        ps = captured["ps"]
        self.assertNotIn("--steps", ps, "steps=8 不应生成显式 --steps（与队列默认同档）")
        self.assertNotIn("--cfg", ps)

    def test_steps_45_emits_explicit_steps_and_cfg(self):
        """非默认档显式生成 --steps 45 --cfg。"""
        captured = {}

        def fake_ssh(ps_body, timeout=900):
            captured["ps"] = ps_body
            return 0, '{"state": "done"}'

        with patch.object(example_h3q, "_require_env"), \
                patch.object(example_h3q, "_scp_up", return_value="remote_prompt.txt"), \
                patch.object(example_h3q, "_ssh", side_effect=fake_ssh), \
                patch.object(example_h3q, "_scp_down"):
            example_h3q.render_via_h3q(
                "a woman standing", [], "out.png", steps=45, dry_run=False)

        ps = captured["ps"]
        self.assertIn("--steps 45", ps)
        self.assertIn("--cfg 3.5", ps)


if __name__ == "__main__":
    unittest.main()
