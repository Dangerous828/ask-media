# persistent-matchup-strip-causal-rally-payoff

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: persistent-matchup-strip-causal-rally-payoff
description: "Create original short videos using the 对阵条不掉线｜小球方向连续到决胜反应 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 对阵条不掉线｜小球方向连续到决胜反应

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Keep one fixed two-competitor identity strip registered throughout the sequence.
- Establish the play axis and both starting positions before the rally accelerates.
- Use at least one overhead recalibration before the decisive exchange.
- Show the scoring outcome and contrasting reactions before ending, with the identity strip still visible.

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
# 对阵条不掉线｜小球方向连续到决胜反应 — 摘要

## 用途

让固定对阵信息条持续占据画面一部分，作为高速剪辑中的身份和阵营锚点；动态区域则按发球、接球、相持、险球和决胜顺序推进，每次切镜都用球的入射方向、击球手或身体重心完成接力，最后必须给出同一球的落点结果和双方不同反应。

## 推荐输入格式

`固定双人对阵信息条 + 先交代动作轴线 + 同一小物体发出/接回/反击/决胜 + 每次切镜继承方向/击打侧/重心 + 1次俯视重校 + 可见得分结果和双方反应`

## 可直接改写的简短示例

> 上方动作区同时交代成年钴蓝ORBIT、琥珀TIDE、两端球门和球台轴线；下方四分之一固定两侧剪影、队名和0-0比分；只在同一未决分中交替一次球拍近景、一次面部反应和一次低位球台视角；TIDE伸展反击，ORBIT回中；冰球完整越过ORBIT球门线，固定对阵条只把比分改为0-1；TIDE克制举拳，ORBIT放低球拍

## 必须保留的结构锚点

- Keep one fixed two-competitor identity strip registered throughout the sequence.
- Establish the play axis and both starting positions before the rally accelerates.
- Use at least one overhead recalibration before the decisive exchange.
- Show the scoring outcome and contrasting reactions before ending, with the identity strip still visible.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 对阵条不掉线｜小球方向连续到决胜反应 Template

## Mechanism

Reserve one fixed identity strip for two original competitors, team colors and a compact matchup title; keep it registered through the entire sequence. In the action region, establish the play axis, then build one causally continuous rally through serve, reception, counter, pressure exchange and decisive contact. Every cut must inherit the small object's incoming direction, striking side or player weight shift; use at least one overhead view to recalibrate geography. End only after the object's landing or scoring state is visible, followed by contrasting winner and loser reactions while the identity strip persists. The reusable mechanism is persistent matchup orientation plus small-object causal continuity and terminal reaction—not the source countries, athletes, faces, uniforms, table, paddles, poster art, flags, words, exact rally, camera, crowd, creator identity or timing.

## Invariants

### inv-01

- Rule: Keep one fixed two-competitor identity strip registered throughout the sequence.
- Purpose: Prevents orientation loss during high-density cuts.
- Failure if removed: If the strip moves or disappears, fast inserts can become anonymous highlights.

### inv-02

- Rule: Establish the play axis and both starting positions before the rally accelerates.
- Purpose: Gives each later direction a spatial reference.
- Failure if removed: Close-ups without a baseline make returns impossible to parse.

### inv-03

- Rule: Carry every cut through incoming object direction, striking side or body-weight transfer.
- Purpose: Preserves one causal rally across changing shot scales.
- Failure if removed: Unmatched ball motion turns the point into disconnected spectacle.

### inv-04

- Rule: Use at least one overhead recalibration before the decisive exchange.
- Purpose: Restores table or field geography as density peaks.
- Failure if removed: Without recalibration, the terminal exchange loses positional meaning.

### inv-05

- Rule: Show the scoring outcome and contrasting reactions before ending, with the identity strip still visible.
- Purpose: Closes action, result and social interpretation together.
- Failure if removed: Celebration without a result is unsupported; a result without reactions lacks payoff.


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

- Keep one fixed two-competitor identity strip registered throughout the sequence.
- Establish the play axis and both starting positions before the rally accelerates.
- Use at least one overhead recalibration before the decisive exchange.
- Show the scoring outcome and contrasting reactions before ending, with the identity strip still visible.

## Anti-Copy Boundary

- the source countries, national labels, flags, athlete faces, bodies, uniforms and exact team colors
- the source table-tennis table, paddles, ball path, serves, dives, returns, celebration and crowd reactions
- the source persistent poster art, typography, portraits, brush graphics, copy and lower-half layout
- the source camera sequence, overheads, close-ups, exact 15-second rally timing and animation treatment
- the source creator identity, Seedance 2.5 and GPT Image 2 claims, watermark, platform overlay and branding

## Transfer Tests

1. Two original air-hockey pilots, ORBIT and TIDE, play one continuous glowing-puck point while a fixed lower matchup strip remains. Serve direction, paddle side, overhead rink recalibration, decisive corner rebound and opposed final reactions all close one point.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. Two stop-motion beetle goalkeepers volley one paper seed across a leaf table. A fixed museum label strip identifies COPPER and MOSS while seed direction, leg contact, top view, edge landing and winner/loser posture remain causal.
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

