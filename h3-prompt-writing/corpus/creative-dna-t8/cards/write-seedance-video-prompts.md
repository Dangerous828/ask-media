# write-seedance-video-prompts

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: write-seedance-video-prompts
description: Write model-native Seedance 2.0 video prompts from text, images, video, or audio references. Use for text/image generation, multimodal reference, video editing, extension, track fill, or combined tasks that need stable subjects, explicit asset roles, coherent event order, camera, sound, visible text, and a 4–15 second feasibility check.
---

# Write Seedance Video Prompts

Create a filmable Seedance 2.0 prompt without leaking MiniMax H3 field names or timing grammar. This is a T8-authored companion to the MiniMax repository-bundled `h3-prompt-writing` Skill; use the upstream Skill itself when the target is H3.

## Intake

Confirm only missing information:

- overall duration from 4 through 15 seconds and aspect ratio;
- generation intent: new generation, reference, edit, extension, track fill, or a combination;
- every supplied asset and its narrow role;
- recurring subject bindings, visible action, scene state, camera priority, sound, dialogue, and requested visible copy;
- whether the idea is one simple event or a multi-event sequence.

Do not treat a research video as a generation input. Do not fabricate references, text, dialogue, brands, or sound.

## Build the prompt

1. Assign consecutive `图片N`, `视频N`, and `音频N` labels by modality.
2. State one purpose for every declared asset. Bind ambiguous subjects as `角色A@图片1` or equivalent.
3. Write a cause-and-effect action chain. Include body/object part, direction, speed, force, inertia, contact, and visible consequence where relevant.
4. Prefer one primary camera behavior per shot. Separate genuinely conflicting moves with a cut.
5. Use one natural paragraph for a simple event. Use consecutive `镜头1`, `镜头2`, and so on for complex content.
6. Put dialogue in `{...}`, physical/designed sound in `<...>`, music in `（...）`, and requested visible copy in `【...】`.
7. End with only the constraints that protect identity, geometry, medium, contact, copy, or continuity.

Read `references/template.md` for the task matrix, output skeleton, and final audit.

## Hard rules

- Never add exact per-shot timestamps such as `0–3秒` or “at 3 seconds.” Overall duration is allowed.
- Never emit H3 fields, `<Picture N>/<Video N>`, `[Shot N]`, `(S1)`, timestamp alignment, or H3 retention syntax.
- For edit/extension tasks, name the target as `视频N`, not merely “reference video.”
- For track fill, name two or three videos in playback order.
- Keep every explicit asset reference resolvable and every declared asset purposeful.
- Do not call a paid model, upload media, or import anything into ComfyUI unless the user separately requests that action.

## Deliver

Return the task choice, asset-role map when assets exist, the final Seedance prompt, and short feasibility warnings. Keep the prompt itself clean enough to paste directly into Seedance 2.0.
````

### summary.md

````text
# Seedance 2.0 通用提示词编写

## 摘要

把文字、图片、视频或音频意图整理成 Seedance 2.0 原生提示词，覆盖新生成、多模态参考、编辑、延长、补全和组合任务。重点保证素材职责、主体绑定、事件因果、镜头、声音、文字和 4–15 秒可执行性闭合。

## 使用方法

提供目标时长、画幅、任务类型、素材清单及每项素材的单一职责，再说明主体、事件、镜头、声音和可见文字。Skill 会先做可执行性检查，再输出简单事件段落或连续 `镜头N` 结构。

## 适用范围

- Seedance 2.0 文生/图生、多模态参考、视频编辑、延长、补帧和组合任务。
- 需要把模糊创意整理成模型原生、可审计提示词的场景。
- 不用于 MiniMax H3；H3 应安装并使用官方仓库的 `h3-prompt-writing`。
- 不自动上传素材、不调用付费生成接口，也不导入 ComfyUI 节点。
````

### template.md

````text
# Seedance 2.0 prompt template

## Task matrix

- `text_image_generation`: create a new video from text and optional still/keyframe references.
- `multimodal_reference`: transfer a declared subject, scene, action, camera, effect, style, voice, music, or continuity property.
- `video_editing`: modify a named `视频N`; leave unspecified content unchanged.
- `video_extension`: continue a named `视频N` while preserving audiovisual and narrative continuity.
- `track_fill`: connect two or three named videos in declared playback order.
- `combined`: reference one asset while editing or extending another.

## Planning card

```text
Target: [task family], [4–15 seconds], [aspect ratio]
Subjects: [stable label + 2–3 identity anchors]
Assets: [图片N/视频N/音频N -> one narrow role each]
Event chain: [setup -> trigger -> visible change -> payoff]
Primary camera: [one coherent behavior per shot]
Sound/text: [only requested or evidenced layers]
```

## Simple output

Use one compact paragraph:

```text
[Stable subject binding]. [Initial composition and spatial state]. [Visible trigger and continuous action with speed/force/contact]. [Primary camera behavior]. [Lighting, color, and medium]. [Synchronized sound/dialogue/music/visible copy when requested]. [Compact constraints].
```

## Multi-shot output

```text
镜头1：[composition + subject action + spatial change + camera + necessary sound]
镜头2：[causal handoff + new visible information + coherent camera + necessary sound]
镜头3：[payoff/final state + readable hold + necessary sound]
约束：[only identity, geometry, medium, contact, continuity, or copy protections]
```

Do not attach numeric time ranges to the shots. Let causal and spatial changes determine their length.

## Final audit

- Duration is 4–15 seconds and action density is feasible.
- Shot labels are consecutive when used.
- Every subject and asset label resolves in both directions.
- One shot does not contain contradictory simultaneous camera commands.
- Dialogue language, visible copy, sound, and music are not invented.
- No H3 field name, label, timestamp, or retention syntax remains.
````

