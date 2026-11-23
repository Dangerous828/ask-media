# material-scale-expansion-exact-return-loop

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: material-scale-expansion-exact-return-loop
description: "Create original short videos using the 尺度展开｜微小材质扩张后原样回收 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 尺度展开｜微小材质扩张后原样回收

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish one compact material anchor, surrounding surface and visible trigger before expansion.
- Let fragments of the anchor visibly generate the first larger structure.
- Hold one complete maximum-scale world before contraction begins.
- Reverse the same lineage and optical axis to restore the original anchor and trigger relationship.

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
# 尺度展开｜微小材质扩张后原样回收 — 摘要

## 用途

先锁定一个可辨认的微小材质锚点与触发动作，让同一材质逐级扩张为更大结构和完整世界，再沿可追踪的反向路径把所有尺度层收回，最终回到与开场一致的原始锚点。

## 推荐输入格式

`微小材质锚点 + 可见触发 + 至少两级尺度扩张 + 最大世界保持 + 沿同一谱系精确回收原点`

## 可直接改写的简短示例

> 原创黑橡木剧场地面上，一团紧实白色羊毛位于黄铜音叉下方，小击锤只敲一次，毛团、音叉脚和木纹位置清楚；同一纤维扩展成多层云带，再显出板岩色山脊与房间尺度雾气，一根细羊毛线仍连接天空与地面原点；山脊收成雾，雾收成白云，白云收成纤维并缠回原来同一毛团，音叉和木纹恢复开场关系

## 必须保留的结构锚点

- Establish one compact material anchor, surrounding surface and visible trigger before expansion.
- Let fragments of the anchor visibly generate the first larger structure.
- Hold one complete maximum-scale world before contraction begins.
- Reverse the same lineage and optical axis to restore the original anchor and trigger relationship.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 尺度展开｜微小材质扩张后原样回收 Template

## Mechanism

Lock one small, materially specific anchor and one visible trigger in a stable composition. Expand fragments of that same material through several readable scale levels until they form a complete world, while retaining at least one origin cue. Hold the maximum scale, then reverse the same material lineage and camera axis until the original anchor, trigger relationship and surrounding surface are restored for an exact visual loop.

## Invariants

### inv-01

- Rule: Establish one compact material anchor, surrounding surface and visible trigger before expansion.
- Purpose: Defines an exact state to recover.
- Failure if removed: A generic glow has no material history.

### inv-02

- Rule: Let fragments of the anchor visibly generate the first larger structure.
- Purpose: Binds scale change to one material family.
- Failure if removed: A hard cut to a new world breaks causality.

### inv-03

- Rule: Expand through at least two readable scale levels while retaining an origin cue.
- Purpose: Makes escalation measurable and reversible.
- Failure if removed: Immediate maximum scale feels like an unrelated reveal.

### inv-04

- Rule: Hold one complete maximum-scale world before contraction begins.
- Purpose: Creates a clear apex and reversal threshold.
- Failure if removed: Continuous blur hides whether expansion completed.

### inv-05

- Rule: Reverse the same lineage and optical axis to restore the original anchor and trigger relationship.
- Purpose: Closes an exact reusable loop.
- Failure if removed: Returning to a similar but different object is only a thematic echo.


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

- Establish one compact material anchor, surrounding surface and visible trigger before expansion.
- Let fragments of the anchor visibly generate the first larger structure.
- Hold one complete maximum-scale world before contraction begins.
- Reverse the same lineage and optical axis to restore the original anchor and trigger relationship.

## Anti-Copy Boundary

- the source mixed chili and seed spice pile
- the source adult fingers pinching the pile
- the source rustic wooden tabletop
- the source orange-blue galaxy and planet arrangement
- the source Yapper watermark and exact spice-cosmos-spice composition

## Transfer Tests

1. On an original dark theatre floor, one compact knot of white wool rests beneath a brass tuning fork. A single vibration loosens fibers into a cloud bank, expands into a room-scale weather front and mountain atmosphere, then reverses through cloud and fiber until the identical wool knot sits under the same fork.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In a ceramic acoustics lab, one tiny blue glaze bead under a resonance ring expands into concentric liquid maps, then an entire translucent ocean canyon; after a held abyss state, every layer contracts along the same rings into the identical bead on the original tile.
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

