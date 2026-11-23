#!/usr/bin/env python3
"""Offline contract tests for short_drama_h3q_adapter.py; never submits real work."""
import hashlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

MODULE_PATH = Path(__file__).with_name("short_drama_h3q_adapter.py")
SPEC = importlib.util.spec_from_file_location("short_drama_h3q_adapter", MODULE_PATH)
adapter = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(adapter)
ORIGINAL_SSH = adapter.ssh
ORIGINAL_RUN = adapter.run
ORIGINAL_REF_GATE = adapter.REF_GATE
# short-drama-review 已从 ~/.agents/skills 迁到 drama-skills 子目录，
# 旧默认路径的软链不存在；测试统一指向真实脚本（与 VIDEO_GATE 的 patch 方式一致）。
REAL_REF_GATE = (
    MODULE_PATH.resolve().parents[2]
    / "drama-skills/skills/short-drama-review/scripts/ref_gate.py"
)
assert REAL_REF_GATE.is_file(), f"ref_gate 不存在: {REAL_REF_GATE}"

REF_PROMPT = """subject_definitions:
<Subject 1> is the adult traveler in <Picture 2>, with short brown hair and a blue coat.
<Picture 1> is the opening composition of [Shot 1], showing the traveler beside a station bench.
summary:
[keyframe completion + reference generation] <Subject 1> waits beside the bench, beginning from <Picture 1>.
retention_analysis:
<Subject 1> (appears in [Shot 1]): fully_preserved - adult facial structure, hair silhouette and blue coat remain consistent.
<Picture 1> (appears in [Shot 1]): fully_preserved - the supplied composition establishes the opening frame.
detailed_description:
The target video uses stylized 3D CG rendering with clear directional daylight.
[Shot 1] The traveler stands beside the bench in the opening composition of <Picture 1>. The camera pushes in slowly from a medium shot to a closer view of his face. At 00:00.500, <Subject 1> (S1), speaking with a calm adult male voice, says: <d>[Chinese] 到了。</d> He closes his lips and settles beside the bench.
overall_soundscape:
Quiet station room tone and light fabric movement continue throughout.
non_diegetic_music:
N/A"""

BASE_PROMPT = """For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description:
[Shot 1] Stylized 3D CG, the adult traveler stands beside the bench shown in <Picture 1>. The camera pushes in slowly toward his face as he lifts his gaze, then settles into the supplied framing.
overall_soundscape:
Quiet station room tone continues throughout.
non_diegetic_music:
N/A"""


class H3QAdapterContractTest(unittest.TestCase):
    def setUp(self):
        adapter.POLL_SECONDS = 0
        adapter.ssh = ORIGINAL_SSH
        adapter.run = ORIGINAL_RUN
        adapter.REF_GATE = REAL_REF_GATE
        self.addCleanup(setattr, adapter, "run", ORIGINAL_RUN)
        self.addCleanup(setattr, adapter, "ssh", ORIGINAL_SSH)
        self.addCleanup(setattr, adapter, "REF_GATE", ORIGINAL_REF_GATE)
        self.calls = []
        self.uploaded = []
        self.gate_results = []
        self.media_suffix = ".png"
        self.probe_streams = [
            {"codec_type": "video", "nb_read_packets": "158"},
            {"codec_type": "audio", "nb_read_packets": "200"},
        ]

    def fake_run(self, argv, check=True):
        self.calls.append(argv)
        if len(argv) > 1 and (argv[1] == str(adapter.REF_GATE) or Path(argv[1]).name == "h3_gate.py"):
            result = ORIGINAL_RUN(argv, check=check)
            if Path(argv[1]).name == "h3_gate.py":
                self.gate_results.append(result)
            return result
        command = " ".join(argv)
        if " show " in command:
            return SimpleNamespace(
                stdout=json.dumps({
                    "state": "done",
                    "output": r"E:\H3-Studio\short-drama\job\result" + self.media_suffix,
                }),
                returncode=0,
            )
        if " submit " in command:
            return SimpleNamespace(
                stdout="job abc123def456 kind=image state=queued", returncode=0
            )
        if argv[0] == "scp":
            if argv[1].startswith(adapter.HOST + ":"):
                Path(argv[2]).write_bytes(b"fake-png")
            else:
                self.uploaded.append(Path(argv[1]).read_bytes())
        if argv[0] == "sips":
            Path(argv[-1]).write_bytes(b"compressed-ref")
        if argv[0] == "ffprobe":
            return SimpleNamespace(stdout=json.dumps({"streams": self.probe_streams}), returncode=0)
        return SimpleNamespace(stdout="", returncode=0)

    def exercise(self, collect=False, role="reference_image", reference_path="ref.png",
                 ref_guard_exception=None):
        adapter.run = self.fake_run
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output_root = root / "out"
            output_root.mkdir()
            handle = root / "handle.json"
            reference = root / reference_path
            reference.parent.mkdir(parents=True, exist_ok=True)
            reference.write_bytes(b"ref")
            (root / "视觉设定.md").write_text(
                "# 视觉设定\n\n## 画风基准\n\n"
                "- LOOK-1：ref.png《原生完整画面》\n"
                "- 认可依据：创作者确认。\n", encoding="utf-8")
            job = {
                "modality": "image",
                "job_id": "job1",
                "run_id": "run1",
                "prompt": "test prompt",
                "parameters": {"width": 1344, "height": 768},
                "outputs": ["剧集/EP001/制作成果/images/result.png"],
                "output_root": str(output_root),
                "project_root": str(root),
                "handle_path": str(handle),
                "reference_bindings": [{
                    "slot_id": "REF-HERO",
                    "role": role,
                    "path": reference_path,
                    "label": "角色",
                    "may_control": ["身份"],
                    "must_not_control": ["构图"],
                }],
            }
            if ref_guard_exception is not None:
                job["parameters"]["ref_guard_exception"] = ref_guard_exception
            if collect:
                job["collect_provider_job_id"] = "abc123def456"
                handle.write_text('{"provider_job_id":"abc123def456"}', encoding="utf-8")
            old_stdin = sys.stdin
            sys.stdin = io.TextIOWrapper(
                io.BytesIO(json.dumps(job).encode("utf-8")), encoding="utf-8"
            )
            try:
                adapter.main()
            finally:
                sys.stdin = old_stdin
            self.assertEqual(
                json.loads(handle.read_text(encoding="utf-8"))["provider_job_id"],
                "abc123def456",
            )
            self.assertEqual((output_root / "result.png").read_bytes(), b"fake-png")

    def exercise_video(self, prompt=REF_PROMPT, roles=None, collect=False, parameters=None,
                       bindings=None):
        roles = roles if roles is not None else ["reference_image", "reference_image"]
        self.media_suffix = ".mp4"
        gate_path = str(MODULE_PATH.resolve().parents[2] / "h3-video-gate/scripts/h3_gate.py")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output_root = root / "out"
            handle = root / "handle.json"
            (root / "ref.png").write_bytes(b"ref")
            (root / "视觉设定.md").write_text(
                "# 视觉设定\n\n## 画风基准\n\n"
                "- LOOK-1：ref.png《原生完整画面》\n"
                "- 认可依据：创作者确认。\n", encoding="utf-8")
            job = {
                "modality": "video",
                "job_id": "video1",
                "run_id": "run1",
                "prompt": prompt,
                "parameters": parameters or {"width": 1024, "height": 576, "duration": 6},
                "outputs": ["result.mp4"],
                "output_root": str(output_root),
                "project_root": str(root),
                "handle_path": str(handle),
                "reference_bindings": bindings if bindings is not None else [{
                    "role": role,
                    "path": "ref.png",
                    "label": "角色身份与起始构图",
                    "may_control": ["成年骨相", "本集造型"],
                    "must_not_control": ["动作", "表情"],
                } for role in roles],
            }
            if collect:
                job["collect_provider_job_id"] = "abc123def456"
            stream = io.TextIOWrapper(io.BytesIO(json.dumps(job).encode("utf-8")), encoding="utf-8")
            with patch.object(adapter, "run", side_effect=self.fake_run), \
                    patch.object(adapter, "VIDEO_GATE", gate_path), patch.object(sys, "stdin", stream):
                adapter.main()
            self.assertEqual((output_root / "result.mp4").read_bytes(), b"fake-png")
            if collect:
                return None
            self.assertEqual(json.loads(handle.read_text())["provider_job_id"], "abc123def456")
            evidence = handle.with_suffix(".evidence")
            manifest = json.loads((evidence / "manifest.json").read_text())
            self.assertEqual(manifest["context"]["run_id"], "run1")
            self.assertEqual((evidence / "prompt.txt").read_text(), prompt)
            self.assertEqual(len(manifest["context"]["references"]), len(roles))
            gate_call = next(call for call in self.calls if len(call) > 1 and Path(call[1]).name == "h3_gate.py")
            first_upload = next(i for i, call in enumerate(self.calls) if call[0] == "scp")
            self.assertLess(self.calls.index(gate_call), first_upload)
            return (evidence / "prompt.txt").read_text(encoding="utf-8")

    MULTISHOT_SCRIPT = (
        "Window one: a locked-off two-shot in a garden. At 00:00.000 the girl on the right "
        "raises the water gun. At 00:00.500 she (S1) says <d>[Chinese] 站住！</d> "
        "The window ends on the standoff.\n"
        "---\n"
        "Window two: the same garden and camera. At 00:00.000 the boy on the left already "
        "holds a small wooden ukulele. At 00:02.600 she (S2) sings "
        "<d>[Chinese] 不穿秋裤会变冷。</d> The window ends on the pair smiling."
    )

    def exercise_multishot(self, parameters=None, prompt=None, bindings=None):
        """multishot 走的是同一条 adapter 路径：准入、闸门、留档、取回都不旁路。"""
        self.media_suffix = ".mp4"
        self.probe_streams = [
            {"codec_type": "video", "nb_read_packets": "451"},
            {"codec_type": "audio", "nb_read_packets": "588"},
        ]
        params = {"width": 768, "height": 448, "workflow": "multishot",
                  "frames_per_shot": 226, "shot_count": 2}
        params.update(parameters or {})
        return self.exercise_video(prompt=prompt or self.MULTISHOT_SCRIPT,
                                   roles=["reference_image", "reference_image"],
                                   parameters=params, bindings=bindings)

    @staticmethod
    def identity_binding():
        return {"role": "reference_image", "path": "ref.png", "label": "角色身份板",
                "may_control": ["身份", "成年骨相"],
                "must_not_control": ["构图"]}

    @staticmethod
    def scene_binding():
        return {"role": "reference_image", "path": "ref.png", "label": "场景板",
                "may_control": ["场景地理与构图", "陈设布局"],
                "must_not_control": ["身份"]}

    def submitted_argv(self):
        return [call for call in self.calls if " submit " in " ".join(call)]

    def test_multishot_submits_through_the_same_adapter_path(self):
        self.exercise_multishot()
        submit = next(call for call in self.calls if len(call) > 1 and " submit " in " ".join(call))
        argv = " ".join(submit)
        self.assertIn("--workflow multishot", argv)
        self.assertIn("--frames-per-shot 226", argv)
        self.assertIn("--shot-count 2", argv)
        self.assertIn("--width 768", argv)
        self.assertIn("--height 448", argv)
        # 不得混入单镜档位参数
        self.assertNotIn("--workflow pdd_lu", argv)
        self.assertNotIn("--no-upscale", argv)

    def test_multishot_total_frames_come_from_windows(self):
        job = {"parameters": {"workflow": "multishot", "frames_per_shot": 226,
                              "shot_count": 2, "duration": 5}}
        self.assertEqual(adapter.expected_frames(job), 451)

    def test_multishot_delivered_frames_are_a_range_not_the_formula(self):
        # 2026-11-19 EP005 S-002: requested 107x2 (formula 213) delivered 192f.
        # The formula is a request, not the length the V2 sampler re-times to.
        job = {"parameters": {"workflow": "multishot", "frames_per_shot": 107,
                              "shot_count": 2}}
        low, high = adapter.output_frame_bounds(job)
        self.assertEqual(adapter.expected_frames(job), 213)
        self.assertLessEqual(low, 192)
        self.assertGreaterEqual(high, 213)

    def test_single_shot_still_requires_the_exact_frame_count(self):
        job = {"parameters": {"duration": 5}}
        low, high = adapter.output_frame_bounds(job)
        self.assertEqual(low, high)
        self.assertEqual(low, adapter.expected_frames(job))

    def test_multishot_rejects_bad_window_maths_before_upload(self):
        with self.assertRaises(RuntimeError):
            adapter.multishot_argv({"frames_per_shot": 225, "shot_count": 2,
                                    "width": 768, "height": 448})
        with self.assertRaises(RuntimeError):
            adapter.multishot_argv({"frames_per_shot": 226, "shot_count": 9,
                                    "width": 768, "height": 448})
        with self.assertRaises(RuntimeError):
            adapter.multishot_argv({"frames_per_shot": 226, "shot_count": 2,
                                    "width": 770, "height": 448})
        # 未声明 workflow 的调用仍受 16GB 实测上限保护。
        with self.assertRaises(RuntimeError):
            adapter.multishot_argv({"frames_per_shot": 226, "shot_count": 3,
                                    "width": 768, "height": 448})

    def test_multishot_lifts_total_frame_ceiling(self):
        # 显式 multishot 作业不再被 451 帧上限拦截：676 帧照样产出 CLI 参数。
        argv = adapter.multishot_argv({"workflow": "multishot", "frames_per_shot": 226,
                                       "shot_count": 3, "width": 768, "height": 448})
        self.assertEqual(argv[argv.index("--shot-count") + 1], "3")
        self.assertEqual(adapter.expected_frames({"parameters": {
            "workflow": "multishot", "frames_per_shot": 226, "shot_count": 3}}), 676)

    def test_multishot_script_rejects_bracket_leading_window_before_upload(self):
        # 2026-11-19 EP004: `[Shot 1] ...` made the node parse the script as JSON.
        script = "[Shot 1] a girl stands.\n---\n[Shot 2] she turns."
        with self.assertRaises(RuntimeError) as ctx:
            adapter.verify_multishot_script(script, 2)
        self.assertIn("JSON", str(ctx.exception))

    def test_multishot_script_requires_matching_window_count(self):
        with self.assertRaises(RuntimeError):
            adapter.verify_multishot_script("only one window", 2)

    def test_multishot_script_rejects_single_shot_section_names(self):
        with self.assertRaises(RuntimeError):
            adapter.verify_multishot_script(
                "subject_definitions:\n<Subject 1> is a girl.\n---\nshe turns.", 2)

    def test_multishot_script_accepts_plain_windows(self):
        self.assertEqual(
            adapter.verify_multishot_script(
                "A girl stands.\n---\nShe turns to the lens.", 2), 2)

    def test_multishot_passes_explicit_reference_subjects(self):
        self.exercise_multishot(parameters={"reference_subjects": "1,1"})
        self.assertIn("--reference-subjects 1,1", " ".join(self.submitted_argv()[0]))

    def test_multishot_does_not_invent_reference_subjects(self):
        self.exercise_multishot()
        self.assertNotIn("--reference-subjects", " ".join(self.submitted_argv()[0]))

    def test_multishot_defaults_reference_image_size_to_match(self):
        self.exercise_multishot()
        argv = " ".join(self.submitted_argv()[0])
        self.assertIn("--reference-image-size match", argv)

    def test_multishot_passes_reference_image_size_max_through(self):
        self.exercise_multishot({"reference_image_size": "max"})
        argv = " ".join(self.submitted_argv()[0])
        self.assertIn("--reference-image-size max", argv)

    def test_invalid_reference_image_size_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "reference_image_size must be one of"):
            adapter.multishot_argv({"workflow": "multishot", "width": 768, "height": 448,
                                    "reference_image_size": "native"})

    def test_reference_image_size_is_multishot_only(self):
        with self.assertRaisesRegex(RuntimeError, "只对 workflow=multishot"):
            self.exercise_video(parameters={"width": 1024, "height": 576, "duration": 6,
                                            "reference_image_size": "max"})
        self.assertEqual(self.submitted_argv(), [])

    def test_same_scene_continuous_requires_an_explicit_scene_anchor_index(self):
        # 不允许自动推测锚点：显式声明同场连续就必须指名 scene_anchor_index。
        with self.assertRaisesRegex(RuntimeError, "scene_anchor_index"):
            self.exercise_multishot(
                {"same_scene_continuous": True},
                bindings=[self.identity_binding(), self.scene_binding()])
        self.assertEqual(self.submitted_argv(), [])

    def test_same_scene_continuous_requires_identity_and_scene_bindings(self):
        # 身份卡不构成地理/构图锚；必须在任何上传前拒绝。
        with self.assertRaisesRegex(RuntimeError, "does not declare a scene"):
            self.exercise_multishot(
                {"same_scene_continuous": True, "scene_anchor_index": 1},
                bindings=[self.identity_binding(), self.identity_binding()])
        self.assertEqual(self.submitted_argv(), [])
        # 只有场景锚、没有身份参考同样拒绝。
        with self.assertRaisesRegex(RuntimeError, "identity reference"):
            self.exercise_multishot(
                {"same_scene_continuous": True, "scene_anchor_index": 1},
                bindings=[self.scene_binding(), self.scene_binding()])
        self.assertEqual(self.submitted_argv(), [])

    def test_same_scene_continuous_requires_explicit_bindings(self):
        with self.assertRaisesRegex(RuntimeError, "reference_bindings"):
            self.exercise_multishot(
                {"same_scene_continuous": True, "scene_anchor_index": 1},
                bindings=[])
        self.assertEqual(self.submitted_argv(), [])

    def test_same_scene_continuous_accepts_a_declared_scene_anchor(self):
        self.exercise_multishot(
            {"same_scene_continuous": True, "scene_anchor_index": 2},
            bindings=[self.identity_binding(), self.scene_binding()])
        self.assertEqual(len(self.submitted_argv()), 1)

    def test_default_ref_gate_resolves_to_the_hub_install(self):
        # 默认路径必须指向真实存在的技能中枢副本；~/.agents 只是历史同步目标。
        with patch.dict(adapter.os.environ, {"SHORT_DRAMA_REF_GATE": ""}):
            resolved = adapter._ref_gate_path()
        expected = (Path.home() / ".skills/hub/drama-skills/skills/"
                    "short-drama-review/scripts/ref_gate.py")
        self.assertEqual(resolved, expected)
        self.assertTrue(resolved.is_file())

    def test_scene_change_without_the_flag_is_unaffected(self):
        # 换场/硬切不声明 same_scene_continuous：身份卡参考照常通过。
        self.exercise_multishot(bindings=[self.identity_binding(), self.identity_binding()])
        self.assertEqual(len(self.submitted_argv()), 1)

    def test_scene_anchor_index_selects_the_explicit_binding(self):
        with self.assertRaisesRegex(RuntimeError, "does not declare a scene"):
            self.exercise_multishot(
                {"same_scene_continuous": True, "scene_anchor_index": 1},
                bindings=[self.identity_binding(), self.scene_binding()])
        self.assertEqual(self.submitted_argv(), [])

    def test_scene_anchor_index_out_of_range_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "1-based position"):
            self.exercise_multishot(
                {"same_scene_continuous": True, "scene_anchor_index": 3},
                bindings=[self.identity_binding(), self.scene_binding()])
        self.assertEqual(self.submitted_argv(), [])

    def test_scene_anchor_index_without_the_flag_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "same_scene_continuous=true"):
            self.exercise_multishot(
                {"scene_anchor_index": 2},
                bindings=[self.identity_binding(), self.scene_binding()])
        self.assertEqual(self.submitted_argv(), [])

    def test_same_scene_continuous_is_multishot_only(self):
        with self.assertRaisesRegex(RuntimeError, "只对 workflow=multishot"):
            self.exercise_video(parameters={
                "width": 1024, "height": 576, "duration": 6,
                "same_scene_continuous": True})
        self.assertEqual(self.submitted_argv(), [])

    def test_multishot_runs_the_real_multishot_gate_mode(self):
        # 2026-11-19 起多窗不再「整块豁免结构项」，而是走 --mode multishot：
        # 闸门逐窗检查 G39/G40，干净脚本通过，且提交照常发生。
        submitted = self.exercise_multishot()
        self.assertIn("Window one", submitted)
        self.assertTrue(self.gate_results, "multishot 也必须真的过闸，不能跳过")
        last_argv = next(call for call in self.calls
                         if len(call) > 1 and Path(call[1]).name == "h3_gate.py")
        self.assertIn("--mode", last_argv)
        self.assertIn("multishot", last_argv)
        self.assertIn("--shot-count", last_argv)
        self.assertEqual(self.gate_results[-1].returncode, 0, self.gate_results[-1].stdout)
        submitted_argv = next(call for call in self.calls
                              if len(call) > 1 and " submit " in " ".join(call))
        self.assertIn("--workflow multishot", " ".join(submitted_argv))

    def test_multishot_gate_rejects_a_json_looking_window(self):
        # 2026-11-19 EP004 实证：`[Shot 1] ...` 让节点把整份脚本当 JSON。
        script = "[Shot 1] a girl stands.\n---\n[Shot 2] she turns."
        with self.assertRaises(RuntimeError) as ctx:
            self.exercise_multishot(prompt=script)
        self.assertIn("JSON", str(ctx.exception))
        self.assertEqual(self.submitted_argv(), [])

    def test_multishot_gate_downgrade_is_limited_to_structural_rules(self):
        # gate 对两窗裸正文只能判出结构项（G01 等）；台词类硬规则在模式无法判定时
        # 根本不会产出。所以降级白名单必须**只**含结构项——一旦有人把 G17/G18
        # 也放进白名单，就会静默放过真正的台词错误。这里直接钉住白名单边界。
        structural = {"G01", "G02", "G03", "G25", "G08b"}
        self.assertFalse(structural & adapter.BLOCKING_GATE_WARNINGS,
                         "G17/G18 是台词硬规则，不得进入结构降级集合")
        self.assertEqual(adapter.BLOCKING_GATE_WARNINGS, {"G17", "G18"})

    def test_gate_blockers_has_no_workflow_wide_exemption(self):
        # 多窗有真正的闸门模式后，任何 error 都阻断——不再有 workflow 级白名单。
        structural = [{"level": "error", "rule": "G01", "message": "no section"}]
        self.assertEqual(len(adapter.gate_blockers(structural, "multishot")), 1)
        self.assertEqual(len(adapter.gate_blockers(structural, "ref2va")), 1)

        content = [{"level": "error", "rule": "G15", "message": "非英文正文"}]
        self.assertEqual(len(adapter.gate_blockers(content, "multishot")), 1)
        self.assertEqual(len(adapter.gate_blockers(content, "ref2va")), 1)

        dialogue = [{"level": "warn", "rule": "G17", "message": "画外说话未写闭嘴"}]
        self.assertEqual(len(adapter.gate_blockers(dialogue, "multishot")), 1,
                         "台词硬规则不得被 multishot 降级")

        mixed = structural + content
        self.assertEqual([f["rule"] for f in adapter.gate_blockers(mixed, "multishot")],
                         ["G01", "G15"], "多窗不再豁免结构项，两类 error 都要阻断")

    def test_video_preserves_six_sections_and_excludes_chinese_contract(self):
        submitted_prompt = self.exercise_video()
        self.assertEqual(submitted_prompt, REF_PROMPT)
        self.assertNotIn("Reference input contract", submitted_prompt)
        for metadata in ("角色身份与起始构图", "成年骨相", "本集造型", "动作", "表情"):
            self.assertNotIn(metadata, submitted_prompt)
        self.assertTrue(submitted_prompt.endswith("non_diegetic_music:\nN/A"))
        self.assertIn(REF_PROMPT.encode("utf-8"), self.uploaded)
        self.assertEqual(len(self.gate_results), 1)
        self.assertEqual(self.gate_results[0].returncode, 0, self.gate_results[0].stdout)
        gate_call = next(call for call in self.calls if "h3_gate.py" in " ".join(call))
        self.assertEqual(gate_call[-5:], ["--frames", "158", "--refs", "2", "--json"])
        submit = next(" ".join(call) for call in self.calls if " submit " in " ".join(call))
        self.assertIn("h3qg.py", submit)
        self.assertIn("--refs", submit)
        self.assertNotIn("--first-frame", submit)

    def test_video_single_first_frame_passes_real_base_gate(self):
        self.assertEqual(self.exercise_video(prompt=BASE_PROMPT, roles=["first_frame"]), BASE_PROMPT)
        self.assertEqual(self.gate_results[0].returncode, 0, self.gate_results[0].stdout)
        gate_call = next(call for call in self.calls if "h3_gate.py" in " ".join(call))
        self.assertEqual(gate_call[-5:], ["--frames", "158", "--refs", "1", "--json"])
        submit = next(" ".join(call) for call in self.calls if " submit " in " ".join(call))
        self.assertIn("--first-frame", submit)
        self.assertNotIn("--refs", submit)

    def test_video_first_and_last_frame_reach_fl2va(self):
        """FL2VA 是本地通道真实支持的模式：两个帧都要透传到 --first-frame / --last-frame。"""
        self.exercise_video(prompt=BASE_PROMPT, roles=["first_frame", "last_frame"])
        submit = next(" ".join(call) for call in self.calls if " submit " in " ".join(call))
        self.assertIn("--first-frame", submit)
        self.assertIn("--last-frame", submit)
        self.assertNotIn("--refs", submit)

    def test_video_last_frame_requires_first_frame(self):
        with self.assertRaisesRegex(RuntimeError, "last_frame requires a first_frame"):
            self.exercise_video(roles=["last_frame"])
        self.assertEqual(self.calls, [])

    def test_video_last_frame_cannot_join_a_reference_group(self):
        with self.assertRaisesRegex(RuntimeError, "cannot mix last_frame and reference_image"):
            self.exercise_video(roles=["first_frame", "last_frame", "reference_image"])
        self.assertEqual(self.calls, [])

    def test_video_mixed_reference_roles_fail_before_any_remote_call(self):
        with self.assertRaisesRegex(RuntimeError, "cannot mix first_frame and reference_image"):
            self.exercise_video(roles=["first_frame", "reference_image"])
        self.assertEqual(self.calls, [])
        self.assertEqual(self.uploaded, [])

    def test_legal_side_view_motion_reminder_does_not_block_submission(self):
        prompt = BASE_PROMPT.replace("[Shot 1] Stylized", "[Shot 1] A fixed side view shows the car driving from left to right. Stylized")
        self.exercise_video(prompt=prompt, roles=["first_frame"])
        report = json.loads(self.gate_results[0].stdout)
        self.assertTrue(any(f["rule"] == "G34" and f["level"] == "warn" for f in report["findings"]))
        self.assertTrue(any(" submit " in " ".join(call) for call in self.calls))

    def test_intentional_screen_presentation_reminder_does_not_block_submission(self):
        prompt = BASE_PROMPT.replace("[Shot 1] Stylized", "[Shot 1] He holds the phone up to the camera. Stylized")
        self.exercise_video(prompt=prompt, roles=["first_frame"])
        report = json.loads(self.gate_results[0].stdout)
        self.assertTrue(any(f["rule"] == "G35" for f in report["findings"]))
        self.assertTrue(any(" submit " in " ".join(call) for call in self.calls))

    def test_video_invalid_source_prompt_is_rejected_by_real_gate(self):
        with self.assertRaisesRegex(RuntimeError, "video prompt gate rejected"):
            self.exercise_video(prompt=REF_PROMPT + "\n角色身份")
        self.assertEqual(self.gate_results[0].returncode, 1)
        self.assertIn("G15", self.gate_results[0].stdout)
        self.assertFalse(any(" submit " in " ".join(call) for call in self.calls))
        self.assertEqual(self.uploaded, [])
        self.assertFalse(any(call[0] == "ssh" for call in self.calls))

    def test_video_duration_is_checked_by_real_gate(self):
        with self.assertRaisesRegex(RuntimeError, "video prompt gate rejected"):
            self.exercise_video(prompt=REF_PROMPT.replace("00:00.500", "00:07.000"))
        self.assertEqual(self.gate_results[0].returncode, 1)
        self.assertIn("G11", self.gate_results[0].stdout)
        self.assertFalse(any(" submit " in " ".join(call) for call in self.calls))

    def test_video_reference_count_is_checked_by_real_gate(self):
        with self.assertRaisesRegex(RuntimeError, "video prompt gate rejected"):
            self.exercise_video(roles=["reference_image"])
        self.assertEqual(self.gate_results[0].returncode, 1)
        self.assertIn("G08", self.gate_results[0].stdout)
        self.assertFalse(any(" submit " in " ".join(call) for call in self.calls))

    def test_video_collect_never_uploads_gates_or_resubmits(self):
        self.exercise_video(collect=True, roles=["first_frame", "reference_image"])
        self.assertFalse(any(" submit " in " ".join(call) for call in self.calls))
        self.assertFalse(any(call[0] == "sips" for call in self.calls))
        self.assertEqual(self.gate_results, [])
        self.assertEqual(self.uploaded, [])

    def test_submit_uploads_reference_contract(self):
        self.exercise(collect=False)
        self.assertTrue(any(" submit " in " ".join(call) for call in self.calls))
        submit = next(" ".join(call) for call in self.calls if " submit " in " ".join(call))
        self.assertNotIn("--gate-off", submit)
        self.assertTrue(any(
            b"Reference input contract" in data and "角色".encode("utf-8") in data
            for data in self.uploaded
        ))
        ref_gate_call = next(call for call in self.calls if "ref_gate.py" in " ".join(call))
        self.assertLess(self.calls.index(ref_gate_call), next(
            index for index, call in enumerate(self.calls) if call[0] == "scp"))
        self.assertIn("ref.png", ref_gate_call)

    def test_creator_approved_reference_exception_reaches_h3qg(self):
        exception = {
            "slot_id": "REF-HERO",
            "reference_sha256": hashlib.sha256(b"ref").hexdigest(),
            "creator_ack": True,
            "reason": "Creator confirmed the shelf lines belong to one scene.",
        }
        self.exercise(ref_guard_exception=exception)
        submit = next(" ".join(call) for call in self.calls if " submit " in " ".join(call))
        self.assertIn("h3qg.py", submit)
        self.assertIn("--gate-off", submit)
        self.assertTrue(any("ref_gate.py" in " ".join(call) for call in self.calls))

    def test_reference_exception_rejects_mismatched_hash_before_upload(self):
        exception = {
            "slot_id": "REF-HERO",
            "reference_sha256": "0" * 64,
            "creator_ack": True,
            "reason": "Creator confirmed the shelf lines belong to one scene.",
        }
        with self.assertRaisesRegex(RuntimeError, "reference hash"):
            self.exercise(ref_guard_exception=exception)
        self.assertFalse(any(call[0] in {"ssh", "scp"} for call in self.calls))
        self.assertFalse(any(" submit " in " ".join(call) for call in self.calls))

    def test_reference_exception_does_not_bypass_acceptance_gate(self):
        exception = {
            "slot_id": "REF-HERO",
            "reference_sha256": hashlib.sha256(b"ref").hexdigest(),
            "creator_ack": True,
            "reason": "Creator confirmed the shelf lines belong to one scene.",
        }
        with self.assertRaisesRegex(RuntimeError, "reference acceptance gate rejected"):
            self.exercise(reference_path="剧集/EP001/制作成果/images/ref.png",
                          ref_guard_exception=exception)
        self.assertFalse(any(call[0] in {"ssh", "scp"} for call in self.calls))
        self.assertFalse(any(" submit " in " ".join(call) for call in self.calls))

    def test_reference_exception_requires_ack_and_one_image_reference(self):
        exception = {
            "slot_id": "REF-HERO",
            "reference_sha256": hashlib.sha256(b"ref").hexdigest(),
            "creator_ack": False,
            "reason": "Creator confirmed the shelf lines belong to one scene.",
        }
        with self.assertRaisesRegex(RuntimeError, "creator acknowledgement"):
            self.exercise(ref_guard_exception=exception)
        self.assertFalse(any(call[0] in {"ssh", "scp"} for call in self.calls))

        job = {
            "modality": "video",
            "parameters": {"ref_guard_exception": {**exception, "creator_ack": True}},
            "reference_bindings": [{"slot_id": "REF-HERO", "role": "reference_image"}],
        }
        with self.assertRaisesRegex(RuntimeError, "only supported for image"):
            adapter.validate_ref_guard_exception(job)
        job["modality"] = "image"
        job["reference_bindings"].append({"slot_id": "REF-OTHER", "role": "reference_image"})
        with self.assertRaisesRegex(RuntimeError, "exactly one reference image"):
            adapter.validate_ref_guard_exception(job)

    def test_unaccepted_generated_reference_fails_before_upload(self):
        with self.assertRaisesRegex(RuntimeError, "reference acceptance gate rejected"):
            self.exercise(reference_path="剧集/EP001/制作成果/images/ref.png")
        self.assertEqual(self.uploaded, [])
        self.assertFalse(any(" submit " in " ".join(call) for call in self.calls))
        self.assertFalse(any(call[0] == "sips" for call in self.calls))

    def test_reference_gate_diagnostics_are_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            job = {
                "project_root": str(root),
                "modality": "image",
                "parameters": {"width": 768, "height": 1344},
                "reference_bindings": [],
            }
            with patch.object(adapter, "run", return_value=SimpleNamespace(
                    returncode=1,
                    stdout=json.dumps({
                        "allowed": False,
                        "code": "missing_look_baseline",
                        "message": "project has no creator-accepted look baseline",
                    }),
                    stderr="")):
                with self.assertRaisesRegex(
                        RuntimeError,
                        r"missing_look_baseline — project has no creator-accepted look baseline"):
                    adapter.verify_reference_acceptance(job)

    def test_reference_gate_non_json_failure_keeps_raw_output(self):
        job = {
            "project_root": "/tmp",
            "modality": "image",
            "parameters": {},
            "reference_bindings": [],
        }
        with patch.object(adapter, "run", return_value=SimpleNamespace(
                returncode=1, stdout="", stderr="traceback: boom")):
            with self.assertRaisesRegex(RuntimeError, "traceback: boom"):
                adapter.verify_reference_acceptance(job)

    def test_first_frame_uses_guarded_client(self):
        self.exercise(role="first_frame")
        submit = next(" ".join(call) for call in self.calls if " submit " in " ".join(call))
        self.assertIn("h3qg.py", submit)
        self.assertIn("--first-frame", submit)

    def test_frames_stay_lossless_and_are_never_resampled(self):
        """Frames are the delivered pixels: PNG, native size, no -Z at all.

        `sips -Z 1344` ENLARGES small inputs and SHRINKS large ones, so the old
        lossless branch resampled a 1536x864 real last frame down to 1344 and
        stretched an 896x512 plate up to 1344. Either way the pixels handed to
        the model were no longer the ones the creator reviewed, which is the
        entire point of the flf relay.
        """
        self.calls.clear()
        self.exercise_video(prompt=BASE_PROMPT, roles=["first_frame"])
        sips = [call for call in self.calls if call[0] == "sips"]
        self.assertTrue(sips, "expected an sips encode call")
        self.assertIn("png", sips[-1])
        self.assertNotIn("768", sips[-1])
        self.assertNotIn("-Z", sips[-1])

        self.assertTrue(adapter.lossless_binding(
            {"role": "first_frame", "may_control": []}))
        self.assertTrue(adapter.lossless_binding(
            {"role": "last_frame", "may_control": []}))
        self.assertTrue(adapter.lossless_binding(
            {"role": "reference_image", "may_control": ["起始构图", "人物站位"]}))

    def test_asset_boards_stay_lossless_by_default(self):
        """默认所有参考图走原生 PNG；旧 768 JPEG q80 只在 H3Q_REF_LOSSLESS=0 恢复。

        旧测量只在 Qwen Image 静帧上成立，H3 视频通道从未确认；现在一致性锚点
        一律喂原始像素，只有超过 2048 长边才走 PNG 降采样，不放大、不转 JPEG。
        """
        self.calls.clear()
        self.exercise_video()
        sips = [call for call in self.calls if call[0] == "sips"]
        self.assertTrue(sips)
        self.assertIn("png", sips[-1])
        self.assertNotIn("768", sips[-1])
        self.assertNotIn("jpeg", sips[-1])
        self.assertTrue(adapter.lossless_binding(
            {"role": "identity", "may_control": ["脸型", "发型"]}))

    def test_reference_lossless_switch_overrides_both_ways(self):
        """H3Q_REF_LOSSLESS=0 must restore the old 768/JPEG q80 path."""
        import os as _os
        self.calls.clear()
        previous = _os.environ.get("H3Q_REF_LOSSLESS")
        _os.environ["H3Q_REF_LOSSLESS"] = "0"
        try:
            self.exercise_video()
            sips = [call for call in self.calls if call[0] == "sips"]
            self.assertTrue(sips)
            self.assertIn("768", sips[-1])
            self.assertIn("jpeg", sips[-1])
            self.assertFalse(adapter.lossless_binding(
                {"role": "identity", "may_control": ["脸型"]}))
        finally:
            if previous is None:
                del _os.environ["H3Q_REF_LOSSLESS"]
            else:
                _os.environ["H3Q_REF_LOSSLESS"] = previous

    def test_absurd_source_is_capped_not_resampled(self):
        """Only a long edge above the safety bound may be shrunk, never grown."""
        self.assertEqual(adapter.long_edge("/nonexistent-file.png"), 0)

    def test_video_result_is_probed_for_frames_and_audio(self):
        self.probe_streams = [{"codec_type": "video", "nb_read_packets": "158"}]
        with self.assertRaisesRegex(RuntimeError, "no audio stream"):
            self.exercise_video()
        self.probe_streams = [
            {"codec_type": "video", "nb_read_packets": "60"},
            {"codec_type": "audio", "nb_read_packets": "200"},
        ]
        with self.assertRaisesRegex(RuntimeError, "frames, expected"):
            self.exercise_video()

    def test_uploaded_dialogue_is_compared_with_pinned_screenplay(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "剧集/EP001").mkdir(parents=True)
            (root / "剧集/EP001/剧本.md").write_text("旅人：到了。\n", encoding="utf-8")
            job = {
                "source": "剧集/EP001/视频提示词.md",
                "project_root": str(root),
                "prompt": REF_PROMPT,
            }
            self.assertEqual(adapter.verify_dialogue_against_screenplay(job), "checked")
            job["prompt"] = REF_PROMPT.replace("到了。", "你迟到了。")
            with self.assertRaisesRegex(RuntimeError, "not verbatim"):
                adapter.verify_dialogue_against_screenplay(job)
            (root / "剧集/EP001/剧本.md").unlink()
            self.assertEqual(
                adapter.verify_dialogue_against_screenplay(job),
                "not_checked_missing_screenplay",
            )
            job["source"] = "剧集/EP001/制作规格.md"
            self.assertEqual(
                adapter.verify_dialogue_against_screenplay(job), "not_applicable"
            )

    def test_resolve_real_image_done_record(self):
        state = {
            "params": {"out": r"E:\H3-Studio\renders\image.png"},
            "output": "saved E:/H3-Studio/renders/image.png 1663381 bytes in 27.1s",
        }
        self.assertEqual(
            adapter.resolve_output({"modality": "image"}, state),
            r"E:\H3-Studio\renders\image.png",
        )

    def test_image_deduplicated_job_uses_queue_output_path(self):
        self.assertEqual(adapter.resolve_output(
            {"modality": "image"}, {"params": {"out": r"E:\first\result.png"}},
            fallback=r"E:\retry\result.png"), r"E:\first\result.png")

    def test_resolve_real_video_done_record(self):
        record = r"E:\H3-Studio\renders\video_243frames.json"
        media = r"E:\ComfyUI\output\h3studio\video_00001_.mp4"
        adapter.ssh = lambda command: SimpleNamespace(stdout=media + "\n", returncode=0)
        state = {"output": "COPY_OF_RECORD " + record}
        self.assertEqual(adapter.resolve_output({"modality": "video"}, state), media)

    def submit_line(self):
        return next(" ".join(call) for call in self.calls if " submit " in " ".join(call))

    def test_video_defaults_to_pdd_draft_tier(self):
        """引擎只剩 pdd；draft 首采模板锁 1024x576，长度只认 17k+5 帧数。"""
        self.exercise_video(parameters={"width": 1344, "height": 768, "duration": 6})
        line = self.submit_line()
        for flag in ("--workflow pdd_lu", "--no-upscale", "--sol-profile off",
                     "--frames 158"):
            self.assertIn(flag, line)
        self.assertNotIn("--out-width", line)
        self.assertNotIn("--steps", line)
        self.assertNotIn("--width 896", line)
        self.assertNotIn("--seconds", line)

    def test_pdd_final_tier_upscales_to_the_job_size(self):
        """pdd final 是完整两遍重跑，不需要 draft_job_id/draft_accepted。"""
        self.exercise_video(parameters={
            "width": 1344, "height": 768, "duration": 6, "tier": "final"})
        line = self.submit_line()
        self.assertIn("--workflow pdd_lu", line)
        self.assertIn("--out-width 1344", line)
        self.assertIn("--out-height 768", line)
        self.assertIn("--sol-profile off", line)
        self.assertNotIn("--no-upscale", line)

    def test_unknown_tier_is_rejected(self):
        with self.assertRaisesRegex(RuntimeError, "tier must be one of"):
            self.exercise_video(parameters={"width": 1344, "height": 768, "duration": 6, "tier": "hq"})

    def test_image_reference_upload_preserves_original_bytes_and_extension(self):
        self.exercise(reference_path="ref.PNG")
        uploads = [call for call in self.calls if call[0] == "scp"
                   and not call[1].startswith(adapter.HOST + ":")]
        self.assertEqual(hashlib.sha256(self.uploaded[0]).digest(),
                         hashlib.sha256(b"ref").digest())
        self.assertTrue(uploads[0][2].endswith(".PNG"))
        self.assertFalse(any(call[0] == "sips" for call in self.calls))
        with tempfile.TemporaryDirectory() as temporary:
            source = Path(temporary) / "original.WeBp"
            source.write_bytes(b"original-reference-with-metadata")
            for mode in ("0", "1", "all"):
                with patch.dict(adapter.os.environ, {"H3Q_REF_LOSSLESS": mode}), \
                        patch.object(adapter, "run", side_effect=AssertionError("image preprocessing")):
                    prepared = adapter.prepare_reference(
                        source, Path(temporary), 1, lossless=True, modality="image")
                    self.assertEqual(prepared, source)
                    self.assertEqual(prepared.read_bytes(), b"original-reference-with-metadata")

    def test_image_submit_defaults_and_explicit_overrides(self):
        job = {"job_id": "same-job", "run_id": "same-run", "modality": "image",
               "parameters": {"width": 1536, "height": 2752, "seed": 0}}
        with patch.object(adapter, "ssh", return_value=SimpleNamespace(
                stdout="job abc123def456", returncode=0)) as remote:
            adapter.submit(job, r"E:\work", r"E:\work\prompt.txt", {"refs": "one.PNG"})
            line = remote.call_args.args[0]
            for flag in ("--size 1536x2752", "--seed 0", "--steps 0", "--cfg 3.5",
                         "--loras none", "--resolution 0"):
                self.assertIn(flag, line)
            job["parameters"].update(cfg=1.7, steps=12, resolution=2048,
                                     negative='bad "hands" & blur', loras='detail.safetensors:0.5')
            adapter.submit(job, r"E:\work", r"E:\work\prompt.txt", {"refs": "one.PNG"})
            line = remote.call_args.args[0]
            for flag in ("--cfg 1.7", "--steps 12", "--resolution 2048",
                         '--negative "bad \\"hands\\" & blur"',
                         "--loras detail.safetensors:0.5"):
                self.assertIn(flag, line)
            self.assertEqual(line.count("--cfg"), 1)
            job["parameters"].update(cfg=0, steps=0, resolution=0, loras="off", negative="")
            adapter.submit(job, r"E:\work", r"E:\work\prompt.txt", {})
            line = remote.call_args.args[0]
            for flag in ("--seed 0", "--cfg 0", "--steps 0", "--resolution 0", "--loras off"):
                self.assertIn(flag, line)
            self.assertNotIn("--negative", line)

    def test_image_submissions_isolate_workdir_and_references(self):
        self.exercise()
        first = [call for call in self.calls if call[0] == "scp"
                 and not call[1].startswith(adapter.HOST + ":")]
        self.calls.clear()
        self.exercise()
        second = [call for call in self.calls if call[0] == "scp"
                  and not call[1].startswith(adapter.HOST + ":")]
        self.assertNotEqual(first[0][2], second[0][2])
        self.assertNotEqual(first[1][2], second[1][2])

    def test_fl2va_routing_uses_default_branch(self):
        """首尾帧任务不能落到 pdd_lu：该分支不转发首尾帧（实测 MAD 43.0 vs 3.86）。"""
        params = {"width": 576, "height": 992, "duration": 4.458, "tier": "draft",
                  "workflow": "ref2va"}
        argv = adapter.fl2va_argv(params)
        self.assertNotIn("--workflow", argv)
        self.assertNotIn("pdd_lu", argv)
        self.assertIn("--frames", argv)
        self.assertIn("--sol-profile", argv)
        self.assertIn("107", argv)   # 4.5s -> 107f (17k+5)
        # pdd 档位仍在，只是不用于首尾帧任务
        self.assertIn("--workflow", adapter.tier_argv(params, "j"))

    def test_fl2va_rejects_non_32_canvas(self):
        with self.assertRaises(RuntimeError):
            adapter.fl2va_argv({"width": 575, "height": 992, "duration": 4.5})

    def test_collect_never_resubmits(self):
        self.exercise(collect=True)
        self.assertFalse(any(" submit " in " ".join(call) for call in self.calls))


if __name__ == "__main__":
    unittest.main()
