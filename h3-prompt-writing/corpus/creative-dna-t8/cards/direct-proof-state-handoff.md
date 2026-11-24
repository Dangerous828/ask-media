# direct-proof-state-handoff

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-proof-state-handoff
description: "Create original short videos using the 风险揭晓｜证据交给人物反应 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 风险揭晓｜证据交给人物反应

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 先有干预冲突
- 风险通过可视证据证明
- 镜头交接有物理动机
- 反应简短且改变后续行为

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
# 风险揭晓｜证据交给人物反应 — 摘要

## 用途

一次干预阻止风险，可读证据随后由有动机的镜头交接给人物反应。

## 推荐输入格式

`紧急干预 + 隐藏风险 + 可视证据 + 有动机镜头交接 + 简短反应`

## 可直接改写的简短示例

> 实验员拦住同伴触碰容器，紫外光显出内部裂纹；镜头沿容器反光移交到同伴面部，他安静地收回手并点头。

## 必须保留的结构锚点

- 先有干预冲突
- 风险通过可视证据证明
- 镜头交接有物理动机
- 反应简短且改变后续行为

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 风险揭晓｜证据交给人物反应 Template

## Mechanism

An urgent intervention creates conflict, a controlled visual proof makes the hidden risk undeniable, and one motivated camera handoff transfers that proof to the recipient's compact reaction.

## Invariants

### inv-01

- Rule: Establish an urgent conflict through action before revealing the proof state.
- Purpose: Creates an immediate question and gives the later evidence a causal reason to appear.
- Failure if removed: Opening on the explanation removes tension and turns the scene into a flat demonstration.

### inv-02

- Rule: Hold the proof state visually stable long enough to be understood before the camera hands off.
- Purpose: Makes the evidence itself readable while keeping it integrated with performance.
- Failure if removed: Moving away before the hidden condition resolves makes the intervention feel arbitrary.

### inv-03

- Rule: Use one motivated reframe to hand the last line to a contrasting second speaker.
- Purpose: Converts instruction into a two-person joke without wasting time on coverage.
- Failure if removed: Keeping the camera on the first speaker removes the reaction payoff.


## Variable Slots

| Slot | Constraint |
|---|---|
| authority_role | A visually decisive expert with a clear reason to instruct. |
| recipient_role | A contrasting novice or peer who can answer in one short line. |
| proof_state | A physical condition, instrument reading, light reveal, or object state that becomes visually unambiguous without copying source typography. |
| setting | A context-rich location readable behind a medium close subject. |
| intervention | One brief action or line that stops the unsafe or mistaken behavior before the proof appears. |
| reaction | One gesture and one line that resolve the conflict. |
| camera_handoff | One pan or cut motivated by the second speaker. |
| sound | Location ambience plus non-overlapping dialogue; no music required. |

## Required Human-Facing Anchors

- 先有干预冲突
- 风险通过可视证据证明
- 镜头交接有物理动机
- 反应简短且改变后续行为

## Anti-Copy Boundary

- protected television characters or actor likenesses
- source-series wardrobe, vehicle, desert setup, or color grade
- source-character voices and exact dialogue
- exact guide title, profanity, framing, or prop typography

## Transfer Tests

1. A museum conservator stops an assistant's brush, lowers an ultraviolet inspection hood, and reveals branching fluorescent repairs before the camera follows the glow to the assistant's embarrassed recoil.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: authority_role, recipient_role, proof_state, setting, intervention, reaction
2. An observatory technician blocks a trainee from opening a dome, slides one red safety filter over the sensor, and reveals a dangerous solar flare before the camera follows the red reflection to the trainee's silent step back.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: authority_role, recipient_role, proof_state, setting, sound

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

