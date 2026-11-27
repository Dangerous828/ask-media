# 每集创作文件（2026-11-25）

每集只维护这几类文件。它们是同一套创作事实的不同承载，不是多套并行文档：

```text
剧集/<EP>/
├── 剧本.md              # 故事 + 视觉 canon + 导演 + 逐镜 prose + 接缝说明
├── 制作清单.yaml        # 唯一生产台账（assets / shots / bindings / submit / seams）
├── 场记.md              # 一集一本：空间、轴线、机位、光位、道具、时间线、接缝
├── 脚本/
│   ├── image/IMG-*.txt  # 一图一个：可复制图片提示词正文
│   └── motion_*.txt     # 一镜一个：可复制视频提示词正文；多窗一文件
├── 制作成果/            # 产物，不是文档
└── 审查/look/*.look.json # 准入运行数据，不是举证
```

项目根另需 `short-drama.json`（跑 `project_tool.py init` 生成）。缺它时 `production_tool prepare`
直接拒绝，所以新项目第一步是 init，不是先写文件。它记语言、画幅、集数与 `production_profile`
（实际出片通道的能力档案）；用户点名目标模型后要把选择写进这里，只写在会话里下一轮会退回通用路径。
字段与改法见 `short-drama/SKILL.md`。

不再创建 `创作方向.md`、`视觉设定.md`、`导演.md`、`分镜.md`、`图片提示词.md`、`视频提示词.md`、
`视频提示词-文档正文.md` 或 `设定集/场记.md`。旧项目已有的六文档视为 legacy，迁移时按下面的归属并入；新项目不得再建。

## `剧本.md`

一份文件承担创作正文，按节组织：

| 节 | 内容 |
|---|---|
| 集标题与场次 | `# EP001 集名`；`## EP001-SC001 内/外 · 地点 · 时间`；对白、`[VO]`/`[OS]`/`[SFX]`/`[画面文字]`/`[连续性]`/`[转场]` |
| `## 视觉 canon 与导演` | 画风基准（`- LOOK-<ID>：<路径>《<名>》` + `- 认可依据：<谁> <何时> 认可<什么>`。这两行缺任一行，`prepare` 会以 reference acceptance failed 拦住全部镜；`认可项：`／`待补证：` 不是硬校验——它只对写了「已认可/creator_ack」的资产行出 **warning**，`creator_markdown_check` 不拦）、色盘、运镜收尾固定词、人物/造型/地点/道具识别锚点、导演的观看终点/策略/参考边界/逐场行动/空间声音 |
| `## 分镜` | 逐镜 prose：来源、目的、景别机位、机位锁、构图、运镜、起点、唯一动作、表演、终点、转场、画内文字、声音；每镜 `### 观众 reads` |
| `## 接缝说明` | 本集所有段/窗/镜之间接缝的结构与理由；无接缝也要写“无”并说明 |

规则：

- 视觉锚点与导演决定不另建文件；它们直接写在 `## 视觉 canon 与导演` 下，用二级/三级标题分人物、地点、道具、导演。
- 逐镜 prose 是分镜正文；镜头 ID（`SHOT-...`）写标题，正文不重复生产字段。
- 不在剧本里写 `制作清单` 的 `assets`/`submit`/`hash`/`refs_order` 等生产数据；需要指路时写文件路径和 ID。
- 不再写“视觉依据：《视觉设定.md》”这类跨文件指针；视觉事实就在本文件，正文直接引用条目名。
- 不写审查报告、迁移账、复核记录或“为什么”的举证段；有未解决项就改唯一真源。

## `制作清单.yaml`

唯一生产台账，schema 为 `shot-manifest/v1`；字段、校验和命令见
`short-drama-produce/references/shot-manifest.md`。

- `assets`：身份/场景/道具/关键帧资产，带版本、`sha256`、`admission`。`admission.status` 只能是
  `accepted` / `creator_original` / `reviewed` / `unset`；写别的值，**只要这个资产被某个镜头的 `bindings` 引用**，
  校验器就报错（没被引用的资产不查这一项）；画风基准取 `accepted` 的那条。
- `shots`：每个生成单元一条；`technique`、`status`、`frames`、`prompt`（指向 `脚本/motion_*.txt`）、
  `keyframes[].prompt_ref`（指向 `脚本/image/IMG-*.txt`）、`bindings`、`submit`。
  - `keyframes[]` 每项必填 `id`/`role`/`read`/`at_s`/`use`/`prompt_ref`：`at_s` 是**镜内**时刻（与本镜
    `### 观众 reads` 同一把尺，不是全片绝对时间）；`use` 写这一格的生产或审查用途，必填、取值自定，
    常用 `start_check`。
  - `submit.output` 必须是**文件路径**且扩展名与模态匹配（视频 `.mp4`），不能写目录。
- `seams`：`inter`（跨生成单元）与 `inner`（multishot 窗内）；`join`/`reason` 用枚举，不写 prose。
- `decisions`/`conflicts`/`drift`/`qc`：只放类型化引用和状态，不抄剧情。
- 不把剧情、台词、分镜正文、视觉 canon 抄进清单；清单只存生产数据和指针。

## `场记.md`

**一集一本**，放在 `剧集/<EP>/场记.md`，不按项目共享。它记录本集可核对的事实：

- 空间与轴线：地点、轴、固定锚点、机位侧。
- 调度卡：`CARD-...` 与镜头/窗口的对应；机位高度、距离、俯仰、景别。
- 光位：主光方向、色温、屏幕/道具光。
- 道具与状态：杯、手机等在本集内的起止状态。
- 时间线：段/窗/镜的时间范围。
- 接缝：`## 接缝说明`，与 `制作清单.yaml` 的 `seams` 对齐。

场记是 prepare 阶段的工作，不是生成后的补救；下游只引用账里的值，不重新描述机位、光位、站位。

## `脚本/image/IMG-*.txt`

一图一个，只放**可复制正文**：角色板、场景板、道具板、状态图、关键帧等。文件头可写 1–2 行用途/参考约束；
正文按目标图片模型方言写。清单里的 `keyframes[].prompt_ref` 必须指向这些文件；不在剧本/清单里重复整段提示词。

## `脚本/motion_*.txt`

一镜一个，只放**可复制正文**：单镜写一段；multishot 一文件多窗，窗间用单独一行 `---` 分隔。
清单里的 `shots[].prompt` 必须指向这些文件。正文遵守目标视频模型方言：H3 单镜也要以 `[Shot 1]` 开始，
一窗多镜才依次写 `[Shot 2]`、`[Shot 3]`，且第 2 镜起必须带切镜时间 `[Shot 2] At 00:03.500, ...`；
编号在整个文件里连续递增（跨 `---` 也算），第 2 镜起每镜都带时间，不能每个窗口都从 `[Shot 1]` 重来——单窗模式下闸门会机械核对编号，multishot 模式只核每窗首字符，跨窗连续靠写的时候自己守；台词包进 `<d>[Chinese] 逐字原文</d>` 并在前面给说话人 ID `(S1)`；
不写 `no cuts` 这类 H3 不认的否定短语；一镜到底只写一个连续运镜。方言细则见
`short-drama-video-prompts/references/minimax-h3.md`，写完用 `h3-video-gate` 过一遍。
台词只放逐字原文：`<d>[Chinese] 都听见了。</d>`，说话人放在 `<d>` 前面的 `(S1)`，不写进台词里。
ref 模式与配了系列角色的项目里，闸门会按已定义的名字检查，`<d>角色名：都听见了。</d>` 这种
「名字+冒号」开头会被判成把说话人标签写进台词正文。
台词所在的动作句前写明开口时间（`At 00:00.500, ...` / `Between 00:01.000 and 00:02.000, ...`），
闸门靠它估算台词时长；缺了只 warn，但时长对不上就查不出来。
multishot 过闸门时 `--shot-count` 必须等于文件里用 `---` 分隔出的窗口数，对不上是 error；
每窗帧数从清单 `frames_per_shot` 传给 `--frames`，不给就只核内容不核时长。
传 `--storyboard <各镜秒数>` 会跑 G33 切点对账；不传就跳过这项（切点没人对账）。
对账算法见 `h3-video-gate/SKILL.md`。

## 审查与产物

- `审查/look/*.look.json` 是 `look_check`/`ref_gate` 的准入运行数据，可以保留；它不是审查报告，也不是创作真源。
- `制作成果/` 放图片、视频、成片；路径由 `制作清单.yaml` 的 `submit.output` 指向。
- 不再创建 `审查/<EP>-*.md` 这类审查报告/迁移账/复核记录。需要“举证”说明链路还有未解决项：先解决，把结论写回剧本/清单/场记/prompt 文件。

## 所有权

| 文件/节 | owner |
|---|---|
| `剧本.md` 故事与场次 | `short-drama-write` |
| `剧本.md` `## 视觉 canon 与导演` 的视觉条目 | `short-drama-assets` |
| 同节的导演决定 | `short-drama-direct` |
| `剧本.md` `## 分镜`、`## 接缝说明`、`场记.md` | `short-drama-storyboard`（场记可由主路由协作） |
| `脚本/image/IMG-*.txt` | `short-drama-image-prompts` |
| `脚本/motion_*.txt` | `short-drama-video-prompts` |
| `制作清单.yaml`、`制作成果/` | `short-drama-produce` |
| `审查/look/*.look.json` | `short-drama-review` |

同一文件的不同节可以由不同阶段追加/更新；不得为了并行而复制出第二份“视觉设定/导演/分镜/提示词”文件。
需要指路时写 `剧本.md` 的节名、`制作清单.yaml` 的 ID 或脚本文件路径，不写行号。

## 检查

```bash
python3 {short-drama}/scripts/creator_markdown_check.py 剧集/<EP> --project-root .
python3 {short-drama-direct}/scripts/director_check.py 剧集/<EP>
python3 {short-drama-produce}/scripts/shot_manifest.py validate . --manifest 剧集/<EP>/制作清单.yaml
python3 {h3-video-gate}/scripts/h3_gate.py 剧集/<EP>/脚本/motion_<NNN>.txt --frames <清单里的 frames>
```

`creator_markdown_check.py` 检查文件存在、旧文档缺席、剧本/场记的必要节、清单指针与脚本文件；
`director_check.py` 检查 `## 视觉 canon 与导演` 与 `## 分镜` 的字段、关键帧用途、`reads` 是否覆盖本镜时长；
`shot_manifest.py` 检查资产/镜头/接缝/提交字段；`h3_gate.py` 检查提示词方言。
四个都只报事实，不判断创作质量。逐镜写完就跑前三个，写一条 motion 就跑一次闸门——
不要攒到最后，报错会串在一起分不清是谁的问题。

改这两份契约文档本身时，跑 `tests/test_contract_claims.py`：它把文档里每条「会报 error」
变成一次「改坏 fixture 确认真被拦」的回归，两边脱钩就红。新增一条拦截措辞时在那里加用例。
