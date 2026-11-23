# reciprocal-touch-state-confirmation

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: reciprocal-touch-state-confirmation
description: "Create original short videos using the 双向接触｜动作回应与状态确认 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 双向接触｜动作回应与状态确认

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 主动与回应次序清楚
- 状态信号独立可见
- 结束时两主体仍可区分

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
# 双向接触｜动作回应与状态确认 — 摘要

## 用途

一方轻触之后另一方主动回应，再以独立状态信号证明关系变化。

## 推荐输入格式

`两个主体＋首次接触＋反向回应＋状态信号`

## 可直接改写的简短示例

> 一位成年灯光技师、一盏固定在地面的黄铜机械追光灯、空舞台上的白色定点；只用一套设备。

## 必须保留的结构锚点

- 主动与回应次序清楚
- 状态信号独立可见
- 结束时两主体仍可区分

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 双向接触｜动作回应与状态确认 Template

## Mechanism

A human approaches a responsive engineered counterpart; one tactile initiative is followed by a distinct reciprocal movement, then an independently visible state acknowledgement and a final separated pose that proves the relationship changed.

## Invariants

### inv-01

- Rule: Establish a stable two-sided gap and delay the engineered system's response until after a human initiative.
- Purpose: Creates a clear question of recognition rather than an already-active machine.
- Failure if removed: If the system begins fully responsive, the contact has no dramatic function.

### inv-02

- Rule: Human touch or insertion and system reciprocity are separate readable events across a continuous spatial anchor.
- Purpose: Makes acceptance visible rather than merely declared.
- Failure if removed: A status caption alone would claim an outcome without physical confirmation.

### inv-03

- Rule: Show the acknowledged state and a changed final spatial relation after the reciprocal action.
- Purpose: Completes the interaction with a functional new state.
- Failure if removed: If the scene ends at contact, the audience cannot tell what the interaction enabled.


## Variable Slots

| Slot | Constraint |
|---|---|
| human_role | Adult initiator with a concrete task, not source character identity. |
| counterpart | One engineered responsive object/system with a physical response. |
| contact_interface | One visible sensor, slot or tactile control. |
| reciprocal_motion | Physical acknowledgement distinct from the initial touch. |
| status_signal | Original short visible state change after response, not source dialogue. |
| final_function | Demonstrate newly enabled function in same geography. |
| setting | Can change lab to stage, dock or another controlled environment. |

## Required Human-Facing Anchors

- 主动与回应次序清楚
- 状态信号独立可见
- 结束时两主体仍可区分

## Anti-Copy Boundary

- No source woman's face, tattoos or wardrobe, no white humanoid robot, no intimate near-kiss framing, shoulder embrace, glowing robot chest or source status wording.
- Do not assert source dialogue, actual authentication details or unseen AI intentions.
- No status overlay before the physical response.

## Transfer Tests

1. On a dim empty stage, an adult lighting technician approaches an autonomous tracking spotlight fixed to its floor base. She slowly presents a gloved hand near its cold brass sensor ring; the lamp head first resists, then rotates a few degrees to mirror her hand, and a small mechanical iris opens. Only after a visible sensor contact and motor response does its own panel illuminate the original text 'OPERATOR READY'. She steps aside; the spotlight turns away from her and projects one clean circle on the empty stage.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: human_role, counterpart, contact_interface, reciprocal_motion, status_signal, final_function, setting
2. At a coastal research dock, a field scientist approaches a silent buoy-launch rail. She places one coded sample tag into a physical slot; a small robotic clamp mirrors her hand movement and closes around the tag. A green mechanical flag rises only after the tag is seated; she steps back while the now-enabled rail advances one buoy into its ready cradle.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: human_role, counterpart, contact_interface, reciprocal_motion, status_signal, final_function, setting

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

