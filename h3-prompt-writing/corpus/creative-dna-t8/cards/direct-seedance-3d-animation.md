# direct-seedance-3d-animation

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-seedance-3d-animation
description: Plan and prompt a stylized 3D animated short for Seedance 2.0 with stable character identities, environment continuity, causal story beats, shot-specific performance, camera, sound, and clip handoffs. Use when a story needs one 4–15 second generation or a longer multi-clip plan; not for photoreal live action, a single still, or generic prompt polishing.
---

# Direct Seedance 3D Animation

Turn a story idea into Seedance-native clip prompts. This is a T8-authored companion to the MiniMax repository-bundled `3d-animation-short-generator`; use the upstream Skill for its H3 workflow.

## Workflow

1. Lock aspect ratio, total duration, dialogue language, and whether the deliverable is one clip or a multi-clip short.
2. Write a one-sentence premise and a causal beat spine. The protagonist must cause or respond to each important change.
3. Define each recurring character with a stable label, two or three identity anchors, wardrobe, silhouette, and emotional baseline.
4. Define environment anchors and screen geography before camera moves.
5. Split a long film into clips of at most 15 seconds. Give every clip a visible opening state, change, payoff, and handoff frame/action.
6. Choose generation assets deliberately: character images for identity, scene images for environment, and videos only for a named action/camera/style role.
7. Compile each clip with `references/template.md`, then audit continuity across clips.

## Seedance rules

- Use one compact paragraph for one continuous event; use consecutive `镜头N` blocks for multi-event clips.
- Never put exact per-shot seconds inside a Seedance prompt. Keep assembly timing in the external shot plan.
- Bind every ambiguous subject to `@图片N` or a declared video role; never leave an unused reference.
- Specify performance through gaze, posture, breath, face tension, anticipation, follow-through, and recovery.
- Use one primary camera behavior per shot and preserve direction across handoffs.
- Put dialogue in `{...}`, sound in `<...>`, and music in `（...）` only when required.
- Do not emit H3 fields, H3 labels, `[Shot N]`, or timestamp alignment.

## Boundaries

Do not call a paid model or upload assets without a separate request. Do not import this official-companion entry into ComfyUI; the user's node already includes the upstream presets.

## Deliver

Return the locked story/identity/environment sheet, clip list, one Seedance prompt per clip, cross-clip handoff notes, and the final continuity audit.
````

### summary.md

````text
# Seedance 2.0 三维动画短片

## 摘要

把故事设定转成可生成的三维动画片段，锁定角色身份、环境锚点、因果节拍、表演动作、镜头、声音与跨片段衔接。长片会被拆成每段不超过 15 秒的连续单元。

## 使用方法

提供故事目标、角色与场景设定、总时长、画幅、对白语言和参考素材。Skill 会建立角色/空间锁定表、故事因果链、逐片段开场与交接状态，再输出 Seedance 2.0 提示词。

## 适用范围

- 风格化 3D 故事、角色短片、连续多片段动画。
- 不适合纯写实实拍、单张静帧或无故事目标的通用润色。
- H3 使用官方仓库 `3d-animation-short-generator`；本 Skill 不导入 ComfyUI。
````

### template.md

````text
# Seedance 3D animation template

## Production lock

```text
Format: [ratio], [total duration], [single clip / multi-clip]
Character A: [identity anchors, silhouette, wardrobe, emotional baseline]
Environment: [layout anchors, light direction, palette, fixed objects]
Story chain: [want -> obstacle -> action -> consequence -> payoff]
```

## Per-clip card

```text
Clip purpose: [new story information]
Opening state: [subject pose, screen position, environment state]
Action chain: [anticipation -> committed action -> contact/consequence -> recovery]
Handoff: [last pose, gaze, object motion, camera direction, sound tail]
References: [图片N/视频N -> one role each]
```

## Prompt skeleton

```text
镜头1：[stable subject binding and composition]. [visible performance and object action]. [primary camera behavior]. [light/material/style]. [sound].
镜头2：[continue the causal action without resetting identity or geography]. [new consequence and reaction]. [coherent camera]. [sound/dialogue].
镜头3：[resolve the clip goal and hold a handoff-ready final state].
约束：角色身份、服装、比例、场景锚点和光线方向稳定；无多余角色、无肢体融合、无风格漂移。
```

Use fewer shots when fewer causal changes exist. For a continuous performance, replace the blocks with one paragraph.

## Cross-clip audit

- Identity, wardrobe, scale, handedness, prop ownership, and environment landmarks match.
- Camera direction and moving objects enter the next clip consistently.
- Dialogue and sound tails are not duplicated.
- No clip exceeds 15 seconds and no Seedance prompt contains shot timestamps or H3 syntax.
````

