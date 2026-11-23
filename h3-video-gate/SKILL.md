---
name: h3-video-gate
version: 1.0.9
description: H3 视频提示词的格式自检工具：用户说“检查提示词有没有格式错”“跑一下脚本看看”“这份提示词有没有漏标签”，或要排查 Ref2VA 六段/基础模式三段的标签、时间码、参考编号问题时使用。提示词质量与是否提交由 agent 自己逐条核对后决定，脚本结果仅供参考。不负责剧本、分镜、生图提示词。 短剧任务按正文读取对应阶段知识，本技能继续完成当前工作。
---

# h3-video-gate:H3 视频提示词格式自检

## 短剧项目协作（命中即读，保留本职）

本技能运行格式自检并解释问题。需判断短剧时序/动作含义时读 [short-drama-video-prompts](../drama-skills/skills/short-drama-video-prompts/SKILL.md)；内容验收读 [short-drama-review](../drama-skills/skills/short-drama-review/SKILL.md)。脚本 PASS 不代表内容正确，不能当成故事或画风采纳。 规则见 [协作契约](../SHORT-DRAMA-ROUTING.md)。已读上下文复用；只有跨阶段、状态或初始化才读取short-drama主路由。

一句话:提示词写完可以跑 `scripts/h3_gate.py` 找格式错,它只能判格式、标签、时间线、跨镜设定词;口型落点、发音、音色、表演好坏它管不了。是否提交由 agent 自己逐条核对决定,不看退出码,见文末清单与 `references/checklist.md`。

## 1. 两种模式(以官方规范为准)

- ref(Ref2VA)六段,顺序固定:`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`。
- base(T2VA / I2VA / FL2VA)三段:`integrated_multimodal_description` → `overall_soundscape` → `non_diegetic_music`。
- `integrated_multimodal_description` 只属于 base。ref 稿里出现它是 G03 error,不是"缺字段"(早先人工审查把它当 Ref2VA 必填,是错的)。
- 段名顶格、以冒号结尾;只有两个音频段允许写 `N/A`。无配乐写 `N/A`,不要留空(方言实测留空会被补乐)。

## 2. 过闸流程

1. 写稿:文件名带帧数,如 `s1_v5_141f.txt`(闸门从 `_NNNf` 取时长;帧数按 17k+5 规划)。
2. 跑闸:单镜带 `--refs N`(本次实际上传的参考图张数);整集多文件按镜序一起跑并带 `--series-config`。
3. 改:按每条输出里的"改法"修改,一次只改报出的问题,不顺手重写别处。
4. 再跑:重复 2–3。
5. 跑完把输出贴进交付说明;error 逐条改掉,warn 逐条过目:能改就改,保留的 warn 要能说出理由(例如 G18 成人语速快,已用 `--rate` 复核)。退出码不作为放行依据——是否提交由 agent 自己核对后决定;脚本只保证格式、标签、时间线、算术这些确定性项不漏看。
6. 按 `references/checklist.md` 逐条人工核对后,自己决定是否提交生成。

## 3. 命令速查

```
python3 scripts/h3_gate.py FILE [FILE...] [--mode auto|ref|base|multishot]
        [--frames N | --seconds S] [--refs N] [--rate R]
        [--shot-count N] [--storyboard 秒数表.json]
        [--series-config FILE.json] [--json] [--strict] [-v]
```

| 参数 | 含义 |
|---|---|
| `FILE...` | 一个或多个提示词文件;多文件时命令行顺序即镜序 S1..Sn,并跑 series 检查 |
| `--mode` | 默认 `auto`:含 `subject_definitions:` 判 ref,含 `integrated_multimodal_description:` 判 base,都没有 → G01 |
| `--frames N` / `--seconds S` | 总时长(24fps),二者互斥;缺省从文件名 `_NNNf` 取,仍没有则跳过时长检查并报 G12 warn。注意它对所有文件生效,多镜时长不同请靠文件名 |
| `--refs N` | 本次实际上传的参考图张数;缺省跳过 Picture 张数核对 |
| `--rate R` | 中文台词语速(字/秒),默认 4.1;成人快语速可调高复核 G18 |
| `--series-config` | 跨镜一致性配置,示例见 `references/series-config.example.json` |
| `--json` | 机器可读输出(含 findings、summary.exit_code) |
| `--strict` | warn 也算失败 |
| `-v` | 同时列出通过的规则 |

退出码:0 = 无 error;1 = 有 error(`--strict` 时 warn 也算);2 = 用法 / 文件 / 配置错误。
**自检的单位是"你提交的那份文件"**:对整份文件跑,不要用逐块跑的结果或文件里自述的"0 error"拼出整份结论(实测:自述逐块 0 error 的整份文件跑出 63 个 error)。交付汇报里引用自检结果时,必须是对最终提交文件的整份实跑,并说明哪些项目脚本判断不了。

常用:

```
python3 scripts/h3_gate.py prompts/s1_v5_141f.txt --refs 3
python3 scripts/h3_gate.py prompts/s3.txt --frames 107 -v
python3 scripts/h3_gate.py s1_v5_141f.txt s2_141f.txt s3_107f.txt s4_141f.txt s5_158f.txt s6_141f.txt \
        --series-config references/series-config.example.json
python3 scripts/h3_gate.py prompts/s2_141f.txt --rate 4.8 --json
```

Windows 用 `python` 或 `py -3` 代替 `python3`;脚本只用标准库,Python 3.9+。

## 4. 规则表(与脚本中实际存在的 ID 一致)

| ID | 级别 | 模式 | 检查内容 |
|---|---|---|---|
| G01 | error | 全部 | 无法判定 ref / base 模式 |
| G02 | error | 全部 | 段缺失、重复、顺序错、段名不顶格或缺冒号、内容为空、非音频段写 N/A |
| G03 | error | 全部 | 模式混用:ref 稿出现 `integrated_multimodal_description`;base 稿出现 `detailed_description` / `subject_definitions` |
| G04 | error | ref | `detailed_description` 在 `[Shot 1]` 前缺英文风格开场句 |
| G05 | error | ref | 其它段(含第一个段名之前的文件开头文本)引用的 `<Subject/Picture/Video/Audio N>` 未在 `subject_definitions` 出现 |
| G06 | error | ref | 有 retention 条目或在正文被当画面锚点("begins from / holds / matches … <Picture N>")的标签,缺少以 `<Label N> is` 开头的独立定义行。**已写进 `<Subject N>` 定义里引用的素材图豁免**(官方 ref-en.txt:37/:68 要求这类图不建独立行) |
| G07 | warn | ref | 有独立定义却没有 retention_analysis 条目 |
| G08 | error | 全部 | 同一编号在 `subject_definitions` 里定义了两次(同一标签只能对应一个实体);最大 `<Picture k>` 超过 `--refs`。**不查连续性**:官方 ref-en.txt:110 只要求同类内独立编号,`<Subject 1>`+`<Picture 3>` 合法 |
| G08b | warn | 全部 | `--refs` 大于已标注的 Picture 张数:上传了未标注的参考图 |
| G08c | warn | ref | `subject_definitions` 引用了超出 `--refs` 张数的 `<Picture N>`(模型无从解析)。不查连续性 |
| G09 | error | ref | retention 条目格式 `<Label N> (appears in [Shot a]): marker - 说明`;marker 不在枚举内 |
| G10 | error | 全部 | `[Shot 1]` 带时间戳;后续 `[Shot N] At MM:SS.mmm` 缺失、不递增或 ≥ 总时长 |
| G11 | error/warn | 全部 | 时间戳超总时长(error);区间起点晚于终点(error);同镜内倒退(warn);**非画面段(声景/配乐/retention)的时间码超总时长也判 error**——声景只描述整段持续声音,不写逐事件时间轴 |
| G12 | warn | 全部 | 帧数不满足 17k+5;或无法得知时长 |
| G13 | error | 全部 | `<d>` 不成对,或不是 `<d>[Language] 台词</d>` |
| G14 | error/warn | 全部 | `<d>` 前缺 `(Sx)`;Sx 未按首次发声先后 S1,S2… 编号;retention 里出现 (Sx)(error);说话人像已定义主体却没写 `<Subject N> (Sx)`(warn) |
| G15 | error | 全部 | `<d>` 外出现中文 / 全角字符。画面可见文字例外:引号前有 sign/banner/label/subtitle/neon/menu/poster/placard 等载体并带 reads/painted/stencilled 等动词,或引号后接 `is stencilled/painted/printed…` |
| G16 | error | 全部 | 声景/配乐/summary/retention 段出现 `<d>`;声景/配乐重复台词原文;同一句台词在正文出现多次 |
| G17 | warn | 全部 | `<d>` 前后 350 字符内有 off-screen,却没写画内人物 lips … closed |
| G18 | error/warn | 全部 | 台词估时(字数 / rate)超出总时长 0.6s 以上为 error,小幅超出为 warn;不同说话人台词重叠 > 0.3s 为 warn;找不到开口时间为 warn |
| G19 | warn | 全部 | `overall_soundscape` 写了说话(says/speaks…)或引号台词;`non_diegetic_music` 为空串 |
| G20 | warn | 全部 | 正文英文词数不在本闸门阈值 [150, 600]。判据是这个阈值;官方常态 350–500 只是写作参考,对白密集的稿子允许低于 350 |
| G21 | error | base | base 稿用了 Picture 参考帧(带尖括号或官方裸写法 `Picture 1`)却缺对齐首行 `at 0.00 seconds into the target video, <Picture 1> ...` |
| G22 | warn | 全部 | 未被否定的 night / dusk / moonlight(有 series-config 时改用其 `time_of_day.forbid_any`);前 12 字符内有 no/never/not/without 视为否定 |
| G23 | warn/error | ref | summary 开头缺 `[任务类型]` 前缀(warn);类型不在官方枚举内或重复(error) |
| G24 | warn | 全部 | 出现未知尖括号标签(官方只有 `<d>`/`<scenetrans>`/`<cutoff>` 与 Subject/Picture/Video/Audio);`<scenetrans>` 不成对 |
| G25 | error/warn | 全部 | 本地容量/官方训练范围 4–15s；15s 经 24fps/17k+5 向上吸附为 362 物理帧（15.083s），仅 `--frames 362` 或文件名 362f 按该网格放行，显式 `--seconds` 不共享该豁免。节点 `length` 硬顶 3600f（约150s），超节点一律 error。超本地 15s 默认 error；手搓直投通道可显式 `--allow-long-video` 降为 warn（需人工确认分辨率/显存），h3q 常规路径不透传该 flag。Ref2VA 参考视频输入仍为 2–15s（输入侧约束，与生成长度无关） |
| G26 | error | ref | 参考素材超配额:图 ≤9、视频 ≤3、音频 ≤3、总文件 ≤12 |
| G27 | error | 全部 | 分镜双绑定标签泄漏:`[char:…][scene:…][shot:…][dur:…][hook:…]` 不得进入视频提示词(官方 3d-animation skill STEP 7) |
| G28 | error | base | FL2VA 同时加载 Picture 1 与 Picture 2(首尾帧插值)却写了 ≥2 个 `[Shot N]` 且未声明硬切。官方 `base-en.txt:62` 要求 FL2VA 单段;实测分段会在时间码处抽出真硬切。显式声明切镜(`the camera cuts to` / `hard cut` / `smash cut` / `jump cut` / `match cut` / `cuts directly to` 等)的多段放行。官方原文是「generally favors … use multiple shots only when explicitly specified」:本闸门把「未显式声明」按禁止处理,依据是本地 A/B 实测(同种子同首尾帧,三段式在时间码处出真硬切 mad 106.5,单段 18.8,重渲完全复现),不是比官方更严的口径 |
| G29 | error | 全部 | 出现 `negative:` / `negative_prompt:` / `neg =` 字段形态。H3 在 cfg 1 无负向分支(官方 guide §8 + 源码 `samplers.py:610`),该段不参与采样。**只拦字段名形态**:正文里的否定句不在这条拦,由 G36 提醒(官方 ref-en.txt 含 34 处、base-en.txt 含 12 处,官方 3D 动画 skill 自带 6 连「不要…」风格锁,按数量拦必误伤官方原文);`negative space` 构图术语同不受影响 |
| G30 | error/warn | ref | Subject 定义缺可核对的参考来源,或引用了超出 `--refs` 的 `<Picture k>` |
| G31 | warn | ref | **首帧/开场措辞提醒**:`<Picture N> is the first/opening frame|composition`、`begins/starts/opens from <Picture N>`。只提醒不禁止:真实起始帧合法;`用途：构图` 的核心参考画面不是第 0 秒,要改写成 `composition anchor` 并带对应时刻(`h3-prompt-writing` Body Consistency Rules 第 1 条) |
| G32 | error | 全部 | 台词正文无角色名/说话人标签泄漏 |
| G33 | error | 全部 | **切点对账**(需 `--storyboard 秒数表.json`,不给则本门不跑):每个 `[Shot k]`(k≥2)的 `At MM:SS.mmm` 必须等于 `--storyboard` 各镜秒数的累计,报 written vs computed;缺切点报期望时刻;镜号超出秒数表也报。改秒数忘改正文当场拦(船长仓 cutStarts 规则移植,2026-11) |
| G34 | warn | 全部 | **车辆相对运动提醒**：车辆词与景物横移、车横穿、摄影机横移共现时列出，否定提及也可能命中。按机位、朝向、路径与实际参考判断；合法侧视/跟拍可保留，停靠车辆不说明摄影机与车同动。仅为既有横滑案例的查询入口，不自动阻断，不保证模型必然失败。 |
| G35 | warn | 全部 | **设备展示提醒**：屏幕朝镜头等词共现时列出，核是否上游已确认的展示；自己读屏可考虑越肩。否定提及也可能命中，但不判失败、不自动改机位或阻断。 |
| G36 | warn | 全部 | **正文否定回读**：统计否定词并展示前几处，核对与实际输入、动作和声音时间线是否相容。优先正向状态，必要边界可保留；无独立负向分支不证明文本否定失效。只提醒，不按数量或词命中裁决质量。 |
| G38 | warn | 全部 | **绝对保持词提醒**(2026-11-06):`throughout / the whole time / for the entire shot / in every frame / from the first frame to the last` 声明"整段不变"。同一句只计一处;单镜里"摄影机全程锁定"不列,多镜容器里的会列(它覆盖各 `[Shot N]` 自己的取景)。只列出来让人逐个对照时间线,确认同一对象(手、袖口、道具、机位)别处没有被写成会动或换位。实例:先写"左手平放桌沿"、后写"左腕全程贴着下巴" |
| G39 | error | multishot | 多窗脚本无窗口;窗口数与 `--shot-count` 不符;窗口以 `[`/`{` 开头(H3 会当 JSON 解析失败);窗口内写了单镜段名 |
| G40 | error/warn | multishot | 逐窗查 `<d>` 格式与配对(error)、`<d>` 外中文(error)、每窗帧数与时长(error/warn);**说话人 ID 缺失(warn)、台词超本窗时长念不完(warn)、同一句台词跨窗重复(warn)、窗内时间戳超过本窗时长(error)、off-screen 说话人而窗内没写画内人物闭嘴(warn)**。多窗没有段名,所以 G05/G07/G09/G16(依赖 subject_definitions/retention/声景段)在多窗里没有检查对象,不适用 |
| G41 | error | ref | 身份/场景/风格板被建成独立 `<Picture N> is ...` 条目(官方 ref-en.txt:68 要求写进 Subject 定义里引用)。不锚行首,同一行内也查 |
| G41b | error | ref | 官方四类标签之外的裸引用写法(`character reference image 2` / `reference image 2` / `image 2` / `the second reference photo` / `the second image in refs`)。**扫全文**,正文里出现同样判 error;`image 2 seconds` 这类时长用法不算 |
| G42 | warn | ref | 同一 `<Subject N>` 的外貌短语(≥5 词、含头发/脸型/服饰等静态词)在正文里重复 ≥3 句。身份靠图锁,首次出现提一次,之后只用标签(`ref-subject-picture.md` §3b) |
| S01 | error | series | 含 trigger 的文件,`subject_definitions` 缺 must_include 词,或任意位置出现未否定的 forbid 词 |
| S02 | warn | series | 同一角色的身份定义行跨镜不逐字相同(列出差异词) |
| S03 | warn | series | 缺全部 require_any 时间词,或出现未否定的 forbid_any |
| S04 | warn | series | (Sx) 前 120 字符内的角色与 speaker_map 不一致(官方 Sx 按单次视频内先后编号,只提示) |

S05(相邻镜 Subject 数 / 道具)规格里标为不做,脚本没有实现。多文件但不给 `--series-config` 时 S01–S04 全部跳过,输出会注明。

## 5. series-config 要点

- `characters[].trigger`:在全文出现即视为该角色在镜,同时用于定位 `subject_definitions` 里的身份定义行(S02)。
- `must_include` 只在 `subject_definitions` 里找;`forbid` 全文找。
- 想让 S02 不报,跨镜直接复制同一句身份定义,不要改写。

## 6. 过闸后的提交与验收

**唯一提交入口是 h3q 队列（127.0.0.1:8200，经 `h3qc.py`／带参考图时 `h3qg.py`），操作见 `h3-queue` 技能。**
短剧项目经 `short-drama-produce` 调用 `h3-queue/scripts/short_drama_h3q_adapter.py`。禁止用
`h3_submit_ref.ps1`、计划任务、`Start-Process` 或任何脚本直连 ComfyUI 8199 提交——那会绕过 GPU 串行与
显存看门狗。下面只保留与提示词正确性有关的事实：

- 帧数 17k+5 @24fps:5, 22, …, 124, 141, 158, …, 243, …,本地安全上限 362(15s,与 G25 一致);节点 length 网格上限 3592(≤3600f)。非网格值会被向上取整,导致提示词时间码与实际时长错位、尾镜/台词被截;闸门 G12 就是为此。
- 几何:宽高须为 32 的倍数,面积上限 1344×768(横屏)/ 768×1344(竖屏)。**超过 1344×768 无收益**(官方:H3 训练在约 1MP)。
- 机械过闸只证明格式；出片后由 `short-drama-review` 的媒体验收先画风后剧情裁决，闸门 PASS 不是质量结论。

### 闸门留档（每次真实提交都要有一份可复核的证据）

`scripts/gate_evidence.py` 的 `run_archived_gate(prompt, checker, destination, arguments, context)` 为一次
闸门执行建一个**唯一目录**（已存在就拒绝，不覆盖历史），固定保存：实际送检的 `prompt.txt`、冻结的
`h3_gate.py` 源码、可选 `series-config.json`、完整 `gate-report.json`、`gate-stderr.txt` 和带逐文件
SHA 的 `manifest.json`（含 `checker_source`、argv、context、`exit_code`）。执行的是**冻结副本**，所以
原文件在检查期间被改也不影响这次结论；闸门失败同样留全报告。

生产接线：short-drama 的 h3q adapter 把证据放在持久目录 `<handle_path>.evidence/`，并上传证据里那份
冻结 prompt；Magpie MCP 的视频提交把证据放在 `~/Downloads/h3q/gate-evidence/<uuid>/`。手工跑
`h3_gate.py` 不会自动留档，提交汇报里引用的结论必须是**对最终提交文件整份实跑**的那一次。

**不要用新规则解释旧报告。** 规则与阈值改动后，旧证据目录里的报告仍代表当时那一版检查器（哈希可对
源码）；重跑得到不同结论时，是「这次检查」与「那次提交」的差别，不能把新结论当作历史提交的理由。

## 6b. 现行生产档位

> 完整参数与实测见 [h3-queue](../h3-queue/SKILL.md)。本技能只列与提示词/闸门判断相关的部分。

- **引擎只保留 `pdd`**（2026-11-15 起）：`lu2` / `legacy` 已下线，adapter 与 server 两条校验路径都会拒。
- **一采画布**：`pdd` 缺省 1024×576（模板锁定）；16 GB 卡上限 **1536×864**。
- **`sol-profile` 默认 `off`**：Sol 加速档比 off 慢 3.5% 且构图会跑掉，一律不要开。
- **`pdd_lu` 二采**：转发 `--out-width/--out-height`，362 帧到 1536×864 约 832 秒。
- **`--tile-size` 必须为 0**：空间分块让每个 tile 各自重想内容，产生镜像/重复纹样（实测判废）。
- **带首帧/首尾帧的任务不走 `pdd_lu`，因此没有二采**：`pdd_render_ref.py` 没有 `--first-frame`/`--last-frame`。`h3_generate_video` 与项目 adapter 现在按输入分流——带 `first_frame` 就落默认分支 `h3_render_ref.py`（单首帧 i2va、首尾帧 fl2va），只有挂 `refs` 的全参考组任务才走 pdd draft/final。默认分支没有二采档，要升分辨率走 `h3_upscale_video` 后处理放大（纯 latent 放大、无第二遍扩散、构图与音轨原样保留）。转场卡做法见 `h3-queue/references/transcard.md`。
- **多窗容器总帧数上限约 450 帧**：这是显存物理上限；adapter 对显式 `workflow=multishot` 只告警不拦截，超限 OOM 风险自负。
- **切点时长**：本地安全档 4–15 秒（16G 容量/训练范围）；15 秒经 24fps/17k+5 向上吸附为 362 物理帧（15.083 秒）。节点 length 可到 5–3600 帧，超 362f 属容量/质量风险而非字段违规。

**OOM 处置顺序（官方）**：①降 megapixels ②缩短到 5 秒 ③降到 16 步或 turbo 8 ④换 `pruned_w6a8` + int8 VAE ⑤关其他占内存程序。官方提醒「Your tight spot is the 32 GB of RAM as much as the card」——模型共约 40GB 靠部件轮换，跑前关游戏和重浏览器标签。

**商用红线**：H3 许可证排除美 / 欧 / 英 / 韩，商用需另购授权。

## 6c. `--strict` 下的时长红线：刻意短镜**没有声明入口**

G25 短端提示语写着「延长到 ≥ 4s 或确认这是刻意的短镜」，但代码里**没有后半句那条路**：`--mode` / `--frames` / `--seconds` / `--refs` / `--rate` 都不承载短端豁免；`--series-config` 的 `load_config()` 只认 `characters` / `time_of_day` / `speaker_map` 三个键；没有环境变量或配置文件入口。长端已新增 `--allow-long-video`（仅把 >15s 的 error 降为 warn，节点 3600f 硬顶与 <4s 短端都不受它影响），h3q adapter 不透传该 flag。

⇒ **设计上就是短镜的镜头，在 `--strict` 下结构上不可能 exit 0**，与素材好坏无关。

实测（《咕角色C嘎》EP01 v5 定稿 8 条，`--refs 2 --frames N --strict`）：v5_03 / v5_04 各 90 帧（3.75 s）→ exit 1（G25 warn），依据是剧本写明计划时长 3.5s；v5_09 124 帧按 `--rate 5.5`（成人急促呼喊）exit 0，音频实测未截断；其余 5 条 exit 0。

**处置口径**：G25/G18 这类**由剧本设计产生**的 warn 被 `--strict` 拦住时，按项目验收纪律走「非 strict 复核 + 记录理由」，**不要为了过闸去改剧本时长**（剧本是唯一真源，同 `video-studio/story_check` 的铁律）。汇报时写清「N 条 exit 0 / M 条因设计时长报 warn」，**不要写成"N 条全过闸"**。

补豁免入口（如 `--allow-short "<镜头>,<理由>"`，warn 仍打但不算失败）是**待办**——闸门改动会影响所有在途项目，需单独立项。

## 7. 已知不可机械检查项

闸门通过不等于能用。以下只能人工 / 模型判断或生成后核对,详见 `references/checklist.md`:

- 口型会不会落到最显眼的正脸上(G17 只查有没有写闭嘴)
- 发音是否念对、多音字、儿化
- retention marker 档位选得对不对(G09 只查是否在枚举内)
- 台词在表演节奏上装不装得下(G18 只按平均语速估算)
- 跨镜服装 / 道具 / 污渍状态的连续性(S01 只查配置里的词)
- 同一角色跨镜音色一致(Sx 编号不保证音色)
- **参考图被写成首帧 / 把结果态当起点**(最贵的一条):当某张图**不是**本镜真实起始帧(身份板、三视图、场景板、结果态)时,`<Picture 1> is the first frame`、`The shot begins from <Picture 1>`、`pose and expression fully_preserved` 这类写法会让模型从错误状态开场。闸门对 ref 模式出现这类措辞给 G31 告警;交稿前人工逐图确认"这张图只控制什么、动作从哪一刻开始"。确实是分镜冻结的起始帧(`用途：起始帧`)时,这类措辞是正确写法(见 `short-drama-video-prompts` 的 H3 方言范例)。
- `fully_preserved` 只说明"保留多少",不说明"从哪一刻开始";图与时序冲突时换图或改时序,不要降档来"修"。
- `<Picture N>` 与实际上传顺序是否一一对应
- 风格是否由正文开场句给出,而不是指望风格卡参考图
- 画面可见文字、手部、道具物理是否合理
