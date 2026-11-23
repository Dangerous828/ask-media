# 2.11 2026-11-12 latent 放大（成品帧回编码，不重采样）

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
- 权重取自 `models/latent_upscale_models/`：本链路节点 `H3LatentUpscaleLBH` 记录名为
  `minimax_h3_latent_upscaler_3d_bf16.safetensors`（690 MB）。注意本仓
  `scripts/mkdraft.py` 的 `MinimaxH3LatentUpscaler3D` 节点写的是 `..._fp16.safetensors`；
  两条链路节点不同（LBH vs 3D upscaler）、权重各按其节点记录，非同一权重的口径矛盾；部署机核对 `models/latent_upscale_models/` 下实际文件名，
  不符会报找不到权重。
- 纯 video latent 输入也接受（`_streams()` 返回单流时直接放大）；AV latent 输入会原样带过音频流。

**入口一：MCP（推荐）**

`magpie-h3-mcp` 的 `h3_upscale_video`：

```json
{"source": "/path/to/take.mp4", "scale": 2.0, "label": "EP001-upscale"}
```

- 默认 2×，也可显式给 `width`/`height`；`save_path` 缺省为 MCP 默认输出目录。
- 工具自动 ffprobe 源、上传到 `ComfyUI/input/`、生成图、提交、轮询、取回并校验非空。
- 实测：451f / 768×448 → 1536×896，**165.1 s**，GPU 峰值约 6.8 GB。
  这是修正前的旧值：1536×896 强拉 16:9 会变形，交付须用 `aspect="16:9"` 得到
  **1536×864**（见 [`delivery-specs.md`](delivery-specs.md) §2.15）；本实测耗时仅代表该次测量，不代表修正后档位。

**入口二：手工工作流**

固定图模板存内部工程档案（未随公开版发布）；模板结构固定，只需改 `VHS_LoadVideo.video` 与 `H3LatentUpscaleLBH.width/height` 两处值。

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

