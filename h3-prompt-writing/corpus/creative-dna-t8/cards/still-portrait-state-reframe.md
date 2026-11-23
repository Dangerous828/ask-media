# still-portrait-state-reframe

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: still-portrait-state-reframe
description: "Create original short videos using the 静态人像转义｜微表情改写前段含义 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 静态人像转义｜微表情改写前段含义

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 主体与机位稳定
- 后段变化清楚但克制
- 变化重释前段静止

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
# 静态人像转义｜微表情改写前段含义 — 摘要

## 用途

让近静镜头留出观察时间，再用少量可见状态变化改变读法。

## 推荐输入格式

`成年主体＋稳定环境＋一个后段可见变化`

## 可直接改写的简短示例

> 原创成年跑者，一条雨后空旷终点跑道，灰色跑步夹克，右手攥着一张无品牌号码布；人物和场地保持固定。

## 必须保留的结构锚点

- 主体与机位稳定
- 后段变化清楚但克制
- 变化重释前段静止

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 静态人像转义｜微表情改写前段含义 Template

## Mechanism

Hold one stable subject and place almost motionless under a coherent slow camera approach; in the latter portion of the same view, a small coherent sequence of gaze, expression and visible-state changes becomes readable and reframes the preceding stillness. A transfer may deliberately simplify this to one clear cue. Source-specific bilateral tears and styling are excluded.

## Invariants

### inv-01

- Rule: Keep one subject and one spatial setting stable through a long near-still hold.
- Purpose: Lets the viewer notice a small late difference rather than track changing geography.
- Failure if removed: Rapid location or identity changes consume attention and erase the subtle payoff.

### inv-02

- Rule: Use one slow, legible camera approach or progressive reframing while the subject's motion stays smaller than the camera movement.
- Purpose: Builds attention without substituting montage spectacle for performance.
- Failure if removed: Abrupt cuts or fast camera motion make a micro-change hard to perceive.

### inv-03

- Rule: Reserve a small, coherent visible-state development for the later close view and hold long enough to read it; a transfer may simplify this to one cue.
- Purpose: The delayed cue changes how the earlier restraint is interpreted.
- Failure if removed: If the cue occurs early, is invisible, or is replaced by explanatory text, the delayed reinterpretation disappears.


## Variable Slots

| Slot | Constraint |
|---|---|
| subject | One original stable adult person or clearly designed nonhuman subject; preserve identity. |
| setting | One persistent original space, not the source's ornate room. |
| camera | One slow approach or tightening frame; no rapid montage. |
| late_state_change | One original small visible cue, not the source's exact smile-and-tear pairing. |
| palette_medium | Original visual medium and color design. |
| sound | Optional original restrained sound timed to the cue; not inferred source audio. |

## Required Human-Facing Anchors

- 主体与机位稳定
- 后段变化清楚但克制
- 变化重释前段静止

## Anti-Copy Boundary

- Do not copy the source person's face, hair ornaments, costume, luxury setting, pose, lighting palette or bilateral-tears-plus-smile combination.
- Do not import creator caption wording, brand/tool credits or the original framing trajectory frame by frame.
- Do not treat the source emotion or backstory as known.

## Transfer Tests

1. An adult marathon runner stands nearly still at an empty finish line; a slow approach ends with one hand unclenching to release a crumpled race bib.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: subject, setting, late_state_change, palette_medium, sound
2. A stop-motion maintenance robot holds position in a silent observatory; a slow approach ends when its single chest light changes from amber to green.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: subject, setting, late_state_change, palette_medium, sound

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

