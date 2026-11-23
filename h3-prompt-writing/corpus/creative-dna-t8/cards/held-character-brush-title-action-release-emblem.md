# held-character-brush-title-action-release-emblem

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: held-character-brush-title-action-release-emblem
description: "Create original short videos using the 停顿型角色预告｜凝视、书法字卡、一次动作释放与徽记收束 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 停顿型角色预告｜凝视、书法字卡、一次动作释放与徽记收束

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Hold one adult character portrait with three identity anchors until one micro-action becomes salient.
- Use one restrained material mark with no more than one short exact phrase.
- Release exactly one committed full-body action and settle immediately afterward.
- Convert the settled identity into a stable poster with one name and at most one identity line.

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
# 停顿型角色预告｜凝视、书法字卡、一次动作释放与徽记收束 — 摘要

## 用途

先用长于常规剪辑的角色凝视建立身份与情绪，再让一条墨迹和极少文字承担概念转场；回到远景继续等待，随后只释放一次清楚动作，把此前静止蓄积的能量兑现，最后以角色全身、原创名称和单一徽记组成稳定海报。

## 推荐输入格式

`明确成年原创角色以三项身份锚点和长停顿肖像建立 + 一次材料笔触只承载一个短词 + 回到环境远景时氛围移动但角色继续等待 + 只释放一次完整身体动作并立即收住 + 同一角色、一个原创名称和最多一行身份文字组成稳定徽记海报`

## 可直接改写的简短示例

> 成年轨道植物学家 MARA 的头盔近景保持，银色脸疤、青绿衣领、橙色种子盒固定，只睁开眼睛；同一成年人站在轨道温室远景，叶片和玻璃雨痕移动，人物不行动；奶油海报上，同一完整成年人位于圆形叶片徽记内，准确【MARA】和【ORBITAL KEEPER】出现

## 必须保留的结构锚点

- Hold one adult character portrait with three identity anchors until one micro-action becomes salient.
- Use one restrained material mark with no more than one short exact phrase.
- Release exactly one committed full-body action and settle immediately afterward.
- Convert the settled identity into a stable poster with one name and at most one identity line.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 停顿型角色预告｜凝视、书法字卡、一次动作释放与徽记收束 Template

## Mechanism

Establish one original clearly adult stylized character with at least three stable identity anchors in a held portrait that lasts long enough for one micro-action to matter. Replace the character once with a restrained brush or material mark carrying no more than one short exact phrase, then return to a wide environmental hold where weather or ambient motion continues but the adult waits. Release exactly one committed full-body action after the pause and let its path create a clean graphic bridge into a terminal emblem. End on a stable poster containing the unchanged full character, one original name and at most one short identity line. The reusable mechanism is held identity, micro-action, minimal brush-title anticipation, environmental waiting, single action release and emblematic poster closure—not the source woman, face, hair, robes, sword, words, title, ink circle, landscape, exact choreography, creator identity or timing.

## Invariants

### inv-01

- Rule: Hold one adult character portrait with three identity anchors until one micro-action becomes salient.
- Purpose: Builds attention through stillness rather than cut frequency.
- Failure if removed: Immediate motion removes the retention contrast.

### inv-02

- Rule: Use one restrained material mark with no more than one short exact phrase.
- Purpose: Turns typography into anticipation instead of exposition.
- Failure if removed: Dense copy breaks the pause rhythm.

### inv-03

- Rule: Return to a wide environment where ambient motion continues but the adult waits.
- Purpose: Transfers tension from face to world scale.
- Failure if removed: Constant character action spends the stored energy too early.

### inv-04

- Rule: Release exactly one committed full-body action and settle immediately afterward.
- Purpose: Concentrates payoff into one readable event.
- Failure if removed: Multiple attacks convert the mechanism into an action montage.

### inv-05

- Rule: Convert the settled identity into a stable poster with one name and at most one identity line.
- Purpose: Closes character and concept into a memorable emblem.
- Failure if removed: Another narrative beat after the poster weakens closure.


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

- Hold one adult character portrait with three identity anchors until one micro-action becomes salient.
- Use one restrained material mark with no more than one short exact phrase.
- Release exactly one committed full-body action and settle immediately afterward.
- Convert the settled identity into a stable poster with one name and at most one identity line.

## Anti-Copy Boundary

- the source anime adult woman, face, violet hair, robes and exact expressions
- the source sword, luminous slash, rain plain, rocks and storm environment
- the source FIRST LIGHT, THE TIDE TURNS, NO WITNESS, SUZURI and KEEPER OF THE QUIET HOUR wording
- the source brush mark, ink circle, poster layout, action choreography and exact edit timing
- the source creator identity, MiniMax H3 claim and anime identity

## Transfer Tests

1. An adult orbital botanist holds one breath inside a fogged helmet, a single condensation line writes 'WAKE', a silent greenhouse wide waits, one seed pod opens in a full-body gesture, and the same figure resolves into the original name poster 'MARA'.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. An adult jazz drummer remains still with one lifted stick, a brush of spilled silver forms 'HUSH', the empty club holds, one cymbal strike releases light, and the musician settles into an original 'NOVA' identity card.
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

