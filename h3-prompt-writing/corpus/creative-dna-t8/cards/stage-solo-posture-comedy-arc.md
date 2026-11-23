# stage-solo-posture-comedy-arc

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-solo-posture-comedy-arc
description: "Create original short videos using the 单人表演弧｜坐起前倾再释放 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 单人表演弧｜坐起前倾再释放

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Keep one locked seated-eye-level direct-address frame.
- Move from reclined to upright in one continuous visible shift.
- Insert a readable still pause after the peak.
- Return body depth toward the opening while changing expression.

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
# 单人表演弧｜坐起前倾再释放 — 摘要

## 用途

固定直视镜头里，单人用躺靠、坐起、前倾、手势和后仰释放完成完整表演弧，不依赖来源台词。

## 推荐输入格式

`锁定单人镜头 + 躺靠基线 + 连续坐起前倾 + 单一物证动作 + 停顿后带变化回位`

## 可直接改写的简短示例

> 锁定镜头下，年轻女性水网调度员从侧躺靠连续坐起，前倾说一句原创干冷台词，只举一次滴水传感器标签，停顿后带着笑意旋回。

## 必须保留的结构锚点

- Keep one locked seated-eye-level direct-address frame.
- Move from reclined to upright in one continuous visible shift.
- Insert a readable still pause after the peak.
- Return body depth toward the opening while changing expression.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 单人表演弧｜坐起前倾再释放 Template

## Mechanism

Use one locked direct-address frame and let a solo speaker's posture carry the arc: relaxed baseline, visible attention shift, forward engagement, compact gesture proof, then an earned release that returns the body toward the original depth. The reusable structure depends on posture, eye line and breath-sized pauses, not on source dialogue meaning.

## Invariants

### inv-01

- Rule: Keep one locked seated-eye-level direct-address frame.
- Purpose: Makes posture the measurable variable.
- Failure if removed: Coverage changes hide whether the performance arc works.

### inv-02

- Rule: Move from reclined to upright in one continuous visible shift.
- Purpose: Creates the decisive engagement transition.
- Failure if removed: Starting upright removes the primary contrast.

### inv-03

- Rule: Use no more than one dominant gesture at the forward peak.
- Purpose: Preserves focus and realism.
- Failure if removed: Constant gesturing flattens emphasis.

### inv-04

- Rule: Insert a readable still pause after the peak.
- Purpose: Lets viewers register the change.
- Failure if removed: Immediate release makes the peak feel accidental.

### inv-05

- Rule: Return body depth toward the opening while changing expression.
- Purpose: Creates closure without resetting emotion.
- Failure if removed: An unchanged final face makes the arc feel circular rather than resolved.


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

- Keep one locked seated-eye-level direct-address frame.
- Move from reclined to upright in one continuous visible shift.
- Insert a readable still pause after the peak.
- Return body depth toward the opening while changing expression.

## Anti-Copy Boundary

- source male speaker appearance
- source green couch and living room
- source life-joke prompt wording
- source exact gestures and laugh timing

## Transfer Tests

1. A young female night water-grid dispatcher reclines sideways in an industrial swivel chair, notices a blue message tube, sits forward to deliver one original river line, raises one dripping sensor tag, pauses and swivels back with an unexpected grin.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A stylized wooden puppet museum guide rests in a jointed miniature chair, notices one mechanical flag, pitches forward to deliver an original inventory line, raises one cracked wax seal, pauses and folds back with a newly painted surprised expression.
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

