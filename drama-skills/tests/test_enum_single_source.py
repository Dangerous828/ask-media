"""The single-source contract for the shared creator vocabularies.

`skills/short-drama/scripts/enums.py` is the authority for 景别/近景类/运镜/
画幅/REF 用途. Most consumers live inside the `short-drama` skill and import
it; a few cannot — `short-drama-edit` and `short-drama-produce` must stay
runnable with only their own directory copied, and the dashboard's `app.js`
is JavaScript. Those carry local copies, and this module is what keeps the
copies honest: change `enums.py` without updating every copy named below and
the suite goes red. That is the single-source guarantee the three-model
review asked for (kimi: 「枚举必须单一来源——一个 py/json 文件，md 引用它、
check 导入它、下游 prompt 映射也用它」), executed where import cannot reach.

The second half of the module pins the *warn* behaviour: a 景别 value that
names no known scale word is reported as a warning — never an error — and the
miss rate over the repo's own accepted example projects is recorded as
assertions, so a change in either direction (a vocabulary word lost, or a
new false-positive class) shows up in CI instead of in a creator's terminal.
"""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any

SUITE = Path(__file__).resolve().parents[1]
SKILLS = SUITE / "skills"


def load(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


enums = load("enum_single_source", SKILLS / "short-drama/scripts/enums.py")
creator_views = load(
    "enum_single_source_views", SKILLS / "short-drama/scripts/creator_views.py"
)
creator_markdown_check = load(
    "enum_single_source_checker",
    SKILLS / "short-drama/scripts/creator_markdown_check.py",
)
edit_tool = load(
    "enum_single_source_edit", SKILLS / "short-drama-edit/scripts/edit_tool.py"
)
provider_adapters = load(
    "enum_single_source_providers",
    SKILLS / "short-drama-produce/scripts/provider_adapters.py",
)


class SingleSourceWithinShortDramaTests(unittest.TestCase):
    """The skill that owns enums.py must read them from enums.py."""

    def test_creator_views_reexports_the_shared_scales(self) -> None:
        self.assertEqual(creator_views.SCALES, enums.SHOT_SCALES)
        self.assertEqual(creator_views.CLOSE_SCALES, enums.CLOSE_SCALES)
        # Each module loads its own enums instance (skills are copied alone),
        # so identity cannot hold; the behaviour must. The word list is the
        # same object shape and reads the same words in the same order.
        for framing, expected in (
            ("过肩中近景，桌面高度", "中近景"),
            ("手与茶杯大特写", "大特写"),
            ("角色A近景，三分之四侧", "近景"),
            ("越过右肩看屏幕", ""),
        ):
            self.assertEqual(
                creator_views.shot_scale(framing), expected, framing
            )
            self.assertEqual(enums.shot_scale(framing), expected, framing)

    def test_the_checker_reads_the_ref_purposes_from_enums(self) -> None:
        self.assertEqual(
            creator_markdown_check.REF_PURPOSES, enums.REF_PURPOSES
        )

    def test_the_cut_list_reader_regex_covers_exactly_the_moves(self) -> None:
        # creator_views builds MOVE_RE from enums.CAMERA_MOVES; the edit tool
        # (below) holds the enforced copy. Both must accept the same words.
        for move in enums.CAMERA_MOVES:
            self.assertIsNotNone(creator_views.MOVE_RE.match(f"{move} 8%"))
            self.assertIsNotNone(creator_views.MOVE_RATE_RE.match(f"{move} 2.5%/秒"))
        self.assertIsNone(
            creator_views.MOVE_RE.match("环绕 8%"),
            "a word outside enums.CAMERA_MOVES parsed as a cut-list move",
        )


class EditToolCopyTests(unittest.TestCase):
    """`edit_tool.py` cannot import across the skill boundary; its local copy
    is held word-for-word against enums.py here instead."""

    def test_camera_moves_match(self) -> None:
        self.assertEqual(edit_tool.CAMERA_MOVES, enums.CAMERA_MOVES)

    def test_camera_hold_matches(self) -> None:
        self.assertEqual(edit_tool.CAMERA_HOLD, enums.CAMERA_HOLD)

    def test_camera_opposites_match(self) -> None:
        self.assertEqual(edit_tool.CAMERA_OPPOSITES, enums.CAMERA_OPPOSITES)

    def test_move_limits_match(self) -> None:
        self.assertEqual(
            edit_tool.CAMERA_MOVE_LIMITS, enums.CAMERA_MOVE_AMOUNT_RANGE
        )
        self.assertEqual(
            edit_tool.CAMERA_RATE_LIMITS, enums.CAMERA_MOVE_RATE_RANGE
        )


class ProviderAdapterCopyTests(unittest.TestCase):
    """The provider ratio sets carry their own "adaptive"; the concrete
    ratios must be exactly enums.ASPECT_RATIOS."""

    def test_seedance_ratios_match(self) -> None:
        self.assertEqual(
            provider_adapters.SEEDANCE_RATIOS - {"adaptive"},
            set(enums.ASPECT_RATIOS),
        )

    def test_minimax_ratios_match(self) -> None:
        self.assertEqual(
            provider_adapters.MINIMAX_VIDEO_RATIOS - {"adaptive"},
            set(enums.ASPECT_RATIOS),
        )


class DashboardAppJsCopyTests(unittest.TestCase):
    """app.js is JavaScript, so its tables are parsed and compared here."""

    APP = SKILLS / "short-drama/assets/dashboard/app.js"

    @classmethod
    def setUpClass(cls) -> None:
        text = cls.APP.read_text(encoding="utf-8")
        rung = re.search(
            r"const SCALE_RUNG = \{([^}]*)\}", text
        )
        assert rung is not None, "SCALE_RUNG table not found in app.js"
        cls.rung_words = set(re.findall(r'"([^"]+)"\s*:', rung.group(1)))

    def test_every_scale_has_a_rung(self) -> None:
        self.assertEqual(self.rung_words, set(enums.SHOT_SCALES))

    def test_the_placeholder_diagram_knows_every_scale(self) -> None:
        # placeholderSVG keeps a sizes table of its own; 细节 is drawn by the
        # dedicated branch. Every non-细节 scale needs a figure, and no word
        # outside the vocabulary may appear in either table.
        text = self.APP.read_text(encoding="utf-8")
        sizes = re.search(r"const sizes = \{([^}]*)\}", text)
        assert sizes is not None
        drawn = set(re.findall(r'"([^"]+)"\s*:', sizes.group(1)))
        self.assertEqual(drawn | {"细节"}, set(enums.SHOT_SCALES))


class ShotScaleWarnTests(unittest.TestCase):
    """The warn-level enum check: severity, wording and the known miss rate.

    These assertions are the false-positive ledger. The golden project writes
    creator vocabulary into `framing.size` on every shot; creator-first's
    EP001 writes prose 景别 values with exactly one shot (the over-shoulder
    screen insert) naming no scale word. If a vocabulary change moves either
    number, this file is where the decision gets recorded — not a creator's
    terminal on the night before a delivery.
    """

    def test_a_known_scale_word_in_prose_is_not_a_warning(self) -> None:
        records = [
            {"shot_id": "SHOT-1", "framing": "双人中近景，胸口高度"},
            {"shot_id": "SHOT-2", "framing": {"size": "手与茶杯大特写"}},
        ]
        self.assertEqual(enums.check_enums(records), [])

    def test_an_unknown_value_is_a_warning_never_an_error(self) -> None:
        records = [{"shot_id": "SHOT-1", "framing": {"size": "超近画面"}}]
        warnings = enums.check_enums(records)
        self.assertEqual(len(warnings), 1)
        self.assertEqual(warnings[0]["severity"], "warning")
        self.assertEqual(warnings[0]["code"], "ENUM_SHOT_SCALE_UNKNOWN")
        self.assertIn("enums.py", warnings[0]["message"])

    def test_an_empty_or_missing_framing_is_not_a_warning(self) -> None:
        # 分镜.md's own check already reports a missing 景别 field; the enum
        # check must not pile a second diagnostic onto the same line.
        self.assertEqual(
            enums.check_enums(
                [{"shot_id": "SHOT-1", "framing": ""}, {"shot_id": "SHOT-2"}]
            ),
            [],
        )

    def test_creator_first_example_miss_rate_is_recorded(self) -> None:
        storyboard = (
            SKILLS.parent / "examples/creator-first/EP001/分镜.md"
        ).read_text(encoding="utf-8")
        warnings = creator_markdown_check.enum_warnings(storyboard)
        # 22 shots, one of which (the over-shoulder screen insert) names no
        # scale word. A number above 1 means the vocabulary lost a word; 0
        # means the check stopped reading the field.
        self.assertEqual(len(warnings), 1, [w[:60] for w in warnings])

    def test_the_cli_verdict_line_stays_first_and_the_exit_code_zero(self) -> None:
        # The OK line is the contract the dashboard and the golden tests read;
        # warnings ride behind it and never move the exit code.
        fixture = SUITE / "tests/fixtures/director-v1"
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            episode = project / "剧集/EP900"
            shutil.copytree(fixture / "剧集/EP900", episode)
            shutil.copy2(fixture / "short-drama.json", project / "short-drama.json")
            result = subprocess.run(
                [
                    sys.executable,
                    str(SKILLS / "short-drama/scripts/creator_markdown_check.py"),
                    str(episode),
                    "--project-root",
                    str(project),
                ],
                check=False,
                capture_output=True,
                text=True,
                cwd=SUITE,
            )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(result.stdout.startswith("OK: "), result.stdout)


class GoldenProjectMissRateTests(unittest.TestCase):
    """The JSONL storyboard path: creator vocabulary is a warning, not error."""

    def test_golden_shots_jsonl_creator_vocabulary_warns_on_every_shot(self) -> None:
        path = (
            SUITE
            / "examples/golden-project/剧集/EP001/storyboard/shots.jsonl"
        )
        records = [
            json.loads(line)
            for line in path.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.startswith('{"record_type"')
        ]
        warnings = enums.check_enums(
            [{"shot_id": r.get("shot_id"), "framing": r.get("framing")}
             for r in records]
        )
        # All five golden shots write `medium_or_detail_by_story_job` — an
        # accepted creator vocabulary outside the 8-word list. This is the
        # documented reason the check is a warning today: 5/5 accepted shots
        # would fail a hard enum.
        self.assertEqual(len(warnings), len(records))


if __name__ == "__main__":
    unittest.main()
