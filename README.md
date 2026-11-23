# Agent Skills · 影像创作与方法论

一套给 AI Agent 用的技能（skills），覆盖从短剧剧本到出图、出视频、验收、剪辑的完整影像链路，外加写作与设计类通用技能。

技能格式遵循常见的 `SKILL.md`（YAML frontmatter + Markdown 正文）约定，可被支持该格式的 Agent 直接加载。

## 目录

入口是 `ask-media/SKILL.md`——影像任务先读它选路。它把工作分成 11 个阶段（开发 → 剧本 → 资产 → 导演 → 场记 → 分镜 → 图片词 → 视频词 → 生产 → 验收 → 剪辑交付），每个阶段指向对应的 owner 技能。阶段表由 `ask-media/chain.json` 生成，改阶段只改 JSON 再跑 `gen_table.py`。

主要技能：

- **链路入口**：`ask-media`
- **短剧套件**：`drama-skills/`（12 个 `short-drama-*` 技能，管项目事实、阶段边界与连续性）
- **静帧与分镜**：`doc-still-prompt`、`anim3d-still-pitfalls`、`storyboard-30s`、`video-previs`、`director-style-presets`
- **视频提示词与闸门**：`h3-prompt-writing`、`h3-video-gate`
- **生产与验收**：`h3-queue`、`video-studio`、`concat-video`、`narration-route`
- **复刻**：`shortvideo-understand`、`video-shot-reverse`
- **写作与设计**：`write-article`、`write-tweet`、`humanizer`、`grab-article`、`frontend-design`、`mobile-ios-design`、`mobile-android-design`、`ui-ux-pro-max`、`tailwind-design-system`、`web-design-guidelines`

`AGENTS.md` 是根级路由与纪律约定。

## 说明

这是从内部技能库整理出的公开版本，仅包含通用方法论。项目实测数据、内部路径与客户相关信息已移除，因此部分文档中的"实测记录"引用的是脱敏后的示例标识。

部分技能的完整能力依赖具体运行环境（本地 GPU 队列、特定 API 等）；文档描述方法与判据，不附带这些环境配置。
