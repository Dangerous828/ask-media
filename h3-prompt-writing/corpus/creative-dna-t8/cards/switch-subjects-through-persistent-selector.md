# switch-subjects-through-persistent-selector

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: switch-subjects-through-persistent-selector
description: "Create original short videos using the 互动图鉴｜固定菜单切换生物 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 互动图鉴｜固定菜单切换生物

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 菜单、数据区和主视窗位置固定
- 每次内容变化前必须有可见选择
- 名称参数和主体同步更新
- 每个被选主体完成一个定义动作
- 结尾保持完整最终选择状态

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
# 互动图鉴｜固定菜单切换生物 — 摘要

## 用途

菜单、数据区和主视窗固定不动，选择器逐项切换，每次让名称、参数与主视窗主体同步更新并完成一个定义动作。

## 推荐输入格式

`固定选择菜单 + 固定数据区 + 固定主视窗 + 至少4个原创对象 + 每次可见选择 + 同步字段更新 + 一个定义动作`

## 可直接改写的简短示例

> 固定气象无人机图鉴依次选择五台原创无人机，每次先移动选择器，再同步更新呼号、风力参数和主视窗，并让新无人机在对应天气舱完成一个定义动作。

## 必须保留的结构锚点

- 菜单、数据区和主视窗位置固定
- 每次内容变化前必须有可见选择
- 名称参数和主体同步更新
- 每个被选主体完成一个定义动作
- 结尾保持完整最终选择状态

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 互动图鉴｜固定菜单切换生物 Template

## Mechanism

Keep one information interface and spatial grid fixed while a visible selector chooses one item at a time. Each selection must update the title, concise attributes and one large live viewport together; the selected subject then performs one short behavior that proves the new state before the next choice.

## Invariants

### inv-01

- Rule: Keep one selector grid, one data zone and one live viewport fixed.
- Purpose: Creates an inspectable state machine.
- Failure if removed: Moving interface regions make updates difficult to compare.

### inv-02

- Rule: Show one visible selector action before every content change.
- Purpose: Makes each update causal.
- Failure if removed: Unmotivated swaps become a montage.

### inv-03

- Rule: Update title, attributes and live subject as one synchronized state.
- Purpose: Prevents contradictory interface evidence.
- Failure if removed: Partial updates make the catalog feel broken.

### inv-04

- Rule: Give each selected subject one short defining behavior.
- Purpose: Proves more than a static thumbnail.
- Failure if removed: Idle subjects do not justify a live viewport.

### inv-05

- Rule: End on a held complete state with selector and selected subject both visible.
- Purpose: Lets the viewer verify the final choice.
- Failure if removed: Cutting away immediately removes the proof relation.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair with a readable role. |
| setting | A new setting with fixed spatial anchors and no source-specific surface. |
| escalation_variable | One causal variable that changes through visible stages. |
| performance_rule | A restrained acting or motion rule that keeps the mechanism legible. |
| camera_grammar | An information order that proves each state without copying source shot boundaries. |
| payoff | A clean final physical, informational or social consequence. |
| sound_family | An original hierarchy of diegetic cues; no unsupported source-audio claim. |

## Required Human-Facing Anchors

- 菜单、数据区和主视窗位置固定
- 每次内容变化前必须有可见选择
- 名称参数和主体同步更新
- 每个被选主体完成一个定义动作
- 结尾保持完整最终选择状态

## Anti-Copy Boundary

- CREATURE ENCYCLOPEDIA title
- source creature designs
- source names and statistics
- the exact source grid and cursor path

## Transfer Tests

1. A fixed weather-drone field guide selects five original drones; tile, call sign, wind rating and large live weather test update together for each choice.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A seed-vault interface selects five invented plants; fixed specimen grid, growth attributes and large time-lapse diorama update in one synchronized state.
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

