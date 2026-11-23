# build-viewpoint-scale-spectacle-ladder

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: build-viewpoint-scale-spectacle-ladder
description: "Create original short videos using the 尺度奇观阶梯｜每镜重置参照再逼近 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 尺度奇观阶梯｜每镜重置参照再逼近

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Give each vignette an immediately familiar scale anchor.
- Use one dominant impossible silhouette per vignette.
- Increase proximity, not just nominal size.
- End with a viewpoint-level encounter that preserves spatial legibility.

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
# 尺度奇观阶梯｜每镜重置参照再逼近 — 摘要

## 用途

每个短段先重置熟悉视点与尺度参照，再让一个不可能的空中形态进入；通过观察距离与遮挡变化逐步逼近，最终以近距离视点遭遇收束。

## 推荐输入格式

`5个熟悉尺度参照 + 每镜1个巨型原创形态 + 视点变化 + 距离逐步缩短 + 近距离终态`

## 可直接改写的简短示例

> 五种原创巨型空中种子结构依次出现在风场、列车窗、采石场、温室与维护车视点中，每次距离更近，最后从车顶正上方掠过。

## 必须保留的结构锚点

- Give each vignette an immediately familiar scale anchor.
- Use one dominant impossible silhouette per vignette.
- Increase proximity, not just nominal size.
- End with a viewpoint-level encounter that preserves spatial legibility.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 尺度奇观阶梯｜每镜重置参照再逼近 Template

## Mechanism

Reset a familiar viewpoint and scale anchor in each vignette, introduce one impossible airborne form that preserves readable silhouette, vary observer distance and occlusion, then escalate proximity until the final viewpoint encounter feels immediate rather than merely larger.

## Invariants

### inv-01

- Rule: Give each vignette an immediately familiar scale anchor.
- Purpose: Makes the impossible size measurable.
- Failure if removed: A blank sky provides no scale proof.

### inv-02

- Rule: Use one dominant impossible silhouette per vignette.
- Purpose: Keeps the spectacle readable.
- Failure if removed: Several equal forms create visual noise.

### inv-03

- Rule: Change observer carrier or occlusion between vignettes.
- Purpose: Prevents a repetitive size montage.
- Failure if removed: Identical viewpoints flatten the ladder.

### inv-04

- Rule: Increase proximity, not just nominal size.
- Purpose: Creates a real escalation toward encounter.
- Failure if removed: Distant forms remain postcards.

### inv-05

- Rule: End with a viewpoint-level encounter that preserves spatial legibility.
- Purpose: Converts spectacle into immediate stakes.
- Failure if removed: An abstract final close-up loses the observer relationship.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair whose role is clear without source identity. |
| setting | A materially new setting with fixed spatial anchors and no source-specific location. |
| causal_carrier | One object, route, mark or device that visibly carries the causal chain. |
| state_change | Five ordered states with observable handoffs, not a decorative montage. |
| camera_grammar | A new proof-oriented information order that does not copy source shot boundaries. |
| payoff | A held final consequence that resolves or recontextualizes the setup. |
| sound_family | An original hierarchy of story-world cues supporting each visible change. |

## Required Human-Facing Anchors

- Give each vignette an immediately familiar scale anchor.
- Use one dominant impossible silhouette per vignette.
- Increase proximity, not just nominal size.
- End with a viewpoint-level encounter that preserves spatial legibility.

## Anti-Copy Boundary

- source giant whale, manta, nautilus, jellyfish and shark
- Shanghai skyline, airplane window, highway and car POV
- the exact animal order and city landmarks
- source blue atmospheric spectacle palette

## Transfer Tests

1. Five original airborne seed structures appear over a coastal wind farm, train window, quarry road, public greenhouse and maintenance rover; each new anchor shortens distance until a translucent seed sail crosses directly over the rover canopy.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family
2. Five enormous folded-paper weather instruments drift through an archive city, observatory window, tram corridor, plaza and bicycle POV, with increasing occlusion and a final near overhead pass.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, causal_carrier, state_change, camera_grammar, payoff, sound_family

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

