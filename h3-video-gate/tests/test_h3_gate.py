# -*- coding: utf-8 -*-
"""h3_gate.py 的回归测试。

运行(在技能根目录 h3-video-gate/ 下):
    python3 -m unittest discover -s tests -v

夹具在 tests/fixtures/,只读,不修改。真实夹具的断言来自已验证的实跑结果;
合成用例从 s6_141f.txt 派生,每次只做一处改动,先断言改动锚点存在,
避免夹具变化后测试悄悄失效。
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL_ROOT = os.path.dirname(HERE)
GATE = os.path.join(SKILL_ROOT, "scripts", "h3_gate.py")
FIXTURES = os.path.join(HERE, "fixtures")
SERIES_CONFIG = os.path.join(SKILL_ROOT, "references", "series-config.example.json")
SERIES_ORDER = [
    "s1_v5_141f.txt",
    "s2_141f.txt",
    "s3_107f.txt",
    "s4_141f.txt",
    "s5_158f.txt",
    "s6_141f.txt",
]


def fx(name):
    return os.path.join(FIXTURES, name)


def run_gate(*args):
    """调用闸门脚本,返回 (退出码, stdout+stderr)。"""
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, GATE] + list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        cwd=SKILL_ROOT,
    )
    return proc.returncode, proc.stdout + proc.stderr


def run_gate_json(*args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    proc = subprocess.run(
        [sys.executable, GATE, "--json"] + list(args),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env,
        cwd=SKILL_ROOT,
    )
    return proc.returncode, json.loads(proc.stdout)


def read_fixture(name):
    with open(fx(name), "r", encoding="utf-8-sig") as fh:
        return fh.read().replace("\r\n", "\n")


class RealFixtureTests(unittest.TestCase):
    """真实夹具:预期以已验证实跑结果为准。"""

    def test_s3_picture_cited_inside_subject_is_legal(self):
        """<Picture 1> 作为构图锚被写进 <Subject N> 定义里引用 → 合规，不报 G06。

        官方 ref-en.txt:37 要求只作素材来源的图写进 Subject 定义、不建独立行；
        这类图没有独立 Picture 定义行是正确的，不能反过来判它缺定义。
        """
        code, out = run_gate(fx("s3_107f.txt"))
        self.assertEqual(code, 0, out)
        self.assertNotIn("G06", out)

    def test_s2_refs3_passes_with_warnings(self):
        code, out = run_gate(fx("s2_141f.txt"), "--refs", "3")
        self.assertEqual(code, 0, out)
        self.assertIn("G08b", out)
        self.assertRegex(out, r"\[WARN\] G18 ")
        self.assertIn("叠在一起", out)  # 妈妈与豆豆台词重叠
        self.assertIn("G17", out)

    def test_s1_v5_refs3_chinese_outside_d_g15(self):
        code, out = run_gate(fx("s1_v5_141f.txt"), "--refs", "3")
        self.assertEqual(code, 1, out)
        self.assertIn("G15", out)
        self.assertIn("外卖", out)
        self.assertRegex(out, r"\[WARN\] G18 ")

    def test_series_config_catches_beige_cardigan_s01(self):
        files = [fx(n) for n in SERIES_ORDER]
        code, out = run_gate(*(files + ["--series-config", SERIES_CONFIG]))
        self.assertEqual(code, 1, out)
        self.assertIn("S01", out)
        self.assertIn("beige cardigan", out)

    def test_json_output_parses(self):
        code, data = run_gate_json(fx("s3_107f.txt"))
        self.assertEqual(code, 0, data)
        self.assertEqual(data["summary"]["exit_code"], 0)
        self.assertNotIn("G06", {f["rule"] for f in data["findings"]})

    def test_missing_file_is_usage_error(self):
        code, _out = run_gate(fx("does_not_exist_141f.txt"))
        self.assertEqual(code, 2)


class SyntheticFromS6Tests(unittest.TestCase):
    """从 s6_141f.txt 派生的最小反例;每个用例只改一处。"""

    def setUp(self):
        self.base = read_fixture("s6_141f.txt")
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text):
        # 文件名带 _141f,时长与 s6 原文一致
        path = os.path.join(self.tmp.name, "syn_141f.txt")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        return path

    def mutate(self, old, new):
        self.assertIn(old, self.base, "s6 夹具里找不到改动锚点:%r" % old)
        return self.base.replace(old, new, 1)

    def write_config(self, config):
        path = os.path.join(self.tmp.name, "series.json")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(config, fh, ensure_ascii=False)
        return path

    def test_control_s6_unmodified_passes(self):
        # 对照组:合成用例的失败应只来自各自的改动
        code, out = run_gate(self.write(self.base))
        self.assertEqual(code, 0, out)

    def test_a_ref_with_integrated_section_g03(self):
        text = self.base.rstrip("\n") + (
            "\n\nintegrated_multimodal_description:\nThe target video is an extra base-mode block.\n"
        )
        code, out = run_gate(self.write(text))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"\[ERROR\] G03 ")

    def test_b_missing_music_section_g02(self):
        self.assertIn("\nnon_diegetic_music:", self.base)
        text = self.base.split("\nnon_diegetic_music:")[0] + "\n"
        code, out = run_gate(self.write(text))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"\[ERROR\] G02 ")
        self.assertIn("non_diegetic_music", out)

    def test_c_dialogue_without_language_tag_g13(self):
        text = self.mutate(
            "her voice warm and off-hand.",
            "her voice warm and off-hand. <Subject 2> (S1) says: <d>你好</d>",
        )
        code, out = run_gate(self.write(text))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"\[ERROR\] G13 ")

    def test_d_unknown_retention_marker_g09(self):
        text = self.mutate(
            "fully_preserved - the toddler's identity",
            "foo_marker - the toddler's identity",
        )
        code, out = run_gate(self.write(text))
        self.assertEqual(code, 1, out)
        self.assertRegex(out, r"\[ERROR\] G09 ")
        self.assertIn("foo_marker", out)

    def test_e1_negated_dusk_does_not_trigger_g22(self):
        text = self.mutate(
            "dappled light on the lawn.",
            "dappled light on the lawn. There is no dusk light.",
        )
        config = self.write_config({"time_of_day": {"forbid_any": ["dusk"]}})
        _code, data = run_gate_json(self.write(text), "--series-config", config)
        self.assertNotIn("G22", {f["rule"] for f in data["findings"]})

    def test_e2_at_dusk_with_explicit_config_triggers_g22_warn(self):
        text = self.mutate(
            "dappled light on the lawn.",
            "dappled light on the lawn. The courtyard glows at dusk.",
        )
        config = self.write_config({"time_of_day": {"forbid_any": ["dusk"]}})
        _code, data = run_gate_json(self.write(text), "--series-config", config)
        hits = [f for f in data["findings"] if f["rule"] == "G22"]
        self.assertTrue(hits, data["findings"])
        self.assertTrue(all(f["level"] == "warn" for f in hits))

    def test_e3_night_without_time_config_is_notchk_not_ok(self):
        text = self.mutate(
            "dappled light on the lawn.",
            "moonlight on the lawn at night.",
        )
        # 只验证 G22 的 NOTCHK；临时输入去除会独立触发 G38 的绝对时长措辞，夹具保持只读。
        self.assertIn("over the whole shot", text)
        text = text.replace("over the whole shot", "over the slow push-in", 1)
        code, out = run_gate(self.write(text), "--strict", "-v")
        self.assertEqual(code, 0, out)
        self.assertNotIn("G22", out)  # 既无 warn,也不伪装成 [OK] G22

    def test_e4_require_any_alone_does_not_enable_g22(self):
        text = self.mutate(
            "dappled light on the lawn.",
            "dappled light on the lawn. The courtyard glows at dusk.",
        )
        config = self.write_config({"time_of_day": {"require_any": ["afternoon"]}})
        _code, data = run_gate_json(self.write(text), "--series-config", config)
        self.assertNotIn("G22", {f["rule"] for f in data["findings"]})


class OfficialSpecAlignment(unittest.TestCase):
    """2026-10-17:对照官方 MiniMax-H3 skills/h3-prompt-writing 原文补充的规则(误报修正 + 漏报补齐)。"""

    HEAD = ("subject_definitions:\n<Subject 1> is a woman in <Picture 1>.\n\n"
            "summary:\n%s The target video shows <Subject 1> dancing.\n\n"
            "retention_analysis:\n<Subject 1> (appears in [Shot 1]): fully_preserved - kept.\n\n"
            "detailed_description:\nLive-action cinematic style, soft light.\n"
            "[Shot 1] At 00:00.000, <Subject 1> stands. %s Holds through 00:10.125.\n\n"
            "overall_soundscape:\nSoft room tone.\n\nnon_diegetic_music:\nN/A\n")

    def _run(self, text, *extra):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "t_243f.txt")
            open(f, "w", encoding="utf-8").write(text)
            return run_gate("--refs", "1", *extra, f)

    def test_g23_missing_prefix_warns(self):
        code, out = self._run(self.HEAD % ("", ""))
        self.assertIn("G23", out)

    def test_g23_valid_prefix_ok(self):
        code, out = self._run(self.HEAD % ("[reference generation]", ""))
        self.assertNotIn("G23", out)

    def test_g23_bad_enum_errors(self):
        code, out = self._run(self.HEAD % ("[make video]", ""))
        self.assertEqual(code, 1)
        self.assertIn("G23", out)

    def test_g24_unknown_tag_warns(self):
        code, out = self._run(self.HEAD % ("[reference generation]", "Audio continues <cutoffted>."))
        self.assertIn("G24", out)

    def test_g25_over_15s_errors(self):
        code, out = self._run(self.HEAD % ("[reference generation]", ""), "--frames", "481")
        self.assertEqual(code, 1)
        self.assertIn("G25", out)

    def test_g26_video_quota_errors(self):
        extra = "<Video 1> <Video 2> <Video 3> <Video 4>"
        code, out = self._run(self.HEAD % ("[reference generation]", extra))
        self.assertIn("G26", out)

    def test_g08_audio_independent_numbering_allowed(self):
        extra = "<Audio 2> is reused."
        code, out = self._run(self.HEAD % ("[reference generation]", extra))
        self.assertNotIn("G08 ", out.replace("G08b", ""))

    def test_g14_audio_as_source_no_speaker_required(self):
        extra = "When <Audio 1> reaches the phrase <d>[English] lonely lonely.</d>, <Subject 1> waves."
        code, out = self._run(self.HEAD % ("[reference generation]", extra))
        self.assertNotIn("G14", out)

    def test_g14_group_speaker_ids_allowed(self):
        extra = "<Subject 1> (S1) and a friend (S2) shout together (S1,S2), <d>[English] Wait for us!</d>"
        code, out = self._run(self.HEAD % ("[reference generation]", extra))
        self.assertNotIn("找不到说话人", out)


class LocalDurationBoundaryTests(unittest.TestCase):
    """15 秒请求向上吸附为 362 帧,只豁免明确帧数来源的物理时长。"""

    def _run(self, *extra, frames_in_name=141):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "boundary_%df.txt" % frames_in_name)
            # 时长规则的 strict 控制输入不携带无关 G38；原始真实夹具仍保持只读。
            text = read_fixture("s6_141f.txt")
            self.assertIn("over the whole shot", text)
            text = text.replace("over the whole shot", "over the slow push-in", 1)
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            return run_gate_json(path, *extra)

    def test_15_seconds_and_360_frames_keep_grid_warning(self):
        for args, source in ((["--seconds", "15"], "--seconds"),
                             (["--frames", "360"], "--frames")):
            with self.subTest(source=source):
                code, data = self._run(*args)
                self.assertEqual(code, 0, data)
                self.assertEqual(data["files"][0]["frames"], 360)
                self.assertEqual(data["files"][0]["duration_source"], source)
                self.assertNotIn("G25", {f["rule"] for f in data["findings"]})
                self.assertEqual([f["level"] for f in data["findings"]
                                  if f["rule"] == "G12"], ["warn"])
                strict_code, strict_data = self._run(*args, "--strict")
                self.assertEqual(strict_code, 1, strict_data)
                self.assertEqual(strict_data["summary"]["errors"], 0)

    def test_362_explicit_frames_and_filename_pass_strict(self):
        for args, filename_frames, source in ((["--frames", "362"], 141, "--frames"),
                                              ([], 362, "文件名")):
            with self.subTest(source=source):
                code, data = self._run(*args, "--strict", frames_in_name=filename_frames)
                self.assertEqual(code, 0, data)
                self.assertEqual(data["summary"]["warnings"], 0)
                self.assertEqual(data["files"][0]["frames"], 362)
                self.assertAlmostEqual(data["files"][0]["duration_seconds"], 362 / 24)
                self.assertEqual(data["files"][0]["duration_source"], source)

    def test_frames_above_15s_only_accept_exact_362_grid(self):
        # 361虽接近362仍非合法豁免;363/365非网格,379是下一网格。
        for frames in (361, 363, 365, 379):
            for use_filename in (False, True):
                with self.subTest(frames=frames, filename=use_filename):
                    args = [] if use_filename else ["--frames", str(frames)]
                    code, data = self._run(*args, frames_in_name=frames if use_filename else 141)
                    self.assertEqual(code, 1, data)
                    hits = [f for f in data["findings"] if f["rule"] == "G25"]
                    self.assertEqual([f["level"] for f in hits], ["error"])
                    self.assertIn("362", hits[0]["message"])
                    self.assertNotIn("365", hits[0]["message"].split("改法:")[-1])

    def test_excess_seconds_cannot_inherit_362_frame_exemption(self):
        # --seconds优先于文件名;即使恰好对应362帧,它仍是超额秒数请求。
        for seconds in (str(362 / 24), "15.083333", "15.2", "16"):
            with self.subTest(seconds=seconds):
                code, data = self._run("--seconds", seconds, frames_in_name=362)
                self.assertEqual(code, 1, data)
                self.assertEqual(data["files"][0]["duration_source"], "--seconds")
                self.assertEqual([f["level"] for f in data["findings"]
                                  if f["rule"] == "G25"], ["error"])

    def test_allow_long_video_downgrades_long_frames_to_warn(self):
        # --allow-long-video 只用于手搓直投通道:447f 的 G25 从 error 降为 warn。
        code, data = self._run("--allow-long-video", "--frames", "447")
        self.assertEqual(code, 0, data)
        self.assertEqual([f["level"] for f in data["findings"]
                          if f["rule"] == "G25"], ["warn"])

    def test_allow_long_video_cannot_bypass_node_hard_cap(self):
        # 节点硬顶 3600f 任何通道都不能超, exemption flag 无效。
        code, data = self._run("--allow-long-video", "--frames", "3617")
        self.assertEqual(code, 1, data)
        self.assertEqual([f["level"] for f in data["findings"]
                          if f["rule"] == "G25"], ["error"])
        self.assertIn("3600", [f["message"] for f in data["findings"]
                               if f["rule"] == "G25"][0])

    def test_allow_long_video_seconds_still_errors(self):
        # 秒数请求不共享 --frames/文件名的豁免,加 flag 仍是 error。
        code, data = self._run("--allow-long-video", "--seconds", "15.083333")
        self.assertEqual(code, 1, data)
        self.assertEqual(data["files"][0]["duration_source"], "--seconds")
        self.assertEqual([f["level"] for f in data["findings"]
                          if f["rule"] == "G25"], ["error"])


class Fl2vaSingleShotAndBareLabel(unittest.TestCase):
    """2026-10-22 EP01 v4 实测补的两条:G28(FL2VA 必须单段)与 G21 裸标签触发。

    两条都源自同一个根因:检查器原先只认「我以为的写法」,不认官方范例的真实写法
    (官方对齐句里帧号写的是裸 `Picture 1 (from Shot 1)`,base-en.txt:25/:201)。
    """

    ALIGN = ("How the reference pictures align with the target video — "
             "Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; "
             "Picture 2 (from Shot 1) aligns with the 4.46-second mark of the target video.\n\n")

    BODY = ("integrated_multimodal_description:\n%s\n\n"
            "overall_soundscape:\nWind moving through the meadow grass.\n\n"
            "non_diegetic_music:\nA sustained warm string pad.\n")

    SINGLE = ("[Shot 1] Smooth 3D CG, the target video opens on Picture 1 and the camera pushes "
              "slowly forward across the meadow toward the two figures, then decelerates into the "
              "exact framing and light of Picture 2 at the end of the shot.")

    MULTI = ("[Shot 1] Smooth 3D CG, the target video opens on Picture 1 and the camera pushes "
             "slowly forward across the meadow.\n\n"
             "[Shot 2] At 00:01.200 the camera continues past the tall grass.\n\n"
             "[Shot 3] At 00:02.800 the camera arrives at the wide view and settles into the exact "
             "framing and light of Picture 2 at the end of the shot.")

    def _run(self, text, *extra):
        with tempfile.TemporaryDirectory() as d:
            f = os.path.join(d, "t_107f.txt")
            open(f, "w", encoding="utf-8").write(text)
            return run_gate("--frames", "107", *extra, f)

    def test_g28_fl2va_multishot_without_declared_cut_errors(self):
        code, out = self._run(self.ALIGN + self.BODY % self.MULTI)
        self.assertEqual(code, 1, out)
        self.assertIn("G28", out)

    def test_g28_single_shot_ok(self):
        code, out = self._run(self.ALIGN + self.BODY % self.SINGLE)
        self.assertNotIn("G28", out)

    def test_g28_declared_hard_cut_is_allowed_by_official(self):
        """base-en.txt:62 允许显式声明的多段,不得误报。"""
        declared = self.MULTI.replace("the camera continues", "the camera cuts to a low angle")
        declared = declared.replace("the camera arrives", "the camera cuts to the wide meadow")
        code, out = self._run(self.ALIGN + self.BODY % declared)
        self.assertNotIn("G28", out)

    def test_g28_does_not_hit_i2va_single_frame(self):
        """I2VA 只加载一张帧,官方允许多段,不得误报。"""
        i2va = ("For the target video, at 0.00 seconds into the target video, "
                "<Picture 1> (from [Shot 1]) is fully referenced.\n\n")
        # I2VA 只锚首帧:正文不得再引用第二张帧,否则结构上就变成 FL2VA 了
        multi_one_frame = ("[Shot 1] Smooth 3D CG, the target video opens on Picture 1 and the "
                           "camera pushes slowly forward across the meadow.\n\n"
                           "[Shot 2] At 00:01.200 the camera cuts to a low angle as they begin to run.\n\n"
                           "[Shot 3] At 00:02.800 the camera cuts to the wide meadow and settles.")
        code, out = self._run(i2va + self.BODY % multi_one_frame)
        self.assertNotIn("G28", out)

    def test_g21_bare_picture_label_still_requires_align_head(self):
        """缺对齐首行时,裸标签写法也必须被抓(原先只认尖括号 => 整份漏检)。"""
        code, out = self._run(self.BODY % self.SINGLE)
        self.assertEqual(code, 1, out)
        self.assertIn("G21", out)

    def test_g21_official_bare_align_head_passes(self):
        """官方裸对齐句不得误报 G21 —— 项目 S01–S08 全部是这种写法。"""
        code, out = self._run(self.ALIGN + self.BODY % self.SINGLE)
        self.assertNotIn("G21", out)


class NegativeSlotField(unittest.TestCase):
    """G29: H3 在 cfg 1 无负向分支(官方 guide §8),`negative:` 字段形态必为死配置。

    校准依据(2026-10-23 实测):官方 base-en.txt 出现 0 次、ref-en.txt 出现 0 次
    `negative:` 字段形态;而正文 no/not/never 在官方 ref-en.txt 有 34 处、
    base-en.txt 有 12 处,官方 3D 动画 skill 更自带 6 连「不要…」风格锁。
    所以本条只拦字段名形态,绝不拦正文否定。
    """

    ALIGN = Fl2vaSingleShotAndBareLabel.ALIGN
    BODY = Fl2vaSingleShotAndBareLabel.BODY
    SINGLE = Fl2vaSingleShotAndBareLabel.SINGLE

    def _run(self, text, *extra):
        return Fl2vaSingleShotAndBareLabel._run(self, text, *extra)

    def test_g29_blocks_negative_field(self):
        """行首 `negative:` 必须报 error,并指明改法。"""
        body = self.SINGLE + "\n\nnegative: low quality, blurry, extra characters"
        code, out = self._run(self.ALIGN + self.BODY % body)
        self.assertEqual(code, 1, out)
        self.assertIn("G29", out)

    def test_g29_blocks_negative_prompt_variant(self):
        """`negative_prompt:` 与 `neg =` 同属字段形态,一并拦。"""
        for variant in ("negative_prompt: blurry", "neg = photoreal skin"):
            body = self.SINGLE + "\n\n" + variant
            code, out = self._run(self.ALIGN + self.BODY % body)
            self.assertIn("G29", out, variant)

    def test_g29_allows_official_positive_style_lock(self):
        """官方 3D 动画 skill 的风格锁是正文多连「不要…」,不得误报。"""
        body = self.SINGLE + ("\n\nStylized 3D cartoon rendering, warm SSS skin, "
                              "no photoreal live action, no flat 2D, no plastic toy skin "
                              "and generous negative space on both sides.")
        code, out = self._run(self.ALIGN + self.BODY % body)
        self.assertNotIn("G29", out)

    def test_g29_allows_body_single_negation(self):
        """正文单句否定(no second television / do not show)是官方用法,不拦。"""
        body = self.SINGLE + ("\n\nThere is absolutely no second television in frame; "
                              "do not show any extra characters.")
        code, out = self._run(self.ALIGN + self.BODY % body)
        self.assertNotIn("G29", out)


class AuditGapRegressionTests(unittest.TestCase):
    """G09/G15/G30/G31/G32 的定向正反回归。"""

    REF = ("subject_definitions:\n<Subject 1> is a woman in <Picture 1>.\n\n"
           "summary:\n[reference generation] The target video shows <Subject 1>.\n\n"
           "retention_analysis:\n<Subject 1> (appears in [Shot 1]): fully_preserved - kept.\n\n"
           "detailed_description:\nLive-action cinematic style, soft light.\n"
           "[Shot 1] <Subject 1> stands. %s Holds through 00:05.880.\n\n"
           "overall_soundscape:\nSoft room tone.\n\nnon_diegetic_music:\nN/A\n")
    BASE = ("integrated_multimodal_description:\n[Shot 1] Live-action cinematic style. %s\n\n"
            "overall_soundscape:\nSoft room tone.\n\nnon_diegetic_music:\nN/A\n")

    def _run(self, text, *extra, config=None):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "audit_141f.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            args = [path]
            if config is not None:
                cfg = os.path.join(d, "series.json")
                with open(cfg, "w", encoding="utf-8") as fh:
                    json.dump(config, fh, ensure_ascii=False)
                args.extend(["--series-config", cfg])
            args.extend(extra)
            return run_gate_json(*args)

    def _ref(self, extra=""):
        return self.REF % extra

    @staticmethod
    def _hits(data, rule):
        return [f for f in data["findings"] if f["rule"] == rule]

    def test_g10_ignores_shot_refs_inside_from_parens(self):
        """官方 base 写法带方括号引用同一镜，不能当第二镜。

        `base-en.txt:19` 是 `<Picture 1> (from [Shot 1]) is fully referenced`；
        `:201` 的 FL2VA 范例是不带方括号的形式。两种都必须过 G10——
        按段落字面取 `[Shot N]` 会把引用数成镜头，照官方写反而报错。
        """
        bracketed = (
            "integrated_multimodal_description: For the target video, at 0.00 seconds "
            "into the target video, <Picture 1> (from [Shot 1]) is fully referenced. "
            "At 4.46 seconds into the target video, <Picture 2> (from [Shot 1]) is "
            "fully referenced.\n\n"
            "[Shot 1] Live-action cinematic style, a woman walks down a lane.\n\n"
            "overall_soundscape: Soft room tone.\n\nnon_diegetic_music: N/A\n")
        _code, data = self._run(bracketed, "--mode", "base", "--frames", "107",
                                "--refs", "2")
        self.assertFalse(self._hits(data, "G10"), data["findings"])

        plain = bracketed.replace("(from [Shot 1])", "(from Shot 1)")
        _code, data = self._run(plain, "--mode", "base", "--frames", "107", "--refs", "2")
        self.assertFalse(self._hits(data, "G10"), data["findings"])

    def test_g10_still_flags_a_duplicated_shot_marker(self):
        """排除括号引用后，真正的重复镜头标记仍要报——别把检查削掉。"""
        two = (
            "integrated_multimodal_description: [Shot 1] A woman walks down a lane "
            "in warm side light. [Shot 1] She stops at the door.\n\n"
            "overall_soundscape: Soft room tone.\n\nnon_diegetic_music: N/A\n")
        _code, data = self._run(two, "--mode", "base", "--frames", "107", "--refs", "1")
        self.assertTrue(self._hits(data, "G10"), data["findings"])

    def test_g09_hint_uses_neutral_composition_anchor(self):
        good = read_fixture("s6_141f.txt")
        _code, data = self._run(good)
        self.assertFalse(self._hits(data, "G09"), data["findings"])

        old = "<Picture 1> ([Shot 1] composition anchor):"
        self.assertIn(old, good)
        code, data = self._run(good.replace(old, "<Picture 1> (unclear role):", 1))
        self.assertEqual(code, 1, data)
        messages = "\n".join(f["message"] for f in self._hits(data, "G09"))
        self.assertIn("([Shot 1] composition anchor)", messages)
        self.assertNotIn("([Shot 1] first frame)", messages)

    def test_g31_first_frame_wording_warns_without_forbidding(self):
        good = read_fixture("s6_141f.txt")
        _code, data = self._run(good)
        self.assertFalse(self._hits(data, "G31"), data["findings"])
        anchor = "At 00:00.000, <Subject 1> stands"
        self.assertIn(anchor, good)
        variants = [
            good.replace("<Picture 1> is the composition anchor for [Shot 1]",
                         "<Picture 1> is the first frame of [Shot 1]", 1),
            good.replace(anchor, "At 00:00.000, the shot begins from <Picture 1>; <Subject 1> stands", 1),
            good.replace(anchor, "At 00:00.000, the shot opens from <Picture 1>; <Subject 1> stands", 1),
        ]
        for index, text in enumerate(variants):
            with self.subTest(variant=index):
                code, data = self._run(text)
                self.assertEqual(code, 0, data)
                self.assertEqual(data["summary"]["errors"], 0)
                hits = self._hits(data, "G31")
                self.assertEqual([f["level"] for f in hits], ["warn"], data["findings"])
                self.assertIn("真实起始帧", hits[0]["message"])

    def test_g30_missing_source_errors_and_bound_subject_passes(self):
        code, data = self._run(self._ref(), "--refs", "1")
        self.assertEqual(code, 0, data)
        self.assertFalse(self._hits(data, "G30"))

        bad = self._ref().replace("a woman in <Picture 1>", "a woman", 1)
        code, data = self._run(bad, "--refs", "1")
        self.assertEqual(code, 1, data)
        self.assertEqual([f["level"] for f in self._hits(data, "G30")], ["error"])

    def test_g30_subject_picture_cannot_exceed_refs(self):
        bad = self._ref().replace("a woman in <Picture 1>", "a woman in <Picture 2>", 1)
        code, data = self._run(bad, "--refs", "1")
        self.assertEqual(code, 1, data)
        hits = self._hits(data, "G30")
        self.assertTrue(any("<Picture 2>" in f["message"] and f["level"] == "error" for f in hits), data["findings"])

    def test_g30_official_video_audio_and_offscreen_sources_pass(self):
        for definition in ("a woman in <Video 1>", "a narration voice in <Audio 1>",
                           "an off-screen adult female narrator"):
            with self.subTest(definition=definition):
                text = self._ref().replace("a woman in <Picture 1>", definition, 1)
                code, data = self._run(text)
                self.assertEqual(code, 0, data)
                self.assertFalse(self._hits(data, "G30"), data["findings"])

    def test_g30_multiple_subjects_may_share_one_picture(self):
        text = self._ref().replace(
            "<Subject 1> is a woman in <Picture 1>.\n",
            "<Subject 1> is a woman in <Picture 1>.\n<Subject 2> is a child in <Picture 1>.\n",
            1,
        ).replace(
            "<Subject 1> (appears in [Shot 1]): fully_preserved - kept.\n",
            "<Subject 1> (appears in [Shot 1]): fully_preserved - kept.\n"
            "<Subject 2> (appears in [Shot 1]): fully_preserved - kept.\n",
            1,
        )
        code, data = self._run(text, "--refs", "1")
        self.assertEqual(code, 0, data)
        self.assertFalse(self._hits(data, "G30"), data["findings"])

    def test_g30_legacy_unnumbered_identity_image_only_warns_with_refs(self):
        text = self._ref().replace("a woman in <Picture 1>",
                                   "a woman from the character reference image", 1)
        code, data = self._run(text, "--refs", "1")
        self.assertEqual(code, 0, data)
        self.assertEqual([f["level"] for f in self._hits(data, "G30")], ["warn"])

    def test_g32_known_subject_name_prefix_errors_but_normal_mentions_pass(self):
        dialogue = "At 00:00.000, <Subject 1> (S1) says: <d>[Chinese] %s</d> "

        def with_line(line):
            return self._ref(dialogue % line).replace(
                "a woman in <Picture 1>", "豆豆, a toddler in <Picture 1>", 1)

        code, data = self._run(with_line("豆豆：快出来！"))
        self.assertEqual(code, 1, data)
        self.assertEqual([f["level"] for f in self._hits(data, "G32")], ["error"])

        for line in ("豆豆，快出来！", "快出来，豆豆！", "小明：快出来！"):
            with self.subTest(line=line):
                _code, data = self._run(with_line(line))
                self.assertFalse(self._hits(data, "G32"), data["findings"])

    def test_g32_series_aliases_are_recognized(self):
        config = {"characters": [{"id": "gungun", "trigger": "woman", "aliases": ["豆豆", "小豆豆"]}]}
        dialogue = "At 00:00.000, <Subject 1> (S1) says: <d>[Chinese] %s</d> "
        code, data = self._run(self._ref(dialogue % "小豆豆：快出来！"), config=config)
        self.assertEqual(code, 1, data)
        self.assertTrue(self._hits(data, "G32"))
        _code, data = self._run(self._ref(dialogue % "小豆豆，快出来！"), config=config)
        self.assertFalse(self._hits(data, "G32"), data["findings"])

    def test_g15_generic_read_does_not_unlock_chinese(self):
        code, data = self._run(self.BASE % 'The characters on the wall read "豆豆快出来".')
        self.assertEqual(code, 1, data)
        self.assertTrue(self._hits(data, "G15"))

    def test_g15_official_visible_text_and_dialogue_remain_legal(self):
        variants = (
            'A red neon sign reading "营业中" glows above the doorway.',
            'The screen reads "本月新增粉丝零".',
            'A banner reads "出口".',
            'The only permitted on-screen text is "豆豆快出来".',
            'At 00:00.000, a child (S1) says: <d>[Chinese] 豆豆快出来！</d>',
        )
        for body in variants:
            with self.subTest(body=body):
                code, data = self._run(self.BASE % body)
                self.assertEqual(code, 0, data)
                self.assertFalse(self._hits(data, "G15"), data["findings"])

    def test_g15_series_config_allowlist_is_exact(self):
        config = {"visible_text": ["豆豆快出来"]}
        code, data = self._run(self.BASE % 'The characters on the wall read "豆豆快出来".', config=config)
        self.assertEqual(code, 0, data)
        self.assertFalse(self._hits(data, "G15"), data["findings"])
        code, data = self._run(self.BASE % 'The characters on the wall read "别乱写".', config=config)
        self.assertEqual(code, 1, data)
        self.assertTrue(self._hits(data, "G15"))


class VehicleMotionRuleG34(unittest.TestCase):
    """G34:车内景物横向流过 / 车横穿画面 / 摄影机与车平行横移。"""

    REF = AuditGapRegressionTests.REF

    def _hits(self, sentence):
        text = self.REF % sentence
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "g34_141f.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            _code, data = run_gate_json(path)
        return [f for f in data["findings"] if f["rule"] == "G34"]

    def test_interior_scenery_sliding_across_the_frame_is_advisory(self):
        hits = self._hits("Inside the car cabin the trees and lamp posts run steadily backward across the frame.")
        self.assertEqual([h["level"] for h in hits], ["warn"], hits)
        self.assertIn("消失点", hits[0]["message"])

    def test_car_crossing_the_frame_is_a_warning(self):
        hits = self._hits("The grey sedan drives from the left to the right of the street.")
        self.assertEqual([h["level"] for h in hits], ["warn"], hits)

    def test_camera_trucking_beside_the_car_is_a_warning(self):
        hits = self._hits("The camera trucks sideways beside the grey sedan at the same speed.")
        self.assertEqual([h["level"] for h in hits], ["warn"], hits)

    def test_negated_motion_remains_advisory_without_claiming_failure(self):
        for sentence in (
            "In the car, the background never slides sideways across the frame.",
            "In the car, trees grow and sweep out past the edges rather than sliding sideways.",
        ):
            hits = self._hits(sentence)
            self.assertTrue(hits and hits[0]["level"] == "warn", (sentence, hits))

    def test_depth_motion_wording_passes(self):
        hits = self._hits("Inside the car the vanishing point stays fixed while nearer lamp posts grow and leave at the edges.")
        self.assertEqual(hits, [])

    def test_sideways_without_a_vehicle_is_not_this_rules_business(self):
        self.assertEqual(self._hits("The camera trucks sideways along the bookshelf."), [])


class ScreenToCameraRuleG35(unittest.TestCase):
    REF = AuditGapRegressionTests.REF

    def _hits(self, sentence):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "g35_141f.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(self.REF % sentence)
            _code, data = run_gate_json(path)
        return [f for f in data["findings"] if f["rule"] == "G35"]

    def test_phone_turned_to_the_camera_warns(self):
        for sentence in ("He holds the phone up to the camera so the list is readable.",
                         "The phone screen faces toward the camera while he nods.",
                         "He turns the phone to the lens."):
            hits = self._hits(sentence)
            self.assertEqual([h["level"] for h in hits], ["warn"], (sentence, hits))
            self.assertIn("越肩", hits[0]["message"])

    def test_over_the_shoulder_and_back_shell_wording_pass(self):
        for sentence in ("The camera arcs behind his right shoulder and reads the phone screen over it.",
                         "Only the phone's back shell faces toward the camera; the screen stays hidden."):
            self.assertEqual(self._hits(sentence), [], sentence)

    def test_negated_screen_to_camera_is_flagged_as_well(self):
        hits = self._hits("The phone is never turned toward the lens.")
        self.assertEqual([h["level"] for h in hits], ["warn"], hits)


class NegationReminderG36(unittest.TestCase):
    REF = AuditGapRegressionTests.REF

    def _hits(self, sentence):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "g36_141f.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(self.REF % sentence)
            code, data = run_gate_json(path)
        return code, [f for f in data["findings"] if f["rule"] == "G36"]

    def test_body_negations_are_listed_with_a_count_and_do_not_block(self):
        code, hits = self._hits("Nobody walks, steps closer or rocks, and no subtitles appear.")
        self.assertEqual(len(hits), 1, hits)
        self.assertEqual(hits[0]["level"], "warn")
        self.assertIn("不证明正文否定失效", hits[0]["message"])
        self.assertNotEqual(code, 1, "G36 is a reminder, it must not fail the file")

    def test_positive_wording_has_no_g36(self):
        _code, hits = self._hits("Planted in place, she rocks the baby side to side while both elders look down at it.")
        self.assertEqual(hits, [])


class FirstFrameCompositionWordingG31(unittest.TestCase):
    """`opening composition` 把构图帧说成第 0 秒;G31 要提醒,而 composition anchor 写法不触发。"""

    def _hits(self, sentence, rule):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "g31_141f.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(AuditGapRegressionTests.REF % sentence)
            code, data = run_gate_json(path, "--refs", "1")
        return code, [f for f in data["findings"] if f["rule"] == rule]

    def test_opening_composition_wording_is_flagged_and_names_the_fix(self):
        code, hits = self._hits("<Picture 1> is the opening composition of this shot.", "G31")
        self.assertEqual([h["level"] for h in hits], ["warn"], hits)
        self.assertIn("composition anchor", hits[0]["message"])
        self.assertNotEqual(code, 1, "G31 is a reminder, it must not fail the file")

    def test_composition_anchor_wording_is_not_flagged(self):
        _code, hits = self._hits(
            "<Picture 1> is the composition anchor for [Shot 1], reached around 00:04.0.", "G31")
        self.assertEqual(hits, [])


    def _document_hits(self, text):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "g31_declaration_141f.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            _code, data = run_gate_json(path, "--refs", "1")
        return [f for f in data["findings"] if f["rule"] == "G31"]

    def test_first_frame_declaration_in_music_does_not_suppress_opening_warning(self):
        for declared_shot in (1, 99):
            with self.subTest(declared_shot=declared_shot):
                text = (AuditGapRegressionTests.REF % "<Picture 1> is the opening composition of this shot.").replace(
                    "non_diegetic_music:\nN/A",
                    "non_diegetic_music:\n<Picture 1> ([Shot %d] first frame): fully_preserved - kept." % declared_shot, 1)
                self.assertEqual([f["level"] for f in self._document_hits(text)], ["warn"])

    def test_unresolved_shot_in_definition_still_warns(self):
        text = (AuditGapRegressionTests.REF % "").replace(
            "subject_definitions:\n",
            "subject_definitions:\n<Picture 1> is the opening composition.\n", 1).replace(
            "retention_analysis:\n",
            "retention_analysis:\n<Picture 1> ([Shot 1] first frame): fully_preserved - kept.\n", 1)
        self.assertEqual([f["level"] for f in self._document_hits(text)], ["warn"])

    def test_explicit_definition_shot_must_match_retention(self):
        for declared_shot, expected in ((2, []), (1, ["warn"])):
            with self.subTest(declared_shot=declared_shot):
                text = (AuditGapRegressionTests.REF % "").replace(
                    "subject_definitions:\n",
                    "subject_definitions:\n<Picture 1> is the first frame of [Shot 2].\n", 1).replace(
                    "retention_analysis:\n",
                    "retention_analysis:\n<Picture 1> ([Shot %d] first frame): fully_preserved - kept.\n" % declared_shot, 1)
                self.assertEqual([f["level"] for f in self._document_hits(text)], expected)

    def test_malformed_or_embedded_retention_declaration_does_not_suppress(self):
        for entry in (
            "<Picture 1> ([Shot 1] first frame): invalid_marker - kept.",
            "<Picture 1> ([Shot 1] first frame): fully_preserved -",
            "A note quotes <Picture 1> ([Shot 1] first frame): fully_preserved - kept.",
        ):
            with self.subTest(entry=entry):
                text = (AuditGapRegressionTests.REF % "The shot begins from <Picture 1>.").replace(
                    "retention_analysis:\n", "retention_analysis:\n" + entry + "\n", 1)
                self.assertEqual([f["level"] for f in self._document_hits(text)], ["warn"])

    def test_same_picture_in_two_shots_keeps_the_undeclared_shot_warning(self):
        body = ("The shot begins from <Picture 1>. "
                "[Shot 2] At 00:03.000, the camera cuts to another view that begins from <Picture 1>.")
        for declared_shots, expected in (((1,), ["warn"]), ((2,), ["warn"]), ((1, 2), [])):
            with self.subTest(declared_shots=declared_shots):
                entries = "".join("<Picture 1> ([Shot %d] first frame): fully_preserved - kept.\n" % n
                                  for n in declared_shots)
                text = (AuditGapRegressionTests.REF % body).replace(
                    "retention_analysis:\n", "retention_analysis:\n" + entries, 1)
                self.assertEqual([f["level"] for f in self._document_hits(text)], expected)

    def test_first_frame_retention_only_suppresses_the_same_shot(self):
        for declared_shot, expected in ((1, []), (99, ["warn"])):
            with self.subTest(declared_shot=declared_shot):
                text = (AuditGapRegressionTests.REF % "<Picture 1> is the opening composition of this shot.").replace(
                    "retention_analysis:\n",
                    "retention_analysis:\n<Picture 1> ([Shot %d] first frame): fully_preserved - kept.\n" % declared_shot, 1)
                with tempfile.TemporaryDirectory() as d:
                    path = os.path.join(d, "g31_crossshot_141f.txt")
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(text)
                    _code, data = run_gate_json(path, "--refs", "1")
                self.assertEqual([f["level"] for f in data["findings"] if f["rule"] == "G31"], expected, data)

    def test_declared_first_frame_in_retention_is_not_flagged(self):
        text = (AuditGapRegressionTests.REF % "The shot begins from <Picture 1>.").replace(
            "retention_analysis:\n", "retention_analysis:\n<Picture 1> ([Shot 1] first frame): fully_preserved - kept.\n", 1)
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "g31b_141f.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            _code, data = run_gate_json(path, "--refs", "1")
        self.assertEqual([f for f in data["findings"] if f["rule"] == "G31"], [], data["findings"])


class AbsoluteHoldG38(unittest.TestCase):
    """G38: 绝对保持词只列出来让人对照时间线,不判错,不阻断。"""

    def _hits(self, body, mode_ref=True):
        text = AuditGapRegressionTests.REF % body
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "g38_141f.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            code, data = run_gate_json(path)
        return code, [f for f in data["findings"] if f["rule"] == "G38"]

    def test_whole_time_clause_is_listed_once_per_sentence(self):
        code, hits = self._hits(
            "She sits with her left wrist against her jaw the whole time and the whole time her hair stays forward.")
        self.assertEqual(len(hits), 1, hits)
        self.assertEqual(hits[0]["level"], "warn")
        self.assertIn("1 处", hits[0]["message"])
        self.assertNotEqual(code, 1)

    def test_actor_absolute_hold_is_listed_when_she_faces_the_camera(self):
        _code, hits = self._hits(
            "Her left wrist stays against her jaw the whole time while she faces the camera.")
        self.assertEqual([h["level"] for h in hits], ["warn"], hits)

    def test_throughout_spatial_extent_is_not_an_absolute_hold(self):
        for sentence in (
            "At 00:00.000, warm light spreads throughout the room.",
            "People are scattered throughout the garden.",
            "Blue reflections appear throughout the whole room.",
        ):
            with self.subTest(sentence=sentence):
                _code, hits = self._hits(sentence)
                self.assertEqual(hits, [], hits)

    def test_throughout_temporal_extent_still_reminds_for_actor_and_prop(self):
        for sentence in (
            "Her left wrist stays against her jaw throughout the shot while she faces the camera.",
            "The cup stays in her hand throughout the entire clip.",
            "Her left wrist stays against her jaw throughout.",
        ):
            with self.subTest(sentence=sentence):
                _code, hits = self._hits(sentence)
                self.assertEqual([h["level"] for h in hits], ["warn"], hits)

    def test_single_shot_camera_lock_is_not_listed(self):
        _code, hits = self._hits("The camera holds a locked-off medium shot for the entire shot.")
        self.assertEqual(hits, [])

    def test_timestamped_camera_static_lock_is_exempt(self):
        for prefix in ("At 00:00.000, ", "[Shot 1] At 00:00.000, ", "[Shot 1] "):
            with self.subTest(prefix=prefix):
                text = (AuditGapRegressionTests.REF % (
                    prefix + "the camera remains locked-off for the entire shot.")).replace(
                    "[Shot 1] <Subject 1> stands. ", "", 1)
                with tempfile.TemporaryDirectory() as d:
                    path = os.path.join(d, "g38_prefix_141f.txt")
                    with open(path, "w", encoding="utf-8") as fh:
                        fh.write(text)
                    _code, data = run_gate_json(path)
                self.assertEqual([f for f in data["findings"] if f["rule"] == "G38"], [], data)

    def test_timestamped_actor_and_prop_holds_still_warn_with_camera(self):
        for sentence in (
            "At 00:00.000, her left wrist stays against her jaw the whole time while she faces the camera.",
            "At 00:00.000, the camera stays fixed while the cup remains in her hand in every frame.",
        ):
            with self.subTest(sentence=sentence):
                _code, hits = self._hits(sentence)
                self.assertEqual([h["level"] for h in hits], ["warn"], hits)
                self.assertIn("At 00:00.000,", hits[0]["message"])

    def test_prop_absolute_hold_is_listed_when_it_faces_the_camera(self):
        _code, hits = self._hits("The cup handle faces the camera in every frame.")
        self.assertEqual([h["level"] for h in hits], ["warn"], hits)

    def test_camera_lock_does_not_hide_actor_or_prop_holds_in_same_sentence(self):
        for sentence in (
            "The camera stays fixed while her left wrist stays against her jaw the whole time.",
            "The camera stays fixed for the entire shot and the cup remains in her hand in every frame.",
        ):
            with self.subTest(sentence=sentence):
                _code, hits = self._hits(sentence)
                self.assertEqual([h["level"] for h in hits], ["warn"], hits)

    def test_only_camera_static_lock_is_exempt_not_camera_motion(self):
        for sentence, expected in (
            ("The camera remains locked-off for the entire shot.", []),
            ("The camera holds its position throughout the shot.", []),
            ("The camera pushes forward for the entire shot.", ["warn"]),
        ):
            with self.subTest(sentence=sentence):
                _code, hits = self._hits(sentence)
                self.assertEqual([h["level"] for h in hits], expected, hits)

    def test_multi_shot_camera_lock_is_listed(self):
        body = ("The camera holds its distance for the whole shot. "
                "[Shot 2] At 00:03.000, the camera cuts to a close-up of her hands.")
        _code, hits = self._hits(body)
        self.assertEqual(len(hits), 1, hits)

    def test_time_anchored_wording_has_no_g38(self):
        _code, hits = self._hits(
            "Her left hand rests on the table edge until 00:02.000, then rises to her jaw.")
        self.assertEqual(hits, [])


class CutMarkAccumulationTests(unittest.TestCase):
    """G33: --storyboard 秒数累计与切点时刻逐字对账。"""

    BASE = ("integrated_multimodal_description:\n"
            "[Shot 1] A quiet laundry room at dusk. %s\n\n"
            "overall_soundscape:\nA tumble dryer hums throughout.\n\n"
            "non_diegetic_music:\nN/A\n")

    def _run(self, text, seconds_list=None):
        with tempfile.TemporaryDirectory() as d:
            path = os.path.join(d, "g33.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(text)
            args = [path, "--mode", "base", "--seconds", "9.5"]
            if seconds_list is not None:
                sb = os.path.join(d, "sb.json")
                with open(sb, "w", encoding="utf-8") as fh:
                    json.dump(seconds_list, fh)
                args.extend(["--storyboard", sb])
            return run_gate_json(*args)

    @staticmethod
    def _hits(data, rule):
        return [f for f in data["findings"] if f["rule"] == rule]

    def test_matching_cut_marks_pass(self):
        body = ("[Shot 2] At 00:03.000, the shopkeeper studies the ticket. "
                "[Shot 3] At 00:05.500, her fingers tighten.")
        code, data = self._run(self.BASE % body, [3.0, 2.5, 4.0])
        self.assertEqual(code, 0, data)
        self.assertFalse(self._hits(data, "G33"), data["findings"])

    def test_mismatched_cut_mark_reports_written_and_expected(self):
        body = ("[Shot 2] At 00:04.000, the shopkeeper studies the ticket. "
                "[Shot 3] At 00:05.500, her fingers tighten.")
        code, data = self._run(self.BASE % body, [3.0, 2.5, 4.0])
        self.assertEqual(code, 1, data)
        hits = self._hits(data, "G33")
        self.assertTrue(hits)
        self.assertIn("00:04.000", hits[0]["message"])
        self.assertIn("00:03.000", hits[0]["message"])

    def test_missing_cut_mark_names_expected_time(self):
        body = ("[Shot 2] At 00:03.000, the shopkeeper studies the ticket. "
                "[Shot 3] her fingers tighten around the thread.")
        code, data = self._run(self.BASE % body, [3.0, 2.5, 4.0])
        self.assertEqual(code, 1, data)
        hits = self._hits(data, "G33")
        self.assertTrue(hits)
        self.assertIn("00:05.500", hits[0]["message"])

    def test_absent_storyboard_leaves_g33_silent(self):
        body = ("[Shot 2] At 00:09.000, far past any declared sum. "
                "[Shot 3] At 00:05.500, out of order too.")
        code, data = self._run(self.BASE % body, None)
        self.assertFalse(self._hits(data, "G33"), data["findings"])

    def test_shot_beyond_storyboard_is_flagged(self):
        body = ("[Shot 2] At 00:03.000, the shopkeeper studies the ticket. "
                "[Shot 4] At 00:05.500, a ghost shot appears.")
        code, data = self._run(self.BASE % body, [3.0, 2.5])
        self.assertEqual(code, 1, data)
        hits = self._hits(data, "G33")
        self.assertTrue(hits)
        self.assertIn("[Shot 4]", hits[0]["message"])



class PictureNumberingG08cTests(unittest.TestCase):
    """G08c: subject_definitions 里 Picture 编号连续性检查。"""

    def setUp(self):
        self.base = read_fixture("s6_141f.txt")
        self.tmp = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, text):
        path = os.path.join(self.tmp.name, "g08c_141f.txt")
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        return path

    def mutate(self, old, new):
        self.assertIn(old, self.base, "s6 夹具里找不到改动锚点: %r" % old)
        return self.base.replace(old, new, 1)

    def test_consecutive_123_no_trigger(self):
        """连续编号 1, 2, 3 → 不触发 G08c。"""
        # 把 <Picture 1> 独立定义行改成同时含 1, 2, 3 三个 Picture 引用
        text = self.mutate(
            "<Picture 1> is the composition anchor for [Shot 1]:",
            "<Picture 1> is the composition anchor for [Shot 1];"
            " <Picture 2> is a close-up reference; <Picture 3> is the wide reference:",
        )
        code, out = run_gate(self.write(text), "--refs", "3")
        self.assertNotIn("G08c", out)

    def test_gap_1_3_is_legal(self):
        """不连续编号 1, 3（缺 2）合法：官方只要求同类内独立编号，不要求连续。"""
        # 在 <Picture 1> 定义行末尾追加对 <Picture 3> 的引用，跳过 2
        text = self.mutate(
            "<Picture 1> is the composition anchor for [Shot 1]: <Subject 1>",
            "<Picture 1> is the composition anchor for [Shot 1]: <Subject 1>;"
            " see also <Picture 3> for extra reference",
        )
        code, out = run_gate(self.write(text), "--refs", "3")
        self.assertNotIn("G08c", out)

    def test_picture_beyond_refs_count_warns(self):
        """引用了超出 --refs 张数的编号 → G08c warn（模型无从解析这张图）。"""
        text = self.mutate(
            "<Picture 1> is the composition anchor for [Shot 1]: <Subject 1>",
            "<Picture 1> is the composition anchor for [Shot 1]: <Subject 1>;"
            " see also <Picture 3> for extra reference",
        )
        code, out = run_gate(self.write(text), "--refs", "1")
        self.assertIn("G08c", out)
        self.assertRegex(out, r"\[WARN\] G08c ")

    def test_single_picture_no_trigger(self):
        """只有单张 <Picture 1> → 不触发 G08c。"""
        # s6 原始夹具 subject_definitions 只有 <Picture 1>，不做任何修改
        code, out = run_gate(self.write(self.base), "--refs", "1")
        self.assertNotIn("G08c", out)


class RegressionAfterAuditFixes(unittest.TestCase):
    """2026-11-21 双轴复审指出的误伤，逐条钉住。

    每一条都是「按官方写法写反而被判错」的真实场景，回归时不许再退化。
    """

    SHELL = """subject_definitions:
{sd}

summary:
[reference generation] A test shot.

retention_analysis:
{ret}

overall_soundscape:
Quiet room tone throughout, a faint hum from the fridge.

non_diegetic_music:
N/A

detailed_description:
A photorealistic medium shot in soft daylight. The room is plain and evenly lit.
[Shot 1] {body}
"""

    def write_case(self, sd, ret, body="she stands still."):
        text = self.SHELL.format(sd=sd, ret=ret, body=body)
        fd, path = tempfile.mkstemp(suffix="_141f.txt", text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(text)
        self.addCleanup(os.unlink, path)
        return path

    def test_g08_same_line_restatement_is_not_a_redefinition(self):
        """同一行里再写 '<Subject 1> is wearing …' 是补充说明，不是定义两次。"""
        path = self.write_case(
            "<Subject 1> is the boy from <Picture 1>, a small child. "
            "<Subject 1> is wearing a tiny bib.",
            "<Subject 1> (appears in [Shot 1]): fully_preserved - face.",
        )
        code, out = run_gate(path, "--mode", "ref", "--refs", "1", "--frames", "141")
        self.assertNotIn("[ERROR] G08", out)

    def test_g06_multi_picture_subject_is_exempt(self):
        """官方写法 '<Subject 1> is the dog in <Picture 1>, <Picture 2>, and <Picture 3>'
        可以吃多张图，不能反过来要求每张都建独立行。"""
        path = self.write_case(
            "<Subject 1> is the Samoyed in <Picture 1>, <Picture 2>, and <Picture 3>, "
            "a large white fluffy dog.",
            "<Subject 1> (appears in [Shot 1]): fully_preserved - fur.\n"
            "<Picture 2> (appears in [Shot 1]): weak_reference - fur texture only.\n"
            "<Picture 3> (appears in [Shot 1]): weak_reference - build only.",
            body="the dog runs across the yard.",
        )
        code, out = run_gate(path, "--mode", "ref", "--refs", "3", "--frames", "141")
        self.assertNotIn("[ERROR] G06", out)

    def test_g06_video_source_is_exempt(self):
        """官方 ref-en.txt:57 的 '<Subject 1> … whose motion comes from <Video 1>' 同样豁免。"""
        path = self.write_case(
            "<Subject 1> is the woman whose appearance comes from <Picture 1> "
            "and whose walking motion comes from <Video 2>, in a grey coat.",
            "<Subject 1> (appears in [Shot 1]): fully_preserved - face.\n"
            "<Video 2> (appears in [Shot 1]): weak_reference - gait only.",
            body="she walks toward the camera.",
        )
        code, out = run_gate(path, "--mode", "ref", "--refs", "1", "--frames", "141")
        self.assertNotIn("[ERROR] G06", out)

    def test_g41_frame_role_in_second_sentence_is_exempt(self):
        """豁免词写在第二句（'It is also the first frame of [Shot 1]'）不能被句号切掉。"""
        path = self.write_case(
            "<Subject 1> is the woman from <Picture 1>, a young woman.\n"
            "<Picture 2> is the identity reference for <Subject 1>. "
            "It is also the first frame of [Shot 1].",
            "<Subject 1> (appears in [Shot 1]): fully_preserved - face.",
        )
        code, out = run_gate(path, "--mode", "ref", "--refs", "2", "--frames", "141")
        self.assertNotIn("[ERROR] G41", out)

    def test_g06_still_requires_line_for_real_frame_anchor(self):
        """真帧锚/构图锚不在豁免范围：缺独立定义行仍判 G06。"""
        path = self.write_case(
            "<Subject 1> is the woman from <Picture 1>, a young woman.",
            "<Subject 1> (appears in [Shot 1]): fully_preserved - face.\n"
            "<Picture 2> (appears in [Shot 1]): partially_preserved - framing.",
        )
        code, out = run_gate(path, "--mode", "ref", "--refs", "2", "--frames", "141")
        self.assertIn("[ERROR] G06", out)


class MultishotDialogueRules(unittest.TestCase):
    """G40 的三条对白规则，与单镜 G14/G18 同一口径。"""

    def write_multi(self, windows, frames=141):
        fd, path = tempfile.mkstemp(suffix="_%df.txt" % frames, text=True)
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write("\n---\n".join(windows) + "\n")
        self.addCleanup(os.unlink, path)
        return path

    def test_speaker_inherited_within_window_is_not_flagged(self):
        """同一句里 (S1) 引出台词 → 合规，不报缺说话人。"""
        w1 = ("Guga (S1) stands at the door and looks up, then says, "
              "<d>[Chinese] 谢谢妈妈！</d>")
        w2 = "The camera settles on the empty hallway."
        path = self.write_multi([w1, w2])
        code, out = run_gate(path, "--mode", "multishot", "--frames", "141",
                             "--shot-count", "2")
        self.assertNotIn("找不到说话人 ID", out)

    def test_speaker_inherited_from_previous_sentence(self):
        """上一句有 (S1)、本句紧接（≤120 字符）→ 沿用上一句说话人，合规。"""
        w1 = ("Guga (S1) looks up at the door. He says, "
              "<d>[Chinese] 谢谢妈妈！</d>")
        w2 = "The camera settles on the empty hallway."
        path = self.write_multi([w1, w2])
        code, out = run_gate(path, "--mode", "multishot", "--frames", "141",
                             "--shot-count", "2")
        self.assertNotIn("找不到说话人 ID", out)

    def test_silent_window_does_not_trigger_speaker_rule(self):
        """没有对白的窗不进入说话人检查。"""
        w1 = "Guga (S1) says, <d>[Chinese] 走吧。</d>"
        w2 = "The empty lane at dusk, wind over concrete."
        path = self.write_multi([w1, w2])
        code, out = run_gate(path, "--mode", "multishot", "--frames", "141",
                             "--shot-count", "2")
        self.assertNotIn("找不到说话人 ID", out)

    def test_scenetrans_restatement_across_windows_is_exempt(self):
        """两侧都写 <scenetrans> 的跨窗复述是官方要求，不算重复发声。"""
        line = "<d>[Chinese] 我下一站就下车。</d>"
        w1 = ("Guga (S1) says, " + line +
              " <scenetrans> the same voice continues into the next shot.")
        w2 = ("The same voice carries on, <scenetrans> " + line)
        path = self.write_multi([w1, w2])
        code, out = run_gate(path, "--mode", "multishot", "--frames", "141",
                             "--shot-count", "2")
        self.assertNotIn("重复出现且没有 <scenetrans>", out)

    def test_duplicate_line_without_scenetrans_is_flagged(self):
        """没有 <scenetrans> 声明却跨窗重复同一句 → 会念两遍，要提示。"""
        line = "<d>[English] I get off at the next station and walk the rest of the way home.</d>"
        w1 = "A woman (S1) says, " + line
        w2 = "Closer on her hands. She (S1) says, " + line
        path = self.write_multi([w1, w2])
        code, out = run_gate(path, "--mode", "multishot", "--frames", "141",
                             "--shot-count", "2")
        self.assertIn("重复出现且没有 <scenetrans>", out)

class HandoffRemainderRegression(unittest.TestCase):
    """交接单 3.1–3.10 的回归：每条既钉住「该拦的拦」，也钉住「正常写法不拦」。"""

    REF = (
        "subject_definitions:\n<Subject 1> is the woman in <Picture 1>.\n"
        "summary: reference generation.\n"
        "detailed_description:\nLive-action, warm alley light.\n"
        "[Shot 1] At 00:00.000 %s\n"
        "overall_soundscape: Quiet room tone.\nnon_diegetic_music: N/A\n"
        "retention_analysis:\n<Subject 1> (appears in [Shot 1]): fully_preserved - face kept.\n"
    )

    def _run(self, text, *args):
        with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8") as f:
            f.write(text)
            path = f.name
        try:
            return run_gate(path, *args)[1]
        finally:
            os.unlink(path)

    def test_g05_scans_text_before_first_section(self):
        text = "改词单说明:本镜沿用 <Subject 7> 的服装\n" + self.REF % "<Subject 1> walks."
        self.assertRegex(self._run(text, "--mode", "ref", "--seconds", "5"), r"G05.*Subject 7")

    def test_g05_clean_preamble_ok(self):
        text = "# note\n" + self.REF % "<Subject 1> walks."
        self.assertNotIn("G05", self._run(text, "--mode", "ref", "--seconds", "5"))

    def test_g16_dialogue_in_summary(self):
        text = self.REF.replace("summary: reference generation.",
                                "summary: she says <d>[Chinese] 你好呀</d>") % "<Subject 1> (S1) says <d>[Chinese] 你好呀</d>"
        self.assertRegex(self._run(text, "--mode", "ref", "--seconds", "5"), r"G16.*summary")

    def test_g15_menu_and_postfix_verb_allowed(self):
        body = ('<Subject 1> passes a laminated menu reading "牛肉面 12元". '
                'A faded "禁止吸烟" is stencilled on the wall.')
        self.assertNotIn("G15", self._run(self.REF % body, "--mode", "ref", "--seconds", "5"))

    def test_g15_bare_chinese_still_error(self):
        out = self._run(self.REF % "<Subject 1> says 你好 loudly.", "--mode", "ref", "--seconds", "5")
        self.assertIn("G15", out)

    def test_g41b_variants(self):
        for phrase in ("reference image 2", "image 2", "the second reference photo"):
            out = self._run(self.REF % ("<Subject 1> matches the %s closely." % phrase),
                            "--mode", "ref", "--seconds", "5")
            self.assertIn("G41b", out, phrase)

    def test_g41b_duration_use_not_flagged(self):
        out = self._run(self.REF % "<Subject 1> holds the pose for the image 2 seconds later on.",
                        "--mode", "ref", "--seconds", "5")
        self.assertNotIn("G41b", out)

    def test_g42_repeated_identity_phrase(self):
        hair = "her dark chestnut shoulder-length hair soft and voluminous, worn loose"
        body = ("<Subject 1> enters, %s.\nAt 00:02.000 <Subject 1> turns, %s.\n"
                "At 00:03.000 <Subject 1> pauses, %s.") % (hair, hair, hair)
        self.assertIn("G42", self._run(self.REF % body, "--mode", "ref", "--seconds", "5"))

    def test_g42_varied_description_not_flagged(self):
        body = ("<Subject 1> enters, her hair loose over one shoulder.\n"
                "At 00:02.000 <Subject 1> tilts her head, eyes crinkling, flush deepening.\n"
                "At 00:03.000 <Subject 1> presses her lips together and looks away.")
        self.assertNotIn("G42", self._run(self.REF % body, "--mode", "ref", "--seconds", "5"))

    def test_g28_hard_cut_declaration_is_allowed(self):
        base = ("integrated_multimodal_description: [Shot 1] Picture 1 (from Shot 1) is the opening frame. "
                "The woman walks. [Shot 2] At 00:02.000, hard cut to Picture 2 (from Shot 2), the ending frame.\n"
                "overall_soundscape: Quiet.\nnon_diegetic_music: N/A\n")
        self.assertNotIn("G28", self._run(base, "--mode", "base", "--seconds", "4"))

    def test_multishot_window_timestamp_beyond_window(self):
        text = "A medium shot of a woman. At 00:09.000 she turns.\n---\nA medium shot of a door."
        out = self._run(text, "--mode", "multishot", "--frames", "107")
        self.assertRegex(out, r"G40.*第 1 窗时间戳 00:09")

    def test_multishot_offscreen_without_lips_closed(self):
        text = ("A woman faces the lens. An adult voice (S2) answers from off-screen, <d>[Chinese] 不行</d>\n"
                "---\nA medium shot of a door.")
        out = self._run(text, "--mode", "multishot", "--frames", "107")
        self.assertRegex(out, r"G40.*off-screen")

    def test_multishot_offscreen_with_lips_closed_ok(self):
        text = ("A woman faces the lens. An adult voice (S2) answers from off-screen, <d>[Chinese] 不行</d> "
                "Her lips remain completely closed.\n---\nA medium shot of a door.")
        out = self._run(text, "--mode", "multishot", "--frames", "107")
        self.assertNotRegex(out, r"G40.*off-screen")


if __name__ == "__main__":
    unittest.main()
