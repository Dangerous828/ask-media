# direct-seedance-paper-collage

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-seedance-paper-collage
description: Turn a narration line, knowledge point, opinion, story beat, or abstract concept into a Seedance 2.0 editorial paper-collage clip with a clear visual metaphor, approved final composition, tactile stop-motion assembly, controlled paper texture, purposeful depth, and synchronized collage sound effects. Use for 4–15 second explainer or B-roll clips; not for realistic presenter ads or editable-layer delivery.
---

# Direct Seedance Paper Collage

Make the idea understandable through paper objects rather than written explanation. This is a T8-authored companion to the MiniMax repository-bundled `paper-collage-explainer-generator`; use the upstream Skill for H3.

## Workflow

1. Extract the intended meaning, emotion, action verb, and one concrete visual metaphor.
2. Choose three to six readable paper groups and a controlled palette. Separate foreground, midground, and background.
3. Default to tactile collage SFX only. Add music, narration, or subtitles only when explicitly requested.
4. Describe or create an approval still that represents the final composition. Bind it only as a visual/final-composition role.
5. Plan assembly as readable physical steps: enter, slide/pop, rebound, press flat, pause, lock.
6. Compile one stable Seedance event with `references/template.md`; use multiple shots only when the meaning genuinely changes.

## Seedance rules

- Bind the approved still as `图片1` when supplied and state its role explicitly.
- Preserve halftone cut-outs, cardstock accents, cream keylines, fibers, torn edges, seams, thickness, and soft paper shadows.
- Keep the camera locked unless one restrained miniature move improves comprehension.
- Use `<...>` for paper slide/pop/press/rustle sounds. Do not add speech, music, visible words, or UI by default.
- Use an overall 4–15 second duration; never add exact per-shot timestamps.
- No H3 fields, H3 labels, or alignment syntax.

## Boundaries

Do not call generation before concept approval. Do not import this upstream entry into ComfyUI.

## Deliver

Return the meaning/metaphor card, object and palette plan, final Seedance prompt, optional audio additions, and a metaphor/material/motion audit.
````

### summary.md

````text
# Seedance 2.0 纸拼贴讲解

## 摘要

把知识点、观点或抽象概念变成可理解的纸张物件关系，并用分步进入、轻弹、压平和锁定完成触感定格装配。重点是隐喻可读、纸材真实、层次明确和默认触感音效。

## 使用方法

提供受众要理解的一句话、情绪/动作词、视觉隐喻、纸张物件、色彩与可选最终构图。Skill 会建立概念锁定表并输出 Seedance 2.0 连续装配提示词。

## 适用范围

- 4–15 秒知识讲解、观点 B-roll、故事节拍或品牌概念插段。
- 不用于写实主持人广告、可编辑图层交付或光滑数字图层漂移。
- H3 使用官方仓库 `paper-collage-explainer-generator`；本 Skill 不导入 ComfyUI。
````

### template.md

````text
# Seedance paper-collage template

## Concept lock

```text
Meaning: [one sentence the audience should understand]
Visual metaphor: [one object relationship]
Emotion/action verb: [...]
Paper groups: [3–6 large separable groups]
Palette: [background + 1–3 accents]
图片1: [optional approved final composition only]
Audio: tactile SFX only / explicitly approved additions
```

## Prompt skeleton

```text
[4–15秒，ratio]。高级编辑纸拼贴定格动画，图片1只提供最终构图、色调和纸材风格。开场是与图片1一致的干净[background color]纸面；[base group]先滑入并轻轻回弹，压平后停顿；[main metaphor group]由可见的独立纸片逐个弹入、叠放、压平，和[secondary group]形成[meaning-bearing relationship]；前景、主体中景和背景层次清楚，最后稳定锁定成图片1所示的完整构图并短暂停留。黑白半调照片剪影、少量彩色卡纸、暖奶油描边、细纤维、轻微不规则撕边、层叠接缝、可见厚度和柔和实体投影始终一致。镜头固定或仅做一次极轻微微距推进。<纸片滑动、轻弹、压平敲击、细小摩擦和纸张窸窣声>。约束：无全局淡入、无光滑数字图层漂移、无高速旋转、无混乱飞散、无牛皮纸脏旧底、无新增物体、无文字Logo水印UI；默认无BGM、无旁白、无字幕。
```

If no final still exists, remove `图片1` and describe the final composition explicitly. Never fabricate a reference label.

## Audit

- The metaphor is understandable without visible text.
- Object count stays readable and every piece has a physical assembly action.
- Opening color and final composition belong to the same palette.
- Motion reads as stepped paper stop-motion, not digital layer animation.
- Only explicitly approved audio layers exist; no shot timestamps or H3 grammar remain.
````

