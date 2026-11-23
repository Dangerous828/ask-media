# -*- coding: utf-8 -*-
"""dashboard openblend 分支平台守卫回归（issue #33-3）。

非 Windows 下 os 没有 startfile：两个入口都必须干净返回 501 JSON，
不得抛 AttributeError 变成 500；Windows 下仍走 os.startfile 返回 200。
"""
import importlib.util
import io
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest import mock

SERVER = Path(__file__).resolve().parents[1] / "dashboard" / "server.py"
SPEC = importlib.util.spec_from_file_location("dashboard_server_under_test", SERVER)
server = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(server)


class _NoStartFileOS:
    """代理真实 os，但确保 hasattr(os, 'startfile') 为 False（模拟非 Windows）。"""

    def __getattr__(self, name):
        if name == "startfile":
            raise AttributeError(name)
        return getattr(os, name)


class _WindowsLikeOS:
    """代理真实 os，注入可观测的 startfile（模拟 Windows）。"""

    def __init__(self, startfile):
        self.startfile = startfile

    def __getattr__(self, name):
        return getattr(os, name)


class OpenBlendGuardTests(unittest.TestCase):
    def _handler(self, path, body):
        h = server.H.__new__(server.H)
        h.path = path
        raw = json.dumps(body, ensure_ascii=False).encode("utf-8")
        h.headers = {"Content-Length": str(len(raw))}
        h.rfile = io.BytesIO(raw)
        sent = {}

        def _send(code, ct, payload):
            sent["code"] = code
            sent["ct"] = ct
            sent["body"] = payload

        h._send = _send
        return h, sent

    def _assert_clean_501(self, sent):
        self.assertEqual(sent.get("code"), 501, "非 Windows 不得返回 500/AttributeError")
        data = json.loads(sent["body"].decode("utf-8"))
        self.assertFalse(data.get("ok"))
        self.assertIn("Windows", data["err"])

    def test_api_run_openblend_non_windows_clean_501(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "scene.blend").write_bytes(b"blend")
            h, sent = self._handler("/api/run", {"step": "openblend", "args": ["scene.blend"]})
            with mock.patch.object(server, "VIDEO", td), \
                 mock.patch.object(server, "os", _NoStartFileOS()):
                h.do_POST()
            self._assert_clean_501(sent)

    def test_api_openblend_route_non_windows_clean_501(self):
        with tempfile.TemporaryDirectory() as td:
            (Path(td) / "scene.blend").write_bytes(b"blend")
            h, sent = self._handler("/api/openblend", {"p": "scene.blend"})
            with mock.patch.object(server, "VIDEO", td), \
                 mock.patch.object(server, "os", _NoStartFileOS()):
                h.do_POST()
            self._assert_clean_501(sent)

    def test_api_run_openblend_windows_calls_startfile(self):
        calls = []
        with tempfile.TemporaryDirectory() as td:
            blend = Path(td) / "scene.blend"
            blend.write_bytes(b"blend")
            h, sent = self._handler("/api/run", {"step": "openblend", "args": ["scene.blend"]})
            with mock.patch.object(server, "VIDEO", td), \
                 mock.patch.object(server, "os", _WindowsLikeOS(calls.append)):
                h.do_POST()
        self.assertEqual(sent.get("code"), 200)
        data = json.loads(sent["body"].decode("utf-8"))
        self.assertTrue(data.get("ok"))
        self.assertEqual(calls, [str(blend)])


if __name__ == "__main__":
    unittest.main()
