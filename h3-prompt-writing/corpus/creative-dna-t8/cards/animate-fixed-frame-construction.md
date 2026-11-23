# animate-fixed-frame-construction

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: animate-fixed-frame-construction
description: "Create original short videos using the 固定机位｜从线稿生成成品 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 固定机位｜从线稿生成成品

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 构图锁定
- 同一对象连续成长
- 至少四个不可逆阶段
- 终态有轻微活化动作

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
# 固定机位｜从线稿生成成品 — 摘要

## 用途

锁定构图，用不可逆的制作阶段让同一对象从草图逐步成为成品。

## 推荐输入格式

`对象 + 固定构图 + 4个不可逆制作阶段 + 终态小动作`

## 可直接改写的简短示例

> 固定正面构图中的纸艺灯塔：铅笔轮廓、纸片立体搭建、色彩与纹理完成、内部灯光点亮，最后纸浪轻轻摆动。

## 必须保留的结构锚点

- 构图锁定
- 同一对象连续成长
- 至少四个不可逆阶段
- 终态有轻微活化动作

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 固定机位｜从线稿生成成品 Template

## Mechanism

A fixed composition turns creation into a readable causal ladder: low-commitment guides establish geometry, committed structure locks it, material finish adds specificity, contextual details certify completion, and one restrained in-medium motion supplies the final surprise.

## Invariants

### inv-01

- Rule: Lock the camera and reserve stable spatial zones before any marks appear.
- Purpose: Makes every later change comparable and cumulative.
- Failure if removed: If framing or layout drifts, the viewer reads a montage of replacements instead of one object making itself.

### inv-02

- Rule: Progress from low-commitment guides to committed structure to material colour or finish.
- Purpose: Creates a legible hierarchy of decisions rather than random simultaneous growth.
- Failure if removed: If finish arrives before structure, the transformation becomes visual noise and loses causal clarity.

### inv-03

- Rule: Delay secondary labels, studies or context until the hero form is already readable.
- Purpose: Extends retention without competing with the main reveal.
- Failure if removed: If every region activates at once, attention fragments and no milestone feels complete.

### inv-04

- Rule: End with one subtle motion that remains faithful to the finished medium while the support stays inert.
- Purpose: Adds an impossible payoff without breaking the artifact illusion.
- Failure if removed: Large three-dimensional motion or support movement turns the elegant category break into an unrelated VFX gag.


## Variable Slots

| Slot | Constraint |
|---|---|
| support | One stable physical or graphic surface with reserved hero and context zones. |
| hero_subject | A single dominant form readable first as guides, then structure, then finish. |
| representation_ladder | Three visibly distinct commitment stages appropriate to the chosen medium. |
| context_details | Two to four secondary marks or diagrams that arrive only after the hero reads. |
| finish_palette | A restrained palette that clarifies material stages. |
| living_idle | One small loop or response that does not leave or volumize the surface. |
| sound_ladder | Material sounds change with each process stage, followed by one payoff accent. |

## Required Human-Facing Anchors

- 构图锁定
- 同一对象连续成长
- 至少四个不可逆阶段
- 终态有轻微活化动作

## Anti-Copy Boundary

- the source bird species, pose, branch and natural-history subject
- the antique two-page folio, exact plate geometry and wooden tabletop
- source handwriting, taxonomic wording, plate number and page marks
- the exact timecode pattern, colour placement, final blink and tail gesture

## Transfer Tests

1. On a dark architectural blueprint, graphite planning arcs become precise white linework, cyan and amber system zones illuminate, tiny legend symbols populate the margin, and one printed status light begins pulsing while remaining flat ink.
   - Preserved: inv-01, inv-02, inv-03, inv-04
   - Changed: support, hero_subject, representation_ladder, context_details, finish_palette, living_idle
2. A square ceramic mural begins as charcoal registration marks, gains cobalt outlines, then mineral glazes flood a geometric koi design; small border motifs appear last and the painted water rings ripple once without leaving the tiles.
   - Preserved: inv-01, inv-02, inv-03, inv-04
   - Changed: support, hero_subject, representation_ladder, context_details, finish_palette, living_idle, sound_ladder

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

