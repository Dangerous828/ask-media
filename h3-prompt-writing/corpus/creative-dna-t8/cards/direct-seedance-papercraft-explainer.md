# direct-seedance-papercraft-explainer

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-seedance-papercraft-explainer
description: Design a Seedance 2.0 science, education, or general-knowledge explainer using layered handmade papercraft, miniature diorama depth, physical paper mechanisms, clear knowledge beats, restrained miniature camera, tactile sound, and stable reference roles. Use for one 4–15 second clip or a longer multi-clip plan; not for flat vector cartoons, live action, or paper-texture-only styling.
---

# Direct Seedance Papercraft Explainer

Make an abstract mechanism feel physically built and teachable. This is a T8-authored companion to the MiniMax repository-bundled `papercraft-stop-motion-explainer`; use the upstream Skill for H3.

## Workflow

1. Lock the topic, audience, core learning sentence, ratio, total duration, and requested deliverable.
2. Choose one visual metaphor: pop-up journey, paper lab, layered cross-section, miniature nature theater, or mechanism board.
3. Design only the characters that improve explanation. Define their paper construction and limited gesture system.
4. Build the stage from foreground, midground, background, and far-background planes. Give every moving element a physical paper mechanism.
5. Split knowledge into causal beats. A 15-second clip normally supports about three or four readable changes; longer work becomes multiple clips of at most 15 seconds.
6. Assign reference images narrow character, scene, mechanism, or style roles and compile.

## Seedance rules

- Bind every recurring character/model to its declared image when supplied.
- Describe cardboard thickness, fibers, folds, seams, tabs, brads, sliders, rotating discs, pull-tabs, layer shadows, and settling.
- Use `镜头N` only for new knowledge states; do not add exact per-shot time ranges.
- Prefer locked, macro, top-down, slow push, or lateral parallax camera behavior—one coherent move per shot.
- Put exact requested labels in `【...】`, speech in `{...}`, tactile sound in `<...>`, and music in `（...）`.
- No H3 fields, H3 labels, timestamp alignment, plastic CG, liquid morphing, or physics-free motion.

## Boundaries

Do not generate media before the plan and references are approved. Do not import this upstream entry into ComfyUI.

## Deliver

Return the learning/metaphor lock, stage and mechanism plan, clip breakdown, Seedance prompt per clip, sound plan, and educational/material/continuity audit.
````

### summary.md

````text
# Seedance 2.0 纸艺定格科普

## 摘要

用分层纸雕、纸偶、纸板机构和微缩景深解释科学、教育或通识内容。知识因果必须由可见拉片、转盘、铰钉、折页或滑轨演示，而不是只给画面贴纸张纹理。

## 使用方法

提供主题、受众、记忆句、视觉模型、角色/场景参考、总时长和画幅。Skill 会设计舞台层次、纸艺机构和知识节拍，并在超过 15 秒时拆成可衔接片段。

## 适用范围

- 科普、教育、机制说明与手工微缩舞台短片。
- 不用于平面矢量动画、实拍或只做纸纹滤镜。
- H3 使用官方仓库 `papercraft-stop-motion-explainer`；本 Skill 不导入 ComfyUI。
````

### template.md

````text
# Seedance papercraft explainer template

## Learning lock

```text
Topic: [preserve domain words]
Audience: [...]
Memory sentence: [one sentence]
Visual metaphor: [paper model/mechanism]
Character/model bindings: [图片N -> one role each]
Stage planes: [foreground / midground / background / far background]
Mechanisms: [tab, brad, slider, disc, fold, page, rail]
```

## Prompt skeleton

```text
镜头1：[paper character/model binding]在四层微缩纸艺舞台中建立[knowledge object]；前景纸片轻微遮挡，中景承载核心模型，背景和远景沿纸轨产生细小视差；镜头[one miniature move]，<paper/cardboard sound>。
镜头2：[physical trigger]推动[tab/slider/disc/fold]，纸模型以分步、轻停顿、微回弹的方式显示[causal explanation]；需要标签时只出现已确认的【exact short label】，镜头保持可读。
镜头3：模型打开/分层/对齐，清楚展示[example or consequence]；角色用一个有限手势指向结果，纸层压平并稳定。
镜头4：[memory sentence visualized as final physical state]，构图与光线收束，纸张摩擦与轻敲声结束。
约束：所有物体由可见厚度的纸和纸板构成；纤维、折痕、接缝、切边、实体投影和分层视差稳定；动作逐帧、物理可信；无塑料CG、平面矢量背景、液体变形、高速环绕、无关文字Logo水印。
```

Use fewer shots when the learning path is simpler. Put multi-clip editorial timing outside the generation prompt.

## Audit

- Each shot teaches one new state and preserves the domain meaning.
- Depth planes and paper mechanisms visibly support explanation.
- Labels are short, approved, stable, and not used as a substitute for animation.
- Motion has stepped manipulation, pause, rebound, and settle.
- No clip exceeds 15 seconds; no exact shot timestamps or H3 grammar remain.
````

