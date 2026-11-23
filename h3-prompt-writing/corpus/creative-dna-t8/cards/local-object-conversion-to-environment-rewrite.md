# local-object-conversion-to-environment-rewrite

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: local-object-conversion-to-environment-rewrite
description: "Create original short videos using the 逐物改写｜局部对象到整片环境 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 逐物改写｜局部对象到整片环境

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish one continuous real environment and one visible selection tool.
- Align the tool with one object before each local conversion.
- Repeat the rule across at least three materially different object scales while keeping geography traceable.
- Apply the established rule once to a whole environmental region and hold the boundary.

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
# 逐物改写｜局部对象到整片环境 — 摘要

## 用途

保持同一第一视角和真实环境，使用一个持续可见的触发工具依次选中不同尺度对象；每次只改写一个局部对象并保留其位置关系，最后把相同转换规则扩大到整片环境。

## 推荐输入格式

`连续真实环境 + 可见选择工具 + 至少三次局部对象改写 + 原位空间配准 + 一次整片环境改写`

## 可直接改写的简短示例

> 原创精密洁净室内，戴手套技术员举起小型琥珀检查发射器，对准石墨色阀门，白色墙板、地面网格和传送设备保持真实；光束触及底盘后只有机器人变成分层示意图，轮位、路线和周围机器保持空间配准；光束指向顶棚网格，相同转换边界自上而下扩展，让顶棚、机器和地面成为统一青色洁净室剖面，发射器仍在前景

## 必须保留的结构锚点

- Establish one continuous real environment and one visible selection tool.
- Align the tool with one object before each local conversion.
- Repeat the rule across at least three materially different object scales while keeping geography traceable.
- Apply the established rule once to a whole environmental region and hold the boundary.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 逐物改写｜局部对象到整片环境 Template

## Mechanism

Keep one real environment and one visible selection tool continuous, align the tool with a sequence of distinct objects, and convert only the selected object into a new visual medium while preserving its spatial anchor and the rest of the world. Repeat across increasing scales, then reserve one final gesture that applies the already-proven conversion rule to a complete environmental region.

## Invariants

### inv-01

- Rule: Establish one continuous real environment and one visible selection tool.
- Purpose: Defines the baseline and causal agent.
- Failure if removed: An unexplained transformed opening has no conversion rule.

### inv-02

- Rule: Align the tool with one object before each local conversion.
- Purpose: Makes every change attributable and readable.
- Failure if removed: Objects changing before selection become random VFX.

### inv-03

- Rule: Convert only the selected object while preserving its location and surrounding reality.
- Purpose: Proves a bounded medium change.
- Failure if removed: Changing the whole frame on every beat removes local evidence.

### inv-04

- Rule: Repeat the rule across at least three materially different object scales while keeping geography traceable.
- Purpose: Builds transferable escalation.
- Failure if removed: Repeated copies of one object do not test the rule.

### inv-05

- Rule: Apply the established rule once to a whole environmental region and hold the boundary.
- Purpose: Creates a terminal scale payoff.
- Failure if removed: Another local conversion cannot close the escalation.


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

- Establish one continuous real environment and one visible selection tool.
- Align the tool with one object before each local conversion.
- Repeat the rule across at least three materially different object scales while keeping geography traceable.
- Apply the established rule once to a whole environmental region and hold the boundary.

## Anti-Copy Boundary

- the source black marker and bare hand
- the source Korean city, bus shelter, elevated train and green bus
- the source illustrated train, pigeon, orange cat and seated anime girl
- the source smiling sun and cloud sky
- the AIGC watermark and exact object order

## Transfer Tests

1. In an original cleanroom, a technician uses an amber inspection beam to select a valve, a conveyor robot and a pressure window. Each selected object alone becomes a transparent exploded blueprint at the same location; the final beam reaches the ceiling grid and converts the whole room into one held schematic cutaway.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In tactile stop-motion pottery, a small copper stamp touches a cup, a kiln cart and a wall vent; each becomes a layered paper cross-section while the clay studio stays intact. The last stamp touches the floor grid and the entire workshop becomes a folded instructional model.
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

