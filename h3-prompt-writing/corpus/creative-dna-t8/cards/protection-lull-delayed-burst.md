# protection-lull-delayed-burst

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: protection-lull-delayed-burst
description: "Create original short videos using the 保护暂停｜短暂暴露后的迟发反转 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 保护暂停｜短暂暴露后的迟发反转

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 防护先证明用途
- 移开后有可见等待
- 同一环境给出延迟回击

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
# 保护暂停｜短暂暴露后的迟发反转 — 摘要

## 用途

防护道具先有用，暂时移开后保留暴露空档，随后发生一次温和迟发反转。

## 推荐输入格式

`成年人物＋防护物＋短暂安全错觉＋迟发变化`

## 可直接改写的简短示例

> 专业烘焙演示台，一位明确成年的烘焙师、一只固定上方面粉料斗、一块在料斗与人物/蛋糕之间的浅斜透明接粉罩、侧边接粉盘和台上的蛋糕。

## 必须保留的结构锚点

- 防护先证明用途
- 移开后有可见等待
- 同一环境给出延迟回击

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 保护暂停｜短暂暴露后的迟发反转 Template

## Mechanism

A protective prop first reads as necessary, then a brief lull tempts an adult operator to move it aside; the camera holds a confident exposed interval before the same environment delivers one delayed benign material burst and an immediately readable reaction.

## Invariants

### inv-01

- Rule: Establish active shelter and a stable external material source in one shared geography.
- Purpose: Makes protection and later exposure physically intelligible.
- Failure if removed: Without visible initial protection, the late burst becomes generic slapstick.

### inv-02

- Rule: Show the protection being deliberately removed, then a short confidently exposed action before the burst.
- Purpose: Creates timing and anticipatory vulnerability.
- Failure if removed: If burst arrives at the exact instant of removal, there is no reversal beat.

### inv-03

- Rule: The late burst comes from the already established environment and leaves a persistent changed material state and visible reaction.
- Purpose: Closes the comic cause-effect chain.
- Failure if removed: An unrelated surprise or instantly dry reset breaks payoff continuity.


## Variable Slots

| Slot | Constraint |
|---|---|
| adult_operator | Unambiguously adult practitioner with a task. |
| shelter | One movable protective prop with visible open/closed or in/out state. |
| hazard_source | Visible, harmless material source established before lull. |
| confident_action | Brief task advance after removing shelter. |
| late_burst | Single delayed event from same source. |
| reaction | Visible, grounded change without injury. |
| material | Physical flour, paper, mist or another benign medium. |

## Required Human-Facing Anchors

- 防护先证明用途
- 移开后有可见等待
- 同一环境给出延迟回击

## Anti-Copy Boundary

- No student-coded uniform, youthful anime face, burgundy umbrella, maple street or exact rain splash pose.
- No sexualized youthful framing; all transfer performers are clearly adult.
- Do not add a fabricated weather forecast or claim intentional sabotage.

## Transfer Tests

1. At a bright professional pastry demonstration, an adult baker works under a transparent, shallow-sloped receiving hood hinged above the counter between the flour hopper and both baker and cake. The motor falls silent; she waits for loose flour on the hood to settle, then tilts the hood toward a built-in catch tray and swings it up sideways, checks that the cake is clear, and steps forward smiling to reveal it. A delayed latch in the same visible hopper releases one harmless flour cascade onto the now-open counter and her apron. She freezes, eyebrows raised, with the hood still raised and the new white flour accumulated below.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: adult_operator, shelter, hazard_source, confident_action, late_burst, reaction, material
2. At an adult puppetry rehearsal, a stage maker waits under a clear safety canopy while a confetti test rig runs. The rig becomes quiet, she swings the canopy aside and steps forward to inspect a puppet. A delayed last batch of paper strips drops from the visible overhead chute; she stops with an exaggerated surprised look while the strips pile around the puppet stand.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: adult_operator, shelter, hazard_source, confident_action, late_burst, reaction, material

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

