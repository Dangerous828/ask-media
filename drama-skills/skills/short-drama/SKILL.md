---
name: short-drama
description: 基于文件系统初始化和继续短剧或漫剧项目，提供 creator-first 六文档路由（剧本/视觉设定/导演/分镜/图片提示词/视频提示词）、场记账（一部戏一本的 `设定集/场记.md`）、本地 Dashboard、制作形态与 Look Development 决策。用户提出“复刻/翻拍一条已有短视频”“创建/继续短剧项目”“看进度/下一步”“做导演方案”“做场记/建连续性账”“打开 dashboard/短剧创作台”“导出制作资料”，或任务跨多个创作阶段时使用；明确的专项请求由对应子 skill 直接处理。
license: MIT
---

# 短剧创作路由

本技能负责项目初始化、跨阶段路由、制作形态与 Dashboard。各阶段正文由对应 owner 完成。

**与专项技能协作**：资产/分镜 owner持有正式条目，doc-still提供单帧成文与事实核对方法；当前写作者回填同一实际正文。h3-prompt-writing负责实际H3词，工程技能继续其检查与执行。本套件提供项目文档、阶段事实和连续性规则；明确专项任务只读匹配子技能，本主路由用于跨阶段、状态与初始化。不重建既有项目、不循环转派。新项目启用导演中间层；旧项目只有补齐《导演.md》后才进入新契约。


## 确定性检查（跑并贴输出，不作放行依据）

判断类问题只靠自看。以下三类必须跑脚本并把输出贴进交付说明，因为漏看一次不会报错：

1. **台词逐字比对**：四字以上引文与《剧本.md》比对，改写台词会浪费一次付费生成。
2. **来源场景 ID 与场记卡拉引用**：每镜「来源」的场景 ID 必须在剧本里存在，剧本每个场景都有镜头承载或登记「未拍场次」；每镜的 `- 场记：CARD-...` 必须在 `设定集/场记.md` 里存在，一卡对一镜——卡不存在、卡无人引用、一卡被两镜引用、一镜引用两卡都要报出来。漏一个 ID 在长文档里看不出来，但它会让账本失去权威。
3. **H3 提交前的格式与算术**：帧数 `17k+5`、`--refs N` 与上传张数一致、六段/三段顺序、时间码、容器时长等于成员时长之和。

warn 逐条说明处理理由；退出码不作为能否继续的依据。会硬拦截的是：参考图准入（`ref_gate`）、真正提交付费生成，以及生产选帧——`SHOT-...#KF-...` 必须解析到《分镜.md》`画面证明计划` 里唯一的 role，`用途：起始帧` ⇔ `first_frame`、`用途：结束帧` ⇔ `last_frame` 必须成对。
## 语料与剪辑准备的继承

文档准备即按本场需求检索语料与剪辑知识；导演选机制，资产补状态，场记落实可见证明与接续条件，再交分镜。跨阶段按已选条款继承，不等素材出来才查手法。完整分工与就绪判据见 [语料机制与剪辑准备](references/mechanism-preparation.md)。新增散文条件由人工回读，现有检查器不自动核验。

## Quick Start

所有项目统一使用 [creator-first 工作流](references/creator-workflow.md)：每集按需维护
`剧本.md`、`视觉设定.md`、`导演.md`、`分镜.md`、`图片提示词.md`、`视频提示词.md`，不建立并行的结构化创作真相。
具体写法见 [六份创作文档](references/creator-documents.md)。
依据三级／记录值／冲突裁决／写作 QC 的单一真相源是 [逐镜证据台账](references/observation-ledger.md)；
六份文档与场记账都只引用它，不各写一份规则。

接手其他 agent 的文档、批量修复报错或重做互相矛盾的分镜与提示词时，先读 [文档修复与复核](references/document-repair-lessons.md)，再按阶段处理。

全片另有**一份**项目级文档 `设定集/场记.md`（场记账），见下文「场记阶段」。它按部、不按集，
每集文档保持六份不变。

## 路由

| 用户要做什么 | owner / 行为 |
|---|---|
| 复刻/翻拍一条已有短视频 | 先按 [视频复刻模式](references/video-remake.md) 拆原片为 `项目开发/原片拆解.md`，用 `video-shot-reverse` 重建九份 `RR-*` 准备文档落 `项目开发/原片还原/`，按 `1.1` 节回填后再进入 develop/write |
| 开发点子、系列承诺、改编和分集地图 | `~/.skills/hub/drama-skills/skills/short-drama-develop/SKILL.md`，仅在用户需要时 |
| 已有多集完整剧本/散稿识别分集 | `~/.skills/hub/drama-skills/skills/short-drama-develop/SKILL.md` 按实际边界建立临时索引 |
| 分析长篇原著 | `~/.skills/hub/drama-skills/skills/short-drama-novel-analyze/SKILL.md`，仅在用户需要时 |
| 写或改单集剧本 | `~/.skills/hub/drama-skills/skills/short-drama-write/SKILL.md` → `剧本.md` |
| 拆人物、造型、地点、道具 | `~/.skills/hub/drama-skills/skills/short-drama-assets/SKILL.md` → `视觉设定.md` |
| 建场记账、核对机位/光位/站位/道具/时间线 | 本技能 → `设定集/场记.md`（一部戏一本） |
| 做导演方案、观看与空间设计、修复分镜注意力 | `~/.skills/hub/drama-skills/skills/short-drama-direct/SKILL.md` → `导演.md` |
| 写资产图片提示词 | `~/.skills/hub/drama-skills/skills/short-drama-image-prompts/SKILL.md` → `图片提示词.md` |
| 做镜头和冻结关键帧（含七项镜头语言锚点） | `~/.skills/hub/drama-skills/skills/short-drama-storyboard/SKILL.md` → `分镜.md` |
| 写视频/时间线音乐提示词 | `~/.skills/hub/drama-skills/skills/short-drama-video-prompts/SKILL.md` → `视频提示词.md` |
| 实际生成媒体 | `~/.skills/hub/drama-skills/skills/short-drama-produce/SKILL.md`，先预览，再显式确认，最后运行 |
| 验收生成的图片和视频 | `~/.skills/hub/drama-skills/skills/short-drama-review/SKILL.md` 的媒体验收：先画风（对照「画风基准」）后剧情；每条生成物在被复用、剪辑或交付前必经 |
| 把已生产的素材剪成成片 | `~/.skills/hub/drama-skills/skills/short-drama-edit/SKILL.md` → `剪辑单.md` 与 `制作成果/成片/`，只用已验收素材 |
| 审稿或校验文档 | `~/.skills/hub/drama-skills/skills/short-drama-review/SKILL.md`，仅在用户点名时 |
| 初始化、Dashboard、归档点名文档 | 本技能 |

`项目开发/` 中的长材料分析与分集索引是可选分析工作区，不参与单集布局判定；写任何一集仍只维护
该集的六份 creator-first Markdown。

现成剧本可直接拆资产；已有视觉事实可直接写图片提示词；启用导演契约时先做《导演.md》再写分镜；
已有分镜可直接写视频提示词。不要为补齐名义流水线伪造上游。

六份创作文档记录剧本、视觉、导演与提示词；剪辑单在素材生产后记录取舍和后期处理。
`设定集/场记.md` 是全片唯一的数值账：机位高度、光位、站位、道具状态、时间推进都从它读。
修改故事、观看与调度、镜头职责或上游时长声明时，回到负责该内容的文档；改这些数值时先改场记账。

## 场记阶段（准备阶段，一部戏一本）

场记是**开拍前的准备工作**，不是生成之后的补救检查。**一张 `CARD-...` 强制对应一个 `SHOT-...`**：
账本先定卡，分镜按卡建镜，数量相等、集合相同，镜内写明 `- 场记：CARD-...`；要多机位就在账本里拆卡。真实片场按场次跳拍，同一场戏的两半可能
隔很多轮才做，所以账必须在第一次生成之前做完。完整规范见
[场记账](references/continuity-breakdown.md)。

``text
剧本 → 资产（先出场景/地点）→ 导演 → 场记 → 分镜 → 图片提示词 → 视频提示词 → 生产
``

- **产出物**：`设定集/场记.md`，一部戏一份，路径固定在设定集根目录，不按集拆、不按场拆。
  文首写 `- 账本：CONT-V001`，改账换版本。
- **输入**：已定稿剧本 + 已出的地点/场景资产 + 白模预演工程。
- **不需要人物形象**。本阶段的人物只是占位模具，写 A/B/C 代号，不写长相、妆造、身份参考；
  人物形象定稿后把代号换成姓名，账本结构不动。资产出到"场景"就能开始，不必等人物形定稿。
- **六本账**：场景空间账、逐场逐镜调度卡（含机位高度与轴线侧）、光位账、道具账、时间线账、白模引用。
- **完成条件**：六本账写完并互相对齐，才允许写第一张分镜和第一条提示词。
- **生成阶段只准引用账本里的值**，不许重新描述机位、光位、站位。账本内部或与剧本对不上时回改账本
  和上游，不在提示词里临场选一个值。

白模（`video-previs`）只为锁机位/走位/轴线/景别/节奏，是人物形象未定时的占位模具；
**哪怕只有一个场景，也必须建一个最基础的白模**（一个场景底 + 人物占位块 + 每镜一个机位）；不接受“单场简单、数值已写清”作为跳过理由，因为后续分镜、静帧、视频提示词分属不同轮次，每轮都会重新理解一次空间关系。它产出的预演产物用来核对场记账，**不作生成参考图**。白模可以从剧本新建（准备阶段的主路径），
也可以从已有原片拉片；两条入口见该技能的「两条入口」。

**白模实摆值必须回写账本，并向下游传播。** 白模摆出来的机位高度、俯仰角、距离、焦距常常与最初写的值
对不上（文字能写对一次，摆出来才发现凑不出想要的景别）。这时要按下面顺序一次性对齐，不许只改账本：

1. 改 `设定集/场记.md` 的调度卡与「白模引用」表，记的是**实摆值**，不是原计划值；
2. 同步改 `分镜.md` 的镜头语言行与**该镜英文正文里的机位句**（两处都要，只改一处中英文就会打架）；
3. 若已完成 `视频提示词.md`，同步改其中的机位描述；
4. 在账本「未对齐项」写明原值为何不成立、改成了什么，供创作者复核。

**下游任一份没有同步，就不算这一步做完，不许继续往下。** 判断方法：把账本的白模机位行与分镜的
镜头语言行并排看，数值与俯仰方向必须逐字一致；出现「平视」对「俯视 12°」这种并存即为未同步。
反过来的时序同样不允许：先写好分镜与提示词、事后才建白模，等于拿白模去核一份已交的稿子却
不回头改——建白模必须在分镜写机位之前，或建完立刻执行上面四步。

账本没写完时不要停在半路去写分镜。项目已有旧分镜或旧提示词、但还没有账本时，先按当前剧本与场景资产
补一本账，再逐镜校正受影响的镜头；这属于补写前置，不是审查回合。

## 执行请求

1. 找到用户给出的项目或资料，只读当前任务的直接输入。
2. 把用户点名的完整范围交给相应 owner；批次只控制上下文，自动续跑。
3. 只有真实创作分叉才询问；不要拿 schema、目录、事务或检查器询问创作者。
4. 范围完成后一次回报完成内容、关键决定、真实未决项和可选下一步。
5. 不自动开始用户没点名的审查、归档或生产。
6. 请求横跨视觉设定、导演、图片提示词、分镜或视频提示词时，结束前按当前六文档做一次视觉依赖对账；
   不因图片提示词和分镜可并行，就把后完成的一支留在另一支的旧引用之外。
7. 视频提示词请求遇到「输入参考图：无」或仍带「待补参考图」时，先路由分镜 owner 检查项目已有图片并刷新绑定。有匹配图就同请求续跑；有必要图缺失就列表停下。
   停下时把三条路一起给出：把已有图片放进项目绑成 `REF-...`；由创作者在自己的工具里出图、本轮先用
   `PLAN-...` 写出逐镜挂图计划并照常产出视频提示词；或者明确改走文生视频。用本套件生产参考图需要项目外的
   adapter 与凭据，只是第一条路的一种做法，不要把它说成唯一入口，也不要只给「生成参考图 / 文生视频」两个选项。
   不把“没有手工指定”当成明确选择文生视频。这一轮如果镜头还缺「视觉依据」，
   同时按已成稿的冻结关键帧回填；两条依据描述同一格画面，不要只补一条。
8. 用户在会话里点名目标视频模型（“按 MiniMax H3 写”“用 Seedance 2.5”）而 `short-drama.json` 的
   `production_profile` 还是 `unset` 时，先把这个选择连同它带来的原生时长、参考方式和正文语言写进档案，
   再继续下游阶段。会话里的一句点名不落到档案上，下一轮就会退回通用路径，方言和时长要重猜。
   档案描述的是**实际出片通道**的能力：本机经 h3q 出 H3 时用 H3 方言里的「本地 h3q 通道档案」
   （只有 `first_frame` 与 `reference`），不要写云端档案再在投产时临时降级。
9. 任何媒体生产开始前，确认《视觉设定.md》已登记「## 画风基准」（见 `~/.skills/hub/drama-skills/skills/short-drama-assets/SKILL.md`）。没有时先
   停下补登记；没有基准就无法判断生成物是否退化，后续验收全部只能是 PROVISIONAL。
10. 生产是“生成一条 → 验收一条 → 才决定下一条用什么输入”的循环，不是一次跑完再统一审。
    被拒素材的派生产物（从它抽的帧、以它为参考的后段）随它作废；剪辑与交付只读已验收素材。
11. 写分镜、图片提示词或视频提示词之前先确认 `设定集/场记.md` 存在且已对齐。缺账时先补场记，
    不带着“机位和光位回头再说”往下写。三个下游 owner 写机位、高度、轴线侧、光位、站位、道具状态
    与时间推进时，只引用场记账对应的行；账里没有的值先补进账本，再写提示词。
    改写某个镜头的这些数值时，先改账本，再改下游。

## 初始化与 Dashboard

需要项目配置时运行：

``bash
python3 {技能目录}/scripts/project_tool.py init ./my-drama --title "示例短剧"
``

直接输入已经确认创作者说明语言、提示词语言、画幅、集数或单集目标时长时，首次 `init` 就带上对应的
`--language`、`--prompt-language`、`--aspect-ratio`、`--episode-count`、`--target-seconds`；只省略
未确认项，不让 Brief 中的确定事实留成配置里的 `null`。写入已确认的生产档案时，状态统一为
`accepted`；`unset` 只表示尚未决定，不另造中间状态。
`init` 只建立配置和空目录；第一次创作时再把文档写入 `剧集/<EP>/`，不预建空文件。
项目已经建好、用户之后才定下目标视频模型时，把选择写进档案，并同时展示它对时长区间、参考方式和
正文语言的影响。档案只接受已发布并已接受的创作者决策，所以是三步，不是一步。先写一行决策记录
（`accepted_value` 就是要落进 `choices` 的对象本身，不要再包一层 `choices`）：

``jsonl
{"decision_id":"CD-H3","status":"accepted","target_locators":[{"src":"short-drama","field":"/creator_authority/production_profile/choices"}],"accepted_value":{"target_video_model":"minimax-h3","video_prompt_dialect":"minimax-h3","video_prompt_language":"en","native_duration_seconds":{"min":4,"max":15},"supported_generation_modes":["first_frame","reference"],"audio_generation":"same_pass"}}
``

上例是**本机经 h3q 出片**的档案（只有首帧与参考图）；改用云端 H3 API 时，`supported_generation_modes` 换成 H3 方言里的云端推荐值。

再发布、接受、写入：

``bash
python3 {技能目录}/scripts/project_tool.py publish <project> --owner short-drama \
  --artifact-id AR-PROFILE --output "创作者决策/production-profile.jsonl=输入/profile.jsonl"
python3 {技能目录}/scripts/project_tool.py accept <project> --artifact-id AR-PROFILE --decision accepted
python3 {技能目录}/scripts/project_tool.py set-authority <project> \
  --field /creator_authority/production_profile/choices \
  --decision-ref "创作者决策/production-profile.jsonl#CD-H3"
``

各字段取值由命中的模型方言给出：`~/.skills/hub/drama-skills/skills/short-drama-video-prompts/SKILL.md` 的 MiniMax H3 / Seedance / Wan 3.0 方言文件都写了
推荐档案。写完用 `status` 复核 `video_model_profile` 是否已经出现。

项目定位与安全写入见 [运行预检](references/runtime-preflight.md)。用户明确要求 Dashboard 时运行：

``bash
python3 {技能目录}/scripts/dashboard_server.py --workspace <workspace> --port 0 --detach --open
``

`--detach` 让服务进程脱离当前 shell 独立运行，会话结束、终端关闭或智能体退出都不会带走它；
链接因此在整个创作期间保持有效。运行中的地址、端口和 pid 记录在
`<workspace>/.short-drama/dashboard.json`（仅本人可读），日志在同目录 `dashboard.log`：

``bash
python3 {技能目录}/scripts/dashboard_server.py --workspace <workspace> --status   # 打印当前链接
python3 {技能目录}/scripts/dashboard_server.py --workspace <workspace> --stop     # 停止
``

同一 workspace 已有在跑的 Dashboard 时，再次启动只会打印同一个链接，不再开第二个端口；确实要换
端口或换令牌时加 `--restart`。不加 `--detach` 时行为不变：前台运行，Ctrl-C 结束。

Dashboard 按阶段展示项目：全剧页给出下一步和分集进度，每集分剧本、设定、导演、分镜、提示词、成片、审查
七个视图，⌘K 搜索全剧。结构视图只读，改动在「编辑原文」里保存 Markdown。画面只认文档里的绑定：
缩略图是分镜里该镜自己的核心参考画面（`用途：构图`；有转场起始帧时取起始帧）的 `REF-...`，每镜素材是剪辑单的「来源」，成片是剪辑输出；没有绑定
就显示空位，不按文件名配图。它不负责工作流编排或媒体生产，需要写作或生成的地方只复制一句请求交回对话。
每集目标时长取自 `status` 的 `format`，节奏对照只用已接受的 `rhythm_profile`。

## 项目级创作决定

制作形态、视觉方向、播放面和集长目标确实约束多个阶段时，展示选择及影响后由用户决定。
Look Development 是可选分支，不是进入图片提示词或分镜的固定门槛；但无论是否做 Look 开发，
**进入媒体生产前**都必须有一张创作者认可的画风基准（Look 测试帧、已接受的原生成片帧或复刻原片帧），
登记在《视觉设定.md》「## 画风基准」。

节奏数值（首钩秒数、情绪触点间隔、反转次数、VO 占比、平均镜长等）住在
`creator_authority.rhythm_profile`。字段与默认值由 `~/.skills/hub/drama-skills/skills/short-drama-develop/SKILL.md` 按制作形态提出，
创作者接受或改写后，按上文三步写入：决策的 `accepted_value` 是完整档案对象，`--field`
写 `/creator_authority/rhythm_profile`；档案已接受后，单改一个值时 `--field` 指向该字段。
`set-authority` 只校验类型与范围，缺字段、越界或多出未知字段都拒绝写入。下游只按 `status` 为 `accepted` 的档案做算术核对，缺失、`unset` 或
`proposed` 都表示「未声明，不核对」。写完用 `status` 复核 `rhythm_profile`；手改后档案不合法时
它返回空档案，问题列在 `rhythm_profile_problems`。

按问题只读取一份相关知识：

- 规则分级与 owner 路由：[规则与路由索引](references/knowhow-index.md)
- 场记账的六本账与写法：[场记账](references/continuity-breakdown.md)
- 输出语言、稳定 ID、所有权与安全边界：[契约与所有权](references/contract-and-ownership.md)
- 实拍、二维、三维、水墨、Q 版、国漫的形态差异：[制作形态](references/production-form-profiles.md)
- 需要比较代表帧时：[Look Development](references/look-development.md)
- 参考图能控制什么、一次能挂几张：[参考角色](references/reference-roles.md)
- 多宫格分镜板能不能用、怎么用：[多宫格规范](references/storyboard-grid.md)
- 遮挡、延迟揭示和观众知情时机：[观众揭示](references/audience-reveal.md)
- 母版、补拍和替代版的职责：[补拍与替代](references/pickup-and-alternate.md)

## 生产与交付边界

外部生产永远保留 `preview -> explicit confirm -> run`。归档只复制用户点名的当前文档和成品，排除
私有输入、凭据、绝对路径与隐藏运行状态；不为归档补造审批、哈希或第二套内容。

用户问“做完了怎么导出/交付给我”时，用 `export` 打包当前状态：

``bash
python3 {技能目录}/scripts/project_tool.py export <project> --out <项目外目录>
``

它把每集现有的六份创作文档和 `剧集/<EP>/制作成果/` 复制到 `--out`，附 `manifest.json` 与
`checksums.sha256`，并排除 `输入/`、`交付/` 和 `.short-drama/`。只要一部分时加
`--episode EP001`（可重复）；只要文字时加 `--no-media`；覆盖旧目录加 `--overwrite`。
`--out` 必须在项目之外。

`export` 是**当前状态快照**，manifest 里 `asserts_approval` 恒为 `false`：它不声称任何审查或
创作者接受。需要带审批证据的正式交付包仍然只有 `package`/`verify` 那条路径。

## 安装维护

只有安装、升级或排障时运行 `python3 scripts/selftest.py`。
