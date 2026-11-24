# direct-seedance-handdrawn-live-fusion

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-seedance-handdrawn-live-fusion
description: Create a Seedance 2.0 prompt for a rough hand-drawn luminous entity that physically contacts a live-action space, continuously transforms while remaining traceable, escapes through adjacent geography, and is followed by a slightly delayed handheld camera. Use for playful 4–15 second mixed-media clips; not for horror, polished CG, unrelated cuts, or simple visual filters.
---

# Direct Seedance Hand-drawn Live Fusion

Design a fresh mixed-media event around physical contact and continuous transformation. This is a T8-authored companion to the MiniMax repository-bundled `handdrawn-live-video-generator`; use the upstream Skill for H3.

## Workflow

1. Choose one everyday live-action space or a set of visibly adjacent areas.
2. Invent a new hand-drawn entity, limited palette, material language, contact object, transformation chain, route, camera reaction, and final spatial payoff.
3. Make the first causal event a readable contact between the drawn entity and a real hand/object.
4. Preserve one trace across transformations: line, tail, smear, contour, color, or rhythmic motion.
5. Let the camera notice and follow slightly late; do not keep the entity perfectly centered.
6. Build a continuous action paragraph unless a genuine cut is required.

## Seedance rules

- Describe contact geometry, resistance, deformation, release, inertia, and the real object's response.
- Use rough crayon, chalk, pencil, pastel, or dry-brush texture with uneven fill, edge chatter, and frame-redrawn variation.
- Keep one entity; do not replace it with an unrelated new creature.
- Prefer one continuous handheld move through connected space. Use `镜头N` only for real cuts.
- Use an overall duration only; never add exact per-shot seconds.
- Use `<...>` for physical sound and `（...）` for music. Do not invent speech or visible text.
- Exclude horror anatomy, threatening attack motion, smooth neon vectors, plastic CG, and perfect tracking.

## Boundaries

Do not copy the upstream example's nouns, transformation sequence, room, route, gag, or ending. Do not call generation or import into ComfyUI without a separate request.

## Deliver

Return the new concept variables, final Seedance paragraph, anti-copy list, and contact/trace/camera/medium audit.
````

### summary.md

````text
# Seedance 2.0 手绘实拍融合

## 摘要

让粗粝发光的手绘实体与真实空间发生可信接触，并沿相邻空间连续变形、逃逸和留下残留。重点是实体可追踪、接触双方都有反应、镜头稍慢半拍跟随，而不是套一个发光滤镜。

## 使用方法

提供实拍空间、手绘媒介与色彩、接触对象、连续变形链、路线、镜头反应和结尾。Skill 会检查空间连续性与变形继承关系，再生成一个连续事件或必要的连续镜头段落。

## 适用范围

- 4–15 秒轻喜剧、奇想或温暖的混合媒介短片。
- 不用于恐怖跳吓、光滑 CG、无因果拼接或简单视觉滤镜。
- H3 使用官方仓库 `handdrawn-live-video-generator`；本 Skill 不导入 ComfyUI。
````

### template.md

````text
# Seedance hand-drawn live-fusion template

## Fresh variables

```text
Live-action space: [one everyday place + adjacent route]
Entity: [initial drawn form]
Medium/palette: [rough medium + 1–3 colors]
Contact: [real hand/object + exact physical relation]
Trace: [feature preserved through all forms]
Transformation chain: [three or four causally connected forms]
Camera reaction: [delayed handheld follow]
Final payoff: [space-scale change + small warm/comic residue]
```

## Single-event prompt skeleton

```text
15秒，16:9。实拍的[space]中，[entity]以[rough medium/palette]出现在[real surface]。它与[real hand/object]发生清晰接触：[contact geometry and real reaction]；接触产生的[trace]连续拉伸为[next form]，沿[adjacent route]逃走，每次变形都保留同一[trace]，没有生成第二个角色。手机手持镜头先看见接触，再慢半拍摇移/前进追赶，实体经常先越过画面边缘，真实物体和人物动作推动相机继续寻找。变化升级为[final spatial payoff]，最后留下[small comic/emotional residue]。手绘质感为[crayon/chalk/pencil/pastel]，线条轻微抖动、填色不均、毛边与逐帧重画感清楚；不是光滑霓虹或3D物体。<contact, paper/stroke and room sounds>。约束：同一空间连续、同一实体可追踪、接触可信、无恐怖解剖、无扑咬跳吓、无字幕Logo水印。
```

Replace every bracket with project-specific content. If a cut is required, convert causal discontinuities into consecutive `镜头N` blocks without timestamps.

## Audit

- Real/drawn contact changes both participants visibly.
- Every transformation inherits a trace from the prior form.
- Geography stays continuous and the camera follows with motivated delay.
- The final payoff grows from the earlier trace rather than appearing arbitrarily.
- Surface nouns and gags are new; no H3 grammar or exact shot time remains.
````

