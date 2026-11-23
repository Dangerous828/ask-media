# verify-recurring-identity-board

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: verify-recurring-identity-board
description: "Create original short videos using the 角色卡验真｜四类证据锁定角色 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 角色卡验真｜四类证据锁定角色

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 角色卡布局保持一致
- 同一身份跨镜稳定
- 四类证据功能不同
- 结尾进入真实场景完成验证

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
# 角色卡验真｜四类证据锁定角色 — 摘要

## 用途

固定角色卡反复出现，用姿态、操作、步态和面部四类不同证据验证同一身份。

## 推荐输入格式

`角色 + 固定角色卡 + 4种不同证明（姿态/操作/步态/面部） + 实景英雄定格`

## 可直接改写的简短示例

> 陶瓷服务机器人与固定角色卡反复对照：证明站姿比例、端盘操作、走廊步态和面部灯光表情，最后在美术馆实景中英雄定格。

## 必须保留的结构锚点

- 角色卡布局保持一致
- 同一身份跨镜稳定
- 四类证据功能不同
- 结尾进入真实场景完成验证

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 角色卡验真｜四类证据锁定角色 Template

## Mechanism

Use one fixed identity board as a recurring visual checkpoint between four different live-scene proofs: silhouette and pose, small performance action, locomotion and face-level detail. Keep the board layout stable while camera scale and environment vary, then remove or subordinate the board so the verified live subject owns the final hero composition.

## Invariants

### inv-01

- Rule: Establish the identity board and live subject together before major action.
- Purpose: Creates an explicit comparison contract.
- Failure if removed: A hidden reference cannot function as visible evidence.

### inv-02

- Rule: Return to the same board layout between distinct live proofs.
- Purpose: Makes each action a new identity check.
- Failure if removed: A changing board destroys the reference baseline.

### inv-03

- Rule: Each live proof must test a different identity dimension.
- Purpose: Avoids redundant beauty shots.
- Failure if removed: Repeated face close-ups do not prove gait or silhouette.

### inv-04

- Rule: Keep defining proportions and markers continuous across board and scene.
- Purpose: Preserves subject identity through camera changes.
- Failure if removed: Marker drift breaks the verification mechanism.

### inv-05

- Rule: End on the verified live subject rather than a board-only frame.
- Purpose: Converts evidence into a satisfying hero payoff.
- Failure if removed: A board-only ending feels like documentation, not completion.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original subject or system whose identity remains stable. |
| setting | A new setting with fixed spatial anchors. |
| escalation_variable | One visible variable that changes in countable causal stages. |
| performance_rule | A restrained behavior rule that makes the mechanism legible. |
| camera_grammar | A coherent information order that does not copy source shot boundaries. |
| payoff | One clean physical or graphic consequence. |
| sound_family | A new hierarchy of diegetic cues supporting state changes. |

## Required Human-Facing Anchors

- 角色卡布局保持一致
- 同一身份跨镜稳定
- 四类证据功能不同
- 结尾进入真实场景完成验证

## Anti-Copy Boundary

- blonde anime cowgirl with black hat and sunglasses
- Route 66 sunset and vintage muscle car
- low-angle boots then sunglasses close-up
- the NOVA character sheet layout and source end card

## Transfer Tests

1. A ceramic service robot's orthographic maintenance card returns between a gallery entrance pose, delicate tray placement, stair locomotion and lens-aperture close-up before the robot owns the final exhibit frame.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A deep-sea diver suit diagram recurs between pressure-door entry, tool exchange, weighted walk and visor reflection, ending on the live diver at the observation window.
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

