# fold-metrics-to-current-state

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: fold-metrics-to-current-state
description: "Create original short videos using the 数据折叠｜总量下钻到当前值 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 数据折叠｜总量下钻到当前值

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Open with one dominant total and a compact label before showing its evidence.
- Unfold the claim into at least two itemized records with visible category separation.
- Compress the detailed records into one aggregate result before changing metric family.
- End on the current-state value and add only one restrained annotation after the value is readable.

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
# 数据折叠｜总量下钻到当前值 — 摘要

## 用途

用一个超大总量建立尺度，展开明细记录证明总量，再折回聚合结果并切换到当前状态值，最后只用一次克制标注锁定结论。

## 推荐输入格式

`超大总量 + 至少2条分类明细 + 聚合结果 + 相关里程碑 + 当前状态值 + 单次克制标注`

## 可直接改写的简短示例

> 一张纸艺能源账单先显示全年总量，翻开展示三条月度记录，再折叠为季度均值；侧页露出节能里程碑，最后展开当前月数值并只盖一个确认章。

## 必须保留的结构锚点

- Open with one dominant total and a compact label before showing its evidence.
- Unfold the claim into at least two itemized records with visible category separation.
- Compress the detailed records into one aggregate result before changing metric family.
- End on the current-state value and add only one restrained annotation after the value is readable.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 数据折叠｜总量下钻到当前值 Template

## Mechanism

Open with one oversized total that calibrates scale, unfold into itemized records that prove the claim, refold those records into an aggregate result, pivot through one intermediate milestone to a current-state value, then use one restrained manual annotation to lock the conclusion.

## Invariants

### inv-01

- Rule: Open with one dominant total and a compact label before showing its evidence.
- Purpose: Creates immediate scale and a clear question about how the total was earned.
- Failure if removed: Starting with many small records removes the hook and hierarchy.

### inv-02

- Rule: Unfold the claim into at least two itemized records with visible category separation.
- Purpose: Turns a large headline into checkable evidence.
- Failure if removed: A second big number without records feels like another unsupported claim.

### inv-03

- Rule: Compress the detailed records into one aggregate result before changing metric family.
- Purpose: Rewards the detail pass with a simplified summary state.
- Failure if removed: Jumping directly from records to the final value leaves the proof unresolved.

### inv-04

- Rule: Use one physically legible panel or carrier change to reveal an intermediate milestone from a different but related metric family.
- Purpose: Makes the information pivot feel causal rather than arbitrary.
- Failure if removed: A plain cut between unrelated metrics obscures their relationship.

### inv-05

- Rule: End on the current-state value and add only one restrained annotation after the value is readable.
- Purpose: Separates the conclusion from the evidence and gives it a memorable hold.
- Failure if removed: Many marks compete with the value; annotating before readability hides the conclusion.


## Variable Slots

| Slot | Constraint |
|---|---|
| headline_total | One original, truthful or explicitly fictional dominant total with a short label. |
| record_set | At least two distinct records whose categories visibly support the headline. |
| aggregate_result | One summary value derived from the record set. |
| milestone_metric | One related intermediate milestone shown through a physical carrier change. |
| current_state | One final current value, not a duplicate of the opening total. |
| material_system | An original medium whose folds, slides, hinges or layer changes explain information transitions. |
| annotation | One brief non-brand manual mark added only after the final value is readable. |
| sound_family | Original tactile cues tied to each information-state change. |

## Required Human-Facing Anchors

- Open with one dominant total and a compact label before showing its evidence.
- Unfold the claim into at least two itemized records with visible category separation.
- Compress the detailed records into one aggregate result before changing metric family.
- End on the current-state value and add only one restrained annotation after the value is readable.

## Anti-Copy Boundary

- 50+
- 期数教程
- 1.5W
- 17.7
- 3.8W
- 4.3W
- source café photographs and crossed red strips
- source black-white-red paper system and final red brush oval

## Transfer Tests

1. A navy-and-cream river-restoration board opens on '24 RESTORED SEGMENTS', unfolds into two transparent field-record cards, compresses to '127K L SAVED', pivots through a baseline efficiency panel and ends on 'CURRENT 92%' with one copper grease-pencil check.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: headline_total, record_set, aggregate_result, milestone_metric, current_state, material_system, annotation, sound_family
2. A translucent museum-conservation light table starts with '80 OBJECTS STABILIZED', fans out humidity and UV exposure records on acetate, stacks them into one reduced-risk index, flips a frosted milestone pane and ends on the current safe-storage rate sealed with one wax thumbprint.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: headline_total, record_set, aggregate_result, milestone_metric, current_state, material_system, annotation, sound_family

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

