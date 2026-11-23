# capability-demo-crowd-witness-challenge

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: capability-demo-crowd-witness-challenge
description: "Create original short videos using the 能力见证｜装备特写—连贯表演—人群反应—挑战交接 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 能力见证｜装备特写—连贯表演—人群反应—挑战交接

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Present the enabling equipment in readable physical contact before revealing the full performer.
- Reveal one stable performer and enough public context to establish who will demonstrate and who can witness it.
- Include a spatially connected bystander response after the feat rather than a detached reaction insert.
- Introduce a second participant or counter-action only after the solo proof is complete.

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
# 能力见证｜装备特写—连贯表演—人群反应—挑战交接 — 摘要

## 用途

先用装备细节提出能力问题，再揭示表演者并连续完成一段可读动作；让围观者的惊讶、拍摄和让路成为公开证明，最后由第二位参与者进入，形成下一轮挑战。

## 推荐输入格式

`装备接触特写 + 稳定表演者 + 连续能力动作 + 同空间见证反应 + 第二参与者挑战交接`

## 可直接改写的简短示例

> 一名快递员把石墨色弹簧后跟支架扣在钴蓝鞋底上，只做一次最终锁扣检查；快递员连续完成两次短回弹、一次交叉转体、一次后向滑行并双脚稳定落在原通道；第二名快递员以琥珀色平板滑行装置从对向进入并停在远端标记，第一人转身面对他，人群留出清楚通道

## 必须保留的结构锚点

- Present the enabling equipment in readable physical contact before revealing the full performer.
- Reveal one stable performer and enough public context to establish who will demonstrate and who can witness it.
- Include a spatially connected bystander response after the feat rather than a detached reaction insert.
- Introduce a second participant or counter-action only after the solo proof is complete.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 能力见证｜装备特写—连贯表演—人群反应—挑战交接 Template

## Mechanism

Open on a legible piece of unusual equipment so the viewer asks what it enables, then reveal and lock one performer identity. Prove the capability through a continuous action phrase whose contact, direction changes and completion remain visible. Widen only after the feat so bystander reactions, recording behavior or cleared space act as social proof. End by introducing a second participant or counter-move that transfers the completed demonstration into a fresh challenge. The mechanism is capability-to-witness-to-challenge progression, not a specific skating style or plaza.

## Invariants

### inv-01

- Rule: Present the enabling equipment in readable physical contact before revealing the full performer.
- Purpose: Creates a precise capability question.
- Failure if removed: Starting on a generic portrait removes the mechanical hook.

### inv-02

- Rule: Reveal one stable performer and enough public context to establish who will demonstrate and who can witness it.
- Purpose: Binds identity, device and arena.
- Failure if removed: Changing performers or hiding the audience breaks accountability for the feat.

### inv-03

- Rule: Show one continuous action phrase with visible contact, direction change and completion.
- Purpose: Turns claimed capability into inspectable proof.
- Failure if removed: Montage-only fragments can conceal whether the action was completed.

### inv-04

- Rule: Include a spatially connected bystander response after the feat rather than a detached reaction insert.
- Purpose: Provides public social proof.
- Failure if removed: Unrelated reaction faces do not verify the demonstrated event.

### inv-05

- Rule: Introduce a second participant or counter-action only after the solo proof is complete.
- Purpose: Creates forward momentum without interrupting the evidence.
- Failure if removed: Early competition muddies whose capability was established.


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

- Present the enabling equipment in readable physical contact before revealing the full performer.
- Reveal one stable performer and enough public context to establish who will demonstrate and who can witness it.
- Include a spatially connected bystander response after the feat rather than a detached reaction insert.
- Introduce a second participant or counter-action only after the solo proof is complete.

## Anti-Copy Boundary

- the source young red-haired woman, black jacket, white shirt and exact facial identity
- the source black multi-wheel inline shoes, fastening details and exact cross-step choreography
- the source modern waterfront plaza, sunset crowd circle and spectators holding phones
- the source exact close-shoe to face reveal to crowd-reaction progression
- the source final second female skater entrance, wardrobe, staging and photographic surface

## Transfer Tests

1. In an original ceramic transit hall, a courier tightens spring-loaded heel frames, stands into view and traverses a marked floor through three continuous rebound turns; commuters step back and record the landing, then a second courier enters with a contrasting low glide for the challenge handoff.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In an original moonlit greenhouse, a maintenance dancer locks magnetic sole plates, rises into frame and crosses a suspended iron walkway with one continuous pivot-and-slide phrase; botanists visibly clear the path and lift inspection cameras, then another technician activates matching soles at the far end.
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

