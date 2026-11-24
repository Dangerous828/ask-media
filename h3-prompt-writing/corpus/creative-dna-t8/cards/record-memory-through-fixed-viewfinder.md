# record-memory-through-fixed-viewfinder

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: record-memory-through-fixed-viewfinder
description: "Create original short videos using the 相机记忆｜固定取景框串联日常 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 相机记忆｜固定取景框串联日常

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 同一原创相机界面全程不变
- 同一人物穿过至少三处连续空间
- 每处空间有一个小动作
- 至少一次阈值或楼梯过渡
- 结尾触镜物理结束记录

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
# 相机记忆｜固定取景框串联日常 — 摘要

## 用途

一个固定相机取景界面贯穿多处日常空间，同一人物每到一处完成一个小动作，最后用手掌触镜物理结束记录。

## 推荐输入格式

`同一人物 + 固定相机界面 + 至少3处连续路线空间 + 每处一个小动作 + 一个明确阈值过渡 + 触镜结束`

## 可直接改写的简短示例

> 年长博物馆修复师在固定口袋相机界面中穿过档案室、修复室、楼梯和雕塑庭院，每处完成一个小动作，最后在屋顶用戴手套的手掌完全盖住镜头。

## 必须保留的结构锚点

- 同一原创相机界面全程不变
- 同一人物穿过至少三处连续空间
- 每处空间有一个小动作
- 至少一次阈值或楼梯过渡
- 结尾触镜物理结束记录

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 相机记忆｜固定取景框串联日常 Template

## Mechanism

Lock one recorder-style viewing interface over the entire film, then let one subject move through a compact route of clearly different everyday places. Each place contributes one small human action and one spatial clue; finish with a direct gesture into the lens so the fixed interface feels like a remembered recording rather than decorative graphics.

## Invariants

### inv-01

- Rule: Keep one original recorder interface visually stable for the whole sequence.
- Purpose: Binds separate places into one recording session.
- Failure if removed: If the interface changes every shot, it becomes decorative motion graphics.

### inv-02

- Rule: Keep one subject and one observer relationship continuous across at least three places.
- Purpose: Turns location changes into a route.
- Failure if removed: Unrelated people and places become a travel montage.

### inv-03

- Rule: Give each place one small readable action rather than a posed beauty shot.
- Purpose: Creates memory detail and human continuity.
- Failure if removed: Pure posing makes the interface feel like a filter.

### inv-04

- Rule: Use one physical threshold or travel action between interior and exterior scale.
- Purpose: Makes spatial progression legible.
- Failure if removed: Abrupt location swaps lose the feeling of an outing.

### inv-05

- Rule: End with a direct lens interaction that physically closes the recording.
- Purpose: Provides an intimate and causal endpoint.
- Failure if removed: A fade without interaction does not complete the observer relationship.


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

- 同一原创相机界面全程不变
- 同一人物穿过至少三处连续空间
- 每处空间有一个小动作
- 至少一次阈值或楼梯过渡
- 结尾触镜物理结束记录

## Anti-Copy Boundary

- source young woman
- source library and mall route
- source drink prop
- the exact source camera HUD

## Transfer Tests

1. An elderly museum restorer records a pocket-camera diary through archive room, stairwell, sculpture court and rooftop, ending by placing a gloved palm over the lens.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A night-market volunteer moves from prep tent to lantern alley, river steps and closing stall while the same camcorder frame persists, ending by clipping the lens cap on.
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

