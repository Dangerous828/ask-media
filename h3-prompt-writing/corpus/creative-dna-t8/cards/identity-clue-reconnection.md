# identity-clue-reconnection

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: identity-clue-reconnection
description: "Create original short videos using the 身份线索回连｜局部累积到主体确认 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 身份线索回连｜局部累积到主体确认

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 同一主体
- 局部线索相互一致
- 结尾回连已见标记

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
# 身份线索回连｜局部累积到主体确认 — 摘要

## 用途

先用一致的局部线索建立身份，再回到已见过的面部标记完成确认。

## 推荐输入格式

`主体＋三项可复认的局部线索＋最终回连`

## 可直接改写的简短示例

> 原创成年海上灯塔维修员；深蓝工作服、普通透明护目镜、沾盐手套、腕部罗盘、肩部安全绳全程固定。晨光下同一座海上灯塔和同一盏信标。

## 必须保留的结构锚点

- 同一主体
- 局部线索相互一致
- 结尾回连已见标记

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 身份线索回连｜局部累积到主体确认 Template

## Mechanism

Build one stable identity through partial but mutually consistent visual clues; after they accumulate, return to a recognizable head/face marker already glimpsed earlier. The source never supplies a final full-body proof, and the face is not fully concealed at the start. An original transfer may strengthen the closing proof without claiming the source did so.

## Invariants

### inv-01

- Rule: Recurring visual design markers across different close crops must remain attributable to one stable character.
- Purpose: A later identity echo can only resolve the clue sequence if the earlier clues have one common owner.
- Failure if removed: If details come from different unmarked subjects, the ending cannot support an identity connection and becomes an arbitrary montage.

### inv-02

- Rule: The sequence must alternate several body regions while repeating at least one design marker; not every crop has to introduce new information.
- Purpose: The middle sustains familiarity and variation before the final identity echo.
- Failure if removed: If the montage stays on only one undifferentiated crop, the later eye/head echo no longer gathers dispersed details into one recognizable design.

### inv-03

- Rule: The ending returns to a previously glimpsed identity marker and preserves recurring design cues, without requiring a source full-body view.
- Purpose: Provides a recognizable identity echo after the detail ladder rather than an unrelated final insert.
- Failure if removed: If the ending drops the earlier identity marker and recurring cues, the fragment sequence no longer resolves to a recognizable stable character.


## Variable Slots

| Slot | Constraint |
|---|---|
| subject_identity | One original figure with a stable design; a human version must be clearly adult, but the mechanism also works with a non-human figure. |
| clue_objects | Three or more original details attributable to one subject; a transfer may reconnect them more explicitly than the source. |
| setting | One new environment with a stable direction or landmark; avoid the source's blank-field anime design. |
| camera_grammar | Close detail views and a final recognizable identity echo; an optional wider whole-subject proof is an original strengthening, not a source claim. |
| decisive_action | An optional original role-confirming action can strengthen the new instance without being attributed to the source. |
| sound_family | Original, action-linked sound design; no claim that the source music or effects were heard. |

## Required Human-Facing Anchors

- 同一主体
- 局部线索相互一致
- 结尾回连已见标记

## Anti-Copy Boundary

- Do not reproduce the source anime character's face, red eyes, black strappy costume, gold hair ornaments or body proportions.
- Do not copy the original exact crop order, cut timings, palette or bare-white visual field.
- Do not use creator names, franchise identifiers, source caption wording or creator prompt text.

## Transfer Tests

1. An adult offshore lighthouse maintainer is identified through salt-stained gloves, a wrist compass and safety line before activating a beacon.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: subject_identity, clue_objects, setting, camera_grammar, decisive_action, sound_family
2. A stop-motion brass courier automaton is introduced through a stamped wheel, folded paper wing and blue-glass eye before its head returns in a miniature post-office set.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: subject_identity, clue_objects, setting, camera_grammar, decisive_action, sound_family

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

