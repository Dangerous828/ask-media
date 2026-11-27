---
name: short-drama-produce
version: 1.0.0
description: 在创作者明确确认后，执行短剧项目的图片、视频、TTS/配音或时间线音乐生产任务，并把结果与精简运行记录落回项目。用户说“生成这张图/这段视频/这句配音/这段配乐”“开始跑图/跑视频/合成语音/生成音乐”“把已确认提示词送去生产”，或要求批量执行已确认媒体任务时使用；不负责创作提示词、镜头、台词、歌词或声音身份，也绝不把预览、继续、预算说明或既有接受状态当作本次付费生产确认。
license: MIT
---

# 确认后生产

本技能只负责把已经写好的生产规格安全送到运行环境配置的 adapter。图片提示词仍归
`$short-drama-image-prompts`，视频提示词归 `$short-drama-video-prompts`，台词与录音表归
`$short-drama-write`，声音身份归 `$short-drama-assets`。


## 确定性检查（跑并贴输出，不作放行依据）

三类必跑脚本（台词逐字比对、来源场景 ID/场记卡引用、H3 提交前格式与算术）及 warn/硬拦截边界的统一口径见 [short-drama](../short-drama/SKILL.md) §确定性检查；本阶段照跑并把输出贴进交付说明。

## 自看硬规则

任何产物出来都要自己看过才往下走：**视频一秒一帧，闸门过了不算看过。** 完整细则与"什么叫不算看过"见 `ask-media` 技能的 `../../../ask-media/references/discipline.md`，本条不复述。

## 语料与剪辑准备的继承

消费当前分镜与提示词中已落实的证明段、状态与接续素材需求。条件未定先回 owner；生产不临场改戏。按真实产物复核可用带及运动余量，clone 定格不算真实运动余量；新生产仍遵守本次授权与逐条验收。完整分工与就绪判据见 语料机制与剪辑准备（`short-drama` 技能 `../short-drama/references/mechanism-preparation.md`）。新增散文条件由人工回读，现有检查器不自动核验。

## Quick Start

只在用户明确要求实际生成后，从当前 `脚本/image/`、`剧本.md（分镜节）` 或 `脚本/motion_*.txt`
取出本次提示词，建立一个有边界的运行 job。`source` 指向拥有这条提示词的当前 Markdown；
creator-first job 必须点名 `source_entry` 选择器，并逐张填写 `reference_bindings`，
带真实参考图却缺绑定的 job 直接失败、不替它猜 role。选择器映射（`IMG-*` / `MOTION-*` /
`SHOT-*#KF-*`）、KF role 与正文的对应、`用途`↔provider role（含 MiniMax / Seedance 取值）、
参考音频绑定、`PLAN-...` 与 `references` 镜像的失败边界，全部见
[adapter-contract.md](references/adapter-contract.md#job-file)，本节不复述。

从新结构清单建 job（不提交、不连渲染机）：

```bash
python3 scripts/manifest_job.py <project> \
  --manifest 剧集/<EP>/制作清单.yaml --shot <SHOT> --output job.json
python3 scripts/production_tool.py prepare <project> --job job.json
```

`manifest_job.py` 支持视频单镜/多窗，也支持按关键帧建图片 job：

```bash
python3 scripts/manifest_job.py <project> \
  --manifest 剧集/<EP>/制作清单.yaml --keyframe <KF-ID> --output job.json
python3 scripts/production_tool.py prepare <project> --job job.json
```

创作者自己在工具里出图、产出落在 `剧集/<EP>/制作成果/images/` 后，由分镜 owner 绑成
`用途：起始帧` 的 `REF-...`；图片始终不进项目时走 `PLAN-...`。走 Magpie MCP
（`h3_generate_project_image` / `h3_generate_project_video`）同样要先查参考图并按 schema 传入，
只传 `parameters` 不代表可以不传；确实无参考才走纯文生并在调用记录里写明。adapter profile
未声明接受 `reference_audio` 时 `run` 在提交前失败，见
[adapter-contract.md](references/adapter-contract.md#adapter-config)。本地图片由内置 adapter
按 base64 data URI 送出，不自建上传服务。输出放在 `剧集/<EP>/制作成果/`；这个 job 是生产工具的
临时输入，不计入每集创作文件：

```bash
python3 {技能目录}/scripts/production_tool.py prepare <project> --job <临时-job.json>
```

先展示 `prepare` 的完整预览；此时不会调用供应商。

## 生产清单（多镜 / 多手法）

一集有多个镜头，或同一集混用 `ref2va` / `i2va` / `fl2va` / `multishot` / `motion_drive` 时，先写
`剧集/<EP>/制作清单.yaml`，再由 [shot_manifest.py](scripts/shot_manifest.py) 校验并生成闸门/提交命令。
清单是**生产 build file**，不是第七份创作文档：只承载资产版本、词稿标签、通道槽位与提交参数；
剧情、台词、提示词正文仍归各自 owner。完整 schema、technique 槽位表与迁移顺序见
[shot-manifest.md](references/shot-manifest.md)。

- `validate`：资产 SHA/准入、technique 必填与禁止槽位、词稿标签双向 diff、refs 顺序/subjects 自洽；
  `origin_plan` 不是当前 plan 的镜头给 warning「旧方案复用，需重新核对绑定」。
- `plan`：输出该镜的 `h3_gate.py` 与 `h3qc` 命令；远端 ASCII 路径用 `<REMOTE_...>` 占位，按投递单替换。
- 清单与 job 的关系：清单是 preflight，`production_tool.py` 的 job 仍是执行单元；
  `identity`/`scene`/`prop`/`style` 映射到 job 的 `reference_image`，`audio` 映射到 `reference_audio`，
  `scene_video`/`action_video` 只走 h3qc / motion-drive 直投。
- 闸门只查格式；标签与资产/槽位是否对得上由清单查。两者都过才提交。

## 提交前必须自看

每次生产都必须经过以下四步，顺序不可合并：

1. 建立一个有边界的 job：一种 modality、明确数量、完整 prompt/spec、参考文件、参数、输出路径和 adapter profile。
2. 运行 `prepare`，把返回的完整预览展示给创作者，尤其是数量、prompt、source entry、
   reference bindings、references、outputs、overwrite 与 adapter。creator-first job 会在这一步机械核对
   所选标题里的可复制提示词，以及参考图槽位、顺序、路径、中文名和控制边界；任一漂移都 fail closed。
3. 等创作者在**看到这份预览之后**明确确认。只有明确同意这项当前任务，才运行 `confirm`；
   “继续”“都做完”“预算没问题”、上游内容已接受或之前确认过另一版，都不算本次生产确认。
4. 运行 `run`。它会在启动 adapter 前消费一次确认；成功或失败后再次执行都必须重新确认，
   防止失败重试意外产生第二笔费用。

job、prompt、参数、输出路径或直接输入任一变化，旧确认立即失效。不得代替创作者填写确认。
当前已确认 job 是本轮唯一工作单元；运行结束后回报结果并交还控制权，不自动准备下一批或启动审查。

`剧本.md（分镜节）` 的「输入参考图」路径只是创作阶段的可读依据与使用意图，不是生产输入快照。进入生产时，
creator-first job 必须从 `脚本/image/`、`剧本.md（分镜节）` 或 `脚本/motion_*.txt` 的对应条目建立绑定；
`prepare` 展示的 `reference_bindings`、`references` 与已确认 job 才是本次 adapter 实际读取哪些
文件字节、各自允许影响什么的权威。非 creator 的结构化规格可不填 `source_entry`/`reference_bindings`，
继续只使用显式 `references`；但新的 image/video job 只要 `source` 指向 canonical `脚本/image/`、
`剧本.md（分镜节）` 或 `脚本/motion_*.txt` 就强制使用对应 selector，不能靠省略字段降级绕过。升级前已经 prepare 并落盘的
旧 job 仍可按原指纹读取。
新生产结果不自动回填或刷新分镜；需要把它改为后续输入时，由分镜 owner 修订文档，再建立新 job
并重新预览、确认。

## 视频先出草稿档（硬规则，2026-11-01）

本地 h3q 视频 job 的 `parameters.tier` 缺省就是 `draft`（当前引擎 `pdd`：8 步蒸馏、1024×576 首采，362 帧渲染约 285 秒（片长约 15 秒）；耗时对照用 pdd final 二采 362 帧约 832.3s（≈14 分钟），不是已退役的 lu2 legacy 20 步档（实测约 12.5–24 分钟））。
档位与引擎的**文档层契约**见 `../../../h3-queue/references/produce-adapter.md` 的「视频引擎」（视频引擎一节）与「视频档位」（视频档位一节）两节；**运行时口径以实现实读为准**（渲染机 `h3qc submit --help` / adapter `parameters.tier` 校验 / MCP schema）。本技能只规定创作侧的确认顺序，不在这里重定义档位。

1. 新写或改过的段**先出 draft**，给创作者看构图、运动方向、身份和因果（**竖屏的验收边界见 `../../../h3-queue/references/tiers-and-capabilities.md`**——竖屏 draft 不能当最终构图看，原因与实测在那里）（`prepare` 的 preview 里 `tier_note` 字段会显示 ⚠️ DRAFT）。**草稿只用于验收，不进剪辑，不作为交付素材**。跨会话继续时必须重新确认 tier——缺省就是 draft，不会自动升档；不要一上来 `final`。
2. 创作者认可某段草稿后，才为它建 `tier: final` 的 job；prepare 预览必须能看出这是 final、且对应哪段已验收草稿。`draft_job_id` / `draft_accepted` 是 lu2 时代的 latent 接续凭据，pdd 分支不读取；可以写进记录便于追溯，但不要把它当成 latent 接续承诺。
3. 引擎当前只有 `pdd`：`engine` 缺省即 `pdd`，`lu2` / `legacy` / `tier: legacy` 已于 2026-11-15 下线，adapter 在提交前拒绝，不在 job 里自创档位。要改档位语义，先改 h3-queue 的 PDD 契约与 adapter，再回到这里。
4. 不要绕过 adapter 自写脚本直连 `h3qc`/`h3qg`：那会跳过参考验收、`h3-video-gate` 留档和本次确认。需要新参数就改 adapter。
5. **不要假设 final 与草稿逐帧同版**——draft→final 的语义（完整重跑、无 latent 接续）见 `../../../h3-queue/SKILL.md` 的档位语义节。final 仍须核对实际细节、动作与声音，画质精修不保证修复台词或口型。

## 命令

只在进入生产边界后把当前提示词和运行参数写成临时 JSON；视频与图片 job 的
`parameters.prompt_language` 跟随当前可复制正文已经解析出的提示词语言，使 adapter 追加的参考约束
使用同一种语言，而不是重新回退成固定英文。不要在创作阶段为每条提示词预建 job。
creator-first 本地H3视频若来源明确写了帧数，`prepare` 会核对job时长吸附后的实际帧数；例如328f允许显示13.67s，但确认参数保留328/24秒精度，不统一写15。生成/容器总时长与成员时长分开核对；其他模型按各自档案映射，不套H3网格。取回后同时对来源、job与真实产物对账。
格式和 adapter 契约见
[adapter-contract.md](references/adapter-contract.md)。命令由
[production_tool.py](scripts/production_tool.py) 提供，然后运行：

```text
python3 <本技能目录>/scripts/production_tool.py prepare <project> --job <job.json>
python3 <本技能目录>/scripts/production_tool.py confirm <project> --job-id <id> --confirmation "CONFIRM <id> <code>"
python3 <本技能目录>/scripts/production_tool.py run <project> --job-id <id> --adapter-config <outside-project-config.json>
python3 <本技能目录>/scripts/production_tool.py status <project> --job-id <id>
python3 <本技能目录>/scripts/production_tool.py collect <project> --job-id <id> --adapter-config <outside-project-config.json>
python3 <本技能目录>/scripts/production_tool.py audit <project>
```

`prepare` 只验证并预览，不生产。`confirm` 只保存与当前 job 指纹绑定的一次性确认。
`run` 才启动 adapter。`collect` 只取回**已经提交过、已经计费**的那次任务的结果，
不重新提交、也不需要新的确认——见下面「中断不等于要重跑」。`audit` 只对账本地任务历史、失败后恢复、重复内容尝试和当前输出字节，
不会调用供应商，也不把技术成功、文件存在或哈希一致写成媒体质量结论。同一 job 存在未决
`running` attempt 时禁止重新 prepare、confirm 或 run；先等待完成或排查遗留 attempt。

## 输入选择

- **image**：读取 `脚本/image/` 的当前 `IMG-*` 可复制正文，或 `剧本.md（分镜节）` 的当前 `SHOT-*#KF-*`
  所选角色正文，加上必要参考图和明确的输出尺寸/数量；creator-first job 使用 `source_entry`
  锁定这一条。资产板走 `IMG-*`，镜头静帧按 frame plan 的 role 选择 composition/start/pose_proof/end；
  两者不互相替代，起始帧缺失时不以冻结构图顶替。
- **video**：读取 `脚本/motion_*.txt` 的当前 `MOTION-*` 可复制正文，并核对 `剧本.md（分镜节）` 中对应镜头、
  冻结关键帧、时长与画幅；creator-first job 使用 `source_entry` 锁定这一条。连续段选择从上一段
  生成结果续接时，下一段 job 同时绑定上一段实际视频和从该视频取得的实际尾帧，并保留
  `continuity_video`、`actual_tail_frame` 的不同职责；供应商 role 由目标模型 adapter 翻译。支持原生视频
  上下文续接的入口按其角色组合提交，不以计划尾帧或文字代替真实文件。本地 h3q 不接受
  `reference_video`：若上游要求继承整段运动/声音上下文，就回 video-prompts 重设计。
  单帧续接在本地 h3q 上有**两条**路，别只记得第一条：
  ① **末槽续接**（默认优先）：身份板/场景板照旧挂，把已验收的真实尾帧放进**最后一个参考槽**，
     正文首句写 `The shot opens on the same framing as <Picture N>.`。身份与起点同时保住、
     剪硬切观感无缝（实测见 `../../../h3-queue/references/incidents.md` §2026-11-13）。
     这条路的 technique 是 `ref2va` 多槽，**不是 `i2va`**。
  ② **首帧接力**：把尾帧提交为下一段 `first_frame`，注明只继承可见状态、不继承原运动或音频；
     这条路整段丢掉身份/地理参考，只在不需要身份锁时用。
  首尾配对与全参考互斥，当前范围见 h3-queue 输入能力（`../../../h3-queue/SKILL.md`）。上一段必须已在审查技能
  通过画风验收并批准复用，它的帧才可能进入下一段。creator-first 视频 job 还会把同集 `剧本.md`
  纳入确认输入指纹和私有快照；项目存在 `h3-series-config.json` 时也一并固定，供跨镜身份与时间检查。
  本地 h3q adapter 在上传前逐字核对实际 `<d>` 台词。旧的已确认任务若快照没有剧本会明确标记 NOTCHK，
  重新 prepare 后才启用对账。
- **tts**：从 `剧本.md` 读取原句与表演要求，声音参考由用户或现有媒体明确提供。不得在生产 job
  中改词，也不为 TTS 另建创作文档。表演要求来自这句台词的括注和上下文：执行端接受自然语言语气时，
  写成一句语气说明放在台词前（「憋屈地压低声音，咬着牙应一声：是。」），同一角色每句挂同一段参考音色；
  只接受枚举情绪时映射到最近的一档，再用强度、音调细调。只给音色、不给语气时，短剧台词会念成播音腔。
- **music**：读取 `脚本/motion_*.txt` 中创作者已确认的时间线音乐章节；主题曲使用已确认歌词，纯配乐
  不携带歌词。供应商不能精确承诺时长时，生成源音轨后仍由 `$short-drama-edit` 按文档里的混音意图完成落点、
  循环、淡入淡出和对白 ducking。

一个 job 不混合 modality。大批量工作拆成创作者能看清数量和成本边界的小 job；不为方便把整季
隐式塞进一次确认。

## Adapter 边界

adapter 配置必须在项目外，只包含 argv 命令和超时；凭据由 adapter 自己从进程环境或系统凭据
存储读取。项目 job、确认记录、运行记录和 Dashboard 都不得保存密钥。

脚本以 JSON stdin 调用 argv 数组，不使用 shell，不拼接命令。adapter 返回本地临时文件；工具只
接受与已确认 targets 完全一致的结果，并把完整文件原子复制到项目的 `剧集/<EP>/制作成果/`
目录。项目和上游 Skill 不写死供应商、模型或即将变化的 API。

内置图片/视频 compiler 会根据已确认的 `reference_bindings`，按顺序向供应商 prompt 附加一段确定性的
引用语义说明（中文名、用途、允许控制与不得控制范围）；不会把槽位名误当成要渲染进画面的文字。
外部 adapter 也必须保留这组语义或明确拒绝，不能只上传文件而静默丢失控制边界。

本技能可选提供四个 stdlib adapter，均通过项目外 adapter config 选择，凭据只从运行环境读取：

- [Seedance](references/providers/seedance.md)：模型/Endpoint ID 必须由账号显式配置；compiler 支持
  官方图片、视频和音频参考 role，内置 runtime 未配置可信上传时仍拒绝本地参考文件。
- [GPT Image 2](references/providers/gpt-image-2.md)：无参考图走 generation，有参考图走 edit；
  固定高保真引用并校验尺寸、格式与透明背景限制。
- [MiniMax Music](references/providers/minimax-music.md)：使用 `music-3.0` 与 hex 结果，区分主题曲
  和纯配乐，不伪造时长请求字段。
- [MiniMax 语音](references/providers/minimax-speech.md)：`tts` 模态；模型与 `voice_id` 都必须
  由账号与文档显式给出，不内置音色清单。只从预置音色合成，不做声音克隆——克隆是授权问题，
  创作者授权的参考录音按普通创作者输入走 `输入/`。
- [MiniMax H3 视频](references/providers/minimax-h3-video.md)：模型 ID、分辨率集合与时长区间必须
  由账号显式配置；提示词进 `content` 的 text 项，参考图按显式 role 绑定，本地参考在没有可信上传时
  fail closed。该模型与画面同一次生成声音，写法影响见视频提示词技能的目标模型能力档案。
- **本地 h3q（本机默认视频/图片通道）**：`h3-queue` 技能的 `../../../h3-queue/scripts/short_drama_h3q_adapter.py`，
  adapter profile `local-h3q-video` / `local-h3q-image`，配置示例见 h3-queue「2.8」。它经 h3q 队列
  提交到 <渲染主机SSH别名>，不需要云端 API Key，也绝不直连 ComfyUI。输入组合与部署核验查 h3-queue 输入能力（`../../../h3-queue/SKILL.md`）：
  单首帧、首尾配对或全参考互斥；没有参考视频、参考音频或无图文生。项目档案须采用 `minimax-h3` 方言中的「本地 h3q 通道档案」；
  档案仍写云端 `minimax-h3` 却要走本地通道时，先让 video-prompts owner 改档案和受影响条目再投产。

## 画风闸门（image / video job）

`prepare` 对每个图片和视频 job 做两项机械检查，任一不过直接失败，不预览、不计费：

1. **普通镜头必须已有创作者认可的画风基准。** 《剧本.md》「视觉 canon 与导演」「## 画风基准」至少一行 `- LOOK-...`，且同小节
   有 `- 认可依据：` 行。只有 LOOK 行、没有认可依据的不算。真正的 Look 开发首跑（还没有任何基准）
   由创作者决定，在 job 的 `parameters` 写 `"no_look_baseline_ack": true`，预览里会看到。
   **角色板、场景板、道具板、分镜板属于设计资产，它们定义画风基准，不能在 job 里缺声明后被当成普通镜头。**
   这些 job 必须在 `parameters.asset_kind` 声明 `character-card` / `scene-card` / `prop-card` / `storyboard`；
   未声明导致的 `missing_look_baseline` 是 job 配错，不是项目缺基准，正确修法是补 `asset_kind`，不是改 adapter、
   不是伪造 `no_look_baseline_ack`，也不是跳过 `ref_gate`。声明后闸门仍会检查生成物再作参考的复用审批。
2. **生成物再作参考必须获批复用。** 以下任一情况都视为生成物：放在 `剧集/<EP>/制作成果/` 或 `production/`
   下；字节哈希等于任何一次运行记录交付过的文件（复制到 `输入/` 也认得出）；文件头带生成器标记
   （ComfyUI 的 PNG prompt/workflow 字段）。它必须有
   `审查/look/<项目相对路径>.look.json`，对应当前字节，且最近一条复核是
   `approved`、`use: reference`、剧情层通过；机械 FAIL 只接受最近复核同时带
   `creator_ack: true` 与 `mechanical_override: true` 的创作者实看豁免。自审的还要有创作者确认；
   派生自另一条媒体的，父媒体
   也必须仍是 approved。基准帧本身豁免（它就是标尺）。 **批准动作的时序**：`review → approve` 与提交一次连续做完；写词、改词的轮次只跑词侧闸门（正文结构检查），
   不要顺手对参考资产跑 `measure`/`--audit`——它会给已批准资产追加 `pending`、把 `approved` 打成 `unknown`，
   提交时被 `ref_gate` 拒收，只能重走一遍独立验收才能恢复（EP004 重制实测：此污染两次打断提交流程）。批准状态的字段语义（追加 `pending`、旧批准失效、`ref_gate` 拒收规则）见 `../short-drama-review/SKILL.md` 画风段，本节不复述。

创作者亲手放进 `输入/` 的原始资产（不带生成器标记、也不是任何运行交付过的字节）不受第 2 项限制。

### 身份板覆盖（多参考 job）

挂了场景板、构图帧和道具板，却整组漏掉角色卡时，上面逐张验收全绿——每张图都合法，缺的是「有没有带」。
`ref_gate check` 因此多做一道覆盖检查：**参考图 ≥ 2 张时，至少要有一张可指认的身份板**（路径/中文名含
`角色卡`/`角色板`/`character-sheet`，或绑定的控制范围含「身份」）。设计资产与 `no_look_baseline_ack`
首跑不在此列：它们本身就是在造身份板。这道检查零输入、不依赖执行者记得勾任何选项，produce、h3q adapter、
Magpie MCP 三条路径都走同一个 `ref_gate`，因此都会自动生效。

需要逐角色核对时，在 job 的 `parameters` 里写 `cast`（本镜出场角色名）、`cast_required: true`，
并用 `cast_aliases` 补齐画面代称与简称（例如「角色C」↔「示例角色C」），否则别名对不上会误报。
确属没有身份可辨的镜头（只有手、剪影、空镜），写 `cast_exempt` 并给出 ≥8 字符的具体理由；
理由会回显在 `prepare` 预览与闸门返回里，静默跳过不受理。

`--bindings` 由 produce 与 h3q adapter 自动带上，闸门据此读每张图的「控制」范围。Magpie MCP 的
`h3_generate_project_image` / `h3_generate_project_video` 只传 `parameters`，这一路按参考图路径与中文名
识别身份板，因此角色卡文件名要含 `角色卡` / `character-sheet` 一类可指认的词；仅靠「控制：身份」
声明职责而文件名无标记时，走 `cast_exempt` 或改用带 bindings 的通道。

补覆盖机位、换角度、末帧延展时尤其容易漏：换了机位不换身份，参考组仍要带齐本镜出场角色的身份板，
做法见 `video-studio` 技能的 `../../../video-studio/references/craft/base-action-coverage.md`（基础动作 → 覆盖机位）。

上述检查由共享 `ref_gate.py check` 统一执行。默认安装位置是技能中枢的
`../short-drama-review/scripts/ref_gate.py`：`production_tool.py` 从本技能目录按
`../short-drama-review/scripts/ref_gate.py` 解析共享副本，解析不到才回退到同目录的 `scripts/ref_gate.py`；
adapter 侧可用 `SHORT_DRAMA_REF_GATE` 显式覆盖共享副本路径，`production_tool.py` 按这两级解析、不读该变量。
`~/.agents/skills/...` 只是同步目标，不作为默认源。生产私有快照会按原项目相对路径带上
《剧本.md》「视觉 canon 与导演」、当前与父媒体 look 报告及生成谱系，并另存哈希清单；h3q adapter 在首次 SSH、参考处理和上传前
用同一命令再验一次，不能只靠 prepare 放行。闸门拒绝时必须先看返回的 `code` 与 `message`：
`missing_look_baseline` 表示缺少基准或设计资产未声明；`reference_not_accepted` 表示生成物未获批复用；
`cast_identity_plate_missing` 表示整组没带身份板；`cast_identity_reference_missing` 表示某个出场角色缺身份图；
`input_error` 表示项目根或路径不可读。不要用一个通用“参考图被拒”代替具体 code。Magpie MCP 的短剧调用只用 `h3_generate_project_image` /
`h3_generate_project_video`；原始生图/生视频工具不用于短剧项目。`scripts/ref_gate.py` 是单技能
独立运行使用的同字节分发副本，以 review 下脚本为源，仅在共享路径不可用时兜底；修改后必须同步并由
`scripts/selftest.py` 核对。

参考图只用真实渲染、禁止拼贴／贴图／矢量重画／局部修图造“受控布局”(含 2026-10-25 EP001 事故)，见
[AGENTS.md](../../../AGENTS.md) §3；状态造不出来时按审查技能 REV-17 回提示词或分镜。连续生产时可在
job `parameters.executor` 写执行者名，审查脚本据此识别自审。

这些 adapter 是已验证请求契约，不是账号可用性或生成质量保证；正式生产仍必须通过上面的本次
确认闸门，并由审查 Skill 判断产物质量。

仓库自带 `fixture_adapter.py` 只用于离线测试，不代表真实生成质量或默认生产 adapter。

## 中断不等于要重跑

提交那一刻就计费；中断后按顺序做：`audit` 看 `orphaned_provider_job` → `collect` 取回 → 只有 collect 确认失败才重新确认重投。**不要在 `orphaned_provider_job` 时直接重投**（等于为同一镜头付第二次钱）。机制与边界见 [adapter-contract.md](references/adapter-contract.md#recovering-a-submitted-task)。

## 结果与复核

成功后回报实际输出路径、媒体类型和运行状态；不要把“adapter 返回成功”写成质量结论。
多任务或重试后先运行 `audit`：终态失败按 `retryable` 路由，重试仍须新的明确确认；输出缺失或
文件的哈希或大小不再等于运行记录时，先复核当前字节或重新生产。`repeated_content` 只是成本与诊断信号，
不能自动判定同文重试合理或不合理；`running_attempt` 是未决运营状态，audit 必须返回 attention。
失败按三路走。超时、限流、服务端错误这类技术失败可做有上限重试。失败信息点名了被拒的是哪
一项输入——提示词文本、参考图或音频——就先改那一项再投：文本被拒改写那一句，把「一拳砸在
对方脸上，血顺着下巴滴」换成「一拳挥空，对方侧身避开，桌上的杯子被带倒」；参考图被拒换一张
构图与角色一致、画面本身合规的**原生资产或已验收生成物**，不手工修图；音频被拒重录那句台词。改动写进新的 job 重新 prepare，让创
作者在预览里看到改的是哪一项再确认；原样重投的那次确认不产生修复，只产生一笔费用。重复内容
缺陷回到对应 prompt/spec owner。

**同来源同因的质量返工不能靠改名清零。** 同一 `source`+`source_entry`+modality 的最新成功产物带人工 `rejected` 审查时，下一个 job 必须在 `parameters.revision` 写明改了什么；同一原因再失败升级为 `strategy: redesign` 并引用真实上游决定。技术失败与 `collect` 取回不算返工。字段、例子与边界见 [adapter-contract.md](references/adapter-contract.md#quality-revision-imagevideo-retries)；缺陷观察与归因由实际看片的人负责。
生产结束后不自动进入剪辑。素材要装配成成片时由用户点名 `$short-drama-edit`；它只取舍已有帧，
不回头改本阶段的 job，也不生成新素材。
每次回报结果都要写明：**这条媒体尚未验收**，在 `$short-drama-review` 的媒体验收（先画风后剧情）
给出结论之前，它不能被当作下一段的参考、不能进剪辑、不能交付。不在生产调用里自动启动复核；
但用户已授权连续多段生产时，这份授权**同时包含逐段调用 `$short-drama-review` 媒体验收**：每段之间先完成该段验收再准备下一段，不能先跑完全部再统一审。
Dashboard 只负责展示这些文件和运行摘要，不提供 adapter 设置或生产按钮。

## 安装维护

只有安装、升级或排障时运行离线自检；普通创作和生产准备不运行：

```bash
python3 scripts/selftest.py
python3 scripts/provider_adapters.py --selftest
```
