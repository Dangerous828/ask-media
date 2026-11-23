# ensemble-dyad-position-realignment

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: ensemble-dyad-position-realignment
description: "Create original short videos using the 关系重排｜群体建立—双人收紧—前后站位 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 关系重排｜群体建立—双人收紧—前后站位

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish at least three readable public roles in one shared spatial axis before isolating a pair.
- Isolate one dyad while keeping enough background context to remember the larger group.
- Use one motivated crossing of the established axis to convert the exchange into a visible position change.
- End with both members readable in a new lead-follow or front-back relationship.

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
# 关系重排｜群体建立—双人收紧—前后站位 — 摘要

## 用途

先用公开群体画面建立人物关系，再把注意力收紧到其中两人；通过可见发言轮次、目光和微动作持续更新两人关系，最后让一人越过原轴线、另一人跟随，形成新的前后站位。

## 推荐输入格式

`公开群体三角色 + 双人隔离 + 逐级收紧的可见交流与微动作 + 单次越轴 + 新前后关系终态`

## 可直接改写的简短示例

> 原创毛毡潮汐钟工坊内，红围巾学徒、黄铜面罩评估员和蓝围裙守钟人站在同一条检查线上，后方修复完成的大型时钟门固定空间轴线；学徒检查刻度盘缺口并看向评估员，评估员放下测量臂并只做一次轻微点头，人物、围巾和工具身份稳定；学徒拿着闭合刻度盘走在前方，评估员落后一步跟随，远处守钟人仍留在校准台旁，时钟叶片只开始一次缓慢同步旋转

## 必须保留的结构锚点

- Establish at least three readable public roles in one shared spatial axis before isolating a pair.
- Isolate one dyad while keeping enough background context to remember the larger group.
- Use one motivated crossing of the established axis to convert the exchange into a visible position change.
- End with both members readable in a new lead-follow or front-back relationship.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 关系重排｜群体建立—双人收紧—前后站位 Template

## Mechanism

Establish a public ensemble and the initial spatial roles of at least three figures, then isolate one dyad while the larger group remains contextual evidence. Progressively tighten coverage through visible speaking turns, gaze and small physical responses without assigning unsupported dialogue meaning. Resolve the exchange through one motivated axis crossing, then reopen the frame on a new lead-follow or front-back relationship. The reusable mechanism is spatial relationship realignment, not a specific costume drama or conversation premise.

## Invariants

### inv-01

- Rule: Establish at least three readable public roles in one shared spatial axis before isolating a pair.
- Purpose: Provides a relationship baseline that can later change.
- Failure if removed: Beginning directly on two faces removes proof that the pair was extracted from a larger public arrangement.

### inv-02

- Rule: Isolate one dyad while keeping enough background context to remember the larger group.
- Purpose: Transfers attention without erasing the social frame.
- Failure if removed: A context-free close-up makes the exchange private and loses the public-position mechanism.

### inv-03

- Rule: Tighten from paired body-scale coverage to smaller gaze, mouth or head changes without inventing dialogue meaning.
- Purpose: Makes the relationship update inspectable through visible performance.
- Failure if removed: Constant shot scale or inferred semantics turns the middle into unsupported explanation.

### inv-04

- Rule: Use one motivated crossing of the established axis to convert the exchange into a visible position change.
- Purpose: Turns interpersonal change into spatial evidence.
- Failure if removed: A cut to an unrelated pose cannot prove how the relation was reorganized.

### inv-05

- Rule: End with both members readable in a new lead-follow or front-back relationship.
- Purpose: Closes the sequence on an inspectable new arrangement.
- Failure if removed: Ending on an isolated face leaves the spatial result unresolved.


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

- Establish at least three readable public roles in one shared spatial axis before isolating a pair.
- Isolate one dyad while keeping enough background context to remember the larger group.
- Use one motivated crossing of the established axis to convert the exchange into a visible position change.
- End with both members readable in a new lead-follow or front-back relationship.

## Anti-Copy Boundary

- the source cloud-top Chinese fantasy platform, monumental gate and distant floating architecture
- the source white-robed and green-robed women, older white-haired man, swords and public formation
- the source exact two-woman speaking and eye-contact order
- the source cheek mark, hair ornaments, robe palette and sword staging
- the source exact foreground walk-past and white-robed follower ending

## Transfer Tests

1. In original felt stop-motion at a tidal-clock workshop, three harbor artisans begin in one inspection line. A red-scarf apprentice and a brass-mask assessor separate beside a calibration table, exchange two silent inspection gestures as the view tightens, then the apprentice crosses the marked floor line and the assessor follows behind into the repaired clock passage.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In a clean robotics lab, three palm-sized service robots start at aligned charging bays. Two roll into a shared test lane, trade short light and arm responses under progressively closer views, then the smaller unit crosses the lane marker and the taller unit follows into a new front-back docking order.
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

