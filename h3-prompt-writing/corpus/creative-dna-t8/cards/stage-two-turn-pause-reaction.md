# stage-two-turn-pause-reaction

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-two-turn-pause-reaction
description: "Create original short videos using the 对话喜剧｜双轮停顿无声反应 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 对话喜剧｜双轮停顿无声反应

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 开场双人中景建立稳定眼线
- 只保留一轮第一人说话
- 两轮之间有一次清楚停顿
- 第二人只说一轮且动作克制
- 结尾第一人无声反应且不再增加说话轮次

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
# 对话喜剧｜双轮停顿无声反应 — 摘要

## 用途

双人同框先建立眼线，第一轮说话后留出清楚停顿，再完成第二轮说话并以第一人的无声反应收尾；具体对白和喜剧语义必须全新原创。

## 推荐输入格式

`双人中景 + 第一轮简短说话 + 一次可读停顿 + 第二轮简短说话 + 第一人的无声反应`

## 可直接改写的简短示例

> 两名原创博物馆夜班保安在休息室对坐：A 问雕像是否眨眼，停顿后 B 冷静回答“只有你转开视线时”，最后 A 无声看向黑暗展厅门，不增加第二句笑点。

## 必须保留的结构锚点

- 开场双人中景建立稳定眼线
- 只保留一轮第一人说话
- 两轮之间有一次清楚停顿
- 第二人只说一轮且动作克制
- 结尾第一人无声反应且不再增加说话轮次

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 对话喜剧｜双轮停顿无声反应 Template

## Mechanism

Use a neutral two-shot to establish equal conversational footing, show one visible speaking turn, hold a clearly readable pause, show a second speaking turn, and end on the first speaker's silent reaction. The source supports only this visual turn-taking and reaction grammar; any question, answer meaning or comic mismatch is an explicitly original instantiation slot, never a source-derived fact.

## Invariants

### inv-01

- Rule: Begin with a neutral two-shot and stable eye lines.
- Purpose: Makes later singles spatially and socially legible.
- Failure if removed: Opening on isolated faces hides the relationship.

### inv-02

- Rule: Use one compact first speaking turn, with its meaning supplied only by the new original instance.
- Purpose: Creates a clean expectation without inventing source semantics.
- Failure if removed: Multiple setup turns blur ownership and weaken the pause.

### inv-03

- Rule: Hold one clearly readable pause between the two visible speaking turns.
- Purpose: Builds a timing interval without inventing source semantics.
- Failure if removed: An immediate second turn removes the visible timing contrast.

### inv-04

- Rule: Use one compact second speaking turn with minimal gesture; its meaning is an original instance variable.
- Purpose: Preserves the visible turn-taking structure while allowing new content.
- Failure if removed: A large performance or extra line turns the held exchange into a sketch montage.

### inv-05

- Rule: End on the first character's silent reaction with no additional speaking turn.
- Purpose: Lets the final visible reaction complete the timing pattern.
- Failure if removed: Additional speaking turns weaken the final hold.


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

- 开场双人中景建立稳定眼线
- 只保留一轮第一人说话
- 两轮之间有一次清楚停顿
- 第二人只说一轮且动作克制
- 结尾第一人无声反应且不再增加说话轮次

## Anti-Copy Boundary

- Friends
- Joey Tribbiani
- Chandler Bing
- Central Perk
- source dialogue and wardrobe

## Transfer Tests

1. Two original night guards sit in a museum break room. One asks whether the marble statue blinked; after a pause the other says, 'Only when you look away,' and the first guard silently turns toward the dark gallery.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. Two lighthouse keepers share tea. One asks whether the foghorn ever gets lonely; after a pause the other answers, 'It calls everyone,' and the first keeper stops stirring.
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

