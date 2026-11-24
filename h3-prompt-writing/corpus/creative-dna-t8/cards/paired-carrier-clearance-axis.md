# paired-carrier-clearance-axis

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: paired-carrier-clearance-axis
description: "Create original short videos using the 双载具间距｜同轴移动与安全错位 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 双载具间距｜同轴移动与安全错位

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 共同运动轴明确
- 相对高度和间距可读
- 不发生穿模或碰撞

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
# 双载具间距｜同轴移动与安全错位 — 摘要

## 用途

两种载具保持同一行进轴线，以高度与距离变化形成无碰撞张力。

## 推荐输入格式

`两种载具＋共同方向＋间距变化＋安全收束`

## 可直接改写的简短示例

> 封闭测试山谷，只有一辆原创蓝色缆车和一艘小型琥珀色维护飞艇；两者都朝同一上站移动，山坡、索道和上站位置固定。

## 必须保留的结构锚点

- 共同运动轴明确
- 相对高度和间距可读
- 不发生穿模或碰撞

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 双载具间距｜同轴移动与安全错位 Template

## Mechanism

Two moving carriers share a clear travel axis while their relative vertical gap narrows and then widens. Spatially legible near-miss tension depends on co-direction, persistent geography, visible clearance and non-contact resolution, not a specific failure cause.

## Invariants

### inv-01

- Rule: Establish exactly two distinct moving carriers on one stable co-directional route.
- Purpose: Makes relative distance meaningful across views.
- Failure if removed: Opposing travel axes or duplicate vehicles make the near-miss geometry incoherent.

### inv-02

- Rule: Show the gap changing while both carriers and a stable environmental reference remain legible; preserve non-contact clearance.
- Purpose: Provides a visible spatial cause for tension.
- Failure if removed: A close-up with no shared scale or apparent collision cannot prove a near miss.

### inv-03

- Rule: End in a wide enough view to prove increased separation on the same route.
- Purpose: Closes the spatial question without an invented impact.
- Failure if removed: Ending during the tight gap leaves the outcome unresolved.


## Variable Slots

| Slot | Constraint |
|---|---|
| lower_carrier | One original lower moving unit with stable silhouette and route. |
| upper_carrier | One original higher moving unit with stable altitude relation; must never contact lower one. |
| environment | Stable route, direction and side landmarks. |
| gap_event | One readable narrowing with a clear minimum safe distance. |
| separation | Visible restoration of vertical gap and shared forward direction. |
| camera | Establish shared axis, prove closest gap, then hold wide separation. |
| sound | Original sound may follow relative motion, not attributed to unheard source audio. |

## Required Human-Facing Anchors

- 共同运动轴明确
- 相对高度和间距可读
- 不发生穿模或碰撞

## Anti-Copy Boundary

- No red numbered race car, black helicopter, mountain track or exact vehicle livery and camera positions.
- Do not copy the source snapshot's unverified power-loss explanation or treat the excerpt as a complete original prompt.
- No crash, real passenger peril or false precise distance claim.

## Transfer Tests

1. A mountain cable car and small maintenance airship move toward the same upper station; the airship dips then restores a visible safe air gap.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: lower_carrier, upper_carrier, environment, gap_event, separation, camera, sound
2. A miniature stop-motion freight trolley and motorized overhead bridge crane travel together down one factory aisle; the crane hook descends close to the trolley roof, stops, then rises while both continue away.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: lower_carrier, upper_carrier, environment, gap_event, separation, camera, sound

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

