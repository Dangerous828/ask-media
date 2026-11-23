# direct-imperfect-memory-farewell

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-imperfect-memory-farewell
description: "Create original short videos using the 复古手持｜日常送别回眸 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 复古手持｜日常送别回眸

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 先建立观察者媒介
- 至少两个普通日常动作
- 外部信号改变目标
- 一次回应后以有动机失误收尾

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
# 复古手持｜日常送别回眸 — 摘要

## 用途

观察者先发现人物日常，外部信号改变人物目标，一次回应后以有动机的拍摄失误结束。

## 推荐输入格式

`观察者媒介 + 日常人物/地点 + 两个日常动作 + 外部信号改变目标 + 一次回应 + 有动机录制失误`

## 可直接改写的简短示例

> 家用摄像机记录泳池管理员收拾浮板和锁柜门，远处哨声让她改变去向；她回头挥一次手，摄影者追拍时短暂失焦并切到水面。

## 必须保留的结构锚点

- 先建立观察者媒介
- 至少两个普通日常动作
- 外部信号改变目标
- 一次回应后以有动机失误收尾

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 复古手持｜日常送别回眸 Template

## Mechanism

An imperfect continuous observer discovers a subject already engaged in an ordinary routine, lingers through small unperformed actions, then lets one external environmental cue change the subject's goal. A single late acknowledgment briefly closes the distance between subject and operator before a motivated exit and imperfect recording finish. Place, subject, routine, cue, medium defects, acknowledgment and exit remain variable.

## Invariants

### inv-01

- Rule: Begin with the operator discovering the subject inside a legible everyday geography rather than presenting a perfect hero frame.
- Purpose: Establishes a lived observer relationship and makes later acknowledgment meaningful.
- Failure if removed: A polished centered opening feels staged and removes the sense of a found private memory.

### inv-02

- Rule: Give the subject at least two low-amplitude routine actions before the external cue arrives.
- Purpose: Builds personality and temporal patience without dialogue or plot exposition.
- Failure if removed: If the cue arrives immediately, the clip becomes a generic arrival or departure shot with no remembered life.

### inv-03

- Rule: Use one visible or audible environmental cue to cause a clear change of goal inside the same continuous geography.
- Purpose: Creates narrative motion without a cut or scripted speech.
- Failure if removed: An uncaused exit feels arbitrary; multiple competing cues fragment attention.

### inv-04

- Rule: Reserve one brief direct acknowledgment of the operator for the threshold just before exit.
- Purpose: Turns detached observation into a personal memory while keeping the behavior candid.
- Failure if removed: Repeated posing feels performative; no acknowledgment leaves the observer relationship emotionally unused.

### inv-05

- Rule: Let medium imperfections follow operator attention—late focus, overshoot, exposure correction or a missed finish—without obscuring the causal action.
- Purpose: Makes the capture feel human while protecting readability.
- Failure if removed: Random constant shake becomes a filter; flawless coverage loses the memory texture; defects at the cue can hide the story.


## Variable Slots

| Slot | Constraint |
|---|---|
| memory_medium | One era-appropriate consumer format with a specific, restrained defect profile. |
| everyday_place | A coherent public or private location whose geography supports one continuous take. |
| subject_identity | An original person with stable appearance, clothing and relationship to the operator. |
| routine_actions | Two or three small actions with props native to the place. |
| external_cue | One event that visibly changes the subject's goal. |
| acknowledgment | One brief glance, nod, gesture or shared joke near exit. |
| exit_path | A physically continuous departure through the established geography. |
| operator_mistake | One motivated focus, zoom, framing or endpoint error that remains readable. |

## Required Human-Facing Anchors

- 先建立观察者媒介
- 至少两个普通日常动作
- 外部信号改变目标
- 一次回应后以有动机失误收尾

## Anti-Copy Boundary

- coastal railway platform, Korean signs, sea-facing parallel tracks, silver commuter train and weathered bench
- young Korean woman, beige trench coat, blue jeans, brown shoulder bag, takeaway coffee and source appearance
- exact stand-sit-sip-train-wave-board sequence and exact fifteen-second boundaries
- source early-2000s MiniDV brand/profile, heavy shake pattern, autofocus targets, exposure behavior and downward platform finish

## Transfer Tests

1. A late-1990s Hi8 home video at a neighborhood community pool discovers a young adult lifeguard stacking kickboards and folding towels; the motorized pool cover starts, he shoulders a duffel, gives the operator one small come-on nod and exits through a chain gate as the camera overshoots.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: memory_medium, everyday_place, subject_identity, routine_actions, external_cue, acknowledgment, exit_path, operator_mistake
2. A small-town bakery closing video on consumer VHS-C follows an older baker brushing flour and tying bread bags; a delivery bell and rolling shutter door trigger departure, she taps the lens hood playfully once and leaves through the back alley while white balance drifts under fluorescent light.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: memory_medium, everyday_place, subject_identity, routine_actions, external_cue, acknowledgment, exit_path, operator_mistake

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

