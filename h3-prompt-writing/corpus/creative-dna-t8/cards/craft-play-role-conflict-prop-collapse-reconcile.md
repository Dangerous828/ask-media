# craft-play-role-conflict-prop-collapse-reconcile

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: craft-play-role-conflict-prop-collapse-reconcile
description: "Create original short videos using the 手作角色扮演｜分工亮相、道具误伤与集体和解 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 手作角色扮演｜分工亮相、道具误伤与集体和解

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Show all collaborators jointly making or arranging one communal prop before roles split.
- Assign opposing play roles through clear but replaceable costume or wearable-device signals.
- Connect one overcommitted gesture directly to the object's collapse and hold the collective reaction.
- End after everyone drops character and shares or repairs the altered space.

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
# 手作角色扮演｜分工亮相、道具误伤与集体和解 — 摘要

## 用途

先让小组共同制作轻质道具，再用服装和可穿戴装置分配对立角色；冲突必须围绕一个预先可见的脆弱公共道具展开，一次过度表演造成可读坍塌，所有人先停住确认后果，再共同退出角色并以修复或坐在一起结束。

## 推荐输入格式

`明确成年协作小组共同制作一个轻质公共道具 + 通过可替换服装或可穿戴装置分成玩闹对立角色 + 脆弱共享物在接触前持续可见 + 一次过度表演直接造成意外坍塌 + 集体停顿确认后果 + 退出角色并共同修复或聚拢`

## 可直接改写的简短示例

> 三名明确成年的博物馆教育员共同摆放泡沫星象台和一根脆弱轻木天线；镜头拉宽，双方围绕同一根轻木天线做一次克制模拟挑战；三人交换一次尴尬目光，放下角色姿态，一起跪下并用保留的碎件重建同一根天线

## 必须保留的结构锚点

- Show all collaborators jointly making or arranging one communal prop before roles split.
- Assign opposing play roles through clear but replaceable costume or wearable-device signals.
- Connect one overcommitted gesture directly to the object's collapse and hold the collective reaction.
- End after everyone drops character and shares or repairs the altered space.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 手作角色扮演｜分工亮相、道具误伤与集体和解 Template

## Mechanism

Begin with an original group of clearly adult collaborators jointly making or arranging one lightweight communal prop. Assign playful opposing roles through replaceable costume or wearable-device signals, then keep one visibly fragile shared object inside the confrontation geography before contact occurs. Let one overcommitted performance gesture cause that object to collapse, hold a collective pause long enough to register the unintended result, and end only after everyone drops the roles and repairs, gathers around or calmly shares the altered space. The reusable mechanism is cooperative baseline, role split, visible collateral risk, accidental consequence and group reconciliation—not the source pandas, faces, costumes, cardboard box, pinwheel, bamboo or stick tower, backyard, exact choreography, camera placement, animation treatment, Dreamina branding, creator identity or timing.

## Invariants

### inv-01

- Rule: Show all collaborators jointly making or arranging one communal prop before roles split.
- Purpose: Creates a cooperative baseline that the later conflict can visibly disturb.
- Failure if removed: Without shared ownership, the collapse reads as generic destruction rather than an unintended group consequence.

### inv-02

- Rule: Assign opposing play roles through clear but replaceable costume or wearable-device signals.
- Purpose: Makes the temporary conflict readable without requiring dialogue or identity copying.
- Failure if removed: If roles are ambiguous, the confrontation has no legible social structure.

### inv-03

- Rule: Keep one fragile shared object visible between the groups before contact.
- Purpose: Preloads a measurable collateral risk inside the scene geography.
- Failure if removed: A prop that appears only when it breaks feels like an inserted gag.

### inv-04

- Rule: Connect one overcommitted gesture directly to the object's collapse and hold the collective reaction.
- Purpose: Turns motion into an observable unintended consequence.
- Failure if removed: A cutaway collapse or instant recovery weakens causality and emotional timing.

### inv-05

- Rule: End after everyone drops character and shares or repairs the altered space.
- Purpose: Converts conflict into a complete reconciliation arc while retaining the consequence.
- Failure if removed: Ending on victory or resetting the prop loses the social payoff.


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

- Show all collaborators jointly making or arranging one communal prop before roles split.
- Assign opposing play roles through clear but replaceable costume or wearable-device signals.
- Connect one overcommitted gesture directly to the object's collapse and hold the collective reaction.
- End after everyone drops character and shares or repairs the altered space.

## Anti-Copy Boundary

- the source panda-like children, faces, bodies, fur, proportions, clothing, bandanas, goggles and poses
- the source leaf-backed villain costume, stacked cardboard control box, colored buttons, pinwheel and exact role arrangement
- the source backyard, fence, bushes, sunset layout, bamboo or stick tower and loose craft materials
- the source confrontation choreography, tower collapse, sitting pose, shot scale, timing and polished animation treatment
- the source creator identity, Dreamina and Seedance 2.5 claims, watermark, overlay and branding

## Transfer Tests

1. Three clearly adult museum educators assemble a lightweight foam planetarium in a courtyard, split into comet-guide and control-console roles, accidentally collapse a balsa antenna during mock play, then break character and repair it together.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. Three adult festival technicians arrange a fabric weather shrine, divide into wind-caller and portable-sensor teams, snag the central paper vane during an exaggerated test and finish seated together retying the frame.
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

