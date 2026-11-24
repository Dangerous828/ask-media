# break-kinetic-text-obstacles

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: break-kinetic-text-obstacles
description: "Create original short videos using the 动力短片｜文字障碍逐个击碎 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 动力短片｜文字障碍逐个击碎

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- 开场先建立受抑制环境状态
- 短词必须占据真实路线空间
- 障碍只能由主角前进动作击碎
- 每次击碎恢复可见环境状态
- 结尾只用一个原创短句命名结果

3. Change source-specific people, setting, props, palette, dialogue, shot boundaries, sound family, and payoff surfaces together.
4. Compile MiniMax H3 and Seedance 2.0 independently; do not leak one model's field syntax into the other.
5. Silently verify anchor coverage, continuity, timing, physical causality, and anti-copy distance before returning the final prompts.

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
# 动力短片｜文字障碍逐个击碎 — 摘要

## 用途

低饱和世界里，短词成为路线上的实体障碍，主角通过前进动作逐个击碎，每次冲击恢复一部分颜色，最后用一个原创短句命名新状态。

## 推荐输入格式

`受抑制环境基线 + 2个短词实体障碍 + 主角前进击碎 + 每次恢复环境状态 + 一个原创结尾短句`

## 可直接改写的简短示例

> 配送无人机穿过灰色物流隧道，依次撞碎实体词 DELAY 与 HOLD，每次冲击恢复一段路线灯，最后停入装载区并出现短句 ROUTE CLEAR。

## 必须保留的结构锚点

- 开场先建立受抑制环境状态
- 短词必须占据真实路线空间
- 障碍只能由主角前进动作击碎
- 每次击碎恢复可见环境状态
- 结尾只用一个原创短句命名结果

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 动力短片｜文字障碍逐个击碎 Template

## Mechanism

Begin in a visually suppressed world, bind one short word or phrase to a physical obstacle in the subject's route, and require the subject's forward action to break that obstacle rather than merely passing it. Each break restores a visible part of the world; finish with one original concise statement that names the achieved state, not the source slogan.

## Invariants

### inv-01

- Rule: Begin with one visibly suppressed environmental state.
- Purpose: Creates a measurable baseline for recovery.
- Failure if removed: Without a baseline, color restoration has no consequence.

### inv-02

- Rule: Turn a short readable word into a real obstacle on the route.
- Purpose: Binds abstraction to physical action.
- Failure if removed: Floating captions do not participate in causality.

### inv-03

- Rule: Require forward subject action to break each obstacle.
- Purpose: Preserves agency and momentum.
- Failure if removed: Passive explosions detach the change from the protagonist.

### inv-04

- Rule: Make each break restore a visible part of the environment.
- Purpose: Converts impacts into cumulative progress.
- Failure if removed: If nothing changes, repeated breaks feel interchangeable.

### inv-05

- Rule: End with one original concise statement describing the achieved state.
- Purpose: Provides a readable payoff without copying a slogan.
- Failure if removed: A long motivational paragraph overwhelms the visual result.


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

- 开场先建立受抑制环境状态
- 短词必须占据真实路线空间
- 障碍只能由主角前进动作击碎
- 每次击碎恢复可见环境状态
- 结尾只用一个原创短句命名结果

## Anti-Copy Boundary

- STUCK IN THE STATIC
- TOO TIRED
- NOT TODAY
- BREAK THE STATIC / RUN YOUR DAY
- source runner and grey city

## Transfer Tests

1. An autonomous delivery drone crosses a monochrome logistics tunnel, shattering physical DELAY and HOLD barriers; each impact restores route lights, ending on ROUTE CLEAR.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. A tiny sailboat crosses a grey paper sea, cutting through physical DOUBT and DRIFT reefs; color returns to wind and water, ending on TRUE COURSE.
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

