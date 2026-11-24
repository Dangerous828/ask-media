# stage-threshold-inspection-passage

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-threshold-inspection-passage
description: "Create original short videos using the 第一视角探险｜穿越后巡检 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 第一视角探险｜穿越后巡检

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 入口与阈值清楚
- 阈值后保持空间连续
- 只检查一个局部线索
- 结尾显示路线状态但不虚构诊断

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
# 第一视角探险｜穿越后巡检 — 摘要

## 用途

从入口跨过阈值后连续通行，局部检查异常，再给出可见但不武断的路线终态。

## 推荐输入格式

`远景入口 + 跨过阈值 + 连续通行 + 局部异常检查 + 可见路线终态（不下诊断）`

## 可直接改写的简短示例

> 植物学小队进入树根洞穴，跨过明暗阈值后沿狭窄通道前进；领队停下检查一条轻摆的空气丝带，未下结论，随后全队继续沿原路线深入。

## 必须保留的结构锚点

- 入口与阈值清楚
- 阈值后保持空间连续
- 只检查一个局部线索
- 结尾显示路线状态但不虚构诊断

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 第一视角探险｜穿越后巡检 Template

## Mechanism

A remote scale view identifies one consequential threshold, a single cut crosses it, and an extended continuous follow converts abstract environment into embodied passage. Moving light, partner or tool coordination and one local material cue interrupt forward motion; the sequence then ends on a clearly visible post-inspection route state without claiming the cue was diagnosed or resolved. Terrain, participants, material cue, route, camera carrier and final route state remain variable.

## Invariants

### inv-01

- Rule: Use the opening scale view to identify one precise threshold or route, not merely an attractive landscape.
- Purpose: Gives the following interior movement a destination and scale conversion.
- Failure if removed: Without a specific threshold, the exterior is disconnected B-roll and the interior cut feels arbitrary.

### inv-02

- Rule: Cross the threshold with one decisive edit or occlusion, then preserve spatial continuity long enough to feel embodied travel.
- Purpose: Turns environment from illustration into a route the audience can inhabit.
- Failure if removed: Repeated coverage cuts erase distance, orientation and physical effort.

### inv-03

- Rule: Bind participants, lights and tools into a clear coordination pattern whose spacing changes with the route.
- Purpose: Supplies readable human-scale motion inside a visually repetitive environment.
- Failure if removed: Independent wandering or identity drift makes the passage feel synthetic and removes practical stakes.

### inv-04

- Rule: Interrupt travel with one local material or environmental cue that can be indicated, measured or physically reacted to.
- Purpose: Creates a causal observation beat rather than endless forward walking.
- Failure if removed: Without a local cue the sequence has atmosphere but no event; an implausible cue destroys documentary credibility.

### inv-05

- Rule: After the inspection, end on one clearly visible route state—continue, pause or change direction—without claiming a diagnosis or hazard response unless directly shown.
- Purpose: Gives the passage a readable post-inspection endpoint while preserving uncertainty.
- Failure if removed: Ending before the route state is visible makes the inspection feel truncated; asserting an unshown diagnosis turns observation into fiction.


## Variable Slots

| Slot | Constraint |
|---|---|
| threshold_environment | A specific opening, hatch, canopy, chamber or access point with visible scale context. |
| field_team | One to three original humans, animals or machines with stable roles and silhouettes. |
| route_geometry | A continuous, physically traversable path with stable orientation anchors. |
| reveal_light | Headlamp, UV beam, lantern, reflected daylight or moving shadow that reveals material layers. |
| local_cue | One plausible airflow, vibration, moisture, sound, particulate or structural change. |
| inspection_action | A gesture or tool action that directs attention to the cue without relying on text. |
| post_inspection_route_state | A visible continuation, pause or direction change after inspection; causation or diagnosis is optional and must not be attributed to the source unless shown. |
| camera_carrier | Aerial, cable, body, rover or handheld path suited to the new environment. |

## Required Human-Facing Anchors

- 入口与阈值清楚
- 阈值后保持空间连续
- 只检查一个局部线索
- 结尾显示路线状态但不虚构诊断

## Anti-Copy Boundary

- glacier valley, blue ice cave, black oval aperture and translucent cyan tunnel
- two glaciologists, orange and blue-yellow suits, helmets, crampons, backpacks and ice axes
- the exact three-second aerial push followed by the same high front-left-to-rear follow route
- source prompt's under-ice water, seasonal melting, marking and retreat scenario

## Transfer Tests

1. A forest botanist and a compact quadruped rover enter an exposed-root sinkhole; a cable-cam threshold view gives way to one low interior follow, the rover's silk airflow ribbon snaps toward a side fissure, the botanist marks the observation, and both continue along the already established main root corridor.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: threshold_environment, field_team, route_geometry, reveal_light, local_cue, inspection_action, post_inspection_route_state, camera_carrier
2. A harbor engineer and a floating sensor puck enter a tidal service tunnel at low water; continuous waist-level following reveals a reversing foam line, the engineer tests it with dye-free cork chips, logs the observation with one physical marker, then continues along the same raised catwalk.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: threshold_environment, field_team, route_geometry, reveal_light, local_cue, inspection_action, post_inspection_route_state, camera_carrier

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

