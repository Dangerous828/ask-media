# micro-ecology-world-title-scale

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: micro-ecology-world-title-scale
description: "Create original short videos using the 微观到世界｜生态线索扩张与片名 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 微观到世界｜生态线索扩张与片名

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 同一线索跨尺度
- 空间逐级扩大
- 片名在最终尺度稳定可读

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
# 微观到世界｜生态线索扩张与片名 — 摘要

## 用途

从微小生态证据扩到建成环境和世界尺度，最后停在原创片名。

## 推荐输入格式

`微观线索＋中景环境＋世界远景＋原创片名`

## 可直接改写的简短示例

> 极地冰芯、显微镜显示器、同一块实物样本、成年野外研究员、短冰道和小型研究站；琥珀色标记从显微图连到实物样本标签，再连到冰原俯瞰图。

## 必须保留的结构锚点

- 同一线索跨尺度
- 空间逐级扩大
- 片名在最终尺度稳定可读

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 微观到世界｜生态线索扩张与片名 Template

## Mechanism

A tiny lit ecological clue becomes a recognizable thread through an intermediate built habitat to a much larger world context, while readable credits accompany movement and a fresh title holds after the scale reveal.

## Invariants

### inv-01

- Rule: Introduce one small light/life cue in an intimate composition and retain a recognizable visual motif as the scale grows.
- Purpose: Gives the audience a thread across spaces.
- Failure if removed: Unrelated pretty macro images will not connect to the later environment.

### inv-02

- Rule: Advance through at least one inhabited/constructed intermediate ecology before revealing its larger geographic or planetary container.
- Purpose: Creates a stepped scale ladder rather than an arbitrary cut to space.
- Failure if removed: Skipping the middle habitat makes the cosmic image decorative rather than earned.

### inv-03

- Rule: Place credits as readable overlays during travel and hold a distinct final original title on a visually calmer largest-scale frame.
- Purpose: Makes the sequence function as a usable title opening.
- Failure if removed: Moving text or premature title loses hierarchy and readability.


## Variable Slots

| Slot | Constraint |
|---|---|
| micro_clue | One distinctive life/light/material cue visible first at close scale. |
| intermediate_habitat | A coherent built or natural environment that spatially relates to the micro cue. |
| large_container | Larger world/context revealed after the habitat, not immediately. |
| motif_handoff | A traceable color/shape/light feature across all scales. |
| credit_system | Small readable credits that do not obscure the visual clue. |
| title | Original short legible title, held in a calmer final frame. |
| sound | Original audio arc; no attribution to unheard source soundtrack. |

## Required Human-Facing Anchors

- 同一线索跨尺度
- 空间逐级扩大
- 片名在最终尺度稳定可读

## Anti-Copy Boundary

- No source title 'NINE MINUTES OF SUN', creator names, exact credit wording or source series premise.
- No orbital seed archive, plant racks, circular planet porthole, space-station glide, exact droplet lens flare or source color/camera compositions in the primary output.
- Do not invent a visible countdown or assert source sound events.

## Transfer Tests

1. An original polar ecology documentary opening: a microscope view of a living microbe inside an ice-core bubble catches an amber glint; the camera then pulls back to the microscope table and the amber motif recurs on the physical ice-core sample tag and across an ice tunnel toward a field station, then resolves as one amber survey route on an overhead ice-field map; hold the new title 'LIVING ICE' in a steady final frame.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: micro_clue, intermediate_habitat, large_container, motif_handoff, credit_system, title, sound
2. An original underwater reef-monitoring opening: one fluorescent coral polyp emits a violet pulse; the pulse appears on a diver's sample gauge, then is tracked by an exterior sensor buoy before an overhead reef-current chart reveals the larger ecosystem; hold the new title 'REEF PULSE' in a calm final frame.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: micro_clue, intermediate_habitat, large_container, motif_handoff, credit_system, title, sound

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

