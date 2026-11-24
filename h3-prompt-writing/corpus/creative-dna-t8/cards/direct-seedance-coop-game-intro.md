# direct-seedance-coop-game-intro

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: direct-seedance-coop-game-intro
description: Design a Seedance 2.0 two-player co-op game menu or opening animation with stable character bindings, approved visual direction, readable UI copy, coordinated palette, explicit interaction events, and a clean final menu state. Use for game concepts and character-led social intros; not for playable game development or copying commercial game branding.
---

# Direct Seedance Co-op Game Intro

Create a two-character menu animation without identity swaps or illegible UI. This is a T8-authored companion to the MiniMax repository-bundled `co-op-game-intro-generator`; use the upstream Skill for H3.

## Workflow

1. Collect player names, game title, ratio, duration, visual style, and optional character references.
2. Lock each character with a unique label, image binding, screen side, palette accent, silhouette, hairstyle, outfit, and pose.
3. Draft one approval frame externally when the user needs visual confirmation. Treat it as layout/style guidance, not an undeclared exact frame guarantee.
4. Verify every requested UI string before prompt writing. Reduce copy if it cannot remain readable.
5. Plan a short interaction chain: idle state → focus change → selection/confirmation → resolved co-op state.
6. Compile; keep character, UI, palette, and screen geography stable.

## Seedance rules

- Bind `玩家A@图片1` and `玩家B@图片2` when character images are supplied. Give an approved menu image a separate layout/style role.
- Use `【...】` for exact menu strings and `{...}` only for spoken dialogue.
- Use one primary camera behavior; menu readability normally favors a locked or restrained camera.
- Use `镜头N` only for real event changes. Never add exact per-shot seconds.
- Do not emit H3 fields, `<Picture N>`, `[Shot N]`, or retention syntax.

## Boundaries

Do not imitate a commercial logo, invent a franchise, or call paid generation without approval. Do not import this upstream entry into ComfyUI.

## Deliver

Return the identity map, UI-copy lock, event chain, final Seedance prompt, and an identity/readability audit.
````

### summary.md

````text
# Seedance 2.0 双人游戏开场

## 摘要

制作两位角色参与的合作游戏菜单或开场动画，重点防止身份互换、位置漂移和 UI 乱码，并用可见的选择与确认反馈形成完整事件。

## 使用方法

提供两位角色素材、玩家名、游戏标题、菜单文字、画幅、时长、色彩和界面方向。Skill 会锁定角色身份、屏幕位置、配色与 UI 层级，再输出 Seedance 2.0 镜头结构。

## 适用范围

- 双人合作概念片、角色社交开场、菜单动效与就绪画面。
- 不负责可玩游戏开发，也不复制商业游戏品牌或未授权角色。
- H3 使用官方仓库 `co-op-game-intro-generator`；本 Skill 不导入 ComfyUI。
````

### template.md

````text
# Seedance co-op game intro template

## Lock sheet

```text
玩家A@图片1: [identity anchors], left/right position, accent color, outfit
玩家B@图片2: [identity anchors], opposite position, accent color, outfit
图片3: [optional approved menu layout/style only]
Title/player/UI text: [exact approved strings]
Palette: [main, UI body, text, functional accent, danger accent]
```

## Prompt skeleton

```text
镜头1：16:9 游戏主菜单构图，玩家A@图片1与玩家B@图片2保持各自身份、服装、位置和色彩绑定。界面层级清晰，出现已确认标题【...】与玩家名【...】【...】。角色做轻微待机动作，镜头稳定。
镜头2：焦点框沿菜单移动到已确认按钮【...】，按钮产生克制的按压、亮边和确认反馈；两位角色的目光与姿态同步响应，<清晰菜单确认音>。
镜头3：界面进入已确认的合作就绪状态，玩家卡和主按钮保持可读，角色完成互补的庆祝动作，构图稳定收束。
约束：两位玩家不可互换、复制或融合；所有菜单文字只使用已确认内容；不新增 Logo、按钮、数值或商业游戏元素；UI 不遮挡脸部。
```

Adapt shot count to the actual event chain. Avoid camera movement when it harms UI readability.

## Audit

- Character labels, screen sides, wardrobe, and palette accents never swap.
- Every visible string is approved and wrapped once in `【...】`.
- UI state changes are causally visible.
- No exact shot timestamps or H3 grammar remains.
````

