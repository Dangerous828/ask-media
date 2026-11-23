# repeat-reset-escalating-mishap-anthology

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: repeat-reset-escalating-mishap-anthology
description: "Create original short videos using the 重复复位｜多场景小灾难逐次升级 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 重复复位｜多场景小灾难逐次升级

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Keep the same active-role and witness relationship readable across every reset.
- Establish an ordinary object and action before each mishap.
- Increase consequence scale or spatial reach across rounds.
- Hold both roles and the largest consequence together.

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
# 重复复位｜多场景小灾难逐次升级 — 摘要

## 用途

同一角色关系反复执行普通准备、主动动作、可见后果、见证者反应和场景复位；每轮更换物理问题并提高后果强度。

## 推荐输入格式

`固定角色关系 + 三轮准备/动作/后果/反应 + 场景复位 + 后果逐轮升级 + 最大结果同框`

## 可直接改写的简短示例

> 原创定格工坊第一幕，铜质学徒机器人拉动松弹簧，垫圈在同一盏绿色监督灯前散开；磁刷把颜料珠拉成扩大轨迹，绿灯清楚后仰，后果大于第一幕；铜机器人、倾斜绿灯与最大齿轮场同框停住，不加入对白或修复结果

## 必须保留的结构锚点

- Keep the same active-role and witness relationship readable across every reset.
- Establish an ordinary object and action before each mishap.
- Increase consequence scale or spatial reach across rounds.
- Hold both roles and the largest consequence together.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 重复复位｜多场景小灾难逐次升级 Template

## Mechanism

Repeat a compact vignette grammar across different spaces: ordinary setup, one autonomous action by the same active role, one visible material consequence, one reaction by the recurring witness, then a clean reset. Change the physical problem each round and increase consequence scale before a held final reaction.

## Invariants

### inv-01

- Rule: Keep the same active-role and witness relationship readable across every reset.
- Purpose: Makes separate rooms feel like one anthology.
- Failure if removed: Changing both roles turns the sequence into unrelated clips.

### inv-02

- Rule: Establish an ordinary object and action before each mishap.
- Purpose: Preserves visible cause and effect.
- Failure if removed: Opening on a mess removes responsibility and timing.

### inv-03

- Rule: Use a different material consequence in each round.
- Purpose: Creates variation rather than duplicate gags.
- Failure if removed: Repeating one mishap adds no proof.

### inv-04

- Rule: Increase consequence scale or spatial reach across rounds.
- Purpose: Builds measurable escalation.
- Failure if removed: Random intensity without a ladder feels arbitrary.

### inv-05

- Rule: Hold both roles and the largest consequence together.
- Purpose: Completes relationship and escalation.
- Failure if removed: Cutting before the reaction loses the payoff.


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

- Keep the same active-role and witness relationship readable across every reset.
- Establish an ordinary object and action before each mishap.
- Increase consequence scale or spatial reach across rounds.
- Hold both roles and the largest consequence together.

## Anti-Copy Boundary

- the source toddler and mother
- the exact household rooms
- the source food, furniture or domestic props
- the exact mishap order and reactions
- the source wardrobe and family identity

## Transfer Tests

1. Three stop-motion workshop vignettes follow one apprentice robot and one supervisor lamp: loose springs, runaway paint beads and a final avalanche of paper gears each reset to a new bench.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A miniature cloud keeper and one weather vane repeat three rooftop experiments: a fog puff, a rain ribbon and a final room-filling snow burst.
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

