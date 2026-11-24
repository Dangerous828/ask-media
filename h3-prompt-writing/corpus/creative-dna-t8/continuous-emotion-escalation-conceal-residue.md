# 情绪压力曲线｜压抑、峰值、遮挡与残余 · Creative DNA 机制卡（T8）

- 验证状态：**外部案例机制，本地 h3q 未测**。原卡来自案例库，未在 MiniMax H3 本地通道出片验收；不得写成"通过配方"。
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）与 comfyui-minimax-h3-prompt-enhancer-T8（插件）。本条目收录的案例库原创摘要、机制说明与提示词模板依 **CC BY 4.0**（许可声明内联于各卡正文，本公开版不附单独文件）使用：署名 T8mars，附仓库链接，并说明本条目加入了中文结构分析与本地适用边界。仓库中的应用/公共校验代码为 MIT；ComfyUI 插件为保留全部权利，**未收录任何插件代码**。抓取日期 2026-11-17。
- 完整原文：下方 `` SKILL.md `` 与 `` template.md `` 为逐字收录，不改写；中文结构分析在原文之后。

## 什么时候查这张卡

委屈想哭、忍住、鼻音、哭出来、被逗笑前的情绪落地。对 EP004 007「委屈想哭·妈妈抱起」最直接。

## 完整原文 · SKILL.md

````markdown
---
name: continuous-emotion-escalation-conceal-residue
description: "Create original short videos using the 情绪压力曲线｜压抑、峰值、遮挡与残余 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 情绪压力曲线｜压抑、峰值、遮挡与残余

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
2. Treat these anchors as mandatory:

- Lock one adult portrait, background, lens distance and light for the complete performance.
- Accumulate at least three readable tension indicators without resetting earlier evidence.
- Place one brief self-protective concealment gesture after the peak and then reveal the face again.
- Hold visible emotional residue such as wet eyes, altered breath or gaze in the terminal state.

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

## 完整原文 · references/template.md

````markdown
# 情绪压力曲线｜压抑、峰值、遮挡与残余 Template

## Mechanism

Lock one adult portrait, background, lens distance and light so that performance changes remain directly comparable. Begin from a controlled emotional baseline, accumulate at least three small facial or breathing indicators without resetting them, resolve once into a single maximum expression, then use one brief self-protective concealment gesture. Reveal the face again and end with visible physiological or behavioral residue rather than restored neutrality. The reusable mechanism is calibrated baseline, cumulative restraint, single peak, protective concealment and residual recovery—not the source woman, face, earrings, grey garment, field background, tear pattern, exact expression, camera, timing, creator identity or unsupported model mapping.

## Invariants

### inv-01

- Rule: Lock one adult portrait, background, lens distance and light for the complete performance.
- Purpose: Makes microchanges comparable against a stable baseline.
- Failure if removed: Camera or lighting changes can impersonate emotional progression.

### inv-02

- Rule: Accumulate at least three readable tension indicators without resetting earlier evidence.
- Purpose: Builds a continuous pressure curve rather than disconnected expressions.
- Failure if removed: Independent face poses become an expression test.

### inv-03

- Rule: Use exactly one maximum expression after the restrained build.
- Purpose: Provides a clear emotional apex.
- Failure if removed: Repeated peaks flatten the arc into cycling.

### inv-04

- Rule: Place one brief self-protective concealment gesture after the peak and then reveal the face again.
- Purpose: Adds behavioral consequence while preserving proof of recovery.
- Failure if removed: Ending fully hidden removes the final performance evidence.

### inv-05

- Rule: Hold visible emotional residue such as wet eyes, altered breath or gaze in the terminal state.
- Purpose: Makes recovery physically credible.
- Failure if removed: Instant neutrality erases the cost of the peak.


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

- Lock one adult portrait, background, lens distance and light for the complete performance.
- Accumulate at least three readable tension indicators without resetting earlier evidence.
- Place one brief self-protective concealment gesture after the peak and then reveal the face again.
- Hold visible emotional residue such as wet eyes, altered breath or gaze in the terminal state.

## Anti-Copy Boundary

- the source woman's facial identity, hair, hoop earrings, grey garment and exact tear pattern
- the source open field background, overcast light, wind behavior, lens and crop
- the source lip, eye, cheek, crying, garment-cover and gaze sequence or exact timing
- the source beauty rendering, skin texture, framing, performance identity and character likeness
- the source creator identity, Seedance 2.5 claim, platform overlay, watermark and branding

## Transfer Tests

1. An adult rescue dispatcher in a fixed fluorescent control-room portrait holds composure through jaw tension, rapid blinking and a trapped breath, breaks once after hearing a safe-return confirmation, covers her mouth with one hand, then lowers it and ends with wet eyes and steadier breathing.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. An adult stage actor in a locked dressing-room mirror portrait suppresses laughter through cheek tension, nostril movement and a trembling lip, releases one full laugh, briefly hides behind a costume collar, then returns with flushed cheeks and residual smile breaths.
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

inv-02 累积至少三个不重置的紧张信号——剧本已有嘴角下拉、眼眶湿、肩抖、揉眼、鼻音，覆盖充分；inv-04 峰值后有一次短暂遮挡再露脸——现稿收在「脸埋妈妈肩上哭出来」，遮挡有了但**再露脸没有**；inv-05 结尾留生理残余——现稿未写。inv-01 要求锁景别／光位／镜头距离作基线，而 007 妈妈入画＋抱起、机位在动，情绪变化会被机位变化冒充，这是最大风险，需在分镜层先决定基线。

## 使用边界

原卡主体是成人肖像，套到一岁多幼儿时必须换成幼儿可见信号（下肢晃、攥衣、鼻音），不要照抄呼吸／咬唇等成人表演。可借的是五条不变量，不是原片的面部与时序。

- 卡里的不变量是**该案例条件下观察到的结构**，不是全局禁令；按语料库纪律，不把个案升级成"所有镜头必须如此"。
- 本条目的结构分析与适用边界是本地补写，不属于 T8 原文；引用时请区分。
