# 视频动作驱动：让角色学参考视频里的动作（Ref2VA + 参考视频 + 参考音轨）

> 本文是这条通道的唯一权威。ask-media 路由表与 h3-queue 主文件只留指针。
> **“动作复刻 / motion”在中枢里有两个不同的东西，先分清：**
>
> | 用户的意思 | 是什么 | 在哪 |
> |---|---|---|
> | 把参考视频**当输入喂给模型**，让角色照着做（本文） | 视频动作驱动：参考视频 + 参考音轨进 `ref_videos` / `ref_video_audios` | 本文 |
> | 把参考视频的动作**拆成文字**，写成带时码的英文状态链 `MOTION-...` 再生成 | 文字复刻：`video-shot-reverse` 逆推 + `short-drama-video-prompts` 写 MOTION 词，走 h3q | `video-shot-reverse/SKILL.md`、`drama-skills/skills/short-drama-video-prompts/SKILL.md` |
>
> 判别：用户说“学这个动作”“照着做”“动作参考视频”“极乐净土那种”“音频也加进去”→ 本文；说“拆镜”“反推分镜表”“写 MOTION 提示词”→ 文字复刻。拿不准时问一句：“是把视频直接喂给模型，还是把动作拆成文字写进词里？”
>
> **实例（EP003）**：项目 `example-project`，成片与动作源在 NAS，与 EP001/EP002 同一层级：`~/Documents/NAS-MOUNT/example-project/EP003/`
>
> | 文件（NAS，相对 `EP003/`） | 内容 |
> |---|---|
> | `EP003-dance-345f-videoref-audio.mp4` | 成片，512×896 / 345f / 14.375s / AAC |
> | `EP003-dance-345f-x2.mp4` | 成片硬切重复两次，28.75s |
> | `动作源/source.mp4` | B 站 BV1Pz4h6wES5 原片（猫耳金发女仆，无台词，14.03s） |
> | `动作源/action_ref.mp4` | 传给 ComfyUI 的动作源（原速，720×1280 / 337f，带 AAC 原声） |
> | `文档/EP003_dance_videoref_audio.json` | 填好占位符的实际提交图 |
> | `文档/投递单-EP003-动作驱动.md`、`验收-EP003-动作驱动.md`、`视频提示词.md`、`EP003_ref2va_prompt_345f.txt`、`EP003-dance-345f-videoref-audio.meta.json` | 投递单、验收、词稿、送检件、运行记录 |
>
> 实证：2026-11-21 EP003「角色A学猫耳女仆卖萌动作」，345 帧 / 14.375s / 512×896，Windows ComfyUI 8199 一次成功，验收六项硬指标 PASS。

## 1. 什么时候走这条

| 创作者要的是 | 走哪条 |
|---|---|
| 角色**照着一段真实视频的动作/节奏做**（手型精细：比心、托腮、拢衣领；舞蹈翻跳） | **本通道** |
| 动作能用文字写清（走位、对白、普通表演） | 文字编排，走 h3q 队列（`h3-queue/SKILL.md`） |
| 只要锁同场连续镜头的构图、机位、色温 | h3q 的 `scene_video`（场景锚，不是动作驱动，音频不接） |

动作视频只当**动作源**。人物与画风永远来自已验收的身份板与视觉设定，参考视频里的人物、服装、水印不进成片（EP003 源视频是金发猫耳女仆，成片零污染，29 帧 OCR 与目视确认）。

## 2. 本通道不走 h3q 队列

**这条通道没有标准入口，必须按本文手搓图直投。** MCP `h3_generate_video` 只有三种输入模式（`refs` / `first_frame` / `first_frame+last_frame`），没有视频动作参考；h3q 队列也没有；`scene_video` 是锁场景构图的场景锚（`H3ReferenceVideo`），不是动作驱动。让它看起来像"能走队列"是这一条最容易犯的误用。（`h3-queue/SKILL.md` §0 已写明）。本通道直接向 Windows ComfyUI `127.0.0.1:8199` 提交 API 图。这是 h3-queue「三条硬纪律」第 1 条的明文例外，条件如下：

1. **提交前必须确认 GPU 空闲**：`h3qc queue` 无 running/waiting，且 `curl 127.0.0.1:8199/queue` 的 `queue_running`、`queue_pending` 都为空。有任务就停下汇报，不抢卡、不重启 ComfyUI。
2. 单次提交，不重试。提交响应不明时先查 `/history/<prompt_id>` 与 `/queue`，确认是否其实已在跑。
3. 创作者对 GPU 使用与耗时已有明确批准（本通道一条要跑一两个小时）。
4. 提交走一次性 runner（§5）。h3q 的幂等、显存预检、参考图闸门在这条路上都没有，所以门禁靠上面三条人工执行。G25 的长视频提醒属人工判读范畴，不是 h3q 兜底。

## 3. 图模板与占位符

模板：`~/.skills/hub/h3-queue/templates/video_motion_drive_graph.json`（`graph` 字段即可直接 POST `/prompt`）。

| 占位符 | 节点 | 填什么 |
|---|---|---|
| `{{PROMPT}}` | 5 `MiniMaxH3ReferenceToVideo.prompt` | 六段 Ref2VA 词稿全文（先过 `h3-video-gate`，见 §4），保留末尾换行 |
| `{{IDENTITY_IMAGE}}` | 20 `LoadImage.image` | 身份板文件名（在 Windows `ComfyUI\input\` 下，ASCII 文件名） |
| `{{ACTION_VIDEO}}` | 30 `LoadVideo.file` | 动作参考视频文件名（同在 `input\`） |
| `{{PREFIX}}` | 11 `SaveVideo.filename_prefix` | 产物前缀，实际落在 `output\video\` |

必须按任务改的数值：

| 字段 | 位置 | 规则 |
|---|---|---|
| `length` | 节点 5 | 帧数，必须 17k+5（345=17×20+5；243=17×14+5）。**取动作视频真实帧数换算后向下取最近的 17k+5**，EP003 的 337f 源片取 345 |
| `width`/`height` | 节点 5 | 16G 卡实测 512×896 可跑 345 帧（峰值 15.55GiB）。更大分辨率先降帧数 |
| `noise_seed` | 节点 6 | 任意整数 |
| `ref_image_size` | 节点 5 | `match`。身份板是多视图拼板时脸可能偏弱，脸漂再改 `max` 或换单张正面图重投 |

固定接线（不要改）：

- 动作：`LoadVideo(30) → GetVideoComponents(31) → MiniMaxH3ReferenceToVideo(5).ref_videos.ref_video_0`，用 `31` 的输出槽 0（images）。
- **音轨参考**：`31` 的输出槽 **1**（audio）→ 节点 5 的 `ref_video_audios.ref_video_audio_0`。**是槽 1，不是槽 2。** 不接这个槽就是「只拿动作、声音让 H3 自己生成」。
- 动作修复：`UNETLoader(1)` 经 `LoraLoaderModelOnly(4)` 挂 `Motion_Repair_V2.safetensors`，强度 0.7，再进 `KSamplerAdvanced(6)`。
- 模型：`minimax_h3_ref2va_pruned_int8_convrot.safetensors`，20 步，`res_multistep` / `simple`，cfg 1.0。

## 4. 提交前

1. **动作视频不要裁剪或变速**，除非创作者点名。EP003 压成 10s/1.4 倍速被否决，改回原速 14s。
2. 词稿按 `h3-prompt-writing` 的 Ref2VA 写法，过 `h3_gate.py --mode ref --frames <length> --allow-long-video`，0 error（≤362f 时不带 flag 也应 0 error；>362f 时必带 flag，G25 降为 warn 仍不计 error）。长视频 warn 需在投递单记录理由；>362f 显存余量极小，先降分辨率再考虑升帧。
3. **词的起点态必须等于身份板/首帧的状态**；参考视频里的动作拍点按时码写进词，每拍给秒数（EP003 的七拍：前伸 0.3s → 托腮 2.7–4.0s → 比心 5.2–6.4s → 垂手 → 再前伸 10.1s → 比划 11.3s → 拢领 12.5s → 合十 13.8s）。
4. **词里的手型要跟参考视频一致**。EP003 词写 open palms，参考是握拳前推，成片跟了参考。口径冲突时参考视频赢，词只管时序，别在词里和参考打架。
5. 把外观污染写进排除：参考视频里的人物特征（猫耳、女仆装、金发、水印）逐项点名为不要。
6. 素材传到 Windows `input\`，传前后各核 SHA256。ComfyUI `LoadImage`/`LoadVideo` 对中文文件名会出问题，用 ASCII 名。

## 5. 一次性 runner 与后台投递

runner：`~/.skills/hub/h3-queue/templates/video_motion_drive_runner.py`。它提交一次、轮询 `/history`、按 SaveVideo 节点（`SAVE_NODE = "11"`）取回产物，并写 `status.json` 与 `.meta.json`（耗时、峰值显存、prompt_id）。

要点：

- **runner 必须脱离 SSH 会话**。EP003 实测 runner 进程随 SSH 子进程回收而退出（`status` 停在 submitted），产物不丢（ComfyUI 仍在跑），但回收要改由 Mac 侧轮询。用 `../templates/launch_detached.ps1`（路径相对本文件所在的 `references/`；下同）启动（2026-11-22 实测：SSH 退出后进程继续运行到结束）：
  ```
  scp templates/launch_detached.ps1 templates/video_motion_drive_runner.py h3-win:E:/ComfyUI/motion_drive_delivery/
  ssh h3-win 'powershell -NoProfile -ExecutionPolicy Bypass -File E:\ComfyUI\motion_drive_delivery\launch_detached.ps1 -Script E:\ComfyUI\motion_drive_delivery\video_motion_drive_runner.py -WorkDir E:\ComfyUI\motion_drive_delivery -Log E:\ComfyUI\motion_drive_delivery\runner.log'
  ```
  目录 `E:\ComfyUI\motion_drive_delivery\` 先建好，把填好占位符的图存成同目录 `graph.json`（runner 读 `GRAPH`）。回收时仍以 Mac 侧 SSH 查 `/history` 为准。
- **产物定位只认 `/history` 的 outputs 字段（subfolder + type=output）**，不能靠 `.mp4` 后缀猜：`LoadVideo` 会把输入视频也列进 images，旧 runner 栽过这个坑。
- 同一条不重试。超时先查 `/history` 和 `/queue`。
- 回收后本机 `ffprobe` 核对帧数、时长、分辨率、音轨。

## 6. 耗时与进度

- 实测：345 帧 + 视频动作 + 音频参考 + Motion_Repair，**7000 秒（116.7 分钟）**，峰值显存 15.55GiB，20GB 模型全程 offload，**采样 20 步，每步约 5m42s**。
- 之前 243 帧单视频参考那次 3323 秒。**帧数每多 42%，耗时翻倍以上**，预估别按线性算。
- **看进度**：ComfyUI 的采样进度条写在 `E:\H3-Studio\logs\serve.log`，读最后一行 `NN%|…| step/total [已用<剩余, N s/it]`。h3q 队列的 `progress` 字段不覆盖这条通道（它不经过 h3q），要自己读 serve.log。
- **判断是不是卡死**：看 serve.log 最后写入时间与 GPU 功耗（`nvidia-smi`，满载推理约 270W，卡死会掉）。CPU 主进程不动是正常的（GPU-bound）。EP003 当时因为只看 CPU 与日志停写，两度怀疑卡死，其实一直在算。

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

风格项单列，不并入硬指标：EP003 的 DV 重颗粒/灰绿偏色/暗角只部分兑现，成片偏干净暖调写真。风格类问题回创作者拍板（接受 / 后期补 / 重出），别用统计反驳观感。

## 8. 已知边界

- 本通道产物 512×896，没有 pdd 的超分链。要交付分辨率走 `h3-queue` §2.11 的 latent 放大（成品帧回编码，不重采样），放大前确认 GPU 空闲。
- 参考音轨是「参考节奏与质感」，不是 1:1 复制原声。要原声得外部混流。
- 单次提交就占满 16G 卡一两个小时，期间 h3q 里排的任务会 `occluded` 等卡。开跑前确认队列里没有更急的活。
- Windows 机器要在线。`ssh h3-win` 偶发 mDNS 解析失败，重试即可。
