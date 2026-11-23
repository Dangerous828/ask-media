# direct-seedance-minimalist-product-ad

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-seedance-minimalist-product-ad
description: Turn real product images and a verified brief into a clean Seedance 2.0 minimalist product film. Use for 4–15 second e-commerce or launch ads that require faithful product color/material/geometry, independent anchor-image roles, product-specific actions, restrained camera, readable integrated copy, sound, and a stable closing frame; not for talking-head ads or invented product features.
---

# Direct Seedance Minimalist Product Ad

Direct an elegant product film around real form and behavior, not a generic white-tech template. This is a T8-authored companion to the MiniMax repository-bundled `minimalist-product-ad-generator`; use the upstream Skill for H3.

## Workflow

1. Confirm usable product images, variant, main color, material, ratio, 4–15 second duration, visual direction, and visible-copy mode.
2. Record only visible or user-confirmed product facts. Stop if the source material cannot protect identity and geometry.
3. Choose a product-specific spine: launch reveal, feature touch, or color family.
4. Define a motion language driven by real edges, mechanisms, highlights, variant motion, or silhouette matches.
5. Use separate reference images for hero identity, material/mechanism detail, and optional final composition; never treat a grid as a video storyboard.
6. Keep copy sparse. Lock exact words, single-line layout, readable contrast, and entry behavior before compiling.
7. Build and audit the prompt with `references/template.md`.

## Seedance rules

- Assign each `图片N` one narrow role and bind the product explicitly in the prompt.
- Preserve original product body color, finish, proportions, ports, controls, packaging, and variant identity.
- Use consecutive `镜头N` blocks for distinct proof beats, without exact time ranges.
- Keep one primary product action and one coherent camera move per shot.
- Put exact requested copy in `【...】`; reduce copy frequency when rendering risk is high.
- Put tactile/product sound in `<...>` and music in `（...）` only when requested.
- Never use H3 fields, H3 reference labels, or timestamp alignment.

## Boundaries

Do not recolor the product, invent a mechanism, fabricate a logo, or call paid generation without approval. Do not import this upstream entry into ComfyUI.

## Deliver

Return the product fact sheet, anchor roles, narrative spine, copy lock, final Seedance prompt, and fidelity/readability audit.
````

### summary.md

````text
# Seedance 2.0 极简产品广告

## 摘要

把真实产品图片与核验后的简报转成极简产品片，保护颜色、材质、几何、接口与机构细节。动作和运镜由产品本身驱动，文案少而可读，结尾保持稳定商品构图。

## 使用方法

提供产品主图、细节图、可选结尾构图、变体、材质、可证实功能、画幅、时长与精确文案。Skill 会为每张图片指定单一职责，再输出 Seedance 2.0 产品证据链。

## 适用范围

- 电商、产品发布、颜色系列与材料/机构展示。
- 不用于口播广告、虚构功能、假参数或廉价通用科技舞台。
- H3 使用官方仓库 `minimalist-product-ad-generator`；本 Skill 不导入 ComfyUI。
````

### template.md

````text
# Seedance minimalist product-ad template

## Product lock

```text
Product: [category + distinctive geometry]
Main variant/color: [exact source value]
Material/finish: [visible source facts]
Mechanism/action: [only visible or confirmed behavior]
Style: [white-tech / dark rim light / brand color field / light lifestyle]
References: 图片1=hero identity; 图片2=material/mechanism; 图片3=final composition/copy style
Copy: [exact 3–5 word line or none]
```

## Prompt skeleton

```text
镜头1：[product@图片1]以最有识别度的角度完成[real product-led reveal]，保留[exact color/material/geometry]；[restrained camera move]与干净负空间建立高级感，<subtle product sound>。
镜头2：通过[mechanism/detail@图片2]展示一个可验证的材质或功能证据；高光沿真实边缘移动，镜头只做一个连贯微距/横移行为。需要文案时只出现一行【exact copy】，字色与背景对比清楚。
镜头3：产品进入[stable closing composition@图片3]，主型号优先、其他型号仅作支持；完整一行【exact final copy】稳定可读，产品与文字都不被遮挡，音乐/声音克制收束。
约束：产品颜色、比例、开口、按钮、接口、材质和包装一致；不生成网格、分屏、锚定图版式、镜面廉价舞台、假Logo、假参数或多行字幕。
```

Remove any shot or copy event that the duration cannot support.

## Audit

- Product facts and movements are source-backed.
- Reference images are independent roles, not sequential panels.
- Each beat proves something new and the closing frame holds cleanly.
- Copy is exact, single-line, sparse, contrasted, and not subtitle-like.
- No shot timestamp or H3 syntax remains.
````

