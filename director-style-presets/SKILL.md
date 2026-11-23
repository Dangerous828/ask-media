---
name: director-style-presets
version: 1.0.1
description: 仅当创作者点名某种导演风格或风格预设（港式警匪、写实冷峻、韦斯对称、张艺谋浓色、电影感写实、赛博霓虹、吉卜力式手绘、国风工笔、水墨、三幕结构、短剧爽点节奏）时，提供对应的镜头语言、生图介质或剧本节奏约束。未点名不使用；不写整帧提示词或分镜表（分别归 doc-still-prompt、short-drama-storyboard / storyboard-30s）；风格形容词不整串灌进 H3 视频提示词，H3 正文只写介质开场句。
---

# 导演风格预设

只做路由：创作者点名哪种风格，就读对应的 `references/<name>.md`，把约束交给正在写词或拆分镜的 owner。

## 铁律

1. **只在点名时用**：创作者没点名，任何风格都不自动套用。
2. **风格介质写进 H3 正文开场 1–2 句，风格形容词不堆砌进 H3**。H3 正文可写介质声明（官方范例即如此：`The target video is in realistic photographic style.`、`Pixar-inspired 3D cartoon rendering…`），但风格卡里的导演形容词（韦斯对称、张艺谋浓色等）属于生图与分镜层，不整串灌进视频提示词。风格也可由首帧/参考图推导。
3. **项目事实优先**：既有身份、服装配色、场景、光源事实与项目画风优先于风格；风格只调整取景、光色关系与节奏，不增删陈设、天气或光源设施。
4. **介质卡会改画风**：标"介质"的卡（cinematic-real、cyber-neon、ghibli-soft、gongbi-guofeng、ink-wash）会改变表现媒介。与项目既定画风不一致时，先向创作者说明冲突并取得确认；3D 动画项目通常不兼容 cinematic-real 与 ghibli-soft。
5. **doc-still 通路**：介质卡不替代 doc-still 所选分支的介质锚点与收尾词（跨分支混用判 no）；Slate 卡里的 negative 字段只在 Slate 生图通路使用，人体部位类排除词不得搬入 doc-still 正文或 negative。
6. **时长与镜数服从项目规格**：风格卡不另设固定秒数。

## 路由表

| 名称 | 类型 | 作用层 | 适用 | 3D 动画项目 | 文件 |
|---|---|---|---|---|---|
| 港式警匪 | 镜头语言 | 分镜 | 都市犯罪、商战 | 可用（只改镜头语言） | `references/hk-crime.md` |
| 写实冷峻 | 镜头语言 | 分镜 | 现实题材 | 可用（不改媒介） | `references/realism-cold.md` |
| 横平竖直对称 | 镜头语言 | 分镜/关键帧构图 | 轻喜剧、童话感 | 可用 | `references/wes-symmetry.md` |
| 浓色仪式感 | 镜头语言 | 分镜/关键帧构图 | 视觉冲击、仪式场面 | 可用 | `references/zhangyimou-color.md` |
| 电影感写实 | 介质 | 生图 | 真人短剧 | 不兼容 | `references/cinematic-real.md` |
| 赛博霓虹 | 介质 + 光色 | 生图 | 科幻、都市犯罪 | 需确认 | `references/cyber-neon.md` |
| 手绘动画（柔和） | 介质 | 生图 | 2D 漫剧、治愈系 | 不兼容 | `references/ghibli-soft.md` |
| 国风工笔 | 介质 | 生图 | 古风言情 | 需确认 | `references/gongbi-guofeng.md` |
| 水墨国风 | 介质 | 生图 | 古装、武侠、文艺 | 需确认 | `references/ink-wash.md` |
| 电影三幕 | 剧本结构 | 剧本/分集 | 电影、长片 | 与画风无关 | `references/three-act.md` |
| 短剧爽点节奏 | 剧本节奏 | 剧本/分集 | 红果系短剧 | 与画风无关 | `references/shortdrama-hook.md` |

## 用法

1. 确认创作者点名的风格与作用层（剧本 / 分镜 / 生图）。
2. 读对应 reference，按"写法"交给 owner：剧本层给 `short-drama-write` / `short-drama-develop`，分镜层给 `short-drama-storyboard`（短剧项目）或 `storyboard-30s`（独立短片），生图层给 `doc-still-prompt`。
3. 风格与项目事实冲突时列出冲突点，由创作者裁决，不自行改资产。

来源：Slate workbench/skills/hk-crime.md、workbench/skills/realism-cold.md、workbench/skills/wes-symmetry.md、workbench/skills/zhangyimou-color.md、workbench/skills/cinematic-real.md、workbench/skills/cyber-neon.md、workbench/skills/ghibli-soft.md、workbench/skills/gongbi-guofeng.md、workbench/skills/ink-wash.md、workbench/skills/three-act.md、workbench/skills/shortdrama-hook.md（原卡保持不动，Slate 运行时仍加载原卡）
