# frontal-retreat-collapsing-corridor

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: frontal-retreat-collapsing-corridor
description: "Create original short videos using the 正面撤退｜通道坍缩逼向唯一庇护 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 正面撤退｜通道坍缩逼向唯一庇护

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish a subject facing the threat while moving backward toward a visible route.
- Advance the environmental hazard along the same corridor axis as the retreat.
- Keep one protective threshold readable behind the subject before the final crossing.
- Use one terminal crossing and visible boundary separation from the hazard.

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
# 正面撤退｜通道坍缩逼向唯一庇护 — 摘要

## 用途

让主体面向威胁、背向目标持续后退，镜头以匹配速度倒退保持脸和来袭环境同框；危险从远端向前逐段占据通道，余量不断缩小，最终主体跨入唯一可见庇护并由边界闭合结束。

## 推荐输入格式

`主体面向威胁后退 + 同轴危险逼近 + 分阶段空间压缩 + 唯一庇护门槛 + 单次边界闭合`

## 可直接改写的简短示例

> 原创纸影灯桥上，奶油色关节木偶面对镜头向后走，远端拱门出现一道黑墨裂纹，近处白色折纸神龛清楚可见；两块纸栏板向内折叠，木偶周围的干净路径被压窄，但主体身份和步态连续；木偶只跨入一次，白纸门在黑墨到达前折合关闭，镜头保持关闭边界，不声称后续结果

## 必须保留的结构锚点

- Establish a subject facing the threat while moving backward toward a visible route.
- Advance the environmental hazard along the same corridor axis as the retreat.
- Keep one protective threshold readable behind the subject before the final crossing.
- Use one terminal crossing and visible boundary separation from the hazard.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 正面撤退｜通道坍缩逼向唯一庇护 Template

## Mechanism

Keep a retreating subject facing an advancing hazard while a camera moves backward at matched speed; progressively reduce corridor clearance along the shared axis, preserve one visible protective threshold behind the subject, then complete one crossing and boundary closure.

## Invariants

### inv-01

- Rule: Establish a subject facing the threat while moving backward toward a visible route.
- Purpose: Defines the frontal-retreat relationship.
- Failure if removed: Turning away removes simultaneous face-and-threat proof.

### inv-02

- Rule: Advance the environmental hazard along the same corridor axis as the retreat.
- Purpose: Creates a measurable closing-distance problem.
- Failure if removed: Random off-axis debris becomes generic chaos.

### inv-03

- Rule: Reduce visible clearance in at least two stages without changing subject identity or route.
- Purpose: Builds escalation through spatial compression.
- Failure if removed: One sudden blast provides no progressive pressure.

### inv-04

- Rule: Keep one protective threshold readable behind the subject before the final crossing.
- Purpose: Gives the retreat a clear actionable destination.
- Failure if removed: A surprise exit appears as an unearned rescue.

### inv-05

- Rule: Use one terminal crossing and visible boundary separation from the hazard.
- Purpose: Resolves the corridor problem without claiming unseen survival.
- Failure if removed: Cutting before the boundary leaves the payoff unproved.


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

- Establish a subject facing the threat while moving backward toward a visible route.
- Advance the environmental hazard along the same corridor axis as the retreat.
- Keep one protective threshold readable behind the subject before the final crossing.
- Use one terminal crossing and visible boundary separation from the hazard.

## Anti-Copy Boundary

- the source astronaut
- metal spacecraft corridor
- space debris and industrial collapse
- the source helmet and suit
- the exact hatch and collapse choreography

## Transfer Tests

1. A paper marionette backs along a lantern bridge while black ink cracks chase it through successive arches; the camera retreats face-on until it enters a white folding shrine and the final paper door seals.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A small maintenance crab walks backward inside a transparent coolant pipe as ice fractures advance from depth; it crosses one warm service iris and the iris closes before the fracture front arrives.
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

