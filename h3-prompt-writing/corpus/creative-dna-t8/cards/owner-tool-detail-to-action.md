# owner-tool-detail-to-action

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: owner-tool-detail-to-action
description: "Create original short videos using the 人物装备归属｜局部切片到全身动作 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 人物装备归属｜局部切片到全身动作

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 人物与工具先建立关系
- 细节保持同一设计
- 动作和全身姿态回证归属

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
# 人物装备归属｜局部切片到全身动作 — 摘要

## 用途

人物与工具先同框，再逐项核对细节，最后用一次动作证明归属。

## 推荐输入格式

`人物＋工具＋三个细节＋一次完整动作`

## 可直接改写的简短示例

> 一名明确成年的女性雪崩搜救训练员；石板灰和橙色工装、左肩无线电、右手手套、同一支无品牌探杆。训练坡面与标记区全程不换。

## 必须保留的结构锚点

- 人物与工具先建立关系
- 细节保持同一设计
- 动作和全身姿态回证归属

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 人物装备归属｜局部切片到全身动作 Template

## Mechanism

Introduce a stable person and their tool together, briefly isolate several owner-tool details, then connect those clues through one coherent body-tool action and a broad resulting stance. The source shows the face and tool early; the ending confirms action ownership rather than revealing a never-seen identity.

## Invariants

### inv-01

- Rule: Establish one stable tool owner before using close inserts.
- Purpose: Gives every later grip or equipment crop a clear subject anchor.
- Failure if removed: Without an established owner, close inserts could belong to several people and the action connection fails.

### inv-02

- Rule: Keep tool geometry and attachment to the same person consistent through detail views and the main action.
- Purpose: Makes the action legible as one carried object, not a sequence of swapped props.
- Failure if removed: If the tool or its hand changes between crops, the final action cannot be causally traced.

### inv-03

- Rule: After the action, show a broad enough pose to confirm where the tool ended relative to the owner.
- Purpose: Supplies a spatial outcome for the detail-and-action montage.
- Failure if removed: If the edit ends on another isolated detail, the viewer cannot verify the final tool-owner relation.


## Variable Slots

| Slot | Constraint |
|---|---|
| subject_role | One original stable tool owner; when human, visibly adult. Preserve body, costume and handedness across all views. |
| tool | One role-appropriate non-branded tool with stable shape and grip location. |
| environment | An original environment with persistent geography and a legible surface or target for the tool action. |
| main_action | One physically readable owner-tool action, not copied sword choreography. |
| camera_grammar | A broad owner-tool anchor, selective inserts, one action view, and a confirming pose; exact source cuts are not copied. |
| sound_family | Original action-linked ambience and contact sound, not a claim about unheard source audio. |
| medium | Visual medium may be live action, stop motion or another original form while owner-tool continuity remains legible. |

## Required Human-Facing Anchors

- 人物与工具先建立关系
- 细节保持同一设计
- 动作和全身姿态回证归属

## Anti-Copy Boundary

- No source anime face, hair, pale glowing coat, butterfly ornaments, blade pattern or exact color scheme.
- No source sword choreography, exact cut cadence, character identity, creator text or prompt wording.
- No franchise marks, source username, logo or weapon violence in the transferable preset.

## Transfer Tests

1. An adult avalanche-rescue trainee plants one search probe into a marked snow-training patch after boot, radio and tool details.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: subject_role, tool, environment, main_action, camera_grammar, sound_family, medium
2. A stop-motion clockwork repair puppet tightens one loose carousel wheel with a small wrench, then the carousel turns while puppet and wrench remain in a wide tabletop view.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: subject_role, tool, environment, main_action, camera_grammar, sound_family, medium

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

