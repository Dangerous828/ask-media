# build-earned-arrival-journey

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: build-earned-arrival-journey
description: "Create original short videos using the 人物旅程｜从困境走向目标 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 人物旅程｜从困境走向目标

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 起点困境明确
- 目标空间提前可见或可理解
- 至少三个连续物理过渡
- 抵达后完成目标动作

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
# 人物旅程｜从困境走向目标 — 摘要

## 用途

让人物从可见困境出发，经过连续物理过渡，抵达目标并完成动作。

## 推荐输入格式

`人物困境 + 可见目标空间 + 3个物理过渡 + 抵达后的完成动作`

## 可直接改写的简短示例

> 疲惫的钟表匠被困在地下维修间，远处钟塔是目标；他穿过狭窄管道、升降平台和风雨屋顶，抵达后重新启动大钟。

## 必须保留的结构锚点

- 起点困境明确
- 目标空间提前可见或可理解
- 至少三个连续物理过渡
- 抵达后完成目标动作

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 人物旅程｜从困境走向目标 Template

## Mechanism

A recognizable person remains the emotional coordinate while an externally observed journey moves from constrained work pressure into an expanded goal space. Context is revealed through material interactions and camera parallax rather than direct exposition; scale and light increase toward the transition, and a final task-completing interaction—not a gesture to the lens—turns anticipation into earned arrival. Shot count, camera carrier and reveal order are variable.

## Invariants

### inv-01

- Rule: Keep one recognizable person emotionally legible across changing spaces, using face, posture or task behavior as the recurring anchor rather than requiring a selfie.
- Purpose: Preserves human stakes and orientation while allowing external, profile, wide or body-mounted camera implementations.
- Failure if removed: Without a recurring human coordinate, the route becomes anonymous location coverage; requiring a close selfie would make the template surface-specific.

### inv-02

- Rule: Make every contextual reveal originate from a physical interaction—moving a cart, opening geometry, passing an obstacle or handing off an object—and let the camera discover it through parallax, reframing or occlusion.
- Purpose: Makes camera change causal and informative without prescribing wrist turns or a return-to-face pattern.
- Failure if removed: Unmotivated coverage feels decorative; copying the same turn-and-recover move makes new instances mechanically identical.

### inv-03

- Rule: Create one legible transition from compressed effort to expanded possibility using at least two of scale, light, depth, sound or traffic flow; the transition may occur through a door, lift, ramp, curtain, bend or temporal match.
- Purpose: Gives the physical route a visible emotional direction.
- Failure if removed: If every space has equal brightness and scale, arrival has no visual payoff.

### inv-04

- Rule: Choose a capture grammar appropriate to each new world and keep its rules consistent; controlled documentary texture may come from parallax, shallow focus, operator lag or environmental occlusion, not a fixed bundle of DV defects.
- Purpose: Protects immediacy while allowing polished 35mm, shoulder documentary, fixed observational or body-mounted variants.
- Failure if removed: A copied artifact bundle reveals the source; random defects or identity drift destroy route comprehension.

### inv-05

- Rule: Resolve arrival through one task-completing physical interaction between the person and the goal environment, while their emotional state remains readable without addressing the lens.
- Purpose: Closes spatial and emotional questions through consequence rather than a copied reaction gesture.
- Failure if removed: A generic smile or hand sign does not prove arrival; a destination-only cut loses the human cost that made it meaningful.


## Variable Slots

| Slot | Constraint |
|---|---|
| traveler | One original adult subject with stable identity and a clear reason to move. |
| prep_space | A compressed, imperfectly lit working area with readable practical obstacles. |
| context_reveals | One to three physically motivated discoveries whose order and camera implementation change with the instance. |
| material_handoff | An object, obstacle or collaborator changes the route or objective; avoid mirror-based self-checks. |
| goal_threshold | A brighter, wider destination visibly different from the prep space. |
| capture_texture | Select an instance-specific external, fixed, body-mounted or handheld grammar; do not reuse a bundled source artifact signature. |
| resolution_action | A material action that proves the person has entered or completed the goal, with no direct-to-camera hand sign. |
| shot_structure | Choose three to six events with an order justified by the new task; do not map source beats one-to-one. |

## Required Human-Facing Anchors

- 起点困境明确
- 目标空间提前可见或可理解
- 至少三个连续物理过渡
- 抵达后完成目标动作

## Anti-Copy Boundary

- source face, ethnicity cues, hair, earrings and stage wardrobe
- concert backstage corridor, dressing mirror, curtain and exact stage-light composition
- exact dialogue, countdown, finger-heart gesture and performer premise
- creator-specific DV artifact bundle, wrist-turn/return pattern, mirror readiness check or shot timing copied beat for beat

## Transfer Tests

1. An original ceramic artist is filmed by an external stabilized 35mm camera while pushing a padded kiln cart through a cramped workshop. Shelves create parallax, assistants open a canvas loading bay, and the route expands into a dawn street market where she unwraps one still-warm bowl for the first waiting buyer.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: traveler, prep_space, context_reveals, material_handoff, goal_threshold, resolution_action, shot_structure
2. A telescope technician crosses a narrow daytime maintenance gantry in three long lateral shots, passing a suspended mirror segment and a safety-team handoff before the observatory dome opens to a star-filled night created by a time-match; she seats the final instrument and watches the first signal arrive.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: traveler, prep_space, context_reveals, material_handoff, goal_threshold, capture_texture, resolution_action, shot_structure

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

