# stage-performance-fall-rise-arc

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-performance-fall-rise-arc
description: "Create original short videos using the 舞台表演｜远景起势到倒地复起 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 舞台表演｜远景起势到倒地复起

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 开场先证明全身与巨大场地尺度
- 近景必须晚于动作语言建立
- 全片只有一次决定性下降
- 用俯拍或地面机位证明落地
- 结尾连续复起且不回到开场构图

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
# 舞台表演｜远景起势到倒地复起 — 摘要

## 用途

单人表演先用大远景建立身体与空间，再推进近景表达、完成一次受控倒地和俯拍停留，最后在独立光束中复起。

## 推荐输入格式

`单人表演者 + 巨大空场 + 远景起势 + 近景表达 + 一次受控倒地 + 俯拍确认 + 连续复起`

## 可直接改写的简短示例

> 打击乐舞者独自在废弃天文台起舞，从大远景轨迹进入近景手部节奏，完成一次膝盖先着地的螺旋倒地，俯拍停留后在开启的穹顶光束中连续起身。

## 必须保留的结构锚点

- 开场先证明全身与巨大场地尺度
- 近景必须晚于动作语言建立
- 全片只有一次决定性下降
- 用俯拍或地面机位证明落地
- 结尾连续复起且不回到开场构图

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 舞台表演｜远景起势到倒地复起 Template

## Mechanism

Build a solo performance through a scale-changing camera arc: establish the whole body in a large empty venue, advance to close expressive proof, let the body descend into one floor-level low point, then restore vertical energy in a final isolated light. The reusable template excludes any storyboard or prompt-demo overlay and depends on the visible fall-to-rise performance logic.

## Invariants

### inv-01

- Rule: Open with full-body scale inside a visibly larger venue.
- Purpose: Creates a measurable spatial baseline.
- Failure if removed: Opening close removes the scale contrast needed later.

### inv-02

- Rule: Move closer only after the body's initial movement language is established.
- Purpose: Makes close expression feel earned.
- Failure if removed: Immediate close coverage turns the piece into a generic portrait.

### inv-03

- Rule: Use one controlled descent as the single decisive low point.
- Purpose: Gives the performance an irreversible middle transition.
- Failure if removed: Repeated falls become choreography noise rather than structure.

### inv-04

- Rule: Hold the low point with a camera relation that proves floor contact and body geometry.
- Purpose: Prevents the descent from reading as a cutaway.
- Failure if removed: A hidden landing weakens physical causality.

### inv-05

- Rule: End upright in one isolated light, without recreating the opening framing.
- Purpose: Restores agency while showing change.
- Failure if removed: Returning to the exact opening makes the arc feel reset rather than resolved.


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

- 开场先证明全身与巨大场地尺度
- 近景必须晚于动作语言建立
- 全片只有一次决定性下降
- 用俯拍或地面机位证明落地
- 结尾连续复起且不回到开场构图

## Anti-Copy Boundary

- source performer appearance
- source industrial hall
- source storyboard sheet overlay
- the exact source shot order

## Transfer Tests

1. A percussionist-choreographer performs in a decommissioned observatory: distant circular steps, close hand rhythm, controlled floor spiral, overhead stillness and upright recovery under the open dome.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A paper-costume dancer performs in an empty greenhouse: aisle-wide start, leaf-shadow close work, soft collapse among cloth rows and rise into one shaft of dawn light.
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

