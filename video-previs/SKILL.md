---
name: video-previs
version: 1.0.3
license: MIT
description: >
  为对话/短剧场景做 2D 白模(animatic/blocking previs)：抽帧拉片+切点检测、
  台词提取（OCR烧录字幕 + ASR语音，两路并行）、storyboard JSON、自动正反打/越肩/
  特写/全景机位，直接出 MP4。两个入口：从剧本新建白模（人物形象未定时锁机位/走位/轴线/景别/节奏，
  产物用来写场记账），或对原片抽帧拉片、复刻/翻拍需逐镜原分辨率代表帧与切点证据。只写分镜文字、
  写提示词或生成关键帧时不用。奇观大场面不要用本技能，走 AI 概念图。
---

# video-previs — 2D 对白白模预演

白模是把镜头语言 + 台词，用确定性 2D 程序渲染成可播放预演。**只锁机位/走位/轴线/景别/节奏/台词，不做美术。**

白模是**人物形象未定时的占位模具**。这个阶段的人物只是方块与站位，不承担长相、妆造和身份；
它的任务是先在空间里把摄影机摆对、把人和物的走位走顺、把轴线和景别定下来。
人物形象定稿是后面的事，白模不等它。

## 何时用 / 不用
- 用：对话、短剧、室内对峙、采访、围坐等**固定机位人物关系镜头**。
- 不用：城市飞跃/爆炸/大场面（环境即镜头主体），交 AI 关键帧概念图。

## 白模是必需项，不是可选项

**哪怕只有一个场景，也必须建一个最基础的白模**：一个场景底 + 人物占位块 + 每镜一个机位。不需要美术、贴图或动作细节。

理由不是白模能提升画面，而是**后续 agent 会漂移**：分镜、静帧、视频提示词分属不同轮次，每轮都会重新理解一次"谁在桌子哪一侧、谁在谁左后、反光从哪个角度来"。文字数值能写对一次，不能保证三次都读成同一个意思。

判据：把任意两镜并排看，能不能立刻判断两人相对位置与机位方向前后一致。

不接受"单场简单、账里已经写了数值"作为跳过理由。确实存在技术障碍时，写明卡在哪一步、用什么代替核对，不能写成"没有额外价值"。

## 两条入口

### 入口 A：从剧本新建白模（准备阶段）

场景/地点资产出来之后、人物形象还没定的时候，用白模先锁空间。

1. 读已定稿剧本的目标场次：场景 ID、在场人物、对白、动作、场景时间。
2. 读该项目的地点资产，把地面、主光源、边界陈设、出入口落成 `set` 与必要道具；没有地点资产时，
   只用剧本写明的事实建最小空间，不自行编造家具。
3. 人物写成 `A` / `B` / `C` 这样的占位代号，**不写姓名、不写长相、不写服装细节**。
   站姿/坐姿、左右关系、谁面向谁按剧本动作定。
4. 按剧本与对白拆镜，机位用 `wide` / `near` / `two` / `cu` / `ots` 解析，不要手摆。
   需要固定高度或特殊取景时才写镜头级 `pos` / `look`。
5. 渲染前先校验 JSON，再出 MP4。

这条入口的产物**不是成片参考**，是拿来写场记账的：把白模里实际摆出来的机位类型、机位高度、
轴线侧、景别抄进 `设定集/场记.md`，并反向核对账本里写的值能不能在白模里摆出来。

### 入口 B：从已有视频拉片 / 复刻

见下文「流程」1–3：抽帧、切点、台词 OCR/ASR，产出代表帧与 storyboard JSON。
复刻/翻拍入口另见「流程」第 1 步的 `--rep-frames` 用法。

## 白模与场记账

场记（continuity breakdown）是准备阶段的核心工作，一部戏一本，写在 `设定集/场记.md`。
白模和它是**互相引用**的关系，不是先后替代：

| 方向 | 写什么 |
|---|---|
| 账 → 白模 | 场景空间账的地面/主光源/边界陈设/出入口 → `set` 与道具；调度卡的站位/朝向/姿态 → `actors.pos`、`staging`、`pose`；轴线侧与景别 → `cam` 选择 |
| 白模 → 账 | 每个镜头的「白模引用」行写清：白模工程、白模镜头 id、白模机位类型、核对状态 |

- 账里写的机位高度与轴线侧，必须能在白模里摆出来。摆不出来时，改白模或改账，并写下改了哪一边。
- 白模镜头 id 与场记账的调度卡 id 要能对上；改名或重排镜序时两边一起改。
- 一次只改被要求的那一镜；已经核过的镜不因为重命名而失效。

## 流程
### 1. 拉片（程序）
`python scripts/extract_shots.py <video> --start S --end E [--step 3] [--thresh 9]`
→ 接触印片 `frames_<名>/contact_*.jpg` + 打印切点区间。密集抽帧**人工归并**，定每镜景别/运镜/前后景/画左画右。

复刻/翻拍入口：`python scripts/extract_shots.py <video> --rep-frames <项目>/输入/原片/frames --prefix SRC-`
→ 在代表帧目录另产 `SRC-01.jpg` 等、`shots.json` 与 `原片拆解.md` 骨架。代表帧用 ffmpeg 从每镜中点按原分辨率解码，不缩放、不烧时间戳；骨架只填实测入出点与帧路径，其余均待核对。按 `short-drama` 的 `../drama-skills/skills/short-drama/references/video-remake.md` 把骨架接入 `项目开发/原片拆解.md` 并调整帧的项目相对路径；项目编排归 `short-drama`，媒体验收归 `short-drama-review`，本技能只产原片证据与白模预演。

### 2. 台词提取（ASR + OCR 两路并行，必须都做）
- **OCR 烧录字幕（首选，准）**：视频有内嵌字幕时
  `python scripts/extract_subtitles.py <video> --start S --end E`
  → `<名>_字幕.srt` + `_台词.txt`（带时间轴）。依赖 rapidocr（离线轻量）。
- **ASR 语音（补充）**：无字幕/对白超出字幕/需要听语气停顿
  `python scripts/extract_speech.py <video> --start S --end E --model small --lang zh`
  → `<名>_ASR.srt` + `_ASR_台词.txt`。依赖 faster-whisper（本地 CPU，首次下模型）。
  需要更快或更高精度时可加 `--engine cloud --vendor glm|doubao` 走云端 ASR；配置从工作区的 `<工作区>/workbench/providers.json` 读取（不在本仓），骨架见 `templates/providers.example.json`，填自己的端点与凭据，详见 `references/environment_setup.md` 第 4 节。默认本地链路不依赖该文件。
- **交叉校正规则**：
  - 有烧录字幕 → 以 **OCR 为准**（字幕是片方正本）；ASR 仅补字幕未覆盖的口语/停顿/笑声。
  - 无字幕 → 以 **ASR 为准**，可换 `--model medium/large-v3` 提精度。
  - 两路都产出**带时间轴的 SRT**；据每镜说话人特写镜头，把台词归属到 `speaker`。

### 3. 填 storyboard JSON
复制 `templates/dialogue_storyboard.template.json`，填 actors + shots（字段见 `references/storyboard_schema.md`）。
- shots 时长/切点用步骤1；`line/speaker` 用步骤2 的带时间轴台词对齐到镜头；
- 硬信息（切点、时长、景别、谁说的、画左画右）**从原片读，不猜**。

### 4. 渲染出片
- `python scripts/dialogue_engine.py <storyboard.json> out/白模.mp4`
- 引擎经 ffmpeg 管道直出 H.264/yuv420p/faststart，产物即通用编码，无需再转码。
  找不到 ffmpeg 会明确报错，不会用 mp4v 冒充成品；本机需先装 ffmpeg（见 references/environment_setup.md）。
- 抽帧与原片并排核对；只改 JSON 秒级重渲。

### 5. 深度动作捕捉（白模之后）
从原片生成深度/动作遮罩视频，用于校准走位、动作与景别：
- 深度图（首选，全场景近亮远暗，忠实模型输出）：
  `python scripts/motion_depth.py <video> --start S --end E --fps 12 --out 深度图.mp4`
  - 默认 `--enhance none`（忠实原始，不改远近关系）；需要时才 `--enhance stretch|clahe` 轻微提对比。
  - 可选 `--color inferno`（伪彩）、`--invert`、`--global-norm`（全段统一尺度）。
- 人像剪影（仅人物，备选）：`python scripts/motion_silhouette.py <video> --style gray|binary`
- 质量验证：`python scripts/depth_verify.py <深度.mp4>`（输出亮度分布/前景背景分离度/增强对照图）。
- 注意：单目深度在转场叠化帧、剧烈镜头运动处可能失真，以原始解读为准，不要默认拉伸/时序修改。

## 关键规则
- 相机由站位解析（wide/near/two/cu/ots），勿手摆；1:1 复刻才用显式 pos/look 或镜头级 staging/table。
- **一次只改被要求的那一镜，已确认镜头绝不修改。**
- 构图不对先查 blocking（谁左谁右、谁最近最大、围什么道具），再查机位。
- 输出一律 H.264/yuv420p。每步抽帧与原片并排自检。

## ⚠️ 预演图不是生产参考图（跨技能红线）

previs 产物（白模、2D 灰盒、贴图粗糙的 animatic、接触印片）**只能用于判断动作、走位、构图与切点**，
**绝不能当作 H3 / 出图模型的参考图或首帧**。原因：Ref2VA 的参考图会被强继承（`ref_image_size=match`），
白模里的占位方块、错误比例、缺角色、重复布景会被原样放大进成片。

真实事故：把预演合成图直接当 Ref2VA 参考送去生成，结果成片出现**两台电视、角色缺失、姿势全错**，
整批 5 镜判废。正确顺序是：previs 定动作与机位 → 用 Qwen 出**干净的关键帧** → 关键帧才进 reference。

判据：这张图自己能不能直接当剧照交付？不能，就不是生产参考图。

**这条红线也决定了白模的用途**：白模的产物是**写场记账的依据**，不是给生成用的图。
它提供的是可以抄成文字的那几项——机位类型、机位高度、轴线侧、景别、走位与切点；
这些值抄进 `设定集/场记.md` 之后，下游读的是账本，不是白模文件。

**抄进去还没完：实摆值与计划值不一样时，要一路传到下游。** 白模摆出来才发现原来写的
「1.15m 配俯视 12°」凑不出「中景双人」是常事；回写顺序（账本 → 分镜镜头语言行 → 分镜英文
正文机位句 → 已写的视频提示词 → 账本「未对齐项」，缺一份不算做完）以
[ask-media](../ask-media/SKILL.md) 的「白模 → ⑥⑦⑧」条为准，本节不复述。
**先写分镜、事后才建白模、然后不回头改下游，等于白模白做**——下游读的是账本，账本改了
而分镜没改，两边立刻打架（账本写「俯视 12°」、分镜写「平视」）。
所以白模不需要画得好看，需要的是位置和角度对；也不需要为了"看起来像成片"去补角色和美术。

## 深入
- `references/storyboard_schema.md`：JSON 字段与机位算法。
- `references/workflow.md`：从剧本建白模、拉片 vs 复刻、白模与场记账的对应、技术路线、经验。

## 引擎与校验
- 对白/短剧：`scripts/dialogue_engine.py`（自动正反打/越肩/特写/全景，支持镜内台词轨 lines[]、镜头级 staging/table、near 背影）。
  配套校验：`scripts/validate_dialogue.py <json>`（渲染前先校验 cam/角色引用/时长）。
- 走位/动作白模（含 path 走位、yaw+pitch 姿态）：`scripts/previs_engine.py`；配套校验 `scripts/validate_storyboard.py`。
- 分镜建议（台词→wide/ots/cu）：`scripts/plan_coverage.py`。
- 导出：`export_storyboard_xlsx.py`（Excel）、`export_dialogue.py`（带时间戳 srt/txt）。
- 一键：`run_dialogue_pipeline.py <json>`（校验→渲染 H.264→Excel→台词；校验失败即停）。

## 学习向产物
- 关键镜头讲解（为什么这么拍）按 `references/critical_shots_template.md` 三段式：叙事潜台词 / 场景美术 / 镜头语言动机 + 可迁移判断准则。

## 字段规范
- 对白白模完整字段见 `references/storyboard_schema.md`（cam/pos-look/staging/lines 等）。
- 从剧本建白模时，`id` 与「场记」调度卡 id 使用同一套编号，便于两边互查；机位高度写在 `pos` 的 y 值里，
  不要只靠 `cam` 类型隐含。

## 可视化工作台（dashboard）
- 入口：`dashboard/server.py`（自包含 Web 工作台）。默认端口 11872：启动 `python dashboard/launch.py 11872` 或 `python dashboard/server.py 11872`，浏览器开 http://127.0.0.1:11872 。服务只绑 127.0.0.1 回环、无鉴权，勿转发到公网。
- 功能：浏览 projects/ 各项目产物（拉片/台词/分镜/白模/讲解），点标签分阶段查看，文本卡内嵌全文+点击弹窗，视频支持 Range 拖动；后端 `/api/run` 调用本 Skill 脚本。
- 自包含：dashboard 自动向上查找 projects/，脚本优先用同 Skill 的 `scripts/`（详见 `dashboard/README.md` 的目录结构与新建方法），可独立运行。仓库不含 projects/，首次用前按 README 建 `projects/<项目名>/`，否则页面列表为空。

## 可选增强（需配置/外部程序）
- **3D 白模（Blender）**：scripts/blender_previs.py <json> 生成 Blender 构建脚本 gen_<slug>.py，经 Blender MCP/Blender 内执行，做真三维走位推演。配置见 references/environment_setup.md。
- **LLM/Vision（智谱 GLM，可选）**：设环境变量 GLM_API_KEY（或 ZHIPUAI_API_KEY）后启用：
  - scripts/fill_descriptions.py 用 vision 给接触印片/分镜补描述；
  - scripts/explain_storyboard.py 生成关键镜头讲解（叙事/潜台词/镜头语言）；
  - draft_storyboard.py/lapian_docs.py 由接触印片+切点草拟分镜文档。
  - 未配置 key 时这些脚本跳过/报错，不影响离线拉片与白模。
- 完整 ENV（GLM key/model、Blender、离线依赖、ffmpeg）见 references/environment_setup.md。

