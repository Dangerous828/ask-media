# structure-product-proof-launch

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: structure-product-proof-launch
description: "Create original short videos using the 产品广告｜功能证据递进 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 产品广告｜功能证据递进

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 先结果后证据
- 至少三个不同证明状态
- 证据必须可见且递进
- 结尾有明确行动或产品收束

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
# 产品广告｜功能证据递进 — 摘要

## 用途

先给结果，再用多个可见证据逐层证明产品功能，最后收束到行动。

## 推荐输入格式

`产品/服务 + 目标人群 + 3个不同证明状态 + 最终行动`

## 可直接改写的简短示例

> 一款便携净水器，面向户外徒步者：先展示喝到清水的结果，再依次用滤芯剖面、浑水变清和营地实用场景证明功能，最后出现简短购买行动。

## 必须保留的结构锚点

- 先结果后证据
- 至少三个不同证明状态
- 证据必须可见且递进
- 结尾有明确行动或产品收束

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 产品广告｜功能证据递进 Template

## Mechanism

A compressed launch film behaves as a flexible proof state machine rather than a fixed storyboard: an outcome, operation, internal mechanism, maximum contrast event, breadth proof and final action may be merged or reordered as long as each state answers a new product question. A strict material, light and typography system maintains coherence while shot count, information order, camera carrier and breadth device change across instances.

## Invariants

### inv-01

- Rule: Within the first third, establish one emotionally legible outcome and its causal relationship to the product; outcome-first and proof-first openings are both valid.
- Purpose: Gives technical information a human consequence without prescribing a brand-hero first frame.
- Failure if removed: If the product and outcome never connect, the sequence becomes either abstract mood or disconnected documentation.

### inv-02

- Rule: Make each information state answer a different product question, but merge related questions and vary their order according to the new product's strongest causal proof.
- Purpose: Turns speed into cumulative proof instead of a montage of interchangeable beauty shots.
- Failure if removed: If adjacent beats repeat the same claim, the fast pace becomes empty and the product remains vague.

### inv-03

- Rule: Concentrate one maximum contrast event after enough setup to make it legible; the peak may be physical, spatial, typographic or human, and its position is variable.
- Purpose: Creates a memorable second hook without requiring oversized text or a fixed midpoint boundary.
- Failure if removed: Equal intensity across all states produces a flat montage; repeating a source-style giant-text peak exposes the borrowed surface.

### inv-04

- Rule: Bind different modules with one strict contrast system, typography behavior and recurring assembly physics.
- Purpose: Maintains brand coherence while people, interfaces and use cases change rapidly.
- Failure if removed: Unrelated palettes, transitions or type treatments make the film feel like stock fragments.

### inv-05

- Rule: Prove breadth once before the final action using a device native to the new concept—continuous space, physical transformation, one montage, radial staging or audience behavior—not a mandatory card row or grid.
- Purpose: Converts a singular proof into broader relevance without locking the template to one information design.
- Failure if removed: No breadth proof makes the product feel niche; repeating cards then grid reproduces a specific campaign storyboard.

### inv-06

- Rule: Keep all visible copy short, complete and motion-safe: text lands at final size on a cut or via a hard mask and remains sharp long enough to read.
- Purpose: Protects comprehension in a dense 15-second information sequence.
- Failure if removed: Scaling, warping or partially formed words compete with the product proof and create spelling artifacts.


## Variable Slots

| Slot | Constraint |
|---|---|
| product_identity | One original fictional product name and a single-sentence emotional promise. |
| hero_benefit_image | An original person, object or environment showing the desired outcome rather than the interface. |
| capability_modules | Two or three visually distinct proofs that answer different product questions. |
| operation_proof | One legible control, process or physical mechanism that demonstrates how the product works. |
| peak_event | One maximum contrast event expressed through physical, spatial, typographic or human change. |
| breadth_device | One original non-redundant method for proving multiple contexts; avoid the source card-row plus grid pair. |
| graphic_system | A palette, material, light behavior and typography rule unrelated to the source campaign. |
| final_action | One concise CTA displayed in a stable closing lockup. |
| information_order | Choose an order derived from the new product's causal logic, not the source's nine-state sequence. |
| shot_structure | Use five to eight states with materially different boundaries, merges and camera implementations. |

## Required Human-Facing Anchors

- 先结果后证据
- 至少三个不同证明状态
- 证据必须可见且递进
- 结尾有明确行动或产品收束

## Anti-Copy Boundary

- MiniMax H3, HailuoAI, Create Beyond, LIVE RIGHT NOW, AVAILABLE NOW and every other source string
- source woman, violet jellyfish, nebula, purple speed streaks and identical product-category imagery
- source wordmarks, logos, translucent panel compositions, editing interface and creator-card layouts
- the exact nine-panel storyboard, exact beat durations, exact typography positions and source color palette

## Transfer Tests

1. A fictional compact air-quality device called AERIA ONE uses six reordered states: live room control proof, early sleeping-child outcome, combined sensor-filter macro, a physical apartment-scale clean-air peak with no giant text, one continuous environment morph for breadth, and a quiet final lockup.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05, inv-06
   - Changed: product_identity, hero_benefit_image, capability_modules, operation_proof, peak_event, breadth_device, graphic_system, final_action, information_order, shot_structure
2. A fictional adaptive running shoe called KINETIC ARC uses seven asymmetrical states: runner impact outcome, sole pressure trace, foam macro, terrain transition, the athlete clearing one stair as the physical peak, three matched footfalls across surfaces, and a ground-level final action.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05, inv-06
   - Changed: product_identity, hero_benefit_image, capability_modules, operation_proof, peak_event, breadth_device, graphic_system, final_action, information_order, shot_structure

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

