#!/usr/bin/env python3
"""Offline regression for h3qg.gate(): reference batches per chain, no h3qc.

The wrapper is the last deterministic check before a paid submission, so its
own wiring needs tests: which references are checked, under which chain, and
which gaps (a lone last frame, a mixed image batch) used to slip through.
"""
import argparse
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "h3qg", Path(__file__).with_name("h3qg.py"))
h3qg = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(h3qg)


class FakeRun:
    """Record ref_guard invocations; script lookup must not touch the disk."""

    def __init__(self, results):
        self.results = list(results)
        self.calls = []

    def __call__(self, path, args):
        self.calls.append((Path(path).name, [str(a) for a in args]))
        ok, out = self.results.pop(0) if self.results else (True, "")
        return ok, out


def ns(kind="video", refs="", first_frame="", last_frame="", prompt_file=""):
    return argparse.Namespace(kind=kind, refs=refs, first_frame=first_frame,
                              last_frame=last_frame, prompt_file=prompt_file)


class H3QGateReferenceBatches(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.tmp = Path(directory.name)
        self.real = self.tmp / "real.png"
        self.real.write_bytes(b"png")

    def gate(self, args, results):
        fake = FakeRun(results)
        with patch.object(h3qg, "_run", fake), \
                patch.object(h3qg.Path, "exists", lambda self, _=None: True):
            code = h3qg.gate(args)
        return code, fake.calls

    def test_last_frame_alone_is_checked(self):
        code, calls = self.gate(ns(last_frame=str(self.real)), [(True, "")])
        self.assertEqual(code, 0)
        chains = [c for c in calls if c[0] == "ref_guard.py"]
        self.assertEqual(chains, [("ref_guard.py", [str(self.real), "--chain", "first_frame"])])

    def test_last_frame_rejection_blocks_submission(self):
        code, calls = self.gate(ns(last_frame=str(self.real)), [(False, "multi-subject")])
        self.assertEqual(code, 1)
        self.assertTrue(any("--chain" in c[1] and "first_frame" in c[1] for c in calls))

    def test_first_and_last_frame_share_the_single_frame_chain(self):
        code, calls = self.gate(
            ns(first_frame=str(self.real), last_frame=str(self.real)),
            [(True, "")])
        self.assertEqual(code, 0)
        checked = [c for c in calls if c[0] == "ref_guard.py"]
        self.assertEqual(len(checked), 1)
        self.assertIn(str(self.real), checked[0][1][0:2])
        self.assertNotIn(str(self.real) + ",", checked[0][1][0])

    def test_image_refs_use_the_still_chain(self):
        _code, calls = self.gate(ns(kind="image", refs=str(self.real)), [(True, "")])
        checked = [c for c in calls if c[0] == "ref_guard.py"]
        self.assertEqual(checked[0][1][-2:], ["--chain", "still"])

    def test_video_refs_use_the_ref2va_chain(self):
        _code, calls = self.gate(ns(kind="video", refs=str(self.real)), [(True, "")])
        checked = [c for c in calls if c[0] == "ref_guard.py"]
        self.assertEqual(checked[0][1][-2:], ["--chain", "ref2va"])

    def test_video_first_frame_is_not_rechecked_as_a_reference_slot(self):
        _code, calls = self.gate(
            ns(first_frame=str(self.real)), [(True, "")])
        checked = [c for c in calls if c[0] == "ref_guard.py"]
        self.assertEqual(checked, [("ref_guard.py", [str(self.real), "--chain", "first_frame"])])

    def test_no_references_no_guard(self):
        code, calls = self.gate(ns(), [])
        self.assertEqual(code, 0)
        self.assertEqual([c for c in calls if c[0] == "ref_guard.py"], [])

    def test_submit_argparse_knows_last_frame(self):
        parser = argparse.ArgumentParser(add_help=False)
        # Mirror main()'s probe parser; a dropped flag means gate() never sees it.
        for flag in ("--kind", "--refs", "--first-frame", "--last-frame", "--prompt-file"):
            parser.add_argument(flag, default="")
        known, _ = parser.parse_known_args(
            ["submit", "--kind", "video", "--last-frame", "x.png"])
        self.assertEqual(known.last_frame, "x.png")


if __name__ == "__main__":
    unittest.main()
