# single-input-delayed-container-overflow

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: single-input-delayed-container-overflow
description: "Create original short videos using the 单次投入｜容器延迟变化与失控收束 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 单次投入｜容器延迟变化与失控收束

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 只发生一次清楚投入
- 反应沿容器连续扩张
- 纠正行为与残留结果都可见

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
# 单次投入｜容器延迟变化与失控收束 — 摘要

## 用途

一个小输入在封闭系统中延迟引发可追踪的扩张，人尝试纠正后留下终态。

## 推荐输入格式

`容器＋一个投入物＋延迟反应＋纠正尝试＋终态`

## 可直接改写的简短示例

> 一名成年技师、一座桌面布料充气城市模型、一根可见总气管、一个压力表与一只上方回收气囊。

## 必须保留的结构锚点

- 只发生一次清楚投入
- 反应沿容器连续扩张
- 纠正行为与残留结果都可见

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 单次投入｜容器延迟变化与失控收束 Template

## Mechanism

One clearly visible small input into a bounded system is followed by delayed local change, accelerating connected expansion and an attempted human correction that arrives too late to prevent an altered but traceable final state.

## Invariants

### inv-01

- Rule: One small deliberate input occurs in a visibly bounded, initially stable system before the anomaly.
- Purpose: Makes the later reaction causally legible.
- Failure if removed: Without a visible input the runaway result feels like an unrelated effect.

### inv-02

- Rule: A local material response expands continuously through the same system in distinguishable stages.
- Purpose: Preserves escalation and physical continuity.
- Failure if removed: If the system jumps directly to maximum scale, there is no readable delayed-response curve.

### inv-03

- Rule: The operator notices and makes a concrete checking or control action after onset but before the changed state settles.
- Purpose: Converts spectacle into a character-versus-system mini-story.
- Failure if removed: If the operator never tries to intervene, the middle beat and human reaction arc disappear.


## Variable Slots

| Slot | Constraint |
|---|---|
| system | One visibly bounded original mechanism with traceable material or stored energy. |
| small_input | Single deliberate gesture that initiates the response. |
| expanding_response | Local onset followed by connected growth within one environment. |
| operator_check | Concrete, readable check after the response begins. |
| terminal_state | A materially changed end state, preferably controlled for the new instance. |
| medium | May change from fluid/foam to air-filled fabric or spring paper. |
| sound | New material-specific effects; do not attribute unheard source audio. |

## Required Human-Facing Anchors

- 只发生一次清楚投入
- 反应沿容器连续扩张
- 纠正行为与残留结果都可见

## Anti-Copy Boundary

- No mage costume, spell book, potion flask, black cauldron, yellow-green pour, pale twin foam bubble, source dialogue/subtitle fragments or exact workbench framing.
- Do not claim an exact original formula or source prompt from an unbound X reply.
- No arbitrary repair action that resets the system or violates stored matter/energy.

## Transfer Tests

1. In a modern theatre model shop, one adult technician nudges a pneumatic valve beside a miniature inflatable city. A single roof rises beyond its measuring mark, then linked buildings swell in sequence. She checks the pressure gauge and closes the inlet; pressure trapped downstream still lifts one connected fabric street. A clearly marked relief vent opens into an overhead collection canopy, leaving the model safely deflated and the technician stunned.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: system, small_input, expanding_response, operator_check, terminal_state, medium, sound
2. In a printmaking studio, one apprentice pulls a single tension cord on a collapsible paper display. One panel opens, then connected spring-loaded leaves extend beyond their stop marks. She checks the release diagram and clamps the drive, but stored spring tension unfolds the remaining panels until a tether catches them in a final fan-shaped sculpture.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: system, small_input, expanding_response, operator_check, terminal_state, medium, sound

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

