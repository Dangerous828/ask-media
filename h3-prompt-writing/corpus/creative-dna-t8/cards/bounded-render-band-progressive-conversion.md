# bounded-render-band-progressive-conversion

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: bounded-render-band-progressive-conversion
description: "Create original short videos using the 渲染扫描｜局部带逐段改写整体 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 渲染扫描｜局部带逐段改写整体

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish a stable subject and composition before the first conversion pass.
- Keep one readable moving boundary with old and new states visible at the same time.
- Accumulate converted coverage in an ordered progression rather than resetting each pass.
- Remove or deactivate the carrier only after the whole target region is converted and hold the stable result.

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
# 渲染扫描｜局部带逐段改写整体 — 摘要

## 用途

让一条边界清楚的活动带沿主体移动，带内即时显示转换后的媒介，带外继续保留原状态；多次通过累积覆盖整体，最后让扫描带退出以证明完整、稳定的转换结果。

## 推荐输入格式

`稳定主体 + 边界清楚的转换带 + 新旧状态同框 + 单向累积覆盖 + 载体退出后的完整结果`

## 可直接改写的简短示例

> 原创文物修复室里，一张风化木质戏剧面具固定在炭灰支架上，发光竖尺停在面具外，开场全部保持木材；第二次通过中心，眼鼻口在木与玻璃边界上保持一致，已完成区域不回退；竖尺完全滑出，完整玻璃面具独立留在原支架上，只出现一次自然展厅光变化

## 必须保留的结构锚点

- Establish a stable subject and composition before the first conversion pass.
- Keep one readable moving boundary with old and new states visible at the same time.
- Accumulate converted coverage in an ordered progression rather than resetting each pass.
- Remove or deactivate the carrier only after the whole target region is converted and hold the stable result.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 渲染扫描｜局部带逐段改写整体 Template

## Mechanism

Move one sharply bounded rendering carrier across a stable subject; convert only the area inside it, preserve alignment across both edges, accumulate coverage through distinct passes, then remove the carrier and hold the fully converted result.

## Invariants

### inv-01

- Rule: Establish a stable subject and composition before the first conversion pass.
- Purpose: Supplies a trustworthy source-state reference.
- Failure if removed: Starting mid-conversion hides what changed.

### inv-02

- Rule: Keep one readable moving boundary with old and new states visible at the same time.
- Purpose: Makes the carrier's local responsibility directly observable.
- Failure if removed: A full-frame dissolve removes the bounded comparison.

### inv-03

- Rule: Preserve identity, pose and spatial alignment across every boundary crossing.
- Purpose: Proves medium conversion instead of subject replacement.
- Failure if removed: Misregistered features look like morphing or a new subject.

### inv-04

- Rule: Accumulate converted coverage in an ordered progression rather than resetting each pass.
- Purpose: Gives each pass measurable completion value.
- Failure if removed: Resetting the prior area destroys the build toward a whole result.

### inv-05

- Rule: Remove or deactivate the carrier only after the whole target region is converted and hold the stable result.
- Purpose: Shows that the converted state survives independently.
- Failure if removed: Ending with the carrier active leaves completion ambiguous.


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

- Establish a stable subject and composition before the first conversion pass.
- Keep one readable moving boundary with old and new states visible at the same time.
- Accumulate converted coverage in an ordered progression rather than resetting each pass.
- Remove or deactivate the carrier only after the whole target region is converted and hold the stable result.

## Anti-Copy Boundary

- the source young woman
- the exact bedroom or studio interior
- the anime portrait style
- the horizontal hand-carried render strip
- the exact face-to-body conversion order

## Transfer Tests

1. A translucent embroidery hoop moves over a clay museum bird; only the enclosed zone becomes stitched textile, then the hoop exits and the complete textile bird remains.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A vertical frost-light scanner crosses a greenhouse facade; panes inside the strip become paper-cut layers while untouched panes remain glass, ending on one complete paper conservatory.
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

