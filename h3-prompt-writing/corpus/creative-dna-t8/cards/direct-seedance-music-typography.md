# direct-seedance-music-typography

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-seedance-music-typography
description: Plan Seedance 2.0 music-video clips where performance, camera, scene changes, spatial lyric typography, and transitions respond to a locked music window. Use for 4–15 second hooks or longer multi-clip MVs with explicit audio/lyric ownership, subject and scene references, beat-led events, and assembly handoffs; not for ordinary caption cleanup or unlicensed lyric copying.
---

# Direct Seedance Music Typography

Treat music, performance, camera, and visible words as one synchronized design system. This is a T8-authored companion to the MiniMax repository-bundled `music-video-subtitle-generator`; use the upstream Skill for H3.

## Workflow

1. Lock aspect ratio, total duration, exact music window, lyric ownership, language, performer, and intended typography role.
2. If the work exceeds 15 seconds, split it into independently generated clips while preserving one master audio timeline for later assembly.
3. Give character, scene, typography-style, video, and audio references separate roles. Never let a typography card supply a person or location.
4. Map vocal phrases and beat accents to visible performance, scene changes, camera impulses, typography entrances, and transition exits.
5. Keep one main typography event per shot and protect eyes, mouth, and lip-sync.
6. Compile each clip with `references/template.md`; maintain cross-clip identity, palette, grain, light, motion direction, and audio continuity.

## Seedance rules

- Bind a supplied track as `音频1` and state that it provides music/voice timing. Do not declare audio that will not be supplied at generation time.
- Use `{exact lyric}` for performed words and `【exact visible lyric】` for on-screen typography.
- Use `镜头N` in event order, not exact per-shot timestamps. Beat words such as “on the snare” or “after the bass hit” are allowed.
- Keep one coherent camera behavior per shot; use cuts or match motion for scene changes.
- Do not emit H3 fields, `[Shot N]`, H3 labels, or alignment syntax.

## Boundaries

Do not invent or rewrite user-owned lyrics without permission. Do not call generation, upload music, or import into ComfyUI without a separate request.

## Deliver

Return the music/lyric lock, reference-role map, beat-event plan, Seedance prompt per clip, assembly handoffs, and lyric/typography/audio audit.
````

### summary.md

````text
# Seedance 2.0 音乐与动态文字 MV

## 摘要

把音乐窗口、表演、运镜、场景变化和空间歌词文字编成同一个节奏系统。支持 4–15 秒 hook，也支持按主音轨拆分并衔接多个片段。

## 使用方法

提供合法可用的音乐/歌词、准确时间窗、表演者与场景素材、字体包装方向、画幅和总时长。Skill 会建立节拍事件表、素材职责、跨片连续性和逐片段 Seedance 2.0 提示词。

## 适用范围

- MV、音乐视觉、说唱/演唱片段、节拍驱动空间字效。
- 不用于普通字幕清理，也不复制无权使用的歌词。
- H3 使用官方仓库 `music-video-subtitle-generator`；本 Skill 不导入 ComfyUI。
````

### template.md

````text
# Seedance music-typography template

## Master lock

```text
Master audio: 音频1 -> exact music/voice window
Lyrics: [user-supplied / original approved / no lyrics]
Performer@图片1: [identity and wardrobe]
Scene@图片2: [space, light, palette]
Typography style@图片3: [font texture/layout/motion only]
Global look: [grain, color, lighting, lens]
```

## Beat-event plan

Keep external editorial timing in a separate plan. Each event records:

- lyric or musical cue;
- performer action and mouth/breath/gaze behavior;
- one spatial typography event;
- one camera impulse or cut;
- transition handoff.

## Prompt skeleton

```text
音频1提供全片音乐、节奏和人声时序。表演者@图片1保持身份、服装和面部比例，场景@图片2保持空间、光线与色调，图片3只提供文字包装风格。
镜头1：表演者随[opening cue]完成[visible performance]，演唱/说出{exact lyric}；空间文字【exact lyric】在不遮挡眼睛和嘴部的位置以[one motion]出现，镜头[one coherent behavior]。
镜头2：在[snare/bass/vocal accent]发生[hard cut or match move]，动作延续到新构图；表演者完成[next phrase]，只出现一个新的【exact visible lyric】事件。
镜头3：[payoff performance and final text state]，动势与音乐尾部连续收束。
约束：歌词、口型和可见文字逐字一致；每镜头最多一个主文字事件；人物、服装、颗粒、色调、光向稳定；无普通字幕条、无多余文案Logo水印。
```

## Audit

- Every performed and visible word comes from the locked lyric source.
- Audio, character, scene, and typography references do not cross-contaminate roles.
- Cuts land on meaningful musical or vocal events without breaking an active phrase arbitrarily.
- Multi-clip handoffs preserve master-audio position externally; prompts contain no exact shot times.
- No H3 grammar remains.
````

