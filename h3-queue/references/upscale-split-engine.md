# 2.10 2026-11-03 二采 split 引擎（tiled，破 ~300 帧上限）+ SeedVR2 事后超分

> **退役横幅（2026-11-15）**：本节的 split 引擎载体是 **lu2 分支**，该分支已于 2026-11-15 下线（`h3-queue/SKILL.md` §2.10、`h3-prompt-writing/SKILL.md`）。下文「split 引擎（现默认）」里的「现默认」**仅指 lu2 分支内部当时的默认值**，不代表现役可选档——现役二采只有 pdd（见 §2.8）。
>
> **MMH3 参数当前无可用入口**：其载体 `lu_render_ref.py --from-latent` 随 lu2 下线不可达；MCP `h3_upscale_video` 的 graph/schema 不含 refine / denoise / chunk / tile，multishot 成品只输出 IMAGE、没有 latent 可接（R4 入口核查见 [longshot-upscale-contract.md](longshot-upscale-contract.md)）。本节的 `MMH3TemporalSplitParams` / `refine_denoise` / `--upscale-engine` 等参数**仅留离线参考**，不作为生产可用能力；画质走 §2.11 latent 放大或 §2.15 的成品帧回编码低 σ refiner。

**背景**：legacy3d 二采（整段一次过 `MinimaxH3LatentUpscaler3D`，即使开着 `enable_temporal_chunking`）对 311/328/362 帧实测 100% 报 `KSamplerAdvanced [448,96] cannot be broadcast to [1008,96]`，≤300 帧正常。社区结论：长视频放大要在外层做时间分块（temporal chunk）+ 空间分块（spatial tile），每块独立过 upscaler 与采样。

**split 引擎（lu2 分支内当时默认，2026-11-15 起随 lu2 下线，仅离线参考）**：`lu_render_ref.py` 的 pass2 换成 `MMH3 Ultimate Upscale` 单节点管线（bbaudio-2025/Comfyui-MMH3-UltimateUpscale，已装 `<渲染机根目录>\ComfyUI\custom_nodes\Comfyui-MMH3-UltimateUpscale`）：`MMH3TemporalSplitParams(chunk 136/overlap 17) → MMH3LatentUpscaleWithModelParams(3D upscaler 1344×768) → 主节点（每时间块整帧重采样，噪声掩膜保形，frame-0 钉源 + 颜色匹配）`。`--upscale-engine legacy3d` 可回退旧行为。

- **⚠️ 空间分块必须关（`--tile-size 0`，2026-11-04 起客户端默认已是 0）**：破 ~300 帧上限靠时间分块就够，整帧采样显存无压力。镜像伪影实测与历史 bug 见 [incidents.md](incidents.md) §2026-11-04 tile；**2026-11-04 之前不带显式 `--tile-size 0` 跑的 final 都要复检有无镜像伪影**。
- **denoise 语义**：split 引擎精修强度走 `BasicScheduler(denoise=refine_denoise)`；1.0 = 每块按 conditioning 全重绘（内容大漂）。**默认 0.30（2026-11-04 起）**。
  - **0.30 是实测保形点**：`MOTION-EP001-L01B`（311f）与 `MOTION-EP001-L02-ONESHOT`（362f）均到 1920×1088，与同一遍 latent 逐点同构图、同姿态，细节为真实重建（门钉、匾额彩画、舞者五官、裙褶层次、二层观众人形）而非插值锐化。
  - **≥0.45 会开始重绘**：turbo LoRA 是照「纯噪声 4 步」训的，部分 denoise 落在它的训练分布外，模型按 turbo 习惯整体重画。**看到"内容变了"先查 denoise，不要先怀疑 upscaler。**
  - 更保形：0.15–0.25（略软）；想更锐：0.35（动作/质感开始回退）。
- **判保形必须用同一遍 latent**：换一次第一遍就换一次 take。用不同 denoise 的两版互相比、或与历史成片相比，都会把"换 take"误记成"超分漂移"。正确做法见下方 save-latent → from-latent。
- **注意**：LBH 包（Comfyui_Minimax_h3_latent_Upscaler）里的 `MMH3 Split Upscale` 三节点**只做分块精修、不做空间放大**，必须配合先放大过的 latent；完整放大+精修一条龙是 bbaudio 的 `MMH3UltimateUpscale`。两者类名相近易混。
- `h3qc submit` 已透传 `--upscale-engine split|legacy3d`、`--chunk-frames`、`--tile-size`（h3q.py lu2 分支同步；改 h3q.py 后要重启 H3-Queue 计划任务服务才生效）。
- **AV latent cache 节点曾丢失**：`SaveMiniMaxH3AVLatentCache`/`LoadMiniMaxH3AVLatentCache` 的来源包在本机已不存在（2026-11-03 发现），已用最小等价节点补上：`<渲染机根目录>\ComfyUI\custom_nodes\h3_av_latent_cache\__init__.py`（safetensors 存 `video`/`audio` 两个 key）。save-latent → from-latent 链路依赖它。

**多段短片接续（2026-11-04 实测）**：第 N+1 段的 `--first-frame` 必须取第 N 段的**末帧**（`ffmpeg -sseof -0.06 -i <N段>.mp4 -frames:v 1`），不能用分镜关键帧顶替——分镜关键帧描绘的是该段某个中间状态，直接当首帧会让接缝从"上一段终点"直跳到"该段中途"。红裙接缝的实测经过见 [incidents.md](incidents.md) §2026-11-04 L01B→L02。该案例采用单帧视觉接力；当前首尾配对与全参考能力另见本技能「输入能力与续接职责」，不从此历史案例限定所有接缝。

**SeedVR2 事后超分（B 路径，与二采互补）**：已装 `seedvr2_videoupscaler`（numz，`inference_cli.py` 可脱离 ComfyUI 直接跑）+ 权重 `models/SEEDVR2/`（3B fp8 3.2GB + ema_vae fp16 478MB）。ComfyUI 节点 `SeedVR2*` 系列同步可用。实测：draft4（896×512）前 72 帧 → 1260×720，184s（0.39 fps，fp8 无 Sage/FlashAttention）。CLI 必须带 `PYTHONUTF8=1`（GBK 崩 emoji）。适用：救已认可内容的 draft 素材、成片最后一道；产出仍要走 look_check（它是重绘细节的修复模型，不是无损放大）。

**本机环境坑（2026-11-03 实录）**：
1. win 侧 pip/git 配了 `<本地代理端口>` 代理且代理常不在——pip 装 包要 `cmd /c "set HTTP_PROXY=& set HTTPS_PROXY=& ... -i https://pypi.tuna.tsinghua.edu.cn/simple"`；GitHub 大文件从 Mac clone 后 tar + scp 过去（同网段走 `<渲染主机SSH别名-直连>` mDNS 直连，**别走 <渲染主机SSH别名-中转>**，3.7GB 会断）。
2. 装/换 opencv 类包会被运行中的 ComfyUI 锁 `cv2.pyd`（WinError 5）：先停 ComfyUI 再装。
3. 重启 ComfyUI 用计划任务 `schtasks /run /tn H3-ComfyUI`；队列服务是 `H3-Queue`（h3q.py 8200，watchdog 自动拉 ComfyUI）。**别手动 Start-Process 抢端口**。
4. **`gpu.ps1 claim` 的 preempt 会顺带杀掉 h3q 队列进程**（见 19:09 事故，stopping pid … preempted by …，队列 8200 直接死，需要手动 `schtasks /run /tn H3-Queue` 拉回）。手工跑 GPU 任务（如 SeedVR2 CLI）持租约期间，队列渲染会 blocked_vram 等待——任务做完立即 release。
5. hf-mirror 有共享限流；大权重从 Mac `curl huggingface.co` 下载再 scp（校验 SHA256 前 16 位 = HF LFS oid）。
6. 手动 import 测 custom node：ComfyUI 内存日志走 `curl http://127.0.0.1:8199/internal/logs/raw`（JSON entries），能抓 IMPORT FAILED。

