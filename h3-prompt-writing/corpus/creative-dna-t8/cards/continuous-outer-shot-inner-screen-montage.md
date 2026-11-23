# continuous-outer-shot-inner-screen-montage

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: continuous-outer-shot-inner-screen-montage
description: "Create original short videos using the 屏中蒙太奇｜外层连续内屏切换 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 屏中蒙太奇｜外层连续内屏切换

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Introduce one physical display carrier and clearly separate its inner image from the outer world.
- Keep the outer shot continuous with stable device, operator contact and environmental anchors.
- Accumulate at least three distinguishable inner states without losing the display boundary.
- End with the inner result, physical carrier and outer context readable together.

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
# 屏中蒙太奇｜外层连续内屏切换 — 摘要

## 用途

让一台带屏设备始终占据前景并保持外层镜头连续，只允许设备内屏在不同人物或状态间切换；外层背景、手部微调和真实视差持续证明同一现场，最后让内外两层的群体能量形成可读呼应。

## 推荐输入格式

`实体显示设备 + 连续外层镜头 + 至少三种内屏状态 + 外层独立视差/遮挡 + 内外两层终态同框`

## 可直接改写的简短示例

> 原创夜间雨林实验区内，植物学家打开石墨色折叠热成像监视器，屏幕与边框清晰，湿叶、琥珀工作灯和小型团队在后方虚化；薄雾与叶片只在外层移动，监视器内部依次切换蛾翼扫描和花朵开放，显示边界始终完整；最终内屏把蛙、蛾、花和孢子四项读数并列，实体设备、手套和同一虚化温室仍共同可见

## 必须保留的结构锚点

- Introduce one physical display carrier and clearly separate its inner image from the outer world.
- Keep the outer shot continuous with stable device, operator contact and environmental anchors.
- Accumulate at least three distinguishable inner states without losing the display boundary.
- End with the inner result, physical carrier and outer context readable together.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 屏中蒙太奇｜外层连续内屏切换 Template

## Mechanism

Establish one physical display carrier in a continuous outer shot, keep its bezel, operator contact and surrounding geography visibly stable, and confine every montage cut or state change to the inner screen. Use independent outer-layer parallax or occlusion to keep proving that the exterior take has not cut, then finish by bringing the inner result and the persistent outer context into one readable held relationship.

## Invariants

### inv-01

- Rule: Introduce one physical display carrier and clearly separate its inner image from the outer world.
- Purpose: Creates two auditable image layers.
- Failure if removed: An unbounded fullscreen insert removes the screen-within-screen mechanism.

### inv-02

- Rule: Keep the outer shot continuous with stable device, operator contact and environmental anchors.
- Purpose: Makes inner cuts legible as bounded events.
- Failure if removed: Outer cuts turn the sequence into an ordinary montage.

### inv-03

- Rule: Allow meaningful content changes only inside the display while the outer layer supplies independent parallax or occlusion.
- Purpose: Proves that the two layers have different temporal rules.
- Failure if removed: Matching both layers shot-for-shot destroys the contrast.

### inv-04

- Rule: Accumulate at least three distinguishable inner states without losing the display boundary.
- Purpose: Builds progression inside one carrier.
- Failure if removed: One inner clip does not establish a montage system.

### inv-05

- Rule: End with the inner result, physical carrier and outer context readable together.
- Purpose: Closes the nested evidence structure.
- Failure if removed: Ending on an isolated insert discards the continuous outer proof.


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

- Introduce one physical display carrier and clearly separate its inner image from the outer world.
- Keep the outer shot continuous with stable device, operator contact and environmental anchors.
- Accumulate at least three distinguishable inner states without losing the display boundary.
- End with the inner result, physical carrier and outer context readable together.

## Anti-Copy Boundary

- the source silver early-2000s MiniDV camcorder
- the source nighttime fashion crowd and old stone street
- the source party portraits, sunglasses and tan fur coat
- the source REC and timecode screen graphics
- the source exact inner portrait order and electroclash campaign styling

## Transfer Tests

1. In an original nocturnal rainforest lab, a field botanist holds a rugged folding thermal monitor in one continuous outer shot. Mist, leaves and her gloved hands drift around the sharp device while only its screen cuts among a frog, a moth, a flower opening and airborne spores; the final monitor view gathers all four readings while the same wet greenhouse remains blurred behind it.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In stop-motion felt craft, a clockmaker carries a brass diagnostic tablet through one continuous workshop aisle. Hanging gears and wool dust provide outer parallax while the tablet alone switches between four animated mechanism cross-sections; the final cross-section aligns with the unchanged physical clock behind the tablet.
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

