# material-value-ladder-human-payoff

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: material-value-ladder-human-payoff
description: "Create original short videos using the 价值阶梯｜原料—转化—装配—使用回报 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 价值阶梯｜原料—转化—装配—使用回报

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish one recognizable raw material in isolation and then in sufficient quantity before any processing machinery appears.
- Move that material into controlled processing through one visible directional handoff.
- Convert the transformed material into repeated finished units through measured formation and orderly placement.
- Resolve with a real user receiving, using or sharing the completed object, then hold a restrained final lockup.

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
# 价值阶梯｜原料—转化—装配—使用回报 — 摘要

## 用途

先用可识别原料建立价值起点，再以可见的转化、定型和精密装配逐级增加完成度；最后把成品交到真实使用者手中，让工业过程落到清楚的人类回报。

## 推荐输入格式

`可识别原料 + 受控方向交接 + 可见材质转化 + 重复单元定型与装配 + 真实使用回报 + 成品锁定`

## 可直接改写的简短示例

> 一枚粗糙半透明盐晶置于深色砂岩上，随后周围逐渐显出浅层采集晶体床；抛光矿物转化为透明光学树脂，一条黏性料流依次注入六边形棱镜模具；成年沙漠气象员举起天气观察器，只有目镜内显出清楚彩虹风暴图；停留后切到砂岩上的闭合黄铜仪器

## 必须保留的结构锚点

- Establish one recognizable raw material in isolation and then in sufficient quantity before any processing machinery appears.
- Move that material into controlled processing through one visible directional handoff.
- Convert the transformed material into repeated finished units through measured formation and orderly placement.
- Resolve with a real user receiving, using or sharing the completed object, then hold a restrained final lockup.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 价值阶梯｜原料—转化—装配—使用回报 Template

## Mechanism

Build a visible value ladder from one recognizable raw material through controlled intake, state transformation, precise unit formation and orderly final assembly. Each phase must preserve a causal trace of the same material while changing the camera duty to prove the new production state. End with a human use, exchange or sensory payoff that answers why the process was shown, followed by a brief finished-object lockup. The mechanism is process-to-human-value closure, not a particular food, brand or luxury package.

## Invariants

### inv-01

- Rule: Establish one recognizable raw material in isolation and then in sufficient quantity before any processing machinery appears.
- Purpose: Creates a legible value baseline.
- Failure if removed: Beginning on machinery makes the input identity and later transformation ambiguous.

### inv-02

- Rule: Move that material into controlled processing through one visible directional handoff.
- Purpose: Proves that the later product comes from the established input.
- Failure if removed: An unrelated factory cut breaks material causality.

### inv-03

- Rule: Show one unmistakable material-state transformation at a scale where texture and behavior are readable.
- Purpose: Provides the central proof of added value.
- Failure if removed: Skipping the state change turns the sequence into disconnected product shots.

### inv-04

- Rule: Convert the transformed material into repeated finished units through measured formation and orderly placement.
- Purpose: Makes precision and completion inspectable.
- Failure if removed: A single unexplained final object cannot prove controlled manufacture.

### inv-05

- Rule: Resolve with a real user receiving, using or sharing the completed object, then hold a restrained final lockup.
- Purpose: Connects technical process to human consequence.
- Failure if removed: Ending inside the factory leaves the value claim emotionally unfinished.


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

- Establish one recognizable raw material in isolation and then in sufficient quantity before any processing machinery appears.
- Move that material into controlled processing through one visible directional handoff.
- Convert the transformed material into repeated finished units through measured formation and orderly placement.
- Resolve with a real user receiving, using or sharing the completed object, then hold a restrained final lockup.

## Anti-Copy Boundary

- the source cocoa pod seed, cocoa-bean field, bean hopper and chocolate-production machinery
- the source melted-chocolate waves, droplets, filling stream and gold confection cavities
- the source robotic chocolate gripper, brown luxury gift box and gold-wrapped pieces
- the source adult-and-child tasting sequence, domestic beige wardrobe and exact sharing gestures
- the source warm brown-and-gold palette, product framing and persistent Wavespeed Seedance 2.5 watermark

## Transfer Tests

1. In an original desert-optics workshop, one rough translucent salt crystal expands into a harvested crystal bed, travels through a guarded rinse and polishing channel, melts into optical resin, fills small prism molds, is seated by a brass micro-arm into a weather viewer and ends when a desert meteorologist uses the viewer to reveal a rainbow storm map before a clean instrument lockup.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In an original coastal biomaterials studio, one green algae bead expands into cultivation trays, flows through a clear extraction tube, becomes flexible luminous biopolymer, is cast into repeating lantern petals, assembled by a compact robot and ends when night fishermen unfold the lamp on a pier before the closed lantern holds in frame.
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

