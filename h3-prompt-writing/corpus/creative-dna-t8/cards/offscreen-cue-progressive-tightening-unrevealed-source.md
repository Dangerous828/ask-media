# offscreen-cue-progressive-tightening-unrevealed-source

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: offscreen-cue-progressive-tightening-unrevealed-source
description: "Create original short videos using the 画外定位悬念｜反应递进但不揭示来源 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 画外定位悬念｜反应递进但不揭示来源

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish one reaction subject and one bounded offscreen region without showing a source.
- For each new instance, explicitly design a directional offscreen cue for a visible reorientation while the subject stays in the same bounded area; source cue timing remains inferred.
- Keep the cue source outside every frame and avoid explanatory inserts.
- End on a held reaction, residual instrument state or blackout without a source reveal.

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
# 画外定位悬念｜反应递进但不揭示来源 — 摘要

## 用途

在有界空间中只呈现反应者，让画外线索改变其注意方向；每次线索后都以更近的景别和更小的动作更新定位，始终不揭示来源，最后用停顿或黑场保留悬念。

## 推荐输入格式

`反应主体 + 有界画外区域 + 两到三个原创定向声线索 + 逐级收紧景别 + 微反应 + 不揭示来源的停顿或黑场`

## 可直接改写的简短示例

> 原创轨道温室夜间维护舱，一名技术员站在石墨色传感台前，上方灌溉管、深青玻璃、凝露叶片和侧面压力通风口建立有界空间；第二声原创压力滴答从侧面通风口回应，她先转动眼睛再轻轻侧耳，传感台边缘和一盏琥珀灯保持同一空间关系；轮廓与仍在轻颤的压力表停留一拍，温室实用灯依次熄灭并进入完整黑场，不反打、不揭示、不出现说明文字

## 必须保留的结构锚点

- Establish one reaction subject and one bounded offscreen region without showing a source.
- For each new instance, explicitly design a directional offscreen cue for a visible reorientation while the subject stays in the same bounded area; source cue timing remains inferred.
- Keep the cue source outside every frame and avoid explanatory inserts.
- End on a held reaction, residual instrument state or blackout without a source reveal.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 画外定位悬念｜反应递进但不揭示来源 Template

## Mechanism

Establish one bounded subject-space relationship with a clearly hidden offscreen region and progressively tighten from body-scale reorientation to micro-reaction without revealing a source. The creator states that sound supplies spatial information, while local ASR proves narration but not exact cue direction or synchronization; therefore each new transfer must explicitly design its own directional offscreen cues rather than treating source cue timing as observed fact. End on a held response, residual instrument state or blackout.

## Invariants

### inv-01

- Rule: Establish one reaction subject and one bounded offscreen region without showing a source.
- Purpose: Creates a stable localization problem.
- Failure if removed: An unbounded or already visible source removes the suspense mechanism.

### inv-02

- Rule: For each new instance, explicitly design a directional offscreen cue for a visible reorientation while the subject stays in the same bounded area; source cue timing remains inferred.
- Purpose: Connects newly authored unseen space to observable behavior without overclaiming source synchronization.
- Failure if removed: Large relocation or an unspecified cue breaks localization continuity.

### inv-03

- Rule: Tighten the camera after each visible reorientation and reduce motion from body turn to gaze or facial adjustment.
- Purpose: Converts spatial suspense into performance detail using directly visible source structure.
- Failure if removed: Constant shot scale prevents escalation.

### inv-04

- Rule: Keep the cue source outside every frame and avoid explanatory inserts.
- Purpose: Preserves the audience's active spatial inference.
- Failure if removed: Showing the source converts suspense into ordinary coverage.

### inv-05

- Rule: End on a held reaction, residual instrument state or blackout without a source reveal.
- Purpose: Leaves a precise unresolved afterimage.
- Failure if removed: A final reveal cancels the central withholding rule.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair with a readable role. |
| setting | A new setting with fixed spatial anchors and no source-specific surface. |
| escalation_variable | One causal variable that changes through visible stages. |
| performance_rule | A restrained acting or motion rule that keeps the mechanism legible. |
| camera_grammar | An information order that proves each state without copying source shot boundaries. |
| payoff | A clean final physical, informational or social consequence. |
| sound_family | An original hierarchy of diegetic cues; no unsupported source-audio claim. |

## Required Human-Facing Anchors

- Establish one reaction subject and one bounded offscreen region without showing a source.
- For each new instance, explicitly design a directional offscreen cue for a visible reorientation while the subject stays in the same bounded area; source cue timing remains inferred.
- Keep the cue source outside every frame and avoid explanatory inserts.
- End on a held reaction, residual instrument state or blackout without a source reveal.

## Anti-Copy Boundary

- the source woman, keys and dim residential corridor
- the source wall-dominant foreground and single wall lamp
- the source exact rear silhouette to tight face order
- the source implied monster, voice, whisper and knock wording
- the source black ending and exact corridor reaction staging

## Transfer Tests

1. In an original orbital greenhouse, one maintenance technician at a fixed sensor bench hears designed pressure ticks migrate through overhead irrigation pipes. She reorients from ceiling manifold to side vent while the camera tightens from medium to eye-and-ear profile; a fixed gauge needle twitches once, the source remains unseen and the chamber falls to black.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In tactile miniature museum conservation, one clockwork curator beside a glass display follows three designed chime directions through the floor grid. The camera progresses from full figure to painted eye close-up, a row of dust flags bends without showing a cause, and the scene ends on one vibrating brass label holder.
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

