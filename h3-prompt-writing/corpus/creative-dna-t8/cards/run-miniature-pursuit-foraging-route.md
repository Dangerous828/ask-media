# run-miniature-pursuit-foraging-route

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: run-miniature-pursuit-foraging-route
description: "Create original short videos using the 微缩逃亡｜巨物追赶到资源补给 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 微缩逃亡｜巨物追赶到资源补给

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Calibrate miniature scale with one ordinary oversized moving force in the opening.
- Change the movement verb at every material handoff.
- Preserve one travel direction and subject identity across scale changes.
- End with an earned resource that the subject visibly secures or uses.

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
# 微缩逃亡｜巨物追赶到资源补给 — 摘要

## 用途

先用巨物校准微缩尺度，再让同一人物连续改变跑、弹、爬、平衡等动作，最终抵达可用资源。

## 推荐输入格式

`微缩主体 + 巨型移动压力 + 3种材质动作动词 + 连续路线 + 取得并使用资源`

## 可直接改写的简短示例

> 手掌高折纸勘测员逃离滚动清洁刷，依次用弹性量尺带起跳、木线轴攀爬、钢尺平衡，最终取得并点亮电池珠。

## 必须保留的结构锚点

- Calibrate miniature scale with one ordinary oversized moving force in the opening.
- Change the movement verb at every material handoff.
- Preserve one travel direction and subject identity across scale changes.
- End with an earned resource that the subject visibly secures or uses.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 微缩逃亡｜巨物追赶到资源补给 Template

## Mechanism

Make scale readable immediately by placing a miniature subject beside one ordinary oversized force, then convert pursuit into a route of three materially different terrain actions. Each surface must change the subject's movement verb—run, spring, climb, balance or reach—and the final resource must be earned by the route rather than presented as a decorative giant object.

## Invariants

### inv-01

- Rule: Calibrate miniature scale with one ordinary oversized moving force in the opening.
- Purpose: Makes size and threat readable without explanation.
- Failure if removed: A tiny subject alone has no reliable scale.

### inv-02

- Rule: Change the movement verb at every material handoff.
- Purpose: Makes terrain causally useful.
- Failure if removed: Continuous running through new backgrounds becomes a chase montage.

### inv-03

- Rule: Use at least three surfaces with visibly different physical responses.
- Purpose: Builds a reusable material route.
- Failure if removed: Repeated rigid platforms add no new problem-solving.

### inv-04

- Rule: Preserve one travel direction and subject identity across scale changes.
- Purpose: Keeps the route continuous.
- Failure if removed: Discontinuous geography turns actions into unrelated vignettes.

### inv-05

- Rule: End with an earned resource that the subject visibly secures or uses.
- Purpose: Gives the traversal a purpose beyond survival.
- Failure if removed: A decorative giant object is not a payoff.


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

- Calibrate miniature scale with one ordinary oversized moving force in the opening.
- Change the movement verb at every material handoff.
- Preserve one travel direction and subject identity across scale changes.
- End with an earned resource that the subject visibly secures or uses.

## Anti-Copy Boundary

- source tiny boy
- source giant human hand
- source strawberry and pink flower
- source backyard garden route and eating payoff

## Transfer Tests

1. A palm-high paper surveyor is chased by a rolling maintenance brush across a textile workshop, springs from elastic ribbon, climbs a thread spool, balances across a ruler and secures a glowing battery bead.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A miniature frost engineer flees a sweeping magnet inside a clock shop, bounces from a mainspring, climbs a knurled crown, crosses a watch hand and reaches one warm oil capsule.
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

