# trigger-background-state-with-foreground-alignment

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: trigger-background-state-with-foreground-alignment
description: "Create original short videos using the 手势对齐｜前景动作触发后景状态 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 手势对齐｜前景动作触发后景状态

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish one stable subject-target geography and one readable baseline state before the effector enters.
- Use one unambiguous effector path that ends in a clean foreground-to-background alignment with the target.
- Change exactly one target state during or immediately after the alignment, without asserting literal contact that is not shown.
- End on the persistent changed state with one brief acknowledgment or recall gesture, not a second state change.

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
# 手势对齐｜前景动作触发后景状态 — 摘要

## 用途

固定分层构图先给出一个后景基准状态，前景动作沿清楚路径完成视线对齐，只触发一次状态变化，再通过保持、清开与回指确认结果持续。

## 推荐输入格式

`固定前后景 + 可读基准状态 + 单一前景动作路径 + 一次对齐触发 + 状态保持 + 清开后确认`

## 可直接改写的简短示例

> 黄铜天文馆木偶抬起细指示杆，与后景月盘清楚对齐；月盘只转一次，机械标签从 PARKED 翻成 TRACKING。木偶先保持共同证明，再放下指示杆，最后只点亮一个绿色确认灯。

## 必须保留的结构锚点

- Establish one stable subject-target geography and one readable baseline state before the effector enters.
- Use one unambiguous effector path that ends in a clean foreground-to-background alignment with the target.
- Change exactly one target state during or immediately after the alignment, without asserting literal contact that is not shown.
- End on the persistent changed state with one brief acknowledgment or recall gesture, not a second state change.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 手势对齐｜前景动作触发后景状态 Template

## Mechanism

In a fixed layered composition, establish one readable background state, move one foreground effector along a clean path until it visually aligns with the target, change exactly one target state during that alignment, hold the new state long enough to read, then clear the effector and finish by recalling or acknowledging the persistent result.

## Invariants

### inv-01

- Rule: Establish one stable subject-target geography and one readable baseline state before the effector enters.
- Purpose: Gives the viewer a before-state and a precise interaction destination.
- Failure if removed: If the target is already covered or changing, the later gesture has no measurable effect.

### inv-02

- Rule: Use one unambiguous effector path that ends in a clean foreground-to-background alignment with the target.
- Purpose: Turns depth mismatch into a legible apparent interaction.
- Failure if removed: A wandering gesture or several candidate targets makes causality unreadable.

### inv-03

- Rule: Change exactly one target state during or immediately after the alignment, without asserting literal contact that is not shown.
- Purpose: Provides a single causal payoff while preserving the visual nature of the trick.
- Failure if removed: Multiple changes feel like a generic interface demo; no change makes the gesture decorative.

### inv-04

- Rule: Hold the aligned effector and changed state together, then clear the effector while the result persists.
- Purpose: First binds action to result, then proves the result independently.
- Failure if removed: Cutting immediately after the change hides whether the new state is stable.

### inv-05

- Rule: End on the persistent changed state with one brief acknowledgment or recall gesture, not a second state change.
- Purpose: Closes the interaction and can create a changed-state loop endpoint.
- Failure if removed: Resetting to baseline erases the proof; adding another state dilutes the single-action mechanism.


## Variable Slots

| Slot | Constraint |
|---|---|
| foreground_subject | One original subject with a clearly readable effector and stable identity. |
| background_target | One original target whose baseline and changed states are visually distinct. |
| effector_path | One clean trajectory ending at a precise apparent alignment. |
| state_pair | One before state and one after state; no additional state family. |
| depth_grammar | A composition that keeps foreground effector, subject and rear target simultaneously legible. |
| confirmation_hold | Enough time to read both aligned action and changed result. |
| release_or_recall | Clear the target once, then optionally acknowledge the unchanged result. |
| sound_family | Original physical cues for approach, state change, hold and release. |

## Required Human-Facing Anchors

- Establish one stable subject-target geography and one readable baseline state before the effector enters.
- Use one unambiguous effector path that ends in a clean foreground-to-background alignment with the target.
- Change exactly one target state during or immediately after the alignment, without asserting literal contact that is not shown.
- End on the persistent changed state with one brief acknowledgment or recall gesture, not a second state change.

## Anti-Copy Boundary

- T8star-Aix
- +关注
- 已关注
- source profile counts and platform labels
- source face, hairstyle and brown shirt
- source pink-white profile interface and exact pointing placement

## Transfer Tests

1. A stop-motion brass planetarium docent stands before a deep mechanical star panel. Its slender pointer aligns with a moon dial as the panel flips from 'PARKED' to 'TRACKING'; the puppet lowers the pointer, then returns it beside the unchanged confirmation lamp.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: foreground_subject, background_target, effector_path, state_pair, depth_grammar, confirmation_hold, release_or_recall, sound_family
2. An underwater inspection drone hovers in front of a pressure-window iris. One manipulator aligns with a recessed latch, the iris changes from a narrow red slit to an open green ring, the drone backs away to reveal the stable aperture and finally sweeps one spotlight across it.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: foreground_subject, background_target, effector_path, state_pair, depth_grammar, confirmation_hold, release_or_recall, sound_family

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

