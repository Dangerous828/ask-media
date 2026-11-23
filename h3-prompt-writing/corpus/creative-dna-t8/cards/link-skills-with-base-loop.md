# link-skills-with-base-loop

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: link-skills-with-base-loop
description: "Create original short videos using the 技能展示｜基础动作串联升级 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 技能展示｜基础动作串联升级

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 基础动作反复返回
- 至少三项技能逐级变难
- 每个机位只承担一种证明任务
- 峰值后回到基础循环

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
# 技能展示｜基础动作串联升级 — 摘要

## 用途

持续基础动作连接逐级高级技能，每个机位只证明一种运动，峰值后回到基础循环。

## 推荐输入格式

`持续基础动作 + 3种高级技能 + 每次不同功能机位 + 节奏/接触声连续 + 回到基础动作`

## 可直接改写的简短示例

> 检修无人机保持稳定巡航基础动作，依次完成窄缝侧飞、旋转扫描和高速对接；每段用不同机位证明技能，峰值后回到同一巡航节奏。

## 必须保留的结构锚点

- 基础动作反复返回
- 至少三项技能逐级变难
- 每个机位只承担一种证明任务
- 峰值后回到基础循环

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 技能展示｜基础动作串联升级 Template

## Mechanism

Start inside one continuous base motion and make it the mandatory entry and exit for every distinct skill. Increase difficulty across countable stages, assign each camera angle a verification purpose such as contact, clearance, rotation or recovery, combine learned principles near the end, then perform one peak variation and visibly return to the unchanged base loop.

## Invariants

### inv-01

- Rule: Begin mid-loop and keep the base motion active between every skill.
- Purpose: Creates continuous connective tissue.
- Failure if removed: Static resets turn the piece into disconnected highlights.

### inv-02

- Rule: Every skill must depart from and visibly return to the loop.
- Purpose: Proves real continuity.
- Failure if removed: Cuts can otherwise hide failed transitions.

### inv-03

- Rule: Increase difficulty through distinct movement properties.
- Purpose: Builds a readable skill ladder.
- Failure if removed: More of the same move adds speed but not progression.

### inv-04

- Rule: Give each camera angle one proof job.
- Purpose: Makes cutting informative.
- Failure if removed: Decorative angle changes can obscure mechanics.

### inv-05

- Rule: After the peak, return to the original loop without stopping.
- Purpose: Closes the structure and proves control.
- Failure if removed: A freeze at the peak abandons the connective rule.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original subject or system whose identity remains stable. |
| setting | A new setting with fixed spatial anchors. |
| escalation_variable | One visible variable that changes in countable causal stages. |
| performance_rule | A restrained behavior rule that makes the mechanism legible. |
| camera_grammar | A coherent information order that does not copy source shot boundaries. |
| payoff | One clean physical or graphic consequence. |
| sound_family | A new hierarchy of diegetic cues supporting state changes. |

## Required Human-Facing Anchors

- 基础动作反复返回
- 至少三项技能逐级变难
- 每个机位只承担一种证明任务
- 峰值后回到基础循环

## Anti-Copy Boundary

- male capoeira practitioner in white abada
- Salvador da Bahia colorful street
- ginga and named capoeira moves
- berimbau rhythm and the source character sheet

## Transfer Tests

1. An autonomous inspection drone maintains a figure-eight hover loop between gap threading, roll scan, inverted inspection and precision docking, with each angle proving clearance or recovery.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A potter's wheel hand rhythm links centering, collar lift, rib compression and one tall pull before returning to the same centering cadence.
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

