# 2.8 short-drama-produce 接入口

`../scripts/short_drama_h3q_adapter.py` 实现短剧生产工具的 adapter stdin/stdout 契约，让 `prepare → 本次确认 → run/collect` 与本队列共用同一份任务记录。它仍只通过 SSH 调用 Windows 上的 `h3qc.py`／带参考时的 `h3qg.py`，不会直连 ComfyUI。

- 每个 job 只接受一个输出；`idem_key` 包含 job 与 run id，提交后立即把队列 jid 写入 `handle_path` 再轮询。
- `collect_provider_job_id` 只查询并下载既有队列任务，不上传、不重新提交。
- 图像 `output` 为 `saved … bytes` 时优先使用任务参数的真实 `out`；视频 `COPY_OF_RECORD …json` 只读解析记录里的 `comfy_output` MP4，不把 JSON 当成片下载。
- **上传先按 modality 分流**：
  - **`modality=image`：直接上传参考源文件字节，保留扩展名；上传名含唯一请求标识，按绑定顺序编号。** 不经过 `sips`、缩放或重编码。`resolution=0` 由模型按原参考尺寸编码并对齐 32，不代表源像素未经任何模型预处理；采样画布由 `size` 单独指定。
  - **`modality=video`：继续以下按角色分两档的上传策略**（2026-11-08 修订）；以下压缩开关和参考面积归一规则仅用于视频。
  - **`first_frame` / `last_frame` 与 `may_control` 含"起始/首帧/构图/状态"的参考 → 原生尺寸 PNG，绝不重编码。** 这些就是交付像素本身。旧代码用 `sips -Z 1344`，而 **`-Z` 会放大也会缩小**：1536×864 的真实末帧被缩到 1344（模型得自己补回 192px 宽度）、896×512 场景板被拉成 1344×768——**末帧接力交出去的已不是创作者验收过的像素**，这是 flf 契约的根本。只在长边超过 `H3Q_REF_LONG_EDGE`（默认 2048，纯安全上限）时才缩。MCP 旧版还把首帧压成 JPEG q80，属同类缺陷，已修。
  - **身份／造型／道具／场景板 → 长边 768 + JPEG q80（保持实测口径，不动）。** `../../video-studio/SKILL.md` 与 `ref_guard.py` 记着：压完画面更干净，因为板卡噪点不再被放大。该实测出自 Qwen Image 2.1 Turbo 生图（8 步／CFG 1.0／1024×576，4–5 张参考），**H3 视频侧尚未两侧确认**，所以在 A/B 出结论前不因"看起来更保真"就抹掉它。
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
  | `lu2` / legacy（`lib_workflow.build_ref2va`） | 程序化，每张 ref 建一个 `LoadImage` | 无上限（lu2 已下线，仅历史对照） |
  | `pdd_lu`（渲染机侧 `pdd_render_ref.py` + 模板） | 按 refs 动态增删 `LoadImage` 槽位 | 硬上限 9（节点 autogrow `min:0,max:9`） |
  | `mkdraft.py`（本仓手建图 CLI，离线研究副本） | 照模板现有 `LoadImage` 槽位 | **仅 2 槽**：`--ref0/--ref1`，超过模板槽数直接报错 |

  **9 张只走渲染机侧 `pdd_render_ref.py` 渲染器路径**（动态槽位逻辑在该私有脚本内，未随公开版发布，以实际部署为准）。
  本仓 `scripts/mkdraft.py` 是离线研究副本，没有 `--refs` / `grow_ref_slots` / `trim_ref_slots` / `bind_refs`，
  也没有动态扩容；不要用 mkdraft 这条路去验证 9 图，最多 2 张。下方"显存与张数无关"的实测均出自渲染器路径。

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

  → **验构图（draft）可以身份板＋场景板＋道具板全挂上，最多 9 张**（走 pdd_render_ref 渲染器路径；本仓 mkdraft.py 仅 2 槽，不适用），多人镜头不必再用正文文字补身份；
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

  实测记录存项目内部档案（未随公开版发布）。

- **第三条路线：HyperFlow H3 Flash（第三方压缩模型，2026-11-06 开源）——本机 16GB 跑不了，别装。**

  Video Rebirth 出的 H3 压缩版，**独立权重**（13.7B，不到原版 31B 的一半），不是 PDD 之外的一个开关，也不是能叠在原版权重上的 LoRA。4/6/8 步、无 CFG、音画同出（32kHz 立体声）、支持 t2va / fl2va / ref2va（最多 9 图）。

  实测数据（MiniMax 官方上游仓库的 integrations/README.md，1344×768、6 步、2 张参考图）：

  | GPU | ref2v 5.2s / 15s | 峰值 VRAM |
  |---|---|---|
  | RTX 4090 (24G) | 180s / 866s | 22 GiB |
  | RTX 5090 (32G) | 139s / 663s | 30 GiB |
  | **RTX 5070 Ti (16G)** | — | **官方明写 "16 GB GPUs are not measured yet"** |

  **本机不成立的三条硬理由**：
  1. **显存**：峰值要 22 GiB，本机上限 15.92 GiB。现役 PDD 跑 1536×864 已到 15.55 GiB，只剩 0.37 GiB。换 `Q3_K_M` 只省 1.9 GB，而峰值里权重仅约 9 GB、余下 13 GB 是激活值与 VAE，填不上 6 GiB 的缺口。
  2. **没有速度收益**：24G 卡出 15 秒要 866s，比现役 PDD 的 831s 还慢；16G 只会更慢或直接 OOM。
  3. **改动面大**：要 ComfyUI ≥ 0.43.0（版本与运行实例提交号现场核对，以实际部署为准；不同来源的 `git describe` / commit 号可能不一致，判断版本只看 `comfyui_version.py` / `pyproject.toml`，见 [`../SKILL.md` "入口与环境"](../SKILL.md)）、装 `ComfyUI-GGUF` + `ComfyUI-HyperFlow-Flash`、用专属 `HyperFlow GGUF Loader`（普通 loader 不认两时间嵌入器）、整套工作流重写；且要下载约 35 GB（两个 GGUF + 15.7 GB 文本编码器 + VAE），E 盘按部署时实际余量。`<渲染机根目录>` 不是 git 仓库，升级 ComfyUI 后 PDD / LatentUpscaler3D / Sol 那套改动都要重验。

  **什么情况下再来看它**：官方补 16GB 实测数据，或出现 16GB 可跑的精简版。届时重估的唯一看点是**音画同出**这个能力，不是速度。

  来源：[GitHub](https://github.com/Video-Rebirth/hyperflow-h3-flash) · [HF 权重](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash) · [ComfyUI 节点](https://github.com/Video-Rebirth/ComfyUI-HyperFlow-Flash)

- **视频档位 `parameters.tier`（adapter 代码强制，不靠提示）：**

  | engine | tier | 实际参数 | 用途 | 约束 |
  |---|---|---|---|---|
  | `pdd` | `draft`（**缺省**） | `--workflow pdd_lu --no-upscale --sol-profile off`，首采 1024×576 | 验构图/运动/身份。362 帧约 285s | 步数由档位模板固定（8 步）；adapter 会把 `parameters.steps` / `parameters.cfg` 透传到 h3qc 命令行，服务端是否接受以实际部署为准，不要指望靠透传步数改变该档 |
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

