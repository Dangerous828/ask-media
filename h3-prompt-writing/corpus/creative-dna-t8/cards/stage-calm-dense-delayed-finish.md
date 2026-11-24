# stage-calm-dense-delayed-finish

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-calm-dense-delayed-finish
description: "Create original short videos using the 对决节奏｜静止密战一击定局 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 对决节奏｜静止密战一击定局

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 安静建立可读
- 中段交换连续且高密
- 决定性干预只有一次
- 假稳定后才出现不可逆结果

3. Change source-specific people, setting, props, palette, dialogue, shot boundaries, sound family, and payoff surfaces together.
4. Compile MiniMax H3 and Seedance 2.0 independently; do not leak one model's field syntax into the other.
5. Silently verify anchor coverage, continuity, timing, physical causality, and anti-copy distance before returning the final prompts.

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
# 对决节奏｜静止密战一击定局 — 摘要

## 用途

先安静建立，进入连续密集交换，再用一次决定性干预、短暂假稳定和延迟结果终结。

## 推荐输入格式

`两个主体/系统 + 可读静止 + 连续密集交换 + 一次决定性干预 + 短暂假稳定 + 延迟结果`

## 可直接改写的简短示例

> 两组动力雕塑先静止对峙，随后连续交换高速磁片；其中一组只做一次反向脉冲，场面短暂恢复平静，数秒后对方结构延迟塌落。

## 必须保留的结构锚点

- 安静建立可读
- 中段交换连续且高密
- 决定性干预只有一次
- 假稳定后才出现不可逆结果

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 对决节奏｜静止密战一击定局 Template

## Mechanism

Organize a two-agent confrontation into three readable states: measured stillness, one continuous dense exchange, and a single decisive intervention. After the intervention, preserve one short false-stability beat before an irreversible physical consequence confirms the result; end on the initiator's controlled state rather than another attack.

## Invariants

### inv-01

- Rule: Begin with readable stillness and a clear relation between both agents.
- Purpose: Establishes parity and spatial stakes.
- Failure if removed: Immediate action removes the contrast state.

### inv-02

- Rule: Treat the middle as one continuous exchange rather than unrelated highlights.
- Purpose: Builds pressure while preserving causality.
- Failure if removed: Disconnected cuts make the decisive event arbitrary.

### inv-03

- Rule: Use only one identifiable state-changing intervention.
- Purpose: Creates a legible decision point.
- Failure if removed: Multiple finishers compete for causal credit.

### inv-04

- Rule: Hold a short false-stability beat after intervention.
- Purpose: Lets the audience register cause before effect.
- Failure if removed: Immediate collapse loses the delayed proof.

### inv-05

- Rule: Confirm the outcome through irreversible physical state while the initiator stays controlled.
- Purpose: Provides closure without restarting action.
- Failure if removed: A reaction-only ending fails to prove the result.


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

- 安静建立可读
- 中段交换连续且高密
- 决定性干预只有一次
- 假稳定后才出现不可逆结果

## Anti-Copy Boundary

- female swordswoman in red
- white-robed assassin
- snow-covered temple courtyard
- blade trap, finishing cut and delayed kneeling fall

## Transfer Tests

1. Two kinetic sculptures start motionless, enter a dense fin-interlock exchange, one alignment pin changes the system, then a counterweight drops after a short false-stable pause.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. Two autonomous sorting arms begin parked, exchange parcels rapidly, one gate reversal changes flow and a delayed bin lock proves the win state.
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

