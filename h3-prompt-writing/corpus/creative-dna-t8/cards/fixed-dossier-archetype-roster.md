# fixed-dossier-archetype-roster

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: fixed-dossier-archetype-roster
description: "Create original short videos using the 定版角色谱系｜同字段框架区分多种原型 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 定版角色谱系｜同字段框架区分多种原型

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Lock portrait zone, title position, field order and sequence counter across every entry.
- Present at least five distinct archetypes in a declared numbered sequence.
- Give every plate one readable title and one brief character micro-action while keeping the interface static.
- Finish on the final numbered dossier plate with all shared anchors intact.

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
# 定版角色谱系｜同字段框架区分多种原型 — 摘要

## 用途

锁定一套完全相同的档案版式、字段顺序和画面注册，让至少五个不同角色依次进入同一槽位；每个角色同时改变主色、轮廓、姿态和一个职责符号，并保留短暂微动作停留，使观众能快速比较一整套世界观原型而不丢失分类体系。

## 推荐输入格式

`固定人物区/标题/字段顺序/计数器 + 至少5个编号原型 + 每个原型同步改变主色/轮廓/姿态微动作/职责图标 + 界面全程不滑动 + 最终编号档案稳定停留`

## 可直接改写的简短示例

> 成年导航员穿修长钴蓝宇航服，用两指描出一条路线弧；左人物区、右上职责标题、三行指标、下方图标和计数固定；翠绿生物过滤维护员轻检叶片舱，随后白青系绳驾驶员收紧腕部卷盘；每张都保持相同裁切和字段位置；紫色碎片分析员穿棱角观测服，在放大镜下旋转一块透明碎片并稳定停留

## 必须保留的结构锚点

- Lock portrait zone, title position, field order and sequence counter across every entry.
- Present at least five distinct archetypes in a declared numbered sequence.
- Give every plate one readable title and one brief character micro-action while keeping the interface static.
- Finish on the final numbered dossier plate with all shared anchors intact.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 定版角色谱系｜同字段框架区分多种原型 Template

## Mechanism

Design one original dossier frame with a fixed portrait zone, fixed title position, fixed field order and stable sequence counter. Cycle at least five distinct archetypes through that exact registration. For each entry, change at least four coordinated channels: dominant accent color, silhouette or body geometry, posture or micro-action, and one role-specific symbol or data motif. Hold each plate long enough for the title and one visual distinction to register, then replace the subject without sliding the interface. End on the final numbered plate rather than a generic montage. The reusable mechanism is fixed taxonomy plus coordinated archetype contrast—not the source seven-sins theme, character faces, bodies, names, costumes, poses, exact palette, wording, logo, interface ornament, creator identity or timing.

## Invariants

### inv-01

- Rule: Lock portrait zone, title position, field order and sequence counter across every entry.
- Purpose: Creates a stable comparison carrier.
- Failure if removed: Moving fields force viewers to relearn the interface for each role.

### inv-02

- Rule: Present at least five distinct archetypes in a declared numbered sequence.
- Purpose: Builds a genuine roster rather than isolated character cards.
- Failure if removed: Too few entries or missing order cannot prove a taxonomy.

### inv-03

- Rule: Change accent color, silhouette, posture and one role symbol together for every archetype.
- Purpose: Makes each role legible through multiple independent channels.
- Failure if removed: Palette-only swaps feel cosmetic and silhouettes alone lack functional meaning.

### inv-04

- Rule: Give every plate one readable title and one brief character micro-action while keeping the interface static.
- Purpose: Combines classification clarity with living presence.
- Failure if removed: No hold prevents reading; full animation overwhelms the comparison frame.

### inv-05

- Rule: Finish on the final numbered dossier plate with all shared anchors intact.
- Purpose: Provides an explicit roster endpoint.
- Failure if removed: A generic collage or disappearing interface breaks the promised sequence.


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

- Lock portrait zone, title position, field order and sequence counter across every entry.
- Present at least five distinct archetypes in a declared numbered sequence.
- Give every plate one readable title and one brief character micro-action while keeping the interface static.
- Finish on the final numbered dossier plate with all shared anchors intact.

## Anti-Copy Boundary

- the source seven-deadly-sins concept, exact role names, character identities, faces, bodies and gender presentation
- the source armor, crowns, gloves, fitted suits, poses, expressions and role symbols
- the source gold, orange, magenta, green, amber, red and violet palette assignments
- the source SE7ENS logo, English copy, metrics, counters, interface ornament, font and graphic timing
- the source creator identity, MiniMax H3 claim, platform overlay, watermark and branding

## Transfer Tests

1. Six original orbital-repair specialists occupy one mission dossier: navigator, hull welder, biofilter keeper, tether pilot, radiation medic and debris analyst. Each changes accent color, suit silhouette, one restrained tool action and a role glyph while the portrait, title, metrics and 01/06 counter remain fixed.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. Five hand-cut paper weather spirits enter one museum label system: fog carrier, hail drummer, drought archivist, tide reader and aurora weaver. Material silhouette, pose, color paper and a weather icon change while the label grid never moves.
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

