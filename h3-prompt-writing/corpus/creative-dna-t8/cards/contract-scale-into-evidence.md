# contract-scale-into-evidence

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: contract-scale-into-evidence
description: "Create original short videos using the 景别收紧｜从世界到眼神 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 景别收紧｜从世界到眼神

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 景别持续收紧
- 人物空间关系稳定
- 证据从环境转到局部再到装置
- 最后用近景反应闭合

5. Change source-specific people, setting, props, palette, dialogue, shot boundaries, sound family, and payoff surfaces together.
6. Compile MiniMax H3 and Seedance 2.0 independently; do not leak one model's field syntax into the other.
7. Silently verify anchor coverage, continuity, timing, physical causality, and anti-copy distance before returning the final prompts.

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
# 景别收紧｜从世界到眼神 — 摘要

## 用途

景别从宏大环境逐步收紧，按人物、局部发现、自有装置和眼神反应形成证据漏斗。

## 推荐输入格式

`宏大环境 + 稳定人物/双人 + 地面或局部发现 + 人物自有装置 + 最后近景反应`

## 可直接改写的简短示例

> 轨道维修舱先展示宏大地球背景，两名工程师保持稳定位置；镜头收紧到地面金属垫片，再到其中一人的腕部检测器，最后停在两人克制交换的眼神。

## 必须保留的结构锚点

- 景别持续收紧
- 人物空间关系稳定
- 证据从环境转到局部再到装置
- 最后用近景反应闭合

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 景别收紧｜从世界到眼神 Template

## Mechanism

Begin with monumental environment scale and a tiny stable subject pair. Contract framing in discrete evidence steps—paired medium, full-body investigation, object inspection, subject-owned mechanism insert and eye-level reaction—so every scale change answers one question and raises a more personal one. Preserve route, axis and identity, keep performance restrained, and stop at the facial endpoint instead of adding another action branch.

## Invariants

### inv-01

- Rule: Establish world scale, route and the stable subject group in an extreme or very wide opening.
- Purpose: Gives later close evidence a measurable spatial and emotional baseline.
- Failure if removed: Opening close removes the scale contrast and makes later inserts feel arbitrary.

### inv-02

- Rule: Contract framing through ordered information layers rather than random beauty shots.
- Purpose: Turns camera scale into an evidence funnel.
- Failure if removed: Repeated similar coverage reveals no new question and produces a flat montage.

### inv-03

- Rule: Move the evidence from the shared environment to a local object and then to a mechanism owned by the lead subject.
- Purpose: Raises personal stakes without requiring a copied threat or effect.
- Failure if removed: Unrelated props do not create an inward causal progression.

### inv-04

- Rule: Preserve the same route axis, subject identities and wardrobe or material markers across every scale change.
- Purpose: Lets the audience read all shots as one continuous investigation.
- Failure if removed: Continuity drift makes the scale ladder look like disconnected footage.

### inv-05

- Rule: End on one restrained face or sensor response immediately after the closest mechanism proof.
- Purpose: Converts physical evidence into a readable human or system endpoint.
- Failure if removed: A new action after the reaction restarts the sequence and weakens the funnel closure.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject_group | One stable person, pair or machine group whose identity remains continuous. |
| monumental_setting | A setting with a readable route and strong wide-scale geography. |
| local_discovery | One small external object or state that justifies stopping. |
| owned_mechanism | One tool, garment mechanism or device physically associated with the lead subject. |
| scale_ladder | A deliberate wide-to-close information order in which each scale reveals new evidence. |
| performance_rule | Restrained testing and recognition rather than exaggerated reaction. |
| final_response | One face, lens or status response that closes the sequence. |

## Required Human-Facing Anchors

- 景别持续收紧
- 人物空间关系稳定
- 证据从环境转到局部再到装置
- 最后用近景反应闭合

## Anti-Copy Boundary

- two wuxia women in white and green robes
- misty Chinese immortal valley settlement
- silver sword, pebble test and the source Mandarin dialogue
- the unverified four-step audio-before-action rule and exact source shot boundaries

## Transfer Tests

1. Two orbital engineers cross a vast repair bay, stop at a washer pulled toward a sealed bulkhead, inspect a wrist seal tester carrying the same pulse and end on one engineer listening toward the door.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject_group, monumental_setting, local_discovery, owned_mechanism, scale_ladder, performance_rule, final_response
2. A ranger pair crosses a giant wind farm, kneels at a frost-covered feather, checks the same crystalline growth on a handheld vane and ends on a controlled gaze toward one silent turbine.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject_group, monumental_setting, local_discovery, owned_mechanism, scale_ladder, performance_rule, final_response

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

