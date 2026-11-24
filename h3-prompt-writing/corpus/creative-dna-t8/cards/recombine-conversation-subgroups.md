# recombine-conversation-subgroups

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: recombine-conversation-subgroups
description: "Create original short videos using the 分组对话覆盖｜两边接力后全桌合流 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 分组对话覆盖｜两边接力后全桌合流

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- Establish the first subgroup and shared table anchors before any cross-table cut.
- Make speaking-turn ownership visibly readable within the first subgroup without assigning source meaning.
- Give the second subgroup one distinct response phase and one listening witness.
- Recombine all participants with the same spatial anchors in a held wide view.

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
# 分组对话覆盖｜两边接力后全桌合流 — 摘要

## 用途

先用第一组双人镜头建立共享社交空间，在组内交接可见发言轮次，再切到桌对面的第二组完成独立回应阶段，最后用更宽构图让所有人物和同一桌面锚点合流；来源对白含义未知，只迁移可见轮次与覆盖顺序。

## 推荐输入格式

`稳定群体空间 + 第一小组可见发言轮次 + 第二小组接力 + 1次非语言动作 + 全体同框收束`

## 可直接改写的简短示例

> 四名原创餐厅工作人员先以两人组建立空间关系，再切到另一两人组完成发言与非语言动作，最后回到四人同框；不规定原片对白含义。

## 必须保留的结构锚点

- Establish the first subgroup and shared table anchors before any cross-table cut.
- Make speaking-turn ownership visibly readable within the first subgroup without assigning source meaning.
- Give the second subgroup one distinct response phase and one listening witness.
- Recombine all participants with the same spatial anchors in a held wide view.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 分组对话覆盖｜两边接力后全桌合流 Template

## Mechanism

Establish one shared social geography by showing the first seated pair, hand visual speaking-turn ownership within that pair, cut across the table to a second pair for a distinct response phase, then return to a wider composition that recombines all participants and the same table anchors. Source dialogue meaning is unknown; only visible turn ownership and coverage order are reusable.

## Invariants

### inv-01

- Rule: Establish the first subgroup and shared table anchors before any cross-table cut.
- Purpose: Creates a stable social half-space.
- Failure if removed: Opening on singles hides group geography.

### inv-02

- Rule: Make speaking-turn ownership visibly readable within the first subgroup without assigning source meaning.
- Purpose: Defines the coverage relay.
- Failure if removed: Indistinct mouth and eye ownership makes the cut arbitrary.

### inv-03

- Rule: Cut to a second subgroup that faces back into the same shared space.
- Purpose: Expands the conversation while preserving geography.
- Failure if removed: A new unrelated location breaks the group.

### inv-04

- Rule: Give the second subgroup one distinct response phase and one listening witness.
- Purpose: Prevents equal-motion visual noise.
- Failure if removed: Both people performing at once hides ownership.

### inv-05

- Rule: Recombine all participants with the same spatial anchors in a held wide view.
- Purpose: Closes the coverage map.
- Failure if removed: Ending on a pair leaves the larger group unresolved.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair whose role is clear without source identity. |
| setting | A materially new setting with fixed spatial anchors and no source-specific location. |
| causal_carrier | One object, route, mark or device that visibly carries the causal chain. |
| state_change | Five ordered states with observable handoffs, not a decorative montage. |
| camera_grammar | A new proof-oriented information order that does not copy source shot boundaries. |
| payoff | A held final consequence that resolves or recontextualizes the setup. |
| sound_family | An original hierarchy of story-world cues supporting each visible change. |

## Required Human-Facing Anchors

- Establish the first subgroup and shared table anchors before any cross-table cut.
- Make speaking-turn ownership visibly readable within the first subgroup without assigning source meaning.
- Give the second subgroup one distinct response phase and one listening witness.
- Recombine all participants with the same spatial anchors in a held wide view.

## Anti-Copy Boundary

- source beach bar and four actors
- source clothing and cocktails
- source dialogue content
- the exact male-pair to female-pair coverage

## Transfer Tests

1. Four polar greenhouse engineers sit around one circular sample table: the first pair compare a cracked seed shell, the opposite pair inspect a moisture graph, one technician rotates a sample cup, and a final wide shows all four agreeing on one marked tray without dialogue.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family
2. Four stop-motion harbor puppets share a chart desk: two place route tiles, the opposite pair respond with tide markers, one lifts a buoy token, and the final wide recombines every puppet and the completed route.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family

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

