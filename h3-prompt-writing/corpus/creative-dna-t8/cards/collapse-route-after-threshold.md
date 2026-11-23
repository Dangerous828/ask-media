# collapse-route-after-threshold

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: collapse-route-after-threshold
description: "Create original short videos using the 路线坍塌｜安全空间逐段消失 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 路线坍塌｜安全空间逐段消失

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 方向与终点固定
- 后方路线只减不增
- 当前段最多一次可恢复失稳
- 主体完全过阈值后才断开最后连接

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
# 路线坍塌｜安全空间逐段消失 — 摘要

## 用途

主体只朝固定终点前进，走过的路线单调消失，完全跨过阈值后最后连接才断开。

## 推荐输入格式

`载体 + 固定方向和终点 + 已走路线逐段消失 + 当前段一次失稳 + 完全过阈值后最后断开`

## 可直接改写的简短示例

> 透明温室管道中的采样车始终朝安全舱行驶，驶过的管段依次塌陷；当前管段只发生一次摇摆，车辆完全进入安全舱后最后接口才断开。

## 必须保留的结构锚点

- 方向与终点固定
- 后方路线只减不增
- 当前段最多一次可恢复失稳
- 主体完全过阈值后才断开最后连接

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 路线坍塌｜安全空间逐段消失 Template

## Mechanism

Lock one subject to a single screen-direction destination, then remove traversed route segments monotonically from behind while introducing one instability under the current segment. Alternate local control proof with wide remaining-route proof, and end with the subject fully crossing a safety threshold one beat before the final connection fails.

## Invariants

### inv-01

- Rule: Establish one visible destination and one travel direction.
- Purpose: Makes remaining distance measurable.
- Failure if removed: Changing destination destroys the countdown.

### inv-02

- Rule: Remove only already-traversed safe space from behind.
- Purpose: Prevents arbitrary danger and blocks retreat.
- Failure if removed: Random forward gaps can make survival impossible rather than tense.

### inv-03

- Rule: Add one recoverable instability under the current segment.
- Purpose: Tests control without replacing route logic.
- Failure if removed: Too many local hazards obscure the monotonic collapse.

### inv-04

- Rule: Alternate close control with wide remaining-route evidence.
- Purpose: Proves both agency and structural countdown.
- Failure if removed: Only close shots hide how much route remains.

### inv-05

- Rule: Cross the full threshold before the last connection fails.
- Purpose: Produces unambiguous escape proof.
- Failure if removed: Cutting away before full crossing leaves the outcome uncertain.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original subject or system whose identity remains stable. |
| setting | A new setting with fixed spatial anchors. |
| escalation_variable | One visible variable that changes in countable causal stages. |
| performance_rule | A restrained behavior rule that makes the mechanism legible. |
| camera_grammar | A coherent information order that does not copy source shot boundaries. |
| payoff | One clean physical or graphic consequence. |
| sound_family | A new hierarchy of diegetic cues supporting state changes. |

## Required Human-Facing Anchors

- 方向与终点固定
- 后方路线只减不增
- 当前段最多一次可恢复失稳
- 主体完全过阈值后才断开最后连接

## Anti-Copy Boundary

- dark SUV on a suspension bridge
- heavy rain and black water
- sliding abandoned cars and snapping cables
- the source bridge-deck collapse and far-shore anchorage

## Transfer Tests

1. A pollen courier capsule moves through a suspended greenhouse tube as sealed cells detach behind, one current cell tilts and the capsule reaches an airlock before the final collar releases.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A cave survey cart crosses modular crystal rails that dissolve behind it, stabilizes one rotating slab and reaches a stone dock before the last rail drops.
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

