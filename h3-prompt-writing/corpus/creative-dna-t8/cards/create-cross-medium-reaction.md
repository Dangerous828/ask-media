# create-cross-medium-reaction

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: create-cross-medium-reaction
description: "Create original short videos using the 二维角色｜真人接触三级反应 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 二维角色｜真人接触三级反应

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 平面与真实媒介同框
- 只有一次关键接触
- 反应至少三级升级
- 结尾由平面媒介自身完成

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
# 二维角色｜真人接触三级反应 — 摘要

## 用途

真实世界一次接触触发平面角色的三级反应，并以媒介自身的变化收尾。

## 推荐输入格式

`平面角色 + 真实场景 + 一次跨媒介接触 + 三级反应 + 媒介专属结尾`

## 可直接改写的简短示例

> 书桌贴纸上的纸片机器人被真人手指轻触：先轻颤，再鼓起并喷出纸屑火花，最后整张桌垫折成通往它的纸桥。

## 必须保留的结构锚点

- 平面与真实媒介同框
- 只有一次关键接触
- 反应至少三级升级
- 结尾由平面媒介自身完成

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 二维角色｜真人接触三级反应 Template

## Mechanism

A single flat 2D character shares a locked photoreal environment with a real hand; one small cross-medium contact causes a three-stage readable reaction that ends in a medium-specific impossible effect.

## Invariants

### inv-01

- Rule: Keep exactly one flat animated character inside an otherwise photoreal, stable environment.
- Purpose: Makes the mixed-medium anomaly instantly legible.
- Failure if removed: Multiple animated elements blur the boundary and weaken the hook.

### inv-02

- Rule: Show real-to-animated contact before the reaction begins.
- Purpose: Provides a causal bridge between media layers.
- Failure if removed: A reaction without contact feels like an unrelated animation loop.

### inv-03

- Rule: Escalate in three readable states: neutral, discomfort, impossible payoff.
- Purpose: Lets the audience track cause and intensity without cuts.
- Failure if removed: Jumping directly to the final effect removes anticipation and acting.

### inv-04

- Rule: Keep the camera locked and let contact, expression, and effects move attention.
- Purpose: Protects spatial continuity between real and animated layers.
- Failure if removed: Camera movement makes contact alignment harder to read.


## Variable Slots

| Slot | Constraint |
|---|---|
| photoreal_arena | A stable real location with clear depth and one interaction surface. |
| flat_character | One original 2D paper- or sticker-like adult mascot, visually distinct from the source. |
| real_agent | One live-action hand or tool entering from a consistent edge. |
| contact_object | A small real object whose motion can visibly cross the medium boundary. |
| sensation | A simple cause such as cold, static, scent, or weight, not source heat/chili. |
| reaction_states | Three visually distinct but causally continuous poses. |
| payoff_effect | An original safe effect appropriate to the new sensation. |
| sound | Real location ambience plus contact-synced foley and one effect accent. |

## Required Human-Facing Anchors

- 平面与真实媒介同框
- 只有一次关键接触
- 反应至少三级升级
- 结尾由平面媒介自身完成

## Anti-Copy Boundary

- source girl character, hairstyle, clothes, face, outline, or childlike proportions
- source kitchen, wok, food, seasoning jar, spoon interaction, and camera composition
- chili or heat tasting, lateral tear jets, red forehead, and fire breathing
- exact reaction timing and source visual effects

## Transfer Tests

1. A flat 2D alpine-fox sticker at a real tea counter receives one drop of mint extract, sips, shivers, and exhales a small frost cloud that freezes a spoon.
   - Preserved: inv-01, inv-02, inv-03, inv-04
   - Changed: photoreal_arena, flat_character, contact_object, sensation, reaction_states, payoff_effect
2. A flat 2D robot sticker at a real workbench receives one drop of lubricant, tests a hinge, spins with the over-loose joint, and stops with a dizzy status-light pattern.
   - Preserved: inv-01, inv-02, inv-03, inv-04
   - Changed: photoreal_arena, flat_character, real_agent, contact_object, sensation, payoff_effect

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

