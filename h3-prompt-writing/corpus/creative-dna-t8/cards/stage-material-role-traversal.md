# stage-material-role-traversal

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-material-role-traversal
description: "Create original short videos using the 微缩闯关｜同一材质连续变形 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 微缩闯关｜同一材质连续变形

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 开场先证明主体与地形尺度
- 同一材质至少承担三种连续物理角色
- 每次解决动作必须引出下一个材质状态
- 外部尺度工具只在后段进入一次
- 结尾主体恢复自主稳定状态

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
# 微缩闯关｜同一材质连续变形 — 摘要

## 用途

让一个微型主体穿越同一巨型地形，地形依次变成路面、阻力、载体和弹性过渡，最后由一个外部尺度工具只进入一次完成跨越。

## 推荐输入格式

`微型主体 + 单一巨型地形 + 同一材质至少3种连续物理角色 + 一次晚段外部桥梁 + 恢复自主的稳定结尾`

## 可直接改写的简短示例

> 微型温室信使横穿一片巨型蜡质叶：叶面从路脊变成湿滑露水面、移动叶脉和弹性纤维；最后一支全尺寸玻璃滴管只进入一次成为桥，信使抵达种子标记旁稳定站立。

## 必须保留的结构锚点

- 开场先证明主体与地形尺度
- 同一材质至少承担三种连续物理角色
- 每次解决动作必须引出下一个材质状态
- 外部尺度工具只在后段进入一次
- 结尾主体恢复自主稳定状态

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 微缩闯关｜同一材质连续变形 Template

## Mechanism

Establish one tiny protagonist crossing a single oversized terrain, then make that same substrate change physical role in a causal ladder: reliable footing becomes resistance, resistance becomes an improvised carrier, and the carrier becomes an elastic transition. Only after the protagonist has attempted those states, introduce one full-scale tool exactly once as a final bridge. End with the protagonist back in a stable self-possessed pose so scale assistance resolves the route without erasing agency.

## Invariants

### inv-01

- Rule: Prove the protagonist-to-terrain scale relation in the opening before the first obstacle.
- Purpose: Turns scale into usable story geography rather than a delayed reveal.
- Failure if removed: Without early scale proof, later material deformation reads as arbitrary VFX.

### inv-02

- Rule: Make one continuous substrate perform at least three visibly different physical roles in causal order.
- Purpose: Lets the environment generate the action ladder without introducing unrelated threats.
- Failure if removed: If every beat uses a new prop, the sequence becomes a montage instead of one evolving material problem.

### inv-03

- Rule: Let each attempted solution expose the next material state rather than resetting the route.
- Purpose: Preserves causal momentum and makes escalation legible.
- Failure if removed: Independent gags remove the sense that the traveler is learning and adapting.

### inv-04

- Rule: Use one late external-scale tool exactly once as a bridge, not as the opening scale reveal.
- Purpose: Provides a stronger second scale proof and a decisive transition after self-propelled effort.
- Failure if removed: An early or repeated giant tool steals agency and collapses the material traversal into handling.

### inv-05

- Rule: End on a stable pose that visibly restores agency after the external bridge.
- Purpose: Prevents assistance from becoming defeat and gives the action chain a performance payoff.
- Failure if removed: Ending in midair or on the tool leaves the causal result unresolved.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original, stable subject or group with a readable role. |
| setting | A new setting with fixed spatial anchors and no source-specific surface. |
| escalation_variable | One causal variable that changes through visible stages. |
| performance_rule | A restrained acting rule that keeps the mechanism legible. |
| camera_grammar | An information order that proves each state without copying source shot boundaries. |
| payoff | A clean final physical or social consequence. |
| sound_family | An original hierarchy of diegetic cues supporting state changes. |

## Required Human-Facing Anchors

- 开场先证明主体与地形尺度
- 同一材质至少承担三种连续物理角色
- 每次解决动作必须引出下一个材质状态
- 外部尺度工具只在后段进入一次
- 结尾主体恢复自主稳定状态

## Anti-Copy Boundary

- tiny chibi man on giant pepperoni pizza
- stretchy melted cheese terrain
- full-size fork and hand
- warm kitchen and drinking glass

## Transfer Tests

1. A tiny greenhouse courier crosses one enormous waxy leaf: the surface shifts from firm ridge to slick dew sheet to elastic vein sling, then one full-size glass pipette enters once as a bridge before the courier lands beside a seed marker.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A miniature archive scout traverses one giant folded linen map: crisp fold, snagging loose thread and springing fabric pocket form the ladder; one brass compass leg enters once as the final bridge before a wax-seal pose.
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

