# flat-token-physical-spill-recovery

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: flat-token-physical-spill-recovery
description: "Create original short videos using the 平面物件落地｜打断表演与收拾恢复 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 平面物件落地｜打断表演与收拾恢复

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 先建立稳定平面布局
- 图形落成实体并打断活动
- 收拾后回到同一人物动作

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
# 平面物件落地｜打断表演与收拾恢复 — 摘要

## 用途

稳定平面布局中，图形落成实体打断动作，人物收拾后继续原活动。

## 推荐输入格式

`表演者＋原创平面图形＋实体掉落＋收拾恢复`

## 可直接改写的简短示例

> 米白排程板、六个无品牌彩色圆点、一名素蓝罩衫的成年纸偶表演者、小托盘。

## 必须保留的结构锚点

- 先建立稳定平面布局
- 图形落成实体并打断活动
- 收拾后回到同一人物动作

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 平面物件落地｜打断表演与收拾恢复 Template

## Mechanism

A performer moves within a stable graphic layout. Her movement sits immediately beside the flat-token-to-physical-prop spill, though the source does not prove one gesture caused it. The sudden fall interrupts the routine; a brief recovery restores performance. The paper-theatre transfer adds an explicit sweep trigger as an original causal enhancement, not a claimed source fact. Preserve boundary crossing and reaction-repair, not the branded desktop.

## Invariants

### inv-01

- Rule: Establish one performer inside a stable graphic layout first.
- Purpose: The audience knows the boundary.
- Failure if removed: Without stable layout the spill looks like generic confetti.

### inv-02

- Rule: Place performer motion immediately beside flat tokens gaining mass and falling, without claiming the source proves a particular trigger gesture; a new transfer may make the trigger explicit.
- Purpose: Creates a readable graphic-to-physical surprise while preserving source uncertainty.
- Failure if removed: Without motion adjacency the boundary break reads as unrelated decoration.

### inv-03

- Rule: Pause for reaction and recovery, then resume the same performer routine.
- Purpose: Completes comic arc.
- Failure if removed: Without repair and return this is only a VFX demonstration.


## Variable Slots

| Slot | Constraint |
|---|---|
| performer | One persistent adult. |
| layout | Original unbranded 2D tokens. |
| gesture | One clear trigger. |
| physical_props | Limited count, visible landings. |
| repair | Visible collection. |
| return | Resumes original routine. |

## Required Human-Facing Anchors

- 先建立稳定平面布局
- 图形落成实体并打断活动
- 收拾后回到同一人物动作

## Anti-Copy Boundary

- No branded OS desktop, recognizable app icons or logo art.
- No source person's face, costume or exact dance.
- No copied wallpaper or layout.

## Transfer Tests

1. An adult paper-theatre performer sweeps a hand across an unbranded schedule board. Six printed circles become small weighted discs and fall to the floor. She pauses, collects them in a tray and resumes her puppet routine.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: performer, layout, gesture, physical_props, repair, return
2. An adult museum guide points at an original projected star chart. Five plain glyphs become foam stars and drop onto a padded stage. She stacks them below the projection and resumes explaining.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: performer, layout, gesture, physical_props, repair, return

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

