# MiniMax H3 提示词方言

只在目标档案明确写 `target_video_model: minimax-h3` 时使用。云端 API 的推荐档案如下；本机经 h3q
出片时改用下文「本地 h3q 通道档案」，两者不能混用：

```json
{
  "target_video_model": "minimax-h3",
  "video_prompt_dialect": "minimax-h3",
  "video_prompt_language": "en",
  "native_duration_seconds": {"min": 4, "max": 15},
  "supported_generation_modes": ["text", "first_frame", "first_last_frame", "reference"],
  "audio_generation": "same_pass"
}
```

H3 的结构字段用英文；这不等于把中文对白翻成英文。每句中文对白保持原文并写成
`<d>[Chinese] 逐字台词</d>`，由本条视频内的说话人 ID 引出。不要在对白前增加外语、语气词或未写入剧本的开场句。

## 本地 h3q 通道档案（本机默认）

本机出片走 <渲染主机SSH别名> 上的 h3q 队列（见 `h3-queue` 技能），不是云端 API。这条通道实际透传三种输入（互斥，选一）：
单张 `first_frame`；`first_frame` + `last_frame`（FL2VA）；或若干 `reference_image`。
项目用它出片时，档案写成：

```json
{
  "target_video_model": "minimax-h3",
  "video_prompt_dialect": "minimax-h3",
  "video_prompt_language": "en",
  "native_duration_seconds": {"min": 4, "max": 15},
  "supported_generation_modes": ["first_frame", "first_last_frame", "reference"],
  "supported_workflows": ["ref2va", "multishot"],
  "audio_generation": "same_pass"
}
```

`supported_generation_modes` 说的是**输入形态**（首帧／首尾帧／参考图组），
`supported_workflows` 说的是**执行容器**：`ref2va` 是一次生成只装一镜，`multishot` 是一次生成装
多个窗口（`[Shot N]` 切点由模型在 latent 层接缝）。两者正交：multishot 仍然吃参考图组。

模式列表就是这条通道的能力边界，上游从分镜起就按它写，而不是投产时才发现做不到：

- **没有文生**：每镜都要有真实参考图；没有图时先补图，不能写成文生镜头。
- **支持首尾帧（FL2VA）**：h3q 服务端与 CLI 都支持 `--last-frame`，适配器已透传 `role: last_frame`。
  用法是 `first_frame` + `last_frame` 两张一组，模型在两者之间插值，终点精确可控。
  两条硬约束：**尾帧必须与首帧同组出现**（单独给尾帧无处插值）；**首尾帧与 `reference_image` 互斥**
  （同时给两种，模型既被要求"精确到达这一帧"又被要求"从这些图取身份"，服务端只能二选一）。
  需要身份图与地理图时走 `reference` 全参考组，用正文写起点与终点，不要挤进 FL2VA。
- **没有参考视频、参考音频**：要求继承整段运动/声音的原生上下文续接在此不可执行。
  上游可选择独立全参考起链，或只继承可见状态的真实尾帧 `first_frame` 视觉接力；需要两端状态时也可选FL2VA。
  组合能力和损失统一见 h3-queue 输入能力（`../../../../h3-queue/SKILL.md`），接缝选择见 [段间接缝](seam-transition.md)。
  既有案例的3.38与41.87是当时输入和度量下的读数，不是所有镜头的通过阈值或必然失败证明；选择后按实际素材核对，剪辑补不出缺失动作。
  不要把上一段尾帧塞进 `reference_image` 冒充续接：
  它只带来上一段的画质损失和漂移，带不来动作与声音连续。只有当上一段已通过画风验收并被批准复用，
  且起始空间状态确实无法用原生参考表达时，才可以把它的一帧作为一张 `构图` 参考加入，而不替换原生参考。
- **音色不能锁**：每段同轨重新生成人声，同一角色跨段音色会漂。需要稳定声线时，由创作者决定是否在后期
  做人声分离/静音后以 TTS 重建对白层（见 `short-drama-edit`），或接受这个风险；直接叠加 TTS 会形成双人声。

### 多窗容器（multishot）的生产字段映射

`supported_workflows` 含 `multishot` 时，同一场次、时间连续的一组镜头可以装进一次生成。
文档侧只写创作内容，执行字段由生产 job 承载；两边对应关系固定：

| 文档侧 | 生产 job `parameters` |
|---|---|
| 「交付分组」row 声明「容器模式：多镜容器」+ 成员 | `workflow: "multishot"`、`shot_count`（成员数） |
| 成员镜的时长 | `frames_per_shot`（单窗帧数，`17k+5`；各窗相同时只给一个值） |
| 每个成员的「输入参考图」顺序与 `用途` | `reference_bindings`：顺序即槽位，`role` 取 `reference_image` |
| 组内声明「同场连续」 | `same_scene_continuous: true` + `scene_anchor_index`（1-based，指向承担地理/构图的槽） |
| 参考编码尺寸 | `reference_image_size`：`match`（默认，缩到生成画布）或 `max`（保留原生像素 ≤2048） |

**同场连续的身份 + 地理职责**：`same_scene_continuous=true` 的组必须同时具备

- 至少一张承担**身份**的参考（`用途：身份` 或 `造型状态`），binding 的 `may_control` 写明身份/造型，
  且 `must_not_control` 不得否认；
- 一个明确的 `scene_anchor_index` 指向承担**地理/构图**的参考（`用途：地理` 或 `构图`），
  binding 的 `may_control` 写明场景/构图，`must_not_control` 不得否认。

身份与地理/构图必须由**不同的参考图**承担：adapter 把 `scene_anchor_index` 指向的那张当锚，
身份要由另一条绑定提供。同一张图既写身份又写地理会被拒，先把两类参考拆开。

缺任一项就在提交前拒绝，不靠渲染器兜底。**换场、硬切、缺省或显式 `false` 的组不受这条约束**——
它们按原有写法走，不因为这条契约多出要求。

`reference_image_size` 只在 multishot 有意义；在 `ref2va` 作业上声明会被拒绝而不是静默忽略。
`same_scene_continuous` 不是渲染器参数：它只在 adapter／MCP 的提交校验里生效，渲染器不认识它。

**每个窗口不必复述上一窗的收尾状态。** V2 采样器已在 latent 层把前一窗末段钉进下一窗，接缝连续性
不依赖提示词复述；只有在换机位、换主体或正文自身需要交代起点时才重述。个别 relay 案例写过的
「chain boundary is a clean same-camera cut」是那个案例的写法，不是 multishot 的准入条件。

点名 MiniMax H3 只选定模型与方言，不表示创作者选了文生视频。当镜头需要人物、场景、道具或起始构图一致性时，
先按主 Skill 完成真实图片发现与缺口列表。有任何必要图片仍缺失时，不因 H3 同时支持 Base 模式就默默改用文生视频。

## Base / 首帧 / 首尾帧

文生视频、首帧和首尾帧使用三段结构：

```text
integrated_multimodal_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```

- `integrated_multimodal_description` 按 `[Shot 1]`、`[Shot 2]` 写画面、动作、说话人、逐字对白和同步声音；
  单镜也保留 `[Shot 1]`。第一镜不加切镜时间戳，后续切镜用 `[Shot 2] At 00:03.500, ...`，时间递增且落在本次生成时长内。
  小样本观察到切点接近要求，但仍有偏差；交付要求精确时应检查实际切点并在剪辑中调整。
- `overall_soundscape` 汇总环境声、物理音效和非语言人声，不重复对白；对白事件留在上面的主时间线。
  **`craft_default` · 声景是第二动作轨**：把环境声写成与画面动作绑定的事件，而不是背景气氛清单——
  「铜铃在撞击的瞬间炸响」比「环境中有铜铃声」更强：绑定了动作的声景事件会反过来驱动视频把
  撞击演出来（船长仓 Qwen/ComfyUI 通道实测，2026-11 引入）。对白与歌声仍留在主时间线，声景层
  不复述它们。
  无非画内配乐时写 `non_diegetic_music: N/A`，不要留空让模型补乐——这一条有实测支撑，见
  [无对白镜](#无对白镜)。
- 首帧模式从输入帧的可见姿态开始；首尾帧模式只能到达上游已接受终点，不发明过渡后的新状态。

## 无对白镜

在 `overall_soundscape` 写清全镜的环境声、音效或静默。
**`craft_default`**：只描述需要的声轨（环境声、脚步、衣料摩擦、哭声等正向声音）；不写「无对白」「不出现人声」，没有写进去的声音就不会被要求。
人物嘴部状态按实际表演写，不能把无对白一律改成全程闭嘴。

无非画内配乐时保留 `non_diegetic_music: N/A`。小样本中省略这一层出现过额外配乐，
显式写空可作为 H3 的默认写法，不保证所有生成都遵守。
时间线总结只列本镜实际存在的声音层，不照抄包含对白的模板。

## 选哪一种模式

模式由本镜「输入参考图」里各槽位的 `用途` 决定，不由“想不想用多模态”决定：

| 本镜绑定的图 | H3 模式 | 正文结构 |
|---|---|---|
| 没有图，且创作者已明确选择文生视频 | Base（文生） | 三段 |
| 只有一张真实的画面首帧（`用途：起始帧`） | `first_frame` | 三段 |
| 一张 `用途：起始帧` + 一张 `用途：结束帧` | `first_last_frame` | 三段 |
| 本镜核心参考画面（`用途：构图`），无论是否还有人物/地点/道具/风格图 | `reference`（full-reference） | **六段**（**默认路径**） |
| 包含人物/地点/道具图（如角色三视图、场景板），无论是否带起始帧 | `reference`（full-reference） | **六段** |
| 转场帧：从相邻镜实际视频截出的 `用途：起始帧`（+ `结束帧`），仅在两镜很难自然转场时 | `first_frame` / `first_last_frame`（与 reference 互斥） | 三段 |

> ⚠️ **【红线防呆 · 严禁指鹿为马】**：
> - 角色三视图、立绘、设定图（如 `turnaround`、`EP01S01_char_turnaround_v1.jpg`、`gugu_turnaround`）属于【**人物参考图**】，其职责是锁定角色外观（`<Picture 1>`），**绝对不是视频的「起始帧」**！
> - 只有当某张图就是本镜头第 0 秒画面本身的真实起幅时，才可称为「起始帧」。
> - 凡是依赖角色卡/三视图出片，即使全镜只有这一张参考图，也必须命中第 4 行的 `reference`（full-reference）**六段式**结构，严禁误套用第 2 行的单图起始帧三段模式！

`REF-...` 和 `PLAN-...` 在这张表里同权：模式由 `用途` 组合决定，与图片此刻在不在项目里无关。
创作者在 H3 的网页界面里自己挂图时，正文照这张表写，`顺序` 就是他挂图的次序。

H3 官方另有只给尾帧、由模型推断开场的 L2VA 模式。本套件不使用它：开场由分镜已接受的起点决定，
把它交给模型推断会让 `SHOT-...` 的起点失去权威。因此 `结束帧` 只在同时绑定 `起始帧` 时出现。

第四行是最常见、也最容易写错的一种。H3 的首/尾帧输入与参考输入**互斥**，所以「起始帧 + 角色板 +
场景板」不能拆成 `first_frame` 加 `reference_image`：整组统一走 full-reference，起始帧也以
`reference_image` 送入，正文按下面的标签编号引用。用哪一种模式在《视频提示词.md》里由 `用途` 组合读出，
不写进「生成方式」字段——该字段仍只有「文生视频」和「图生视频」两个值。

## Full-reference

任何 `reference_image`、`reference_video` 或 `reference_audio` 进入任务时，改用六段结构，段名和正文说明均用英文：

```text
subject_definitions: ...
summary: ...
retention_analysis: ...
detailed_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: ...
```

**这六段是一条提示词，一次整体提交。** 它们是同一个 `MOTION-...` 的可复制正文，从第一段到最后一段
一起放进那一次生成的提示词框，不是六次生成、也不是只提交第一段。三段结构的 Base / 首帧 / 首尾帧同理。
默认一镜一次生成，下一镜换成它自己那条完整正文；几个镜头装进同一次生成的条件见
[多镜容器](#多镜容器切点由叙事决定不由关键帧数量决定)。

### 素材标签怎么编号

正文用 `<Picture N>`、`<Video N>`、`<Audio N>` 指向本次 job 的实际素材，`<Subject N>` 指向可复用的可见内容。
**编号按同类素材在本镜「输入参考图」里的 `顺序` 递增**：第 1 张图片是 `<Picture 1>`，第 2 张是 `<Picture 2>`，
视频和音频各自从 1 开始。生产端 compiler 按同一顺序附加引用契约，所以文档里手写的编号必须和 `顺序` 一致；
两套编号不一致时模型会收到互相矛盾的素材说明，而接口不会报错。

因此写 full-reference 正文前，先把本镜的槽位按 `顺序` 列一遍，例如：

```text
REF-SHOT-START（顺序：1；用途：起始帧）  -> <Picture 1>
REF-XIAOYU-SHEET（顺序：2；用途：身份）  -> <Picture 2>
REF-STUDY-PLATE（顺序：3；用途：地理）    -> <Picture 3>
```

这份清单不依赖文件路径，只依赖 `顺序` 和 `用途`，所以图片由创作者自己挂载时它照样成立：
把上面的 `REF-` 换成 `PLAN-`，定位符换成 `SHOT-...#KF-...` 或 `IMG-...`，正文一个字都不用改。
起始/结束帧的 SHOT 简写只解析计划中唯一 `start/end`，不取 composition。创作者按 `顺序`
在生成界面里挂图，`<Picture N>` 就对得上。

`PLAN-...` 的图套件没有看过，所以 `subject_definitions` 和 `retention_analysis` 写的是
**这张图按它的 `用途` 必须保留什么**，事实取自《视觉设定.md》和本镜对应 role 的计划帧正文，而不是对像素的观察结论。
两种槽位的句式相同：`用途` 决定保留什么，本来就不是看图看出来的。不要因为图没进项目就改写成
「未验证」或省略保留强度——那会让执行端收不到本镜真正的保留要求。

`subject_definitions` 把每个主体绑到它的标签上，句式为
`<Subject 1> is the ... in <Picture 2>, with ...`；`retention_analysis` 逐条写保留强度和出现的镜次，
视觉素材用 `fully_preserved`、`partially_preserved`、`attribute_transfer`、`weak_reference`，
音频素材用 `fully_copy`、`partially_copy`、`reference`、`weak_reference`，例如
`<Subject 1> (appears in [Shot 1]): fully_preserved - 短发轮廓、连帽外套配色与鞋型保留`。
每个标签在六段里保持同一写法，不留下没有定义的标签。

### 每张图带什么、不带什么

`用途` 决定这一张在正文里被要求保留什么，具体到哪几项由该槽位自己写下的 `控制` 范围决定。

需要保留构图时，在 `控制` 中点名构图、站位或机位高度。
`不得控制` 记录不应照搬的内容，生成后仍需检查实际参考影响，不能把文字声明当成模型保证。
本镜没有起始帧时，地点图会把景别拉宽，要在 `detailed_description` 里写具体取景，见
[目标模型能力档案](target-model-profile.md#参考条件方式)。

`起始帧` 只锚定开场构图与姿态，`身份` 锚定这个人跨镜不变的长相与体态（角色板同时固定本集造型时，
`控制` 里会写明），
`地理` 只锚定空间关系，`造型状态` 只锚定服装与损污。把这条差异写进 `retention_analysis`，
不要让角色板顺带决定构图，也不要让场景板顺带决定人物长相。

`(Sx)` 在**每条视频内**按实际发声先后从 S1 编号（H3 官方规则，闸门 G14 机械检查），同一条视频里同一角色只用一个 ID；跨视频的一致靠同一段声音描述与 `<Subject N>`，不靠固定 Sx 号；中文对白只出现在 `<d>[Chinese] ...</d>` 内。禁字幕写进可见文字约束，
与获准的画内文字分开。
Full-reference 的逐字对白与同步声音放在 `detailed_description` 的对应事件里，`overall_soundscape` 仍只汇总底声与音效。
不要为了“多模态”把所有资产图都带上；每镜只绑定它真正可见且需要保持的起始帧、人物、地点或关键道具图。

### 一个完整例子

分镜里的槽位（三张图：本镜起始帧、角色板、场景板）：

```markdown
- 输入参考图：REF-SHOT002-START（顺序：1）· 剧集/EP001/制作成果/images/SHOT-EP001-002.png《SHOT-EP001-002 起始帧》（用途：起始帧；控制：起始构图、双人站位；不得控制：尚未发生的动作、终态）；REF-XIAOYU-SHEET（顺序：2）· 输入/参考图/小雨定妆.png《小雨定妆照》（用途：身份；控制：脸型、发型剪影、身高比例；不得控制：构图、动作、表情）；REF-STUDY-PLATE（顺序：3）· 输入/参考图/家庭书房.png《家庭书房场景图》（用途：地理；控制：书桌方位、书架墙、灯位；不得控制：人物身份、动作、道具状态）
```

对应的 full-reference 正文（`生成方式：图生视频`，模式为 `reference`）：

```text
subject_definitions: <Subject 1> is the elementary-school boy in <Picture 2>, with a round short black haircut and a light grey-blue hooded jacket over a white inner shirt. <Subject 2> is the home study in <Picture 3>, with the desk against the window wall, a full bookshelf on the left and a warm desk lamp. <Picture 1> is the first frame of [Shot 1], showing the boy seated at the desk from above with the textbook open in front of him.
summary: The boy leans over an open textbook at his desk and stops when he notices the printed map.
retention_analysis: <Picture 1> ([Shot 1] first frame): fully_preserved - overhead framing, desk edge position and the boy's seated placement are kept exactly as supplied at 00:00.000. <Subject 1> (appears in [Shot 1]): fully_preserved - face shape, hair silhouette and the jacket-over-shirt layering stay identical; his pose and expression are set by this shot, not by <Picture 2>. <Subject 2> (appears in [Shot 1]): partially_preserved - desk orientation, bookshelf wall and lamp position are kept; the props on the desk follow this shot.
detailed_description: [Shot 1] ...
overall_soundscape: ...
non_diegetic_music: N/A
```

三张图各自只负责一件事：`<Picture 1>` 给第 0 秒的画面，`<Picture 2>` 给身份，`<Picture 3>` 给地理。
把这条差异写进 `retention_analysis`，生成后检查身份、构图与地理是否分别保留。

### 默认路径：`用途：构图` 的图不是第 0 秒

本技能的默认路径是核心参考画面（`用途：构图`）加身份、地点、道具图。核心参考画面是分镜 `画面证明计划` 里
`composition` 那一行对应的帧，它在镜内的**某个时刻**（`时刻` 列），常常不是 0.0 秒——例如过肩镜里他已经俯身到她耳边，
而镜头是从"她一个人"开始的。把它写成 `opening composition` / `begins from` / "open the shot exactly as supplied"，
等于同时告诉模型"第 0 秒就是这张图"和"第 0 秒她独自一人"，模型两头听。

构图帧锚定机位、取景、光向，人物位置和姿态以分镜的起点与时间窗为准：

```text
subject_definitions: … <Picture 1> is the composition anchor for [Shot 1]: it fixes <机位 / 取景 / 光向中它要守住的几项>, and shows the arrangement reached around <画面证明计划里的时刻>.
retention_analysis: … <Picture 1> ([Shot 1] composition anchor): partially_preserved - <守住的几项> hold for the whole shot; the positions and poses at 00:00.000 are set by this shot and reach the picture's arrangement near <该时刻>.
detailed_description: [Shot 1] … <0 秒时画面里真有的人和状态> … Around <该时刻> the arrangement of the frame corresponds to <Picture 1>: <此刻图里的人物位置与状态> …
```

对应时刻取自 `画面证明计划` 的 `时刻` 列。`起始帧` / `结束帧` 用途的图才写 `first frame` / `last frame`。
这几句沿用官方 ref-en 的 `the shot begins from` / `the shot's keyframe corresponds to` / `the shot ends on`；
没有做过 A/B，出片后先实看第 0 秒是否等于预期。同一规则的单一出处是 `h3-prompt-writing` 的 *Body Consistency Rules* 第 1 条。

### 多镜容器：切点由叙事决定，不由关键帧数量决定

**`taste_option`**：几个相邻镜头可以装进同一次 full-reference 生成。切在哪里是导演按剧情决定的事，
不是"有几张图就能切几刀"。连续运镜走到一个视觉死角（被前景遮住、门框穿过、视线落点转移、反应先于动作、
声音先于画面）时，自然就是切点，**不需要为这一刀准备关键帧**。

**`craft_default`**：装容器的条件：

- 成员在同一场次、同一条资产绑定链、时间连续，已接受时长之和在 4–15 秒内，容器算术按 [交付形态](delivery-profile.md) 记账；
- **每个切点写明叙事动机**：在 `[Shot k] At 00:0X.XXX,` 那一句里先交代"为什么现在切"（被什么挡住、
  视线落到哪里、哪个声音先进来），再写切后可见的内容。写不出动机的切点就并回上一镜，不要为凑结构硬切；
- **第一切必须有构图锚点**（起始帧，或承担构图的 reference 图）。后续各切**可以有也可以没有**自己的关键帧：
  - 有关键帧的成员，按每张图的 role 与对应时刻写对齐句（见下），`<Picture N>` 按参考清单顺序编号；
  - 没有关键帧的切，**不写对齐、不虚构 `<Picture>`**，由上一切的运镜走到切点，切后画面靠正文写清可见主体、
    机位关系和光，身份与地点由共用的身份图、地点图承担；
  - 只有这一切必须精确控制构图、新机位或新地点（例如必须是越肩看屏幕），才为它补关键帧；
- 参考清单里关键帧（如有）按切的顺序排在前面，共用的身份、地点图接在后面。

有关键帧的成员，正文第一行、`subject_definitions` 之前写对齐句。**每个成员都按 role 对齐**：先读该帧在成员 `画面证明计划` 中的局部时刻，再加上成员的累计起点（前面成员的已接受镜长之和），得到整次生成里的对齐时刻：`全局时刻 = 成员累计起点 + 帧局部时刻`。

- `start` / `用途：起始帧`：局部时刻为 0，对齐成员起点，写该成员的 first frame；
- `composition` / `用途：构图`：局部时刻取对应 read 内的指定时刻，写 composition anchor；它可以在任何成员的中后段；
- `pose_proof` 若获准作为参考输入：保留关键姿势与指定 read 时刻的职责，不改标为 first frame；
- `end` / `用途：结束帧`：局部时刻取成员终点，写该成员的 last frame。

例如成员 1 长 3 秒，成员 2 从全局 3 秒开始；成员 1 的起始帧在全局 0 秒，成员 2 的构图帧在其局部 2 秒，则对齐到全局 5 秒：

```text
<Picture 1> aligns with the 0.00-second mark as the first frame of [Shot 1]; <Picture 2> is the composition anchor for [Shot 2] and aligns with the 5.00-second mark.
```

`detailed_description` 写 `[Shot 2] At 00:03.000, the camera cuts to ...`，在全局 `00:05.000` 才写画面达到 `<Picture 2>` 的排列。切点等于成员累计起点，构图对齐等于累计起点加该帧局部时刻，两者分别核对；第一成员的构图帧也照此计算。
`subject_definitions` 与 `retention_analysis` 为每张关键帧保留它负责的成员、role 和对应时刻。

**没有逐切关键帧的已知代价（一组 9 秒三切小样本）**：切点会偏。要求 3.0/6.0 秒切时，每切都挂关键帧的落在 2.88–3.04 / 6.00–6.04；
只挂第一切的偏到 2.92–3.88 / 5.88–6.21，后面两切的构图明显偏离关键帧，还出现过一次多出来的切。所以：

1. 把无关键帧的切放在**天然遮挡或运镜过渡处**，偏半秒到一秒观众看不出来；不要放在需要精确卡点的动作中间；
2. 出片后实看切点位置和切后构图：偏移不大就采用，偏离大或多出一刀，改的是**这一切的动机与切后描述**，不是去补图；
3. 偏移只影响本段内的节奏，剪辑阶段可以在切点附近修入出点；它不会改变已接受的叙事镜长。

## 素材数量上限

一次生成最多 1 张首帧、1 张尾帧、9 张 `reference_image`、3 段 `reference_video`、3 段 `reference_audio`；
视频与音频每段 2–15 秒，且各自合计不超过 15 秒。分辨率取 `768P` 或 `2K`（`MiniMax-H3-Max` 另为 `480P`/`768P`）。
超过上限时在分镜阶段按重要性取舍，并写明放弃了哪些参考，不在正文里假装它们仍然生效。

**`craft_default` · 超限取舍判据**（来源：miora-video-studio §3.3 通道实测，2026-11 引入）：

1. 按**文字还原难度**排，不按固定顺序——机械道具、角色身份最依赖参考图，优先保留；
   环境最可由文字承载，先舍弃；
2. 再看**出镜多寡与离镜头远近**：近景常驻角色优先于远景一闪而过者；
3. **形态过滤**：同一角色的多形态只保留本单元实际出现的形态——形态切换发生在本单元内
   才两张都留。

**`craft_default` · 正文长度经验**（miora 通道实测；本地 h3q 通道报错面不同，仅作压缩档位参考）：
约 2400 字中文首投出现 context-ir 报错，压缩到约 1800 字重投成功；约 1900 字 + 3 图首投即过。
超长正文的处理顺序：先删设定段里本单元不出场的条目，再合并各镜重复的构图描述，不截台词。

本镜还没有起始帧图片时有两条路：由 `$short-drama-produce` 用 `SHOT-...#KF-...` 选择计划中的
`start` 正文生成，拿到真实文件后由分镜 owner 绑成 `用途：起始帧` 的 `REF-...`；或者由创作者
把该镜起始帧正文复制到自己的工具里出图，本轮先记成 `PLAN-...（用途：起始帧）`、定位符写本镜
`SHOT-...#KF-...`，或用能解析唯一 start 的 SHOT 简写。
两种写法本阶段都原样抄入，正文写法相同。

`输入参考图` 只登记参考**图片**。连续段需要的上一段实际视频与实际音频不走这个字段，由下面的
「连续段」小节和生产 job 的绑定承担；不要为了凑成一份清单把视频路径塞进 `REF-...`。

## 连续段

H3 的首/尾帧模式与 full-reference 模式互斥，不能在同一请求混用 `first_frame`/`last_frame` 和
`reference_image`/`reference_video`/`reference_audio`。连续段需要上一段实际视频和实际尾帧时，统一走
full-reference：

- 上一段实际视频：`reference_video`，正文称 `<Video 1>`，控制动作、节奏和声音连续；
- 该视频的实际尾帧：`reference_image`，正文称 `<Picture 1>`，只作为新段开场的可见姿态与构图锚点。

不要把尾帧标成 `first_frame`。这不是措辞偏好，而是 H3 官方接口的互斥输入契约。

## 时长

**`structural_invariant`（执行端契约）**：MiniMax-H3 的 `duration` 必填，为 4–15 的任一整数秒，

> **本地 h3q 不传 `duration`，只传 `--frames`（整数，必须落 `17k+5`）。** 上面这条是**云端字段**的契约，
> 不要照搬到本地：本地写 `--seconds 7` 会被忽略，实际长度由帧数决定（7 秒要写成 `175f` = 7.292s）。
> 换算表见 `seam-transition.md` §6.3.2。**方案里写真实秒数（小数），提交只写帧数。**

并非只有 5/10/15 三档。网页界面或 job 的时长设置要与分镜时长和正文终点一致；写在提示词里的秒数
不能替代生成设置。短动作在合法镜长内完成并保持已接受终点；超过 15 秒的镜头回分镜按闭合状态拆开。
本阶段不偷改镜头秒数。

分镜的叙事镜长常带小数（`2.5s`、`6.3s`），而 `duration` 只收整数秒。换算口径——
**向上取整到不短于叙事镜长的最小整数，低于 4 秒按 4 秒兜底，剪辑按叙事镜长取采用区间**——
见[叙事镜长与生成时长](target-model-profile.md#叙事镜长与生成时长)。不要为了凑整数而压缩动作或
改动已接受的叙事镜长。

`MiniMax-H3-Max` 是另一型号：5–15 秒、480P/768P，仅支持文生和首/尾帧，不支持 full-reference。
不能把本页 H3 的参考音频路径或 4 秒下限套到 Max。

### 对白容量与自然语速

**`craft_default`**：按 [对白预算](performance-action-timing.md#对白预算) 先核对完整发声需要多久，
再给主时间线安排开口、停顿与落点。分镜镜长够长但开口太晚，一样会赶词。
H3 中文小样本可参考约 4.1 个可发声字/秒；用实际可发声区间估算，生成后核对台词完整性。
样本出现过赶词与静默截断，不能据此确定通用截断阈值。
口语语言、声线与语速描述放在 `<d>` 外；`<d>` 内只放语言标签和逐字台词，不放秒数或表演指令。
说话人按本条视频首次发声顺序用 `(S1)`、`(S2)`；full-reference 中说话人物同时写 `<Subject N> (Sx)`。

无参考音频时，以自然语言交代说话方式、开口 cue、句间停顿和说完后的动作；文本估时区间只留在镜头说明中，
不把每个词硬塞进小数秒槽。实际有音频对齐依据或已接受的精确时点时，才据此细化声音时序。
H3 官方接口未提供独立 `speech_rate` 参数，也没有公布「中文每秒固定几字」的可靠公式；
提示词中的语速与时机是生成指导，不能当作秒级执行保证。仅追加“自然语速”无法补上缺失的发声时间。

同一次生成内，已接受的对白跨切镜时可以用 `<scenetrans>` 并声明声音连续；它不会增加总时长，也不能
保证两个独立 job 的音频无缝衔接。`<cutoff>` 表示视频结束时有意截断发声，只用于剧本已要求的截断，
不用于处理装不下的完整台词。

### 说话人绑定

**`craft_default`**：说话人第一次出现时，在 `<d>` 外交代他在画内还是画外、以及音色（年龄、性别、高低），
台词跟在他的可见动作句后面（仍只出现一次），不集中列在正文末尾：
`<Subject 1> (S1), the boy on-screen with a clear high voice, opens his mouth and calls out: <d>[Chinese] ...</d>`。
台词期间画里还有别人的正脸时，把那个人明写成不说话：
`The messenger does not speak; his lips remain completely closed.`——与官方画外音写法
`while his lips remain completely closed` 是同一句式。

一镜实测（远处小孩喊一句，近处骑手不说话，骑手在台词期间仍正对镜头）：现行写法 3 次中 2 次口型落在骑手、
小孩闭嘴；加上述两条后 3 次全部落在小孩。19 条样本的发声基频都在儿童区间——模型没有选错声音，
只是把口型放到画面里最显眼的正脸上。骑手已出画或背对时，两种写法 12 次全部正确。所以分镜能安排时，
先让不说话的人出画或背身；不能时才靠这两条兜底，生成后仍核对口型落在谁脸上。

### 有配音或参考音频时

**`craft_default`**：已有同句同表演音频时，先测实际发声与停顿，再确定镜长。没有现成音频仍可按文本估计
写提示词，不为完成本阶段自动调用 TTS 或生成服务。

- 只参照音色、情绪或说话方式：使用 `reference`；它会重新表演本镜台词，不能拿参考音频的文件长度
  当作新台词时长，也不携带参考音频里无关的原话。
- 已接受完整声音轨原样复用：`fully_copy` 表示整条最终音轨；只用对白层或片段并另加环境声时使用
  `partially_copy`，写清源片段与目标时间的对应。复用用到的发声区间要完整容纳，不为适配镜长压缩语速。
- 参考音频走 full-reference，配合至少一张参考图或一段参考视频；每段音频 2–15 秒，最多三段、合计
  不超过 15 秒。图片改用 `reference_image`，不能与 `first_frame`/`last_frame` 混用。

`fully_copy` 等是官方提示词的复用意图，不是逐样本一致的验收证明。生成后核听逐字内容、语速、停顿、
尾音完整性与口型；项目需要精确锁定已有音轨时，以后期保留该音轨并核对画面同步作为最终依据。

### Context-IR 的作用

H3-Context-IR 把多模态输入增强成结构化提示词，本身不生成视频，且仍要求调用方先给出 4–15 秒的
`duration`。它不能代替对白预算。若执行端使用该服务，检查增强后的逐字台词、声音时间线与原时长一致，
不因使用官方增强就跳过容量检查。

官方依据（2026-09-07 核对）：

- [Base 提示词指南](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/base-en.txt)：对白位置、说话人、语速描述、切镜时间戳与跨镜发声。
- [Full-reference 指南](https://github.com/MiniMax-AI/MiniMax-H3/blob/main/skills/h3-prompt-writing/references/ref-en.txt)：六段结构、音频引用与复用语义。
- [视频生成 API](https://platform.minimax.io/docs/api-reference/video-generation-v2-create)：必填时长、型号差异和输入模式互斥。
- [官方 CLI 的 H3 指南](https://github.com/MiniMax-AI/cli/blob/main/skill/h3-video/references/h3-video.md)：音频配合视觉参考，声音对齐与生成后检查。
- [Context-IR API](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir)：提示词增强和独立的时长输入。
