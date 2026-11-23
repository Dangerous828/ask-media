# identity-locked-style-world-carousel

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: identity-locked-style-world-carousel
description: "Create original short videos using the 造型轮播｜身份锁定跨风格世界 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 造型轮播｜身份锁定跨风格世界

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish one stable portrait with face, body proportions, orientation and camera axis readable before the first switch.
- Use one repeatable transition gate while preserving the subject's facial identity and registration.
- Pass through at least three materially different worlds while retaining the same identity anchors.
- Return through the same gate to the opening world and portrait relationship.

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
# 造型轮播｜身份锁定跨风格世界 — 摘要

## 用途

锁定同一人物的脸部、正面姿态与高位光轴，利用受控过曝作为阶段门，让环境、服装和题材世界成套切换；每轮都保留身份锚点，完成多世界升级后沿同一门返回开场人像。

## 推荐输入格式

`固定主体身份与镜头关系 + 至少四个材质/版式不同的风格世界 + 每阶段改变两项风格通道 + 递增密度 + 可读身份终态`

## 可直接改写的简短示例

> 原创白色水下校准舱内，一只半透明水母导航员正面悬浮，钟罩月牙缺口和三条琥珀触须清楚，背景是中性网格；环境变成青色冰档案库，黑岩换成透明冰抽屉，并新增两片银色阅读鳍；三条琥珀触须和月牙缺口持续可追踪；移除所有世界专属配件，恢复白色校准舱、中性网格、月牙缺口和三条琥珀触须，保持开场正面人像关系

## 必须保留的结构锚点

- Establish one stable portrait with face, body proportions, orientation and camera axis readable before the first switch.
- Use one repeatable transition gate while preserving the subject's facial identity and registration.
- Pass through at least three materially different worlds while retaining the same identity anchors.
- Return through the same gate to the opening world and portrait relationship.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 造型轮播｜身份锁定跨风格世界 Template

## Mechanism

Lock one subject's face, core proportions, frontal orientation and camera axis in a stable portrait. Use one consistent transition gate to replace at least two coordinated style channels per stage—environment, wardrobe, material, props or light—while preserving the identity anchors. Escalate through visibly different worlds, then use the same gate to return to the exact opening world and portrait relationship.

## Invariants

### inv-01

- Rule: Establish one stable portrait with face, body proportions, orientation and camera axis readable before the first switch.
- Purpose: Creates the identity baseline.
- Failure if removed: An immediate montage gives no stable comparison state.

### inv-02

- Rule: Use one repeatable transition gate while preserving the subject's facial identity and registration.
- Purpose: Makes world changes comparable.
- Failure if removed: Unrelated cuts can hide identity drift.

### inv-03

- Rule: Change at least two coordinated style channels in each new world.
- Purpose: Proves full world replacement rather than recoloring.
- Failure if removed: A palette swap alone is not a world carousel.

### inv-04

- Rule: Pass through at least three materially different worlds while retaining the same identity anchors.
- Purpose: Stress-tests identity continuity.
- Failure if removed: Near-duplicate sets provide weak evidence.

### inv-05

- Rule: Return through the same gate to the opening world and portrait relationship.
- Purpose: Closes an exact identity loop.
- Failure if removed: A new final glamour portrait cannot verify the baseline.


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

- Establish one stable portrait with face, body proportions, orientation and camera axis readable before the first switch.
- Use one repeatable transition gate while preserving the subject's facial identity and registration.
- Pass through at least three materially different worlds while retaining the same identity anchors.
- Return through the same gate to the opening world and portrait relationship.

## Anti-Copy Boundary

- the source young woman in a black office suit
- the source cat-ear event styling, armored battlefield, underwater goggles, pastoral cloak and red carpet
- the source cool white office and paparazzi crowd
- the source white-blue overexposure transition
- the source exact world order, frontal fashion portrait staging and Hailuo/MiniMax marks

## Transfer Tests

1. An original translucent jellyfish navigator floats frontally inside a white calibration tank, identified by one crescent bell notch and three amber tendrils. A circular caustic flare carries it through a volcanic archive, a cyan ice library, a moss observatory and a black velvet signal chamber, changing environment and accessories while the notch, tendrils and scale stay fixed before returning to the white tank.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In tactile paper stop motion, one masked courier puppet is locked to a front-facing registration stand. A folding iris moves it through a red print shop, silver lunar depot, green rain shelter and blue acoustic theatre; paper costume layers and props change in pairs while one split mask and triangular badge persist, then the iris returns to the plain stand.
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

