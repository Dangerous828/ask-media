# prove-product-through-first-person-test

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: prove-product-through-first-person-test
description: "Create original short videos using the UGC测评｜开箱到一口实证 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# UGC测评｜开箱到一口实证

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 开场测评者与未开封产品同框
- 先完整展示内容再进入细节
- 只有一个产品专属功能证据
- 必须完成一次真实使用并保留结果
- 结尾产品与变化后的反应同框

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
# UGC测评｜开箱到一口实证 — 摘要

## 用途

真人与未开封产品同框起手，完整开箱后给一个关键微距证据，再完成真实使用，并让产品与变化后的反应一起收口。

## 推荐输入格式

`出镜测评者 + 未开封产品 + 完整内容展示 + 一个产品专属微距证据 + 一次完整使用 + 产品与反应同框`

## 可直接改写的简短示例

> 陶艺师测评便携手冲套件：先展示密封盒并完整摆出部件，微距证明滤网四分之一圈锁定，完成一次无渗漏冲煮与品尝，最后举起套件和干燥接缝并克制点头。

## 必须保留的结构锚点

- 开场测评者与未开封产品同框
- 先完整展示内容再进入细节
- 只有一个产品专属功能证据
- 必须完成一次真实使用并保留结果
- 结尾产品与变化后的反应同框

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# UGC测评｜开箱到一口实证 Template

## Mechanism

Structure a first-person product testimonial as a proof ladder: introduce the unopened object and speaker together, expose contents, isolate one tactile or functional macro proof, let the speaker perform one genuine use action, then hold the product and changed reaction together. The product claim must be earned by visible use rather than spoken hype.

## Invariants

### inv-01

- Rule: Open with presenter and unopened product in the same frame.
- Purpose: Binds person, object and expectation.
- Failure if removed: A product-only beauty shot lacks testimonial ownership.

### inv-02

- Rule: Reveal the complete contents before isolating details.
- Purpose: Gives macro proof a known context.
- Failure if removed: Macro-first editing can hide what is actually being evaluated.

### inv-03

- Rule: Choose one product-specific tactile or functional proof.
- Purpose: Makes the claim inspectable.
- Failure if removed: Generic close-ups create polish without evidence.

### inv-04

- Rule: Perform one complete use action with the outcome still visible.
- Purpose: Converts product state into demonstrated experience.
- Failure if removed: A cut before the result turns use into implication.

### inv-05

- Rule: End with product and changed human reaction readable together.
- Purpose: Links proof to evaluation.
- Failure if removed: A reaction without the object can feel unrelated or staged.


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

- 开场测评者与未开封产品同框
- 先完整展示内容再进入细节
- 只有一个产品专属功能证据
- 必须完成一次真实使用并保留结果
- 结尾产品与变化后的反应同框

## Anti-Copy Boundary

- source woman
- source burger and fries
- source packaging
- source caption and kitchen-like setting

## Transfer Tests

1. A ceramic artist unboxes a compact pour-over kit, reveals all pieces, uses a macro close-up on the locking filter seam, brews one cup, tastes it and holds the assembled kit with a calm approval reaction.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A cyclist tests a pocket rain-shell pouch, reveals the folded garment, uses a macro close-up on the sealed zipper, pulls it on under a spray test and ends holding the dry inner cuff beside a relieved expression.
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

