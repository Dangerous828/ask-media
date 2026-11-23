# shared-ride-reaction-stop-recovery-exit

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: shared-ride-reaction-stop-recovery-exit
description: "Create original short videos using the 同乘反应曲线｜设施加速、共同峰值、骤停与离场 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 同乘反应曲线｜设施加速、共同峰值、骤停与离场

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Two stable original identities, adjacent seat positions and one shared carrier establish the baseline.
- Reaction intensity follows measurable carrier motion through grip, lean and facial evidence.
- A single complete stop precedes mutual checking and visible recovery.
- The terminal exit shows both companions leaving the same carrier together after releasing the restraint.

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
# 同乘反应曲线｜设施加速、共同峰值、骤停与离场 — 摘要

## 用途

把两名原创伙伴固定在同一游乐设施和相邻座位，用共同外部运动依次推动戒备、加速反应和情绪峰值；设施骤停后双方必须互相确认、恢复，再共同离开。

## 推荐输入格式

`两个稳定原创成年或非人伙伴身份与相邻座位 + 一个共同载具及可测量运动强度 + 反应随载具速度逐级增加并只有一个共同峰值 + 载具只完整停止一次 + 双方互相确认并恢复 + 共同解除约束并离开同一载具`

## 可直接改写的简短示例

> 让两名原创成年布偶音乐家并排坐在灯笼动力山坡车首排：高个青色鹤佩红围巾，矮个铜色狐狸戴圆眼镜。；最陡下降处保持双人同框，两者只出现一次共同张口反应峰值，灯笼尾迹证明载具速度。；两者松开安全杆、共同踏上平台，在准确原创标牌【HILL NOTE RIDE】下小幅鞠躬后一起离场。

## 必须保留的结构锚点

- Two stable original identities, adjacent seat positions and one shared carrier establish the baseline.
- Reaction intensity follows measurable carrier motion through grip, lean and facial evidence.
- A single complete stop precedes mutual checking and visible recovery.
- The terminal exit shows both companions leaving the same carrier together after releasing the restraint.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 同乘反应曲线｜设施加速、共同峰值、骤停与离场 Template

## Mechanism

把两名原创伙伴固定在同一游乐设施和相邻座位，用共同外部运动依次推动戒备、加速反应和情绪峰值；设施骤停后双方必须互相确认、恢复，再共同离开。 The reusable mechanism preserves causal order, spatial anchors and the final proof while replacing every source-specific person, location, object, wording, choreography and design.

## Invariants

### inv-01

- Rule: Two stable original identities, adjacent seat positions and one shared carrier establish the baseline.
- Purpose: Establishes the baseline identity, object or geography that every later state must preserve.
- Failure if removed: Without this exact baseline rule, later changes cannot be attributed to the same subject, object or place, so the sequence loses its reference state. Removed rule: "Two stable original identities, adjacent seat positions and one shared carrier establish the baseline."

### inv-02

- Rule: Reaction intensity follows measurable carrier motion through grip, lean and facial evidence.
- Purpose: Makes the visible trigger precede and explain the first mechanism response.
- Failure if removed: Without this exact trigger rule, the response appears spontaneously and the central cause-and-effect claim is no longer demonstrated. Removed rule: "Reaction intensity follows measurable carrier motion through grip, lean and facial evidence."

### inv-03

- Rule: Both companions reach one shared peak without swapping seats or losing identity.
- Purpose: Keeps the middle progression registered instead of allowing an unexplained reset.
- Failure if removed: Without this exact progression rule, the middle can jump to a replacement state and the accumulated result is no longer traceable. Removed rule: "Both companions reach one shared peak without swapping seats or losing identity."

### inv-04

- Rule: A single complete stop precedes mutual checking and visible recovery.
- Purpose: Reconnects the changed or partial state to the established subject and spatial anchor.
- Failure if removed: Without this exact reconnection rule, detail or transformed shots can belong to a different subject or geography and continuity cannot be verified. Removed rule: "A single complete stop precedes mutual checking and visible recovery."

### inv-05

- Rule: The terminal exit shows both companions leaving the same carrier together after releasing the restraint.
- Purpose: Turns the terminal hold into observable proof that the mechanism completed.
- Failure if removed: Without this exact terminal-proof rule, the sequence stops on motion alone and never confirms the promised outcome or preserved aftermath. Removed rule: "The terminal exit shows both companions leaving the same carrier together after releasing the restraint."


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

- Two stable original identities, adjacent seat positions and one shared carrier establish the baseline.
- Reaction intensity follows measurable carrier motion through grip, lean and facial evidence.
- A single complete stop precedes mutual checking and visible recovery.
- The terminal exit shows both companions leaving the same carrier together after releasing the restraint.

## Anti-Copy Boundary

- all source faces, bodies, wardrobe, identities and creator-specific character designs
- the source location, set dressing, props, products and exact environmental geometry
- all source words, logos, watermarks, typefaces and brand identifiers
- the source choreography, exact camera path, shot durations and transition timing
- the source palette, signature effects, prompt wording, creator handle and narrative particulars

## Transfer Tests

1. Two adult puppet musicians share a hill coaster, recover after one stop and bow before leaving together.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. Two adult robot botanists share a wind tunnel capsule, recover after shutdown and walk into the lab together.
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

