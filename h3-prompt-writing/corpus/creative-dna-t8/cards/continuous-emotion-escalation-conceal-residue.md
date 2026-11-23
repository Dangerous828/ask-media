# continuous-emotion-escalation-conceal-residue

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: continuous-emotion-escalation-conceal-residue
description: "Create original short videos using the 情绪压力曲线｜压抑、峰值、遮挡与残余 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 情绪压力曲线｜压抑、峰值、遮挡与残余

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Lock one adult portrait, background, lens distance and light for the complete performance.
- Accumulate at least three readable tension indicators without resetting earlier evidence.
- Place one brief self-protective concealment gesture after the peak and then reveal the face again.
- Hold visible emotional residue such as wet eyes, altered breath or gaze in the terminal state.

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
# 情绪压力曲线｜压抑、峰值、遮挡与残余 — 摘要

## 用途

锁定同一人像、背景和镜头距离，以可累计的眼神、嘴部、呼吸与泪痕变化把中性状态连续推向一次情绪峰值；峰值后允许一个短暂遮挡动作，但必须重新露出面部，并保留可读的情绪残余，而不是瞬间恢复。

## 推荐输入格式

`固定成年单人近景、背景、光线与焦段 + 中性校准 + 至少3项不重置的压力信号 + 仅1次情绪峰值 + 峰值后短暂保护性遮挡 + 重新露面并保留情绪残余`

## 可直接改写的简短示例

> 原创成年救援调度员看向镜头旁状态屏，以专业中性状态建立基线；原创安全归队提示音后，她只出现一次释然哭泣峰值，泪液和呼吸自然；她放下手，看向状态屏，湿眼、泛红皮肤与下颌余张力仍存在

## 必须保留的结构锚点

- Lock one adult portrait, background, lens distance and light for the complete performance.
- Accumulate at least three readable tension indicators without resetting earlier evidence.
- Place one brief self-protective concealment gesture after the peak and then reveal the face again.
- Hold visible emotional residue such as wet eyes, altered breath or gaze in the terminal state.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 情绪压力曲线｜压抑、峰值、遮挡与残余 Template

## Mechanism

Lock one adult portrait, background, lens distance and light so that performance changes remain directly comparable. Begin from a controlled emotional baseline, accumulate at least three small facial or breathing indicators without resetting them, resolve once into a single maximum expression, then use one brief self-protective concealment gesture. Reveal the face again and end with visible physiological or behavioral residue rather than restored neutrality. The reusable mechanism is calibrated baseline, cumulative restraint, single peak, protective concealment and residual recovery—not the source woman, face, earrings, grey garment, field background, tear pattern, exact expression, camera, timing, creator identity or unsupported model mapping.

## Invariants

### inv-01

- Rule: Lock one adult portrait, background, lens distance and light for the complete performance.
- Purpose: Makes microchanges comparable against a stable baseline.
- Failure if removed: Camera or lighting changes can impersonate emotional progression.

### inv-02

- Rule: Accumulate at least three readable tension indicators without resetting earlier evidence.
- Purpose: Builds a continuous pressure curve rather than disconnected expressions.
- Failure if removed: Independent face poses become an expression test.

### inv-03

- Rule: Use exactly one maximum expression after the restrained build.
- Purpose: Provides a clear emotional apex.
- Failure if removed: Repeated peaks flatten the arc into cycling.

### inv-04

- Rule: Place one brief self-protective concealment gesture after the peak and then reveal the face again.
- Purpose: Adds behavioral consequence while preserving proof of recovery.
- Failure if removed: Ending fully hidden removes the final performance evidence.

### inv-05

- Rule: Hold visible emotional residue such as wet eyes, altered breath or gaze in the terminal state.
- Purpose: Makes recovery physically credible.
- Failure if removed: Instant neutrality erases the cost of the peak.


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

- Lock one adult portrait, background, lens distance and light for the complete performance.
- Accumulate at least three readable tension indicators without resetting earlier evidence.
- Place one brief self-protective concealment gesture after the peak and then reveal the face again.
- Hold visible emotional residue such as wet eyes, altered breath or gaze in the terminal state.

## Anti-Copy Boundary

- the source woman's facial identity, hair, hoop earrings, grey garment and exact tear pattern
- the source open field background, overcast light, wind behavior, lens and crop
- the source lip, eye, cheek, crying, garment-cover and gaze sequence or exact timing
- the source beauty rendering, skin texture, framing, performance identity and character likeness
- the source creator identity, Seedance 2.5 claim, platform overlay, watermark and branding

## Transfer Tests

1. An adult rescue dispatcher in a fixed fluorescent control-room portrait holds composure through jaw tension, rapid blinking and a trapped breath, breaks once after hearing a safe-return confirmation, covers her mouth with one hand, then lowers it and ends with wet eyes and steadier breathing.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. An adult stage actor in a locked dressing-room mirror portrait suppresses laughter through cheek tension, nostril movement and a trembling lip, releases one full laugh, briefly hides behind a costume collar, then returns with flushed cheeks and residual smile breaths.
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

