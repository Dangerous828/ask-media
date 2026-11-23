# stage-one-signal-reversal

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-one-signal-reversal
description: "Create original short videos using the 一对多反转｜单一证据胜出 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 一对多反转｜单一证据胜出

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 多数方案先制造噪声或冲突
- 单一信号保持克制
- 有明确校准动作
- 最终用物理结果而非口号证明胜出

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
# 一对多反转｜单一证据胜出 — 摘要

## 用途

多个喧闹方案看似占优，单一克制信号通过校准和物理证明完成反转。

## 推荐输入格式

`喧闹多数 + 克制单一信号 + 校准动作 + 可见物理证明`

## 可直接改写的简短示例

> 五台机器人各自给出冲突读数，一枚克制的音叉信号完成校准；所有机械臂同步归零，并共同生成一个稳定透明球作为物理证明。

## 必须保留的结构锚点

- 多数方案先制造噪声或冲突
- 单一信号保持克制
- 有明确校准动作
- 最终用物理结果而非口号证明胜出

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 一对多反转｜单一证据胜出 Template

## Mechanism

A noisy system makes quantity look powerful, one restrained corrective signal interrupts it, and a physical consequence proves that calibrated clarity beats accumulation.

## Invariants

### inv-01

- Rule: Show the asymmetric one-versus-many matchup before either side explains it.
- Purpose: Creates an immediate comparison question.
- Failure if removed: If the single answer appears first, there is no reversal.

### inv-02

- Rule: Let the many-item side perform longer and occupy more space before the concise answer.
- Purpose: Builds apparent advantage and visual noise.
- Failure if removed: Equal screen time makes the payoff predictable and weak.

### inv-03

- Rule: Give the single corrective signal a dedicated sensory close-up.
- Purpose: Turns a small action or object into the strongest information beat without requiring copied text or props.
- Failure if removed: A wide or simultaneous reveal loses hierarchy and emphasis.

### inv-04

- Rule: End with calm control versus noisy consequence, not another explanation.
- Purpose: Converts the logical reversal into a visual punchline.
- Failure if removed: A verbal summary repeats information and drains comic energy.


## Variable Slots

| Slot | Constraint |
|---|---|
| arena | A stable comparison space unrelated to gambling or the source saloon. |
| many_side | One expressive character with three to five compact labeled options. |
| one_side | One calm character with a single short answer label. |
| many_signals | Three to five distinct controls, sounds, lights, routes, or gestures that create legible visual noise. |
| single_answer | One visually and sonically distinct corrective action or object that carries the reversal without needing text. |
| proof | A visible consequence showing why the concise answer wins. |
| meltdown | Safe exaggerated reaction with no weapons or copied gesture. |
| sound | Escalating object sounds, one reveal accent, and a short consequence sound. |

## Required Human-Facing Anchors

- 多数方案先制造噪声或冲突
- 单一信号保持克制
- 有明确校准动作
- 最终用物理结果而非口号证明胜出

## Anti-Copy Boundary

- legacy cartoon characters, voices, silhouettes, or franchise animation surface
- saloon, gambling table, gold-and-carrot stakes, or Western props
- source model names and exact card text
- pistols, smoke-cloud surrender, exact poses, and shot compositions

## Transfer Tests

1. In a whimsical calibration lab, a frantic octopus pulls five mismatched levers while a maintenance robot taps one brass tuning fork; the resonance aligns the machines and produces one perfect glass sphere.
   - Preserved: inv-01, inv-02, inv-03, inv-04
   - Changed: arena, many_side, one_side, many_signals, single_answer, proof, meltdown
2. In a nocturnal vineyard, five autonomous pruning drones chase competing light paths until one gardener strikes a pitch pipe; the swarm settles into a single measured spiral and trims one clean row.
   - Preserved: inv-01, inv-02, inv-03, inv-04
   - Changed: arena, many_side, one_side, many_signals, single_answer, proof, sound

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

