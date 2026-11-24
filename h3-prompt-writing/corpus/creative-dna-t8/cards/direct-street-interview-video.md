# direct-street-interview-video

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-street-interview-video
description: "Design natural vertical street-interview and walk-and-talk video prompts for MiniMax H3 or Seedance 2.0. Use when a user wants spontaneous documentary energy, a referenced recurring person, first-person handheld follow, concise dialogue, moving daylight, believable street parallax, or a consent-led interaction that must fit 4–15 seconds without unreachable beats."
---

# Direct Street Interview Video

Create an original street interaction from a reusable documentary mechanism. This is a non-official, user-contributed Skill; it is not a MiniMax or ByteDance preset.

## Intake

Collect or infer only what is needed:

- target model, task type, duration from 4 through 15 seconds, and aspect ratio;
- the interaction goal, location, subject role, interviewer role, relationship, and ending;
- every generation-time image or video and its narrow role;
- exact approved dialogue, speaker order, and language;
- whether physical contact is explicitly wanted and appropriate;
- the one primary camera behavior, ambient sound, and any requested music or visible text.

Treat the analyzed demonstration video as research evidence, not as an automatic generation reference. Never fabricate a reference asset or dialogue.

## Build the scene

1. Start with one readable social premise: approach, recognition, question, demonstration, compliment, request, or compact reveal.
2. Give the on-camera subject one stable visual identity. With reference media, bind two or three distinctive anchors and preserve wardrobe continuity.
3. Use one continuous route unless a new shot is causally necessary. The default camera is first-person handheld backpedaling or side-walking at conversational distance.
4. Make the relationship change visible through distance, gaze, pace, hand gesture, body angle, or a shared object. Do not substitute random camera motion for performance.
5. Let the street move around the subject: foreground occlusion, background parallax, passing light and shadow, and small exposure adaptation.
6. Keep dialogue subordinate to visible action. Allow each line to finish before the next speaker begins.
7. End on a visible resolved state: permission granted, pose found, object shown, route chosen, reaction landed, or conversation naturally released.

## Feasibility gate

- Every timestamp or later beat must occur before the actual target duration.
- For about 10 seconds, prefer two or three short spoken turns and one continuous event chain.
- For about 15 seconds, prefer no more than four or five short turns unless speech is intentionally rapid and the user supplied it.
- Remove a shot before compressing dialogue into unnatural speed.
- Do not place a new setup exactly at the video endpoint.
- Do not claim 4K, HDR, film stock, lens metadata, or platform provenance unless the user requested or supplied it.
- Default to verbal or gestural positioning. Add touch only when the user explicitly wants it and the staging is consensual, motivated, and physically clear.

## Compile for MiniMax H3

- Select T2VA, I2VA, FL2VA, L2VA, or Ref2VA from the actual generation-time inputs.
- Use the three-field Base structure when no reference relationship is needed.
- Use the six-field Ref2VA structure when a supplied person, wardrobe, voice, scene, or movement reference must be tracked.
- Write official-strict rewrite prose in English. Preserve approved dialogue only in `<d>[Language]...</d>` and identify speakers with `(S1)`, `(S2)`.
- Start with `[Shot 1]` and no timestamp. Later shots use consecutive labels and increasing timestamps below the target duration.
- Keep dialogue only in the detailed visual timeline; do not repeat it in the soundscape.

## Compile for Seedance 2.0

- Write in Chinese by default and choose a task from the actual inputs.
- Use one compact paragraph for a continuous walk-and-talk; use consecutive `镜头N` only when there is a real cut or event boundary.
- Bind references as `角色A@图片1` or equivalent and give every asset one explicit role.
- Put dialogue in `{...}`, physical sound in `<...>`, music in `（...）`, and requested visible text in `【...】`.
- Do not use H3 fields, H3 labels, speaker IDs, or exact per-shot timestamps.

## Validation

Before returning the result, verify:

- duration, speech, and action are jointly feasible;
- every asset reference resolves and every declared asset has a purpose;
- the subject, wardrobe, environment, route, light direction, and hand/object state remain continuous;
- camera motion follows the interaction and does not conflict with itself;
- dialogue order, lip movement, ambience, and optional music do not duplicate or contradict each other;
- the execution changes subject, place, wardrobe, dialogue, route, framing, and ending instead of copying the demonstration surface;
- no paid generation, upload, ComfyUI import, or node modification is performed without a separate request.

## Deliver

Return:

1. one-sentence concept;
2. task and asset-role map;
3. a compact feasibility note;
4. the MiniMax H3 prompt;
5. the Seedance 2.0 prompt;
6. a short continuity and anti-copy audit.
````

### summary.md

````text
# Natural Street Interaction — Skill 摘要

> **分类：非官方 · 用户贡献。** 本 Skill 由用户提供的 AIGC 样片与提示词组启发，经独立拆解、时长校正和双模型重写形成；不是 MiniMax 或 ByteDance 官方 Skill。

## 一句话机制

在连续的真实街道路线中，让镜头与人物边走边交流；人物的距离、视线、步速与手势逐步缩短社交距离，环境视差、树影和现场声同时证明空间真实，最终落到一个清楚且自然的互动结果。

## 风格

- 竖屏、第一人称、纪实街拍与轻微手机手持感
- 单一路线上的跟拍或倒退拍摄，不靠无意义快切制造热闹
- 自然光穿过树叶或建筑缝隙，在人物与背景上连续移动
- 表演以目光、呼吸、步态、微表情和手势为主
- 现场环境声优先；对白短、轮次清楚、不过载

## 适用范围

- 街头采访、偶遇、搭讪式剧情、城市漫步和人物介绍
- 服装、美妆、生活方式、旅行或城市氛围短片
- 有单人参考图、需要保持身份与服装稳定的 Ref2VA / 多模态参考
- 4–15 秒内可以由一个连续动作链讲清的互动

## 不适用范围

- 大段口播、超过五轮的复杂辩论或需要字幕解释的知识内容
- 多地点、多人物群戏、精密舞蹈或大量硬切覆盖镜头
- 未经明确要求的陌生人强行肢体接触
- 需要逐帧复刻某个真人、具体地点、穿搭或原对白的请求

## 使用方法

1. 明确互动目的、目标时长、画幅、人物关系、场景路线和结尾。
2. 如果有素材，给每张图或视频分配唯一角色：身份、服装、环境、动作或声音。
3. 先写“接近—交流—关系变化—落点”的因果链，再决定是否需要切镜。
4. 按时长删减对白：10 秒优先 2–3 句短对白；15 秒也不要机械塞满台词。
5. 分别使用 H3 与 Seedance 模板编译，不能在两种模型之间复制语法。
6. 检查身份、步态、路线、光影、手部接触、声音与时间是否闭合。

## 可变槽位

| 槽位 | 说明 |
|---|---|
| `social_premise` | 偶遇、采访、认出、问路、展示、邀请或道别 |
| `on_camera_subject` | 身份、两三个稳定外观锚点、服装与当前情绪 |
| `interviewer_role` | 画外摄影师、同行者、店主、朋友或路人 |
| `route_geometry` | 直行、侧向并行、拐角会合、短暂停步后继续 |
| `distance_change` | 从远到近、并肩、停下、转身或保持礼貌距离 |
| `gesture_chain` | 目光、整理衣物、指向、递物、示范或告别 |
| `camera_follow` | 倒退跟拍、侧向并行、短暂定住、轻微重构图 |
| `light_behavior` | 树影、橱窗反射、建筑阴影或云层变化 |
| `dialogue` | 用户确认的短句、语言、说话顺序与停顿 |
| `resolved_state` | 许可、姿势、展示、路线、反应或自然离场 |

## 核心质量门

- 第二个事件不能从目标时长终点才开始。
- 镜头运动必须由人物路线或视线驱动。
- 触碰必须有动机、双方可读且不会产生手臂穿插。
- 不把“4K、超高清、电影感”当作缺少动作与空间设计的替代品。
- 样片只提供机制证据；人物外貌、服装、城市、对白和构图不属于可复制模板。

更深入的不变量、消融解释、转移测试和失败修复见 [template.md](./template.md)。
````

### template.md

````text
# Natural Street Interaction Template

## Mechanism

A continuous street route turns a short conversation into visible relationship change: the subject and camera establish distance, exchange one readable social signal, adjust pace or position together, and land on a resolved state while environmental parallax, moving daylight, and location sound prove continuity.

## Invariants

### inv-01 — One readable social premise

- **Rule:** Establish who initiated the interaction and why within the opening action or first short line.
- **Why it matters:** The viewer understands the relationship without exposition.
- **Ablation:** Without it, eye contact and walking look like unrelated beauty footage.

### inv-02 — Camera follows human geography

- **Rule:** The primary camera move must respond to the subject's walking line, turn, stop, gaze, or gesture.
- **Why it matters:** Handheld movement feels documentary rather than random.
- **Ablation:** Without motivated geometry, shake and reframing become noise.

### inv-03 — Performance changes the social distance

- **Rule:** Show at least one visible change in distance, pace, body angle, gaze, or shared-object relation.
- **Why it matters:** The interaction has progression even with minimal dialogue.
- **Ablation:** Without it, the middle is a flat loop of talking while walking.

### inv-04 — Environment proves the continuous route

- **Rule:** Preserve coherent background parallax, moving light/shadow, and location ambience across the event.
- **Why it matters:** These cues ground both subject and camera in the same street.
- **Ablation:** Without them, the person appears composited over an unstable background.

### inv-05 — The ending is a state, not a cutoff

- **Rule:** Reserve enough time for permission, pose, reveal, reaction, route choice, or clean release to become readable.
- **Why it matters:** The scene feels authored rather than truncated.
- **Ablation:** Starting a new beat at the endpoint makes the promised payoff disappear.

## Variable slots

```text
Duration/aspect: [4–15 seconds] / [9:16, 16:9, or requested]
Social premise: [one clear reason to interact]
Subject: [role + two or three stable identity anchors + wardrobe]
Interviewer: [off-screen or visible role]
Street: [specific but original urban context]
Route geometry: [straight, parallel, corner meeting, stop-and-resume]
Opening distance: [wide, conversational, or close]
Performance chain: [gaze → pace/gesture change → resolved state]
Camera follow: [one primary handheld behavior]
Light behavior: [observable moving natural light]
Dialogue: [approved short lines and speaker order]
Sound: [location ambience + synchronized foley + optional music]
Ending: [one readable final state]
```

## Anti-copy boundary

Never reproduce the demonstration person's likeness, body styling, black tube-top outfit, exact tree-lined street, fence-and-road composition, dialogue, or beat timing. Do not retain the same walking path and simply replace nouns. Change at least six of these together: subject category, relationship, location, route geometry, wardrobe, dialogue purpose, camera implementation, light pattern, prop/contact, and ending.

## Transfer tests

### Transfer A — rain-market product discovery

A ceramic artist walks beside a covered evening market stall while an off-screen host asks one short question. The artist slows, turns a glazed cup through the stall light, and holds it under an awning drip so the surface color changes. The camera side-walks instead of backpedaling; reflections and umbrellas provide parallax; the ending is a quiet material reveal, not a pose or touch.

### Transfer B — sunrise running-route check-in

A neighborhood running coach approaches along a riverside path, answers a compact pace question, briefly matches the camera operator's stride, then points toward a fork and releases into the chosen route. A chest-height jogging camera follows in parallel; low sun flickers through railings; footfalls and breath replace fashion performance.

These tests must remain non-binding. Invent a new execution for the user.

## Quality repairs

- **Dialogue feels rushed:** remove a turn, move information into gesture, and allow a breath-sized pause between speakers.
- **Second shot never appears:** move its action earlier or delete the cut; never start it at the duration boundary.
- **Subject floats over the street:** add continuous occlusion, parallax, foot contact, and moving light across both subject and environment.
- **Camera feels chaotic:** choose backpedal, side-walk, or brief hold as the primary behavior and remove simultaneous orbit/zoom/crane commands.
- **Hands intersect during positioning:** replace touch with a spoken cue or widen the framing and define the exact contact geometry.
- **Identity drifts:** reduce appearance language to stable anchors, bind the reference explicitly, and remove contradictory beauty adjectives.
- **Result copies the sample:** change the social purpose, route, wardrobe, camera side, light system, dialogue, and ending before compiling.

## Model routing

- Use [h3-template.md](./h3-template.md) for MiniMax H3 Base or Ref2VA.
- Use [seedance-template.md](./seedance-template.md) for Seedance 2.0 text/image generation or multimodal reference.
````

