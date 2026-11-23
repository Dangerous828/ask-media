# use-material-as-progress-clock

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: use-material-as-progress-clock
description: "Create original short videos using the 工艺过程｜材料覆盖当进度 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 工艺过程｜材料覆盖当进度

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 同一工艺物贯穿
- 选定材料变量只增不减
- 至少四个可区分阶段
- 最后明确揭晓成品

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
# 工艺过程｜材料覆盖当进度 — 摘要

## 用途

同一工艺物保持连续，用只增不减的材料变量作为清晰进度钟。

## 推荐输入格式

`同一工艺物 + 一个只增不减的材料变量 + 4个阶段 + 成品揭晓`

## 可直接改写的简短示例

> 同一块陶瓷浮雕保持在转台上，釉色覆盖从边缘、纹路、主体到全部表面只增不减，最后窑火反光中揭晓成品。

## 必须保留的结构锚点

- 同一工艺物贯穿
- 选定材料变量只增不减
- 至少四个可区分阶段
- 最后明确揭晓成品

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 工艺过程｜材料覆盖当进度 Template

## Mechanism

Compress a multi-stage making process around one persistent artifact and one irreversible visual variable that only increases—coverage, polish, oxidation, translucency or revealed pattern. Alternate contact-level macro proof with scale-restoring views, ensure each cut advances the same artifact, and reserve the longest hold for the completed state. Craft, object, material, palette, stage count and final display are variable.

## Invariants

### inv-01

- Rule: Establish one artifact in an unadvanced base state.
- Purpose: Creates the zero point for the visual clock.
- Failure if removed: Without a base state, progress cannot be measured.

### inv-02

- Rule: Keep object identity and defining geometry stable across process cuts.
- Purpose: Lets the viewer accumulate changes on one artifact.
- Failure if removed: Object swaps look like unrelated demonstrations.

### inv-03

- Rule: Advance one irreversible material variable in a single direction.
- Purpose: Turns coverage into an intuitive timeline.
- Failure if removed: Reversing or resetting the variable breaks progress.

### inv-04

- Rule: Show direct tool-to-material contact at each key state change.
- Purpose: Provides causal proof and tactile credibility.
- Failure if removed: Off-screen transformations feel like magic rather than craft.

### inv-05

- Rule: Give the finished artifact a longer clean hold after the final operation.
- Purpose: Rewards the compressed process and confirms completion.
- Failure if removed: Ending during the last tool action denies the payoff.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original subject whose identity and silhouette remain stable. |
| setting | A new setting with fixed spatial anchors and no source-specific location. |
| escalation_variable | One readable variable that changes monotonically or in countable stages. |
| performance_rule | One restrained performance rule that makes the mechanism legible. |
| camera_grammar | A coherent information order that does not copy the source shot boundaries. |
| payoff | One clean physical or graphic consequence that closes the causal chain. |
| sound_family | A new hierarchy of diegetic cues supporting each state change. |

## Required Human-Facing Anchors

- 同一工艺物贯穿
- 选定材料变量只增不减
- 至少四个可区分阶段
- 最后明确揭晓成品

## Anti-Copy Boundary

- red bulbous vase with raised coiled dragon-like relief
- gold leaf applied over red lacquer
- source Chinese numbered stage plaques
- source artisan face, workshop and exact tool sequence

## Transfer Tests

1. A ceramic relief tile progresses from pale bisque through carved channels to increasing translucent teal glaze coverage, final kiln gloss and a clean gallery reveal.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A wooden music-box lid moves from raw carving to increasing blue resin inlay, sanding, polish and a reflective final pattern.
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

