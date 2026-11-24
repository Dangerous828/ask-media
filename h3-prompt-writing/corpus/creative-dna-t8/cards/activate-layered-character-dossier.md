# activate-layered-character-dossier

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: activate-layered-character-dossier
description: "Create original short videos using the 人物档案｜能力逐层点亮 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 人物档案｜能力逐层点亮

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 人物身份稳定
- 档案框架固定
- 信息层级按功能递进
- 终态是可执行的待命状态

3. Change source-specific people, setting, props, palette, dialogue, shot boundaries, sound family, and payoff surfaces together.
4. Compile MiniMax H3 and Seedance 2.0 independently; do not leak one model's field syntax into the other.
5. Silently verify anchor coverage, continuity, timing, physical causality, and anti-copy distance before returning the final prompts.

## MiniMax H3

- Use the current official H3 task grammar and language profile.
- Separate integrated visual action, overall soundscape, and non-diegetic music or explicit silence.
- Use timestamps only to make event order executable; keep shots consecutive and duration-safe.

## Seedance 2.0

- Define stable subjects once and preserve event order, camera motivation, sound intent, and overall duration.
- Use a simple paragraph for simple concepts or an ordered multi-shot structure for complex concepts.
- State overall duration once; do not copy H3 field labels or per-shot timecode grammar.

## Output

Return one concept sentence, the filled slots, an anchor-coverage check, one MiniMax H3 prompt, one Seedance 2.0 prompt, and a short anti-copy validation note.

## Non-Negotiable

- A subject-only request is underspecified. Preserve that subject and complete the mechanism instead of returning a generic portrait or showcase.
- Do not omit, reorder, or weaken a required anchor.
- Do not reuse source people, brands, dialogue, exact storyboard, signature props, exact timings, or recognizable effect surfaces.
````

### summary.md

````text
# 人物档案｜能力逐层点亮 — 摘要

## 用途

固定档案界面不换主体，按身份、诊断、能力、工具和待命状态逐层激活。

## 推荐输入格式

`稳定人物 + 固定档案界面 + 身份→诊断→能力→工具→待命状态`

## 可直接改写的简短示例

> 深海潜水员始终位于固定档案框：先显示身份轮廓，再扫描呼吸系统，随后点亮耐压能力、展开机械工具，最后进入待命姿态。

## 必须保留的结构锚点

- 人物身份稳定
- 档案框架固定
- 信息层级按功能递进
- 终态是可执行的待命状态

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 人物档案｜能力逐层点亮 Template

## Mechanism

Hold one subject and one modular information grid completely stable while a dossier boots from absence to completeness in a strict hierarchy. Each phase activates a new semantic layer—identity, role, diagnostics, capability, equipment and status—while the subject performs only micro-motion. Information order, not camera travel, creates retention; subject, domain, panel geometry, palette and labels are variable.

## Invariants

### inv-01

- Rule: Begin with a partially hidden subject inside a fixed modular grid.
- Purpose: Creates an identity question and spatial memory.
- Failure if removed: A fully revealed first frame removes the discovery ladder.

### inv-02

- Rule: Activate information layers in a semantic hierarchy from identity to capability.
- Purpose: Prevents visual noise and makes every phase answer one question.
- Failure if removed: Random panel order produces decoration instead of explanation.

### inv-03

- Rule: Keep subject pose and grid geometry stable while module states change.
- Purpose: Makes progress attributable to the interface.
- Failure if removed: Camera movement or pose changes destroy state comparison.

### inv-04

- Rule: Use one restrained accent color to indicate activation and completion.
- Purpose: Provides a readable visual clock.
- Failure if removed: Multiple competing activation colors blur hierarchy.

### inv-05

- Rule: End with one global active-state pulse after all key modules are complete.
- Purpose: Supplies a clean completion signal.
- Failure if removed: No final confirmation makes the boot feel unfinished.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original subject whose identity and silhouette remain stable. |
| setting | A new setting with fixed spatial anchors and no source-specific location. |
| escalation_variable | One readable variable that changes monotonically or in countable stages. |
| performance_rule | One restrained performance rule that makes the mechanism legible. |
| camera_grammar | A coherent information order that does not copy the source shot boundaries. |
| payoff | One clean physical or graphic consequence that closes the causal chain. |
| sound_family | A new hierarchy of diegetic cues supporting each state change. |

## Required Human-Facing Anchors

- 人物身份稳定
- 档案框架固定
- 信息层级按功能递进
- 终态是可执行的待命状态

## Anti-Copy Boundary

- named ZENITH cybernetic operative and exact face
- cyan-black tactical dossier with source panel arrangement
- cybernetic arm diagnostic image and source stat values
- source headings, labels, iconography and final slogan

## Transfer Tests

1. A deep-sea survey pilot stands inside a navy-and-amber expedition dossier that boots from silhouette to identity, pressure tolerance, suit integrity, navigation skills, tool loadout and ready-state pulse.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A fantasy field botanist appears inside a parchment-and-emerald archive that reveals identity, biome expertise, specimen map, tool kit and expedition clearance.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family

## Model Skeletons

### MiniMax H3

    integrated_multimodal_description: [new subject, environment, ordered actions, camera, light and final state preserving every anchor]
    overall_soundscape: [diegetic ambience, action cues and causal payoff]
    non_diegetic_music: [original music arc or N/A]

### Seedance 2.0

    任务：[原创实例意图]
    总时长约[4–15]秒。
    主体定义：[稳定人物、物体与空间关系]
    事件或镜头：[按因果顺序实现全部锚点]
    整体风格与画质：[原创媒介、光影、色彩与声音]
    约束：[连续性、物理逻辑、反复制与结尾状态]

Adapt shot count to the user's concept. Preserve the causal mechanism, not a fixed storyboard.
````

