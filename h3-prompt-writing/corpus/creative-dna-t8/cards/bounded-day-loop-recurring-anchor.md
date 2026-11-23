# bounded-day-loop-recurring-anchor

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: bounded-day-loop-recurring-anchor
description: "Create original short videos using the 日程闭环｜重复锚点串联整日任务 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 日程闭环｜重复锚点串联整日任务

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Open on one inactive base state with a visible time or wake cue.
- Build a readable readiness package through at least three distinct preparation duties.
- Complete one visible destination duty before beginning the return.
- Return the same identity and object anchors to the original base and settle into a resting state.

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
# 日程闭环｜重复锚点串联整日任务 — 摘要

## 用途

从一个静止起点出发，用重复人物特征和随身物串联准备、出发、通勤与工作，并在片尾回到与开场相呼应的休息状态；高密度切换仍保持一天的因果顺序。

## 推荐输入格式

`静止基地与时间提示 + 至少三项准备任务 + 身份/随身物锚点 + 通勤与目的地任务 + 返回基地休息`

## 可直接改写的简短示例

> 原创微缩种子档案馆黎明，一名毛毡管理员躺在叶片吊床旁，黄铜露水钟、三个空种子位和苔藓挎包同框；钟响一次后睁眼；准备完成的管理员离开壁龛，苔藓挎包和一角外露信封持续作为锚点，层层档案架向下滑过；管理员把三封信放回原位，将同一苔藓挎包置于黄铜露水钟下并重新躺进叶片吊床，全部锚点可读

## 必须保留的结构锚点

- Open on one inactive base state with a visible time or wake cue.
- Build a readable readiness package through at least three distinct preparation duties.
- Complete one visible destination duty before beginning the return.
- Return the same identity and object anchors to the original base and settle into a resting state.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 日程闭环｜重复锚点串联整日任务 Template

## Mechanism

Open on one inactive home state, build a visible readiness package through several compact preparation duties, carry recurring identity and object anchors through departure, transit and one productive destination duty, then return those same anchors to the original base and settle into a resting state that visibly closes the day loop.

## Invariants

### inv-01

- Rule: Open on one inactive base state with a visible time or wake cue.
- Purpose: Defines the start of a bounded day cycle.
- Failure if removed: An already active opening removes the loop baseline.

### inv-02

- Rule: Build a readable readiness package through at least three distinct preparation duties.
- Purpose: Makes departure causally earned.
- Failure if removed: Unrelated grooming inserts create montage without progression.

### inv-03

- Rule: Carry stable identity and at least one recurring object anchor from the base into transit.
- Purpose: Preserves the subject through dense location changes.
- Failure if removed: Changing identity or losing all anchors breaks the day route.

### inv-04

- Rule: Complete one visible destination duty before beginning the return.
- Purpose: Gives the commute a concrete purpose.
- Failure if removed: Travel without a task leaves the middle unresolved.

### inv-05

- Rule: Return the same identity and object anchors to the original base and settle into a resting state.
- Purpose: Closes the day as a visible cycle.
- Failure if removed: Ending elsewhere turns the sequence into an open travel montage.


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

- Open on one inactive base state with a visible time or wake cue.
- Build a readable readiness package through at least three distinct preparation duties.
- Complete one visible destination duty before beginning the return.
- Return the same identity and object anchors to the original base and settle into a resting state.

## Anti-Copy Boundary

- the source black-haired anime woman with red glasses and S cardigan
- the source smartphone alarm, toast, toothbrush and shoulder bag
- the source apartment, subway platform, office and bedroom return
- the source exact morning routine and commute order
- the source clothing marks, laptop interface and room layout

## Transfer Tests

1. In an original miniature seed archive, a felt librarian wakes beside a brass dew clock, cleans its viewing lens, packs three labeled seed envelopes and fastens a moss satchel, rides a leaf elevator to catalogue one glowing pod, then returns the same satchel and envelopes to its alcove and folds into a hammock beside the dew clock.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In realistic orbital maintenance, one compact inspection drone wakes on a charging cradle, clears its optic, loads a sealant cartridge and unlocks two stabilizers, travels through a tube junction to patch one radiator seam, then returns with the same cartridge shell and status light to dock and power down.
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

