# performer-anchor-semantic-lyric-escalation

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: performer-anchor-semantic-lyric-escalation
description: "Create original short videos using the 歌词表演｜稳定主唱锚点与逐句语义升能 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 歌词表演｜稳定主唱锚点与逐句语义升能

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Introduce one stable original performer, performance tool and first lyric in the same readable opening relation.
- Give each lyric line exact readable copy and one distinct motion or spatial behavior derived from its meaning.
- Use graphic elements to expand the performance space without covering the face, hands or primary action.
- After the last lyric proof, reduce text density and end on a longer performer-led movement release.

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
# 歌词表演｜稳定主唱锚点与逐句语义升能 — 摘要

## 用途

用一个持续可辨的原创表演者稳定身份，每句歌词都获得可读文字和与语义一致的图形动作；镜头、版式和群体能量逐句提高，最后减少文字密度，让表演者接管结尾释放。

## 推荐输入格式

`稳定原创表演者 + 3至4句原创歌词 + 每句语义图形行为 + 人物始终可辨 + 逐句升能 + 清字后的表演释放`

## 可直接改写的简短示例

> 银色寸发成年男性穿芥末黄工装夹克，持黑色麦克风沿检修线前进，脚边准确出现【MARK THE PULSE】，四枚信号青轨道标记依次点亮；表演者把麦克风举向关闭的检修门，【OPEN THE CIRCUIT】弯成信号青弧线，门板沿弧线向两侧打开；清除歌词，只保留四枚小型青色路线标记；同一表演者进入明亮中央线，放低麦克风，完成一组完整肩臂动作，背景工人同步举起工作灯回应

## 必须保留的结构锚点

- Introduce one stable original performer, performance tool and first lyric in the same readable opening relation.
- Give each lyric line exact readable copy and one distinct motion or spatial behavior derived from its meaning.
- Use graphic elements to expand the performance space without covering the face, hands or primary action.
- After the last lyric proof, reduce text density and end on a longer performer-led movement release.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 歌词表演｜稳定主唱锚点与逐句语义升能 Template

## Mechanism

Keep one original performer continuously identifiable while each short lyric line appears with accurate readable typography and one graphic behavior derived from its meaning. Raise energy line by line through camera proximity, repeated figures, spatial graphics or audience scale, but never let text obscure the face or replace the performer. After the final lyric proof, reduce copy density and let the same performer carry a longer movement release. The reusable mechanism is performer-anchored semantic lyric escalation, not the source singer, lyrics, vector surface, wardrobe or exact layouts.

## Invariants

### inv-01

- Rule: Introduce one stable original performer, performance tool and first lyric in the same readable opening relation.
- Purpose: Binds identity to the lyric system immediately.
- Failure if removed: Text without a performer becomes a title reel; a performer without text loses the lyric premise.

### inv-02

- Rule: Give each lyric line exact readable copy and one distinct motion or spatial behavior derived from its meaning.
- Purpose: Turns lyrics into visible action rather than subtitles.
- Failure if removed: Generic bouncing text or misspelling weakens semantic proof.

### inv-03

- Rule: Keep the performer traceable through every lyric phase while increasing at least one energy channel per line.
- Purpose: Builds escalation without identity drift.
- Failure if removed: Changing performers or increasing everything at once breaks continuity and legibility.

### inv-04

- Rule: Use graphic elements to expand the performance space without covering the face, hands or primary action.
- Purpose: Lets layout and performance coexist.
- Failure if removed: Foreground type that masks the body destroys the anchor.

### inv-05

- Rule: After the last lyric proof, reduce text density and end on a longer performer-led movement release.
- Purpose: Pays off the accumulated energy through character action.
- Failure if removed: Another dense card at the end prevents performance closure.


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

- Introduce one stable original performer, performance tool and first lyric in the same readable opening relation.
- Give each lyric line exact readable copy and one distinct motion or spatial behavior derived from its meaning.
- Use graphic elements to expand the performance space without covering the face, hands or primary action.
- After the last lyric proof, reduce text density and end on a longer performer-led movement release.

## Anti-Copy Boundary

- the source illustrated female singer, long braids, oversized pink sunglasses, microphone, jewelry and blue-gray outfit
- the source exact lyrics Follow my steps, Catch the rhythm, Start a wave and One by one
- the source pink-orange-blue vector palette, crowd, arrows, numbered ladder and radial paint fields
- the source exact lyric timing, layouts, camera angles and semantic graphic assignments
- the source creator's image and audio reference package and any source music or voice identity

## Transfer Tests

1. An original screen-printed male spoken-word performer in a night railway depot delivers 'Mark the pulse / Carry the signal / Open the circuit / Build the chorus'; route marks, relay lines, opening gates and assembling light bars act out each line before a body-led final refrain.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. An original paper-cut marine biologist performs a four-line educational chant inside a public aquarium; bubbles count the first line, fish paths trace the second, coral fans open for the third and visitor silhouettes join the fourth before the scientist leads a word-light final gesture.
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

