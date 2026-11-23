---
name: h3-queue
version: 1.1.2
license: MIT
description: 仅在要往渲染机（RTX 5070 Ti 16GB，SSH 别名按部署配置）真跑出图或出视频时使用——用户说“出片”“出图”“跑视频/跑图”“生成这张图/这段视频”“提交任务”“送去生产”即命中；也用于查队列里有多少任务／自己排第几／还要等多久，或排查 ComfyUI 抢占与 OOM。规定常规任务经 h3q（127.0.0.1:8200）提交；AI-Canvas-tauri 使用自己的 ComfyUI 提交路径，属于明确例外。负责真实任务提交、状态与产物核对；也负责已验收成片的 latent 放大（h3_upscale_video，后处理通道，不重采样）；不编写提示词，不做成片剪辑。**用户要“让角色学/照着一段参考视频的动作做”（视频动作驱动、动作参考、学动作、翻跳、参考视频+参考音轨）时也命中本技能：走不经 h3q 的 ComfyUI 直投通道，先读 references/video-motion-drive.md。** **用户要做“转场卡/接缝中间段/两镜之间插一段/首尾帧接起来”时也命中：用 scripts/transcard.py 一条命令跑完取帧→上传→FL2VA 出片→两端验收，做法见 references/transcard.md。** 短剧任务按正文读取对应阶段知识，本技能继续完成当前工作。
---

# h3-queue：GPU 生产队列的提交纪律

## 短剧项目协作（命中即读，保留本职）

本技能继续核对并经h3q提交真实任务、追踪结果。短剧实际生产先读 [short-drama-produce](../drama-skills/skills/short-drama-produce/SKILL.md) 的本次授权与输入/产物记录要求，仍由本技能执行本地队列通道；不额外安装adapter或另开审批。单纯查询排队/显存/OOM和下载既有文件不启动创作。 规则见 [协作契约](../SHORT-DRAMA-ROUTING.md)。已读上下文复用；只有跨阶段、状态或初始化才读取short-drama主路由。

一句话：**常规出图/出视频经 `h3q` 提交；用户授权使用 AI-Canvas-tauri 时，允许该应用直接连接 ComfyUI 8199 提交，无需经过 h3q。** AI Canvas 直连不会获得 h3q 的显存预检、幂等与项目参考图闸门，提交前确认 ComfyUI 与 h3q 当前任务状态，避免与其他 GPU 任务并发。

## 入口与环境

- **最低 ComfyUI 版本（以实际部署为准）**：H3-Image 需 v0.45.0+、Qwen 2.1 Turbo 需 v0.40.0+、H3 视频需 v0.30.0+（Multishot 建议 v0.34+）。此处 Turbo 指权重/节点支持版本，与已退役的 Turbo LoRA 出图档不是一回事。
- **版本口径**：同一部署可能出现多个"版本号"（`comfyui_version.py` / `pyproject.toml`、`git describe`、运行实例 `git commit` 不一致）。判断当前版本只看 `comfyui_version.py` / `pyproject.toml` 的实际值；`git describe` 与提交号受仓库 tag / 工作树状态影响，不作为版本依据。特性是否可用以 `/object_info` 中节点是否注册为准。具体以实际部署为准。

## 0. 队列速查：先入队，轮到再检查显存

- **任务已获本次生产授权，输入与闸门已通过，就先入 h3q。** 项目 MCP 用 `wait=false`，CLI 省略 `--wait`。保存 `job_id`，再查状态或排位。当前 GPU 忙、显存低或显示 `occluded`，都无需在调用端等卡空；轮到任务执行时，由 h3q worker 查 ComfyUI 和显存，必要时回收或等待。
- **查谁在跑，先看 `h3_queue_status` 的队列视图（不带 `health`）或 `h3qc queue`。** `occluded` 表示 ComfyUI 有运行中或待处理的任务。`external_running` / `external_pending` 是 ComfyUI 的计数，包含 h3q 自己派发的任务。只有核对同一时段的 h3q 活动任务和 ComfyUI 队列后，才能判断是否有绕过 h3q 的任务。`up for Ns` 表示距上次健康探测成功的时间；判断是否重启要查进程或日志。
- **看任务跑到哪一步：读 `progress`，不读「~left」。** `h3qc queue`、`h3qc show <jid>`、`GET :8200/queue`、`GET :8200/job/<jid>` 和 MCP `h3_queue_status` 对正在运行的任务都带 `progress`：`phase`（`loading_models` 载模型 / `sampling` 采样 / `starting` 刚开始）、当前采样阶段的 `stage`、`step/total`、`pct`、`sec_per_it`、`stage_eta_s`，以及 `log_age_s`（ComfyUI 日志距今多久没写）。数据来自 ComfyUI 日志（`logs/serve.log`）里本任务开始之后的 tqdm 进度条。
  - **只给当前阶段的进度，不给整任务百分比。** 一个任务有多个采样阶段（总步数各不同，每段从 0 起，如 8 步一采、20 步二采），整任务总量事先未知，编造会不准。
  - **`~left` 是同类任务历史中位数减已用时**，345 帧、两小时的任务它会一直显示几秒。`overdue: true`（已用时超过中位数 1.5 倍）出现时，以 `progress` 为准。
  - **判断是不是卡死看 `log_age_s`**：采样一步可能几分钟，进度条几分钟才动一次，但日志文件一直有写入，`log_age_s` 会反复回到几秒内；持续变大（比如超过 10 分钟）且 `step` 不变，才是真的停了。2026-11-21 EP003 的 345 帧视频动作任务全程 5m42s/步、共 7000 秒，期间进度条就是这样慢。
  - 任务刚开始、日志里还没有本任务的内容时 `phase=starting`，不是故障。
- **查询超时记为状态未知。** 已有 `job_id` 就按原 ID 查询；提交响应不明时先核对既有记录，确需重试使用原 `idem_key`。健康查询超时可改查队列，不凭超时判断空闲或重启。

### 为什么必须走队列

这张卡 16 GB，H3 常驻约 14 GB。多个会话各自直连 ComfyUI 提交时，后到的任务多要一点显存就 OOM，CUDA context 变 sticky（连 `cuMemGetInfo` 自己都开始报错），实例挂掉，**所有会话一起停摆**；而各客户端超时后又重提交，一次偶发 OOM 被放大成"互相阻断"。

历史证据（2026-10-20 实测）：`serve.log` 里 505 行 `CUDA error: out of memory`、578 个 Traceback；空闲时显存仍被占 14.1/16.3 GB。

**为什么空闲还占 14 GB（2026-11-21 定位并修复）**：ComfyUI 的 smart-memory 默认把模型留在显存里等下个任务，启动参数里没有 `--disable-smart-memory`，所以 H3 权重约 14 GB 常驻。队列原先只在 preflight 请求 `/free`（开跑前），任务结束路径没有任何释放动作，于是跑完就僵在那儿，直到下个任务 preflight 才可能被清。现在 `run_one()` 在 `set_state(done/failed)` 之后统一调 `release_vram()`，成功和失败都释放——崩溃的渲染同样留着 14 GB，不该让下一个任务继承。`/free` 实测 5 秒内从 13.9 GB 回落到 462 MB。

队列解决的是**准入控制**，不是排队本身（ComfyUI 自带队列本来就是串行的）：

| 失效模式 | 队列的做法 |
|---|---|
| 多会话同时提交 | 单一 FIFO；`idem_key` 幂等，同一任务只有一条记录 |
| 显存接近打满 | 任务照常入队；轮到执行时由 worker 检查，必要时请求 `/free` 回收，仍不足则等待（`blocked_vram`） |
| 任务跑完显存不回落 | 每个 job 结束（成功或失败）自动调 `release_vram()` → `/free`（`unload_models`+`free_memory`），日志留 `release_vram: models unloaded after job <jid>` |
| 客户端超时/断线 | 提交立即返回 job id，人走了也不会变成重复渲染 |
| 开机没起 ComfyUI | 看门狗发现后自动拉起，队列挂起等待 |
| ComfyUI 有运行中或待处理任务 | 健康状态显示 `occluded`；worker 等执行窗口。查任务归属用 h3q 队列和 ComfyUI 记录对照 |

## 1. 三条硬纪律

1. **常规任务经 h3q 提交；AI-Canvas-tauri 是例外**。用户在 AI Canvas 里运行该应用的 ComfyUI 工作流时可直接提交 8199；此例外不扩展到 `curl POST /prompt`、`render_qwen.py`、`h3_submit*.ps1` 或其他工具。先检查 ComfyUI 和 h3q 的运行情况，避免 GPU 任务并发。
2. **禁止重启 / kill ComfyUI 来"解决问题"**。卡住先查队列状态和显存，再决定；重启会打断别人正在跑的活。
3. **任何会重试的调用都必须带 `--idem-key`**。超时重投、脚本重跑、agent 自我纠错都算。同一个 key 提交多次只跑一次。
   - **key 要能区分"不同的活"**：同一提示词换 `--seed` 或换输出名是另一张图，key 里就得带上 seed／输出名。
     实测事故：4 档提示词 × 3 seed，key 只写了档名，**12 次提交只渲出 4 张**——其余 8 次被幂等去重，
     `--wait` 对去重后的旧 job 照样返回 done，`rc=0`，客户端看着全成功（`h3qc.py ls` 里只有 4 条记录）。
   - **本地任务记录按jid原子合并**：并行查询/取回只能写回本次变化，不把网络调用前的整份旧快照覆盖其他任务。提交响应和真实job id先持久化；发现本地丢记录时先按已有id取回，不额外重投。
   - **提交成功 ≠ 产物存在**：幂等去重让二者脱钩。交付前**逐张校验文件存在且非空**，别用"数张数 / 看 rc"代替产物核对。（short-drama adapter 已在取回后自动核对视频非空、帧数与音轨。）

**参考图来源纪律（与三条硬纪律同级）：** 任何带 `--refs` / `--first-frame` 的提交，参考图只能是创作者原始资产、
已登记的画风基准，或经 `short-drama-review` 的 `look_check.py` 以 `--use reference` 批准、剧情层通过的生成物。
脚本拼贴、贴图、矢量示意、局部重绘、裁片、从未验收或被拒视频里抽的帧，一律不得作为参考提交。
短剧项目通常经 `short-drama-produce` 或 Magpie MCP 的 `h3_generate_project_image` / `h3_generate_project_video`
项目感知入口提交；两者都会调用共享 `ref_gate.py` 做参考图准入校验——这是整条链上唯一会硬拦截的两处之一（参考图必须真实存在、`PLAN-` 不得投产、生成物作参考必须有 `审查/look/*.look.json`），因为它挡的是误花 GPU 与错挂参考。AI-Canvas-tauri 是用户授权的独立提交例外，应用不会自动执行该闸门，使用项目参考图前仍须核对其准入状态。手工 `h3qc/h3qg` 与原始
`h3_generate_image/video` 仅供非短剧任务或创作者原始资产，不用于短剧生成物复用。

**两条通道的档位语义一致（2026-11-05 对齐，2026-11-15 起为 PDD）**：`short_drama_h3q_adapter.py`（skill 侧）与
MCP 侧（独立部署的 magpie-h3-mcp 服务，不入本仓库）的 `h3_generate_video` / `h3_generate_project_video` 实现同一套
`engine=pdd`、`tier=draft|final` 语义，参数名一致（`tier`、`width`、`height`）。**改其中一边必须同步另一边**，
否则同一句指令走不同入口会拿到不同行为。
pdd 的 `draft → final` 是两次完整采样，**没有 pass-1 latent 接续**；`draft_job_id` / `draft_accepted` /
`from_latent` / `refine_denoise` / `chunk_frames` 是 lu2 时代字段，pdd 分支不读取，不要用它们推断
「交付的就是验收过的那一版」。档位矩阵与实测见 §2.8。

## 输入能力与续接职责

本地短剧 adapter 接受以下互斥组合；真实生产前核对当前服务端白名单与渲染路径，客户端有参数不等于该部署端到端已验证。其他技能的档位/模式说明引用本节及§2.8，不另维护一套能力表。

| 输入组合 | 可承担的职责 | 未由此保证的内容 |
|---|---|---|
| `reference_image` 有序多图 | 按正文的身份、地理、道具与构图范围生成 | 不是精确首帧；冲突属性不能因已准入就全保留 |
| `first_frame` 单图 | 从真实起始图的可见状态开始；可选已验收前段尾帧做视觉接力 | 不携带前段运动/声音上下文，不能称原生视频续接 |
| `first_frame + last_frame` | 首尾帧插值（FL2VA，转场卡/中间段 C 就用这个），adapter已有成对校验与透传 | 两端和中间仍须验收；与全参考互斥，不能另挂身份图 |

没有 `reference_video` / `reference_audio` 或无图文生入口。**要让角色学一段参考视频的动作（含参考音轨）走另一条通道，不经 h3q**：见 [references/video-motion-drive.md](references/video-motion-drive.md)。原生视频上下文续接要求实际视频输入，不能用一张尾帧冒充。若只需要继承可见状态，上游可明确选择单帧视觉接力；需要精确两端时可选首尾帧，不预设每一刀都走同一路线。

**首帧/首尾帧一律走默认分支，不走 pdd 草稿档**：`pdd_lu` 调的 `pdd_render_ref.py` 没有 `--first-frame`/`--last-frame`；2026-11-22 实测同一对首尾帧、同 107f、同 seed，pdd_lu 产物首帧与指定首帧 MAD **43.0**，默认分支 **3.86**。现在按输入自动分流：`h3_generate_video` / 项目 adapter 只要带 `first_frame` 就落到 `h3_render_ref.py`（单首帧→i2va，首尾帧→fl2va），不再拼 `--workflow pdd_lu`；只挂 `refs` 的全参考组任务照旧走 pdd draft/final。两帧按渲染器语义传 ComfyUI `input/` 里的**裸文件名**；经 h3q 提交时 `sol_profile` 缺省落 `off`。**转场卡直接用 `scripts/transcard.py`，别手搓命令**——见 references/transcard.md。项目内的活（produce 那条路）还要先把两端帧过参考准入（`look_check` assess→review→approve --use reference），`ref_gate` 会把未批准的帧挡成 `reference_not_accepted`；`transcard.py` 是通道级工具，不替你走这道准入。

`draft → final` 查§2.8：pdd 两档各自完整采样，`final` 会产出新 take，不依赖同 seed、也没有 latent 可续；交付前须对 final 本身重新验收。图像精修不保证对白、口型或声线正确。

## 2. 怎么提交

**提交入口是渲染机侧私有定制脚本，不随本仓库发布。** `h3qc.py`（队列客户端）、
`h3q.py`（队列服务）、`h3qg.py`（带参考图闸门的提交包装）、`h3q_img.py`（出图执行器）
须另行取得并部署在渲染机的 `<渲染机脚本目录>`，用渲染机自带的 python 执行。
本仓库**不含**这些脚本；公开仓按文档直接调用会找不到文件，以实际部署为准。
SSH 通道按部署配置选择（本仓库不内置具体主机别名）。

```bash
PY='<渲染机python>'
CLI='<渲染机脚本目录>\h3qc.py'
```

**出图必带参考图（所有通道，Qwen 2.1 与 H3-Image 都适用）：** 提交 `--kind image` 之前，必须先查本镜有没有参考图——来源是 doc-still-prompt 的绑定、分镜的 `SHOT-...#KF-...`、项目资产板/角色卡，或对话里刚给的图。有参考图就必须带上：CLI 用 `--refs`、adapter 用 `reference_bindings`、MCP（`h3_generate_image` / `h3_generate_project_image`）按该工具的 schema 传参考图；带参考的提交走 `h3qg.py`。**没有参考图就按纯文生图跑，是提交时就要明确说出来的决定，不是默认状态**：确实无参考（首次造身份板、纯文生探索）才可以不带，并在提交记录里写明"本次纯文生图，无参考图"。有参考图却没带的提交一律视为漏提交——发现后不要直接认产物，先补参考重投。参考图文件须已在 ComfyUI 的 `input/`（MCP 由调用方上传），否则执行器收不到图，等同没带。

### 出图（Qwen Image 2.1）

```bash
$PY -s $CLI submit --kind image \
  --prompt-file '<渲染机提示词目录>\s1.txt' \
  --out        '<渲染机产物目录>\s1.png' \
  --size 768x1344 --seed 42 \
  --label 'S1 定妆' --idem-key 's1-still-20261020'
```

- `--size` 是真实采样画布 `WxH`，宽高向下对齐到 32 的倍数，最小各 32；输出不再自动做 center crop。**要作视频首帧或参考的关键帧，按目标视频画布出**（`768x1344` / `1344x768` / `1024x576` 等）。
  当前 MCP 部署默认 `2k-16x9=2752x1536`（env `H3Q_IMAGE_SIZE`），是横屏；竖屏 2K 显式给 `2k-9x16=1536x2752`。
- 缺省值由渲染机/MCP 部署定义，**以实现实读为准**（`h3qc submit --help` / MCP schema / 覆盖键 `H3Q_IMAGE_*`，见 [still-api-params.md](references/still-api-params.md)）；实测时点为 CFG 3.5、无 LoRA、`steps=0` 按参考选 40/45 步。可显式设置 `cfg`、`steps`、`loras`、`resolution`，不自动叠加 Turbo LoRA。
- 图片分支会丢弃 `out_width` / `out_height`（视频尺寸）；`refine_denoise` / `refine_steps` 可透传给图片二采，见下方「出图（MiniMax H3-Image）」。
- 带参考图：`--refs a.png,b.png`（CLI 文件须已在 ComfyUI 的 `input/`；MCP 上传本地源文件，见 §2.8）。`resolution=0` 默认按原参考尺寸编码，模型仍对齐 32；它控制参考编码，不替代 `size` 指定的采样画布。
- **负向仅在 `cfg>1` 生效**（`negative_prompt: negative if cfg > 1.0 else ""`）。显式 `cfg=1` 仍受尊重，此时 MCP 对非空 negative 返回无效提示。
- `seed=0` 是有效种子，保留原值。同秒同 label/seed 的独立 MCP 调用各用唯一请求目录和输出名；仅显式复用 `idem_key` 才复用队列任务。

### 出图（MiniMax H3-Image）

`--engine` 选 H3-Image 权重；省略时走上面的 Qwen Image 2.1 通路。
现役只保留 W4A8 一档（社区量化 Q4_K_M 已从脚本移除）。用
`qwen3vl_32b_minimax_h3_nvfp4_awq.safetensors` 文本编码器与
`minimax_h3_image_vae_fp16.safetensors`，`MiniMaxH3ImageConditioning` + Euler/simple，
6 步、CFG 1.0。

| engine | 权重 | loader |
|---|---|---|
| `h3-image-w4a8` | `minimax_h3_image_pruned_w4a8.safetensors` | `UNETLoader` |

```bash
$PY -s $CLI submit --kind image --engine h3-image-w4a8 \
  --prompt-file '<渲染机提示词目录>\poster.txt' \
  --out '<渲染机产物目录>\poster-w4a8.png' \
  --size 1536x1024 --seed 42 --steps 6 \
  --idem-key 'poster-w4a8-seed42'

# 可选第二次采样：VAE 回编码 → 第二个 KSampler（seed+1）→ 解码
$PY -s $CLI submit --kind image --engine h3-image-w4a8 \
  --prompt-file '<渲染机提示词目录>\poster.txt' \
  --out '<渲染机产物目录>\poster-w4a8-refine.png' \
  --size 1536x1024 --seed 42 --steps 6 \
  --refine-denoise 0.30 --refine-steps 6 \
  --idem-key 'poster-w4a8-refine-seed42'
```

- `--refine-denoise` 缺省 0 = 单次采样；大于 0 才追加二采节点，`--refine-steps 0` 用渲染器默认步数。二采保构图与文字，纹理区会重绘；实测同 seed 下几何/文字类 PSNR 27–32 dB，高纹理类 17–19 dB。
- `--refs` 透传到 conditioning 节点的 `images.image_N`；命令行文件名须已在 ComfyUI `input/`。`--checkpoint`、`--loras`、`--alpha`、输出尺寸覆盖不适用于该引擎。
- **参考图实测边界（2026-11-15，7 素材 × 忠实重绘/只改冷光）**：W4A8 的 `--refs` 全批通过。原社区量化 Q4_K_M 在 1152×768 带参考图时卡死（GPU 100%、显存占满、渲染器 903s 超时），已从脚本移除，不再作为可选档。
- 同批对照结论：**参考图编辑维度 Qwen 2.1 比 H3 W4A8 更忠实**（7 例里 6 例结构保真更高），H3 W4A8 改光时常连主体、机位一起重绘并顺手抬曝光。纯文生复杂规格仍是 H3 更强；两者按任务类型分开选。实测记录存内部工程档案（未随公开版发布）。
- MCP 的 `h3_generate_image` 目前只走 Qwen 通路，未暴露 `engine`；要用 W4A8 走上面的队列 CLI。

### 出图参数

| 调用方式 | 步数 | LoRA | 说明 |
|---|---|---|---|
| 默认值以实现实读为准（覆盖键 `H3Q_IMAGE_*`） | 实测时点：纯文生 40 / 带参考 45 步 | 实测时点：无（`none`） | 负向仅 `cfg>1` 生效；耗时按实际尺寸、参考和排队情况判断 |
| `--loras 'X:1.0'` | 显式设置或按默认选择 | 指定的 X | 按该 LoRA 的推荐参数设置 steps/CFG |
| `--alpha 1` | 按默认选择 | 无 | 走 `SaveImageWithAlpha`（拆 alpha 再存） |

底模**不用换**：`qwen_image_2.1_int8_convrot` 保持不变。
文本编码器可选档：`qwen3vl_8b_int8_convrot`（9.35 GB，INT8 快路）、`qwen3vl_8b_w4a8`（6.31 GB，最小）。

**原生 2K 画布**（模型按这些尺寸训练，细节来自真实推理而非放大）：
`2k-1x1=2048x2048`、`2k-3x4=1792x2400`、`2k-4x3=2400x1792`、`2k-2x3=1696x2528`、
`2k-3x2=2528x1696`、`2k-9x16=1536x2752`、`2k-16x9=2752x1536`。
`--size` 可直接给预设名。显存与耗时随尺寸增大；视频首帧按项目目标画布显式选择尺寸。

用 `qwen-image-2.1-fix-1.0` 那种画质修正 LoRA 时，按它自己的推荐参数给 `--steps 20 --cfg 3`，
不要叠加本档默认。

参数来源与 A/B 量化数据见
[references/still-standard-tier-20261105.md](references/still-standard-tier-20261105.md)
（历史基础模型实测，含 CFG 与负向通道机制；耗时仅代表对应实验）。

### 出视频（MiniMax H3）

```bash
$PY -s $CLI submit --kind video \
  --prompt-file '<渲染机提示词目录>\s1.txt' \
  --slug s1 --version v1 \
  --width 768 --height 1344 --seconds 10 \
  --refs a.png,b.png \
  --label 'S1 视频' --idem-key 's1-vid-v1'
```

- 视频提示词必须**先过 `h3-video-gate`**（`../h3-video-gate/scripts/h3_gate.py` 退出码 0）才提交，队列不检查提示词内容。
- **带 `--refs` 的提交可走 `h3qg.py`**（video-studio 提供，与 `h3qc.py` 同目录）：提交前自动跑参考图检查，拦住则不入队。它只包装客户端、不动常驻服务，不需重启队列、不打断别人在跑的活；`--gate-off` 显式跳过并留痕。
- 帧数按 17k+5；`--seconds` 会自动吸附到帧网格。
- **`17k+5` 换不到整秒，分镜名义时长与成片实际时长必然差一截。** 24 fps 下常用帧数：107=4.458s、124=5.167s、141=5.875s、175=7.292s、192=8.000s、243=10.125s、328=13.667s。分镜写 5.5s 只能取 141f 或 124f；成片总长按**帧数÷24**核，不要拿镜头表的整数秒相加（EP01 名义 43.125s，实际 1067 帧 = 44.459s，差的 1.334s 全部来自这一步；HANDOFF-接手必读记 1099 帧 / 45.79s 为不同版本成片，勿并列比较）。
- **产物文件名由 worker 重写，不是提交参数拼出来的。** 传了 `--out-width/--out-height` 也不会把尺寸写进文件名（EP01 提交参数写作 `s04_up1_141frames_1344.mp4`，实际落盘是 `s04_up1_141frames.mp4`）。真实路径只认 `h3qc.py show <JOBID>` 的 `output` 字段，不要按提交命令自己拼 scp 路径。

### 提交后立即返回，或等待任务完成

CLI 默认在入队后返回 `job_id`，MCP 使用 `wait=false` 获得同样行为。CLI 加 `--wait` 会等任务离开队列；Ctrl-C 只退出客户端等待，队列任务继续。

## 2.5 档位能力与队列执行能力

详见 [档位能力与队列执行能力](references/tiers-and-capabilities.md)。

## 2.6 PDD 超分图的离线配方参考

详见 [PDD 超分图的离线配方参考](references/pdd-offline-recipe.md)。

## 2.7 出图接口与参数透传

详见 [出图接口与参数透传](references/still-api-params.md)。

## 2.8 short-drama-produce 接入口

详见 [short-drama-produce 接入口](references/produce-adapter.md)。

## 2.10 二采 split 引擎（tiled）+ SeedVR2 事后超分

> 无 §2.9，编号为历史遗留，内容无缺失。

详见 [二采 split 引擎（tiled）+ SeedVR2 事后超分](references/upscale-split-engine.md)。

## 2.11 latent 放大（成品帧回编码，不重采样）

详见 [latent 放大（成品帧回编码，不重采样）](references/latent-upscale.md)。

## 2.12 多镜容器的容量与打包

详见 [多镜容器的容量与打包](references/multishot-capacity.md)。

## 2.13 续接的两条路：Ref2VA 末槽 vs 纯 I2VA 首帧

详见 [续接的两条路：Ref2VA 末槽 vs 纯 I2VA 首帧](references/continuity-routes.md)。

## 2.14 多窗一次生成（H3 Multishot）

详见 [多窗一次生成（H3 Multishot）](references/h3-multishot.md)。

## 2.15 画质增强路线与交付规格

详见 [画质增强路线与交付规格](references/delivery-specs.md)。

## 2.16 长镜头接住 × 超分的契约

详见 [长镜头接住 × 超分的契约](references/longshot-upscale-contract.md)。

## 3. 怎么看清队列：有多少、我第几、还要多久

```bash
$PY -s $CLI queue     # 最常用：谁在跑、谁在等、各自 ETA
$PY -s $CLI health    # ComfyUI 可达性、显存、看门狗
$PY -s $CLI show <JOBID>
$PY -s $CLI ls [--state queued]
$PY -s $CLI stats
```

`queue` 输出形如：

```
RUNNING
  70852e2176a9   image  S1 定妆   elapsed 1s    ~44s left
WAITING
  #2   1dc6906a9ce1   video  s1    starts ~10:25:37 (in 44s)
  #3   11f62a696ae0   video  s2    starts ~10:35:37 (in 10m44s)
measured   image~45s  video~10m00s
```

- **跑第几** = `WAITING` 里的 `#N`；`#1` 是下一个。提交响应里也直接给出 `position`。
- **还要多久** = `in …`。ETA 用**这台机器自己已完成的同类任务的中位耗时**算，`measured` 一行就是当前采用的基数；机器还没跑过同类任务时用保守种子（图 45 s、视频 600 s）。

## 4. 任务状态怎么读

```
queued → running → done
   │         │
   │         └→ failed        渲染报错，看 note / queue\logs\<kind>_<slug>_*.log
   ├→ blocked_vram            显存回收不到底线，停靠等人工处理
   └→ cancelled               排队时被取消
```

- `blocked_vram` 是**有意停靠**：宁可不动，也不在只剩 1 GB 的卡上硬提交。腾出显存后重新提交即可。
- **两个阈值**（`H3Q_MIN_FREE_GB` / `H3Q_FLOOR_GB`，2026-11-21 从 2.0/1.5 提到 **4.0/3.0**）：可用显存低于 `MIN_FREE` 就先请求 `/free`；回收后仍低于 `HARD_FLOOR` 才停靠。原先 1.5 GB 的底线等于允许在只剩一两个 G 的卡上开跑，看着「明明没显存了还照样丢进去」，实际是在赌——H3 峰值要 15 GB 上下，赌输就是 OOM + sticky context。
- ComfyUI 挂掉时任务退回 `queued` 等待，不丢；恢复后自动续跑（`attempts` 会加一）。
- `failed` 且 note 含 `TIMEOUT`：上游可能还在跑，**不要盲目重投**；先 `queue` 看现场。

## 5. 什么情况下不能用队列

- 只想验证工作流连线、不占 GPU：用 ComfyUI 网页 UI 或在 `h3_render_ref.py` 加 `--validate-only`。
- **AI-Canvas-tauri** 按用户授权可直接通过 ComfyUI 隧道提交，不经过本队列；它不具备队列的显存预检、幂等或项目参考图闸门。其他 Mac 侧直连链路仍应迁入本队列。
- 成片剪辑、拼接、字幕：走 `concat-video`，不占这张卡。

## 6. 排障顺序

1. `h3qc.py health` —— 队列自己活着吗？ComfyUI 可达吗？显存多少？看门狗 tick 在涨吗？
2. `h3qc.py queue` —— 是真在跑，还是卡在 `blocked_vram`？
3. `Get-Content <渲染机根目录>\queue\h3q.log -Tail 40` —— 队列自己的日志。
4. `Get-Content <渲染机根目录>\queue\logs\<kind>_<slug>_<ver>_<jid>.log` —— 单任务渲染日志。
5. 仍然 OOM：确认没有绕过队列的提交（查 `<渲染机根目录>\logs\serve.log` 尾部）；必要时降尺寸/步数重投，不要重启实例。

服务管理（只在确认队列自己挂了时才动）：

```powershell
schtasks /query /tn "H3-Queue" /fo LIST /v
schtasks /run   /tn "H3-Queue"
```

队列以 **SYSTEM** 身份、随系统启动、失败每分钟重试、无执行时限。不要改成交互用户身份——SSH 建的计划任务在无桌面会话时不会启动（实测 `LastTaskResult=267011`，任务永远不动）。

## 7. 端点速查（脚本化调用时）

服务在 `127.0.0.1:8200`，只监听回环。

| 方法 | 路径 | 用途 |
|---|---|---|
| POST | `/job` | `{kind, params, idem_key}`，立即返回 job id + position |
| GET | `/job/<id>` | 详情（含 `position` / `eta_s` / `eta_at`） |
| GET | `/jobs?state=queued` | 列表 |
| GET | `/queue` | running / waiting / 排位 / ETA |
| GET | `/health` | ComfyUI 可达性、显存、看门狗 |
| GET | `/stats` | 各状态计数 + measured 耗时 |
| POST | `/job/<id>/cancel` | 仅 `queued` 可取消 |

Python 客户端可直接 `urllib` 打这些端点；也可以复用渲染机上 `h3qc.py` 的函数。

## 8. 部署物与源码

**队列服务**

- 线上（渲染机）：`h3q.py`（服务）、`h3qc.py`（客户端）、`h3q_img.py`（出图执行器）、`h3qg.py`（带参考闸门的包装），均在 `<渲染机脚本目录>`；这些是渲染机侧私有定制脚本，**须另行取得并部署在渲染机，不随本仓库发布**（以实际部署为准）
- 队列数据：`<渲染机根目录>\queue\h3q.db`（SQLite）、`queue\h3q.log`、`queue\logs\`
- 本仓库 `scripts/` 只保留离线研究副本（见下方），与渲染机线上脚本**不是同源**，不要拿它当线上代码或据此推断服务端行为

**草稿超分档（见 §2.5）**

| 文件 | 作用 |
|---|---|
| `<渲染机脚本目录>\mkdraft.py` | 生成草稿超分图（任意提示词 / 参考图 / seed / 帧数） |
| `<渲染机脚本目录>\pdd_run.py` | 提交器：先等 ComfyUI 空闲，全程记录峰值显存 |
| `<渲染机脚本目录>\validate.py` | 提交前静态校验（节点已注册、输入齐全、连线可达 Save*） |
| `<渲染机脚本目录>\run_detached.ps1` | 让提交进程脱离 SSH 会话（否则断线即被杀） |
| `<渲染机工作目录>\graphs_draft_lu\DRAFT_LU_standard.json` | 已验证的标准档位图（22 节点） |
| `<渲染机工作目录>\make_graphs.py` | 批量入口；`draft` 档已直接产出超分链路 |

模板源：`<渲染机工作目录>\eval\graphs\03_submit_pdd_xiuxian_draft.json` —— PDD 图唯一的源头，`mkdraft.py` 和 `make_graphs.py` 都从它派生，改它两边一起变。

**离线研究副本**：本技能 `scripts/` 留有 `mkdraft.py` / `pdd_run.py` / `validate.py` / `run_detached.ps1` / `h3_quick.py` 作历史记录，
其中 `pdd_run.py`、`h3_quick.py` 直连 8199，**不部署、不调用**。

`h3_quick.py` 依赖的 `lib_workflow.py` 同样是**渲染机侧私有定制脚本，须另行取得并放在本脚本同目录，不入本仓库**；
公开仓直接运行会因缺该模块 `ImportError`。其 `--tier` 合法值是 `draft|hq|ref8|ref6`。

**远端环境变量统一命名**（`transcard.py` / `short_drama_h3q_adapter.py` / `video-studio/scripts/example_h3q.py` 一致）：
主名 `H3Q_SSH_HOST`（SSH 可达的渲染机）、`H3Q_REMOTE_PY`（渲染机 python 路径）；
旧名 `H3Q_HOST`、`H3Q_PY`、`H3Q_REMOTE_PYTHON` 仍作兼容别名，读取顺序为**新名 → 旧名**（两者都设时以新名为准）。
三处脚本调的是同一台渲染机，设一套主名即可同时满足。

注意它们依赖的目标机环境：ComfyUI 在 `127.0.0.1:8199`（默认端口是 8188，8199 为渲染机本机自定义）、嵌入 python 与 PDD 模板同样按渲染机部署位置配置。
