---
name: short-drama-review
version: 1.0.0
description: 审查短剧项目中的原著分析、故事、剧本、视觉设定、导演方案、图片提示词、分镜 reads、关键姿势与冻结关键帧、视频提示词和已有媒体，并且是生成图片与视频的唯一验收 owner（先画风后剧情，look_check / video_check）。用户提出“这张图/这段视频能不能用”“验收出图/出片/成片”“画风对不对”“审稿/检查剧本”“检查导演/分镜注意力”“检查资产或连续性”“检查图片/视频提示词”“审查模板感”“根据生产观察做项目校准”时使用；只写审查问题、结论和修订要求，不代替 owner 修改来源文件。
license: MIT
---

# 短剧审查

优先由未参与当前版本创作的 reviewer 执行；条件不允许时可以自检并如实说明。审查与修改是两个工作
单元：本技能只定位问题、影响和必须达到的修订结果，不在同一轮替 owner 改来源。

## 自看硬规则

任何产物出来都要自己看过才往下走：**视频一秒一帧，闸门过了不算看过。** 完整细则与"什么叫不算看过"见 `ask-media` 技能的 `../../../ask-media/references/discipline.md`，本条不复述。

## 语料与剪辑准备的继承

审计划时核对完整模板条款→导演采纳/改编→CARD/SHOT→证明时间窗的承载；审媒体时对同一清单给真实时间码、画面/声音证据及未验范围。摘要不代替完整不变量，结构闸门不代替实看；计划覆盖不能写成媒体 PASS。完整分工与就绪判据见 语料机制与剪辑准备（`short-drama` 技能 `../short-drama/references/mechanism-preparation.md`）。新增散文条件由人工回读，现有检查器不自动核验。

## Quick Start

直接读取用户点名的当前文件。单集审查需要落盘时写 `审查/EP001-审查.md`；独立文件审查使用
`审查/<主题>-审查.md`。用户只要口头结论时直接回复，不为“完整”创建审查文件。

审查 Markdown 建议结构：

```markdown
# EP001 审查

- 范围：剧本、分镜、视频提示词
- 结论：REVISE
- 复核方式：独立 reviewer / 自检

## Blocker · REV-001 · 画面文字未被镜头承载
- 位置：剧本.md / EP001-SC002；分镜.md / SHOT-EP001-004
- 证据：……
- 影响：……
- 修订结果：由 short-drama-storyboard 补入准确文字及可读条件。
- 规则：`reviewed_invariant · SHT-01`
```

引用只使用文件名、标题 ID、行号或短引文；不建立 sources 声明、哈希、record ID 或第二套状态。

## 选择审查范围

- `source_analysis`
- `story_script`
- `assets_continuity`
- `image_prompts`
- `storyboard_keyframes`
- `video_prompts`
- `production_outputs`
- `final_cut`
- `full_episode`
- `delivery_privacy`
- `project_calibration`

只读对应资料，不预加载整个项目：

- 原著分析：[原著分析审查表](references/rubric-source-analysis.md)
- 故事、场景、行动与对白，改编是否守住原著人物与主线，已接受节奏档案的核对，开场、结尾与中段的局部检查：[故事剧本审查表](references/rubric-story-script.md)
- 身份、变体、连续性、时代与图片提示词：[资产提示词审查表](references/rubric-assets-prompts.md)
- 原文落实、镜头、关键帧与视频运动：[视觉运动审查表](references/rubric-visual-motion.md)
- 完整审查方法：[审查方法](references/review-method.md)
- 制作端常见缺陷：[生产质量门](references/production-quality-gates.md)
- 授权生产观察的项目内校准：[项目校准](references/project-calibration.md)
- 模板感、重复手法或 AI 味：[反模板修订](references/anti-template-repair.md)
- 阶段边界、参考媒体与规则表：[阶段契约](references/stage-contract.md)

## 工作流

### 1. 冻结范围

写清当前要审哪些文件、章节、镜头或提示词，以及创作者已经明确的限制。目标在审查中发生变化时，
重新读取再下结论。

### 2. 先查可证明事实

- 六文档的可见 ID、引用和时长是否一致；
- 启用 director-v1 时，导演场次与镜头计划能否解析到正式 SHOT，reads 是否无缺口/重叠覆盖镜长，
  start/pose/end 的时刻和关键姿势正文是否相符；
- 剧本对白、动作、声音、画面文字是否都有画面/声音承载；
- 人物、地点、道具状态和镜头起止是否连续；
- 提示词是否从准确起点到准确终点；
- 目标模型画音同轨时，声音内容、时序和发声边界是否与来源一致；无对白镜是否交代底声或静默
  （`VID-22`、`VID-23`，见 [视觉运动审查表](references/rubric-visual-motion.md)）；
- 私有输入、凭据、绝对路径或内部流程文字是否泄漏。

缺少必要输入时只停止依赖它的判断，其他问题可以继续汇总。

### 3. 带证据审内容

每个 finding 包含：位置、必要短引文或冲突事实、观众/制作影响、必须达到的修订结果、owner、严重
程度和规则等级。不能只说“AI 味”“不够电影感”或给无证据分数。

### 4. 跨文档综合

```text
剧本事实 -> 视觉设定 -> 导演观看与调度 -> 镜头 reads 与边界 -> 首帧/关键姿势/尾帧 -> 视频运动 -> 下一状态
```

优先守住原意、知情时机与连续性，不奖励脱离来源的华丽提示词。

### 5. 结论与分派

- `APPROVE`：没有阻断问题；
- `APPROVE_WITH_NOTES`：只有不阻断的改进；
- `REVISE`：存在结构、内容或限制冲突；
- `PROVISIONAL`：关键输入不足，暂时无法完成判断。

按 owner 分组修订要求。本轮完成后交还控制权；修改和复审只有用户明确请求时开始。用户已授权的连续生产
按 produce 的逐段授权执行媒体验收，不要求每段再次点名审查。

## 严重程度

- `blocker`：不安全、不可交付或会让流程走错；
- `major`：明显破坏剧情理解、连续性或制作结果；
- `minor`：有具体影响但不阻断；
- `note`：创作选择或可选润色。

## 边界

- 不提交图片、视频、TTS 或音乐任务，不配置 adapter，不把 Dashboard 操作当生产授权。
- 运行环境能读取媒体时，`production_outputs` 必须真的抽帧读图，见下一节；只有读不到媒体时才明确
  限制，并且不从文字或 adapter 状态推断脸部一致、表演、口型、混音或市场表现。
- 生产观察必须绑定准确输入、提示词、参考、配置和结果版本；不能泛化成通用规则。
- 审查文件只保留修订所需的最小证据，不复制完整私有输入。

## 媒体验收（production_outputs）

本技能是生成图片和视频的**唯一验收 owner**。`short-drama-produce` 只运行 `measure` / 技术测量并
交付待审媒体，不执行 `review` / `approve` / `reject`，不判质量；`short-drama-edit` 只取舍已验收素材，
`video-studio` 的四件套与信号脚本只提供测量。任何生成物在被绑成下一次生成的参考、进入剪辑或
交付之前，都必须先在这里拿到结论。

**每一镜都另起一个未参与生产、未继承制作结论的全新 reviewer 上下文。** reviewer 必须直接读取真实
媒体、全部参考图、当前剧本、分镜和提示词；生产 agent 的转述不能代替这些输入。整片再换另一名全新
reviewer，不能由任何逐镜 reviewer 兼任。这里的独立是实际流程隔离，不是防伪权限：`--reviewer` 只
记录归属，名字不同或写着 `independent` 都不证明独立，工具也不输出 `independent=true`。
**独立 reviewer 的操作化定义**：当前上下文中没有本段视频提示词的写作历史，没有本段视频的生产任务记录，没有参与过本镜的参考图绑定决策。满足这三条才算独立；否则视为自审，结论可供参考但不能作为验收依据。
实际委派、参考组变化或ASR歧义时，读 [reviewer输入与观察范围](references/reviewer-evidence-handoff.md)：保留真实子会话输入/返回出处，制作端不代写未测项，声音替换先有实际听辨和项目方案依据。

顺序固定，前一层不过就停，后续项记 `UNVERIFIED`，不拿未审项补足结论：

1. **画风与画质（REV-15，一票否决）。** 运行
   `python3 scripts/look_check.py measure <project> --media <文件...>`（从生成视频抽帧、裁切或
   二次处理得到的图加 `--derived-from <父媒体>`）。它对照《视觉设定.md》「## 画风基准」里带
   `认可依据` 的原生画面，按色彩分布选最近的那张基准，量清晰度、纹理、平涂块、色彩分布、饱和度与
   画幅，写出 `审查/look/<媒体的项目相对路径>.look.json` 和保持原比例的左基准、右候选对比图。
   **必须读这张对比图**，写下材质、光、纹理、人物质感实际看到了什么。机械 FAIL 默认阻断；
   创作者实看后可在 `approve` 显式使用 `--creator-ack` 豁免统计判定，报告记录
   `mechanical_override=true`，原机械结论保持不变；包括画幅不符在内的机械项都可由该确认豁免。
   无确认不能改判，PASS 也不等于通过。
   项目还没登记带认可依据的基准时结论为 `PROVISIONAL`，先让 assets owner 登记。

   亮度、对比度、过曝这类有争议的画风项，不能只靠整体印象下结论，先跑**像素统计**：裁出争议区域
   （窗区/高光区/暗部），量 `>245` 占比、暗部分位（p5）与均值，对照基准同区域，数字写进证据。
   压缩图幅的整体描述会漏掉死白与对比度塌陷（EP001 KF-04 v5→v7，2026-11-20 实测：窗区 `>245` 从
   15.5% 压到 2.5%、暗部 p5 回 31——创作者肉眼可见的差异只有统计里才说得清）；创作端用负向词压制
   过曝后，复测同一统计确认收敛。

   **创作者的观感说法是症状报告，不是待反驳的论断。** 先把它翻译成可核对的视觉特征、对图逐项核实，
   再下结论；全局统计正常而创作者仍说颜色坏时，是统计抓不住灰雾感与色感（同日 KF-06 v2：σ/饱和度与
   基准同档，创作者一眼判「颜色明显是坏的」）。判「瑕疵」前先查**肌理分布**：颗粒/纹理只在局部=瑕疵；
   全画面统一铺满（皮肤、衣服、墙面同一种搓揉感）=画布/笔触质感=风格取向——此时先问创作者这个风格
   要不要，不按缺陷修（同日实测：把全画面油画肌理误判为「大腿鸡皮瑕疵」，撤回）。一轮没对上就直接给
   候选术语加特征清单再核对（「你说的 X 是指 ①平涂大色块 ②统一笔触肌理 ③灰雾？」），不让创作者
   反复逼近说法。常见说法先核对的特征：

   | 创作者说 | 先核对 |
   |---|---|
   | 油画感／老照片／大色块 | 物体内部有无色彩层次、平涂色块、全画面统一笔触肌理 |
   | 对比度丢了／灰蒙蒙／发雾 | 灰白薄雾；词里是否叠了 low-contrast/milky 类反向带偏的调色修正 |
   | 过曝／死白 | 争议区 `>245` 占比、p5、基准同区对照 |
   | 塑料／蜡像感 | 皮肤血色过渡、高光层次 |
   | 鸡皮／颗粒／噪 | 全画面统一性：局部=瑕疵，统一=风格 |

   全幅统计只在**同一构图条件下**才说明退化，所以比较条件是 measure 的显式输入：
   `--comparison unknown|comparable|different-framing --comparison-note "<景别、主体比例、景深的实际观察>"`，
   默认 `unknown`。只有 `comparable` 时统计结论才是机械 FAIL/WARN 的依据；`unknown` 与
   `different-framing` 时机械结论记 `NOTCHK`（统计数值仍留在报告里作定位信号），**NOTCHK 不是通过**，
   画风项只能记 `UNVERIFIED` 或由 reviewer 实读对比图后按 `different-framing` 逐项审再判——换景别、换构图
   本身不能算画质退化，也不能算自动放行。画幅（宽高比）与基准不符仍记机械 FAIL，但可由创作者实看确认豁免。
   重新 measure 时可比性或测量依据变了，旧批准与旧逐项审查自动失效（追加 `pending`，历史不覆盖）；
   共享 `ref_gate` 拒收沿用旧批准的 `unknown` 或依据已变更的报告。
   独立人物、道具、地点**资产板**改用 `measure --kind asset`：不与完整场景基准比较，机械结果为 NOTCHK，
   必须直接读原图核对身份、视图、文字、裁切和用途。场景帧与视频不得用 asset 类别绕过场景指标。
2. **技术。** 单段按来源预期运行，例如
   `python3 scripts/video_check.py <project> --media <视频> --expect-seconds 13.666666666666666 --expect-size 896x512`；
   这里328帧/24fps和draft尺寸仅为示例，实际取本段来源与档位。不同预期的镜头分别测。
   未传预期时 frames PASS 只说明读到帧，不证明等于来源；`--multi-shot` 只用于已接受的多镜容器，不能隐藏单镜藏切。
   音轨、黑帧、切点候选和头尾刹车是技术信号，再实看伪影、闪烁、穿模与空间。
   **跨段接缝**：同场相邻多段一起审查时，加 `--seam` 测量接缝处结构差异：
   `python3 scripts/video_check.py <project> --media <敤1> <敤2> --seam`；
   MAD≥28 发 WARN，MAD≥55 发 FAIL。WARN/FAIL 时必须实看接缝两侧各 1 秒，明确写出漂移有/无后再作结论。
   反向同样成立：**MAD 全绿不证明无硬切**。创作者反馈"还有硬切"而接缝测量全过时，按
   `../short-drama-video-prompts/references/seam-transition.md` §0.1 第 0 步判型（画面缝／镜内相位断／情绪缝），
   别拿指标反驳创作者——EP004 006+007 实测：接缝五帧几乎逐帧一致，创作者仍判"抱起来那一下"硬切，
   根因在词层（入场压缩／情绪跳档），不在接缝指标里。
3. **表演与连续性。** 抽帧实读人物、道具、空间和动作因果，状态与分镜起止一致。抽帧下限**不得宽于**
   `ask-media` 技能的 `../../../ask-media/references/discipline.md` 的「视频采样间隔 ≤1 秒」：按此换算 8 秒镜至少 9 帧，
   下面的 5／8 帧只在镜头更短、间隔仍 ≤1 秒时才可用，**不是上限豁免**；多人、肢体交叠、道具交接一律取逐帧序列。
   联系表和首尾对照只算初筛，结论里写明“未逐帧”。
   **首帧后漂移**：走 `first_frame` 模式的段，起始帧锁第 0 帧，模型对中间路径无约束。
   额外核对：① 第 3 秒附近人物与起始帧是否同一身份；② 空间锚点是否与起始帧一致；③ 有道具操作时道具是否保持同一形态。这三项不因起始帧正确而省略。
4. **对白与声音。** 逐句对照剧本直接回听并观看发声画面；ASR 只用来定位，不能证明精确台词、
   口型或声线，即使转写与剧本一致也不能把这三项判成 PASS。

每一层的结论单独写，不让后层的通过掩盖前层的失败。道具数量对了、台词对了，都不能弥补画风退化。
每镜和整片都必须由 reviewer 逐项输出以下六种 `PASS` / `FAIL` / `UNVERIFIED`，没有适用内容时也须
根据剧本与真实媒体明确核实，不得省略或把“没测”写成 PASS：

| CLI 检查项 | 审查内容 |
|---|---|
| `look_technical` | 画风基准、材质光影、画质与技术测量、可见伪影 |
| `identity_costume` | 人物身份、脸部与体型、服装造型及参考图一致性 |
| `hand_limb_contact` | 手指数与畸形、肢体交叠、人物/道具接触和交接 |
| `action_spatial_continuity` | 动作因果、起止状态、站位朝向、空间与道具连续性 |
| `dialogue_lip_sync` | 对照剧本的精确台词、发声人、口型与发声区间 |
| `audio_voice` | 直接回听声线、音色跨镜一致性、清晰度和声音接缝 |

用 `look_check.py review` 保存六项及各项实际观察；命令只记录 reviewer 结论，不授予剪辑或参考权限。
六项各给一个状态，并用六个 `--evidence 检查项=观察` 写明实际看到/听到的证据。示例省略号必须替换
为逐项真实状态和观察，不能原样复制成结论：

```bash
python3 scripts/look_check.py review <project> --media <文件> --scope shot \
  --reviewer <名> --script <剧本> --storyboard <分镜> --prompt <提示词> \
  --reference <实际参考图...> \
  --look-technical <PASS|FAIL|UNVERIFIED> --identity-costume <...> \
  --hand-limb-contact <...> --action-spatial-continuity <...> \
  --dialogue-lip-sync <...> --audio-voice <...> \
  --evidence look_technical="<观察>" --evidence identity_costume="<观察>" \
  --evidence hand_limb_contact="<观察>" --evidence action_spatial_continuity="<观察>" \
  --evidence dialogue_lip_sync="<观察>" --evidence audio_voice="<观察>"
```

审查与用途决定均只追加不覆盖。`approve` 要求同一 reviewer、同一范围、当前媒体字节**和当前测量依据
（measurement_id）**的六项全部 PASS；任何 FAIL / UNVERIFIED 都不能批准。

**静帧（关键帧、资产帧）没有音轨**，`dialogue_lip_sync` 与 `audio_voice` 在本帧上无从判定。静帧可以按既有
契约照旧走六项，但报告会用 `not_applicable` 标出这两项；**这个标注的意思是"本帧没验过口型与声线"，
不是"验过且通过"**。读报告时不能把六项全绿当成声音也验过了——口型与声线只在视频阶段的 `video_check`
判定。静帧也可以显式记 `N/A`，表示不在本帧判定。机械画风 FAIL 默认阻断，
仅创作者实看后的 `--creator-ack` 可豁免包括画幅在内的机械项并留下 `mechanical_override`
（统计判定只在 `comparable` 下成立，见第 1 层）：

```bash
# 只入选剪辑
python3 scripts/look_check.py approve <project> --media <文件> --use edit --reviewer <名> --note "<看到了什么>"
# 还要作为下一段的参考：剧情层（第 3、4 层）也必须已逐帧核对通过
python3 scripts/look_check.py approve <project> --media <文件> --use reference --story-pass \
  --story-note "<道具、站位、状态核对结论>" --reviewer <名> --note "<看到了什么>"
python3 scripts/look_check.py reject <project> --media <文件> --reviewer <名> --note "<原因>"
```

- `--use edit` 只允许进剪辑，不授予参考权限；只有 `--use reference` 且额外带 `--story-pass` /
  `--story-note` 的逐镜媒体才会被生产闸门放行为参考。reference 的剧情通过不能由 edit 批准反推。
- 拒绝一条媒体会把所有 `derived_from` 指向它的报告标为 `superseded`；派生物要重新验收。
- 逐镜/整片审核人与本地生产执行者相同时拒绝批准，`--creator-ack` 不能把本地生产者自审变成独立审查。
  没有本地执行者的外部生图不再自动判成自审，但逐镜/整片批准必须带创作者实看后的 `--creator-ack`，
  报告记录 `provenance=external_no_local_executor`。独立资产板不是镜头，仍按原图人工验收；其自审
  reference 才使用创作者确认。
- 报告中的 `independence=process_isolation_required` 是流程要求，不是认证结果。调用方必须真的
  创建新 reviewer 上下文，并保留其独立输入与结论；禁止只改 reviewer 字段就宣称完成独立审查。

## 成片验收（final_cut）

`short-drama-edit render` 产出成片后，本技能同样负责交付前验收，不能只凭 `verify` 退出码或文件存在放行。
另起一名与所有逐镜 reviewer 都不同的全新 reviewer，直接读取整片、剪辑单及上述来源，按同一六项
运行 `look_check.py review ... --scope final_cut`，再以 `approve ... --scope final_cut --use edit`
记录结论；整片没有 reference 权限。任何必要项 UNVERIFIED 都保持未通过。

1. 运行 `edit_tool.py verify`；有 FAIL 必须返回非 0。黑场、音画规格、响度目标、切点和未测项分别记录，
   未测不等于通过。
2. 对整片及跨场相邻段按同一画风基准运行 `look_check.py`，重点看跨段色彩、材质和人物渲染是否突然跳变；
   对照《剪辑单.md》抽看每个接缝前后帧。
3. 回听对白、旁白和音乐接缝，核对字幕逐字来自《剧本.md》，并确认实际交付文件就是 verify 测过的文件。
   需要统一声线或替换对白层的，按 edit 的既有后期路线处理，不把双人声或音色漂移隐瞒为通过。

单镜素材的验收不能代替整片验收；整片通过后，才可复制到 NAS 或标记为可交付。

## 缺陷分诊顺序

成片出问题时先定位到输入，再决定改什么，不直接重抽：

1. 回看这一镜的关键帧或参考图本体：缺陷是否已经在输入里（手数、人数、身份特征、道具）。
2. 身份段与正文是否漏写或写反了该特征；不出场的角色是否被写进了正文。
3. 以上都正常才改词；同因连续两次失败就退回分镜或换输入（REV-17），不再抽种子。

创作者一次报来多条缺陷时，先暂停后续提交，逐条归因到“设计 / 提示词 / 参考图 / 随机性”，修一处后
横扫所有用到同一特征的镜头，再恢复生产。

**质量返工不是重新抽卡。** 同一 `IMG/MOTION/SHOT` 来源条目已有绑在当前字节上的人工 `rejected` 结论时，
produce 的 `prepare`/`run` 会要求新 job 在 `parameters.revision` 里绑定**这一次**拒绝：准确的上一个 job/run、
稳定 `failure_key`、实际观察、真正改动的输入、保持不变项、预期结果；改动多处还要联动理由，同一原因
再次失败要升级为带导演/分镜/视觉/图片提示词来源的上游重设计。审查侧负责给出可归因的拒绝结论和稳定的
`failure_key`；工具只核结构，不判断身体可及性或失败语义。技术失败与 `collect` 不属于质量返工。
格式与停止条件见[项目校准](references/project-calibration.md)与[生产质量门](references/production-quality-gates.md)。

## 安装维护

只有安装、升级或排障时运行 `python3 scripts/selftest.py`。
