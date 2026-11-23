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

## 安装

前提：一个支持 Agent Skills（`SKILL.md`）的客户端，例如 Claude Code、Codex、OpenCode、pi；部分脚本需要 Python 3.9+。

### 方法一：skills 命令（推荐）

```bash
npx skills add Dangerous828/ask-media -y -g
```

`-g` 全局安装，所有目录可用；去掉 `-g` 则只装到当前目录。更新时重新执行同一条命令即可。如果该命令找不到技能，改用方法二手动链接。

### 方法二：手动链接

```bash
git clone https://github.com/Dangerous828/ask-media.git && cd ask-media
mkdir -p "$HOME/.claude/skills"
for skill in ask-media video-studio video-previs h3-queue h3-prompt-writing h3-video-gate; do
  ln -s "$PWD/$skill" "$HOME/.claude/skills/$skill"
done
```

不同客户端的技能目录：

- Claude Code：`~/.claude/skills/<技能名>/`
- Codex：`${CODEX_HOME:-$HOME/.codex}/skills/<技能名>/`
- OpenCode：`~/.config/opencode/skills/<技能名>/`

每个技能都是独立安装单元，只用其中几个时，只链接对应目录即可。

### 入口与环境

- 影像任务先读 `ask-media/SKILL.md` 选路，再按阶段读对应的 owner 技能。
- 需要额外环境的技能：`video-previs` 需要智谱 GLM API Key（`ZHIPUAI_API_KEY` 或 `GLM_API_KEY`）；`h3-queue` / `video-studio` 需要作者本地的 ComfyUI + h3q 生产队列，不附带；`shortvideo-understand` 需要 yt-dlp。其余技能多为纯文档，直接可用。

## 说明

这是从内部技能库整理出的公开版本，仅包含通用方法论。项目实测数据、内部路径与客户相关信息已移除，因此部分文档中的"实测记录"引用的是脱敏后的示例标识。

部分技能的完整能力依赖具体运行环境（本地 GPU 队列、特定 API 等）；文档描述方法与判据，不附带这些环境配置。

## 许可

- 本仓库自有技能：[MIT License](LICENSE)，Copyright (c) 2026 Dangerous828。
- 随仓附带的三方技能保留各自许可：
  - `drama-skills/`：MIT，Copyright (c) 2026 drama-skills contributors（上游 [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills)）
  - `shortvideo-understand/`：MIT，Copyright (c) 2026 Chubby
  - `humanizer/`：CC BY-NC 4.0，Copyright (c) 2026 shiujan，仅限非商业使用；商用授权见 [lieflat.work](https://lieflat.work/skills/less-ai-tone/)
