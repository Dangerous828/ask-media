# observer-to-subject-camera-handoff

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: observer-to-subject-camera-handoff
description: "Create original short videos using the 镜头交接｜外部观察转为主体掌镜 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 镜头交接｜外部观察转为主体掌镜

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish one subject through an external trailing or observational camera.
- Use one site-specific exchange while the observer still owns the view; the exchange may be adjustment, response, installation, activation or material contact and must not require picking up or presenting an object.
- Use one motivated continuity bridge immediately before the switch, such as occlusion, equipment installation, mounting or carrier handoff.
- Switch exactly once to a subject-controlled capture and keep stable identity plus environmental context readable.

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
# 镜头交接｜外部观察转为主体掌镜 — 摘要

## 用途

先由外部观察镜头发现并跟随主体，让主体完成一次地点专属的环境交互，再给出环境尺度证明；随后使用遮挡、设备安装或载体交接等有动机的连续桥，片尾只把拍摄权交给主体一次。

## 推荐输入格式

`外部观察跟随 + 一次场景专属控制交换 + 一次环境广角证明 + 动机明确的遮挡或载体交接 + 片尾一次主体控制镜头`

## 可直接改写的简短示例

> 原创太阳能温室内，一台陶土巡检机器人穿过垂落藤蔓走向三组灌溉百叶，琥珀肩部标记始终稳定；机器人位于下方，三道对齐光带、太阳能玻璃、灌溉肋架和整片作物响应共同可读，身份与地点变化同时成立；机器人以同一琥珀肩标面对自己控制的可拆摄像机，后方三组已校准百叶和光带仍可见，蓝色状态灯闪一次后保持，不再回到顶轨镜头

## 必须保留的结构锚点

- Establish one subject through an external trailing or observational camera.
- Use one site-specific exchange while the observer still owns the view; the exchange may be adjustment, response, installation, activation or material contact and must not require picking up or presenting an object.
- Use one motivated continuity bridge immediately before the switch, such as occlusion, equipment installation, mounting or carrier handoff.
- Switch exactly once to a subject-controlled capture and keep stable identity plus environmental context readable.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 镜头交接｜外部观察转为主体掌镜 Template

## Mechanism

Begin with an external observer discovering and following one subject through a readable environment. Let the subject complete one site-specific exchange while the observer still owns the view, then provide one wider location proof. Use one motivated continuity bridge such as occlusion, equipment installation, mounting or carrier handoff before switching exactly once to a subject-controlled capture that still preserves subject identity and environmental context.

## Invariants

### inv-01

- Rule: Establish one subject through an external trailing or observational camera.
- Purpose: Defines initial camera ownership and spatial relationship.
- Failure if removed: Opening in selfie mode removes the handoff.

### inv-02

- Rule: Use one site-specific exchange while the observer still owns the view; the exchange may be adjustment, response, installation, activation or material contact and must not require picking up or presenting an object.
- Purpose: Connects subject and setting before camera ownership changes.
- Failure if removed: A generic pose or decontextualized gesture provides no environmental exchange.

### inv-03

- Rule: Provide one wider location proof with stable identity before the ownership switch.
- Purpose: Makes the final background and subject auditable.
- Failure if removed: Continuous face close-ups leave the setting unproven.

### inv-04

- Rule: Use one motivated continuity bridge immediately before the switch, such as occlusion, equipment installation, mounting or carrier handoff.
- Purpose: Makes the ownership change causal without prescribing source staging.
- Failure if removed: An unrelated cut to subject-controlled footage breaks continuity.

### inv-05

- Rule: Switch exactly once to a subject-controlled capture and keep stable identity plus environmental context readable.
- Purpose: Completes the change in camera ownership.
- Failure if removed: Returning to observer coverage or losing all location evidence weakens the terminal handoff.


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

- Establish one subject through an external trailing or observational camera.
- Use one site-specific exchange while the observer still owns the view; the exchange may be adjustment, response, installation, activation or material contact and must not require picking up or presenting an object.
- Use one motivated continuity bridge immediately before the switch, such as occlusion, equipment installation, mounting or carrier handoff.
- Switch exactly once to a subject-controlled capture and keep stable identity plus environmental context readable.

## Anti-Copy Boundary

- the source young woman with long dark hair and pale beach outfit
- the source tropical foliage, turquoise bay and white sand
- the source sandals and small shell-like found object
- the source exact crouch, seated portrait, shoreline walk and selfie order
- the source beauty-vlog facial presentation and beach composition

## Transfer Tests

1. In an original solar greenhouse, a ceiling-rail camera follows a compact clay inspection robot through hanging vines. The robot calibrates three irrigation louvers and the resulting light bands sweep across the crop bed; a wide observer view proves the full greenhouse response. Under an opaque maintenance gantry the robot docks with a detachable camera cradle, then emerges carrying that camera in a subject-controlled front-facing status view with the calibrated louvers behind it.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In paper-cut undersea research, a fixed reef drone observes a felt diver entering a kelp corridor. The diver taps an acoustic beacon and waits while three light rings propagate through the reef; a wide current map proves the environmental response. A bubble curtain then occludes the diver while she unclips the drone's tethered inspection camera, and the image returns once as her controlled inward-facing field note with beacon rings still visible behind her.
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

