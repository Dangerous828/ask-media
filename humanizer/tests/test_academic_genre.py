#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""语体档回归测试。

跑法：
    python3 tests/test_academic_genre.py

守四条边界：
1. general 档与上游 detect.py 行为一致（等级表 = REGEX_HITS 原样）。
2. academic 档恰好把 ACADEMIC_DEMOTE 里 6 条降到 C，其余等级不动。
3. X 级（已否决）在两个档位都保持 X——降级绝不能把它们变成可改项。
4. 论文核查清单只在 academic 报告出现，且明确写出「脚本未核实」。
5. report.py 能用两个档位的 --json 存档出报告，不抛异常、不丢分级节。

本测试不依赖外部网络与第三方库，只用标准库。
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import detect  # noqa: E402
import report  # noqa: E402

SAMPLE = """# 3 方法

## 3.1 实验设置

目的：验证所提方法在不同数据规模下的表现。方法：采用三组对照实验，分别使用 1000、5000 与 10000 个样本。结果：在样本量为 10000 时，准确率达到 0.912。

对于小规模数据集来说，模型的收敛速度较慢。因此，我们增加了预热轮数。此外，在特征维度方面，本文采用主成分分析进行降维。当训练轮数超过 50 时，损失曲线趋于平稳。

本研究使用一种基于多头自注意力机制的、面向长文本序列的层级化编码结构，该结构在保持计算复杂度不变的前提下提升了表示能力。实验涉及准确率、召回率、F1 值、AUC 以及推理时延五项指标，各项指标的统计量均在表 2 中给出。

值得注意的是，该方法的性能提升幅度有限。综上所述，所提框架在多数设定下均能取得稳定表现，这为后续研究奠定了基础，具有里程碑意义。

## 3.2 结果分析

如表 2 所示，本文方法在三个数据集上均有提升。这意味着所提模块具备一定泛化能力。我们将学习率、批大小、权重衰减、丢弃率、预热比例依次设为 1e-4、32、0.01、0.1、0.06。

研究表明，此类结构能够显著改善长程依赖建模。实验结果显示：在阈值取 0.5 时，F1 达到最优。换言之，阈值选择对最终表现具有明显影响。
""" * 3


def run_detect(path: Path, genre: str) -> str:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "detect.py"), str(path),
         "--genre", genre, "--max-hits", "1"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return proc.stdout


def run_json(path: Path, genre: str) -> dict:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts" / "detect.py"), str(path),
         "--genre", genre, "--json"],
        capture_output=True, text=True, encoding="utf-8", check=True,
    )
    return json.loads(proc.stdout)


class GenreTests(unittest.TestCase):

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.paper = Path(self.tmp.name) / "paper.md"
        self.paper.write_text(SAMPLE, encoding="utf-8")

    def tearDown(self):
        self.tmp.cleanup()

    # 1 general 档等级表原样
    def test_general_levels_unchanged(self):
        general = detect.effective_levels("general")
        expected = {nm: lv for lv, nm, *_ in detect.REGEX_HITS}
        self.assertEqual(general, expected,
                         "general 档必须逐项等于上游 REGEX_HITS 的级别")
        self.assertNotIn("degraded", general)

    def test_general_report_has_no_genre_marker(self):
        out = run_detect(self.paper, "general")
        self.assertIn("[A] 机械改候选", out)
        self.assertNotIn("语体档：academic", out)
        self.assertNotIn("[论文核查]", out)
        self.assertNotIn("语体保留·降 C", out)

    # 2 academic 档精确降级
    def test_academic_demotes_exactly_six(self):
        general = detect.effective_levels("general")
        academic = detect.effective_levels("academic")
        changed = {nm for nm in general if general[nm] != academic[nm]}
        self.assertEqual(changed, set(detect.ACADEMIC_DEMOTE),
                         "只有 ACADEMIC_DEMOTE 列出的规则才允许变级")
        for nm in changed:
            self.assertEqual(academic[nm], "C", f"{nm} 必须降为 C 只报告")

    def test_academic_report_moves_demoted_to_c(self):
        out = run_detect(self.paper, "academic")
        self.assertIn("语体档：academic", out)
        self.assertIn("[C] 只报告（默认不改）", out)
        self.assertIn("[语体保留·降 C]", out)
        # 本样本的命中全是降级项，A/B 区应整段消失
        self.assertNotIn("[A] 机械改候选", out)
        self.assertNotIn("[B] 建议改候选", out)
        # 降级项出现在 C 区，且带降级理由
        c_sec = out.split("[C] 只报告（默认不改）")[1].split("[X]")[0]
        for nm in ("顿号并列≥3", "前置话题壳", "当…时从句"):
            self.assertIn(nm, c_sec)

    # 3 X 级恒定
    def test_x_level_never_changes(self):
        for genre in ("general", "academic"):
            levels = detect.effective_levels(genre)
            for lv, nm, *_ in detect.REGEX_HITS:
                if lv == "X":
                    self.assertEqual(levels[nm], "X",
                                     f"{nm} 在 {genre} 档被改级了")

    def test_x_rules_present_in_academic_report(self):
        out = run_detect(self.paper, "academic")
        self.assertIn("[X] 已否决特征", out)
        self.assertIn("这意味着", out)
        self.assertIn("概括替代", out)

    # 4 论文核查清单
    def test_paper_checks_only_in_academic(self):
        out = run_detect(self.paper, "academic")
        self.assertIn("[论文核查]", out)
        for name, _ in detect.ACADEMIC_PAPER_CHECKS:
            self.assertIn(name, out)
        self.assertIn("脚本查不到这一层", out)
        self.assertIn("报告不等于已通过核查", out)

    def test_paper_checks_absent_in_general(self):
        self.assertNotIn("[论文核查]", run_detect(self.paper, "general"))

    def test_academic_synonym_wording_is_terminology(self):
        out = run_detect(self.paper, "academic")
        self.assertIn("[术语核对]", out)
        self.assertIn("术语必须统一", out)
        self.assertNotIn("[B] 用词不敢重复", out)

    # 5 JSON 契约与 report.py 兼容
    def test_json_has_genre_and_levels(self):
        for genre in ("general", "academic"):
            d = run_json(self.paper, genre)
            self.assertEqual(d["genre"], genre)
            self.assertEqual(d["levels"], detect.effective_levels(genre))
            self.assertEqual(d["demoted"] != {}, genre == "academic")

    def test_report_md_both_genres(self):
        for genre in ("general", "academic"):
            d = run_json(self.paper, genre)
            with self.subTest(genre=genre):
                page = report.build_report_md(
                    SAMPLE, SAMPLE, d, d, None, "改前.md", "改后.md")
                self.assertIn("分级问题清单", page)
                self.assertIn("论文核查", page) if genre == "academic" \
                    else self.assertNotIn("论文核查", page)
                self.assertIn("语体保留" if genre == "academic" else "机械改", page)

    def test_report_html_both_genres(self):
        for genre in ("general", "academic"):
            d = run_json(self.paper, genre)
            with self.subTest(genre=genre):
                page = report.build_report(
                    SAMPLE, SAMPLE, d, d, None, "改前.md", "改后.md")
                self.assertIn("分级问题清单", page)
                self.assertEqual("论文核查" in page, genre == "academic")

    # 边界：候选抽取不受语体影响
    def test_candidates_still_work(self):
        proc = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "detect.py"), str(self.paper),
             "--genre", "academic", "--candidates", "--json"],
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        payload = json.loads(proc.stdout)
        self.assertIn("meta", payload)
        self.assertIn("n_candidates", payload["meta"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
