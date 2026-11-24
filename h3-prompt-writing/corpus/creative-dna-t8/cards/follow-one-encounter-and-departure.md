# follow-one-encounter-and-departure

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: follow-one-encounter-and-departure
description: "Create original short videos using the 纪实跟拍｜行进中偶遇再离开 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 纪实跟拍｜行进中偶遇再离开

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 先侧面跟拍再揭示更大路线
- 人物在镜头转换中保持行走
- 全片只发生一次偶遇
- 回应克制且不停止路线
- 结尾人物继续经过或远离镜头

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
# 纪实跟拍｜行进中偶遇再离开 — 摘要

## 用途

侧面跟拍同一人物离开狭窄空间，镜头漂到身后并揭示更大路线；只发生一次偶遇和一次克制回应，人物随后继续离开。

## 推荐输入格式

`侧面连续跟拍 + 狭窄起点 + 行进中空间揭示 + 一次偶发横穿 + 一次克制回应 + 继续离开`

## 可直接改写的简短示例

> 夜班烘焙师从狭窄服务通道走上有顶渡轮码头，镜头从侧面漂到身后；一只信鸽落在路线前方，他只点头并侧移半步，然后继续经过镜头走向服务门。

## 必须保留的结构锚点

- 先侧面跟拍再揭示更大路线
- 人物在镜头转换中保持行走
- 全片只发生一次偶遇
- 回应克制且不停止路线
- 结尾人物继续经过或远离镜头

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 纪实跟拍｜行进中偶遇再离开 Template

## Mechanism

Follow one subject through a real public route without stopping the world for coverage. Start in side profile, let the camera drift behind as the space opens, allow one incidental person or event to cross the route, capture a single restrained acknowledgment, then continue past the camera so the encounter remains a lived moment rather than a staged climax.

## Invariants

### inv-01

- Rule: Begin with a side-profile follow before revealing the larger route.
- Purpose: Creates a spatial discovery rather than an establishing postcard.
- Failure if removed: Starting wide removes the observer's gradual reveal.

### inv-02

- Rule: Keep the subject walking through the camera transition.
- Purpose: Preserves lived continuity.
- Failure if removed: Stopping for coverage makes the passage feel staged.

### inv-03

- Rule: Allow exactly one incidental crossing or encounter to enter the established route.
- Purpose: Provides a small narrative event.
- Failure if removed: Multiple incidents turn observation into montage.

### inv-04

- Rule: Use one restrained acknowledgment without halting the route.
- Purpose: Gives the event emotional weight while staying naturalistic.
- Failure if removed: A large reaction becomes a climax the scene has not earned.

### inv-05

- Rule: End with continued movement past or away from camera.
- Purpose: Keeps the encounter embedded in ordinary life.
- Failure if removed: A posed final look converts the piece into a portrait.


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

- 先侧面跟拍再揭示更大路线
- 人物在镜头转换中保持行走
- 全片只发生一次偶遇
- 回应克制且不停止路线
- 结尾人物继续经过或远离镜头

## Anti-Copy Boundary

- source woman
- source flower shop and public square
- source children
- source wardrobe and exact route

## Transfer Tests

1. A night-shift baker exits a narrow service corridor onto a covered ferry pier; a courier pigeon lands across the route, the baker shortens one step, nods and continues as the bird lifts away.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A greenhouse technician leaves a humid propagation aisle for an open loading canopy; one loose seed envelope skims across the route, the technician catches and clips it to a rail, then continues.
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

