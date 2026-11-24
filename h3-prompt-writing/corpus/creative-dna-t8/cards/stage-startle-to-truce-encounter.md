# stage-startle-to-truce-encounter

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: stage-startle-to-truce-encounter
description: "Design short cinematic encounters that move from calm observation to an impossible close appearance, a readable startle response, and a restrained truce gesture for MiniMax H3 or Seedance 2.0. Use when a user wants fantasy-versus-technology contrast, cockpit or window eyelines, pursuit compressed into 4–15 seconds, non-lethal escalation, identity-reference continuity, or a tense scene that resolves through performance instead of injury or dialogue exposition."
---

# Stage Startle-to-Truce Encounter

Build an original close encounter whose tension resolves through spatial reversal and performance. This is a non-official, user-contributed Skill; it is not a MiniMax or ByteDance preset.

## Intake

Collect or infer only what is needed:

- target model, task type, duration from 4 through 15 seconds, and aspect ratio;
- calm subject, technical observer, separating boundary, encounter space, and final relationship state;
- one bounded startle or defensive action and whether it is visibly non-lethal;
- every generation-time image or video and its narrow role;
- identity anchors, vehicle or enclosure continuity, eyeline geometry, primary camera role, sound, and text policy.

Treat the demonstration MP4 as research evidence, not as a generation input. Never invent a reference asset, source link, attack, injury, dialogue, or reciprocal gesture.

## Build the encounter

1. Establish a calm baseline and one readable distance between subject and observer.
2. Reveal the observer through a distinct point of view or enclosure so both sides of the encounter are legible.
3. Use one bounded escalation: alarm, defensive burst, evasive turn, shield, marker, or abrupt recoil. Do not stack unrelated weapons and effects.
4. Reverse the spatial relation by letting the formerly observed subject close an apparently impossible distance.
5. Confirm proximity with a shared axis, matched speed, correct eyelines, and one frame containing both sides of the boundary.
6. Externalize the observer's startle through shoulders, grip, head turn, breath, or gaze.
7. Reserve the ending for a small conciliatory offer and a readable held response. Reciprocity is optional unless the user asks for it.

## Feasibility gate

- Use four or five causal beats for a 12–15 second result; shorten the chain for briefer clips.
- Put the decisive close appearance before the final quarter so the reaction and truce have room to land.
- Keep threat non-lethal unless the user explicitly requests otherwise; never require injury to prove escalation.
- Do not call countermeasure flares, marker pods, alarms, or light trails guided missiles unless complete evidence proves that identity and direction.
- Use one primary camera purpose per beat: establish, observer POV, kinetic proof, proximity proof, or reaction payoff.
- For window or canopy interaction, bind screen direction, eye height, relative speed, reflection, and the physical barrier.
- When an image is supplied, use it only for declared identity or wardrobe unless the user explicitly assigns scene or first-frame control.

## Compile for MiniMax H3

- Choose Base or Ref2VA from the actual generation-time assets, not from the research sample.
- Use official-strict English fields. Keep the first shot untimestamped; later timestamps must increase and stay within the duration.
- Put appearance, action, camera, synchronized effects, and any dialogue inside the visual timeline.
- Keep ambience and action effects in `overall_soundscape`; do not repeat them elsewhere.
- Use a final shared-axis shot long enough to prove the gaze and truce offer.

## Compile for Seedance 2.0

- Use a complex multi-shot structure for the full calm-to-truce arc.
- Write consecutive `镜头N` beats in event order without exact per-shot timestamps.
- Bind every supplied asset as `角色A@图片1` or equivalent and assign one narrow role.
- Use `<...>` for physical effects, `{...}` for dialogue, and `（...）` for music.
- Keep constraints shorter than the action design and remove all H3 field syntax.

## Validation

Before returning the result, verify:

- the baseline, observer POV, escalation, proximity proof, startle, and truce form one causal chain;
- subject identity, observer, enclosure, screen direction, speed, light, and boundary remain continuous;
- the defensive action is named from visible mechanics rather than assumed intent;
- both eyelines converge across the barrier and the conciliatory gesture is physically readable;
- the execution changes subject type, setting, transport, threat device, camera implementation, palette, sound, and ending behavior instead of copying the demonstration surface;
- H3 and Seedance syntax remain separate;
- no paid generation, upload, ComfyUI import, or node modification occurs without a separate request.

## Deliver

Return:

1. one-sentence concept;
2. task and asset-role map;
3. one compact recommended input for a prompt-enhancer field;
4. MiniMax H3 prompt;
5. Seedance 2.0 prompt;
6. continuity, feasibility, and anti-copy audit.
````

### summary.md

````text
# Startle-to-Truce Encounter — Skill 摘要

> **分类：非官方 · 用户贡献。** 本 Skill 由用户提供的 AIGC 样片与提示词文本启发，经完整解码、逐段画面核对、时长修复和双模型重写形成；不是 MiniMax 或 ByteDance 官方 Skill。

## 一句话机制

让一个平静主体被技术观察者发现，通过双方视角建立认知差；一次非致命惊慌反应把距离推到极端，主体再以不可能的近距离同框反转空间权力，最后用持续对视和一个迟疑手势尝试把威胁降级，但不虚构双方已经和解。

## 推荐简写输入

把下面这一段替换槽位后直接放入提示词增强器，比复制整篇样片提示词更稳定：

```text
15秒，16:9。[平静主角]被[技术观察者]意外发现；双方通过独立视角建立距离。观察者因主角突然贴近[舷窗/观察窗/透明屏障]而做一次非致命惊慌反应，主角保持克制并与其准确对视。结尾由观察者迟疑地做出求和手势，主角以停留、轻微表情或小幅回应让关系降级。保持身份、载具、屏障、速度、光向和视线连续；不受伤，不堆叠武器，不加字幕Logo水印。
```

如使用参考图，再加一句：

```text
图片1只锁定角色A的身份、脸型、发型与服装，不继承原图场景、构图、姿势或首帧。
```

## 风格与适用范围

- 幻想主体与现代科技、自然生物与研究设备、微缩生命与控制室之间的反差相遇
- 驾驶舱、潜航器、观察窗、温室玻璃、实验舱或透明屏障两侧的精准对视
- 4–15 秒内可讲清的追近、惊吓、误判、试探与非语言和解
- 需要参考图锁定单一角色身份、但必须重建场景和动作的 H3 Ref2VA 或 Seedance 多模态参考
- 靠眼神、肩颈、握力、手势和相对速度完成的轻喜剧或温和戏剧反转

## 不适用范围

- 需要完整战争、多人战术、连续爆炸和复杂武器逻辑的动作大片
- 把受伤、血腥或真实攻击作为必要卖点的内容
- 无法给最终对视和手势留出阅读时间的过载分镜
- 只替换精灵、战机、飞剑、浮空山或水果名词的表面复刻

## 核心质量门

- 决定性贴近必须早于结尾，给受惊和求和留出时间。
- 防御动作只能按可见结构命名；看见对称光轨时不能自动写成制导导弹。
- 结尾至少证明“手势被看见”，不强行声称对方接受和解。
- 玻璃两侧必须具有正确的视线、反射、屏幕方向和匹配速度。
- 13 秒样片不能冒充精确 15 秒；生成模板可重新设计为 15 秒，但必须重新分配事件。

完整不变量、消融解释、转移测试与失败修复见 [template.md](./template.md)。
````

### template.md

````text
# Startle-to-Truce Encounter Template

## Mechanism

A calm subject and a technical observer begin at a readable distance; alternating viewpoints establish asymmetric knowledge, one bounded defensive overreaction increases tension, the observed subject closes the distance and becomes the active side of the encounter, and a shared-axis gaze plus one small conciliatory gesture converts danger into an awkward truce attempt.

## Invariants

### inv-01 — Calm baseline before intrusion

- **Rule:** Establish the subject's stable behavior and the observer's initial distance before the threat changes.
- **Why it matters:** The later startle reads as a contrast rather than generic action noise.
- **Ablation:** Without a calm baseline, the viewer cannot tell what changed or why the reaction matters.

### inv-02 — Two viewpoints carry different information

- **Rule:** Give the subject and observer distinct proof views, such as exterior subject framing and an enclosed observer POV.
- **Why it matters:** The viewer understands who noticed whom and which side lacks information.
- **Ablation:** Without the observer view, surprise becomes an unsupported facial reaction.

### inv-03 — One bounded overreaction

- **Rule:** Use one readable, non-lethal alarm, recoil, evasive move, defensive burst, shield, marker, or countermeasure.
- **Why it matters:** A single escalation gives the encounter stakes without consuming the whole runtime.
- **Ablation:** Without it, the close appearance has no tension; with several unrelated attacks, causality collapses.

### inv-04 — Spatial power reversal is physically proved

- **Rule:** The formerly distant subject must close the separation and share one axis, matched motion, or one frame with the observer across a clear boundary.
- **Why it matters:** Proximity changes the subject from an object of observation into an active participant.
- **Ablation:** A reaction close-up without proximity proof leaves the encounter geography ambiguous.

### inv-05 — Gesture de-escalation receives a hold

- **Rule:** End with sustained eye contact and one small conciliatory offer; hold the other subject's visible reaction long enough to show the offer was perceived.
- **Why it matters:** Performance, not exposition or injury, supplies the payoff.
- **Ablation:** Cutting immediately after the gesture makes it decorative and leaves the relationship unresolved.

## Variable slots

```text
Duration/aspect: [4–15 seconds] / [requested ratio]
Calm subject: [role + stable identity anchors + baseline action]
Observer: [role + enclosure or viewing device]
Initial separation: [distance and spatial axis]
Boundary: [canopy, viewport, glass wall, holographic shield, water surface]
Observer viewpoint: [cockpit POV, instrument insert, over-shoulder, reaction close-up]
Bounded escalation: [alarm, recoil, flare, marker, shield, evasive motion]
Distance-closing action: [glide, swim, climb, roll, materialize, match speed]
Startle performance: [grip, shoulder recoil, head turn, breath, gaze]
Truce offer: [open palm, lowered tool, light signal, nod, object placement]
Held response: [gaze, softened posture, minimal reciprocal gesture, continued parallel motion]
Camera proof: [exterior geography, observer POV, shared-axis two-shot]
Sound: [ambient system + escalation transient + restrained ending]
```

## Anti-copy boundary

Do not reproduce the demonstration's fantasy woman, specific hair ornaments, fruit, sword flight, military jet, pilot costume, floating mountains, vertical light column, flare composition, or exact canopy staging. Do not turn those nouns into placeholders. Change subject category, observer system, environment, boundary, movement physics, escalation device, palette, sound family, camera implementation, and ending behavior together.

## Transfer tests

### Transfer A — deep-reef inspection truce

An adult bioluminescent reef courier rests above a thermal garden while a research submersible watches from a distance. The operator releases three harmless locator pods when the courier suddenly matches the vessel's speed. The courier appears beside the spherical viewport; the operator recoils, then presses an open palm to the glass. The courier holds eye contact and answers with a small two-finger signal. Water drag, buoyancy, amber cabin light, cyan organisms, sonar ticks, and a lateral underwater tracking axis replace every aerial and military surface.

### Transfer B — greenhouse guardian at the glass

A night horticulturist inside a climate-control booth notices a large luminous pollen guardian moving between dark greenhouse aisles. The automatic fans flare defensively and scatter mist. The guardian rides the airflow to the booth window and stops inches from the glass. The horticulturist lowers a mist nozzle, turns off the alarm, and places one seed tray at the sill; the guardian remains still while its wing light softens. Locked interior geometry, macro wing motion, wet glass reflections, fan-driven mist, and one static final two-shot replace vehicle pursuit.

Both transfers preserve `inv-01` through `inv-05` while changing subject, setting, physics, observer, boundary, escalation, camera, palette, sound, and ending object.

## Quality repairs

- **Prompt promises more than the video can hold:** reduce to calm baseline, observer reveal, one escalation, proximity proof, and truce hold.
- **Threat identity is ambiguous:** describe visible launch geometry and light behavior; do not label it as a missile, weapon, or attack without proof.
- **Close appearance feels like teleportation:** add a short distance-closing trajectory or a motivated occlusion before the shared-axis shot.
- **Eyelines miss across glass:** fix screen side, eye height, reflection, and matched speed before adding facial detail.
- **Startle is cartoonish:** use grip tension, shoulder recoil, breath, head turn, and widened eyes instead of screaming or loss of control.
- **Gesture has no payoff:** hold the receiver's gaze or posture change; reciprocity is optional.
- **Identity drifts:** bind two or three stable anchors and remove redundant beauty adjectives.
- **Result copies the sample:** replace every named subject, prop, vehicle, landscape, threat device, camera path, and ending gesture before compiling.

## Recommended enhancer input

```text
15秒，16:9。[平静主体]被[技术观察者]发现；观察者因主体突然贴近[透明边界]而做一次非致命惊慌反应。用外部空间镜头、观察者视角和最终同轴双人镜头证明距离反转。结尾让观察者迟疑地发出求和手势，主体以可读停留或最小回应结束。身份、载具、边界、相对速度、光向与视线连续，不受伤，不堆叠武器，不加字幕Logo水印。
```

## Model routing

- Use [h3-template.md](./h3-template.md) for MiniMax H3 Base or Ref2VA.
- Use [seedance-template.md](./seedance-template.md) for Seedance 2.0 text/image generation or multimodal reference.
````

