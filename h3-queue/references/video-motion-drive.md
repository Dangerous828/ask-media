# 视频动作驱动：让角色学参考视频里的动作（Ref2VA + 参考视频 + 参考音轨）

> 本文是这条通道的唯一权威。ask-media 路由表与 h3-queue 主文件只留指针。
> **“动作复刻 / motion”在中枢里有两个不同的东西，先分清：**
>
> | 用户的意思 | 是什么 | 在哪 |
> |---|---|---|
> | 把参考视频**当输入喂给模型**，让角色照着做（本文） | 视频动作驱动：参考视频 + 参考音轨进 `ref_videos` / `ref_video_audios` | 本文 |
> | 把参考视频的动作**拆成文字**，写成带时码的英文状态链 `MOTION-...` 再生成 | 文字复刻：`video-shot-reverse` 逆推 + `short-drama-video-prompts` 写 MOTION 词，走 h3q | `../../video-shot-reverse/SKILL.md`、`../../drama-skills/skills/short-drama-video-prompts/SKILL.md` |
>
> 判别：用户说“学这个动作”“照着做”“动作参考视频”“极乐净土那种”“音频也加进去”→ 本文；说“拆镜”“反推分镜表”“写 MOTION 提示词”→ 文字复刻。拿不准时问一句：“是把视频直接喂给模型，还是把动作拆成文字写进词里？”
>
> **实测经过**：这条通道的首条完整实例（素材清单、帧数换算、拍点时码、零污染核验、风格兑现情况）见 [incidents.md](incidents.md) §2026-11-21「EP003 视频动作驱动首条实例」，耗时见同节后的「EP003 任务耗时（视频动作直投通道）」。本文只留现行规则。

## 1. 什么时候走这条

| 创作者要的是 | 走哪条 |
|---|---|
| 角色**照着一段真实视频的动作/节奏做**（手型精细：比心、托腮、拢衣领；舞蹈翻跳） | **本通道** |
| 动作能用文字写清（走位、对白、普通表演） | 文字编排，走 h3q 队列（`../SKILL.md`） |
| 只要锁同场连续镜头的构图、机位、色温 | h3q 的 `scene_video`（场景锚，不是动作驱动，音频不接） |

动作视频只当**动作源**。人物与画风永远来自已验收的身份板与视觉设定，参考视频里的人物、服装、水印不进成片。零污染要按 §7 的核法逐项过，不能靠目视一句「没看到」。

## 2. 本通道不走 h3q 队列

**这条通道没有标准入口，必须按本文手搓图直投。** MCP `h3_generate_video` 只有三种输入模式（`refs` / `first_frame` / `first_frame+last_frame`），没有视频动作参考；h3q 队列也没有；`scene_video` 是锁场景构图的场景锚（`H3ReferenceVideo`），不是动作驱动。让它看起来像"能走队列"是这一条最容易犯的误用。（`../SKILL.md` §0 已写明）。本通道直接向 Windows ComfyUI `127.0.0.1:8199` 提交 API 图。这是 h3-queue「三条硬纪律」第 1 条的明文例外，条件如下：

1. **提交前必须确认 GPU 空闲**：`h3qc queue` 无 running/waiting，且 `curl 127.0.0.1:8199/queue` 的 `queue_running`、`queue_pending` 都为空。有任务就停下汇报，不抢卡、不重启 ComfyUI。
2. 单次提交，不重试。提交响应不明时先查 `/history/<prompt_id>` 与 `/queue`，确认是否其实已在跑。
3. 创作者对 GPU 使用与耗时已有明确批准（本通道一条要跑一两个小时）。
4. 提交走一次性 runner（§5）。h3q 的幂等、显存预检、参考图闸门在这条路上都没有，所以门禁靠上面三条人工执行。G25 的长视频提醒属人工判读范畴，不是 h3q 兜底。

## 3. 图模板与占位符

模板：`../templates/video_motion_drive_graph.json`（`graph` 字段即可直接 POST `/prompt`）。

| 占位符 | 节点 | 填什么 |
|---|---|---|
| `{{PROMPT}}` | 5 `MiniMaxH3ReferenceToVideo.prompt` | 六段 Ref2VA 词稿全文（先过 `h3-video-gate`，见 §4），保留末尾换行 |
| `{{IDENTITY_IMAGE}}` | 20 `LoadImage.image` | 身份板文件名（在 Windows `ComfyUI\input\` 下，ASCII 文件名） |
| `{{ACTION_VIDEO}}` | 30 `LoadVideo.file` | 动作参考视频文件名（同在 `input\`） |
| `{{PREFIX}}` | 11 `SaveVideo.filename_prefix` | 产物前缀，实际落在 `output\video\` |

必须按任务改的数值：

| 字段 | 位置 | 规则 |
|---|---|---|
| `length` | 节点 5 | 帧数，必须 17k+5（345=17×20+5；243=17×14+5）。**取动作视频真实帧数换算后向上取最近的 17k+5**：向下取会截掉动作尾段；向上取多出的几帧靠动作自然收束补齐，不回放源片开头。换算实例见 [incidents.md](incidents.md) §2026-11-21「EP003 视频动作驱动首条实例」。时序对齐按 §4 的拍点秒数为准，不按帧号一一对应 |
| `width`/`height` | 节点 5 | 16G 卡实测 512×896 可跑 345 帧。更大分辨率先降帧数 |
| `noise_seed` | 节点 6 | 任意整数 |
| `ref_image_size` | 节点 5 | `match`。身份板是多视图拼板时脸可能偏弱，脸漂再改 `max` 或换单张正面图重投 |

固定接线（不要改）：

- 动作：`LoadVideo(30) → GetVideoComponents(31) → MiniMaxH3ReferenceToVideo(5).ref_videos.ref_video_0`，用 `31` 的输出槽 0（images）。
- **音轨参考**：`31` 的输出槽 **1**（audio）→ 节点 5 的 `ref_video_audios.ref_video_audio_0`。**是槽 1，不是槽 2。** 不接这个槽就是「只拿动作、声音让 H3 自己生成」。
- 动作修复：`UNETLoader(1)` 经 `LoraLoaderModelOnly(4)` 挂 `Motion_Repair_V2.safetensors`，强度 0.7，再进 `KSamplerAdvanced(6)`。
- 模型：`minimax_h3_ref2va_pruned_int8_convrot.safetensors`，20 步，`res_multistep` / `simple`，cfg 1.0。
- 负向槽（节点 3 `CLIPTextEncode`，text 留空）仅为满足采样器的 required 输入而**占位**；cfg 1.0 下没有负向分支，该段不参与采样（见 h3-video-gate G29）。不要往节点 3 里写 `low quality, blurry, distorted` 之类内容——在 cfg 1.0 下不会生效，只会制造"配了负向"的错觉。

## 4. 提交前

1. **动作视频不要裁剪或变速**，除非创作者点名。压短或放快之后，词里的时码与拍点全部对不上；改回原速是唯一干净的解（一次被否决的经过见 [incidents.md](incidents.md) §2026-11-21「EP003 视频动作驱动首条实例」）。
2. 词稿按 `h3-prompt-writing` 的 Ref2VA 写法，过 `h3_gate.py --mode ref --frames <length> --allow-long-video`，0 error（≤362f 时不带 flag 也应 0 error；>362f 时必带 flag，G25 降为 warn 仍不计 error）。长视频 warn 需在投递单记录理由；>362f 显存余量极小，先降分辨率再考虑升帧。
   `--mode ref` 是**六段官方 Ref2VA**（`subject_definitions` / `summary` / `retention_analysis` /
   `detailed_description` / `overall_soundscape` / `non_diegetic_music`），不是三段基础模式：
   写了 `integrated_multimodal_description` 会被 G03 拒，内容要并进 `detailed_description`。
   这条通道在六段之外还有三条硬格式，漏了必报 error：
   - `subject_definitions` 每条写成 `<Subject N> is … in <Picture k>`——**身份板在词稿里就是 `<Picture 1>`**
     （对应图模板节点 20 `LoadImage`）。只写「来自身份板」而不写 `<Picture k>` 会被 G30 判「没有可核对的参考来源」。
   - `summary` 开头写任务类型前缀 `[reference generation]`（G23）。
   - `retention_analysis` **每一行**都以 `<Subject N> (appears in [Shot N]): fully_preserved - …` 开头（G09）；
     想说明动作时序也挂在这条标签下，不要另起一句无标签的说明。
   `detailed_description` 在 `[Shot 1]` 之前要 1–2 句英文风格开场（G04）。
3. 清单里这一镜要 `technique: motion_drive`、绑定一个 `action_video` + 至少一个 `identity`，
   并给 `submit`（`workflow: motion_drive`、`width`、`height`、`refs_order`）——缺宽高报 `SUBMIT004`，
   缺 `refs_order` 报 `SUBMIT011`。`manifest_job.py` 会明确拒绝为这一镜建 job 并指回本文，
   这是有意的 fail closed，不是 bug。
4. **词的起点态必须等于身份板/首帧的状态**；参考视频里的动作拍点按时码写进词，每拍给秒数。七拍写满的一份词稿见 [incidents.md](incidents.md) §2026-11-21「EP003 视频动作驱动首条实例」。
5. **词里的手型要跟参考视频一致**。口径冲突时参考视频赢，词只管时序，别在词里和参考打架（词写 open palms、参考是握拳前推、成片跟了参考的实例见 [incidents.md](incidents.md) §2026-11-21「EP003 视频动作驱动首条实例」）。
6. 把外观污染写进排除：参考视频里的人物特征（猫耳、女仆装、金发、水印）逐项点名为不要。
7. 素材传到 Windows `input\`，传前后各核 SHA256。ComfyUI `LoadImage`/`LoadVideo` 对中文文件名会出问题，用 ASCII 名。

## 5. 一次性 runner 与后台投递

runner：`../templates/video_motion_drive_runner.py`。它提交一次、轮询 `/history`、按 SaveVideo 节点（`SAVE_NODE = "11"`）取回产物，并写 `status.json` 与 `.meta.json`（耗时、峰值显存、prompt_id）。

要点：

- **runner 必须脱离 SSH 会话**。挂在 SSH 上的 runner 会随子进程回收而退出，`status` 停在 submitted，产物不丢（ComfyUI 仍在跑），但回收只能改由 Mac 侧轮询。用 `../templates/launch_detached.ps1`（路径相对本文件所在的 `references/`；下同）启动（2026-11-22 实测：SSH 退出后进程继续运行到结束）：
  ```
  scp ../templates/launch_detached.ps1 ../templates/video_motion_drive_runner.py <渲染主机SSH别名>:/path/to/motion_drive_delivery/
  ssh <渲染主机SSH别名> 'powershell -NoProfile -ExecutionPolicy Bypass -File <ComfyUI根目录>\motion_drive_delivery\launch_detached.ps1 -Script <ComfyUI根目录>\motion_drive_delivery\video_motion_drive_runner.py -WorkDir <ComfyUI根目录>\motion_drive_delivery -Log <ComfyUI根目录>\motion_drive_delivery\runner.log'
  ```
  目录 `<ComfyUI根目录>\motion_drive_delivery\` 先建好，把填好占位符的图存成同目录 `graph.json`（runner 读 `GRAPH`）。回收时仍以 Mac 侧 SSH 查 `/history` 为准。
- **产物定位只认 `/history` 的 outputs 字段（subfolder + type=output）**，不能靠 `.mp4` 后缀猜：`LoadVideo` 会把输入视频也列进 images，旧 runner 栽过这个坑。
- 同一条不重试。超时先查 `/history` 和 `/queue`。
- 回收后本机 `ffprobe` 核对帧数、时长、分辨率、音轨。

## 6. 耗时与进度

- **耗时按非线性估**：帧数每多四成，墙钟就翻倍以上，别按线性外推。两次同通道任务的帧数与墙钟对照见 [incidents.md](incidents.md) §2026-11-21「EP003 任务耗时（视频动作直投通道）」。
- 一条跑一两个小时是常态（20 步、20GB 模型全程 offload），排期按这个量级报。
- **看进度**：ComfyUI 的采样进度条写在 `<渲染机根目录>\logs\serve.log`，读最后一行 `NN%|…| step/total [已用<剩余, N s/it]`。h3q 队列的 `progress` 字段不覆盖这条通道（它不经过 h3q），要自己读 serve.log。
- **判断是不是卡死**：看 serve.log 最后写入时间与 GPU 功耗（`nvidia-smi`，满载推理约 270W，卡死会掉）。CPU 主进程不动是正常的（GPU-bound）——只看 CPU 占用和日志停写会误判成卡死。

## 7. 验收

出片后由干净代理逐帧实测（`short-drama` 链路的验收执行者纪律），六项硬指标：

| 项 | 怎么测 |
|---|---|
| 身份 | 每 0.5s 抽帧与身份板对照，逐帧 MAD 无身份切换尖峰 |
| 动作时序 | 每拍点对照参考视频同秒的帧，列出实测出现秒数与手型差异 |
| 外观污染 | 全帧 OCR（tesseract psm 11 + 6）+ 水印 ROI 条带 + 目视，逐项核猫耳/服装/发色/字幕 |
| 音轨 | 采样数 = 帧数/24 × 采样率；`volumedetect`、`silencedetect`；包络自相关主频与参考比 |
| 完整性 | 零拷贝帧、黑帧、定格、断裂；MAD 最大值位置是动作起手而非切点 |
| 循环补完 | 每 0.25s 条带看半截动作有没有被补成完整循环（抬手后又放下） |

风格项单列，不并入硬指标：参考视频的颗粒、偏色、暗角这类质感，兑现与否要按成片实看，别假定模型会照搬。风格类问题回创作者拍板（接受 / 后期补 / 重出），别用统计反驳观感（一次只部分兑现的实测见 [incidents.md](incidents.md) §2026-11-21「EP003 视频动作驱动首条实例」）。

## 8. 已知边界

- 本通道产物 512×896，没有 pdd 的超分链。要交付分辨率走 `h3-queue` [§2.11 · latent-upscale](latent-upscale.md) 的 latent 放大（成品帧回编码，不重采样），放大前确认 GPU 空闲。
- 参考音轨是「参考节奏与质感」，不是 1:1 复制原声。要原声得外部混流。
- 单次提交就占满 16G 卡一两个小时，期间 h3q 里排的任务会 `occluded` 等卡。开跑前确认队列里没有更急的活。
- Windows 机器要在线。`ssh <渲染主机SSH别名>` 偶发解析失败，重试即可。
