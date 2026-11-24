# build-microexpression-greeting-arc

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: build-microexpression-greeting-arc
description: "Create original short videos using the 微表情问候｜侧身发现到笑容回稳 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 微表情问候｜侧身发现到笑容回稳

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- Begin from a readable side orientation rather than immediate frontal address.
- Reach and hold direct gaze before the emotional peak.
- Use one countable peak expression without a large body gesture.
- Recover to an open relaxed state and hold.

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
# 微表情问候｜侧身发现到笑容回稳 — 摘要

## 用途

用近乎锁定的人像镜头完成五段微表情问候：侧身开始、建立直视、短暂垂眼停顿、闭眼笑容达到峰值，再回到开放而放松的表情；不换场景、不加大动作。

## 推荐输入格式

`单一人像 + 侧身开始 + 稳定直视 + 垂眼停顿 + 1次峰值表情 + 开放表情回稳`

## 可直接改写的简短示例

> 年长纸张修复师侧身拿着修复地图，转头直视、垂眼停顿、闭眼微笑，再睁眼回到放松表情；全程保持同一安静档案室。

## 必须保留的结构锚点

- Begin from a readable side orientation rather than immediate frontal address.
- Reach and hold direct gaze before the emotional peak.
- Use one countable peak expression without a large body gesture.
- Recover to an open relaxed state and hold.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 微表情问候｜侧身发现到笑容回稳 Template

## Mechanism

Use one nearly locked portrait to make a greeting readable through five small state changes: begin in side orientation, establish direct gaze, lower the gaze into a brief self-contained pause, peak with one closed-eye smile, and recover to an open relaxed expression without changing setting or adding a large gesture.

## Invariants

### inv-01

- Rule: Begin from a readable side orientation rather than immediate frontal address.
- Purpose: Creates a visible discovery step.
- Failure if removed: Starting frontal removes the orientation change.

### inv-02

- Rule: Reach and hold direct gaze before the emotional peak.
- Purpose: Makes the viewer relationship explicit.
- Failure if removed: A passing glance gives no stable connection.

### inv-03

- Rule: Insert one brief downward-gaze pause with the body still anchored.
- Purpose: Creates contrast before the smile.
- Failure if removed: Continuous smiling flattens the arc.

### inv-04

- Rule: Use one countable peak expression without a large body gesture.
- Purpose: Keeps the change legible at portrait scale.
- Failure if removed: A broad wave or jump overwhelms the facial proof.

### inv-05

- Rule: Recover to an open relaxed state and hold.
- Purpose: Closes the greeting without looping abruptly.
- Failure if removed: Ending at the closed-eye peak feels cut off.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair whose role is clear without source identity. |
| setting | A materially new setting with fixed spatial anchors and no source-specific location. |
| causal_carrier | One object, route, mark or device that visibly carries the causal chain. |
| state_change | Five ordered states with observable handoffs, not a decorative montage. |
| camera_grammar | A new proof-oriented information order that does not copy source shot boundaries. |
| payoff | A held final consequence that resolves or recontextualizes the setup. |
| sound_family | An original hierarchy of story-world cues supporting each visible change. |

## Required Human-Facing Anchors

- Begin from a readable side orientation rather than immediate frontal address.
- Reach and hold direct gaze before the emotional peak.
- Use one countable peak expression without a large body gesture.
- Recover to an open relaxed state and hold.

## Anti-Copy Boundary

- source anime schoolgirl
- source stairwell and shopping bag
- source sailor-style shirt and denim skirt
- the exact shy-girl facial design

## Transfer Tests

1. An original elderly paper conservator turns from a worktable, meets camera through round lenses, lowers the gaze to a repaired map, gives one closed-eye relieved smile, then reopens the eyes and holds the restored sheet.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family
2. A small stop-motion clay lighthouse keeper rotates from the lamp housing, focuses two painted eyes toward camera, dips toward a tiny logbook, lifts one crescent smile, then settles into a relaxed open-eyed pose.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family

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

