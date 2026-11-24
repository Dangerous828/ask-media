# foreground-witness-monument-handoff

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: foreground-witness-monument-handoff
description: "Create original short videos using the 见证者退场｜前景横穿到远端巨构 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 见证者退场｜前景横穿到远端巨构

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 远端目标先有锚点
- 前景移动有独立层次
- 最终远景清楚交接尺度

3. Change source-specific people, setting, props, palette, dialogue, shot boundaries, sound family, and payoff surfaces together.
4. Compile MiniMax H3 and Seedance 2.0 independently; do not leak one model's field syntax into the other.
5. Silently verify anchor coverage, continuity, timing, physical causality, and anti-copy distance before returning the final prompts.

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
# 见证者退场｜前景横穿到远端巨构 — 摘要

## 用途

以近处见证者建立尺度，镜头离开前景后让一次近景运动带出远方目的地。

## 推荐输入格式

`前景见证者＋远端目标＋近景横穿＋远景停留`

## 可直接改写的简短示例

> 清晨货港，一位成年线路工程师，安全栏杆，对岸同一座巨型悬索转运桥，近处三辆小型自动巡检车。

## 必须保留的结构锚点

- 远端目标先有锚点
- 前景移动有独立层次
- 最终远景清楚交接尺度

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 见证者退场｜前景横穿到远端巨构 Template

## Mechanism

A human-scale foreground witness establishes a remote monumental destination; a continuous camera drift leaves the witness, a distinct near-plane motion crosses the path, and a clear far-wide hold delivers the landscape.

## Invariants

### inv-01

- Rule: Establish a near observer against a stable distant destination.
- Purpose: Lets audience read the scale crossing.
- Failure if removed: Without near/far contrast, the move becomes an unmotivated landscape pan.

### inv-02

- Rule: Clear the initial foreground while keeping the destination anchored.
- Purpose: Transfers the viewpoint from watching to entering.
- Failure if removed: If the destination jumps or the observer stays dominant, the transition does not read.

### inv-03

- Rule: A separate nearer-plane motion crosses the view before the final uncluttered destination hold.
- Purpose: Guides eye and emphasizes layered depth.
- Failure if removed: Without near-plane movement, the final wide is only another static vista.


## Variable Slots

| Slot | Constraint |
|---|---|
| witness | One adult or clear scale marker in near plane. |
| destination | One fixed monumental place with stable horizon. |
| near_plane_guides | Several independently moving entities with readable direction and depth. |
| camera_path | Smooth move past witness toward established destination. |
| medium_palette | Original physical setting; no copied fantasy light-animal motif. |

## Required Human-Facing Anchors

- 远端目标先有锚点
- 前景移动有独立层次
- 最终远景清楚交接尺度

## Anti-Copy Boundary

- No moonlit castle, gothic silhouettes, deer, cloak, glowing wolves or source waterfall layout.
- Do not invent a physical connection between the moving near-plane figures and distant architecture.
- No original creator name, branding or exact panoramic composition.

## Transfer Tests

1. At an original near-future cargo port just before dawn, an adult route engineer stands by a railing facing a gigantic suspension transfer bridge across container cranes. The camera begins behind her, then glides beyond the rail as she exits frame. Several small autonomous inspection carts cross the near pier laterally, their white work lamps tracing separate paths. Hold the unchanged huge bridge and shipping channel after the carts clear; no fantasy beasts or magical activation.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: witness, destination, near_plane_guides, camera_path, medium_palette
2. At a sunlit salt-flat observatory, a solitary adult meteorologist frames a distant radio array from the lip of a low ridge. The camera glides past him. A line of wind-driven sensor kites crosses the close ground in a staggered wave, then clears to show the same array in an open wide view.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: witness, destination, near_plane_guides, camera_path, medium_palette

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

