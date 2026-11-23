# Agent Skills · 影像创作与方法论

一套给 AI Agent 用的技能（skills），覆盖从短剧剧本到出图、出视频、验收、剪辑的完整影像链路，外加写作与设计类通用技能。

技能格式遵循常见的 `SKILL.md`（YAML frontmatter + Markdown 正文）约定，可被支持该格式的 Agent 直接加载。

## 目录

入口是 `ask-media/SKILL.md`——影像任务先读它选路。它把工作分成 11 个阶段（开发 → 剧本 → 资产 → 导演 → 场记 → 分镜 → 图片词 → 视频词 → 生产 → 验收 → 剪辑交付），每个阶段指向对应的 owner 技能。阶段表由 `ask-media/chain.json` 生成，改阶段只改 JSON 再跑 `gen_table.py`。

主要技能：

- **链路入口**：`ask-media`、`creative-dna-cards`
- **短剧套件**：`drama-skills/`（第三方，MIT；12 个 `short-drama-*` 技能，管项目事实、阶段边界与连续性，实际位置在 `drama-skills/skills/*` 两层深）
- **静帧与分镜**：`doc-still-prompt`、`anim3d-still-pitfalls`、`storyboard-30s`、`short-film-scene-continuity`、`video-previs`
- **导演与表演**：`director-style-presets`、`acting-beats-dual-track`
- **视频提示词与闸门**：`h3-prompt-writing`、`h3-video-gate`
- **生产与验收**：`h3-queue`、`video-studio`、`concat-video`、`narration-route`
- **复刻**：`shortvideo-understand`（自研 skill；`lib/chubby_common` 复用 Chubby 代码，MIT）、`video-shot-reverse`
- **写作与设计**：`write-article`、`write-tweet`、`grab-article`、`humanizer`（第三方，CC BY-NC 4.0，**仅限非商业使用**）、`frontend-design`、`mobile-ios-design`、`mobile-android-design`、`tailwind-design-system`、`web-design-guidelines`

`AGENTS.md` 是根级路由与纪律约定。

## 安装

前提：一个支持 Agent Skills（`SKILL.md`）的客户端，例如 Claude Code、Codex、OpenCode、pi；部分脚本需要 Python 3.9+。用 `npx skills add` 安装需要 Node.js 22.20+（Node 20 会直接崩）。

### 方法一：skills 命令（推荐）

```bash
npx skills add Dangerous828/ask-media -y -g
```

`-g` 全局安装，所有目录可用；去掉 `-g` 则只装到当前目录。更新时重新执行同一条命令即可。

**注意**：`short-drama-*` 的 12 个技能嵌套在 `drama-skills/skills/*` 两层深，`npx skills add` 能否自动发现嵌套技能**未验证**。装完请核对：11 个阶段的全部 owner 技能（含 12 个 `short-drama-*`）都应出现在你的技能目录里；缺了就按方法二补第二轮软链。

### 方法二：手动链接

```bash
git clone https://github.com/Dangerous828/ask-media.git && cd ask-media
mkdir -p "$HOME/.claude/skills"

# 顶层技能：只链含 SKILL.md 的目录，排除 scripts/ 与 drama-skills/ 容器
# "$skill" 是 shell 变量（示例写法），不是仓库里的固定路径
for skill in */; do
  [ -f "$skill"/SKILL.md ] || continue
  ln -s "$PWD/$skill" "$HOME/.claude/skills/$skill"
done

# 嵌套技能：drama-skills 的 12 个 short-drama-* 单独一轮；11 个阶段每段都有一个 short-drama-* owner，漏装则每段都缺
for skill in drama-skills/skills/*/; do ln -s "$PWD/$skill" "$HOME/.claude/skills/$(basename "$skill")"; done
```

不同客户端的技能目录：

- Claude Code：`~/.claude/skills/<技能名>/`
- Codex：`~/.agents/skills/<技能名>/`（项目级用 `.agents/skills/`；`${CODEX_HOME:-$HOME/.codex}/skills/` 为旧版兼容路径）
- OpenCode：`~/.config/opencode/skills/<技能名>/`

每个技能都是独立安装单元，只用其中几个时，只链接对应目录即可。

### 入口与环境

- 影像任务先读 `ask-media/SKILL.md` 选路，再按阶段读对应的 owner 技能。
- 需要额外环境的技能：`video-previs` 需要智谱 GLM API Key（`ZHIPUAI_API_KEY` 或 `GLM_API_KEY`）；`h3-queue` / `video-studio` 需要本地 ComfyUI + h3q 生产队列，不附带；`shortvideo-understand` 需要 yt-dlp。其余技能多为纯文档，直接可用。

## 模型栈

作者实际运行这套技能的模型组合（技能描述方法与判据，不绑定任何特定模型，均可按各技能的环境变量替换为自己的）：

- **Agent 运行**：桌面 Agent（Alma）经本地聚合网关路由多家模型——日常对话、文档写作与路由判读用 flash 档快模型，跨文档联动与双轴审查等重活用旗舰档。
- **视频生成**：MiniMax H3（H3-Video）。本地 ComfyUI 经 h3q 队列串行提交，模式含 Ref2VA（参考图）、I2VA（首帧）、FL2VA（首尾帧）、Multishot（多窗一次生成），档位与帧网格见 `h3-queue/`。
- **图像生成**：本地 Qwen Image 2.1 为主（Qwen Research License，仅限研究与评估，商用需另行向 Qwen 申请许可）；H3-Image 作独立出图引擎（`--refine-denoise > 0` 时追加二次采样；MiniMax-H3-Image Community License）；云端混元（OpenAI-compatible 接口）作无 GPU 时的补充通道。参数档位见下方「出图口径」。
- **画质增强**：SeedVR2 事后超分与 latent 放大（`h3_upscale_video`，成品帧回编码、不重采样）。
- **语音转写**：本地 whisper-large-v3（Apple Silicon 权重），全程离线零上传。

## 出图口径

档位口径的权威链、「不写数字」的边界与例外都在 [AGENTS.md](AGENTS.md) 的「档位事实的权威链」段，本节不复述；实读入口见 [`still-api-params.md`](h3-queue/references/still-api-params.md)，带日期的档位实测快照见 [`still-standard-tier-20261105.md`](h3-queue/references/still-standard-tier-20261105.md)。

## 说明

这是从内部技能库整理出的公开版本，仅包含通用方法论：

- 内部项目名、路径、主机名与用户名已替换为占位符（如 `<渲染机脚本目录>`、`角色A-D`、`example-project`）；实测记录保留测量数值本身。
- 部分文档引用的渲染机脚本（`h3qc.py` 等）与内部工程档案不在本仓库中，文中已注明。
- 完整能力依赖具体运行环境；文档描述方法与判据，不附带这些环境配置。
- 文档引用可用 `scripts/check_references.py` 校验（退出码 0 表示全部引用可解析）。它的口径：markdown 链接**按相对本文件**解析，不写 `../` 就判断链；反引号里的路径允许仓库根写法；不做「同名兜底」——只写文件名不写路径算断链，必须写清相对路径。脚本会打印跳过了多少条（占位符 / 项目产物 / 无斜杠提及 / 上游夹具）以及整份豁免的文件类别，所以「0 断链」不等于「每个引用都验过」。
- 「`<文件>` §N」式的编号指向用 `scripts/check_section_refs.py` 校验：它打开目标文件确认里面真有 §N 这个标题。删节、改节号之后指针会指向不存在的编号，而文件本身仍是存在的——上面那个脚本查不出来。

## 许可

- 本仓库自有技能：[MIT License](LICENSE)，Copyright (c) 2026 Dangerous828。
- 随仓附带的三方技能保留各自许可：
  - `drama-skills/`：MIT，Copyright (c) 2026 drama-skills contributors。本地改写分叉，上游 [zenstory-ai/drama-skills](https://github.com/zenstory-ai/drama-skills)（上游最新 v0.13.0 / commit 7fed9df，2026-11-22）；本仓 vendored 于 2026-11-02（收编时点，此后为本地改写分叉），同步上游前先比对上游 CHANGELOG。
  - `shortvideo-understand/`：自研 skill；`lib/chubby_common` 复用 Chubby 代码（MIT，Copyright (c) 2026 Chubby）。
  - `humanizer/`：CC BY-NC 4.0，Copyright (c) 2026 shiujan，仅限非商业使用；商用授权见 [lieflat.work](https://lieflat.work/skills/less-ai-tone/)。
  - `frontend-design/`：Apache-2.0，来源 [anthropics/skills](https://github.com/anthropics/skills)。
  - `web-design-guidelines/`：上游 MIT（[vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines)），已随 vendored 核实，与 frontmatter `license: MIT` 一致。
- MiniMax 官方文档逐字节转载：`video-studio/references/official/base-en.txt`、`video-studio/references/official/ref-en.txt`、`h3-prompt-writing/references/base-en.txt`、`h3-prompt-writing/references/ref-en.txt` 转自 [MiniMax-AI/MiniMax-H3](https://github.com/MiniMax-AI/MiniMax-H3) 官方 skill（`base-en.txt` 222 行、SHA256 前 12 位 `2cfebc096a6e`；`ref-en.txt` 341 行、`1e574f356716`）。MiniMax-H3 仓库无 LICENSE 文件、GitHub license 字段为空（2026-11-23 经 API 核实），社区常见 Community License 声明属模型权重层面、未见覆盖仓库文档的明文条款；此处转载保留原文并署名来源，如上游后续发布文档许可条款，以之为准。原先照搬的官方索引 `h3-prompt-writing/OFFICIAL_SKILLS_INDEX.md` 已改写为本仓本地索引，仅保留官方仓库绝对链接。
