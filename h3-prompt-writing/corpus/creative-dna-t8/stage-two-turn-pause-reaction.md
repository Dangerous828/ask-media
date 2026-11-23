# 对话喜剧｜双轮停顿无声反应 · Creative DNA 机制卡（T8）

- 验证状态：**外部案例机制，本地 h3q 未测**。原卡来自案例库，未在 MiniMax H3 本地通道出片验收；不得写成"通过配方"。
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）与 comfyui-minimax-h3-prompt-enhancer-T8（插件）。本条目收录的案例库原创摘要、机制说明与提示词模板依 **CC BY 4.0**（[LICENSE-CONTENT](https://github.com/T8mars/minimax-h3-prompt-skill-T8/blob/main/LICENSE-CONTENT)）使用：署名 T8mars，附仓库链接，并说明本条目加入了中文结构分析与本地适用边界。仓库中的应用/公共校验代码为 MIT；ComfyUI 插件为保留全部权利，**未收录任何插件代码**。抓取日期 2026-11-17。
- 完整原文：下方 `` SKILL.md `` 与 `` template.md `` 为逐字收录，不改写；中文结构分析在原文之后。

## 什么时候查这张卡

双人同镜、一问一答、捧哏短答、停顿、结尾无声反应。对 EP001 镜2「讨要」最直接。

## 完整原文 · SKILL.md

````markdown
---
name: stage-two-turn-pause-reaction
description: "Create original short videos using the 对话喜剧｜双轮停顿无声反应 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 对话喜剧｜双轮停顿无声反应

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 开场双人中景建立稳定眼线
- 只保留一轮第一人说话
- 两轮之间有一次清楚停顿
- 第二人只说一轮且动作克制
- 结尾第一人无声反应且不再增加说话轮次

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

## 完整原文 · references/template.md

````markdown
# 对话喜剧｜双轮停顿无声反应 Template

## Mechanism

Use a neutral two-shot to establish equal conversational footing, show one visible speaking turn, hold a clearly readable pause, show a second speaking turn, and end on the first speaker's silent reaction. The source supports only this visual turn-taking and reaction grammar; any question, answer meaning or comic mismatch is an explicitly original instantiation slot, never a source-derived fact.

## Invariants

### inv-01

- Rule: Begin with a neutral two-shot and stable eye lines.
- Purpose: Makes later singles spatially and socially legible.
- Failure if removed: Opening on isolated faces hides the relationship.

### inv-02

- Rule: Use one compact first speaking turn, with its meaning supplied only by the new original instance.
- Purpose: Creates a clean expectation without inventing source semantics.
- Failure if removed: Multiple setup turns blur ownership and weaken the pause.

### inv-03

- Rule: Hold one clearly readable pause between the two visible speaking turns.
- Purpose: Builds a timing interval without inventing source semantics.
- Failure if removed: An immediate second turn removes the visible timing contrast.

### inv-04

- Rule: Use one compact second speaking turn with minimal gesture; its meaning is an original instance variable.
- Purpose: Preserves the visible turn-taking structure while allowing new content.
- Failure if removed: A large performance or extra line turns the held exchange into a sketch montage.

### inv-05

- Rule: End on the first character's silent reaction with no additional speaking turn.
- Purpose: Lets the final visible reaction complete the timing pattern.
- Failure if removed: Additional speaking turns weaken the final hold.


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

- 开场双人中景建立稳定眼线
- 只保留一轮第一人说话
- 两轮之间有一次清楚停顿
- 第二人只说一轮且动作克制
- 结尾第一人无声反应且不再增加说话轮次

## Anti-Copy Boundary

- Friends
- Joey Tribbiani
- Chandler Bing
- Central Perk
- source dialogue and wardrobe

## Transfer Tests

1. Two original night guards sit in a museum break room. One asks whether the marble statue blinked; after a pause the other says, 'Only when you look away,' and the first guard silently turns toward the dark gallery.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. Two lighthouse keepers share tea. One asks whether the foghorn ever gets lonely; after a pause the other answers, 'It calls everyone,' and the first keeper stops stirring.
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

## 结构分析（本地补写，非原文）

inv-01 开场双人中景建立稳定眼线——EP001 起始帧已锁住双人构图；inv-03 两轮之间一次清楚停顿——现有 00:00.3–00:01.6 有部分兑现；**inv-05 结尾第一人无声反应、不再加说话轮次——现稿以她 00:08.2「谢谢」＋搭肩收尾，角色D没有无声反应，这是可补的一条**。反复制边界里的原剧角色/咖啡馆不得带入。

## 使用边界

原卡是喜剧结构，不是分镜模板；镜头数量按题材定。inv-05 若与目标剧情冲突（必须台词收尾），显式记录偏离，不要偷偷删掉不变量。

- 卡里的不变量是**该案例条件下观察到的结构**，不是全局禁令；按语料库纪律，不把个案升级成"所有镜头必须如此"。
- 本条目的结构分析与适用边界是本地补写，不属于 T8 原文；引用时请区分。
