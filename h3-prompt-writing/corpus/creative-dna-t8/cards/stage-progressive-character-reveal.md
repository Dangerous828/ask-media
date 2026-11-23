# stage-progressive-character-reveal

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-progressive-character-reveal
description: "Create original short videos using the 角色登场｜细节到全身揭晓 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 角色登场｜细节到全身揭晓

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 从可识别细节开始
- 揭晓尺度逐步扩大
- 角色只做一次代表动作
- 以全身定格完成身份确认

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
# 角色登场｜细节到全身揭晓 — 摘要

## 用途

从标志细节开始，逐层扩展到面部、动作和全身英雄定格。

## 推荐输入格式

`标志细节→局部轮廓→面部→一次动作→全身英雄定格`

## 可直接改写的简短示例

> 先拍老式列车长的黄铜打票钳，再露出制服轮廓和面部；他只完成一次打票动作，最后在蒸汽站台中全身英雄定格。

## 必须保留的结构锚点

- 从可识别细节开始
- 揭晓尺度逐步扩大
- 角色只做一次代表动作
- 以全身定格完成身份确认

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 角色登场｜细节到全身揭晓 Template

## Mechanism

Reveal one stable character through a controlled information ladder: signature detail, partial or rear silhouette, face, one restrained personality action and complete hero view. Each stage must answer one identity question while preserving exact defining features and calm secondary motion. Character, medium, environment, reveal detail, gesture, camera axis and mood are variable.

## Invariants

### inv-01

- Rule: Begin on one signature detail rather than the full design.
- Purpose: Creates an identity question and gives small features value.
- Failure if removed: A full-body opening removes progressive revelation.

### inv-02

- Rule: Use a partial or rear silhouette before showing the face.
- Purpose: Establishes body language and delays recognition.
- Failure if removed: Jumping directly to a portrait flattens the reveal ladder.

### inv-03

- Rule: Preserve defining identity, materials and silhouette through every stage.
- Purpose: Makes separate shots read as one character.
- Failure if removed: Redesign drift breaks trust and comparison.

### inv-04

- Rule: Allow only one restrained signature action after the face reveal.
- Purpose: Adds personality without replacing presentation with action.
- Failure if removed: Multiple gestures or combat beats dilute the introduction.

### inv-05

- Rule: End on a clean complete hero view and hold it.
- Purpose: Provides the promised design proof.
- Failure if removed: Cropping or immediate exit denies completion.


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

- 从可识别细节开始
- 揭晓尺度逐步扩大
- 角色只做一次代表动作
- 以全身定格完成身份确认

## Anti-Copy Boundary

- source black-haired female design with cream oversized sleeves and red ties
- repeated character-sheet strip beneath every shot
- source sunlit stone courtyard and exact orbit
- source hand-to-eye gesture, boots and final low-angle pose

## Transfer Tests

1. A retro-futurist train conductor is revealed through a gloved ticket-punch detail, a side silhouette behind frosted carriage glass, a face reveal as the door opens, one waist-level ticket punch and a high-angle full-body platform hold.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A moss-armored forest courier appears through a shoulder clasp, a side silhouette behind hanging roots, a profile reveal, one waist-level map fold and a complete eye-level stance beneath a canopy.
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

