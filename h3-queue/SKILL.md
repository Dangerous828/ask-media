---
name: h3-queue
version: 1.1.2
description: 仅在要往新台式机（win-desktop / DESKTOP-10Q7AIV，RTX 5070 Ti 16GB）真跑出图或出视频时使用——用户说“出片”“出图”“跑视频/跑图”“生成这张图/这段视频”“提交任务”“送去生产”即命中；也用于查队列里有多少任务／自己排第几／还要等多久，或排查 ComfyUI 抢占与 OOM。规定常规任务经 h3q（127.0.0.1:8200）提交；AI-Canvas-tauri 使用自己的 ComfyUI 提交路径，属于明确例外。负责真实任务提交、状态与产物核对；也负责已验收成片的 latent 放大（h3_upscale_video，后处理通道，不重采样）；不编写提示词，不做成片剪辑。**用户要“让角色学/照着一段参考视频的动作做”（视频动作驱动、动作参考、学动作、翻跳、参考视频+参考音轨）时也命中本技能：走不经 h3q 的 ComfyUI 直投通道，先读 references/video-motion-drive.md。** **用户要做“转场卡/接缝中间段/两镜之间插一段/首尾帧接起来”时也命中：用 scripts/transcard.py 一条命令跑完取帧→上传→FL2VA 出片→两端验收，做法见 references/transcard.md。** 短剧任务按正文读取对应阶段知识，本技能继续完成当前工作。
---

# h3-queue：GPU 生产队列的提交纪律

## 短剧项目协作（命中即读，保留本职）

本技能继续核对并经h3q提交真实任务、追踪结果。短剧实际生产先读 [short-drama-produce](../drama-skills/skills/short-drama-produce/SKILL.md) 的本次授权与输入/产物记录要求，仍由本技能执行本地队列通道；不额外安装adapter或另开审批。单纯查询排队/显存/OOM和下载既有文件不启动创作。 规则见 [协作契约](../SHORT-DRAMA-ROUTING.md)。已读上下文复用；只有跨阶段、状态或初始化才读取short-drama主路由。

一句话：**常规出图/出视频经 `h3q` 提交；用户授权使用 AI-Canvas-tauri 时，允许该应用直接连接 ComfyUI 8199 提交，无需经过 h3q。** AI Canvas 直连不会获得 h3q 的显存预检、幂等与项目参考图闸门，提交前确认 ComfyUI 与 h3q 当前任务状态，避免与其他 GPU 任务并发。

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
`magpie-h3-mcp/server.py`（MCP 侧，`h3_generate_video` / `h3_generate_project_video`）实现同一套
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

CLI 在 Windows 侧：`E:\H3-Studio\scripts\h3qc.py`（用自带的 python 执行）。
同在局域网时从 Mac 优先走 `ssh win-desktop`；远程按实际可用通道选 `win-desktop-cf`、`uu-2222` 或 `h3-win`（见 `dsh-cpuser-ops`）。

```bash
PY='E:\ComfyUI\ComfyUI_windows_portable\python_embeded\python.exe'
CLI='E:\H3-Studio\scripts\h3qc.py'
```

### 出图（Qwen Image 2.1）

```bash
$PY -s $CLI submit --kind image \
  --prompt-file 'E:\H3-Studio\prompts\s1.txt' \
  --out        'E:\H3-Studio\renders\s1.png' \
  --size 768x1344 --seed 42 \
  --label 'S1 定妆' --idem-key 's1-still-20261020'
```

- `--size` 是真实采样画布 `WxH`，宽高向下对齐到 32 的倍数，最小各 32；输出不再自动做 center crop。**要作视频首帧或参考的关键帧，按目标视频画布出**（`768x1344` / `1344x768` / `1024x576` 等）。
  当前 MCP 部署默认 `2k-16x9=2752x1536`（env `H3Q_IMAGE_SIZE`），是横屏；竖屏 2K 显式给 `2k-9x16=1536x2752`。
- **默认基础模型 CFG 3.5、无 LoRA（`loras=none`）**；`steps=0` 交给渲染器选择纯文生 40 步、带参考 45 步。可显式设置 `cfg`、`steps`、`loras`、`resolution`，不自动叠加 Turbo LoRA。
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
  --prompt-file 'E:\H3-Studio\prompts\poster.txt' \
  --out 'E:\H3-Studio\renders\poster-w4a8.png' \
  --size 1536x1024 --seed 42 --steps 6 \
  --idem-key 'poster-w4a8-seed42'

# 可选第二次采样：VAE 回编码 → 第二个 KSampler（seed+1）→ 解码
$PY -s $CLI submit --kind image --engine h3-image-w4a8 \
  --prompt-file 'E:\H3-Studio\prompts\poster.txt' \
  --out 'E:\H3-Studio\renders\poster-w4a8-refine.png' \
  --size 1536x1024 --seed 42 --steps 6 \
  --refine-denoise 0.30 --refine-steps 6 \
  --idem-key 'poster-w4a8-refine-seed42'
```

- `--refine-denoise` 缺省 0 = 单次采样；大于 0 才追加二采节点，`--refine-steps 0` 用渲染器默认步数。二采保构图与文字，纹理区会重绘；实测同 seed 下几何/文字类 PSNR 27–32 dB，高纹理类 17–19 dB。
- `--refs` 透传到 conditioning 节点的 `images.image_N`；命令行文件名须已在 ComfyUI `input/`。`--checkpoint`、`--loras`、`--alpha`、输出尺寸覆盖不适用于该引擎。
- **参考图实测边界（2026-11-15，7 素材 × 忠实重绘/只改冷光）**：W4A8 的 `--refs` 全批通过。原社区量化 Q4_K_M 在 1152×768 带参考图时卡死（GPU 100%、显存占满、渲染器 903s 超时），已从脚本移除，不再作为可选档。
- 同批对照结论：**参考图编辑维度 Qwen 2.1 比 H3 W4A8 更忠实**（7 例里 6 例结构保真更高），H3 W4A8 改光时常连主体、机位一起重绘并顺手抬曝光。纯文生复杂规格仍是 H3 更强；两者按任务类型分开选。详见 `~/Downloads/h3-project-frames-20261115/项目素材参考图编辑实测.md`。
- MCP 的 `h3_generate_image` 目前只走 Qwen 通路，未暴露 `engine`；要用 W4A8 走上面的队列 CLI。

### 出图参数

| 调用方式 | 步数 | LoRA | 说明 |
|---|---|---|---|
| **默认 `cfg=3.5, steps=0`** | **纯文生 40 / 带参考 45** | 无（`none`） | 负向有效；耗时按实际尺寸、参考和排队情况判断 |
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
  --prompt-file 'E:\H3-Studio\prompts\s1.txt' \
  --slug s1 --version v1 \
  --width 768 --height 1344 --seconds 10 \
  --refs a.png,b.png \
  --label 'S1 视频' --idem-key 's1-vid-v1'
```

- 视频提示词必须**先过 `h3-video-gate`**（`scripts/h3_gate.py` 退出码 0）才提交，队列不检查提示词内容。
- **带 `--refs` 的提交可走 `h3qg.py`**（video-studio 提供，与 `h3qc.py` 同目录）：提交前自动跑参考图检查，拦住则不入队。它只包装客户端、不动常驻服务，不需重启队列、不打断别人在跑的活；`--gate-off` 显式跳过并留痕。
- 帧数按 17k+5；`--seconds` 会自动吸附到帧网格。
- **`17k+5` 换不到整秒，分镜名义时长与成片实际时长必然差一截。** 24 fps 下常用帧数：107=4.458s、124=5.167s、141=5.875s、175=7.292s、192=8.000s、243=10.125s、328=13.667s。分镜写 5.5s 只能取 141f 或 124f；成片总长按**帧数÷24**核，不要拿镜头表的整数秒相加（EP01 名义 43.125s，实际 1067 帧 = 44.459s，差的 1.334s 全部来自这一步）。
- **产物文件名由 worker 重写，不是提交参数拼出来的。** 传了 `--out-width/--out-height` 也不会把尺寸写进文件名（EP01 提交参数写作 `s04_up1_141frames_1344.mp4`，实际落盘是 `s04_up1_141frames.mp4`）。真实路径只认 `h3qc.py show <JOBID>` 的 `output` 字段，不要按提交命令自己拼 scp 路径。

### 提交后立即返回，或等待任务完成

CLI 默认在入队后返回 `job_id`，MCP 使用 `wait=false` 获得同样行为。CLI 加 `--wait` 会等任务离开队列；Ctrl-C 只退出客户端等待，队列任务继续。

## 2.5 档位能力与队列执行能力

**提交前核对实际服务端 `build_argv` 与渲染器，不只看客户端帮助或档位表。** 2026-10-24在win-desktop核验：h3q视频分支支持first_frame、帧数、尺寸和步数；**2026-10-29 起 `h3qc submit` 另支持 `--workflow lu2|pdd_lu`、`--loras`、`--no-upscale`、`--out-width/--out-height`，短剧 adapter 已用 `parameters.tier` 暴露（见 §2.8），2026-11-01 起默认 draft**；仍没有任意graph参数；Mac adapter 已有 last_frame 成对校验与透传路径；该历史核验不能说明当前部署缺少首尾帧，实际服务端支持范围按本技能「输入能力与续接职责」核对。I2VA实际调用lib_workflow的Q4 Turbo图。下表hq/ref6属于构图工具能力，不等于该队列可以选择的生产档位。只有队列实际支持且输出workflow已核对，才报告使用相应档位。

`h3_quick.py`直连8199，不能替代h3q，**不得用于任何提交**（离线研究也必须在 GPU 空闲且经创作者同意时，由人工执行）。入口不支持优选档时明确记录实际回退与质量验证，不把增加步数当作切换底模或提高量化精度。下表只记录离线实测，**h3q 当前不可选这些档位**：

| 档位 | 底模 | LoRA | 步数 | 模式 | 用途 |
|---|---|---|---|---|---|
| `draft` | `fl2va_turbo_Q4_K_M.gguf` | 无（烘焙） | 8 | I2VA | 旧档，仅回退用 |
| `hq` | `fl2va_pruned_w6a8` | `fl2v_turbo_8step_v1.0_768p` | 8 | I2VA | 离线实测较优；h3q 不可选 |
| `ref8` | `ref2va_pruned_int8` | 无 | 20 | Ref2VA | 定稿 |
| `ref6` | `ref2va_pruned_w6a8` | `ref2v_turbo_8step_v1.1_768p` | 8 | Ref2VA | 未实跑；h3q 不可选 |

**换档的实测依据（2026-10-21，同首帧/同提示词/同 seed）**：

| 场景 | draft Q4 | hq w6a8 | 结论 |
|---|---|---|---|
| 横屏 1344×768×192f | 686.4 s / SSIM 0.808 | **546.3 s / SSIM 0.878** | 快 20%，更像官方 |
| 竖屏 768×1344×107f | 295.4 s | **222.6 s** | 快 25% |

> ⚠️ **关键不是清晰度，是构图稳定性。** 竖屏实测中 draft(Q4) 中段漂成脸部特写，
> hq(w6a8) 全程稳住中景。原因是 Q4 的 turbo 蒸馏自 **544p**，跑 768p 时先验错位。
> 官方 768p 专用 LoRA 才对齐。

`ref6` 文件与脚本已就绪但**未实跑验证**，首次用先跑小样。

**画布硬约束**：宽高必须都是 **32 的倍数**。720/1080 都不合法，报
`height=720 is not a multiple of 32`。用 1248×704、1312×736、1344×768、768×1344。

**PDD 竖屏支持（2026-11-20 新增，example-project 9:16）**：此前 pdd 首采锁死
1024×576 横屏，width/height 只作用于二采，draft 档会被静默吞掉（产物仍是横屏）。
现 `pdd_render_ref.py` 新增 `--width/--height` 覆盖首采（默认 1024×576 不变，
横屏任务 argv 逐字节不变），`h3q.py` pdd_lu 分支已透传（改后需重启 H3-Queue
计划任务）。MCP `_pdd_argv` 仅在 width<height 时传首采：draft 竖屏首采=width/height；
final 竖屏首采按 out/1.5 就近取 32 倍数推导、二采=width/height。MCP 改动需 Alma
重连 magpie-h3 才生效，重连前可直连 `h3qg.py submit --workflow pdd_lu --width ...
--height ... --no-upscale`。竖屏推荐尺寸（对 896×1536 基准的 aspect 差均 <2%）：
draft 首采 **576×992**（0.46%，面积小于横屏默认），final 二采 **832×1440**
（0.95%，面积在 1536×864 上限内，首采推导 544×960）。896×1536 本身面积超
1536×864 上限会被拒，不是竖屏专属问题。

## 2.6 PDD超分图的离线配方参考

当前h3q没有任意graph提交参数。本节的pdd_run/run_detached不能作为真实生产入口，等待空闲不等于队列准入；仅保留图结构和既有测量供离线研究。生产前必须具备经h3q可执行的对应路径，不绕过队列。档位配方的用途区分：
`hq/ref6` 是**快速看构图与表演**（单段，快）；PDD 是**要 1536x864 交付尺寸**时用。

```
pass 1    1024x576   PDD nfe=8  euler            ← 定构图
超分      latent 3D 1.5x -> 1536x864             ← 加细节
pass 2    1536x864   PDD nfe=8  denoise=0.5      ← 收拢放大带来的软感
```

| 指标 | 实测值 |
|---|---|
| 输出 | 1536x864 / 243 帧 / 24fps / 10.125s |
| 耗时 | 446.6 s |
| 峰值显存 | ~15.1 GiB（不 OOM） |
| 文件 | 9.56 MB |

### 为什么是这条，不是直接跑 1344x768

**构图由 pass 1 的分辨率决定，不由 seed 决定。** 同 seed 1017、同参考图，实测三档画面内容不同：
`896x512` 无山 / `1024x576` 云海偏左 / `1344x768` 远山清晰。所以草稿用别的分辨率，**看到的画面不是成片的画面**。
这条链路的好处是 pass 1 锁住构图，超分只在同一构图上加细节——草稿批准的那一帧，就是成片的那一帧。

### 怎么生成

```bash
# 单镜、任意提示词（推荐，参数化）
$PY -s 'E:\H3-Studio\scripts\mkdraft.py' \
  --out  'E:\H3-Studio\prod1017\graphs_draft_lu\myshot.json' \
  --prompt-file 'E:\H3-Studio\prod1017\prompts\myshot.txt' \
  --ref0 myshot_start.png --ref1 myshot_city.png \
  --seed 1017 --frames 243 --tag myshot

# 只要纯草稿、不超分（省时间，用于快速看表演）
#   追加 --no-upscale  -> 1024x576，约 167 s

# 批量（固定三个镜头）
python -s make_graphs.py draft <city.png>
```

### 离线执行记录（禁止用于生产提交）

历史上超分图由 `pdd_run.py`（直连 8199）和 `run_detached.ps1` 执行。它们绕过 h3q，**agent 不得调用**；
需要超分链路时报告“h3q 未暴露该档位”，由创作者决定是否让队列支持。

### 想改哪里（按收益排序）

| 旋钮 | 现在 | 说明 |
|---|---|---|
| pass 2 `denoise` | 0.5 | 降到 0.25 只留 2 块，预计省 100+ 秒；超分本身已给细节 |
| pass 2 `nfe` | 8 | 改 4 = 每步吞两块，最省；画质要自己看 |
| 超分目标 | 1536x864 | 1.5x。注意官方标定路径是 `896 → 1.5x → 1344`，从 1024 出发会超出原生范围 |

⚠️ 别改成单段高分辨率硬跑：1344x768 单段 385.8 s，比这条 446.6 s 便宜，但**构图不同**，草稿就白看了。

## 2.7 出图接口与参数透传

当前默认与画布规则统一见 §2「出图（Qwen Image 2.1）」。基础模型保持 `qwen_image_2.1_int8_convrot`。

| 入口 | 图片参数契约 |
|---|---|
| `h3q_img.py` | `STEPS_T2I=40` / `STEPS_REF=45` / `DEFAULT_CFG=3.5` / `DEFAULT_LORAS=none`；`steps=0` 按是否带参考选择步数；`--size` 指定真实采样画布，`--resolution 0` 按原参考尺寸编码并对齐 32；输出保留采样画幅，不自动中心裁切 |
| `h3q.py` / `h3qc.py` | image 分支透传 `cfg` / `negative` / `steps` / `loras` / `resolution` / `alpha`；保留数值 `seed=0`、`steps=0`、`resolution=0` |
| MCP `h3_generate_image` / `h3_generate_project_image` | schema 暴露并显式透传上述参数；缺省 `cfg=3.5` / `steps=0` / `loras=none` / `resolution=0`。部署覆盖键为 `H3Q_IMAGE_CFG` / `H3Q_IMAGE_STEPS` / `H3Q_IMAGE_LORAS` / `H3Q_IMAGE_RESOLUTION`，尺寸由 `H3Q_IMAGE_SIZE` 指定 |

真实提交经队列；例如：

```bash
$PY -s $CLI submit --kind image \
  --prompt-file 'E:\H3-Studio\prompts\s1.txt' \
  --out 'E:\H3-Studio\renders\s1.png' --size 2k-9x16 \
  --cfg 3.5 --steps 0 --loras none --resolution 0 --seed 0 \
  --negative 'text, watermark, logo' \
  --label 'S1 定妆' --idem-key 's1-still-seed0'
```

`--alpha 1` 可输出 RGBA。自定义 LoRA 使用自己的推荐 steps/CFG，显式传入 `loras`；`--fast` 仅为兼容参数，由渲染器忽略。历史测量见 [基础模型实测记录](references/still-standard-tier-20261105.md)，记录中的耗时与画质结论仅适用于对应实验。


## 2.8 short-drama-produce 接入口

`scripts/short_drama_h3q_adapter.py` 实现短剧生产工具的 adapter stdin/stdout 契约，让 `prepare → 本次确认 → run/collect` 与本队列共用同一份任务记录。它仍只通过 SSH 调用 Windows 上的 `h3qc.py`／带参考时的 `h3qg.py`，不会直连 ComfyUI。

- 每个 job 只接受一个输出；`idem_key` 包含 job 与 run id，提交后立即把队列 jid 写入 `handle_path` 再轮询。
- `collect_provider_job_id` 只查询并下载既有队列任务，不上传、不重新提交。
- 图像 `output` 为 `saved … bytes` 时优先使用任务参数的真实 `out`；视频 `COPY_OF_RECORD …json` 只读解析记录里的 `comfy_output` MP4，不把 JSON 当成片下载。
- **上传先按 modality 分流**：
  - **`modality=image`：直接上传参考源文件字节，保留扩展名；上传名含唯一请求标识，按绑定顺序编号。** 不经过 `sips`、缩放或重编码。`resolution=0` 由模型按原参考尺寸编码并对齐 32，不代表源像素未经任何模型预处理；采样画布由 `size` 单独指定。
  - **`modality=video`：继续以下按角色分两档的上传策略**（2026-11-08 修订）；以下压缩开关和参考面积归一规则仅用于视频。
  - **`first_frame` / `last_frame` 与 `may_control` 含"起始/首帧/构图/状态"的参考 → 原生尺寸 PNG，绝不重编码。** 这些就是交付像素本身。旧代码用 `sips -Z 1344`，而 **`-Z` 会放大也会缩小**：1536×864 的真实末帧被缩到 1344（模型得自己补回 192px 宽度）、896×512 场景板被拉成 1344×768——**末帧接力交出去的已不是创作者验收过的像素**，这是 flf 契约的根本。只在长边超过 `H3Q_REF_LONG_EDGE`（默认 2048，纯安全上限）时才缩。MCP 旧版还把首帧压成 JPEG q80，属同类缺陷，已修。
  - **身份／造型／道具／场景板 → 长边 768 + JPEG q80（保持实测口径，不动）。** `video-studio/SKILL.md` 与 `ref_guard.py` 记着：压完画面更干净，因为板卡噪点不再被放大。该实测出自 Qwen Image 2.1 Turbo 生图（8 步／CFG 1.0／1024×576，4–5 张参考），**H3 视频侧尚未两侧确认**，所以在 A/B 出结论前不因"看起来更保真"就抹掉它。
  - **做实验**：`H3Q_REF_LOSSLESS=all` 强制全 PNG，`=0` 强制全 JPEG。
  - 张数不再构成压缩理由：显存峰值与参考图张数无关（见 §2.8），`ref_image_size: match` 本来就把每张归一到输出面积。
- 严格按 `reference_bindings` 数组顺序上传。视频接受 **`reference_image` / `first_frame` / `last_frame`** 三种角色（旧文档写"只接受前两种"已过期），其余角色 fail closed；互斥关系由 adapter 强制并有测试覆盖：`last_frame` 必须配 `first_frame`（FL2VA 是两帧插值）；`last_frame` 与 `reference_image` 互斥；`first_frame` 与 `reference_image` 互斥。
- **输入能力**统一见本技能「输入能力与续接职责」：单首帧、首尾配对、全参考互斥，没有参考视频/音频或无图文生，不接受任意 graph。档位由 `parameters.tier` 决定。单帧视觉接力不等于整段视频上下文续接，上游档案与所选组合保持一致。
- 图片把 `<Picture N>`、用途、允许／禁止控制范围追加到实际提示词。视频逐字使用来源中的三段或六段正文，参考定义和保留范围由该正文承载，不在段落外追加元数据契约。
- 新视频不能同时使用 `first_frame` 与 `reference_image`：后端首帧路径会忽略其他参考，adapter在任何SSH操作前拒绝此混送。首帧加身份图的Ref2VA任务应整组使用 `reference_image`；单首帧Base任务可单独用 `first_frame`。既有任务collect仍只取回。
- 首次提交在 SSH、参考处理与上传之前，对私有快照调用共享 `ref_gate.py`；视觉设定、当前 look 报告、父媒体报告和生成谱系随快照固定，退出码非 0 或 JSON 未明确 `allowed:true` 都拒绝。collect 不重复验收或上传。
- 视频对最终实际提示词调用 `h3-video-gate`，传入24fps且向上吸附到17k+5的实际帧数和全部图片数量；G17/G18 警告也阻断，G20 这类词数提示不一律误伤短稿；项目有 `h3-series-config.json` 时随任务快照传入。creator-first 任务还把同集 `剧本.md` 固定进快照，上传前逐字核对 `<d>` 台词。**每次视频提交都把格式自检记录写入 `<handle_path>.evidence/`（唯一目录，拒绝覆盖）**：冻结实际执行的 `h3_gate.py`、最终上传的 `prompt.txt`、series 配置、完整 `gate-report.json`、stderr、`manifest.json` 与逐文件 SHA，并记录 job/run、参数与每张参考的原图/上传字节哈希；上传的就是证据目录里那份冻结 prompt，格式自检报错时报告同样保留。collect 只取回既有任务，不新建提交证据。带参考提交走 `h3qg.py`。路径与 SSH host 用 `H3Q_*` 环境变量覆盖，共享闸门可用 `SHORT_DRAMA_REF_GATE` 覆盖，job 与 adapter config 不写凭据。
- 取回视频后必须校验：非空、可解码、帧数等于实际吸附帧数、含音频流；校验失败不交付，不把 scp 成功当成媒体验收。
- **视频引擎 `parameters.engine`（2026-11-07 起，adapter 代码强制）：**

  | engine | 用途 | 默认 |
  |---|---|---|
  | `pdd`（**缺省**） | 官方 Alibaba PAI PDD 8 步蒸馏，首采 1024×576（模板锁定）。**唯一能让空间/透视关系成立的组合**，比 lu2 快约 10 倍 | ✅ 新项目一律用它 |
  | `lu2` | 旧两段式 turbo 4 步。544p 蒸馏跑 768p，**画面空间结构会崩**（实测把「两车之间的窄缝」画成「标准车位」） | **2026-11-15 已下线，不再可选**（仅留作历史对照） |

  **2026-11-07 实测（EP002 第 006 镜，同素材同 seed 777001 同 362 帧）：**

  | 组合 | 墙钟 | 窄缝成立 |
  |---|---|---|
  | 旧 lu2 draft（896×512 4步） | ~120s | ❌ 标准车位 |
  | **pdd 8步 Sol off（1024×576）** | **285.8s** | ✅ 成立 |
  | pdd + 二采 1536×864 | **832.3s** | ✅ 成立 |
  | lu2 legacy 20步（1344×768） | ~1440s | ❌ 机位更乱 |

- **⚠️ Sol 加速档一律不要开**（2026-11-07 实测）：`sol_scheduled` 比 off 慢 3.5% 且**构图跑掉**；`sol_int8qkpv` 快 22.8% 但**同样跑掉**。稀疏注意力跳过部分 token，丢掉的是空间线索。`H3FrontLoadedSigmas`（−24% 步数）也不能配 PDD——beta57 步点只有 2/40 落在 PDD 训练网格上，会被 `on_off_grid=error` 拦下。
  → **`pdd_render_ref.py` 与 `lu_render_ref.py` 的 `--sol-profile` 默认已改为 `off`**（2026-11-07）。

- **参考图槽位：不是 2 张，实测到 9 张（2026-11-08）**

  | 路径 | 建图方式 | 上限 |
  |---|---|---|
  | `lu2` / legacy（`lib_workflow.build_ref2va`） | 程序化，每张 ref 建一个 `LoadImage` | **一直无上限** |
  | `pdd_lu`（`pdd_render_ref.py` + 模板） | 照模板的 `LoadImage` 槽位 | 改前**只有 2 槽**（模板 114/214），现按 refs 动态增删，硬上限 9 |
  | `mkdraft.py`（手建图 CLI） | 同上模板 | 改前只有 `--ref0/--ref1`，现加 `--refs` 逗号表，与渲染器共用同一实现 |

  **槽位逻辑只有一份**：`mkdraft.grow_ref_slots / trim_ref_slots / bind_refs`，`pdd_render_ref.build_graph` 调 `M.bind_refs`。
  不要再在别处复制实现，也不要去找第二份——漂移过一次就是本次"2 张"误传的由来。
  回归核对（原始备份 vs 现版）：**2 张生产路径逐字节一致**；1 张不一致是修掉了模板遗留图混入的缺陷。
  备份：`mkdraft.py.bak-refslots-20261108`、`pdd_render_ref.py.bak-refslots-20261108`。

  **节点真实上限是 9**（`MiniMaxH3ReferenceToVideo.ref_images` autogrow `min:0, max:9`），不是 h3q 也不是模型的 2 张限制。`h3_gate.py` 不限制数量，只核对 `<Picture N>` 编号 ≤ 实际上传数。

  **实测：显存峰值与参考图张数无关（2026-11-08）**：

  | refs | draft 1024×576 | final 1536×864 |
  |---|---|---|
  | 2 | 15.14 GiB / 285.8s | ✅ 15.55 GiB / 831.2s |
  | 3 | 15.14 / 290.6s | 未测 |
  | 5 | 15.15 / 310.6s | 未测 |
  | 6 | 未测 | ✅ **15.53 GiB / 882.4s**（2026-11-08） |
  | 9 | 15.14 / 340.6s | ❌ 失败于 node 304 `SamplerCustomAdvanced`，605.9s（**已排除参考图数量**） |

  **draft 档参考图几乎不吃显存**（2→9 张峰值都在 15.14–15.15），只涨时间约每张 7.8 秒。

  **✅ 结论：final 档的显存不随参考图张数增长。** 6 张二采 15.53 GiB，比 2 张的 15.55 GiB 还略低——
  峰值由二采主序列（138,672 token）决定，参考图那点 token 挤不进影响因素。时间才是要付的代价：
  2→6 张 = 831.2s→882.4s，**每张约 +13 秒**（draft 档每张约 +8 秒）。

  所以 **9 张那次失败与张数无关**。报错正文：

  ```
  torch.OutOfMemoryError: Allocation on device 0 would exceed allowed memory.
  Currently allocated : 901.46 MiB
  Requested           : 50.93 MiB
  Device limit        : 15.92 GiB
  Free (according to CUDA): 0 bytes
  ```

  **PyTorch 自己只占 901 MiB、只申请 50.93 MiB，CUDA 却报可用 0 字节**，摘要还写 `CUDA OOMs: 0`。
  这不是"任务用光 16GB"的形态，而是**设备被别的东西占满**的形态；同时段 `h3q health` 报
  `external work running=1`。

  → **final 档挂多张是安全的**：6 张已实测成功，峰值与 2 张同级。按每张 +13s 排时间预算即可。
  但开跑前仍要确认显存窗口干净（`nvidia-smi` 看 PID 归属，别用 `external work running` 判断，见下条），
  否则一次瞬时分配失败会被误读成容量问题——本次就是这么绕了一圈。

  → **验构图（draft）可以身份板＋场景板＋道具板全挂上，最多 9 张**，多人镜头不必再用正文文字补身份；
  → **出片（final）实测通过 2 张与 6 张**，显存无增长；要多张直接上，按每张 +13s 排时间预算即可。
  9 张那次失败属另一类问题（sticky context / 瞬时分配），不是容量；**重跑即可，不要因此退回 2 张**。
  → 一次 OOM 会让 ComfyUI 进入 Sticky 状态需重启，`h3q` 看门狗会自动拉起。

  顺带修掉的缺陷：改前 refs 数**少于**模板槽数时，多出来的槽仍接着模板自带图，模型会当额外的 `<Picture N>` 吃进去（现按 refs 裁剪）。回归核对：2 张路径改前改后**逐字节一致**。

- **⚠️ `h3qc health` 两个字段容易读错（2026-11-08 连错两次，务必看清）**

  | 字段 | 真实含义 | **不是**什么 |
  |---|---|---|
  | `comfy up for <N>s` | `now() - comfy_last_ok`，距上次**健康探测成功**多少秒 | ❌ **不是进程运行时长**。`up for 0s` = 刚刚应答正常，**不代表刚重启** |
  | `external work running=<N>` | 直接取 ComfyUI `/queue` 的 running 数 | ❌ **不是"别的客户端在占卡"**。h3q 自己提交、正在跑的任务也在这里计数 |

  判"有没有别人占卡"不能靠这两个字段。可靠做法：`nvidia-smi --query-compute-apps=pid,used_memory` 看 PID 归属，
  再对 `h3qc queue`（h3q 自己的任务）做差。

  这条纠正同时推翻了上面的一个推断：**`external work running=1` 不构成"9 张那次失败是别人干扰"的证据**。
  那次失败目前仍未归因：报错正文的 `Free (according to CUDA): 0 bytes` 配合 `Currently allocated 901 MiB`
  是 h3q 自述的 **CUDA context sticky** 形态（`cuMemGetInfo` 本身开始失效），
  而不是干净的"显存被外部占满"。两种解释都还没被排除，**6 张二采是判据**。

  实测记录见项目 `项目开发/参考图槽位放开实测-20261108.md`。

- **第三条路线：HyperFlow H3 Flash（第三方压缩模型，2026-11-06 开源）——本机 16GB 跑不了，别装。**

  Video Rebirth 出的 H3 压缩版，**独立权重**（13.7B，不到原版 31B 的一半），不是 PDD 之外的一个开关，也不是能叠在原版权重上的 LoRA。4/6/8 步、无 CFG、音画同出（32kHz 立体声）、支持 t2va / fl2va / ref2va（最多 9 图）。

  实测数据（官方 `integrations/README.md`，1344×768、6 步、2 张参考图）：

  | GPU | ref2v 5.2s / 15s | 峰值 VRAM |
  |---|---|---|
  | RTX 4090 (24G) | 180s / 866s | 22 GiB |
  | RTX 5090 (32G) | 139s / 663s | 30 GiB |
  | **RTX 5070 Ti (16G)** | — | **官方明写 "16 GB GPUs are not measured yet"** |

  **本机不成立的三条硬理由**：
  1. **显存**：峰值要 22 GiB，本机上限 15.92 GiB。现役 PDD 跑 1536×864 已到 15.55 GiB，只剩 0.37 GiB。换 `Q3_K_M` 只省 1.9 GB，而峰值里权重仅约 9 GB、余下 13 GB 是激活值与 VAE，填不上 6 GiB 的缺口。
  2. **没有速度收益**：24G 卡出 15 秒要 866s，比现役 PDD 的 831s 还慢；16G 只会更慢或直接 OOM。
  3. **改动面大**：要 ComfyUI ≥ 0.43.0（运行实例版本升级前现场核对，2026-11-15 运行实例 git commit b0b7435）、装 `ComfyUI-GGUF` + `ComfyUI-HyperFlow-Flash`、用专属 `HyperFlow GGUF Loader`（普通 loader 不认两时间嵌入器）、整套工作流重写；且要下载约 35 GB（两个 GGUF + 15.7 GB 文本编码器 + VAE），E 盘 2026-11-15 实测余 148.7 GB。`E:\H3-Studio` 不是 git 仓库，升级 ComfyUI 后 PDD / LatentUpscaler3D / Sol 那套改动都要重验。

  **什么情况下再来看它**：官方补 16GB 实测数据，或出现 16GB 可跑的精简版。届时重估的唯一看点是**音画同出**这个能力，不是速度。

  来源：[GitHub](https://github.com/Video-Rebirth/hyperflow-h3-flash) · [HF 权重](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash) · [ComfyUI 节点](https://github.com/Video-Rebirth/ComfyUI-HyperFlow-Flash)

- **视频档位 `parameters.tier`（adapter 代码强制，不靠提示）：**

  | engine | tier | 实际参数 | 用途 | 约束 |
  |---|---|---|---|---|
  | `pdd` | `draft`（**缺省**） | `--workflow pdd_lu --no-upscale --sol-profile off`，首采 1024×576 | 验构图/运动/身份。362 帧约 285s | 不接受 `parameters.steps` |
  | `pdd` | `final` | `--out-width/--out-height` 二采，`--sol-profile off` | 出成片。362 帧到 1536×864 约 832s | **16GB 上限 1536×864**（实测峰值 15.55/15.92 GiB）；超过直接拒绝 |

  > **2026-11-15 起引擎只保留 `pdd`，`lu2`/`legacy` 全部下线**（操作者指令）。`VIDEO_ENGINES=("pdd",)`、`VIDEO_TIERS=("draft","final")`；adapter/server 两条校验路径都会拒 `engine=lu2` / `tier=legacy`，底层 `--workflow lu2|legacy` 变不可达死代码。多窗另走 `multishot`（v2，见 §2.14，不占 engine/tier）。lu2 的历史实测数据仅留作对照，不再是可选档位。

  **长度只认帧数**：`pdd_lu` 忽略 `--seconds`，长度只认 17k+5 的 `--frames`；adapter 自动换算。

  **二采耗时**：362 帧 pdd 从 285s 增到 832s（+546s）。12–15 秒的段按 14–15 分钟排。

顺序固定：**草稿 → 创作者看 → final**。job 里什么都不写就是 draft；想出 final 必须在 prepare 预览里能看到 `tier: final` 和对应草稿，创作者才有机会确认。`h3qg` 只是 `h3qc submit` 的闸门包装，同样透传这些参数。

项目外 adapter config 示例：

```json
{
  "adapters": {
    "local-h3q-image": {
      "command": ["python3", "~/.agents/skills/h3-queue/scripts/short_drama_h3q_adapter.py"],
      "timeout_seconds": 1800,
      "reference_roles": ["reference_image", "first_frame"]
    },
    "local-h3q-video": {
      "command": ["python3", "~/.agents/skills/h3-queue/scripts/short_drama_h3q_adapter.py"],
      "timeout_seconds": 3600,
      "reference_roles": ["reference_image", "first_frame"]
    }
  }
}
```

修改 adapter 后至少运行 `py_compile` 和 `python3 scripts/test_short_drama_h3q_adapter.py` 的 submit/reference/collect 契约测试；离线测试不证明远端生成质量。

## 2.10 2026-11-03 二采 split 引擎（tiled，破 ~300 帧上限）+ SeedVR2 事后超分

**背景**：legacy3d 二采（整段一次过 `MinimaxH3LatentUpscaler3D`，即使开着 `enable_temporal_chunking`）对 311/328/362 帧实测 100% 报 `KSamplerAdvanced [448,96] cannot be broadcast to [1008,96]`，≤300 帧正常。社区结论：长视频放大要在外层做时间分块（temporal chunk）+ 空间分块（spatial tile），每块独立过 upscaler 与采样。

**split 引擎（现默认）**：`lu_render_ref.py` 的 pass2 换成 `MMH3 Ultimate Upscale` 单节点管线（bbaudio-2025/Comfyui-MMH3-UltimateUpscale，已装 `E:\...\custom_nodes\Comfyui-MMH3-UltimateUpscale`）：`MMH3TemporalSplitParams(chunk 136/overlap 17) → MMH3LatentUpscaleWithModelParams(3D upscaler 1344×768) → 主节点（每时间块整帧重采样，噪声掩膜保形，frame-0 钉源 + 颜色匹配）`。`--upscale-engine legacy3d` 可回退旧行为。

- **⚠️ 空间分块必须关（`--tile-size 0`，2026-11-04 起客户端默认已是 0）**：2026-11-03 实测 512px tile（1344×768 → 3×2）时每 tile 主体按 conditioning 各自重绘，**左右 tile 画出同款舞者/对称人群（镜像伪影），成片判废**；破 ~300 帧上限靠时间分块就够，整帧采样显存无压力（legacy2 全段 1344×768×40 latent 帧原生采样本就通过），tile 版反而更慢（717s vs 整帧 385s）。
  - **历史 bug（已修）**：`h3qc.py` 的 `--tile-size` 默认曾是 **512**，而 `h3q.py` lu2 分支只要参数存在就无条件透传，于是"默认档"实际把空间分块打开了，`lu_render_ref.py` 自己的 0 默认被覆盖。**任何在 2026-11-04 之前不带显式 `--tile-size 0` 跑的 final，都要复检有无镜像伪影。**
- **denoise 语义**：split 引擎精修强度走 `BasicScheduler(denoise=refine_denoise)`；1.0 = 每块按 conditioning 全重绘（内容大漂）。**默认 0.30（2026-11-04 起）**。
  - **0.30 是实测保形点**：`MOTION-EP001-L01B`（311f）与 `MOTION-EP001-L02-ONESHOT`（362f）均到 1920×1088，与同一遍 latent 逐点同构图、同姿态，细节为真实重建（门钉、匾额彩画、舞者五官、裙褶层次、二层观众人形）而非插值锐化。
  - **≥0.45 会开始重绘**：turbo LoRA 是照「纯噪声 4 步」训的，部分 denoise 落在它的训练分布外，模型按 turbo 习惯整体重画。**看到"内容变了"先查 denoise，不要先怀疑 upscaler。**
  - 更保形：0.15–0.25（略软）；想更锐：0.35（动作/质感开始回退）。
- **判保形必须用同一遍 latent**：换一次第一遍就换一次 take。用不同 denoise 的两版互相比、或与历史成片相比，都会把"换 take"误记成"超分漂移"。正确做法见下方 save-latent → from-latent。
- **注意**：LBH 包（Comfyui_Minimax_h3_latent_Upscaler）里的 `MMH3 Split Upscale` 三节点**只做分块精修、不做空间放大**，必须配合先放大过的 latent；完整放大+精修一条龙是 bbaudio 的 `MMH3UltimateUpscale`。两者类名相近易混。
- `h3qc submit` 已透传 `--upscale-engine split|legacy3d`、`--chunk-frames`、`--tile-size`（h3q.py lu2 分支同步；改 h3q.py 后要重启 H3-Queue 计划任务服务才生效）。
- **AV latent cache 节点曾丢失**：`SaveMiniMaxH3AVLatentCache`/`LoadMiniMaxH3AVLatentCache` 的来源包在本机已不存在（2026-11-03 发现），已用最小等价节点补上：`E:\...\custom_nodes\h3_av_latent_cache\__init__.py`（safetensors 存 `video`/`audio` 两个 key）。save-latent → from-latent 链路依赖它。

**多段短片接续（2026-11-04 实测）**：第 N+1 段的 `--first-frame` 必须取第 N 段的**末帧**（`ffmpeg -sseof -0.06 -i <N段>.mp4 -frames:v 1`），不能用分镜关键帧顶替。分镜关键帧描绘的是该段的某个中间状态，直接当首帧会让接缝从"上一段终点"直跳到"该段中途"。
实测 `L01B`（终点=红裙糊满全屏）→ `L02`：用 `SHOT-EP001-004.png`（已是红裙扫开、中堂可见）作首帧时，接缝处从"红裙糊满"直接跳到"红裙在左+小二清晰"，肉眼可见；改用 `L01B` 末帧后，接缝变成"红裙糊满 → 红裙糊满（同色调）→ +0.5s 扫开露出大厅"，转场自然。该案例采用单帧视觉接力；当前首尾配对与全参考能力另见本技能「输入能力与续接职责」，不从此历史案例限定所有接缝。

**SeedVR2 事后超分（B 路径，与二采互补）**：已装 `seedvr2_videoupscaler`（numz，`inference_cli.py` 可脱离 ComfyUI 直接跑）+ 权重 `models/SEEDVR2/`（3B fp8 3.2GB + ema_vae fp16 478MB）。ComfyUI 节点 `SeedVR2*` 系列同步可用。实测：draft4（896×512）前 72 帧 → 1260×720，184s（0.39 fps，fp8 无 Sage/FlashAttention）。CLI 必须带 `PYTHONUTF8=1`（GBK 崩 emoji）。适用：救已认可内容的 draft 素材、成片最后一道；产出仍要走 look_check（它是重绘细节的修复模型，不是无损放大）。

**本机环境坑（2026-11-03 实录）**：
1. win 侧 pip/git 配了 `127.0.0.1:7897` 代理且代理常不在——pip 装 包要 `cmd /c "set HTTP_PROXY=& set HTTPS_PROXY=& ... -i https://pypi.tuna.tsinghua.edu.cn/simple"`；GitHub 大文件从 Mac clone 后 tar + scp 过去（同网段走 `win-desktop` mDNS 直连，**别走 win-desktop-cf**，3.7GB 会断）。
2. 装/换 opencv 类包会被运行中的 ComfyUI 锁 `cv2.pyd`（WinError 5）：先停 ComfyUI 再装。
3. 重启 ComfyUI 用计划任务 `schtasks /run /tn H3-ComfyUI`；队列服务是 `H3-Queue`（h3q.py 8200，watchdog 自动拉 ComfyUI）。**别手动 Start-Process 抢端口**。
4. **`gpu.ps1 claim` 的 preempt 会顺带杀掉 h3q 队列进程**（见 19:09 事故，stopping pid … preempted by …，队列 8200 直接死，需要手动 `schtasks /run /tn H3-Queue` 拉回）。手工跑 GPU 任务（如 SeedVR2 CLI）持租约期间，队列渲染会 blocked_vram 等待——任务做完立即 release。
5. hf-mirror 有共享限流；大权重从 Mac `curl huggingface.co` 下载再 scp（校验 SHA256 前 16 位 = HF LFS oid）。
6. 手动 import 测 custom node：ComfyUI 内存日志走 `curl http://127.0.0.1:8199/internal/logs/raw`（JSON entries），能抓 IMPORT FAILED。

## 2.11 2026-11-12 latent 放大（成品帧回编码，不重采样）

**用途**：把已经验收的 H3 成片放大一档，只加细节、不改构图与表演。它不是生成，也不是 §2.10 的二采精修——**这条链路没有第二遍扩散采样**，画面结构由源片决定。

**为什么走这条路**：Multishot 内置的 `(H3 latent x2)` 依赖 Tr1dae 的 `MiniMaxH3LatentUpscaleCombined`，本机没有；装 Motion-Context 也会被 Multishot 按版本点名拒绝（0.3.1 抢 `PackedLayout`，0.4.0+ 直接抛错）。而 CORE 采样器只输出 IMAGE、不暴露 latent，所以不能直接接放大节点。可行解是把成品帧用 H3 video VAE 回编码成 latent，再交给盘上的 LBH 3D 网络。

**链路**（`ComfyUI-H3-ResCascade` + 自带节点）：

```
VHS_LoadVideo（原帧序，force_rate=0）
  → VAELoader(minimax_h3_video_vae_fp16)
  → VAEEncode
  → H3LatentUpscaleLBH(width, height, lbh_model)
  → VAEDecode（同一 video VAE）
  → CreateVideo(images, audio=VHS 音轨) → SaveVideo
```

- `H3LatentUpscaleLBH` 的 `width/height` 是**像素**目标，内部按 `VAE_DOWN=16` 换算 latent 尺寸；对齐 32 即可。
- 权重取自 `models/latent_upscale_models/`：`minimax_h3_latent_upscaler_3d_bf16.safetensors`（690 MB）。
- 纯 video latent 输入也接受（`_streams()` 返回单流时直接放大）；AV latent 输入会原样带过音频流。

**入口一：MCP（推荐）**

`magpie-h3-mcp` 的 `h3_upscale_video`：

```json
{"source": "/path/to/take.mp4", "scale": 2.0, "label": "EP001-upscale"}
```

- 默认 2×，也可显式给 `width`/`height`；`save_path` 缺省 `~/Downloads/h3q/`。
- 工具自动 ffprobe 源、上传到 `ComfyUI/input/`、生成图、提交、轮询、取回并校验非空。
- 实测：451f / 768×448 → 1536×896，**165.1 s**，GPU 峰值约 6.8 GB。

**入口二：手工工作流**

固定图模板见项目 `_ops/EP001-新工作流效果-完整剧情-20261112/工作流副本/CORE-FULL-LATENTLBH.api.json`。改 `VHS_LoadVideo.video` 与 `H3LatentUpscaleLBH.width/height` 即可。

**验收实测（2026-11-12，EP001 两版成片）**

| 指标 | CORE | V2 |
|---|---|---|
| 保真 PSNR（降回源尺寸后比对） | 30.11 dB | 30.21 dB |
| 保真 SSIM-luma | 0.9923 | 0.9923 |
| 锐度 / LANCZOS | 2.10× | 2.08× |
| 接缝最大比（跨镜 / 镜内，阈值 <10） | 1.80 | 1.74 |

**纪律（与 §1 同级）**

1. **h3q 只收 `image`/`video` 生成 job，本链路是后处理例外**。MCP 工具直连 8199，但提交前强制校验 `/health` state=healthy、`external_running=0`、ComfyUI 队列为空；任一不满足直接拒绝。手工提交也必须先做同样检查，不许和生成任务抢卡。
2. 该例外**不扩展到任何生成任务**。出图/出视频仍走 §2 的 h3q 提交。
3. 产物校验同 §1：下载后必须非空、可解码；`done` 不等于文件存在。

**已知限制**

1. **451 帧 → 447 帧**：H3 video VAE 的时间网格不是任意帧数，回编码会在尾部截断（0.167 s）。实测尾部四帧与前一帧 MAD 仅 0.83–1.21，属静止收尾，无可见跳变；音轨同步截到同一长度。
2. **只加细节，不重绘结构**。需要更锐的线条或重画质感，用 §2.10 的 `MMH3 Ultimate Upscale`（`refine_denoise` 0.30）或 `H3HiresFix`，不要指望这条链路。
3. **长度上限**：整段一次 VAE 编解码，显存随帧数线性涨。16 GB 卡实测 451 帧 6.8 GB，约到 1200–1500 帧（50–60 s）就见顶；更长先分段时间码再拼，或换 MMH3 的分块管线。

**与 §2.10 的分工**

| | §2.10 MMH3 二采 | §2.11 latent 放大 |
|---|---|---|
| 是否重采样 | 是（每块低 sigma 精修） | **否** |
| 画面结构 | 可重绘细节与质感 | 与源片一致 |
| 速度 | 分钟级、随 denoise 与块数 | 165 s / 19 s 素材 |
| 适合 | 想让画面「更贵」 | 只想让画面「更清」 |

## 2.12 多镜容器的容量与打包（2026-11-12 实测）

同一场连续动作要多次切镜时，先决定是「放进一个多镜容器一次生成」还是「逐镜独立生成再拼」。判据不是镜数，是**显存**。

**实测容量（win-desktop RTX 5070 Ti 16 GB，CORE `H3MultishotSampler`）**

| 项 | 数值 |
|---|---|
| 单镜训练范围 | 124–362 帧（5.2–15.1 s） |
| 单镜节点硬上限 | multishot 采样器：481 帧（CORE）/ 1450 帧（V2）；`MiniMaxH3ReferenceToVideo` 单节点 length：5–3600 帧（两者是不同节点，别混） |
| `shot_count` 上限 | 8（CORE）/ 64（V2） |
| **两镜 226+226 = 451 帧** | 峰值 **15096 MiB**，耗时 470.8 s |
| 同结构 V2 451 帧 | 峰值 15124 MiB，耗时 445.7 s |

**真正的天花板是容器总帧数，约 450 帧（18.8 s）**——这是显存物理上限，不是 adapter 的硬拦截。2026-11-18 起 `short_drama_h3q_adapter.py` 对显式 `workflow=multishot` 的作业**放行超限帧数：只在 stderr 告警、不拦截**（未声明 workflow 的调用仍按 451 拦，防止别的路径误用绕过显存保护）；超过 451 帧会 OOM 的风险由创作者自行承担。帧数线性吃显存，`shot_count` 不是限制条件：

- `2 × 15 s`（720 帧）会 OOM，`3 × 12 s`（864 帧）同样；
- `2 × 9.4 s`（451 帧）是实测能跑满整个 16 GB 的形状；
- 单镜 362 帧（15.1 s）可以，但同容器里再塞第二镜就应把总帧数压到 ≤450；超了不会被引擎拒绝，但 OOM 风险自负。

**打包规则**

1. 连续切段若总帧数 ≤450 → 用一个容器，接缝由模型内部处理，不再做末帧接力。
2. 总帧数 >450 → **建议**按语义闭合点拆成多个容器或逐镜独立生成；不要为了塞进一个容器把动作压缩后让尾部静止。adapter 已放行，这类作业会照常提交，拆不拆由创作者按显存判断。
3. 换场硬切永远独立成段，不进容器（没有连续接缝需求，硬切即可）。
4. 容器内的每镜仍各自 ≤362 帧，且每镜要有独立职责与可信起止状态。

**与叙事镜长的关系**：分镜先按声音事件定镜长，再用本节的容量决定怎么打包。镜长 12–15 s 的连续段通常两镜就超 450 帧，只能逐镜生成，接缝要按「末帧接力 + 剪辑层」预算；想把两镜放进一个容器，就要把单镜压到约 9.4 s。

**长镜的模型风险（2026-10-30 角色C EP01 实测）**：13.667 s 的「静→动」单镜在 8.5 s 之后模型开始重建角色（同一角色出两份）并吞掉升高、后拉指令；压到 10.125 s 并补人数与连续体声明后成立。同一批把两处相邻同事件镜合并（8 s / 10.125 s），8 镜降 6 镜、切点 7 降 5、台词一条没删，观感立刻连起来。

- 判据是**事件密度**，不是时长上限：去掉这个切口观众还看得清后果，就合并。
- 静→动、人数变化、指令堆叠的镜头要更保守，优先压到 10 s 附近。
- 顶到 15 s 上限的单镜必须逐句核对对白落点，尾部不带新事件。

## 2.13 续接的两条路：Ref2VA 末槽 vs 纯 I2VA 首帧（2026-11-13 实测）

`h3qc submit` 有两条输入分支，模型和步数完全不同：

| 分支 | 触发 | 模型 | 步数 | 身份 / 构图 |
|---|---|---|---|---|
| I2VA | `--first-frame` | `minimax_h3_fl2va_turbo_Q4_K_M.gguf` | 8 | 只在该分支的纯 I2VA 提示词下稳定 |
| Ref2VA | `--refs` | ref2va int8 + 32B TE | 20 | 稳定 |

**两条路要配各自的提示词，混用会悄悄失效。**

- **Ref2VA（带身份/地理图）**：把上一段真实末帧放**最后一个参考槽**，正文用
  `The shot opens on the same framing as <Picture N>.` 起句。2026-11-13 EP003 001→002a 实测：
  首帧与上段末帧构图、身份、道具数量一致，剪硬切无缝感。
- **纯 I2VA（首帧接力）**：`seam-transition.md` 第七组实测帧差 3.38，条件是整段**不带任何参考图**、
  正文按首帧三段结构写。这条分支一旦混入 Ref2VA 式的 `<Picture N>` 定义与对齐首行，
  2026-11-13 EP003 002a 实测首帧不生效（角色、服装、画风全部更换，与所给首帧无关）。
- 需要身份 + 起点时，Ref2VA 是唯一同时拿到两者的路；只要动作连续、能接受丢掉参考图，纯 I2VA 更准。

**槽位纪律（Ref2VA）**

1. `--refs` 的传入顺序就是 `<Picture 1..N>` 的顺序。角色在前、场景居中、构图参考在末槽。
2. 生成入口要把文档里的 `Image N` 逐条换成 `<Picture N>`，定义行也要保留（gate G08b 查每个上传槽位有标签、G21 查 base 对齐首行）。
3. 槽位编号与正文引用不一致时，模型会按错图取参考——这种错误 gate 查不出来，只能靠出图/出片自看。
4. `--first-frame` 与 `--refs` 互斥，代码直接报错。

## 2.14 多窗一次生成（H3 Multishot，2026-11-13 接入 h3q）

### 先判断要不要用多窗（2026-11-20 定，给后续 agent 的选路依据）

**默认单镜 `pdd`，能拆成两个单镜就拆。** 多窗不是"同机位就该用"，它只解决一件事：
同一机位、同一场景里，动作或对话必须无缝连续，拆成两段会有肉眼可见的接缝。

| 判断 | 选哪条 | 依据 |
|---|---|---|
| 这镜能不能拆成两个单镜（各自有首帧/参考） | **能拆就拆，走单镜 pdd** | 单镜走 8 步蒸馏、快于多窗记忆采样约一个量级（多窗无 pdd 版本）；带日期耗时实测格见 seam-transition.md §0.2 multishot 行 |
| 是否同机位同场景、且接缝必须无缝（动作接力、连续对话、光影不能跳） | 才考虑 multishot | context_pin 把上一窗末 22 帧 raw latent 钉进下一窗 |
| 只是"同一个房间，先后两个动作" | **不算**，拆单镜 | 用上一镜末帧当下一镜首帧即可，EP005 002 就是这么过的 |
| 有静默窗（这一窗没人说话） | 慎用多窗 | ref2va 会给静默段编台词，调参压不住，只能后期换底噪或 guide_audio 锁音轨 |
| 创作者反馈"还是有硬切"，逐帧看机位/光影/人物大小都连续 | **先判型再动手——多窗救不了词层的缝**：先判缝型再动手：查某角色的入场/落位是不是被压缩成"中途姿态凭空出现"（镜内相位断），还是只有情绪在切点跳档（情绪缝）。判型顺序见 seam-transition.md §0.1 第 0 步、词层修法判据见 `h3-prompt-writing/references/failure-modes.md` 对应行，本表不复制。修完词才重出，别反复重做容器 | EP004 006+007 三轮三个根因（2026-11-19/20）：多窗钉死画面缝后，"抱起来那一下"=妈妈入场被压缩，下一轮"瞬间开哭"=情绪跳档，同一条片两个硬切两个不同根因，都修在词层 |

**代价要写进决策**：双窗 20 分钟以上（EP005 S-002 实测 26 分钟）；需要 `scene_video`
做场景锚，否则房间会被重画；静默窗有编台词风险。

**选路硬依据（2026-11-21 实测）**：单镜 `first_frame`（锁首帧）与 `refs`（身份板）在 adapter 层**互斥**，同 job 不可兼得（直接报错）。所以**双人同场、既要锁起帧又要双身份板的连续段，只有 multishot 一条路**（两窗各挂各的身份板）——别再试「单镜带两人」绕路。context_pin 验证状态见 §2.16 末段 2026-11-21 更新（0.45.3 已实测通过）。

**反面教材（2026-11-19/20）**：EP005 002 走双窗，26 分钟出片，盘里摆着冰棍、练习册提前
摊开，判废。改成单镜拆成 002a（关门+两句独白）+ 002b（大肥鱼入场）后，002a 接缝与台词
一次通过。**"同机位"本身不是用多窗的理由。**
**反面教材之二（词层缝，2026-11-19/20）**：EP004 末段 006+007 多窗把画面接缝做到几乎逐帧一致，
创作者仍连续两轮判"还有硬切"——两轮根因不同：第一轮"抱起来那一下"是**妈妈入场被压缩**（入场与落位被写成一拍，模型画出"已经弯腰在那"的中途
姿态，无入场过渡帧）；第二轮"瞬间开哭"才是**情绪跳档**（窗 1 结尾委屈含泪 → 窗 2 开头 0.7s 内
张嘴大哭）。两轮修法都在词层、不在容器——判型顺序见 seam-transition.md §0.1 第 0 步，逐条判据与
修法见 `h3-prompt-writing/references/failure-modes.md` 对应行，本节不复制。多窗管不了词层的相位断。

### 通道与参数

同机位且确需无缝连续时，用 `--workflow multishot` 一次出两窗，接缝由模型内部处理。

**通道**：`h3qc submit --workflow multishot --frames-per-shot 226 --shot-count 2 --refs a.png,b.png,...`
→ h3q 调用 `scripts/multishot_render_ref.py` → **V2 `H3MultishotMemorySampler`（模板 `config/multishot-v2.json`）**。

> **2026-11-15 起 multishot = V2 取代 CORE（操作者指令"去掉 CORE 全部替换"）**。改动已落地并实测跑通全生产链（h3_generate_video → h3q.py → multishot_render_ref.py → H3MultishotMemorySampler+context_pin → 8199 → 出片）：
> - 模板：`config/multishot-core.json` 保留为历史；现用 `config/multishot-v2.json`（MemorySampler node30、context_pin、pin_frames=22、output_scale=1 不超分、SaveVideo node27 / SaveAudio node28）。
> - 渲染器 `multishot_render_ref.py` 已改为 v2 节点映射（sampler 8→30 / save 11→27、12→28）；原 CORE 版备份 `.bak-core-20261115`。h3q.py multishot 分支参数不变、完全兼容。
> - **v2 内建超分不用**：`output_scale=1 / upscale_model_name=(none)`。v2 内建 latent 超分（`(H3 latent x1.5/x2)`）在本机 16G 出片发糊、多窗更慢到出不来，不可用（见记忆 h3-v2-latent-upscale-bad-on-16g）；要超分走成片后处理 `h3_upscale_video`（§2.11）。
> - **必须注册的多角色参考参数**（渲染器已加）：
>   - `reference_subjects`（如 `"1,1"`=2图2人 / `"3,3"`）：多角色参考不分组会被当同一人 blend。**2026-11-19 起渲染器不再自动编 `"1,1,1"`**——它以前按 refs 张数"每人一张"兜底，等于给场景锚也造了一个从不出现的"第三个人"；现在留空就交给节点默认（全部 `<Subject 1>`），并由渲染器日志告警。**V2 记忆采样器没有「这张图只当场景、不当人」的参考输入**：`reference_subjects` 只能把图片分组到 `<Subject N>`，同场连续任务里的场景锚仍会占一个 subject 名额，这一点写在 MCP/渲染器参数说明里。端到端路径：`h3qc --reference-subjects` → `params.reference_subjects` → `h3q` 白名单 → `multishot_render_ref.py --reference-subjects`。
>   - `reference_image_size`：`match`=缩到生成画布（省显存快）；`max`=参考图原生(≤2048)不缩（清晰但 shot2 offload 更重更慢，实测 2×141 双窗 max 约 12min vs match 约 9min）。**默认 match**——渲染器 `multishot_render_ref.py` 的形参缺省、adapter 未声明、MCP 未声明三处都是 `match`，任一处都不按 `max` 兜底；需要保留参考原像素时才显式传 `max`。
>   - **端到端参数路径（只有这一条）**：`h3qc submit --workflow multishot --reference-image-size match|max` → 写入 `params.reference_image_size` → `h3q.py` 白名单原样转发 → `multishot_render_ref.py --reference-image-size` → 采样器输入。跳过任一环就是静默丢弃，不要绕过 h3qc 直传渲染器。
>   - `same_scene_continuous`：**不是渲染器参数**，`h3qc/h3q/renderer` 都不认识它；它只存在于 adapter `parameters` 与 MCP 入参，必须在提交前完成校验，验不过就不提交。只在显式声明 `true` 且 `workflow=multishot` 时生效，要求同组同时具备：①至少一张已准入的**身份**参考；②一个明确的 `scene_anchor_index`（adapter 用 `reference_bindings` 的 1-based 序号；MCP 用 refs 的 1-based 序号）指向**已准入的地理/构图锚**；③bindings 的 `may_control` 写清身份职责与地理/构图职责，`must_not_control` 不得否认。换场、硬切、未声明都完全跳过这条校验，行为与引入前一致；非 multishot 作业显式 `true` 直接拒绝。
> - **场景锚首选 `scene_video`（2026-11-19 晚起端到端接通）**：同场连续时给上一镜已验收成片的
>   片段，走 `reference_video`（LoadVideo → GetVideoComponents → H3ReferenceVideo），节点把它声明为
>   「同一场景的早先时刻」，保留取景、机位距离、房间内容与色温。**不要再把场景图塞进 `refs`**：
>   记忆采样器会把 `reference_images` 里每张图都声明成「`<Subject N>` 的照片」，场景图会占掉一个
>   人物名额并把画面拉向人脸（EP005 S-002 实测：只用文字描述场景时整间房被重画成远景；接上
>   `scene_video` 后构图与 001 完全一致）。参数：`scene_video`（片段文件）、`scene_video_start`
>   （默认 8.5 秒）、`scene_video_seconds`（默认 3.0 秒，2-4 秒足够，更多只增加每步 token 开销）。
>   音频不接，采样器自动配静音，只带房间与光线。与 `scene_anchor_index` 二选一，同给直接拒绝；
>   仍需至少一张已准入的身份参考。端到端路径：MCP `scene_video`（project 入口给项目相对路径，
>   自动转绝对并 scp 到 ComfyUI input/，**不走图片缩图管线**）→ `h3qc --scene-video` →
>   `params.scene_video` → `h3q` 白名单 → `multishot_render_ref.py --scene-video`（运行时注入
>   200/201/202 三个节点，模板保持干净）。`--model` 同日接通，可覆盖模板 checkpoint，不必再为
>   换权重复制模板；`bank_clip_frames` / `audio_pin_frames` 也已透传到同一层。
> - **`auto_chunk_ffn`（2026-11-19 起默认 on，端到端已接通）**：权重装不下时，用 sol-attn 的
>   `MiniMaxH3ChunkFeedForward` 把 FFN 分块（chunks=2），让 DiT 保持驻留，而不是每步从内存
>   流式加载。**EP004 v5 006/007 实测**：294f×2 @1344×768，权重 10.9GB + 激活池 2.3GB 超过
>   14.4GB 可用，`loaded partially; 2067 MB offloaded`，**626 秒/步**（正常 6 秒），8 步 83 分钟；
>   `H3AutoReserve` 已明确警告「这不是慢渲染，通常会在 CUDA kernel 里死掉并带走服务端」。
>   路径：`h3qc --auto-chunk-ffn on|off` → `params.auto_chunk_ffn` → `h3q` 白名单 →
>   `multishot_render_ref.py --auto-chunk-ffn` → node 30。缺 sol-attn 时节点打印 `skipped`
>   并照常跑，不会因为开关而失败。
> - **慢的根因不是参考图**：参考图只占几 MB，`reference_image_size=max` 也只是让 token 每步多走一遍。
>   真正吃显存的是 **10.9GB 权重 + 2.3GB 激活池**；把参考图挪去 RAM 救不了每步流式加载。
>   要提速只有三条：①`auto_chunk_ffn` 让权重驻留；②降 `frames_per_shot`（294→226→141）；
>   ③降画布。三条都不改变叙事，只改单窗时长。
> - **多窗代价仍在**：v2 每多一窗记忆库+22帧latent 使 shot2 起必 offload，慢；单镜快、多窗长片 16G 上代价高。
> - **已知双层压缩**：上传层 `REF_LONG_EDGE=2048`（MCP `_prep_for_upload`，全档位通用）对长边>2048 的参考图仍会 PNG 下采样（如 3104 三视图板→2048）；`reference_image_size=max` 只保证 2048 内不再缩。身份参考尽量用单张≤2048 图，别塞超大拼板。

**script 格式**：一个文件，两窗之间用单独一行 `---` 分隔；每窗写自己的 `00:00.000 → 00:09.417` 时间线、对白与可见状态。
不要写 `subject_definitions:` / `integrated_multimodal_description:`（那是 Ref2VA/Base 的六段三段结构）。

> **窗口正文不要以 `[` 或 `{` 开头。** `H3MultishotMemorySampler` 用 `text.startswith("[")`
> 判定整份脚本是不是 JSON 数组；以 `[Shot 1] ...` 开头的窗口会被当成坏 JSON，
> 自动修复失败后抛 `H3 script looks like JSON but does not parse`。
> **2026-11-19 EP004 v5 006/007 就是这么白烧的**：9.6 秒后 node 30 `execution_error`，
> 而脚本内容本身完全正确。窗口正文直接从场景/人物写起即可。
>
> **2026-11-19 起三层都会在提交前拦住这个错误**：
> ① `h3_gate.py --mode multishot`（G39 查窗口数/窗口开头/单镜段名混入，G40 逐窗查
> `<d>` 格式、`<d>` 外中文、每窗 15s 上限）；② adapter `verify_multishot_script`
> 在 SSH/上传前拒绝；③ MCP `_verify_multishot_script` 在建临时文件前拒绝。
> **多窗不再「整块豁免结构项」**——那是把检查删掉，不是适配。

> 第二窗开头**没有必须复述前一窗收尾状态的通用硬规则**。V2 `H3MultishotMemorySampler` 已在 latent 层用 `context_pin`
> 把前一窗末 22 帧钉进下一窗，接缝连续性不依赖提示词复述；只有在换机位、换主体或正文自身需要交代起点时才重述，
> 否则重复描述会与第一窗的收束句冲突。个别历史案例写过「chain boundary is a clean same-camera cut」，
> 那是该案例的写法，不是 multishot 的准入条件。

**实测（2026-11-13 EP003 001+002a）**：2×226f → 451f / 18.792s / 768×448，内部接缝 PSNR **31.9 dB**
（同一对镜头逐段生成再拼为 23.4 dB，肉眼可见人物放大约 6%、妈妈背影变宽）。

**音色跨窗必须钉住（2026-11-13 EP003 005+006 实测）**：`H3MultishotSampler` 有两个开关决定音色：

- `seed_per_shot` 必须保持 **True**。节点作者的实测原话是「每窗换 seed 才跨窗保住脸；所有窗共用一个 seed
  会让脸和声音一起漂移」。渲染器曾把它设成 False，结果第二窗音色明显变调（F0 291 → 364 Hz）。
- `self_anchor_voice=True`：第一窗渲完后，它自己的音频成为后续每窗的 `<Audio 1>` 参考，音色钉在模型
  实际念出来的那一版上。实测两窗角色C F0 340 / 327 Hz（差 0.7 个半音）。第一窗要安排一句干净独白。

需要跨集、跨文件固定音色时喂外部音频：`H3MultishotSampler` 有 `voice_ref` / `voice_ref_2` / `voice_ref_3`
（AUDIO，接 `LoadAudio`），底层官方节点 `MiniMaxH3ReferenceToVideo` 也有 `ref_audios`（最多 3 条，
提示词里写 `<Audio 1>`）。`ComfyUI-H3-Multishot` 自带 `H3ReferenceAudio` 负责转 32 kHz 立体声。

**参数与限制**

| 项 | 值 |
|---|---|
| 单窗帧数 | `17k+5`，226f = 9.417s 已验证；单窗 ≤362f |
| 总帧上限 | 16 GB 卡实测 ≤450；adapter 已放行，超限只告警不拦截（见 §2.12） |
| 输出尺寸 | 直接给 `--width/--height`（768×448），没有 pdd 二采放大；要更大走 §2.11 latent 放大 |
| 参考图 | 走 `--refs`，最后一槽放构图参考；数量可变（renderer 动态重建 ImageBatch 链） |
| 身份 | 走首窗的完整人物描述，不靠 `(Sx)` 之外的东西 |

**分工**：同机位连续、总帧 ≤450 的段落用 multishot 一次出；换场、反打、总帧超限**建议**按 Ref2VA 逐段生成再硬切（adapter 已不再按 451 硬拦，超限会照常提交，显存风险自负）。

**闸门**：multishot 脚本用 `h3_gate --mode multishot`，由 G39/G40 检查每窗格式与时长（每窗 ≤15s），G25 在 multishot 模式下不注册、不适用。
组窗前先用 gate 逐条检查每个**单镜**提示词（`--mode ref --frames <单窗帧数> --refs N`，必须 0 error）；单镜 >15s 默认被 G25 拦。
`--allow-long-video` 仅供不经 h3q 的手搓直投通道显式豁免长端 warn，h3q adapter 不透传该 flag；h3q 常规路径仍受 G25 error 兜底。

**长镜末段回灌参考图（2026-11-13 EP003 010 实测）**：12.958 s 的双人镜（身份板三视图 + 场景板 + 构图参考）在后段把画面切成灰底三视角角色板，等于把参考图直接渲进成片。正文结尾补一句「同一花园取景保持到最后一帧：脚下草地、身后木栅栏与黄花、上方蓝天、影子朝右」后重出，回灌消失。长镜（≥10 s）且挂角色三视图时，结尾要显式锁场景与机位，别让「两人并排微笑」成为正文的最后一句。

## 2.15 画质增强路线与交付规格（2026-11-14 定版，后续出片必读）

**通道状态（2026-11-15 更新：无缝链统一 v2，CORE 停用）**：多镜头长叙事拼接**只用 `H3_Seamless_Chain_v2.json`**；`H3_Seamless_Chain_CORE.json` **自 2026-11-15 起列入停用入口，不再从它起新活**（需求方拍板，见角色C仓库 `01-创作文档/H3无缝衔接-两方案与验证清单.md` 〇节）。理由：v2 的记忆采样器 `H3MultishotMemorySampler` 带记忆库、默认衔接 `context_pin`——前一镜末 22 帧以原始 latent 直钉下一镜，不过 VAE 解码再编码，运动速度/方向/颜色位级一致，接缝处重生成约 0.92 s 在解码时剪掉（需装 ComfyUI-H3-Motion-Context）；CORE 是 fl2va 尾帧接首帧，每跳过一次像素空间、保真不如 latent 直钉，其唯一优势（零第三方依赖、随开随跑）在统一环境后不再需要。**注意 v2 的 texture ratchet**：每接一次纹理锐化约 +13%，单链建议不超过约 4 个窗口（30–40 s）；`seed_per_shot` 保持开（实测更保脸）；音频每跳略闷，长链在场景切断处重启新链。
- 本机落点说明：win `E:\H3-Studio` 上从未落过正式 `workflows\H3_Seamless_Chain_CORE.json`/`v2.json`，只有 `agent-mcp\jobs\h3ms-20261112\` 下两份实验 tmp 快照；2026-11-15 已把 `H3_Seamless_Chain_CORE.tmp.json` 移入同目录 `_stopped\` 并加 `.STOPPED`（v2 tmp 保留）。生产在用的 `E:\H3-Studio\config\multishot-core.json` 是 `H3MultishotSampler` 通道（**2026-11-15 起 h3q multishot 已改用 `config/multishot-v2.json` = `H3MultishotMemorySampler`，见 §2.14**；multishot-core.json 保留为历史），与 CORE/v2 两套实验草稿不是同一份文件。
- 两方案（待本地验证，非本次落地）：方案一 LD 收尾超分（`output_scale=1.0` 是坑——接了放大模型时 1.0=不修正≠关，4x 模型会满 4x 输出；放大模型 3D 动画先试通用 `RealESRGAN_x4plus` 非 anime_6B）；方案二 `H3_Keyframes.json` 单镜头锚定（≤15s，关键帧硬钉约 26dB）。

**「两个口」口径（2026-11-15 考证）**：11-11 `session-e4dfa006` seq 1551 的 `ask_user_question`「中间那条转视角接缝镜，用哪种输入？」给出的两个选项是 `refs`（全参考组当构图参考）与 `first_frame + last_frame`（首尾帧插值）；10-22 `session-90a8c286` seq 2604 也问过 FL2VA / Ref2VA 二选一。11-14 创作者说「这两个口都不用了」，落点是**不再把它们当画质/超分路线**，与本节「不属于画质增强入口」一致；两项输入功能保持可用，生产仍靠 `refs` 挂身份板与场景板。`H3_Seamless_Chain_CORE`（**已停用**）/ `V2`（**当前唯一无缝链**）是另一回事。

**定位**：§2.11 的 latent 放大是给二次采样准备更大网格的中间步骤，不是成品超分器。纯放大链路 `VAEEncode → H3LatentUpscaleLBH → VAEDecode` 没有第二遍扩散采样，直接解码可比源片更软；社区共识是放大后必须接 Stage 2 低 σ refiner（<https://comfyui-wiki.com/en/news/2026-08-08-minimax-h3-latent-upscaler>、<https://github.com/LBH-123-AI/Comfyui_Minimax_h3_latent_Upscaler>）。把它当终端放大器用属工具错配。

**P0 前置（任何超分方案之前，按顺序做完）**

1. **装配脚本的交付规格随超分输出走**，输出 `scale=WxH` 不写死成 1024×576；素材放大后硬编码会把收益在输出层 downscale 掉。
2. **修画幅**：1536×896 强拉 16:9 会变形，用 1536×864 或先 pad/crop 到同一比例。
3. **同尺寸 A/B**：放大版与源版归一到同一尺寸再比，把「模型收益」与「交付层缩放」分离。
4. **两条目标分开评估**：「同尺寸低 σ 重采样」（目标仍 1024×576，重画线条后缩回）与「像素超分后保持高分辨率交付」（输出 1536×864 / 1080p，必须同步改装配规格）。
5. 锐度、PSNR、SSIM 只作定位；结论按整段完整播放的实际所见写，抽帧与 ffprobe 代替观看。

**P0 三层落地（2026-11-14 已改）**

| 层 | 位置 | 改动 |
|---|---|---|
| 文档 | 本节 + `concat-video/SKILL.md` 铁律 | 交付规格随素材走、同尺寸 A/B、按镜头内容分叉 |
| 脚本 | `剧集/EP003/脚本/concat.py` | 交付规格自动随素材：扫描 ORDER 全部素材源宽，任一段宽>1024（放大版 1536）则输出 `1536x864`，否则 `1024x576`，无需手工设 `CONCAT_OUT_SIZE`（显式设环境变量仍可覆盖）；`force_original_aspect_ratio=increase + crop` 取代强拉 16:9 |
| MCP | `~/.local/lib/magpie-h3-mcp/server.py` 的 `h3_upscale_video` | 新增 `aspect="16:9"`：只给 `scale` 时按目标宽反推 16:9 高（1536×896 → 1536×864）；显式给 `height` 时优先。MCP 长驻进程，改动需重启该服务后生效 |

**R1 离线实测（2026-11-15）**：两档交付规格真实渲染 4 产物全部 1024×576 / 1536×864、无黑边；固定 1024 档同尺寸 A/B 净 **−20.51%** lap_var（源 130.451 → 纯缩放往返 112.702 → latent 放大缩回 103.697），**收益被输出层吃掉并转负**；1536 档同尺寸 A/B 源版纯上采样 41.383 vs latent 放大版 54.301（**+31.22%**），只有同步 `CONCAT_OUT_SIZE=1536x864` 才保留。1536×896 强拉 1536×864 使圆帽 w/h ×1.0367 / h ×0.9649（变形），`increase+crop` 只裁上下各 16 px、w/h ×0.996~0.999（保形）。`server.py` 的 `aspect` 逻辑与 schema 离线 8 例 PASS、`py_compile` PASS；**实出一张需 MCP 长驻服务重启后参数才可见（本会话工具 schema 未含 `aspect`），标「需 GPU + 需重启」**。

**U1/S3 定案实测（2026-11-15，已定为交付方案）**：EP003 MS001（1024×576/447f）三种超分同尺寸 1536×864 lap_var 对比——U0 纯 lanczos 插值 42.76（基线）／**U1 latent 放大（`h3_upscale_video(width=1536, aspect="16:9")`）57.38 = +34.17%**／U2 放大→缩回1024→再放大 33.90 = **−20.73%**。三条结论固化：① **交付超分定 U1**——latent 放大相对 lanczos 基线 +34% 净增益，只加细节不重绘（不加第二遍扩散，不与 §2.11「不是成品超分器」矛盾：那说的是相对**源片**可能更软，这里 +34% 是相对**插值基线**，对 768/1024 小图拉 1536 有意义）；② **绝不缩回 1024**（U2 证明 −20.73%，比不放大更差），装配层 `CONCAT_OUT_SIZE` 必须随素材 1536×864；③ **像素超分 SeedVR2 仍 FAIL**（过锐化），只有 latent 放大可用。`aspect="16:9"` 生效前提是**重启 MCP 长驻服务**（旧进程按 scale=2 会得 1536×1152/1536×896）。
**接缝 cross-fade 定案**：S1 同段内窗缝 ΔYAVG 仅 1.3（模型内部已连续，不处理）；S2 跨镜头硬切帧间 MAD 76.59；S3 同素材 cross-fade d=0.25 把切点 MAD 压到 **15.93（降 79%）**。cross-fade 是**按切点启用的工具、非全量规则**——场切/反打/回主位（EP003 剪辑单 §2 的 C2/C3/C4/C5/C7/C9/C10）硬切是导演意图，默认保持；只有剪辑明确要求柔化某缝时才在 `concat.py` 的 `DISSOLVE` 里加条目。

**试验顺序（按镜头内容分叉）**

**按镜头内容分叉，不按单帧锐度分数排序**。Sogni 2026-09 横评（<https://blog.sogni.ai/blogs/minimax-h3-upscaling/>）：FlashVSR v1.1 单帧推断细节最锐，但**机位推拉／摇移时高频细节逐帧爬行、闪烁**（temporal aliasing），只推荐近静态镜头；MiniMax H3 Latent Upscaler (Community) + refinement 用 H3 自己精修，加的细节跨帧一致、扛得住运动，是 H3 视频的推荐。本机 `models/FlashVSR` 权重为空（11-03 下载被取消），没有通过验收的本机实测。

| 顺序 | 方案 | 适用与要点 |
|---|---|---|
| 1 | **H3 低 σ refiner**（§2.10 `MMH3 Ultimate Upscale` `refine_denoise 0.30` / `H3HiresFix`，<https://github.com/bbaudio-2025/Comfyui-MMH3-UltimateUpscale>、<https://github.com/tazmannner/ComfyUI-H3-ResCascade>） | **运动镜头、长镜头、连续段首选**。成品帧 VAE 回编码后精修，同源质感、保 take、音频原样，跨帧一致。451 f 超 ~300 f 整段上限须时间分块（`chunk 136 / overlap 17`、`--tile-size 0`）；16 GB 只在 362 f / 1536×864 验证过（15.55 GiB、832 s）；空间 tile 会出镜像伪影；低 denoise 仍可能小人物位移，产物重走媒体验收 |
| 2 | **FlashVSR**（<https://github.com/OpenImagingLab/FlashVSR>、<https://github.com/1038lab/ComfyUI-FlashVSR>） | **仅锁定机位／近静态特写**。吃成品 MP4、与生成通道解耦，官方 10 s→1080p 约 41 s；节点在 win `custom_nodes/ComfyUI-FlashVSR`，权重需下载。16 GB 用 Tiny / Tiny Long + `enable_tiling`；451 f 整段必裁 5–10 s（社区报 15 s 长片在 16 GB 崩）；RTX 50 系 Block-Sparse 兼容官方标 unknown，triton 编译报错是高频坑。上镜头前先确认这一镜没有推拉摇移 |
| 3 | **SeedVR2 3B fp8**（已装，§2.10 B 路径） | 特写／交付镜头备选。环境零改动，`inference_cli.py` 可脱离 ComfyUI 跑；官方点名「720p AIGC 轻退化源会过锐化」，正对短剧 draft 素材，大运动不鲁棒。16 GB 用 batch 9–13 + temporal_overlap + VAE tiling + BlockSwap，慢，音轨用 ffmpeg 后合，产出走 `look_check`。**2026-11-15 本机实测 FAIL**：008b 5 s 静态特写过锐化（绒面织纹成规则网纹、硬亮边、皮肤蜡质、指甲白点伪高光、左缘偏色、水枪振铃），时序与人物道具虽 PASS 但降回源尺寸仍 ×1.807 锐度＝重绘加锐；`--prepend_frames 4` 使输出多 4 帧、头部平移、5.0→5.167 s 且无音轨，直接进剪辑会音画/接缝错位；0.11 fps（5 s 片段 ≈19 min），**不为 EP003 存量铺开** |

**不先行**：逐帧 ESRGAN / SUPIR / CCSR / DAT / HAT（无时序建模，官方教程定为 "quick local option but flickers"）、RTX VSR（增强克制到看不出变化）、Wan2.2 / LTX creative 重绘（改头换面，短剧一致性不允许上主线）、Multishot `output_scale`（作者自承 "visibly softer"，只是 decode 后 Lanczos resize，给分辨率不给细节）。

**试验纪律**：一次只投一个 5–10 s 片段；后处理直连 8199 前按 §2.11 校验 `/health` healthy、`external_running=0`、ComfyUI 队列为空，与生成任务错峰；产物整段完整播放验收并落 `look_check`。上述三条都属重绘修复，按新镜头全流程验收。

**multishot 段的硬约束**：服务端 multishot 分支只透传 width / height / frames_per_shot / shot_count / seed / steps，不接受 `tier=final`。**2026-11-15 起 multishot 走 v2 `H3MultishotMemorySampler`（§2.14）**，该采样器**有**内建 latent 超分参数（`upscale_model_name=(H3 latent x1.5/x2)` + `output_scale`），但本机 16G 实测内建超分**发糊不可用**（见记忆 h3-v2-latent-upscale-bad-on-16g），故渲染器固定 `output_scale=1 / (none)`；这类素材要画质，只能走「成品帧回编码 + 低 σ refiner」或「像素域时序超分」/ §2.11 后处理。

**pdd 的 draft→final 不是精修接续（2026-11-15 一手核对）**：`draft → --save-latent → final --from-latent` 语义只存在于已下线的 **lu2** 分支；pdd 分支 draft 只有 `--no-upscale`、final 只有 `--out-width/--out-height`，两路径都不读写 latent，`tier=final` 是**完整两遍重跑、产出新 take**。adapter 与 MCP 已同步：`draft_job_id` / `draft_accepted` / `from_latent` / `refine_denoise` / `chunk_frames` 在 pdd 下不读取，MCP schema 已标注为 lu2 时代字段；SHOT-003 是 `engine=pdd + tier=draft`，结构上没有可接续的 pass-1 latent。升 final 必须锁 **1536×864**（`width*height > 1536*864` 面积判据会硬拒 1536×896），16 GB 一手峰值只验过 362 f。

**R2 生成层实测（2026-11-15，独立 reviewer 完整播放验收 = REVISE）**：用全修订正文（时间线写满 9.417 s、两窗无定格句）重出的 `MS001-重出-v1.mp4`，`silencedetect=-38dB:d=0.6` 仍在 15.497–18.768 留 **3.271 s** 尾段静默（旧素材 3.362 s，仅 −0.091 s），总量 7.299 s / 5 段。完整播放 + 50 张 ≤0.4 s 抓帧 + 尾部 f360–f450 逐帧 MAD（min 0.1522 / mean 1.3665 / max 2.8909，低于 0.05 的帧 **0/90**）证明**画面层持续微动作、不是定格** → 「定格句 + 时间线写满」在画面层生效。声音层根因（只读复核，`验证/R2-声音层根因.md`）：是 `H3MultishotSampler` 生成的音频在 **15.30→15.60 s 平滑收束**（−16.16 → −68.11 dBFS，每 20 ms 降 2–5 dB）后进入 **−64~−66 dBFS 近静音稳态**（非零采样约 98%、峰值 ≤−52 dBFS、音轨全长 18.768344 s / 600587 采样帧完整），**属生成层模型行为，与转码/装配削掉无关**；15.497 只是 −38 dB 阈值穿越点，旧素材跨 take 同形态复现。REV-001 对口修复是**后期合成超市 hum（需创作者授权 DSP）**，不是 `self_anchor_voice`：实际执行 workflow 里 `seed_per_shot=true` / `self_anchor_voice=true` 已由 renderer `set_controls` 覆写到位，两开关只钉声线、不保证环境床连续，关掉还会引入已实测音色漂移；`voice_ref` 未接（R9 三处断点另案）。提示词本轮无需再改（job.prompt 与现用脚本 strip 后逐字相等 4812 字符，script 只是 sampler 一个输入，措辞强度不构成尾段音频控制）。
切点 f225↔f226 的灰度 MAD 4.422 与 RGB 均值台阶 −2.28/−1.76/−1.23 是**模型内部接缝一次局部重绘 + 窗2 曝光微差**（人物左上 9.4/8.2 vs 背景 1.8–4.5，伴刘海/眉/眼斑高光/糖支倾角重绘，量级 <1% 满幅，f227–f242 稳定新水平），**不是** R10 的逐段 GRADE 台阶（全帧均匀、单帧 −11.938 / YAVG step +12.484）；全局归一只能近似拉回整体亮度，消除不了局部重绘。判 PASS 另记 minor REV-002。`R2-成片验收.md:76` 引的 §2.11 `CreateVideo(audio=VHS 音轨)` 是 latent 放大链，本片实际是 `CreateVideo(10).audio=["8",1]`，引用以本节为准。独立 reviewer 六项：look_technical / identity_costume / hand_limb_contact / action_spatial_continuity PASS，dialogue_lip_sync / audio_voice UNVERIFIED（无实听通道）。
另四个多窗正文是 **4 文件 8 窗**，其中只有 `ms_001_002a.txt` 两窗全修订，`ms_005_006` / `ms_007_008a` / `ms_009_010` 共 6 窗结尾仍留 `camera unchanged` + `The window ends on this … arrangement` 静态收束句（「六窗已修订」的口径不成立）。现用成片的静默达标由 `concat.py` CRUSH 裁切达成，生成层 4 段素材最长单处 4/4 全不达标；判据 10.72 / 1.28 的完整口径 UNVERIFIED。

## 2.16 长镜头接住 × 超分的契约（2026-11-14 社区调研）

**硬冲突**：`ComfyUI-H3-Multishot` 的 SETTINGS.md 明确 **two-pass upscale 不可与 `context_pin` / `latent_handoff` / audio spine 同用**——它们把 raw latent 或单条 denoise 轨迹带过接缝，二采保不住，节点直接报错而非静默降级；可用的是 **5 项** `cut / seamless / seamless_tail / first_frame / flf_chain`（SETTINGS.md L118-123 一手原文，此前本节漏了 `seamless_tail`）。两套无缝链工作流保持可用（§2.15），后续选型守这条（<https://github.com/jlucasmcrell/ComfyUI-H3-Multishot/blob/master/SETTINGS.md>）。

**multi 的连续性不止尾帧**：本机 `CONTINUITY_OPT_RAW` 有 7 种（`cut / seamless / seamless_tail / latent_handoff / first_frame / flf_chain / context_pin`，[部署报告:166](<~/Code/kTool/_ops/H3-Multishot-部署报告-20261112.md#L166>)）；多窗一次生成的接缝由模型内部处理，`context_pin` 把上一段尾部 **22 帧 raw latent** 钉进下一段内部关键帧坐标（bit-identical、无 VAE 往返），`latent_handoff` 是单条 denoise 轨迹跨缝，`flf_chain` 是 N+1 张边界板每缝共用一张，官方 `Add Guide` 还能把多张静帧按 `frame_idx` 钉到时间线。**只有 `first_frame` 那一种走尾帧**；把 multi 说成「尾帧接力」是错的。B 的真实难点因此不是「换输入」，而是这些多帧锚与两遍渲染互斥：绕法是降级到 SETTINGS.md 允许的 5 项 continuity（`first_frame` 需换 fl2va checkpoint 且 bank disabled；`flf_chain` 需 N+1 张边界板绑 `keyframe_images`），或在 refiner 里用 `frame-0` 钉源 + frozen overlap mask 保证锚住的帧不被覆盖。`ClipStream Dual` 本机包未装且单卡，其 `offload_model=true` 是 CPU offload 不是分卡，**本机不成立**。`context_pin` 在 ComfyUI **0.45.3 已实测通过**（2026-11-21 EP002 冒烟 job `e354e3e7da4f`，双窗 362f / 576×992 / 带音频）：MC 未激活状态下全链出片、无 MC-missing / shape-mismatch 报错、容器缝 f169→f170 连续——部署报告 §6 基于 0.39 的结论在 0.45.3 复验成立。**边界同时实测清楚：容器只消容器缝**；同片窗 2 内 f191→192 凭空入场、f209→210 景别跳都是词层问题（判型走 seam-transition §0.1 第 0 步、条目查 `failure-modes` 对应行），拿容器救不了词层。

**多帧参考锚定**（都是生成条件，不替代超分）：ComfyUI 官方 `MiniMax H3: Multiframe Reference` 用链式 `Add Guide` 把静帧按 `frame_idx` 钉到时间线（模板 1.5/3.0/5.0 s 三锚、9 图上限，guides 对文本编码器不可见，需并进 `ref_images`）（<https://docs.comfy.org/tutorials/video/minimax/minimax-h3-multiframe>）；`PrefixStream` 的 `Native Masked AV` 用原生 `noise_mask` 保护上一段尾部 AV latent（39 帧，H3 网格 5/22/39/56…，`Trim Prefix` 在像素＋波形空间裁重叠头）（<https://github.com/knoic/ComfyUI-MiniMaxH3-PrefixStream>）；`Motion-Context` / `ClipStream Dual` / `Continuum` 存尾帧与 latent 供下一段复用（<https://github.com/NikoDemon80/ComfyUI-H3-Motion-Context>、<https://github.com/AraneaQwQ/ComfyUI-H3-ClipStream>）；LTX 多关键帧条件 + extension（输入 ≥73 帧、总长 ≤505）（<https://github.com/Lightricks/LTX-Video>）。

**同管线做画质**：`MMH3 UltimateUpscale` 单节点「时间分块（chunk 136 / overlap 17）→ 3D latent upscaler → 每块低 σ 重采样 → 空间＋时间缝合」，音频每 chunk 直通、峰值绑定单 tile（<https://github.com/bbaudio-2025/Comfyui-MMH3-UltimateUpscale>）；LBH `MMH3 Split Upscale` 只做分块精修不含空间放大（REQ 无 width/height），`seam_polish` / `color_match` 是该节点参数，`seam_denoise` 实际在 `MMH3SpatialSplitParamsV10`、`grade_pin` 未在 `/object_info` 命中，`tile 0` 是 CLI 层 `--tile-size 0` 不是节点参数（<https://github.com/LBH-123-AI/Comfyui_Minimax_h3_latent_Upscaler>）；`ResCascade H3 Hires Fix` σ 0.45 + 2 步 + `Face Atlas` 把 512px 脸 tile 缝回 hires 帧（<https://github.com/tazmannner/ComfyUI-H3-ResCascade>）；SeedVR2 用 `--temporal_overlap / --prepend_frames / --color_correction` 跨批次保缝（<https://huggingface.co/numz/SeedVR2_comfyUI>），FlashVSR 用因果 KV-cache 带上一 clip 特征（<https://arxiv.org/html/2510.12747v1>）。

**接缝纪律**（超分后相邻段不跳）

1. 重复边界帧必须裁（像素＋音频波形空间），否则 1 帧顿挫；音频 40 ms equal-power weld 要另补偿，否则每缝短 40 ms、3 镜累计 80 ms A/V desync。
2. **校正放循环外、对成片做单一全局目标**（`color_level=scene` + `master_normalize=luma`）；逐段各自调色实测三镜内纹理 +142%、亮度 +18%，且每个接缝都有台阶。
3. raw latent 接力优先于像素回编码（bit-identical、无 VAE 往返）；分辨率不一致直接拒绝，不悄悄走有损路径。
4. refiner 内 `frame-0 anchor_strength=0.999` + 重叠区 cross-fade + frozen overlap mask，保证连续缝不被覆盖；`Join Match` / `Sigmas Tail` 量亮度、对比、细节台阶。
5. 本机定量：multishot 内部接缝 **31.9 dB** vs 逐段拼 **23.4 dB**；latent 放大后跨镜 MAD 3.2985→2.0899、跨镜/镜内最大比 7.46→1.80（接缝落差未被放大）。装配层不做 cross-fade，因为模型内部接缝已连续。

**后续出片路线排序**

- **A｜只改装配层**（分段后处理 + 全局归一，已随 §2.15 P0 落地）：不重出、不换 take，唯一对存量成片有正收益的一条。
- **B｜下一集主干**：AV latent 续接与时间分块 refiner 放同一张图，同时解决连续性与画质；需改生成通道 / MCP `h3_generate_video` / `h3q.py` 分支 / adapter `VIDEO_WORKFLOWS`，并补接缝验收项。立项前先解决「two-pass 与 `context_pin` 互斥」和「451 f 时间分块在 16 GB 峰值未实测」两个硬点。**R4 入口核查（2026-11-15 一手源码）**：`h3q.py:833-834` 的 `/job` 只认 `kind in ("image","video")`，无后处理 kind；`h3_upscale_video` 的 graph 写死 7 节点纯 LBH（server.py:1120-1133）、schema 无 refine / denoise / chunk / tile；`lu_render_ref.py --from-latent` 的 split 引擎虽是同一套 MMH3 图，但要求 prompt-file + H3 model + 文本 conditioning 与 AV latent cache，451 f multishot 成品只输出 IMAGE、没有 latent。→ **R4 在「不新增入口」下 FAIL / 需工程投入**；最小改法是只改 Mac 侧 `server.py` 加 `refine` 分支（重建半张生成图 + 音频透传 + 重启 MCP，Win 零改动），并把「后处理例外」从「不重采样」扩到「低 σ 扩散精修」，需操作者单独授权。
- **C｜16 GB 上只有阉割版，下一集挑交付镜头试**：官方完整 in-context regeneration（H3-Context-IR + H3-Regenerate-2K）是 hosted，API 只吃未修改 768P、不给权重（<https://nvlabs.github.io/Sana/Open-H3-Regenerate-2K>、<https://github.com/MiniMax-AI/MiniMax-H3>、<https://www.minimax.io/blog/minimax-h3>）；ComfyUI 教程仍写 2K 需单独 upscale pass，核心已合并本地 2K latent upscale 节点（PR <https://github.com/Comfy-Org/ComfyUI/pull/17412> / <https://github.com/Comfy-Org/ComfyUI/pull/17411>）。本地开源替代是 NVIDIA `Open-H3-Regenerate-2K`：冻结 H3 + refiner LoRA → 3D latent 放大（无 decode/re-encode）→ re-noise σ 0.909 → 3 步 Euler / CFG 1 → 2560×1440；多数 ComfyUI 移植丢掉 Context-IR，只有 **IC/Ref2VA 分支**把 draft 留在参考上下文里，接近原意（<https://github.com/NVlabs/Sana/tree/sol-engine/models/Open-H3-Regenerate-2K>、<https://github.com/o-l-l-i/ComfyUI-Olm-Open-H3-Regenerate-2K>、<https://github.com/1038lab/ComfyUI-Open-H3-Regenerate-2K>）。
  **16 GB 门槛**：2K fast VAE 一手峰值 21 GB(5 s) / 45 GB(15 s) 直接超卡；必须 r128 低秩（1.95 GB + Sharp 1.24 GB）、2 步、**stock VAE + tiled decode**、`--reserve-vram 6` + `vae_tile_size` / `window_frames` 分段。可核的最低显存一手成功是 8 GB 笔记本 2K 22–26 分钟/条（<https://www.youtube.com/watch?v=c20x4es0Aqo>）；**5070 Ti 16 GB 无一手 2K regeneration 实测，未找到可靠一手来源**。画质代价：refiner 会改脸、手势与水花，社区建议 LoRA ≤0.7、Sharp 0–0.5，属重生成不是保 take 超分。落地要改 MCP（regen 参数或新工具）＋生成通道（h3q 新 workflow 分支）＋交付规格（§2.15 P0）＋新增「重生成是否改脸、改表演、改小字」验收项；上线前先只读核对 `/object_info` 增量与权重清单，注意 attention/layout patch 所有权冲突（本机 `sol-attn` 的 Sol 与 NVIDIA SoL-Engine 不是同一个东西，[部署报告:198-206](<~/Code/kTool/_ops/H3-Multishot-部署报告-20261112.md#L198>)）。**不为 EP003 存量做**；下一集挑 1–2 个交付镜头先在 1080p 档试，确认不改脸不改词再谈铺开。

**本机核对（2026-11-15 只读实测，投前必读）**：`models/loras` 里没有 r128 低秩权重与 `sharp_curve_branches.safetensors`（三个 1.95 GB turbo LoRA 是步数蒸馏 LoRA，不是 regen refiner，别误判到位）；fast VAE 也不在 `models/vae`，节点 `vae_name` 默认却指向它，首跑会抛 `get_full_path_or_raise`，必须显式接 stock VAE。本机装的是 `1038lab/ComfyUI-Open-H3-Regenerate`，README 原话「The 2K pass gets the same prompt encoded as text only, like NVIDIA's refine」——**text-only refine、丢掉 Context-IR**；IC/Ref2VA 分支（`o-l-l-i/ComfyUI-Olm-Open-H3-Regenerate-2K`）本机没装，R7 的「是否真保留原始上下文」在本机 UNVERIFIED。节点 `INPUT_TYPES` 没有 `vae_tile_size` / `window_frames` / `lock_audio`，等价物是 `audio_mode="silence (reference)"` + Finish 的 audio mux、`temporal_chunking` / `max_frames`、VAE 超显存自动回退 tiled decode，勿按字面参数名投。`--reserve-vram` 当前启动参数是 **0.25**，改成 6 要改 H3-ComfyUI 计划任务并重启；regen 包本身在抢 `PackedLayout` 所有权的冲突名单里。另 `comfyui_version.py` / `pyproject.toml` 是 0.45.3，`git describe` 仍是 v0.39.0、启动参数未动，0.39 上测的 layout 结论未重验。

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
3. `Get-Content E:\H3-Studio\queue\h3q.log -Tail 40` —— 队列自己的日志。
4. `Get-Content E:\H3-Studio\queue\logs\<kind>_<slug>_<ver>_<jid>.log` —— 单任务渲染日志。
5. 仍然 OOM：确认没有绕过队列的提交（查 `E:\H3-Studio\logs\serve.log` 尾部）；必要时降尺寸/步数重投，不要重启实例。

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

Python 客户端可直接 `urllib` 打这些端点；也可以复用 `E:\H3-Studio\scripts\h3qc.py` 的函数。

## 8. 部署物与源码

**队列服务**

- 线上：`E:\H3-Studio\scripts\h3q.py`（服务）、`h3qc.py`（客户端）、`h3q_img.py`（出图执行器）
- 队列数据：`E:\H3-Studio\queue\h3q.db`（SQLite）、`queue\h3q.log`、`queue\logs\`
- 源码副本与本文件同源的说明：`~/Code/kTool/h3-queue/`

**草稿超分档（见 §2.5）**

| 文件 | 作用 |
|---|---|
| `E:\H3-Studio\scripts\mkdraft.py` | 生成草稿超分图（任意提示词 / 参考图 / seed / 帧数） |
| `E:\H3-Studio\scripts\pdd_run.py` | 提交器：先等 ComfyUI 空闲，全程记录峰值显存 |
| `E:\H3-Studio\scripts\validate.py` | 提交前静态校验（节点已注册、输入齐全、连线可达 Save*） |
| `E:\H3-Studio\scripts\run_detached.ps1` | 让提交进程脱离 SSH 会话（否则断线即被杀） |
| `E:\H3-Studio\prod1017\graphs_draft_lu\DRAFT_LU_standard.json` | 已验证的标准档位图（22 节点） |
| `E:\H3-Studio\prod1017\make_graphs.py` | 批量入口；`draft` 档已直接产出超分链路 |

模板源：`E:\H3-Studio\prod1017\eval\graphs\03_submit_pdd_xiuxian_draft.json` —— PDD 图唯一的源头，`mkdraft.py` 和 `make_graphs.py` 都从它派生，改它两边一起变。

**离线研究副本**：本技能 `scripts/` 留有 `mkdraft.py` / `pdd_run.py` / `validate.py` / `run_detached.ps1` / `h3_quick.py` 作历史记录，
其中 `pdd_run.py`、`h3_quick.py` 直连 8199，**不部署、不调用**。

注意它们依赖的目标机环境：ComfyUI 在 `127.0.0.1:8199`、嵌入 python 在 `E:\ComfyUI\ComfyUI_windows_portable\python_embeded\python.exe`、PDD 模板在 `prod1017\eval\graphs\`。
