# direct-seedance-brand-promo

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-seedance-brand-promo
description: Build a Seedance 2.0 brand, product, website, app, shop, or personal-project promo from verified assets and claims. Use when the user needs a truthful 4–15 second reel with a clear hook, product proof, controlled typography, camera, sound, CTA, and provenance-aware asset roles; not for inventing claims or imitating unavailable brand marks.
---

# Direct Seedance Brand Promo

Create a product-specific promotional short rather than a generic effects reel. This is a T8-authored companion to the MiniMax repository-bundled `brand-promo-video-generator`; use the upstream Skill for H3.

## Workflow

1. Confirm the official/user-provided assets, campaign goal, audience, channel, ratio, duration, copy language, CTA, and required disclaimers.
2. Build a truth sheet containing exact names, features, claims, UI states, product appearance, colors, logo rules, and source notes.
3. Reject or omit anything that cannot be verified. Never redraw an unavailable logo or fabricate a metric.
4. Select one story spine: intent-to-result, interaction-to-proof, problem-to-outcome, or image-to-benefit.
5. Plan only the beats that fit 4–15 seconds. Each beat must reveal new product evidence.
6. Assign every generation asset one narrow role and compile.
7. Show the pre-production card before any paid generation or upload.

## Seedance rules

- Bind products, people, UI, or mascots to declared images when references are supplied.
- Keep one primary action per shot; use product edges, cursor paths, UI flow, light, or matched geometry for transitions.
- Use consecutive `镜头N` blocks only when the reel has multiple distinct events. Do not put exact per-shot timestamps in the prompt.
- Put requested visible copy in `【...】` exactly. Keep it short and readable; omit copy rather than inventing it.
- Put physical/UI sound in `<...>`, dialogue in `{...}`, and music in `（...）`.
- No H3 fields, H3 labels, retention analysis, or alignment syntax.

## Boundaries

Do not call generation, upload brand assets, or publish a campaign without explicit authorization. Do not import this upstream entry into ComfyUI.

## Deliver

Return the truth sheet, asset-role map, story spine, Seedance prompt, visible-copy list, and a final claim/identity/continuity checklist.
````

### summary.md

````text
# Seedance 2.0 品牌宣传短片

## 摘要

依据可核验的品牌、产品、网站、应用或个人项目素材，组织 4–15 秒宣传片。核心是把卖点变成可见的产品证据，控制品牌外观、UI、文案、声音与 CTA，拒绝虚构功能和指标。

## 使用方法

提供官方或自有素材、受众、渠道、时长、画幅、已确认卖点、精确文案和 CTA。Skill 会先建立事实表与素材职责，再选择叙事骨架并输出 Seedance 2.0 提示词。

## 适用范围

- 产品发布、网站/App 演示、店铺、个人项目与品牌 Reel。
- 不用于编造品牌声明、仿造不可用 Logo 或无证据的性能宣传。
- H3 使用官方仓库 `brand-promo-video-generator`；本 Skill 不导入 ComfyUI。
````

### template.md

````text
# Seedance brand promo template

## Truth and intent card

```text
Brand/product: [exact verified name]
Audience/channel: [...]
Promise: [one verified benefit]
Proof: [visible product interaction, UI state, output, or physical result]
Copy/CTA: [exact requested text]
Assets: [图片N/视频N -> identity, product, UI, action, camera, style, or continuity]
```

## 15-second-capable story spines

- Intent → product mechanism → useful output → proof → CTA.
- Hero reveal → interaction → feature macro → result → brand lockup.
- Context → process → evidence → outcome → promise.

Remove a beat when the duration cannot support it; never compress proof into decorative montage.

## Prompt skeleton

```text
镜头1：[brand hook with verified product/subject binding], [one clear action], [primary camera move], [brand palette and light], [sound].
镜头2：[the product mechanism or UI interaction visibly causes a result], [matched transition], [requested copy 【...】 only if readable].
镜头3：[concrete proof and stable hero composition], [CTA/brand lockup only from verified assets], [music/sound resolution].
约束：产品外形、颜色、材质、UI、人物和标识保持一致；不新增功能、指标、文案、Logo 或水印。
```

## Audit

- Every claim and visible word has an approved source.
- Every identity-bearing asset is declared and purposeful.
- Product motion causes visible evidence.
- Copy holds long enough to read and does not compete with the product.
- No exact shot timestamps or H3 syntax appears.
````

