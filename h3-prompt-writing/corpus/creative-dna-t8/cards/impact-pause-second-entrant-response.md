# impact-pause-second-entrant-response

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: impact-pause-second-entrant-response
description: "Create original short videos using the 冲击停顿｜第二角色入场与近景确认 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 冲击停顿｜第二角色入场与近景确认

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 冲击位置清楚
- 第二角色在停顿后入场
- 主角最终身份可辨

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
# 冲击停顿｜第二角色入场与近景确认 — 摘要

## 用途

局部冲击固定空间，短暂停顿后第二角色入场回应，最终以主角近景确认。

## 推荐输入格式

`固定空间＋一次冲击＋警觉停顿＋第二角色回应`

## 可直接改写的简短示例

> 洁净工业测试厅、红框校准区、一块轻质泡棉测试块、两台外形不同的自动巡检机器人。

## 必须保留的结构锚点

- 冲击位置清楚
- 第二角色在停顿后入场
- 主角最终身份可辨

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 冲击停顿｜第二角色入场与近景确认 Template

## Mechanism

A sudden localized impact pins the first agent in one geometry; a guarded pause and offscreen anticipation precede a second entrant's brief tightly bounded exchange, then a close stable view identifies the primary agent.

## Invariants

### inv-01

- Rule: An abrupt arrival or impact establishes one fixed pressure point in the scene.
- Purpose: Creates a concrete spatial problem.
- Failure if removed: Without the pressure point the later hold lacks cause.

### inv-02

- Rule: Hold the first agent visibly poised while a second agent is delayed offscreen.
- Purpose: Lets stillness store energy and direct gaze.
- Failure if removed: Immediate back-to-back impacts erase contrast and anticipation.

### inv-03

- Rule: The second arrival triggers one short readable exchange, then isolate the first agent in a final identity hold.
- Purpose: Converts tension into action and closes on a stable subject.
- Failure if removed: If the final frame is only chaotic motion, response and continuity are lost.


## Variable Slots

| Slot | Constraint |
|---|---|
| first_agent | One clearly stable adult or machine. |
| pressure_point | Visible safe localized impact and persistent mark or object. |
| second_agent | Enters only after readable quiet hold. |
| exchange | Short legible interaction without inferred injury. |
| final_identity | Close stable subject/marker after exchange. |
| setting | Original location, not copied station. |

## Required Human-Facing Anchors

- 冲击位置清楚
- 第二角色在停顿后入场
- 主角最终身份可辨

## Anti-Copy Boundary

- No subway platform, passing train, tiled cylinder, damaged wall pattern, original woman's likeness or exact fighting choreography.
- No unsupported injury, fatality or hidden motive claim.
- Targets use safe non-contact or machine interaction, not real interpersonal harm.

## Transfer Tests

1. In a clean industrial test hall, one autonomous inspection robot stops abruptly beside a red-marked pressure pad after a harmless foam calibration block drops from a ceiling rig directly into its forward sensor lane. The robot visibly detects the block and brakes before it. Its front sensor remains aimed at an empty entry lane during a long motor-idle hold. A second contrasting robot rolls in; the two execute a tightly spaced but non-colliding exchange of calibration arms at the same pad. End close on the first robot's sensor, both machines and dropped foam block still in their original positions.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: first_agent, pressure_point, second_agent, exchange, final_identity, setting
2. In a brightly lit competitive dance rehearsal, an unambiguously adult lead dancer lands on one marked stage square as a lightweight scenic curtain snaps down behind her. She holds a poised stance while another adult partner enters from offstage; they trade three precise non-contact gesture phrases. End on the lead dancer's controlled gaze, with the curtain and stage mark unchanged.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: first_agent, pressure_point, second_agent, exchange, final_identity, setting

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

