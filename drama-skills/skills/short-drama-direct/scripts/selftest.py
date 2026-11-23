#!/usr/bin/env python3
"""Offline tests for the director-v1 Markdown checker."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from director_check import check_director, validate_episode

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("selftest.py requires Python 3.9 or newer")

SCREENPLAY = "# EP001\n\n## EP001-SC001 内 · 洗衣房 · 清晨\n\n角色A摊开右手。\n"
DIRECTOR = """# EP001 导演方案

## EP001-SC001 · 证物先于解释

- 戏剧行动：角色A要让角色B看见证物；角色B先按取衣流程接待；角色A用沉默和摊手推进。
- 转折与承受：牌背线头显露；角色B停手并重新理解来意；离场时她无法继续按流程应对。
- 观众知情：先看见拒绝递交，再随角色B看见线头，最后才给血迹细节。
- 观看方案：同一柜台空间保留双方动作和反应，只有证据需要辨认时切近。
- 空间与声音：柜台分隔双方；角色A右手持牌、左手空；角色B杯在台面；停机引导注意。叙事必需：两人在场、牌在角色A手里、牌背线头可见；允许偏差：杯子位置、柜台陈设。

### 镜头计划

| Shot | 来源与职责 | 入场状态 | 主要变化 | 离场状态与交接 |
|---|---|---|---|---|
| SHOT-EP001-001 | EP001-SC001；让观众先见拒绝再见证物 | 角色A右手握牌，角色B擦杯 | 停机后角色A摊手，角色B停手 | 牌背朝上未易手，交给证据近景 |
"""
# Plan-2/plan-3 schema: ID-declared 叙事必需, a 6th 承载 column and per-cell
# state ledgers. Every guard this schema buys has one positive and at least
# one negative case below.
SCHEMA_DIRECTOR = """# EP001 导演方案

## EP001-SC001 · 证物先于解释

- 戏剧行动：角色A要让角色B看见证物；角色B先按取衣流程接待；角色A用沉默和摊手推进。
- 转折与承受：牌背线头显露；角色B停手并重新理解来意；离场时她无法继续按流程应对。
- 观众知情：先看见拒绝递交，再随角色B看见线头，最后才给血迹细节。
- 观看方案：同一柜台空间保留双方动作和反应，只有证据需要辨认时切近。
- 空间与声音：柜台分隔双方；角色A右手持牌、左手空；角色B杯在台面；停机引导注意。叙事必需：N1=牌背线头在摊手后可读 [实体:角色A,取衣牌]；N2=牌在角色A手里 [实体:角色A,取衣牌]；允许偏差：杯子位置、柜台陈设。

### 镜头计划

| Shot | 来源与职责 | 入场状态 | 主要变化 | 离场状态与交接 | 承载 |
|---|---|---|---|---|---|
| SHOT-EP001-001 | EP001-SC001；让观众先见拒绝再见证物 | 角色A右手握牌，角色B擦杯 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交] | 停机后角色A摊手，角色B停手 | 牌背朝上未易手 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头] | N1、N2 |
"""
SHOT = """## SHOT-EP001-001 · 摊手
- 来源：EP001-SC001
- 时长：6s
- 起点：右手握牌。
- 终点：牌背朝上。

### 观众 reads
| Read | 时间窗 | 观众要理解什么 | 注意如何到达 | 停留与承接 |
|---|---|---|---|---|
| R1 | 0.0–2.0s | 角色A拒绝按流程交牌 | 角色B的问话与角色A的沉默先后落下 | 停顿后停机引导右手 |
| R2 | 2.0–6.0s | 牌背线头改变角色B的判断 | 右手摊开后角色B停手 | 留时间看见她的反应，再切证据 |

### 画面证明计划
| Frame | role | read | 时刻 | 证明责任 | 生产/审查用途 |
|---|---|---|---|---|---|
| KF-001-START | start | R1 | 0.0s | 右拳持牌、牌背朝角色B | 首帧 |
| KF-001-POSE | pose_proof | R2 | 3.0s | 摊掌与角色B停手同时可读 | 仅关键姿势审查 |
| KF-001-END | end | R2 | 6.0s | 牌未易手且牌背朝上 | 尾帧 |

### 冻结关键帧提示词
> 右拳持牌。

### 关键姿势提示词
#### KF-001-POSE
> 摊掌与角色B停手。

### 收尾关键帧提示词
> 牌背朝上。
"""


def codes(document: str = SHOT) -> list[str]:
    return check_director(DIRECTOR, SCREENPLAY, document)


def schema_codes(document: str = SHOT) -> list[str]:
    return check_director(SCHEMA_DIRECTOR, SCREENPLAY, document)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def main() -> int:
    require(codes() == [], "the valid director-v1 example must pass")

    require(any("缺少场景导演条目" in error for error in check_director("", SCREENPLAY, SHOT)), "missing scene")
    missing_field = DIRECTOR.replace("- 观众知情：先看见拒绝递交，再随角色B看见线头，最后才给血迹细节。\n", "")
    require(any("缺少观众知情" in error for error in check_director(missing_field, SCREENPLAY, SHOT)), "missing field")
    require(any("未出现在导演镜头计划" in error for error in codes(SHOT.replace("SHOT-EP001-001", "SHOT-EP001-999"))), "unplanned shot")

    gap = SHOT.replace("R2 | 2.0–6.0s", "R2 | 2.5–6.0s")
    require(any("无缺口无重叠" in error for error in codes(gap)), "read gap")
    overlap = SHOT.replace("R2 | 2.0–6.0s", "R2 | 1.5–6.0s")
    require(any("无缺口无重叠" in error for error in codes(overlap)), "read overlap")
    wrong_total = SHOT.replace("R2 | 2.0–6.0s", "R2 | 2.0–5.0s")
    require(any("应完整覆盖本镜" in error for error in codes(wrong_total)), "read total")
    wrong_read = SHOT.replace("KF-001-POSE | pose_proof | R2", "KF-001-POSE | pose_proof | R9")
    require(any("引用不存在的 read R9" in error for error in codes(wrong_read)), "unknown read")

    early_start = SHOT.replace("KF-001-START | start | R1 | 0.0s", "KF-001-START | start | R1 | 1.0s")
    require(any("start 必须在 0s" in error for error in codes(early_start)), "start boundary")
    pose_at_start = SHOT.replace("KF-001-POSE | pose_proof | R2 | 3.0s", "KF-001-POSE | pose_proof | R2 | 0.0s")
    require(any("不得冒充首/尾帧" in error for error in codes(pose_at_start)), "pose at start")
    wrong_end = SHOT.replace("KF-001-END | end | R2 | 6.0s", "KF-001-END | end | R2 | 5.0s")
    require(any("end 必须在镜末" in error for error in codes(wrong_end)), "end boundary")
    no_pose_text = SHOT.split("### 关键姿势提示词")[0] + "### 收尾关键帧提示词\n> 牌背朝上。\n"
    require(any("缺少关键姿势提示词" in error for error in codes(no_pose_text)), "missing pose text")
    no_end = SHOT.replace("| KF-001-END | end | R2 | 6.0s | 牌未易手且牌背朝上 | 尾帧 |\n", "")
    require(any("end 计划与收尾" in error for error in codes(no_end)), "end mismatch")
    duplicate_start = SHOT.replace(
        "| KF-001-POSE | pose_proof | R2 | 3.0s | 摊掌与角色B停手同时可读 | 仅关键姿势审查 |",
        "| KF-001-START-2 | start | R1 | 0.0s | 第二个错误起点 | 首帧 |",
    )
    require(any("最多有一个 start" in error for error in codes(duplicate_start)), "duplicate start")
    wrong_pose_heading = SHOT.replace("#### KF-001-POSE", "#### KF-WRONG")
    require(any("关键姿势标题与 pose_proof 计划不一致" in error for error in codes(wrong_pose_heading)), "pose heading mismatch")

    no_start = SHOT.replace("| KF-001-START | start | R1 | 0.0s | 右拳持牌、牌背朝角色B | 首帧 |\n", "")
    require(any("缺少 start" in error for error in codes(no_start)), "missing start")

    omitted = check_director(
        DIRECTOR,
        SCREENPLAY + "\n## EP001-SC090 内 · 走廊 · 夜\n\n过场。\n",
        "# EP001 分镜\n\n- 未拍场次：EP001-SC090（理由：与主场重复:同一动作）\n" + SHOT,
    )
    require(omitted == [], f"a reasoned unfilmed scene must be accepted: {omitted}")

    with tempfile.TemporaryDirectory() as directory:
        episode = Path(directory)
        (episode / "剧本.md").write_text(SCREENPLAY, encoding="utf-8")
        (episode / "分镜.md").write_text(SHOT, encoding="utf-8")
        require(validate_episode(episode) == [], "legacy episode remains on legacy path")
        (episode / "导演.md").write_text(DIRECTOR, encoding="utf-8")
        require(validate_episode(episode) == [], "director file opts an old episode into v1")

    # ---- plan 2: carried_by reference integrity ----
    require(schema_codes() == [], "the ID-schema example must pass")
    unknown_nid = SCHEMA_DIRECTOR.replace("| N1、N2 |", "| N1、N9 |")
    require(
        any("承载列引用了未声明的 N-ID N9" in error for error in check_director(unknown_nid, SCREENPLAY, SHOT)),
        "unknown N-ID",
    )
    uncarried = SCHEMA_DIRECTOR.replace("| N1、N2 |", "| 无 |")
    require(
        any("没有任何镜头承载" in error for error in check_director(uncarried, SCREENPLAY, SHOT)),
        "uncarried necessity",
    )
    skipped_column = SCHEMA_DIRECTOR.replace(" | N1、N2 |", " |", 1)
    require(
        any("必须带承载列" in error for error in check_director(skipped_column, SCREENPLAY, SHOT)),
        "row skipping the carrier column",
    )
    orphan_carrier = SCHEMA_DIRECTOR.replace(
        "叙事必需：N1=牌背线头在摊手后可读 [实体:角色A,取衣牌]；N2=牌在角色A手里 [实体:角色A,取衣牌]；",
        "叙事必需：牌背线头在摊手后可读、牌在角色A手里；",
    )
    require(
        any("未声明任何 N-ID" in error for error in check_director(orphan_carrier, SCREENPLAY, SHOT)),
        "carrier column without declared IDs",
    )

    # ---- plan 3: the per-beat state ledger ----
    one_sided = SCHEMA_DIRECTOR.replace(
        "牌背朝上未易手 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
        "牌背朝上未易手",
    )
    require(
        any("必须成对声明" in error for error in check_director(one_sided, SCREENPLAY, SHOT)),
        "one-sided ledger",
    )
    bad_holder = SCHEMA_DIRECTOR.replace("持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头", "持有:取衣牌; 知情:观众=拒绝递交、观众=牌背线头")
    require(
        any("持有项必须形如" in error for error in check_director(bad_holder, SCREENPLAY, SHOT)),
        "malformed holding item",
    )
    non_audience = SCHEMA_DIRECTOR.replace("知情:观众=拒绝递交、观众=牌背线头", "知情:角色B=牌背线头")
    require(
        any("知情项暂只支持" in error for error in check_director(non_audience, SCREENPLAY, SHOT)),
        "non-audience knowledge",
    )

    # A second planned shot exercises the cross-cut diff: continuity kept,
    # then each of the three reversals.
    TWO_SHOT_DIRECTOR = SCHEMA_DIRECTOR.replace(
        "| SHOT-EP001-001 | EP001-SC001；让观众先见拒绝再见证物 | 角色A右手握牌，角色B擦杯 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交] | 停机后角色A摊手，角色B停手 | 牌背朝上未易手 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头] | N1、N2 |\n",
        "| SHOT-EP001-001 | EP001-SC001；让观众先见拒绝再见证物 | 角色A右手握牌，角色B擦杯 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交] | 停机后角色A摊手，角色B停手 | 牌背朝上未易手 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头] | N1、N2 |\n"
        "| SHOT-EP001-002 | EP001-SC001；让角色B的反应在近景里落定 | 角色B停着的手与牌背同框 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头] | 角色B先辨认线头再看人 | 角色B没有拿牌 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头] | N1 |\n",
    )
    TWO_SHOT_STORYBOARD = SHOT + "\n" + SHOT.replace(
        "## SHOT-EP001-001 · 摊手", "## SHOT-EP001-002 · 反应"
    ).replace("来源：EP001-SC001", "来源：EP001-SC001").replace(
        "KF-001-START", "KF-002-START"
    ).replace("KF-001-POSE", "KF-002-POSE").replace("KF-001-END", "KF-002-END")
    # The second shot reuses the reads/keyframe grammar of the first, which
    # is all check_director needs; the exit 知情 (拒绝递交、牌背线头) matches
    # the second shot's entry, so the clean two-shot plan passes.
    require(
        check_director(TWO_SHOT_DIRECTOR, SCREENPLAY, TWO_SHOT_STORYBOARD) == [],
        f"the two-shot ledger example must pass: {check_director(TWO_SHOT_DIRECTOR, SCREENPLAY, TWO_SHOT_STORYBOARD)}",
    )
    handover_reversed = TWO_SHOT_DIRECTOR.replace(
        "角色B停着的手与牌背同框 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
        "角色B停着的手与牌背同框 [在场:角色A,角色B; 持有:角色B=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
    )
    require(
        any("持有延续断裂" in error for error in check_director(handover_reversed, SCREENPLAY, TWO_SHOT_STORYBOARD)),
        "prop reversed across the cut",
    )
    presence_lost = TWO_SHOT_DIRECTOR.replace(
        "角色B停着的手与牌背同框 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
        "角色B停着的手与牌背同框 [在场:角色A; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
    )
    require(
        any("在场延续断裂" in error for error in check_director(presence_lost, SCREENPLAY, TWO_SHOT_STORYBOARD)),
        "presence lost across the cut",
    )
    knowledge_forgotten = TWO_SHOT_DIRECTOR.replace(
        "角色B停着的手与牌背同框 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
        "角色B停着的手与牌背同框 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交]",
    )
    require(
        any("知情在切点消失" in error for error in check_director(knowledge_forgotten, SCREENPLAY, TWO_SHOT_STORYBOARD)),
        "knowledge forgotten across the cut",
    )
    knowledge_shrinking = TWO_SHOT_DIRECTOR.replace(
        "牌背朝上未易手 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
        "牌背朝上未易手 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=牌背线头]",
    )
    require(
        any("知情单调被破坏" in error for error in check_director(knowledge_shrinking, SCREENPLAY, TWO_SHOT_STORYBOARD)),
        "knowledge shrinking inside a shot",
    )
    knowledge_early = TWO_SHOT_DIRECTOR.replace(
        "角色B没有拿牌 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
        "角色B没有拿牌 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头、观众=角色B拒绝]",
    ).replace(
        "角色B停着的手与牌背同框 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头]",
        "角色B停着的手与牌背同框 [在场:角色A,角色B; 持有:角色A=取衣牌; 知情:观众=拒绝递交、观众=牌背线头、观众=角色B拒绝]",
    )
    require(
        any("知情在切点凭空出现" in error for error in check_director(knowledge_early, SCREENPLAY, TWO_SHOT_STORYBOARD)),
        "knowledge arriving at a cut nobody planned",
    )

    print("36 self-tests passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
