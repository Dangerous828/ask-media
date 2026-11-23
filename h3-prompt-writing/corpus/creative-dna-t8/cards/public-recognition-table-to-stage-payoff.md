# public-recognition-table-to-stage-payoff

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: public-recognition-table-to-stage-payoff
description: "Create original short videos using the 公共兑现｜席间期待—揭晓—群体释放—登台锁定 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 公共兑现｜席间期待—揭晓—群体释放—登台锁定

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish the full public venue and terminal recognition destination before isolating a peer group.
- Create a calm, readable small-group baseline inside the larger event.
- Keep the recognized subject spatially traceable through group release and movement toward the destination.
- End with the same subject, a concrete recognition object and the public destination readable together.

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
# 公共兑现｜席间期待—揭晓—群体释放—登台锁定 — 摘要

## 用途

先用大型正式场合和席间小群体建立期待，再让公开揭晓把私人关系瞬间转成共同反应；通过拥抱和穿越人群的连续路线释放情绪，最终把被认可者锁定在舞台终点。

## 推荐输入格式

`公共场合与终点 + 小群体平静基线 + 单次公开揭晓 + 共同释放与连续路线 + 人物和认可物终点锁定`

## 可直接改写的简短示例

> 承压玻璃礼堂内布满琥珀桌灯，前方只有一个发光标本台，窗外深青海水与远处珊瑚结构可见；投影只显示原创珊瑚礁修复图与四个简洁头像，回到同桌时四人同步显出惊讶，首席工程师用手停住一次呼吸；同一工程师打开盒子、在麦克风旁举起一枚小型活珊瑚胶囊，后方实时珊瑚画面亮起新生息肉；只保留可见说话动作，不指定台词

## 必须保留的结构锚点

- Establish the full public venue and terminal recognition destination before isolating a peer group.
- Create a calm, readable small-group baseline inside the larger event.
- Keep the recognized subject spatially traceable through group release and movement toward the destination.
- End with the same subject, a concrete recognition object and the public destination readable together.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 公共兑现｜席间期待—揭晓—群体释放—登台锁定 Template

## Mechanism

Establish a public recognition venue and its terminal stage before narrowing to one small peer group with a calm relational baseline. Use one public announcement or display to trigger a connected, visible group reaction. Keep the recognized subject traceable through an uninterrupted chain of embraces, standing and movement across the venue, then finish with the same subject isolated at the public destination holding a concrete recognition object. The mechanism is private baseline to public-status transformation, not a celebrity, award brand or specific speech.

## Invariants

### inv-01

- Rule: Establish the full public venue and terminal recognition destination before isolating a peer group.
- Purpose: Defines the stakes and route in advance.
- Failure if removed: Opening only at the table makes the later stage feel unrelated.

### inv-02

- Rule: Create a calm, readable small-group baseline inside the larger event.
- Purpose: Provides a relationship state that can visibly change.
- Failure if removed: Immediate celebration removes contrast and causal anticipation.

### inv-03

- Rule: Use one public announcement or display to trigger reactions within that same group.
- Purpose: Binds public information to private emotional consequence.
- Failure if removed: A detached reaction montage cannot prove who received the news.

### inv-04

- Rule: Keep the recognized subject spatially traceable through group release and movement toward the destination.
- Purpose: Turns status change into a continuous physical journey.
- Failure if removed: Teleporting directly to stage loses the communal payoff and route.

### inv-05

- Rule: End with the same subject, a concrete recognition object and the public destination readable together.
- Purpose: Provides unambiguous terminal proof.
- Failure if removed: Ending in the aisle or on unrelated applause leaves recognition unresolved.


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

- Establish the full public venue and terminal recognition destination before isolating a peer group.
- Create a calm, readable small-group baseline inside the larger event.
- Keep the recognized subject spatially traceable through group release and movement toward the destination.
- End with the same subject, a concrete recognition object and the public destination readable together.

## Anti-Copy Boundary

- the source Hollywood awards venue, black-tie tables, golden stage and Academy-like statuette
- the source recognizable celebrity-like faces, identities, wardrobe and table grouping
- the source nominee portrait wall, generated names and exact announcement graphics
- the source exact surprise, embrace, aisle-walk and acceptance-speech staging
- the source warm gold-and-black ceremony palette, microphone framing and documentary surface

## Transfer Tests

1. In an original underwater research dome, a wide establishes the glass auditorium and illuminated specimen platform, then four marine engineers wait at one table. A projection reveals their reef-restoration design, the team embraces the lead engineer, she walks through a corridor of colleagues and ends on the platform holding a small living-coral capsule beside the restored reef feed.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. In an original rural night-school festival, a wide establishes a lantern courtyard and timber presentation porch, then three adult learners and their teacher wait at a bench. A hand-painted results board reveals the selected solar-pump design, the group releases into embraces, the designer crosses the applauding courtyard and ends on the porch holding the working brass valve as water begins flowing in the background.
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

