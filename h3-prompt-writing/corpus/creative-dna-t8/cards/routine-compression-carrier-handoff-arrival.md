# routine-compression-carrier-handoff-arrival

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: routine-compression-carrier-handoff-arrival
description: "Create original short videos using the 流程压缩｜动作载体接力到目的地兑现 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 流程压缩｜动作载体接力到目的地兑现

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Introduce one stable subject, starting state and destination goal before the compression accelerates.
- Assign every beat one distinct routine duty and one visible carrier that survives into the following transition.
- Make progress spatially monotonic from origin through transit to the stated destination.
- End with the same subject at the destination completing one observable result action.

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
# 流程压缩｜动作载体接力到目的地兑现 — 摘要

## 用途

把较长的日常流程压成连续短动作，每次剪辑都由姿态、手中物或运动方向接力；身份和目标始终可追踪，最后必须抵达目的地并完成一个可验证的结果动作。

## 推荐输入格式

`稳定主体与目的地 + 单职责短动作 + 姿态/手中物/方向接力 + 累积准备状态 + 单向路线 + 终点结果动作`

## 可直接改写的简短示例

> 原创成年海岸研究员关闭琥珀色天气提示灯，坐起并查看墙上潮汐卡；同一张脸、短深色头发和床边锈红防风外套清楚可见；研究员把样本管、折叠地图和便携仪表放入同一标本箱，扣上两枚锁扣，用右手提起并从左向右出门；研究员扫描标本箱条码，进入后把箱子放在野外终端旁并打开调查地图，终端亮起绿色状态，同一人物坐定准备工作

## 必须保留的结构锚点

- Introduce one stable subject, starting state and destination goal before the compression accelerates.
- Assign every beat one distinct routine duty and one visible carrier that survives into the following transition.
- Make progress spatially monotonic from origin through transit to the stated destination.
- End with the same subject at the destination completing one observable result action.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 流程压缩｜动作载体接力到目的地兑现 Template

## Mechanism

Compress a long routine into short, causally ordered duties. Give each beat one visible action and one persistent carrier—body direction, hand path, prop, wardrobe state or destination cue—that enters the next cut. Preserve a stable subject identity and monotonic progress toward one goal; the ending must show both arrival and a concrete completion action. The reusable mechanism is carrier-bound routine compression, not the source person, luxury apartment, office, taxi or exact fifteen-action list.

## Invariants

### inv-01

- Rule: Introduce one stable subject, starting state and destination goal before the compression accelerates.
- Purpose: Gives every fast cut one shared purpose.
- Failure if removed: A montage of attractive actions without a declared goal becomes an unrelated lifestyle reel.

### inv-02

- Rule: Assign every beat one distinct routine duty and one visible carrier that survives into the following transition.
- Purpose: Makes speed readable through causal handoffs.
- Failure if removed: Hard cuts with no shared hand, prop, direction or state feel arbitrary.

### inv-03

- Rule: Keep identity and the accumulated preparation state traceable through all wardrobe, prop and location changes.
- Purpose: Prevents compression from looking like different people or reset attempts.
- Failure if removed: Face, wardrobe or prop drift breaks the journey.

### inv-04

- Rule: Make progress spatially monotonic from origin through transit to the stated destination.
- Purpose: Turns many locations into one route.
- Failure if removed: Unmotivated backtracking or repeated origin shots erase forward movement.

### inv-05

- Rule: End with the same subject at the destination completing one observable result action.
- Purpose: Converts arrival into payoff rather than mere scenery.
- Failure if removed: Stopping at an exterior or smile does not prove the routine succeeded.


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

- Introduce one stable subject, starting state and destination goal before the compression accelerates.
- Assign every beat one distinct routine duty and one visible carrier that survives into the following transition.
- Make progress spatially monotonic from origin through transit to the stated destination.
- End with the same subject at the destination completing one observable result action.

## Anti-Copy Boundary

- the source young woman, facial identity, hairstyle, white sleepwear and black office outfit
- the source luxury apartment, cosmetics, heels, watch, black handbag, tumbler and laptop
- the source yellow taxi, city storefronts, glass office tower and access-gate design
- the source exact fifteen-action GRWM list, ordering, match cuts, reflections and final desk smile
- the source creator prompt wording, reference image identity and any visible brands or signage

## Transfer Tests

1. An original night-shift paramedic moves from wake-up through uniform check, equipment loading, bicycle transit and hospital entry; hand placement and a red medical pouch carry each cut before a powered-on triage tablet proves readiness.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. An original coastal field researcher progresses from weather check through sample packing, boat transfer and cliff-station entry; a cobalt specimen case and left-to-right movement connect each location before the case is logged into a scanner.
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

