# handoff-ensemble-focus

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: handoff-ensemble-focus
description: "Create original short videos using the 群演聚焦接力｜全场到主位再回合奏 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 群演聚焦接力｜全场到主位再回合奏

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish the full ensemble and surrounding response field before isolating a lead.
- Bring two central contributors into one shared action before ownership narrows.
- Reintroduce the co-lead before the ending.
- Finish wide enough to show the ensemble responding in one synchronized state.

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
# 群演聚焦接力｜全场到主位再回合奏 — 摘要

## 用途

先建立完整群体与观众或工作场，再让两名中心贡献者进入共享动作；镜头隔离其中一名主位完成完整证明段，随后重新引入共同主位，并以更宽的同步群体终态收束。

## 推荐输入格式

`全体建立 + 主位聚焦 + 次主位回归 + 群体节奏持续 + 回到全体合奏终态`

## 可直接改写的简短示例

> 机械工坊全体先建立节奏，镜头聚焦粉色主位的工具动作，次主位随后回归并接力，最终退回全景呈现全部工作台同步运行。

## 必须保留的结构锚点

- Establish the full ensemble and surrounding response field before isolating a lead.
- Bring two central contributors into one shared action before ownership narrows.
- Reintroduce the co-lead before the ending.
- Finish wide enough to show the ensemble responding in one synchronized state.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 群演聚焦接力｜全场到主位再回合奏 Template

## Mechanism

Establish a complete ensemble and its audience or work field, bring two central contributors into a shared action, isolate one lead long enough for a complete proof phrase while the ensemble remains spatially implied, then reintroduce the co-lead and finish on a wider synchronized group state.

## Invariants

### inv-01

- Rule: Establish the full ensemble and surrounding response field before isolating a lead.
- Purpose: Makes later focus changes legible.
- Failure if removed: Opening close hides the ensemble stakes.

### inv-02

- Rule: Bring two central contributors into one shared action before ownership narrows.
- Purpose: Defines the co-lead relationship.
- Failure if removed: An immediate solo gives no handoff.

### inv-03

- Rule: Give one lead enough uninterrupted screen ownership to complete a proof phrase.
- Purpose: Makes the focus transfer countable.
- Failure if removed: Rapid cutting never establishes ownership.

### inv-04

- Rule: Reintroduce the co-lead before the ending.
- Purpose: Returns focus from individual to partnership.
- Failure if removed: A solo-only ending abandons the opening pair.

### inv-05

- Rule: Finish wide enough to show the ensemble responding in one synchronized state.
- Purpose: Closes the nested focus levels.
- Failure if removed: Ending close loses the group payoff.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair whose role is clear without source identity. |
| setting | A materially new setting with fixed spatial anchors and no source-specific location. |
| causal_carrier | One object, route, mark or device that visibly carries the causal chain. |
| state_change | Five ordered states with observable handoffs, not a decorative montage. |
| camera_grammar | A new proof-oriented information order that does not copy source shot boundaries. |
| payoff | A held final consequence that resolves or recontextualizes the setup. |
| sound_family | An original hierarchy of story-world cues supporting each visible change. |

## Required Human-Facing Anchors

- Establish the full ensemble and surrounding response field before isolating a lead.
- Bring two central contributors into one shared action before ownership narrows.
- Reintroduce the co-lead before the ending.
- Finish wide enough to show the ensemble responding in one synchronized state.

## Anti-Copy Boundary

- source retro male singers and band
- Eddie & The Comet Tails sign
- source stage, microphones and audience
- the exact rock performance blocking and wardrobe

## Transfer Tests

1. In a kinetic sculpture workshop, two lead technicians begin before a full crew and moving test wall; the camera isolates the color-calibration lead for one complete adjustment, reintroduces the motion lead, and ends wide as every module synchronizes.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family
2. At a botanical lantern launch, two coordinators begin among a full volunteer ring; one coordinator receives a complete close proof while setting the timing beacon, the second returns to trigger the release, and the final wide shows the whole ring lifting lantern pods together.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family

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

