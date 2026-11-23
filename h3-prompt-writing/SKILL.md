---
name: h3-prompt-writing
version: 1.3.1
license: MIT
description: 写 MiniMax H3 视频提示词正文（T2VA 文生 / I2VA 图生 / FL2VA 首尾帧 / L2VA / Ref2VA 全参考）。用户说“写视频提示词”“把分镜转成 H3 提示词”“图生视频或文生视频提示词”“H3 三段或六段正文”“画面描述、环境声、配乐怎么写”“参考图标签 Picture 1 怎么标”时使用；也用于对齐首尾帧与关键帧。Write MiniMax H3 video generation prompts, composing integrated_multimodal_description, overall_soundscape and non_diegetic_music. 短剧任务按正文读取对应阶段知识，本技能继续完成当前工作。
compatibility: Portable to any agent that can read local files — no external API calls, MiniMax Hub tools, or proprietary runtime required.
---

# H3 Prompt Writing

## 短剧项目协作（命中即读，保留本职）

本技能继续撰写完整H3正文、声音与参考标签。短剧任务先读 [short-drama-video-prompts](../drama-skills/skills/short-drama-video-prompts/SKILL.md) 的动作、时长与交接规则，再按本技能官方模式写作；已有分镜与已接受素材继续使用，不默认要求别的技能先写一份稿。 规则见 [协作契约](../SHORT-DRAMA-ROUTING.md)。已读上下文复用；只有跨阶段、状态或初始化才读取short-drama主路由。

机位、景别、高度、光位、站位和持物取自《场记.md》对应的调度卡，戏剧意图取自《导演.md》，本镜起止和时间窗取自《分镜.md》；本技能只把它们翻译成 H3 正文，不重新决定。三处说法不一致时回上游改，不在正文里挑一个糊过去。

## Workflow

1. 先选模式再写词。判据（缺省不要退化成"只挂一张首帧"）：
   - **Ref2VA 全参考**：出现任一项 —— 角色身份要锁定、同框多人、同一角色给了多视图或多张图、要继承场景板、要用分镜板、要参考运镜或音色、多素材混合。短剧与动画项目默认走这条。
   - **I2VA**：只给一张明确起始帧，且身份/场景/风格都不需要额外参考。
   - **FL2VA**：首尾帧都给且中间是连续运动（硬切段落不用，本链实测有尾部运动谷）。
   - **L2VA**：只给终点帧。
   - **T2VA**：无任何素材（官方模式说明；**本地 h3q adapter 不支持纯文生**，无法提交，见下文「本地 h3q 约束」）。
   角色一致性是卖点时，不许用"一张首帧 + 文字描述"糊过去：那张图只当起始帧，身份另按 Ref2VA 的 `<Subject N>` 引用。
2. For base text/keyframe modes, read `references/base-en.txt` and follow its final prompt structure.
3. For full-reference mode, read `references/ref-en.txt` and follow its six-section rewrite format.
4. Preserve the exact field names, section order, labels, and timing notation from the selected guide.
5. 动笔前先读三样东西：**真正的首帧（或构图锚点图及其对应时刻）**、本镜场记卡、本镜分镜的 reads 时间窗。先继承导演已采纳的完整模板条款、场记状态/接续条件和分镜证明时间窗，按 [语料机制与剪辑准备](../drama-skills/skills/short-drama/references/mechanism-preparation.md) 翻译成可见动作；缺必要决定先回对应 owner，不在正文阶段重选机制或补戏。同类场景在 [语料库](corpus/README.md) 有已验证条目时按需查：取其结构（身份锁段、设备缺陷枚举、每拍一动作带因果），不照抄格式——本地提交必须仍是六段/三段方言并补声景。**镜头涉及双人一问一答／停顿、情绪压抑到哭、身份漂移、产品功能演示且已有条件不足、确需补查时，直接读 `../creative-dna-cards/SKILL.md` 按镜头机制查 [Creative DNA 机制卡索引](corpus/creative-dna-t8/INDEX.md)（全量库：`corpus/creative-dna-t8/search.py 关键词`），一次只读一张，把不变量翻译成可见证据并写进本镜验收清单；卡的英文骨架不得当 H3 正文复制。链上引入点见 [PRODUCTION-INTEGRATION.md](corpus/creative-dna-t8/PRODUCTION-INTEGRATION.md)。** 写完按下面的 *Body Consistency Rules* 逐条读一遍。

## Base Modes

- T2VA: build the full audiovisual timeline from text.
- I2VA: start from the first frame and develop forward from it.
- FL2VA: describe the continuous path between the first and last frames.
- L2VA: infer a plausible opening and converge to the supplied last frame.

Use `integrated_multimodal_description`, `overall_soundscape`, and `non_diegetic_music` in the order shown in `references/base-en.txt`.

## Full-Reference Mode

Ref2VA rewrites use `subject_definitions`, `summary`, `retention_analysis`, `detailed_description`, `overall_soundscape`, and `non_diegetic_music` in that order. Reference labels stay consistent across all sections.

Read `references/ref-en.txt` for label rules, retention analysis, and complete examples.
混合参考职责不清、或把模型支持误当作当前入口可用时，先读 [参考职责与入口核对](references/market-reference-roles.md)；六段格式仍以上述指南为准。
### 两个参考标签各自管什么（写词前必须先分清，分不清就会乱用）

**判据只有一句：这张图是"素材来源"还是"画面本体"。**

| 标签 | 回答的问题 | 什么时候用 |
|---|---|---|
| `<Subject N>` | 画面里**要出现什么东西** | 人、动物、物体、场景、服装、道具、特效、风格、动作、姿势——一切"可见内容"的**素材来源**。身份板、多视图板、场景板、风格图、道具板全走这里 |
| `<Picture N>` | 哪张图**直接就是某个时刻的画面** | 它自己就是首帧／关键帧／尾帧／编辑后关键帧／构图锚，或整段的分镜规划板 |

- **身份板永远不是 Picture。** 官方反规则（ref-en.txt:68）：图若只用来定义角色、场景、服装或风格，不得建独立 Picture 条目，应写进对应 `<Subject N>` 定义里引用。把它写成 `<Picture 2> is the three-view character sheet that fixes …` = 告诉模型"某时刻画面里该出现一块三视图板"，会直接长出板子或换脸。
- **一个 Subject 可引用多张图**（ref-en.txt:48）：多视图身份板是同一个人的多个来源，合并成一句；拆成多个独立 Picture 会被当成多个实体（多出人／角色消失）。
- **编号按类内出现顺序，不要求连续**（ref-en.txt:110）：有几个真帧锚就写几个 Picture，不要为凑连续把身份板塞成 Picture。
- **身份由图像素锁住，正文不重复外貌**：首次清晰出现时提一次（特征＋画面位置＋当前动作，限于本镜真看得见的部分），之后只用标签（ref-en.txt:246）。正文反复复述发型/服装反而会与"画背影"打架。
- 详细判据、错误症状对照与正误写法示例见 [Subject / Picture 分工](references/ref-subject-picture.md) §0／§3b；模型图像上限 9 张、混合总数 12 个、同框身份图 ≤2 张见同文件。
When a render comes back with a known failure mode (extra character/animal, shards, melt, crosstalk, lost beats), look up `references/failure-modes.md` (symptom tier — do not read through while writing).

## Known failure modes (lookup, not load-time)

写词被打回、或成片出现"多出来的角色/动物、碎片、融化、串音、动作丢半"时，打开
`references/failure-modes.md` 查"写法 → 崩坏 → 替代写法"对照表（含出场治理三件套与音频标签自洽）。
**平时写词不要通读它**；加载期只需要记住两条：不出场角色连定义都不写；一时刻一实体。

### 写词前反查（30 秒，只扫触发词，不通读）

上面两条是**出事后**的入口，拦不住「自己不知道正在犯这个错」。下面这张清单是**写词前**的入口：
写完看一眼这几类，有对号的就翻 `failure-modes.md` 对应行。

| 触发词（你的镜头里有这些吗） | 先翻哪条 | 最短结论 |
|---|---|---|
| **手上/身上有没有多出来的东西**（袋子、包、手机、钥匙、道具） | 否定句写在尾部无效 | 否定的力量取决于语法位置。把「手上是什么」写进**首帧状态句**，并点名**唯一允许持有的物体**；末尾写 "no bag" 无效 |
| **同框有几个人**，参考图挂全了吗 | 配角没挂身份板 | 在身份图上限内，该镜**所有出场人物**都要挂身份板，不能只挂主角；超上限的走冻结文字身份段或拆镜（上限与写法见 `references/ref-subject-picture.md`）；配角的脸不会因为同框而自动对齐 |
| 有没有写 **"no XXX" / "without XXX" / "不得出现"** | 正文尾部否定无效 | 正文没有独立的负向条件分支，否定句只是一个可渲染的名词串。改成正向场景写法：把「手上是什么」写进首帧状态句 |
| 画面里有没有**悬空/重影/重复**风险物（屏幕、牌子、手持物） | 换素材只看指标／绝对保持词 | 锁物体画面时同段写明**人物在画内位置**；道具小动作写不住就让道具不出现 |
| 这镜有没有**换素材或改出点** | 换素材只看音频指标 | 必须**同时验画面与声音**；剪辑单写死的来源是真相源，文件名后缀不是质量排序 |
| 多人同镜、多人并排 | 出场治理三件套 | 逐一点名站位与朝向；对整组人的行为，文字锁没有力量，改词两次仍在就改参考图几何或机位 |

**优先级口诀**：手上多出东西 → 查首帧状态句；同框人不够像 → 查身份板；写了否定句 → 全部改成正向写法。完整对照表见 [failure-modes.md](references/failure-modes.md)（含"他没有拔剑"被画进画面等案例）。

## Output Rules

- Write rewrite sections in English; preserve dialogue, lyrics, and visible scene text in their original language.
- Describe each shot by composition, subjects, environment, actions, camera, sound, and the exact point where referenced content appears.
- Preserve action agency and causal order from the creator: specify which subject and limb cross a boundary first, where the contact occurs, and what the other subject does after seeing that invitation. Verify that the reach is visible in the destination space before the response.
- An accepted first frame defines the accepted appearance. Newly revealed garment surfaces still follow that identity; visible new cuffs, stripes or trim need review against the character design.
- Avoid plot summaries, unresolved reference labels, and timing that does not match the requested duration.

## Body Consistency Rules（2026-11-06）

H3 把写下的时间线读得很字面，所以代价最大的失败是提示词**与自己矛盾**或**与自己的输入矛盾**，而不是少一个氛围词。
官方的时间码、`<Picture N>` 标签、`(Sx)` 与声音段是模型语法，照写；要管的是它们之间是否一致、是否绑到了对的东西上。
没有固定槽位：不要为每镜补一段画质清单、一句"全程保持"、一句"画面无文字"。成稿后按下面八条逐条读一遍。

**1. 第 0 秒等于真正的首帧；构图帧不是第 0 秒。** 动笔前先看（或读计划里描述的）首帧：0.000 秒时画面里有谁、手在哪、持什么、光什么样，原样写。
图里有、而 0 秒时还没有的人或物，写它入画的时刻。参考图的 `用途` 决定标签怎么写，不要一律写成 "opening composition"：

| 图的用途 | `subject_definitions` | `retention_analysis` | `detailed_description` |
|---|---|---|---|
| 起始帧（图就是第 0 秒） | `<Picture 1> is the first frame of [Shot 1], showing …` | `<Picture 1> ([Shot 1] first frame): fully_preserved - …` | `The shot begins from <Picture 1>: …` |
| 构图（图是镜内某一刻，锚定机位、取景、光向） | `<Picture 1> is the composition anchor for [Shot 1]: it fixes <这张图要守住的几项：机位 / 取景 / 光向>, and shows the arrangement reached around <画面证明计划里的时刻>.` | `<Picture 1> ([Shot 1] composition anchor): partially_preserved - <守住的几项> hold for the whole shot; positions and poses at 00:00.000 are set by this shot and reach the picture's arrangement near <该时刻>.` | 在它对应的时刻写：`Around <该时刻> the arrangement of the frame corresponds to <Picture 1>: …` |
| 结束帧（图是最后一刻） | `<Picture 2> is the last frame of [Shot 1], …` | `<Picture 2> ([Shot 1] last frame): fully_preserved - …` | `The shot ends on <Picture 2>.` |

构图帧对应的时刻取自分镜 `画面证明计划` 的时刻列。这三种写法用的是官方 ref-en 的自然短语（`the shot begins from` / `the shot's keyframe corresponds to` / `the shot ends on`），对成片的效果没有做过 A/B；出片后第一件事是实看第 0 秒是否等于预期。

**2. 时间线单调，因果有序。** 时间码在正文里自上而下递增；反应不早于触发（她僵住发生在他开口之后，不是之前）；每个动作落在分镜 reads 对应的时间窗里，R3 的内容不要写进 R1。
同一镜内时间码倒退，闸门 G11 只给 warn，但它几乎总是真错。

**3. 台词有起点。** 每句 `<d>` 前后有一个明确的开口时刻或区间，口型动作和说话人在同一句里；依赖这句话的反应排在它之后。时长按 `h3-video-gate` 的口径估（约 4.1 字/秒）。

**3b. 多人对话按实际发言顺序交替写，不要按人归类。** 剧本里 ABAB 的对话，正文与声景也必须 ABAB；`(Sx)` 按首次发声先后编号，不按角色固定。事故经过见 [case-notes.md](references/case-notes.md) §I。

**声景不写说话事件。** 说话属于画面事件，写进正文（`<Subject 1> (S1) says, <d>[Chinese] …</d>`）；`overall_soundscape` 只描述整段持续的环境声音，不写 says/speaks/murmurs/sings，也不写引号台词——官方 base-en.txt:154 要求它只用 1–4 句英文描述整段声床，重复台词会让模型念两遍。闸门 G19/G40 会提示。

**3c. 台词时间码按字数铺，不按句序均分。** 按每句汉字数÷语速估时、先填满可用窗口，超出时砍句数或加长段；估时口径见 `h3-video-gate`（约 4.1 字/秒）。41 汉字塞 6 秒的事故经过与公式见 [case-notes.md](references/case-notes.md) §I。

**4. 一件事只在它发生的地方说一次。** 服装、道具、光在它入画或变化的那句里写；不在开场句、主体句、结尾句各写一遍。
开场风格句取项目画风基准的一两句话（介质、镜头质感、光），不展开成皮肤、织物、颗粒、景深的清单；整段正文末尾不追加"细节总结"。

**5. "全程 / for the entire shot / in every frame / the whole time" 只给整段真不变的事实。** 会动的东西按时刻写：`<部位或物件> <状态> until <时刻>, then <变化>`。
写完搜一遍这几个词，逐个对照时间线（G38 会列出它们）；与首帧不同的状态更要小心——绝对词会把前后写成互相打架的两个句子。

**6. 机位和光取自账本，不凭习惯。** 见下面 *Camera Motion Mapping* 与 *Light and Exposure*。单镜里 `[Shot 1]` 那句 locked-off 取景本身就是锁，写一次；不要再另加一句"摄影机全程保持距离"。多镜容器里不写全程性的机位句，各 `[Shot k]` 写自己的取景，也不把多张场记卡写成一个固定取景。

**7. 声音事件有来源、有起点；底声写一次。** 同一个底声（冰箱、灯丝）不要在声景里换着说法写两遍；对白留在 `detailed_description` 的发生处。

**7b. 开场第一声：除非要的就是一记冲击，否则先起持续层（2026-11-07 实测）。** 模型对"第一个声音"的权重最高，你写什么它就放大什么。声景第一句若写"门被推开"、"杯子放在桌上"、"他清了清嗓子"，成品第 0 秒会是一个满刻度的短促冲击，听感是"开场突然啊一声"。判据：这一镜的开场要不要一个有意的冲击音（撞击切、惊吓、产品开箱的第一下）？要就直接写，并把它写成有意为之的那一记；不要，就让声景先起持续层，动作音落在它上面。

   - **写法**：声景先起持续层，再让动作音落在它上面。
     ```
     overall_soundscape: A steady low room tone with the soft hum of a refrigeration unit,
     distant night traffic beyond the window, and rain ticking on the glass;
     over this continuous bed, a door closes somewhere off-screen at about 00:02.
     ```
   - **不要这样写**（把动作音放在最前）：`overall_soundscape: A door slams. Then room tone.`
   - **成因**：每段独立生成，声音起点不继承上一段；开场没有"已经在响"的基准，模型就用最响的那件事开场。给它一个持续底层，它就有东西垫着，不会甩冲击。
   - EP002 实测 16 段里 3 段命中开场爆音，最狠的两段第 0 秒就是 −5.6/−6.4 dBFS（接近满刻度），随后掉 53.3/42.6 dB——那 0.3 秒完全是废的，戏在 1 秒后才开始。成因见 [failure-modes.md](references/failure-modes.md)「开场爆音」案例。

**8. 画面文字只写存在的，且必须用英文双引号逐字写死。** 场景里有招牌、菜单、屏幕、灯箱、霓虹，就用**英文双引号**把上面的字原样写出、不翻译：`a glowing light box reading "母婴店"`（官方 `base-en.txt:146` §4.5）。场景没有文字就什么也不写，但**不要指望"不写"能压制文字**——见下面第 9 条。
   - 只写"一个发光的灯箱"而不给引号内容，模型会自己编字。2026-11-07 EP002 实测：灯箱只写 `a glowing pink-white light box on the right of frame`，成片里凭空长出英文 `mother…` 招牌。这不是模型不行，是没给它文字身份。
   - **反向也成立**：真要有字就必须给引号内容，否则它编的和你想要的不一样；宁可用"字迹不可读"把可读性降下来。
正文里"某些表面保持无文字"的整句是一个可渲染的名词串（见 failure-modes 的"画面无文字无水印"行），而且常与场景里真有的菜单板自相矛盾。

**9. 不要靠写 `no subtitle / no text / no watermark` 压字幕——本项目实测无效，且可能反向。** H3 `cfg=1` 没有独立负向通道，那句否定只是给模型一个可渲染的名词串。压文字靠正向可见状态（无标识墙面、纯色布景、明确遮挡、景别紧到不含牌面）+ 生成后 OCR 扫描挑片；分镜正文否定与 hdr 见 [failure-modes.md](references/failure-modes.md)「无文字水印」行与「角色/动作描述里写数值」行，H3 是否适合某项见 `../video-studio/references/craft/h3-script-fit.md` §5。


## Style Anchors from the Official 3D-Animation Skill

H3 `cfg=1` 没有独立负向通道；把需要的东西写成正向可见状态（官方 Pixar 正向句与 R2V `fully_preserved`/`partially_preserved` 为默认，短句否定按语义核对、不因 `no/not` 判失效）。源码论证、六项画风禁令原文、未决冲突与 A/B 计划、参考锚四子字段、正文否定案例表、渲染前剥离分镜标记，全部见 [case-notes.md](references/case-notes.md) §J；正文否定的落地立场另见 `../video-studio/references/craft/h3-script-fit.md` §5，失败症状对照见 [failure-modes.md](references/failure-modes.md)。

## Camera Motion Mapping

镜头怎么放、动不动、动多少，**取自本镜的场记卡（机位、高度、焦段、景别、运镜）和分镜的「运镜」一行**。
正文把它翻译成可执行的英文几何句；不凭习惯统一写成固定，也不另外发明运镜。账本与分镜不一致时回上游改。

下表是**句式词库**（来自 storyboard-30s 独立短片体系），在场记/分镜给出对应运镜时取用，不是每镜必选：

| 场记/分镜的运镜 | H3 句式（写进 `detailed_description` 的 `[Shot N]`） |
|---|---|
| 缓慢匀速向前推进 | `The camera pushes in at a slow, even speed, moving from <起幅> toward <落幅>.` |
| 缓慢匀速向后拉开 | `The camera pulls back at a slow, even speed, opening from <起幅> out to <落幅>.` |
| 水平左右横移 | `The camera trucks sideways to the <left｜right> at a steady pace, keeping <主体> in frame.` |
| 垂直上下摇摄 | `The camera tilts <up｜down> steadily, travelling from <起幅> to <落幅>.` |
| 360° 缓慢环绕镜头 | `The camera arcs slowly around <主体>, keeping <主体> centred as the background slides past.` |
| 斯坦尼康跟拍 | `The camera tracks with <主体> in a smooth Steadicam follow, holding <距离/关系> steady.` |
| 固定机位 | 取自场记卡：写出景别、机位高度、轴线侧，并说清这一镜为什么不动、画面里什么在动；不套固定句式 |

### 落位规则

1. **每个 `[Shot N]` 写一句本镜的运镜**，带起止时间（与时间码同句或紧邻）。场记写"固定"就写固定——但固定也要让执行端知道取景和画面里什么在动；这些按本镜需要选写，不是逐项填的清单。
2. **移动要写起幅→落幅**的景别或构图变化，以及触发它的那一拍；只写 "push in" 不写推到哪里，终点由模型决定。场记写了幅度（"极缓推近，不超过 5cm"）就把幅度写进去。
3. **容器里每个成员镜保持自己的场记卡**：成员的机位、景别、高度各成一个 `[Shot k]`，切点写叙事动机（见 *Native Multi-Shot*）。不得把几张卡写成一个固定取景。
   导演要的是"不切"的连续画面时，由上游把成员合并成一镜一卡（回改场记与分镜），视频阶段不自行合并。
4. **构图锚点图的写法**见 *Body Consistency Rules* 第 1 条：构图帧锚定机位与取景，不当第 0 秒。
5. **一次生成里有跨切时**，`summary` 用一句交代整体镜头逻辑（如 `the camera follows her gaze out of the screen and finds him`）。
6. **禁止把运镜写成风格词**（`cinematic camera` / `dynamic movement`），必须是可执行的几何描述；单镜固定镜头里 locked-off 的取景句本身就是锁，不要再另加一句"摄影机全程保持距离"——多镜容器里那一句会覆盖各 `[Shot k]` 自己的取景。

### 失败模式

- 正文无运镜句，或全片都是同一句 `holds a fixed framing` → 成片"原地呼吸"，像会动的漫画；
- 只写运镜词不写起落幅 → 模型把镜头运动做成随机漂移；
- 几张不同机位的场记卡合并成一个 `[Shot 1]` 的固定取景 → 景别、高度、轴线侧的设计全丢（example-project 实例：三张卡合并成一段 13.67 秒固定中景）；
- 场记写推镜、正文写固定 → 以正文为准，场记白写。


## Light and Exposure

证据与完整自检在 `references/case-notes.md` §B（暖灯笼光色观测）与 §B 子节「EP001 首帧续接的亮度观测」。通则：

1. **色温取自账本中的实际光源与状态。** 同源同态的数值冲突先核对上游；不同光源、空间或时刻有已确认差异时按原设定写，不为统一数值改光源。同族两个色温是否导致亮度波动，只是案例 §B 的待验证假设，不能据此删改合法光源。
2. **只写有上游依据的光变。** 账本与分镜明确的开关灯、闪烁或经过不同照明区，保留触发、时刻与结果；稳定光源按稳定状态写。`brightness pulsing`、`flashing`、`brightens then dims`、`exposure shifting` 等变化词仅在这些依据成立时取用，不为氛围额外添加。
3. **表面色彩与受光取自已接受的场景和画面。** 冷色墙面、地面、木构件或有色照明都可按事实保留；仅当上游明确表面中性时才写中性，不把案例里的 RGB 等比表述套到所有表面。
4. **起点亮度关系照实际首帧或上游状态写。** 用本镜实际物件说明最亮处与暗部；后续变化按账本中的因果与时刻展开。已有光照设定上，整体压暗或改色的氛围词也须有上游依据。
5. **同一时刻、同一表面的描述相容。** 颜色或受光确实变化时交代原因与时刻，分别写清前后状态。

EP001 三段首帧都比送进去的图暗一档、且逐段叠加变暗（读数、OpenCV 解码 caveat 与 A/B 验证方案见 [case-notes.md](references/case-notes.md) §B 子节「EP001 首帧续接的亮度观测」）；出片后量第 0 秒用 `seam_check.py` 看 `luma_mean.change_pct` 与 `within_shot_envelope`，没有通用阈值。

## Occlusion Transitions（遮挡转场，摘要）

场景要换、又不想留切点时，用"遮挡扫过"：遮挡期间画面信息量趋近于零，模型换成什么都看不见。四个要素缺一不可：
**具体的遮挡物**（红裙、红绸、肩膀、人群，不写 blur/wipe）/ **来向与去向** / **遮挡程度**（`swallow the frame`、`fills most of the picture`）/ **露出什么**，
再加一句镜头没停：`the camera travels on through that sweep, one unbroken move, as <遮挡物> clears`。
遮挡转场里不写 `cut` 词，也不写 `without cutting`（带 cut 的词是正向条件）。
完整句式、自检、失败模式在 `references/case-notes.md` §C；段间手法的整体选择和本通道实测见 `../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md`。

两段独立生成的视频，拼接处必然有纹理与运动模式的突变：叠化遇到有人物的帧会重影，硬拼会"顿一下"。所以成片上的长运动不在剪辑层拆段；必须拆时接缝只落在全屏遮挡帧或全屏色块帧上，或走生成层接力（见下）。实测数据在 `references/case-notes.md` §D。


## Shot Joining: Three Layers（2026-11-04，调研落库）

连续性问题先在**层**上选，再在手段上选。默认不要从「两段怎么拼得看不出来」开始想。

| 层 | 要解决的问题 | 手段 | 什么时候用 |
|---|---|---|---|
| **L3 叙事** | 该不该切、切在哪、切给观众什么 | match on action / 视线匹配 / 180°·30° / 景别推进 / J-L cut | 切点有信息增量，或需要节奏 |
| **L2 生成** | 切点怎么被生成出来 | `[Shot N]` 原生多镜；`flf_chain` / `context_pin` 接力 | 单次 ≤15s 装不下，或必须分次 |
| **L1 成片** | 接缝怎么藏 | 遮挡 / 叠化 / 硬拼 + 光流 | 已在剪辑层拆开、无法重生成 |

优先级：**L3 → L2 → L1**。先在叙事上决定要不要切，再在生成上决定怎么接，最后才在剪辑上补接缝。只有「已经在剪辑层拆开、且无法重生成」的两段，才进入叠化/硬拼/变速流程。

### L3 的六条切点语法（可直接写进英文正文）

| 术语 | H3 落点 |
|---|---|
| Match on action | `[Shot 2] At 00:03.000, the camera cuts to ... as his hand continues to lift the cup` |
| Eyeline match | 上一镜 `he looks off-screen left`；下一镜给目标物或 `what he sees` |
| 180° 规则 | 每镜写明人物在画面左/右，并保持不变 |
| 30° 规则 | 换角度时同时改景别或机位方向，不要只挪一点 |
| 景别推进 | wide → medium → close-up → detail → reaction → wide |
| J-cut / L-cut | `<scenetrans>` + 官方四个表述之一（建议优先用，见下条） |

## 跨镜连续性表述（官方 §4.4，四个表述）

镜头之间的"接上了"，在正文里**不靠形容词，靠官方给的四个表述**（官方原文是 "may be expressed with"，即「可以用这四种」）。同一句台词/歌词跨切点时，在**两侧**都放 `<scenetrans>`，并明说音频跨切继续（`base-en.txt:142`）：

| 情形 | 官方表述（原样照抄，不要改写） |
|---|---|
| 声音跨切继续 | `continues seamlessly across the cut` |
| 延续到下一镜 | `continues uninterrupted into the next shot` |
| 从前一镜接过来 | `carries over from the previous shot` |
| 整个过渡期间仍可听见 | `remains audible across the transition` |

台词被视频结尾截断时用 `<cutoff>`。

```text
[Shot 1] ... she says: <d>[English] I get off at the next station,</d> and the sentence carries over from the previous shot.
[Shot 2] At 00:03.500, the camera cuts to ... <scenetrans> the line continues seamlessly across the cut.
```

**建议直接用这四个官方表述**（例如 `her voice continues across the cut before the picture changes` 这类自创句未验证，效果不保证——仓内没有同义句的对照实测）。

**注意分工**：这四个短语只解决**声音**跨切。画面上的空间连续要另外靠帧锚（I2VA 首帧 / 真实末帧），不能指望一句话把画面接上。

## Native Multi-Shot `[Shot N]`（官方 §4.2；本地约束见下）

官方原生支持单次生成内多镜：

```text
[Shot 1] Live-action, cinematic, a medium-wide shot frames...
[Shot 2] At 00:03.500, the camera cuts to...
```

- 第一镜不加时间戳；后续镜头以严格递增的切镜时间开头。
- 切镜动词：`the camera cuts to` / `the shot cuts to` / `the shot transitions to` / `the shot changes to` / `the shot switches to`。
- **切点必须引入新信息**（主体/空间/状态/视点/时间）；只是距离或轻微角度变化，优先运镜。
- 镜内 cut 共享一条连续音床（社区实测）；跨切点台词用 `<scenetrans>` 声明音频继续，并配上文「跨镜连续性表述」里那四个官方短语之一（自创句未验证），截断用 `<cutoff>`。
- 一镜到底就**只写一个运镜**（不加 `no cuts` 这类否定短语——官方没有这个词组，而且它会被否定词回读当成待核对的边界）。写多个 `then` 串联的运镜会被 prompt expander 拆成多镜并产生硬切（Fuser 实测：三段运镜 → 1.58s / 3.67s 两个硬切）。
- 多镜时自己写 shot list 和切点时间；必须保留的道具按本镜可见状态写清（如 `the same rough travertine plinth`），不把逐字重述上一窗道具、外貌或环境当成通用硬规则。原 relay 的逐字重复要求仅见下文对应案例。
- **FL2VA 默认单镜**；多镜必须显式声明切镜动词（未声明多镜会在本地格式自检里报出）。

### 本地 h3q 约束

- adapter 走 I2VA（单首帧）/ FL2VA（首尾帧）/ Ref2VA（参考图组），**不支持纯文生**。
- **多窗容器已接入 V2**（选路先读 `../h3-queue/SKILL.md` §2.14：默认单镜 pdd，能拆就拆，只有同机位同场景且接缝必须无缝才用多窗）：`workflow=multishot` 走 `multishot_render_ref.py` → `H3MultishotMemorySampler`
  （模板 `<渲染机根目录>\config\multishot-v2.json`，`context_pin`、`pin_frames=22`、`seed_per_shot=True`、
  `self_anchor_voice` 默认开；渲染器另有 `--no-voice-anchor` 开关，但 **h3q 队列链路不转发它**，
  走队列时改不了）。两窗之间用单独一行 `---` 分隔，接缝由模型在 latent 层处理。
- 因此本地**有** `context_pin` 生成层接力；`flf_chain` 不在当前 V2 模板里，需要时单独部署
  ComfyUI-H3-Motion-Context。
- 写 V2 多窗时：每窗写自己的时间线与可见状态即可，**不必逐窗复述上一窗收尾状态**——`context_pin`
  已把前一窗末 22 帧钉进下一窗，重复描述可能与上一窗的收束句冲突。换机位、换主体或正文自身需要交代
  起点时才重述。
- **同场连续的场景锚用视频片段，不要用图片**（2026-11-19 EP005 S-002 实测）：给 `scene_video`
  指向上一镜已验收成片，正文写 `<Video 1> is an earlier moment of this same continuous scene:
  this shot keeps its framing, its close camera distance, its room contents and its warm colour
  temperature`，再把房间/机位描述逐字写进每一窗。只靠文字描述房间会被整个重画（近景变远景、
  家具换位置）；把场景图塞进 `refs` 则会被当成某个 `<Subject N>` 的照片。构图必须与上一镜的
  实际画面一致，不要凭印象写「桌子在画面中央」这类与源片不符的描述。
- **静默窗会自己编台词，调参压不住**：ref2va 拿到人物+场景参考后倾向给静默段补人声。
  官方 2.6.0 记录无声窗逐字复述 voice anchor；本地 A/B（bank_clip_frames=5、
  audio_pin_frames=3、窗长 141→226）都不能消除。能做的：①静默窗段落不要指望开关解决——`self_anchor_voice` 只钉声线、不保证环境床连续，关掉反而引入已实测的音色漂移；
  ②正文写具体的声音（room tone、脚步声、呼吸），不要只写「没有对白」；③不要写「张嘴/唇动清晰
  但没有配音」这类会诱发补词的描述；④台词必须逐字正确时用 `guide_audio` 预录整条时间线锁死，
  或后期把静默窗音频换成真实底噪（002 这类台词都在前一窗的镜头最适合这条）。

## Seam Design: Airlock / Land Settled

旧 relay 链路已不用；气闸六条规则、矛盾并集、双机制与长链漂移量见 [case-notes.md](references/case-notes.md) §K。当前以 `../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md` 与 multishot V2 为准。

## Generation-Layer Relay vs Edit-Layer Splice

判型与选路的唯一权威源是 `../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md` §0.1（含"创作者反馈还有硬切"的三分支判型）；本表只做词侧速览，与它冲突时以它为准。

| 方案 | 接缝两侧是什么 | 适用 | 代价 |
|---|---|---|---|
| `context_pin` | 同一段 raw latents（22 帧重叠，重生成 0.92s 后裁掉） | 真无缝首选；本地 V2 `multishot` 已内建 | 无需额外部署；走 `workflow=multishot` |
| `flf_chain` | 上一镜末帧作为下一镜首帧（fl2va continuation） | 无第三方依赖 | 每镜要做气闸（原 relay 案例） |
| 镜内硬切 | 同一次生成内的 cut，共享音轨 | 切点有信息增量 | 必须有叙事理由 |
| 遮挡转场 | 单段内遮挡帧 | 无精确时刻要求 | 遮挡物必须具体 |
| 后期叠化/硬拼 | 两次独立采样 | 已在剪辑层拆开、无法重生成 | 纹理/运动突变不可避免 |

优先级：**生成层接力 > 镜内硬切 > 遮挡 > 后期拼**。两段独立生成 + 叠化是最后手段，不是默认方案。

**本地 h3q 上的实测补充（2026-11-05，七组真实渲染，当时的 lu2 draft 512×896；该档 2026-11-15 已退役，现役 pdd draft 为 1024×576）**：

| 方案 | 实测帧差 | 结论 |
|---|---|---|
| 两段独立生成，正文写"接着上一段继续" | **41.87** | 在该案例条件下观察到后段从参考图姿势重演 |
| `flf_chain`：上一段真实末帧做下一段 `first_frame` | **3.38** | 在该案例条件下视觉接上；不证明运动/声音继承或其他镜头通过 |
| 遮挡过渡（把画面遮满） | 三组全败 | 参考图"能看见脸"压过正文 |
| 光线变化（关灯/车灯） | 成功 | 不依赖前段状态 |
| 插入镜（换主体） | 成功 | 不依赖前段状态 |

这些读数只支持当时案例的选择，不构成通用帧差阈值。正文声明“接着上一段”不能传递实际媒体；需要连续时，按剧情选择容器、已验收真实帧视觉接力或重新设计。
`flf_chain` 在本地是单帧接力，会放弃 `reference_image`；不是原生视频上下文续接，也不与两端插值的FL2VA混称。当前输入组合查 [h3-queue](../h3-queue/SKILL.md#输入能力与续接职责)。

## Failure Retry Ladder (official STEP 7)

When a shot renders badly, escalate in this order instead of regenerating blindly. **Before any
step, check the look first:** if the take regressed against the project's look baseline (short-drama-review
`look_check.py`), the fix is to remove whatever degraded input caused it (a composited/edited reference,
a frame extracted from a rejected or drifting take), not to add constraints.

1. Re-render with a strengthened prompt that reinforces the spatial anchors **folded into the scene sentences** (never quote an explicit `reference_anchors:` block — it disturbs set dressing, see above).
2. Cut that shot to ≤6s, move the trimmed seconds to a new adjacent row, re-run the
   shot-table self-check, then re-render.
3. Switch the shot to an alternate model or step setting **only if the actual submission path exposes it**
   (the local h3q queue currently does not; see h3-queue §2.5). Never bypass the queue to reach another preset.
4. Two look-passing attempts that still miss the same story fact, or three failures overall on the same shot:
   stop and ask the user — relax one requirement (drop a prop / simplify the action / lower hook strength),
   move the fact to edit/post, or skip the shot with a `placeholder: missing clip` marker.

**Never** "repair" by compositing, pasting, vector-drawing or locally editing a reference image to force a
layout. The model learns the composite's flat fills and mismatched light as the look, and every later take
that inherits it gets worse.

## Production Presets (measured 2026-10-18 on RTX 5070 Ti 16GB; engine 更新 2026-11-15)

This table records the historical lu2/Sol presets (full basis in the internal production-freeze record, not published in this repo). **Current channel (2026-11-15): only `pdd`** — `draft` runs the PDD 8-step first pass at 1024×576 (`--no-upscale`); `final` adds a second pass up to 1536×864. `lu2` / `legacy` / `tier: legacy` are retired and rejected by both adapter and MCP, so the three-tier rows below are **pre-2026-11-15 lu2 measurements kept for comparison only**. pdd `draft → final` has no latent continuation (`draft_job_id` / `draft_accepted` are no longer read). Multi-window containers use `workflow=multishot` (V2 sampler), which is not an engine/tier. Current contract: `../h3-queue/references/produce-adapter.md`（PDD 引擎见 :22、档位见该文件的「视频档位」节）与 `../h3-queue/SKILL.md` §2.14（multishot）。

- **历史 lu2 draft（896×512，4 步 Turbo LoRA）**：46s–3m05s/段（311–362 帧）。画质软（放大 1.5× 有糊感）。
- **历史 lu2 final（latent 放大二采）**：2026-11-04 起 >300 帧不再受限。二采引擎默认 `split`（MMH3 Ultimate Upscale 时间分块，chunk 136 / overlap 17），实测 311 帧与 362 帧 → 1920×1088 全部通过，单段 16–19 分钟。`--refine-denoise` 默认 0.30（保形点）；`--tile-size` 必须为 0（空间分块会产生镜像伪影）。
- **历史 lu2 legacy（原生 1344×768，20 步 + `spark_mode speed`）**：实测 350 帧 12m32s、311 帧 ~15min。渲染完成后 scp 中断可从 `<渲染机产物目录>\<slug>_<run>_<frames>frames.mp4` 手动拉回。
- **Offline finding**: audio is weakest at 8 steps and usable from 12 up. Judge each take's audio in review instead of refusing the only available path.

## Continuous-Relay: Facts That Carry Over

逐段 `first_frame` 续接时，模型只收到英文正文和那一张末帧；写在文档头、分镜、制作记录里的锁都不会到达模型。
所以**本段可见内容碰到的事实**必须在正文里出现；碰不到的不写。

1. 只写本段会入画、会被动的东西：画面里能看到的服装件、会出现的单实例道具（在它入画的那句写明手里只有这一件，如 `the one fork in her hand`）、本段内会变化的状态（哪件东西到哪一刻为止留在哪）。
2. 写进它发生的那句里，不集中成 `Throughout:` 块，也不把整部片的锁逐段原样复制进每条正文。
3. 绝对词（"全程""for the entire shot"）的使用条件见 *Body Consistency Rules* 第 5 条。
4. 机位不是锁项：本镜机位来自场记卡，动与不动都由 `[Shot N]` 的运镜句写。
5. 制作记录写清每段首帧来源（上一段**真实解码末帧**，`ffmpeg -sseof -0.05 -i <上段> -frames:v 1 <tail>.png`）和抽帧命令；不用另出的关键帧，也不各自独立起链。
6. 接缝验收逐条对应本片已出现过的穿帮（多出一把叉、第二颗草莓、已抹掉的状态回魂、极端特写伪影），每条一个可见量和一个裁切点；"检查连续性"这类泛句不算。

代价：走 `first_frame` 接力即放弃 `reference_image`，身份一致性只能靠已验收的那一帧加正文里的事实。这是有意取舍，不是默认路径；用 Ref2VA 六段时仍由 `subject_definitions` / `retention_analysis` 承担身份。


## Tips for Better Results
- Always match the total duration of the description to the requested video length (4–15 seconds).
- Keep reference labels consistent (e.g. `<Picture 1>`, `<Video 1>`, `<Audio 1>`) across every section.
- Prefer concrete visual and audio details over abstract words like "cinematic" or "beautiful". Abstract emotion words on crowds ("laughing and talking") collapse into smiling, slowly drifting figures; concrete verbs work (`lean against the guests' shoulders, wave wide sleeves, tilt heads and giggle behind raised hands`).
- When using keyframes (I2VA / FL2VA / L2VA), clearly state how the first and/or last frame connects to the timeline (Body Consistency Rules, item 1).

## Community Preset Corpus (ostris, 1000 official-format prompts)

`references/ostris-presets.json.gz` ships 1000 finished H3 prompts in the exact official
syntax (same corpus the official prompt-rewriter LoRA was trained on; credit: ostris).
20 styles x topics; 430 entries in the documentary family (documentary / film-stock /
live-action-cinema / surveillance / vhs-camcorder). Query it with the bundled local script `scripts/h3-preset` (pure local, read-only; run as `python3 scripts/h3-preset ...` from this skill directory):

    python3 scripts/h3-preset --list-styles
    python3 scripts/h3-preset --style documentary --topic animals-nature --n 3
    python3 scripts/h3-preset --id 000244 --full
    python3 scripts/h3-preset --style film-stock --seconds 10 --n 2

Use presets as few-shot anchors or ready-made seeds BEFORE asking a model to invent
structure: they encode shot grammar, <d> dialogue, (S1) speaker ids, camera
type+amplitude+speed, soundscape and music lanes correctly by construction.

## Case Notes（按需，不是加载期材料）

`references/case-notes.md` 收着从具体项目沉淀的实测：每节带着当时项目的物件和数字，只取方法、不取物件。写词时不要通读。入口：

| 节 | 什么时候读 |
|---|---|
| A 连续飞行镜的运动复刻 | 本镜明确要求全程飞行/连续推进，且要对齐源片运动量 |
| B 暖灯笼复刻的光色观测与假设 | 查该片读数、待验证假设与可比区域的限制 |
| C 遮挡转场完整手法 | 摘要不够用时 |
| D 跨段拼接的顿挫与鬼影 | 已在剪辑层拆段、必须选接缝实施方式时 |
| E T8 Creative DNA | 简报描述的是一个可重复的节拍模式（问候、揭示、追逐落点） |
| F 打戏配方 | 冲突/打脸/追逐戏 |
| G 一镜到底多空间状态链、人群表演 | 单次 ≤15s 内连续走通多个空间；人群镜 |
| H 门/容器状态锁与起始帧几何 | 画面里有门、门洞、容器的开合状态 |
