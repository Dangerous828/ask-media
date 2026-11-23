# switch-roles-through-direction-stroke

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: switch-roles-through-direction-stroke
description: "Create original short videos using the 动作成字｜方向笔画驱动角色切换与终态标记 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 动作成字｜方向笔画驱动角色切换与终态标记

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Bind the first action to one dominant directional stroke.
- Use the first landing to change the stroke's composition role.
- Let the second action bend or reconfigure the stroke.
- Hold one final mark that visibly inherits both actions.

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
# 动作成字｜方向笔画驱动角色切换与终态标记 — 摘要

## 用途

第一位角色的动作生成强方向笔画，落地后笔画变成构图分隔；第二位角色沿同一图形轴进入并把笔画弯成新几何，最终标记由两次动作共同完成。

## 推荐输入格式

`第一动作生成方向笔画 + 落地变分隔 + 第二角色沿同轴进入 + 笔画变形 + 无文字终态标记`

## 可直接改写的简短示例

> 蓝色纸艺自动机把炭黑直尺变成构图分隔，琥珀自动机沿同轴进入并把直尺弯成螺旋，两次动作共同形成无文字涡轮标记。

## 必须保留的结构锚点

- Bind the first action to one dominant directional stroke.
- Use the first landing to change the stroke's composition role.
- Let the second action bend or reconfigure the stroke.
- Hold one final mark that visibly inherits both actions.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 动作成字｜方向笔画驱动角色切换与终态标记 Template

## Mechanism

Let one performer action generate or align with a strong directional stroke, use the landing to convert that stroke into a composition divider, switch to a second performer on the same graphic axis, let the second action bend the stroke into a new geometry, then hold the completed abstract mark as the consequence of both actions.

## Invariants

### inv-01

- Rule: Bind the first action to one dominant directional stroke.
- Purpose: Makes motion generate graphic structure.
- Failure if removed: A decorative line adds no causal role.

### inv-02

- Rule: Use the first landing to change the stroke's composition role.
- Purpose: Creates a visible handoff from action to layout.
- Failure if removed: A normal landing leaves no graphic consequence.

### inv-03

- Rule: Introduce a second performer on the established graphic axis.
- Purpose: Links role switch to the same system.
- Failure if removed: A new unrelated frame breaks continuity.

### inv-04

- Rule: Let the second action bend or reconfigure the stroke.
- Purpose: Adds a second causal authorship.
- Failure if removed: An unchanged divider makes the second role redundant.

### inv-05

- Rule: Hold one final mark that visibly inherits both actions.
- Purpose: Closes the graphic causality.
- Failure if removed: A random title card cannot prove the two-action construction.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair whose role is clear without source identity. |
| setting | A materially new setting with fixed spatial anchors and no source-specific location. |
| causal_carrier | One object, route, mark or device that visibly carries the causal chain. |
| state_change | Five ordered states with observable handoffs, not a decorative montage. |
| camera_grammar | A new proof-oriented information order that does not copy source shot boundaries. |
| payoff | A held final consequence that resolves or recontextualizes the setup. |
| sound_family | An original hierarchy of story-world cues supporting each visible change. |

## Required Human-Facing Anchors

- Bind the first action to one dominant directional stroke.
- Use the first landing to change the stroke's composition role.
- Let the second action bend or reconfigure the stroke.
- Hold one final mark that visibly inherits both actions.

## Anti-Copy Boundary

- source red-white-black characters and skateboard
- source graffiti rail, bar swing and number eight
- the exact two-performer graphic choreography
- source color blocking and final mark
- source large numeral 8
- source repeated 8 motif

## Transfer Tests

1. Two original paper-engineering automatons work on a cream drafting table: the first rolls a charcoal ruler into a divider, the second rotates it into a spiral aperture, and both actions resolve as a wordless turbine symbol.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family
2. Two luminous deep-sea maintenance drones traverse one cable axis; the first straightens it into a boundary, the second loops it into a rescue beacon, ending on the physical beacon rather than typography.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family

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

