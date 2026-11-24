# monument-scale-near-contact-return

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: monument-scale-near-contact-return
description: "Create original short videos using the 巨构近触｜尺度远景与微动作回望 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 巨构近触｜尺度远景与微动作回望

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 远景建立大小对比
- 微动作位置可追踪
- 回远景维持同一地理

3. Change source-specific people, setting, props, palette, dialogue, shot boundaries, sound family, and payoff surfaces together.
4. Compile MiniMax H3 and Seedance 2.0 independently; do not leak one model's field syntax into the other.
5. Silently verify anchor coverage, continuity, timing, physical causality, and anti-copy distance before returning the final prompts.

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
# 巨构近触｜尺度远景与微动作回望 — 摘要

## 用途

巨型场景先把旅行者缩小，再靠近一个可读微动作，最后回原远景。

## 推荐输入格式

`巨构＋旅行者＋近接微动作＋原位远景`

## 可直接改写的简短示例

> 一名成年文物修复师、一座巨大的青铜水钟大厅、从开头已亮的少量校准灯和一个待检查的固定齿轮盒。

## 必须保留的结构锚点

- 远景建立大小对比
- 微动作位置可追踪
- 回远景维持同一地理

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 巨构近触｜尺度远景与微动作回望 Template

## Mechanism

A monumental environment makes one traveler tiny; grounded movement inserts tighten to a near-contact micro-gesture, then a return to the unchanged wide site lets intimate attention alter the viewer's reading of scale.

## Invariants

### inv-01

- Rule: A monumental site and much smaller moving subject share one opening geography.
- Purpose: Sets a visible travel objective and scale contrast.
- Failure if removed: Without the original size contrast the late wide return has no recontextualization.

### inv-02

- Rule: Interrupt approach with physically grounded micro inserts before a held intimate gesture.
- Purpose: Converts distance into tactile attention.
- Failure if removed: Without the grounded detail, the close-up feels like an unrelated portrait.

### inv-03

- Rule: Return to the original large geography after the small gesture without claiming an unobserved environment switch.
- Purpose: Makes the held detail resonate at larger scale.
- Failure if removed: Without the return, the macro/micro relationship remains unclosed.


## Variable Slots

| Slot | Constraint |
|---|---|
| traveler | One stable human, animal or machine with grounded locomotion. |
| monumental_site | One pre-established large environment with persistent geography. |
| contact_detail | Small readable surface or mechanism the traveler can approach. |
| micro_gesture | Held minimal movement with a visible physical relation. |
| light_system | Already established practical or environmental lights; no required magic activation. |
| camera_scale | Wide-to-insert-to-close-to-wide ladder. |

## Required Human-Facing Anchors

- 远景建立大小对比
- 微动作位置可追踪
- 回远景维持同一地理

## Anti-Copy Boundary

- Do not use the source white deer, ancient glowing tree or forest-light pattern.
- No invented light ignition on contact: source tree is lit before approach.
- No source handle, watermark, exact bark-contact pose or copied animal portrait.

## Transfer Tests

1. An adult instrument conservator enters an immense dark water-clock hall where scattered bronze calibration lamps already glow. A wide view makes her small beneath the mechanism. Close shots show boot soles crossing grates and a gloved thumb inspecting one tiny engraved gear; she holds her breath and rests a fingertip on the stopped tooth. The camera returns wide to the same already glowing water clock, with the conservator tiny at its base; no magical activation is implied.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: traveler, monumental_site, contact_detail, micro_gesture, light_system, camera_scale
2. A small autonomous reef-inspection rover travels across the deck of a vast grounded oceanographic vessel at dawn. Begin with the entire hull and tiny machine, cut to tread contact and a sensor lens rotating toward a worn hull seam, hold the lens close without activating any new lights, then return to the same wide ship to make the inspected point feel consequential.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: traveler, monumental_site, contact_detail, micro_gesture, light_system, camera_scale

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

