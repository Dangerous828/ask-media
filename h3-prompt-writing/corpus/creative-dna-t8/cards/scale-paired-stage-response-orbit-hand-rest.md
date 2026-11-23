# scale-paired-stage-response-orbit-hand-rest

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: scale-paired-stage-response-orbit-hand-rest
description: "Create original short videos using the 跨尺度舞台搭档｜环绕回应、手掌落点与共同定格 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 跨尺度舞台搭档｜环绕回应、手掌落点与共同定格

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- One clearly adult primary performer and one original miniature companion retain distinct stable identities.
- The environment supplies continuous scale references for both characters.
- The miniature companion reaches the hand through one continuous orbit without arbitrary scale change or teleportation.
- A shared terminal pose keeps both scales, identities and the original stage readable at once.

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
# 跨尺度舞台搭档｜环绕回应、手掌落点与共同定格 — 摘要

## 用途

锁定成年表演者、微型原创伙伴和同一舞台，先用独立动作建立双方身份，再让小伙伴沿可追踪环线回应人物手势；终局必须落到人物手掌或近身位置，并以共同姿态证明跨尺度关系。

## 推荐输入格式

`一名明确成年原创主表演者和一个原创微型伙伴 + 固定舞台与连续尺度参照 + 主体手势先发生、微型伙伴沿可追踪路线回应 + 一次完整环绕与手掌或近身落点 + 终局同框同时证明两种尺度、两个身份和共同姿态`

## 可直接改写的简短示例

> 建立原创成年爵士歌手：银色短发、祖母绿西装、月牙胸针，位于午夜蓝俱乐部舞台和奶油色三角钢琴旁。；歌手用持麦手画出一个缓慢半圆，飞蛾沿同一弧线穿过前景灯光，并以两次振翅闪光回应。；两者在准确原创标题【SMALL LIGHT / BIG STAGE】下共同鞠躬，歌手、飞蛾、钢琴和舞台结构保持不变。

## 必须保留的结构锚点

- One clearly adult primary performer and one original miniature companion retain distinct stable identities.
- The environment supplies continuous scale references for both characters.
- The miniature companion reaches the hand through one continuous orbit without arbitrary scale change or teleportation.
- A shared terminal pose keeps both scales, identities and the original stage readable at once.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 跨尺度舞台搭档｜环绕回应、手掌落点与共同定格 Template

## Mechanism

锁定成年表演者、微型原创伙伴和同一舞台，先用独立动作建立双方身份，再让小伙伴沿可追踪环线回应人物手势；终局必须落到人物手掌或近身位置，并以共同姿态证明跨尺度关系。 The reusable mechanism preserves causal order, spatial anchors and the final proof while replacing every source-specific person, location, object, wording, choreography and design.

## Invariants

### inv-01

- Rule: One clearly adult primary performer and one original miniature companion retain distinct stable identities.
- Purpose: Establishes the baseline identity, object or geography that every later state must preserve.
- Failure if removed: Without this exact baseline rule, later changes cannot be attributed to the same subject, object or place, so the sequence loses its reference state. Removed rule: "One clearly adult primary performer and one original miniature companion retain distinct stable identities."

### inv-02

- Rule: The environment supplies continuous scale references for both characters.
- Purpose: Makes the visible trigger precede and explain the first mechanism response.
- Failure if removed: Without this exact trigger rule, the response appears spontaneously and the central cause-and-effect claim is no longer demonstrated. Removed rule: "The environment supplies continuous scale references for both characters."

### inv-03

- Rule: Every companion move visibly answers a preceding adult gesture along a traceable route.
- Purpose: Keeps the middle progression registered instead of allowing an unexplained reset.
- Failure if removed: Without this exact progression rule, the middle can jump to a replacement state and the accumulated result is no longer traceable. Removed rule: "Every companion move visibly answers a preceding adult gesture along a traceable route."

### inv-04

- Rule: The miniature companion reaches the hand through one continuous orbit without arbitrary scale change or teleportation.
- Purpose: Reconnects the changed or partial state to the established subject and spatial anchor.
- Failure if removed: Without this exact reconnection rule, detail or transformed shots can belong to a different subject or geography and continuity cannot be verified. Removed rule: "The miniature companion reaches the hand through one continuous orbit without arbitrary scale change or teleportation."

### inv-05

- Rule: A shared terminal pose keeps both scales, identities and the original stage readable at once.
- Purpose: Turns the terminal hold into observable proof that the mechanism completed.
- Failure if removed: Without this exact terminal-proof rule, the sequence stops on motion alone and never confirms the promised outcome or preserved aftermath. Removed rule: "A shared terminal pose keeps both scales, identities and the original stage readable at once."


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

- One clearly adult primary performer and one original miniature companion retain distinct stable identities.
- The environment supplies continuous scale references for both characters.
- The miniature companion reaches the hand through one continuous orbit without arbitrary scale change or teleportation.
- A shared terminal pose keeps both scales, identities and the original stage readable at once.

## Anti-Copy Boundary

- all source faces, bodies, wardrobe, identities and creator-specific character designs
- the source location, set dressing, props, products and exact environmental geometry
- all source words, logos, watermarks, typefaces and brand identifiers
- the source choreography, exact camera path, shot durations and transition timing
- the source palette, signature effects, prompt wording, creator handle and narrative particulars

## Transfer Tests

1. An adult singer and a palm-sized glass moth turn one hand arc into a shared club-stage bow.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. An adult watchmaker and a thumb-sized brass bird exchange tool gestures before the bird settles on a glove.
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

