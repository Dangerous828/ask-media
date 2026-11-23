# facial-action-unit-calibration

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: facial-action-unit-calibration
description: "Create original short videos using the 表情校准｜固定身份下的动作单元序列 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 表情校准｜固定身份下的动作单元序列

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Lock one face, background, lighting direction and camera axis before any expression change.
- Separate the expression into readable local units rather than morphing the whole face continuously.
- Keep head motion subordinate to eye, brow, mouth and cheek evidence.
- Use a late closer crop only after identity has been repeatedly proven.

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
# 表情校准｜固定身份下的动作单元序列 — 摘要

## 用途

锁定人物、光线和视角，只让眼睑、眉部、下颌、视线和唇形等局部动作单元分段变化；中间用微小复位防止表情混成连续表演，末段收紧景别检验身份与细节仍稳定。

## 推荐输入格式

`单一稳定人像 + 固定光线背景视角 + 至少4组分离面部动作 + 1次微小复位 + 后段细节近景`

## 可直接改写的简短示例

> 年轻陶瓷快递员在冷色医疗亭中保持同一身份与正面机位，依次展示单侧微笑、闭眼、抬眉、侧视和圆唇；中间短暂回中性，最后只推进到面罩密封近景。

## 必须保留的结构锚点

- Lock one face, background, lighting direction and camera axis before any expression change.
- Separate the expression into readable local units rather than morphing the whole face continuously.
- Keep head motion subordinate to eye, brow, mouth and cheek evidence.
- Use a late closer crop only after identity has been repeatedly proven.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 表情校准｜固定身份下的动作单元序列 Template

## Mechanism

A facial calibration sequence becomes reusable when identity, lighting, background and camera axis stay fixed while distinct facial action units change one group at a time. Brief micro-resets preserve comparability, and a late controlled crop can test fine identity stability without turning the sequence into a narrative performance.

## Invariants

### inv-01

- Rule: Lock one face, background, lighting direction and camera axis before any expression change.
- Purpose: Creates a reliable comparison baseline.
- Failure if removed: Changing the portrait setup makes action units impossible to compare.

### inv-02

- Rule: Separate the expression into readable local units rather than morphing the whole face continuously.
- Purpose: Makes each change diagnosable and reusable.
- Failure if removed: A blended emotional performance hides which feature changed.

### inv-03

- Rule: Insert at least one partial reset toward the baseline between larger changes.
- Purpose: Prevents accumulated distortion and preserves identity.
- Failure if removed: Without a reset, changes can drift into a different face.

### inv-04

- Rule: Keep head motion subordinate to eye, brow, mouth and cheek evidence.
- Purpose: Maintains a stable portrait while allowing orientation tests.
- Failure if removed: Large head turns replace facial proof with pose variation.

### inv-05

- Rule: Use a late closer crop only after identity has been repeatedly proven.
- Purpose: Tests detail stability and provides a clear endpoint.
- Failure if removed: Opening in extreme close-up removes the identity baseline.


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

- Lock one face, background, lighting direction and camera axis before any expression change.
- Separate the expression into readable local units rather than morphing the whole face continuously.
- Keep head motion subordinate to eye, brow, mouth and cheek evidence.
- Use a late closer crop only after identity has been repeatedly proven.

## Anti-Copy Boundary

- older bald grey-bearded man
- black shirt
- dark paneled studio portrait
- source facial-expression order
- source final mouth close-up

## Transfer Tests

1. A young ceramic courier in a cool medical kiosk performs a nonverbal visor-fit calibration: neutral baseline, one-sided brow lift, isolated lower-eyelid tension, closed-lip jaw shift, then one nostril-and-cheek action. A brief neutral reset separates the tests, and the only late close crop verifies the unchanged eye-corner and temple visor seam.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A handcrafted wooden puppet in a sunlit rehearsal booth tests five mechanical face controls in a new order: left brow plate, paired eye shutters, closed jaw sliding sideways, one cheek lever, then a full neutral reset. The camera ends on the unchanged eye hinge and wood grain, never on the mouth.
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

