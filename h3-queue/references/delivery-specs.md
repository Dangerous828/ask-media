# 2.15 画质增强路线与交付规格（2026-11-14 定版，后续出片必读）

**通道状态（2026-11-15 更新：无缝链统一 v2，CORE 停用）**：多镜头长叙事拼接**只用 `H3_Seamless_Chain_v2.json`**；`H3_Seamless_Chain_CORE.json` **自 2026-11-15 起停用**，不再从它起新活（需求方拍板）。决策经过与 `context_pin` 机制实测见 [incidents.md](incidents.md) §2026-11-21 与 [h3-multishot.md](h3-multishot.md) §2.14。**注意 v2 的 texture ratchet**：每接一次纹理锐化约 +13%，单链建议不超过约 4 个窗口（30–40 s）；`seed_per_shot` 保持开（实测更保脸）；音频每跳略闷，长链在场景切断处重启新链。
- 本机落点说明：win `<渲染机根目录>` 上从未落过正式 `workflows\H3_Seamless_Chain_CORE.json`/`v2.json`，只有 `agent-mcp\jobs\h3ms-20261112\` 下两份实验 tmp 快照；2026-11-15 已把 `H3_Seamless_Chain_CORE.tmp.json` 移入同目录 `_stopped\` 并加 `.STOPPED`（v2 tmp 保留）。生产在用的 `<渲染机根目录>\config\multishot-core.json` 是 `H3MultishotSampler` 通道（**2026-11-15 起 h3q multishot 已改用 `<渲染机根目录>\config\multishot-v2.json` = `H3MultishotMemorySampler`，见 §2.14**；multishot-core.json 保留为历史），与 CORE/v2 两套实验草稿不是同一份文件。
- 两方案（待本地验证，非本次落地）：方案一 LD 收尾超分（`output_scale=1.0` 是坑——接了放大模型时 1.0=不修正≠关，4x 模型会满 4x 输出；放大模型 3D 动画先试通用 `RealESRGAN_x4plus` 非 anime_6B）；方案二 `H3_Keyframes.json` 单镜头锚定（≤15s，关键帧硬钉约 26dB）。

**「两个口」口径（2026-11-15 考证）**：11-11 `session-EXAMPLE` seq EXAMPLE 的 `ask_user_question`「中间那条转视角接缝镜，用哪种输入？」给出的两个选项是 `refs`（全参考组当构图参考）与 `first_frame + last_frame`（首尾帧插值）；10-22 `session-EXAMPLE` seq EXAMPLE 也问过 FL2VA / Ref2VA 二选一。11-14 创作者说「这两个口都不用了」，落点是**不再把它们当画质/超分路线**，与本节「不属于画质增强入口」一致；两项输入功能保持可用，生产仍靠 `refs` 挂身份板与场景板。`H3_Seamless_Chain_CORE`（**已停用**）/ `V2`（**当前唯一无缝链**）是另一回事。

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
| 文档 | 本节 + `../../concat-video/SKILL.md` 铁律 | 交付规格随素材走、同尺寸 A/B、按镜头内容分叉 |
| 脚本 | 项目侧私有装配脚本（如 `剧集/EP003/脚本/concat.py`，未随公开版发布，以实际部署为准） | 交付规格自动随素材：扫描 ORDER 全部素材源宽，任一段宽>1024（放大版 1536）则输出 `1536x864`，否则 `1024x576`，无需手工设 `CONCAT_OUT_SIZE`（显式设环境变量仍可覆盖）；`force_original_aspect_ratio=increase + crop` 取代强拉 16:9 |
| MCP | magpie-h3-mcp（独立部署的 MCP 服务，不入本仓库）的 `h3_upscale_video` | 新增 `aspect="16:9"`：只给 `scale` 时按目标宽反推 16:9 高（1536×896 → 1536×864）；显式给 `height` 时优先。MCP 长驻进程，改动需重启该服务后生效 |

**R1 离线实测（2026-11-15）**：固定 1024 档同尺寸 A/B 净 **−20.51%** lap_var（收益被输出层吃掉并转负）；1536 档同尺寸 A/B **+31.22%**，只有同步 `CONCAT_OUT_SIZE=1536x864` 才保留。逐项数值、圆帽变形倍率与 `increase+crop` 保形数据见 [incidents.md](incidents.md) §2026-11-15 R1。`server.py` 的 `aspect` 逻辑与 schema 离线 8 例 PASS、`py_compile` PASS；**实出一张需 MCP 长驻服务重启后参数才可见，标「需 GPU + 需重启」**。

**U1/S3 定案实测（2026-11-15，已定为交付方案）**：EP003 MS001（1024×576/447f）三种超分同尺寸 1536×864 lap_var 对比——U0 纯 lanczos 插值 42.76（基线）／**U1 latent 放大（`h3_upscale_video(width=1536, aspect="16:9")`）57.38 = +34.17%**／U2 放大→缩回1024→再放大 33.90 = **−20.73%**。三条结论固化：① **交付超分定 U1**——latent 放大相对 lanczos 基线 +34% 净增益，只加细节不重绘（不加第二遍扩散，不与 §2.11「不是成品超分器」矛盾：那说的是相对**源片**可能更软，这里 +34% 是相对**插值基线**，对 768/1024 小图拉 1536 有意义）；② **缺省不缩回 1024**（U2 在这组单片段上实测 −20.73%，比不放大更差；装配层 `CONCAT_OUT_SIZE` 随素材走 1536×864。确需缩回时按同尺寸 A/B 复测后再定）；③ **像素超分 SeedVR2 仍 FAIL**（过锐化），只有 latent 放大可用。`aspect="16:9"` 生效前提是**重启 MCP 长驻服务**（旧进程按 scale=2 会得 1536×1152/1536×896）。
**接缝 cross-fade 定案**：S1 同段内窗缝 ΔYAVG 仅 1.3（模型内部已连续，不处理）；S2 跨镜头硬切帧间 MAD 76.59；S3 同素材 cross-fade d=0.25 把切点 MAD 压到 **15.93（降 79%）**。cross-fade 是**按切点启用的工具、非全量规则**——场切/反打/回主位（EP003 剪辑单 §2 的 C2/C3/C4/C5/C7/C9/C10）硬切是导演意图，默认保持；只有剪辑明确要求柔化某缝时才在装配脚本（未随公开版发布）的 `DISSOLVE` 里加条目。

**试验顺序（按镜头内容分叉）**

**按镜头内容分叉，不按单帧锐度分数排序**。Sogni 2026-09 横评（<https://blog.sogni.ai/blogs/minimax-h3-upscaling/>）：FlashVSR v1.1 单帧推断细节最锐，但**机位推拉／摇移时高频细节逐帧爬行、闪烁**（temporal aliasing），只推荐近静态镜头；MiniMax H3 Latent Upscaler (Community) + refinement 用 H3 自己精修，加的细节跨帧一致、扛得住运动，是 H3 视频的推荐。本机 `models/FlashVSR` 权重为空（11-03 下载被取消），没有通过验收的本机实测。

| 顺序 | 方案 | 适用与要点 |
|---|---|---|
| 1 | **H3 低 σ refiner**（成品帧 VAE 回编码后精修路线：§2.11 latent 放大 + `H3HiresFix`；§2.10 `MMH3 Ultimate Upscale` `refine_denoise 0.30` 为其载体之一，但该 MMH3 二采管线随 lu2 于 2026-11-15 下线、参数仅留离线参考，**不作为现役首选入口**，见 §2.10 退役横幅；<https://github.com/bbaudio-2025/Comfyui-MMH3-UltimateUpscale>、<https://github.com/tazmannner/ComfyUI-H3-ResCascade>） | **运动镜头、长镜头、连续段首选**（指「低 σ 精修 + 保 take」这条路线，不是已退役的 MMH3/lu2 入口）。成品帧 VAE 回编码后精修，同源质感、保 take、音频原样，跨帧一致。451 f 超 ~300 f 整段上限须时间分块（`chunk 136 / overlap 17`、`--tile-size 0`）；16 GB 只在 362 f / 1536×864 验证过（15.55 GiB、832 s）；空间 tile 会出镜像伪影；低 denoise 仍可能小人物位移，产物重走媒体验收 |
| 2 | **FlashVSR**（<https://github.com/OpenImagingLab/FlashVSR>、<https://github.com/1038lab/ComfyUI-FlashVSR>） | **仅锁定机位／近静态特写**。吃成品 MP4、与生成通道解耦，官方 10 s→1080p 约 41 s；节点在 win `custom_nodes/ComfyUI-FlashVSR`，权重需下载。16 GB 用 Tiny / Tiny Long + `enable_tiling`；451 f 整段必裁 5–10 s（社区报 15 s 长片在 16 GB 崩）；RTX 50 系 Block-Sparse 兼容官方标 unknown，triton 编译报错是高频坑。上镜头前先确认这一镜没有推拉摇移 |
| 3 | **SeedVR2 3B fp8**（已装，§2.10 B 路径） | 特写／交付镜头备选。环境零改动，`inference_cli.py` 可脱离 ComfyUI 跑；官方点名「720p AIGC 轻退化源会过锐化」，正对短剧 draft 素材，大运动不鲁棒。16 GB 用 batch 9–13 + temporal_overlap + VAE tiling + BlockSwap，慢，音轨用 ffmpeg 后合，产出走 `look_check`。**SeedVR2 仍 FAIL，不为存量铺开**；逐项症状与数字见 [incidents.md](incidents.md) §2026-11-15 SeedVR2 |

**不先行**：逐帧 ESRGAN / SUPIR / CCSR / DAT / HAT（无时序建模，官方教程定为 "quick local option but flickers"）、RTX VSR（增强克制到看不出变化）、Wan2.2 / LTX creative 重绘（改头换面，短剧一致性不允许上主线）、Multishot `output_scale`（作者自承 "visibly softer"，只是 decode 后 Lanczos resize，给分辨率不给细节）。

**试验纪律**：一次只投一个 5–10 s 片段；后处理直连 8199 前按 §2.11 校验 `/health` healthy、`external_running=0`、ComfyUI 队列为空，与生成任务错峰；产物整段完整播放验收并落 `look_check`。上述三条都属重绘修复，按新镜头全流程验收。

**multishot 段的硬约束**：服务端 multishot 分支不接受 `tier=final`（没有 pdd 二采；v2 内建超分在本机 16G 发糊、固定 `output_scale=1`）。**透传清单以实际部署为准**：完整参数见 [`h3-multishot.md`](h3-multishot.md) §2.14 与 adapter `short_drama_h3q_adapter.py` 的 `multishot_argv()`——除 width / height / frames_per_shot / shot_count / seed / steps 外，还含 `--reference-image-size` / `--reference-subjects` / `--auto-chunk-ffn` 以及 `scene_video` / `scene_video_start` / `scene_video_seconds` / `--model` / `bank_clip_frames` / `audio_pin_frames` 的端到端透传；不要按这里的旧短清单判断参数是否被支持。**2026-11-15 起 multishot 走 v2 `H3MultishotMemorySampler`（§2.14）**，该采样器**有**内建 latent 超分参数（`upscale_model_name=(H3 latent x1.5/x2)` + `output_scale`），但本机 16G 实测内建超分**发糊不可用**（见记忆 h3-v2-latent-upscale-bad-on-16g），故渲染器固定 `output_scale=1 / (none)`；这类素材要画质，只能走「成品帧回编码 + 低 σ refiner」或「像素域时序超分」/ §2.11 后处理。

**升 final 必须锁 1536×864**（`width*height > 1536*864` 面积判据硬拒 1536×896），16 GB 一手峰值只验过 362 f。pdd draft→final 为何不是精修接续（无 pass-1 latent、lu2 字段已下线）见 [`../SKILL.md`](../SKILL.md)「两条通道的档位语义」；首帧取上一段末帧的实测见 [incidents.md](incidents.md) §2026-11-04。

**R2 生成层实测（2026-11-15，独立 reviewer 完整播放验收 = REVISE）**：**定格句与时间线写满在画面层生效**（画面持续微动作、不是定格）；**尾段静默是生成层模型行为，修复走后期合成（需创作者授权 DSP），不是改提示词或 `self_anchor_voice`**。逐帧 MAD、音频收束曲线、切点解剖、REV-001/002、4/4 不达标等完整经过见 [incidents.md](incidents.md) §2026-11-15 R2。

