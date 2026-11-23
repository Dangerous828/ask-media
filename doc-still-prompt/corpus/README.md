# 静帧写词语料库

写词质量来自可比的实锚，不来自更多规则。本库收录**经过真实出图验证的条目**：每条是一组「原图观察 → 实际英文 → 真实出图结果 → 教训」。写词前按介质与场景查同类条目，先看别人踩过什么坑、什么写法真的有效。

## 条目格式

```markdown
# <介质>-<场景>-<编号>

- 验证状态：通过 / 部分通过 / 失败（附出图证据路径与通道参数）
- 原图观察：只写可见事实，区分观察与推测
- 实际英文：完整正文，可直接对照
- 出图结果：真实输出与观察的逐维对照
- 教训：哪句英文起了作用（有出图证据）；哪句没被执行；错误归到哪个观察陷阱
```

## 入库纪律

1. **必须出过真实图**。没经过生成的写法只是假设，不入库。
2. 教训必须指向**具体句子**，不写"注意光线"这类空话。
3. 失败条目同样入库，标明错误类别（见下方观察陷阱表）。
4. 单一通道、单一 seed 的结果不写成模型定律；标注通道与参数。

## 外部来源吸收（防"错误吸收"守则）

从外部语料吸收时，历史教训是：把案例蒸馏成一堆全局硬规则，案例本身扔掉——结果是脱离证据链的教条。正确方式：

1. **原文逐字入库**，带来源标注（作者/仓库/原帖，能标就标）。
2. **提炼的每一句话都标条件**："在该案例（通道/模型/分辨率）下观察到"，不写成全局禁令。
3. **格式与内容分开吸收**：内容结构（身份锁段、设备缺陷枚举、每拍一动作）可迁移；提交格式必须换成当前通道方言。
4. **外部验证 ≠ 本地验证**：别人的复测/展示图是别人的口径；本地通道未测就标未验证。
5. **吸收产出是案例和句式，不是规则**——发现自己在往条目里写"必须/不得"，停下来，那是上一轮失败的老路。
6. 视频类案例入 `h3-prompt-writing/corpus/`，静帧类入本目录；各自 README 独立维护。
7. 许可不设闸（家庭中枢自用，创作者授权）；标注来源即可。

## 观察陷阱表（来自 2026-11-06 复刻回归的实测错误）

写反推稿前逐条自问；每类都是实际犯过的错，不是理论风险：

| 陷阱 | 实际案例（2026-11-06） | 写前自问 |
|---|---|---|
| 肢体左右归属 | 黑发人物抓发臂从画面右侧肩部连出（人物自身左臂），初稿写 right | 每条手臂沿可见肩→肘→手连线追一遍；人物自身左右 ≠ 屏幕左右 |
| 遮挡处脑补 | 银发人物手臂末端进入黑发遮挡区，初稿写成"手指扣住高举前臂" | 遮挡末端只有两个合法写法：`hand obscured by …` 或明确记不可见；禁止猜接触 |
| 材质猜测 | 下半幅亮色角状薄片反光，初稿写成"白液喷溅+附着皮肤" | 只写光学外观（`shard-like reflective shapes`）；材质不确定留在审计 |
| 机位角度写浅 | 原图明显俯视（可见头顶、大腿放大），初稿写 just above eye level | 机位必须有投影证据：看得见头顶=俯视；前景放大=近距；说不出证据就不写角度 |
| 影调写偏 | 原图皮肤灰粉低饱和中间调，初稿写 bright overexposed planes + broad wet sheen | 先给最亮/最暗两处锚点，档差写相对关系；局部高光不得放大为整体过曝 |
| 表情统一化 | 原图银发人物一眼挤闭、另一眼睁开，初稿写 eyes are wide | 逐眼核对；不对称表情必须分别写 |
| 朝向冲突 | 要求两人互看，成图两人都正对镜头 | 互看用相对朝向写（face turned toward her），不写看向镜头 |
| 品牌文字执行 | 正文逐字母写 d-e-e-p-s-e-e-k，两轮出图仍渲染 deepseok | 品牌词/生造词不可靠，注明通道限制，关键文字考虑后期方案 |

## 已知可用来源

| 来源 | 内容 | 通道 | 吸收边界 |
|---|---|---|---|
| [awesome-seedance](https://github.com/LearnPrompt/awesome-seedance)（CC BY 4.0） | 672+ 条 Seedance 视频案例，带原帖链接与跨模型复测 | 视频类入 `h3-prompt-writing/corpus/` | 署名引用；结构迁移、格式换方言 |
| [T8mars H3 案例库](https://github.com/T8mars/minimax-h3-prompt-skill-T8)（MIT） | H3 提示词案例库 | 视频类 | 可直接吸收 |
| 无限画布提示词库（本地 `infinite-canvas-stack/data/infinite-canvas.db`） | 1608 条 GPT-Image/GPT-4o/Nano-Banana 提示词，7 个源仓库，含 `{argument}` 参数化模板 | 云端 gpt-image 通道（`magpie_generate_image`）；本地 Qwen 只吸收结构 | 按场景挑不可整库倒；中文正文与 `{argument}` 模板不搬进 Qwen 英文正文；每条标"来源展示图为证，未复测"；肖像类大面积为性感化偶像风格，挑选时注意 |
| [yang0/handraw-style](https://github.com/yang0/handraw-style)（MIT + 署名要求） | 368 条画风（作者/英文风格名/中文特征串）+ 170 条排版图型 + 36 条主题色 | 本地 Qwen 抽测 3 条（`FA-003`/`FG-001`/`FA-039`），均在 Turbo 档 1344×768 出图成立 | **只取文字**，图片不入库；中文 traits 原地选款、须拆成英文可见关系才能进正文；剔掉 traits 里的负向片段；风格卡上的中文特征 OCR 读不出（12/404），要特征请读 JSON |

## 历史吸收源（2026-11-06 重新开放，本轮重吸收）

以下仓库是上一轮吸收的来源（那轮产出了大量死板约束，已废弃该方式）。本轮按"案例不是规则"重新吸收：

| 仓库 | 是什么 | 挖什么 |
|---|---|---|
| [MiniMax-AI/MiniMax-H3](https://github.com/MiniMax-AI/MiniMax-H3) | H3 官方仓库（base-en/ref-en 已在我们技能里） | 官方示例 prompt、skills/3d-animation 的写法 |
| [chatfire-AI/huobao-drama](https://github.com/chatfire-AI/huobao-drama) | AI 短剧生成平台（全栈 TS） | 平台内置的提示词模板与风格预设 |
| [T8mars/T8-penguin-canvas](https://github.com/T8mars/T8-penguin-canvas) | 无限画布本体 | 内置提示词库（上表 SQLite） |
| [HBAI-Ltd/Toonflow-app](https://github.com/HBAI-Ltd/Toonflow-app) | Toonflow 应用 | 续接锁写法（上一轮已吸收"三条锁"） |
| [zhaihao118/Micro-Drama-Skills](https://github.com/zhaihao118/Micro-Drama-Skills) | 短剧全流程 Claude Skills | 10 套视觉风格预设、真实项目 prompt |
| [zhaihao118/hypit](https://github.com/zhaihao118/hypit) | 病毒视频克隆平台 | 复刻类提示词资产（对 video-shot-reverse 线） |
| [T8mars/video-replacement-skill-factory-T8](https://github.com/T8mars/video-replacement-skill-factory-T8) | 视频换角技能工厂 | 换角/修复的 prompt 写法 |

## 现有条目

| 条目 | 介质 | 状态 |
|---|---|---|
| [闪光人像·厨房自拍](flash-portrait-kitchen.md) | 真人摄影 | 通过 |
| [参数对比·加油站场景板](param-compare-gas-plate.md) | 全介质参数层 | 本地实测（三变量同动，方向性结论） |
| [绘画性动漫·双人缠斗](painterly-anime-duo.md) | 2D 插画 | 部分通过（文字+画法残留） |
| [中文图鉴信息图](gpt-image-chinese-infographic.md) | 版式/信息图（云端 gpt-image） | 外部展示图为证，本地未测 |
| [风格预设工具箱·十式](style-presets-micro-drama.md) | 全介质风格层 | 来源项目实用，本地未测 |
| [风格图鉴库·handraw-style](handraw-style-library.md) | 插画/摄影风格选款 + 排版图型 | 本地 Qwen 抽测 3 条通过（368 条未逐条测） |
