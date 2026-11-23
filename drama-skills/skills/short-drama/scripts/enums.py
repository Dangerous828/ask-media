#!/usr/bin/env python3
"""Single source for the shared creator-facing vocabularies.

景别、近景类、运镜行为与剪辑单运镜语法，此前散落在多个文档和脚本里：
`creator_views.py` 定义了 SCALES/CLOSE_SCALES，`edit_tool.py` 定义了
CAMERA_MOVES/CAMERA_HOLD，dashboard 的 `app.js` 各自维护了一份 JS 表，
`shot-craft.md` 和 `still-cuts.md` 用散文描述同一批词。谁多收或少收一
档，半年后就对不上——这是三家模型审查一致指出的 drift 面。

本文件是这些词的权威来源：

* 文档不再各自维护完整清单，只注明「权威来源是本文件」；
* 校验脚本从这里导入；
* 下游 prompt 映射（分镜 → 图片/视频提示词）也从这里读词表。

**跨 skill 边界**：skills 必须保持「单独复制自己的目录即可运行」，所以
`short-drama-edit` 的 ``edit_tool.py`` 与 `short-drama-produce` 的
``provider_adapters.py`` 不在本文件里 import 这些常量（与它们各自的
REFERENCE RESOLVER 块同一条惯例）。它们保留本地定义，而
``tests/test_enum_single_source.py`` 把每一份本地拷贝与这里逐词比对：
改这里不改那里，测试就红。单一来源由测试执行，不由 import 执行。

`tests/test_enum_single_source.py` 还把 `app.js` 里的 JS 表与这里逐词比
对，所以前端表格也由本文件间接约束。

词表语义（分档依据见 `short-drama-storyboard/references/shot-craft.md`
的「景别」一节）：

* ``SHOT_SCALES`` —— 景别，由远及近排列。中近景是中景与近景之间独立
  的一档（竖屏短剧的实际工作景别），细节镜头与大特写分开。
* ``CLOSE_SCALES`` —— 近景类：节奏档案 ``close_shot_share_min`` 计数的
  档位（近景、特写、大特写、细节）。中近景不算近景类。
* ``CAMERA_HOLD`` / ``CAMERA_MOVES`` —— 剪辑单的运镜语法：固定，或
  推近/拉远/左移/右移/上移/下移加百分比幅度或速度。
* ``CAMERA_OPPOSITES`` —— 相邻两段不得互为反向（still-cuts.md）。
* ``ASPECT_RATIOS`` —— 项目画幅（project_tool 的 --aspect-ratio 与
  provider 适配器共享的取值域）。

创作层（分镜的「景别/机位」「运镜」）允许自由散文——「缓推」「双人
中近景」这类表述是合法的创作者语言，不在本词表内也不报错；执行层
（剪辑单）才收封闭枚举。校验据此分两档：执行层枚举外的词按错误处理
（edit_tool 既有行为），创作层枚举外的词只在明显是笔误形态（如「大特
写」写成「大特远近」这类完全不含任何已知景别词的字符串）时给 warning，
先收集误伤数据再决定是否升级——见 `check_enums` 的 docstring。
"""

from __future__ import annotations

import re
from typing import Any

MINIMUM_PYTHON = (3, 9)
import sys

if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit(
        "short-drama needs Python {}.{} or newer; this interpreter is {}.{}".format(
            *MINIMUM_PYTHON, sys.version_info.major, sys.version_info.minor
        )
    )

# ---------------------------------------------------------------- shot size

# Ordered far to close. 中近景 is its own rung between 中景 and 近景.
SHOT_SCALES = ("远景", "全景", "中景", "中近景", "近景", "特写", "大特写", "细节")
# The rhythm profile's close_shot_share_min counts exactly these (develop's
# episode-design reference): 近景、特写、大特写与细节镜头. 中近景 is not one.
CLOSE_SCALES = frozenset({"近景", "特写", "大特写", "细节"})
# Longest words first, so 中近景 and 大特写 are read whole instead of as the
# 近景 or 特写 inside them.
_SCALE_RE = re.compile("|".join(sorted(SHOT_SCALES, key=len, reverse=True)))

# ------------------------------------------------------------------ camera

# 「运镜：推近 8%」 moves the frame across a still. Past 30% the picture is
# mostly crop; the edit contract caps the amount there (edit_tool.py).
CAMERA_HOLD = "固定"
CAMERA_MOVES = ("推近", "拉远", "左移", "右移", "上移", "下移")
CAMERA_OPPOSITES = {
    "推近": "拉远",
    "拉远": "推近",
    "左移": "右移",
    "右移": "左移",
    "上移": "下移",
    "下移": "上移",
}
# The amount/rate bounds a still's camera move may carry (edit_tool.py, and
# still-cuts.md documents the same numbers to the creator).
CAMERA_MOVE_AMOUNT_RANGE = (1, 30)
CAMERA_MOVE_RATE_RANGE = (0.1, 10.0)

# ------------------------------------------------------------------ format

# The aspect ratios a project may declare (project_tool --aspect-ratio); the
# provider adapters accept the same set plus their own "adaptive".
ASPECT_RATIOS = ("1:1", "3:4", "4:3", "9:16", "16:9", "21:9")

# The ref-slot 用途 vocabulary of creator_markdown_check.py, mirrored here so
# reference-roles.md can point at one place for both the doc and the checker.
REF_PURPOSES = (
    "身份",
    "造型状态",
    "地理",
    "构图",
    "尺度",
    "效果",
    "起始帧",
    "结束帧",
    "风格",
)


def shot_scale(framing: str) -> str:
    """The first shot-size word in a 景别/机位 value, or "" when none is named.

    Longer words are tried first at each position, so 中近景 and 大特写 are read
    whole instead of as the 近景 or 特写 inside them.
    """

    match = _SCALE_RE.search(framing or "")
    return match.group(0) if match else ""


def scale_regex_pattern() -> str:
    """The alternation every scale-matching regex should be built from.

    `creator_views.py` used to hand-write ``re.compile("大特写|中近景|远景|…")``;
    exporting the joined pattern keeps any future consumer in step with
    ``SHOT_SCALES`` without each one rebuilding (and mis-ordering) it.
    """

    return "|".join(sorted(SHOT_SCALES, key=len, reverse=True))


def is_close_scale(scale: str) -> bool:
    return scale in CLOSE_SCALES


def check_enums(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Warn-level enum conformance for creator-side shot records.

    Only fields that claim to carry a shot size are examined: the storyboard's
    ``framing.size`` (JSONL path) and the creator markdown's 「景别/机位」 value
    (detected upstream and passed as ``framing`` on the record). A value that
    contains at least one known scale word is accepted, whatever else it says —
    「双人中近景，胸口高度」 is creator prose, not an enum violation.

    A value with *no* known scale word is reported as a warning, never an
    error: the golden project's own accepted records write
    ``medium_or_detail_by_story_job``, and until the miss rate over real
    projects is known, blocking on the enum would trade a small catch rate for
    a certain false-positive rate. The warning count is the data that decides
    the later promotion to an error — see the review consensus this file
    answers (kimi: 「先 warn、后 hard-fail」).
    """

    warnings: list[dict[str, Any]] = []
    for record in records:
        shot_id = record.get("shot_id") or record.get("id") or "?"
        framing = record.get("framing")
        if isinstance(framing, dict):
            value = framing.get("size")
        else:
            value = framing
        if not isinstance(value, str) or not value.strip():
            continue
        if shot_scale(value):
            continue
        warnings.append(
            {
                "code": "ENUM_SHOT_SCALE_UNKNOWN",
                "severity": "warning",
                "shot_id": shot_id,
                "value": value,
                "message": (
                    f"景别值「{value}」不包含任何已知景别词"
                    f"（{'、'.join(SHOT_SCALES)}）；"
                    "若是创作者自定词汇可忽略本警告，若是笔误请改用已知景别词。"
                    "词表权威来源：skills/short-drama/scripts/enums.py"
                ),
            }
        )
    return warnings
