#!/usr/bin/env python3
"""story_check 当前分镜格式与 NOTCHK 行为的回归测试。"""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import story_check


HERE = Path(__file__).resolve().parent
STORY_CHECK = HERE / "story_check.py"
PREFLIGHT = HERE / "preflight.py"


class StoryCheckRegressionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.prompts = self.root / "prompts"
        self.prompts.mkdir()

    def tearDown(self):
        self.tmp.cleanup()

    def write_script(self, text, name="分镜.md"):
        path = self.root / name
        path.write_text(text, encoding="utf-8")
        return path

    def write_prompt(self, name, text):
        path = self.prompts / name
        path.write_text(text, encoding="utf-8")
        return path

    def run_cli(self, script, *extra):
        return subprocess.run(
            [sys.executable, str(STORY_CHECK), "--script", str(script),
             "--shots", str(self.prompts), *extra],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

    def test_legacy_format_still_checked(self):
        script = self.write_script(
            """### 镜头 01 (S01) · 拿钥匙
- **H3 动量因果链**：
  ```text
  Alice reaches for the key → Alice lifts the key
  ```
""",
            name="STORYBOARD.md",
        )
        self.write_prompt("S01.txt", "Alice reaches for the key and then lifts the key.")

        result = story_check.check(script, self.prompts)

        self.assertEqual(result["script_shots"], 1)
        self.assertEqual(result["events_total"], 2)
        self.assertEqual(result["status"], "PASS")
        for key in ("script", "shots_dir", "script_shots", "shot_files",
                    "events_total", "events_by_type", "findings"):
            self.assertIn(key, result)

    def test_shot_format_and_inline_unique_action_are_checked(self):
        script = self.write_script(
            """# EP001 分镜

## SHOT-EP001-001 · 转身
- 时长：3s
- 唯一动作：林夏转身并抬起手。
- 视觉依据：《视觉设定.md》·人物「林夏」（控制：动作）。
"""
        )
        self.write_prompt("SHOT-EP001-001.txt", "林夏转身并抬起手。")

        parsed = story_check.parse_script(script)
        result = story_check.check(script, self.prompts)
        completed = self.run_cli(script, "--json")

        self.assertEqual(parsed["shots"][0]["shot_id"], "SHOT-EP001-001")
        self.assertEqual(parsed["shots"][0]["shot_no"], 1)
        self.assertEqual(result["events_total"], 1)
        self.assertEqual(result["status"], "PASS")
        self.assertEqual(completed.returncode, 0, completed.stdout + completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["status"], "PASS")

    def test_empty_script_is_notchk_and_preflight_does_not_pass(self):
        script = self.write_script("# 空分镜\n\n这里没有可识别的镜头或事件。\n")

        completed = self.run_cli(script, "--json")
        payload = json.loads(completed.stdout)
        preflight = subprocess.run(
            [sys.executable, str(PREFLIGHT), "--script", str(script),
             "--shots", str(self.prompts)],
            capture_output=True, text=True, encoding="utf-8", check=False,
        )

        self.assertNotEqual(completed.returncode, 0)
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(payload["status"], "NOTCHK")
        self.assertEqual(payload["script_shots"], 0)
        self.assertEqual(payload["events_total"], 0)
        self.assertGreaterEqual(payload["notchecked_total"], 1)
        self.assertEqual(preflight.returncode, 1, preflight.stdout + preflight.stderr)
        self.assertIn("[NOTCHK]", preflight.stdout)
        self.assertIn("story_check", preflight.stdout)
        self.assertNotRegex(preflight.stdout, r"\[PASS\s*\]\s+story_check")
        self.assertNotIn("全部通过，可以提交", preflight.stdout)

    def test_shot_without_events_is_notchk(self):
        script = self.write_script(
            """## SHOT-EP001-001 · 空动作
- 时长：3s
- 起点：林夏站着。
"""
        )
        self.write_prompt("SHOT-EP001-001.txt", "林夏站着。")

        completed = self.run_cli(script, "--json")
        payload = json.loads(completed.stdout)

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(payload["script_shots"], 1)
        self.assertEqual(payload["events_total"], 0)
        self.assertEqual(payload["status"], "NOTCHK")
        self.assertIn("SCRIPT_EVENTS_NOTCHK",
                      {finding["kind"] for finding in payload["findings"]})

    def test_non_one_to_one_shot_mapping_marks_order_check_notchk(self):
        script = self.write_script(
            """## SHOT-EP001-001 · 第一段
- 唯一动作：林夏转身并抬起手。

## SHOT-EP001-002 · 第二段
- 唯一动作：林夏放下手。
"""
        )
        self.write_prompt("combined.txt", "林夏转身并抬起手，随后放下手。")

        completed = self.run_cli(script, "--json")
        payload = json.loads(completed.stdout)

        self.assertEqual(completed.returncode, 2)
        self.assertEqual(payload["status"], "NOTCHK")
        self.assertIn("ORDER_SKIPPED", {f["kind"] for f in payload["findings"]})
        self.assertGreaterEqual(payload["notchecked_total"], 1)

    def test_visual_settings_and_aliases_drive_handover_check(self):
        script = self.write_script(
            """## SHOT-EP001-001 · 递钥匙
- 唯一动作：林夏把钥匙递给陈默。
- 视觉依据：《视觉设定.md》·人物「林夏」（控制：动作）；人物「陈默」（控制：接物）；道具「钥匙」（控制：交接）。
"""
        )
        (self.root / "视觉设定.md").write_text(
            """# 视觉设定
## 人物 · 林夏
- 画面代称：Lin
## 人物 · 陈默
- 画面代称：Chen
## 道具 · 钥匙
- 画面代称：brass key
""",
            encoding="utf-8",
        )
        prompt = self.write_prompt(
            "SHOT-EP001-001.txt",
            "Lin hands the brass key to Chen. Chen accepts it.",
        )

        passed = story_check.check(script, self.prompts)
        # 中文动作链 + 全英文提示词：§1 中文字面指纹无从比对，记 NOTCHK 交 §3 事件对账。
        # 不得静默当作 PASS（issue #32-4）。
        self.assertEqual(passed["status"], "NOTCHK")
        self.assertIn("SHOT_FINGERPRINT_CROSS_LANG_NOTCHK",
                      {f["kind"] for f in passed["findings"]})
        self.assertEqual(passed["events_by_type"]["handover"], 1)

        prompt.write_text("Lin holds the brass key near Chen.", encoding="utf-8")
        degraded = story_check.check(script, self.prompts)
        self.assertEqual(degraded["status"], "BLOCK")
        self.assertIn("HANDOVER_DEGRADED",
                      {finding["kind"] for finding in degraded["findings"]})

    def test_chinese_chain_english_prompt_is_explicit_notchk(self):
        """中文动作链 + 全英文提示词：不得静默跳过，必须显式 NOTCHK（issue #32-4）。"""
        script = self.write_script(
            """## SHOT-EP001-001 · 递钥匙
- 唯一动作：林夏把钥匙递给陈默。
"""
        )
        self.write_prompt("SHOT-EP001-001.txt",
                          "Lin hands the brass key to Chen. Chen accepts it.")

        result = story_check.check(script, self.prompts)
        kinds = {f["kind"] for f in result["findings"]}
        self.assertIn("SHOT_FINGERPRINT_CROSS_LANG_NOTCHK", kinds)
        self.assertGreaterEqual(result["notchecked_total"], 1)
        self.assertEqual(result["status"], "NOTCHK")

        # CLI 退出码 2（NOTCHK），不得假装 PASS 放行。
        completed = self.run_cli(script, "--json")
        payload = json.loads(completed.stdout)
        self.assertEqual(completed.returncode, 2)
        self.assertEqual(payload["status"], "NOTCHK")

    def test_pure_chinese_action_chain_fingerprint(self):
        """纯中文动作链必须能参与整镜丢失检查，不能静默跳过，也不能因分词粒度误判。"""
        script = self.write_script(
            """## SHOT-EP001-001 · 第一段
- 唯一动作：林夏转身并抬起手。

## SHOT-EP001-002 · 第二段
- 唯一动作：林夏放下手。
"""
        )
        # 两镜内容都在同一份纯中文提示词里 → 全过，不得因中文整串分词误报整镜丢失。
        self.write_prompt("all.txt", "林夏转身并抬起手，随后放下手。")
        result = story_check.check(script, self.prompts)
        self.assertNotIn("SHOT_CONTENT_MISSING",
                         {f["kind"] for f in result["findings"]})

        # 第二镜内容真实丢失 → 必须判 error（中文指纹确实在工作，而非跳过）。
        for p in self.prompts.glob("*.txt"):
            p.write_text("林夏转身并抬起手。", encoding="utf-8")
        lost = story_check.check(script, self.prompts)
        self.assertIn("SHOT_CONTENT_MISSING",
                      {f["kind"] for f in lost["findings"]})

    def test_unresolvable_handover_assets_are_notchk(self):
        script = self.write_script(
            """## SHOT-EP001-001 · 交接
- 唯一动作：甲把物品递给乙。
"""
        )
        self.write_prompt("SHOT-EP001-001.txt", "甲把物品递给乙。")

        result = story_check.check(script, self.prompts)

        self.assertEqual(result["status"], "NOTCHK")
        self.assertGreaterEqual(result["notchecked_total"], 1)
        self.assertIn("HANDOVER_ASSETS_NOTCHK",
                      {finding["kind"] for finding in result["findings"]})


if __name__ == "__main__":
    unittest.main()
