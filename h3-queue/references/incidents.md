# 事故与排障经过（按日期）

> 本文只收事故经过与本轮排查记录；现行规则由 SKILL.md 与各 references 持有，正文不重复这些经过。
> 每条写清日期 / 条件 / 症状 / 数字 / 结论。数值按当时实测保留，不代表现行档位口径。

## 2026-10-20｜多会话直连 ComfyUI 互相 OOM 阻断

- 条件：这张 16 GB 卡，H3 常驻约 14 GB；多个会话各自直连 ComfyUI 提交。
- 症状：后到任务多要一点显存就 OOM，CUDA context 变 sticky（连 `cuMemGetInfo` 自己都报错），实例挂掉，所有会话一起停摆；客户端超时后又重提交，一次偶发 OOM 被放大成"互相阻断"。
- 数字：`serve.log` 里 **505 行** `CUDA error: out of memory`、**578 个** Traceback；空闲时显存仍占 **14.1/16.3 GB**。
- 结论：必须走单一 FIFO 队列做准入控制，幂等去重 + 提交立即返回 job id；不要靠客户端等待或直连。

## 2026-11-21｜smart-memory 导致空闲仍占 14 GB（已修复）

- 条件：ComfyUI 的 smart-memory 默认把模型留在显存里等下个任务，启动参数没有 `--disable-smart-memory`，H3 权重约 14 GB 常驻。
- 症状：队列原先只在 preflight 请求 `/free`（开跑前），任务结束路径没有释放动作，跑完就僵在那儿，直到下个任务 preflight 才可能被清。
- 数字：`/free` 实测 **5 秒内从 13.9 GB 回落到 462 MB**。
- 结论：`run_one()` 在 `set_state(done/failed)` 之后统一调 `release_vram()`（`/free` = `unload_models` + `free_memory`），成功失败都释放；日志留 `release_vram: models unloaded after job <jid>`。

## 2026-11-21｜准入阈值 2.0/1.5 → 4.0/3.0

- 条件：原 `H3Q_MIN_FREE_GB`/`H3Q_FLOOR_GB` = 2.0/1.5。
- 症状：1.5 GB 的底线等于允许在只剩一两个 G 的卡上开跑——队列看着「明明没显存了还照样丢进去」。
- 数字：H3 峰值约 15 GB；赌输就是 OOM + sticky context（见本文件 §2026-10-20）。
- 结论：提到 4.0/3.0。低于 `MIN_FREE` 先请求 `/free`，回收后仍低于 `FLOOR` 才停靠。

## 2026-11-15｜multishot 渲染器切 v2 节点映射（CORE 版已备份）

- 条件：操作者指令「去掉 CORE 全部替换」，`multishot_render_ref.py` 从 CORE 节点改为 V2 节点。
- 改动：节点映射 sampler **8 → 30**、save **11 → 27**、**12 → 28**；原 CORE 版备份为 `.bak-core-20261115`。
- 兼容：`h3q.py` 的 multishot 分支参数不变、完全兼容，无需同步改调用侧。
- 现用模板 `<渲染机根目录>\config\multishot-v2.json`（MemorySampler node30 / SaveVideo node27 / SaveAudio node28）；`multishot-core.json` 保留为历史。
- 结论：V2 取代 CORE 后，节点号不再是 8/11/12；引用旧节点号的脚本或模板需按上表换算。

## 2026-11-19/20｜EP005 002 双窗判废（"同机位"不是用多窗的理由）

- 条件：EP005 002 走 multishot 双窗。
- 症状与数字：出片 **26 分钟**，盘里摆着冰棍、练习册提前摊开，判废。
- 结论：改成单镜拆成 002a（关门+两句独白）+ 002b（大肥鱼入场）后，002a 接缝与台词一次通过。"同机位"本身不是用多窗的理由；同机位但能拆就拆。
- 另见 §2026-11-19/20 EP005 S-002 场景锚失败。

## 2026-11-19/20｜EP004 006+007 词层缝（两轮三个根因）

- 条件：EP004 末段 006+007 多窗，画面接缝做到几乎逐帧一致，创作者仍连续两轮判"还有硬切"。
- 症状与根因：
  - 第一轮"抱起来那一下"＝**妈妈入场被压缩**：入场与落位被写成一拍，模型画出"已经弯腰在那"的中途姿态，无入场过渡帧（镜内相位断）。
  - 第二轮"瞬间开哭"＝**情绪跳档**：窗 1 结尾委屈含泪 → 窗 2 开头 **0.7 s** 内张嘴大哭。
  - 同一条片两个硬切、两个不同根因，都修在词层、不在容器。
- 结论：判型顺序见 `../../h3-prompt-writing/references/failure-modes.md` 与 `../../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md`；多窗管不了词层的相位断。

## 2026-11-08｜9 张参考图 OOM 调查日记

- 条件：pdd_render_ref.py 渲染器路径，draft 1024×576 与 final 1536×864 两档，参考图 2/3/5/6/9 张。
- 数字（峰值显存 / 墙钟）：
  | refs | draft 1024×576 | final 1536×864 |
  |---|---|---|
  | 2 | 15.14 GiB / 285.8 s | 15.55 GiB / 831.2 s |
  | 3 | 15.14 GiB / 290.6 s | 未测 |
  | 5 | 15.15 GiB / 310.6 s | 未测 |
  | 6 | 未测 | 15.53 GiB / 882.4 s |
  | 9 | 15.14 GiB / 340.6 s | ❌ 失败于 node 304 `SamplerCustomAdvanced`，605.9 s |
- 症状：9 张那次 OOM 报错正文 `torch.OutOfMemoryError: Allocation on device 0 would exceed allowed memory`，`Currently allocated : 901.46 MiB`、`Requested : 50.93 MiB`、`Device limit : 15.92 GiB`、`Free (according to CUDA): 0 bytes`，摘要写 `CUDA OOMs: 0`。PyTorch 自己只占 901 MiB、只申请 50.93 MiB，CUDA 却报可用 0 字节——不是"任务用光 16GB"，而是设备被别的东西占满 / CUDA context sticky 的形态。同时段 `h3q health` 报 `external work running=1`。
- 排查推翻过程：
  - 一开始把 `external work running=1` 当成"别人干扰"的证据；后来确认该字段直接取 ComfyUI `/queue` 的 running 数，h3q 自己派发的任务也计入，**不构成证据**。
  - `comfy up for <N>s` 是 `now() - comfy_last_ok`（距上次健康探测成功），**不是进程运行时长**；`up for 0s` 不代表刚重启。判断有没有别人占卡只能 `nvidia-smi --query-compute-apps=pid,used_memory` 看 PID 归属，再对 `h3qc queue` 做差。
  - **6 张二采是判据**：15.53 GiB 比 2 张的 15.55 GiB 还低，峰值由二采主序列（138,672 token）决定，参考图 token 挤不进影响因素。9 张失败与张数无关；两种解释（sticky context / 瞬时分配）当时都未排除。
- 结论：final 档挂多张安全，**6 张已实测成功、2 张与 6 张已验证**；显存峰值与张数无关，时间每张约 **+13 秒**（final；draft 每张约 +8 秒，2→9 张 285.8→340.6 s）。9 张那次属瞬时分配失败，重跑即可，不要退回 2 张。验构图（draft）最多 9 张，pdd_render_ref 动态扩容；本仓 mkdraft.py 离线副本仅 2 槽（`--ref0/--ref1`），不适用。
- 顺带修掉的缺陷：改前 refs 数**少于**模板槽数时，多出来的槽仍接着模板自带图，模型会当额外的 `<Picture N>` 吃进去（现按 refs 裁剪）。回归核对：2 张路径改前改后逐字节一致。
- 实测记录存内部工程档案（未随公开版发布）。

## 2026-11-07｜Sol 加速档实测（一律不要开）

- 条件：pdd 8 步，1024×576，EP002 第 006 镜，同素材同 seed 777001 同 362 帧。
- 数字与症状：
  | 组合 | 墙钟 | 窄缝成立 |
  |---|---|---|
  | 旧 lu2 draft（896×512 4 步） | ~120 s | ❌ 标准车位 |
  | pdd 8 步 Sol off（1024×576） | 285.8 s | ✅ 成立 |
  | pdd + 二采 1536×864 | 832.3 s | ✅ 成立 |
  | lu2 legacy 20 步（1344×768） | ~1440 s | ❌ 机位更乱 |
- Sol 档：`sol_scheduled` 比 off **慢 3.5%** 且构图跑掉；`sol_int8qkpv` 快 **22.8%** 但同样跑掉。稀疏注意力跳过部分 token，丢掉的是空间线索。`H3FrontLoadedSigmas`（−24% 步数）也不能配 PDD：beta57 步点只有 2/40 落在 PDD 训练网格上，被 `on_off_grid=error` 拦下。
- 结论：`pdd_render_ref.py` / `lu_render_ref.py` 的 `--sol-profile` 默认已改为 `off`（2026-11-07）。

## 2026-11-15｜H3-Image 参考图边界（7 例对照）

- 条件：H3-Image W4A8 与社区量化 Q4_K_M，7 素材 × 忠实重绘 / 只改冷光。
- 症状与数字：W4A8 `--refs` 全批通过；Q4_K_M 在 **1152×768** 带参考图时卡死（GPU 100%、显存占满、渲染器 **903 s** 超时），已从脚本移除，不再作为可选档。
- 忠实度结论：参考图编辑维度 **Qwen 2.1 比 H3 W4A8 更忠实**（7 例里 6 例结构保真更高），H3 W4A8 改光时常连主体、机位一起重绘并顺手抬曝光；纯文生复杂规格仍 H3 更强。两者按任务类型分开选。
- 实测记录存内部工程档案（未随公开版发布）。

## 2026-11-08 前｜sips -Z 重编码首尾帧缺陷（已修）

- 条件：旧代码上传 `first_frame` / `last_frame` 参考时用 `sips -Z 1344` 缩放，MCP 旧版还把首帧压成 JPEG q80。
- 症状与数字：`-Z` 会放大也会缩小——**1536×864** 的真实末帧被缩到 **1344**（模型得自己补回 **192 px** 宽度）、**896×512** 场景板被拉成 **1344×768**。末帧接力交出去的已不是创作者验收过的像素。
- 结论：`first_frame` / `last_frame` 与"起始/首帧/构图/状态"参考一律原生尺寸 PNG、绝不重编码；只在长边超过 `H3Q_REF_LONG_EDGE`（默认 2048）时才缩。MCP 的 JPEG q80 与 sips 缺陷均已修。

## 2026-11-22｜首尾帧输入 MAD 对照（pdd_lu vs 默认分支）

- 条件：同一对首尾帧、同 107f、同 seed（42）。
- 数字：pdd_lu 产物首帧与指定首帧 MAD **43.0**，非 pdd 默认分支 `h3_render_ref.py` **3.86**。
- 结论：`pdd_lu` 的 `pdd_render_ref.py` 没有 `--first-frame`/`--last-frame`；首帧/首尾帧一律走默认分支（i2va / fl2va），转场卡直接用 `../scripts/transcard.py`。项目内还需两端帧先过参考准入（`ref_gate` 会回 `reference_not_accepted`）。

## 2026-11-22｜转场卡中段能力边界实测

- 条件：EP002 SHOT-03 f120→f226 的真实中间段当 ground truth，逐帧比生成的 107 帧。
- 数字：中段 MAD 中位 **23.9**，全片 22–27 之间平坦地高，不单调从 A 走向 B，中间切到一个新状态。身份、发型、服装、巷子、光位都对；表情与说话人不对（原片 S1 笑着说话、S2 静听，生成的 C 里 S1 转头朝镜、S2 张嘴）。
- 结论：转场卡保两端 + 中段身份与空间，不保中段的表情、说话人分配和动作路径。要这几样就把 A→B 的动作拆进一次生成（multishot 或单镜加长）。

## 2026-11-04｜tile 镜像伪影与 `--tile-size` 历史 bug

- 条件：二采空间分块，512 px tile（1344×768 → 3×2）。
- 症状与数字：每 tile 主体按 conditioning 各自重绘，左右 tile 画出同款舞者/对称人群（镜像伪影），成片判废；tile 版更慢（**717 s vs 整帧 385 s**）。
- 历史 bug（已修）：`h3qc.py` 的 `--tile-size` 默认曾是 **512**，而 `h3q.py` lu2 分支只要参数存在就无条件透传，于是"默认档"实际把空间分块打开了，`lu_render_ref.py` 自己的 0 默认被覆盖。**任何在 2026-11-04 之前不带显式 `--tile-size 0` 跑的 final，都要复检有无镜像伪影。**
- 结论：空间分块必须关（`--tile-size 0`，2026-11-04 起客户端默认已是 0）；破 ~300 帧上限靠时间分块就够。

## 2026-11-04｜L01B→L02 红裙接缝（第一遍 latent 的 take 差别）

- 条件：多段短片接续，第 N+1 段的 `--first-frame` 取第 N 段末帧（`ffmpeg -sseof -0.06 -i <N段>.mp4 -frames:v 1`），不能用分镜关键帧顶替。
- 症状：`L01B`（终点＝红裙糊满全屏）→ `L02`：用 `SHOT-EP001-004.png`（已是红裙扫开、中堂可见）作首帧时，接缝从"红裙糊满"直接跳到"红裙在左+小二清晰"，肉眼可见；改用 `L01B` 末帧后变成"红裙糊满→同色调→+0.5s 扫开露出大厅"，转场自然。
- 结论：第 N+1 段首帧取第 N 段末帧；分镜关键帧描绘的是该段某个中间状态，不是上一段终点。

## 2026-10-30｜角色C EP01 长镜重建（事件密度，不是时长）

- 条件：13.667 s 的「静→动」单镜（角色C）。
- 症状与数字：8.5 s 之后模型开始重建角色（同一角色出两份）并吞掉升高、后拉指令；压到 **10.125 s** 并补人数与连续体声明后成立。同一批把两处相邻同事件镜合并（8 s / 10.125 s），8 镜降 6 镜、切点 7 降 5、台词一条没删，观感立刻连起来。
- 结论：判据是**事件密度**不是时长：去掉切口观众还看得清后果就合并；静→动、人数变化、指令堆叠的镜头优先压到 10 s 附近。

## 2026-11-19｜EP004 v5 窗口以 `[` 开头"白烧"

- 条件：`H3MultishotMemorySampler` 用 `text.startswith("[")` 判定整份脚本是不是 JSON 数组。
- 症状与数字：以 `[Shot 1] ...` 开头的窗口被当成坏 JSON，自动修复失败后抛 `H3 script looks like JSON but does not parse`；EP004 v5 006/007 **9.6 秒**后 node 30 `execution_error`，脚本内容本身完全正确，等于白烧。
- 结论：窗口正文不要以 `[` 或 `{` 开头，直接从场景/人物写起。2026-11-19 起三层拦截：① `h3_gate.py --mode multishot`（G39 查窗口数/窗口开头/单镜段名混入，G40 逐窗查 `<d>` 格式、`<d>` 外中文、每窗 15 s 上限）；② adapter `verify_multishot_script` 在 SSH/上传前拒绝；③ MCP `_verify_multishot_script` 在建临时文件前拒绝。多窗不再"整块豁免结构项"。

## 2026-11-19｜EP005 S-002 场景锚失败（scene_video）

- 条件：同场连续任务，场景图塞进 `refs`。
- 症状：只用文字描述场景时整间房被重画成远景；记忆采样器把 `reference_images` 每张图声明成「`<Subject N>` 的照片」，场景图占掉一个人物名额并把画面拉向人脸。
- 结论：场景锚首选 `scene_video`（上一镜已验收成片片段，走 `reference_video`），不要再把场景图塞进 `refs`。参数：`scene_video_start` 默认 8.5 s、`scene_video_seconds` 默认 3.0 s（2–4 s 足够）。与 `scene_anchor_index` 二选一，同给直接拒绝。

## 2026-11-15｜SeedVR2 本机实测 FAIL

- 条件：EP003 008b 5 s 静态特写，SeedVR2 3B fp8（§2.10 B 路径）。
- 症状与数字：过锐化（绒面织纹成规则网纹、硬亮边、皮肤蜡质、指甲白点伪高光、左缘偏色、水枪振铃）；时序与人物道具虽 PASS，但降回源尺寸仍 **×1.807 锐度**＝重绘加锐。`--prepend_frames 4` 使输出多 4 帧、头部平移、**5.0→5.167 s** 且无音轨，直接进剪辑会音画/接缝错位；**0.11 fps**（5 s 片段 ≈19 min）。
- 结论：SeedVR2 仍 FAIL，**不为存量铺开**；交付超分只有 latent 放大可用。

## 2026-11-15｜R2 生成层实测（完整播放验收 = REVISE）

- 条件：全修订正文（时间线写满 9.417 s、两窗无定格句）重出的 `MS001-重出-v1.mp4`。
- 数字与症状：
  - `silencedetect=-38dB:d=0.6` 在 15.497–18.768 留 **3.271 s** 尾段静默（旧素材 **3.362 s**，仅 −0.091 s），总量 7.299 s / 5 段。
  - 完整播放 + **50 张** ≤0.4 s 抓帧 + 尾部 f360–f450 逐帧 MAD（min 0.1522 / mean 1.3665 / max 2.8909，低于 0.05 的帧 **0/90**）证明画面层持续微动作、不是定格。
  - 声音层根因（只读复核）：`H3MultishotSampler` 生成的音频在 **15.30→15.60 s** 平滑收束（−16.16 → −68.11 dBFS，每 20 ms 降 2–5 dB）后进入 **−64~−66 dBFS** 近静音稳态（非零采样约 98%、峰值 ≤−52 dBFS、音轨全长 18.768344 s / 600587 采样帧完整），属生成层模型行为，与转码/装配削掉无关；15.497 只是 −38 dB 阈值穿越点，旧素材跨 take 同形态复现。
  - 切点 f225↔f226 灰度 MAD **4.422**、RGB 均值台阶 −2.28/−1.76/−1.23，是模型内部接缝一次局部重绘 + 窗2 曝光微差（人物左上 9.4/8.2 vs 背景 1.8–4.5，伴刘海/眉/眼斑高光/糖支倾角重绘，量级 <1% 满幅，f227–f242 稳定新水平）；**不是** R10 的逐段 GRADE 台阶（全帧均匀、单帧 −11.938 / YAVG step +12.484）。全局归一只能近似拉回整体亮度，消除不了局部重绘。判 PASS 另记 minor **REV-002**。
  - REV-001 对口修复是**后期合成超市 hum（需创作者授权 DSP）**，不是 `self_anchor_voice`：workflow 里 `seed_per_shot=true` / `self_anchor_voice=true` 已由 renderer `set_controls` 覆写到位，两开关只钉声线、不保证环境床连续，关掉还会引入已实测音色漂移；`voice_ref` 未接（R9 三处断点另案）。prompt 本轮无需再改（job.prompt 与现用脚本 strip 后逐字相等 4812 字符）。
  - 另四个多窗正文是 **4 文件 8 窗**，其中只有 `ms_001_002a.txt` 两窗全修订，`ms_005_006` / `ms_007_008a` / `ms_009_010` 共 6 窗结尾仍留 `camera unchanged` + `The window ends on this … arrangement` 静态收束句。现用成片的静默达标由装配脚本 CRUSH 裁切达成，生成层 4 段素材最长单处 **4/4 全不达标**；该次验收里「10.72 / 1.28」两个判据阈值的完整口径当时未留记录（UNVERIFIED），本文不补编，后续复测需重新标定。
  - 独立 reviewer 六项：look_technical / identity_costume / hand_limb_contact / action_spatial_continuity PASS，dialogue_lip_sync / audio_voice UNVERIFIED（无实听通道）。内部验收记录 §76 引的 §2.11 `CreateVideo(audio=VHS 音轨)` 是 latent 放大链，本片实际是 `CreateVideo(10).audio=["8",1]`，引用以 delivery-specs.md 为准。
- 结论：定格句与时间线写满**在画面层生效**；尾段静默是**生成层模型行为**，修复走后期合成，不是改提示词或 `self_anchor_voice`。
- 来源：`delivery-specs.md` R2 段（详细经过迁此）。

## 2026-11-19｜EP003 multishot 接缝定量

- 条件：EP003 001+002a，2×226f → 451f / 18.792 s / 768×448。
- 数字：内部接缝 PSNR **31.9 dB**；同一对镜头逐段生成再拼为 **23.4 dB**（肉眼可见人物放大约 6%、妈妈背影变宽）。总帧公式：总帧 = 每窗帧数 × 窗数 −（窗数−1），226×2−1 = 451。
- 结论：同机位连续段优先 multishot 内部接缝；总帧公式定义见 `multishot-capacity.md`。

## 2026-11-19｜EP003 005+006 音色跨窗

- 条件：`H3MultishotSampler` 两个开关。
- 数字：`seed_per_shot=True` 保持时脸和声音跨窗稳定；曾设 False 后第二窗音色明显变调（F0 **291 → 364 Hz**）。`self_anchor_voice=True` 实测两窗角色C F0 **340 / 327 Hz**（差 0.7 个半音）。
- 结论：`seed_per_shot` 必须保持 True；第一窗安排一句干净独白供 `self_anchor_voice` 钉声线。

## 2026-11-19｜EP004 v5 006/007 auto_chunk_ffn 慢渲染

- 条件：294f×2 @1344×768，权重 10.9GB + 激活池 2.3GB = 13.2GB，仅这两项并未超过 14.4GB 可用；加上运行时其余常驻占用（CUDA context、VAE、KV / FFN 临时缓冲，具体分项以实际部署为准）后越线。
- 症状与数字：触发 `loaded partially; 2067 MB offloaded`，**626 秒/步**（正常 6 秒），8 步 **83 分钟**；`H3AutoReserve` 警告「这不是慢渲染，通常会在 CUDA kernel 里死掉并带走服务端」。
- 结论：`auto_chunk_ffn` 默认 on，权重装不下时用 sol-attn 的 `MiniMaxH3ChunkFeedForward` 把 FFN 分块（chunks=2），让 DiT 保持驻留而不是每步从内存流式加载。路径：`h3qc --auto-chunk-ffn on|off` → `params.auto_chunk_ffn` → h3q 白名单 → `multishot_render_ref.py --auto-chunk-ffn` → node 30；缺 sol-attn 时节点打印 `skipped` 并照常跑。慢的根因不是参考图（只占几 MB）：权重 10.9GB + 激活池 2.3GB 才是大头；提速只有三条：①`auto_chunk_ffn` 驻留；②降 `frames_per_shot`（294→226→141）；③降画布。

## 2026-11-21｜context_pin 在 0.45.3 实测通过；容器缝与词层缝分开

- 条件：EP002 冒烟 job `job-EXAMPLE`，双窗 362f / 576×992 / 带音频，ComfyUI 0.45.3。
- 症状与数字：MC 未激活状态下全链出片、无 MC-missing / shape-mismatch 报错、容器缝 f169→f170 连续。边界：容器只消容器缝；同片窗 2 内 f191→192 凭空入场、f209→210 景别跳都是词层问题，容器救不了。
- 结论：`context_pin` 把上一段尾部 **22 帧 raw latent** 钉进下一段内部关键帧坐标（bit-identical、无 VAE 往返）；接缝处重生成约 **0.92 s** 在解码时剪掉。`context_pin` 是采样器内建能力，**不依赖 ComfyUI-H3-Motion-Context 激活**——0.45.3 实测 MC 未激活状态下全链出片，见 §2026-11-21。多窗的连续性不止尾帧，只有 `first_frame` 那一种走尾帧。词层判型走 `seam-transition` §0.1 第 0 步、`failure-modes` 对应行。

## 2026-11-13｜续接两分支混用实测

- 条件：EP003 001→002a（Ref2VA 末槽）与 002a（纯 I2VA 混入 Ref2VA 式提示词）。
- 症状与数字：Ref2VA 末槽首帧与上段末帧构图、身份、道具数量一致，剪硬切无缝感；纯 I2VA `seam-transition.md` 第七组实测帧差 **3.38**（条件：整段不带任何参考图、正文按首帧三段结构写）。混入 `<Picture N>` 定义与对齐首行后，2026-11-13 EP003 002a 实测首帧不生效（角色、服装、画风全部更换，与所给首帧无关）。
- 结论：两条路要配各自提示词；Ref2VA 是唯一同时拿到身份 + 起点的路，纯 I2VA 更准但要求不带参考图。`--first-frame` 与 `--refs` 互斥，代码直接报错。

## 2026-11-13｜长镜末段回灌参考图

- 条件：12.958 s 双人镜（身份板三视图 + 场景板 + 构图参考），EP003 010。
- 症状：后段把画面切成灰底三视角角色板，等于把参考图直接渲进成片。
- 结论：正文结尾补一句「同一花园取景保持到最后一帧：脚下草地、身后木栅栏与黄花、上方蓝天、影子朝右」后重出，回灌消失。长镜（≥10 s）且挂角色三视图时，结尾要显式锁场景与机位，别让「两人并排微笑」成为正文最后一句。

## 2026-11-05｜出图实测时点（CFG 3.5 / 无 LoRA / 40 或 45 步）

- 权威：`still-standard-tier-20261105.md:7`（本文件不复述数字，仅登记事故对照用）。
- 结论：Qwen Image 2.1 在该日快照为 CFG 3.5、无 LoRA、`steps=0` 按是否带参考选 40/45 步；现役档位以实现实读为准（`h3qc submit --help` / MCP schema / `H3Q_IMAGE_*` 覆盖键）。

## 2026-11-15｜档位对齐与版本口径（背景）

- CFG 负向机制权威：`still-api-params.md:7-9`「术语与分层」（全仓只定义一次）。
- PDD 竖屏支持：见 `tiers-and-capabilities.md` 竖屏段；draft 首采 **576×992**、final 二采 **832×1440**，896×1536 面积超 1536×864 上限被拒。竖屏 draft 与 final 首采不是同一画布（832×1440 → 544×960，宽高比差约 2%），draft 只验表演不验构图。
- 版本口径：同一部署可能出现多个版本号；判断只看 `comfyui_version.py` / `pyproject.toml` 实际值，`git describe` 与提交号不作依据，特性以 `/object_info` 节点是否注册为准。

## 2026-11-06｜HyperFlow H3 Flash 三条硬理由（不装）

- 条件：Video Rebirth 的第三方压缩版 H3 Flash，13.7B（原版 31B 不到一半），4/6/8 步、无 CFG、音画同出（32 kHz 立体声）、最多 9 图；独立权重，不是 PDD 开关也不是 LoRA。
- 显存表来源 = 第三方压缩模型仓库 Video-Rebirth/hyperflow-h3-flash 的 `<上游仓>/integrations/README.md`（上游仓路径，未随本仓发布；**非 MiniMax 官方上游**；引用时点 2026-11-06，1344×768、6 步、2 张参考图口径，GGUF Q4_K_M，该表未细分 INT8 档）：RTX 4090 (24G) 22 GiB / 180 s（5.2 s）、866 s（15 s）；RTX 5090 (32G) 30 GiB / 139 s、663 s；**RTX 5070 Ti (16G) 该表明写 "16 GB GPUs are not measured yet"**。以上为本仓引用时点记录值，上游现行表可能已更新，以引用时点为准。
- 本机不成立的三条硬理由：
  1. **显存**：峰值要 22 GiB，本机上限 15.92 GiB；现役 PDD 跑 1536×864 已到 15.55 GiB，只剩 0.37 GiB。换 `Q3_K_M` 只省 1.9 GB，而峰值里权重约 9 GB、余下 13 GB 是激活值与 VAE，填不上 6 GiB 缺口。
  2. **没有速度收益**：24G 卡出 15 s 要 866 s，比现役 PDD 的 831 s 还慢；16G 只会更慢或 OOM。
  3. **改动面大**：要 ComfyUI ≥ 0.43.0（版本与运行实例提交号现场核对，以实际部署为准）、装 `ComfyUI-GGUF` + `ComfyUI-HyperFlow-Flash`、专属 `HyperFlow GGUF Loader`、整套工作流重写；下载约 35 GB（两个 GGUF + 15.7 GB 文本编码器 + VAE）。`<渲染机根目录>` 不是 git 仓库，升级 ComfyUI 后 PDD / LatentUpscaler3D / Sol 那套改动都要重验。
- 结论：**别装**。再看条件：官方补 16 GB 实测数据，或出现 16 GB 可跑的精简版；届时唯一看点是**音画同出**，不是速度。
- 来源：[GitHub](https://github.com/Video-Rebirth/hyperflow-h3-flash) · [HF 权重](https://huggingface.co/VideoRebirthAI/hyperflow-h3-flash) · [ComfyUI 节点](https://github.com/Video-Rebirth/ComfyUI-HyperFlow-Flash)

## 2026-11-22｜idem-key 不带 seed/输出名（12 次提交只渲出 4 张）

- 条件：4 档提示词 × 3 seed，key 只写了档名。
- 症状与数字：**12 次提交只渲出 4 张**，其余 8 次被幂等去重；`--wait` 对去重后的旧 job 照样返回 done、`rc=0`，客户端看着全成功（`h3qc.py ls` 里只有 4 条记录）。
- 结论：key 里必须带上 seed／输出名；提交成功 ≠ 产物存在，交付前逐张校验文件存在且非空。

## 2026-11-12｜latent 放大首个实测（旧画幅，已修正）

- 条件：MCP `h3_upscale_video`，451f / 768×448 → 1536×896。
- 数字：**165.1 s**，GPU 峰值约 **6.8 GB**；同批两版成片保真 PSNR 30.11（CORE）/ 30.21（V2）dB，SSIM-luma 均 0.9923，锐度 2.10×/2.08×，接缝最大比 1.80/1.74。
- 结论：这是修正前旧值——1536×896 强拉 16:9 会变形，交付须用 `aspect="16:9"` 得 1536×864（见 `delivery-specs.md` P0）；耗时仅代表该次测量。

## 2026-11-15｜R1 画幅 A/B 实测（圆帽变形数字）

- 条件：两档交付规格真实渲染 4 产物；同尺寸 A/B 比 lap_var。
- 数字：4 产物全部 1024×576 / 1536×864、无黑边。固定 1024 档同尺寸 A/B 净 **−20.51%** lap_var（源 130.451 → 纯缩放往返 112.702 → latent 放大缩回 103.697），收益被输出层吃掉并转负；1536 档同尺寸 A/B 源版纯上采样 41.383 vs latent 放大版 54.301（**+31.22%**），只有同步 `CONCAT_OUT_SIZE=1536x864` 才保留。
- 圆帽变形：1536×896 强拉 1536×864 使圆帽 w/h ×1.0367 / h ×0.9649（变形），`increase+crop` 只裁上下各 **16 px**、w/h ×0.996~0.999（保形）。
- 结论：`server.py` 的 `aspect` 逻辑与 schema 离线 8 例 PASS、`py_compile` PASS；实出一张需 MCP 长驻服务重启后参数才可见。P0 规则（1536×896 强拉变形、用 1536×864）在 `delivery-specs.md` P0 持有。

## 2026-11-20｜PDD 草稿分辨率决定构图（不是 seed）

- 条件：同 seed **1017**、同参考图，pass1 分别用 `896×512` / `1024×576` / `1344×768`。
- 数字与症状：三档画面内容不同——`896×512` 无山 / `1024×576` 云海偏左 / `1344×768` 远山清晰。构图由 pass1 分辨率决定，不由 seed 决定。
- 结论：草稿用别的分辨率，看到的画面就不是成片的画面；pass1→超分→pass2 链路里草稿批准的那一帧就是成片那一帧。竖屏 MCP 的 draft/final 是两次完整采样、首采画布不同，不适用该结论（见 `tiers-and-capabilities.md` 竖屏段）。链路实测：1536×864 / 243 帧 / 24 fps / 10.125 s，446.6 s，峰值约 15.1 GiB，文件 9.56 MB；单段 1344×768 硬跑 385.8 s 但构图不同。

## 2026-11-21｜EP003 任务耗时（视频动作直投通道）

- 条件：345 帧 + 视频动作 + 音频参考 + Motion_Repair，512×896，Windows ComfyUI 8199 直投（不经 h3q），20 步。
- 数字：**7000 秒（116.7 分钟）**，峰值显存 15.55 GiB，20 GB 模型全程 offload，**每步约 5m42s**；此前 243 帧单视频参考那次 **3323 秒**（帧数每多 42%，耗时翻倍以上）。
- 结论：`~left` 是同类任务历史中位数减已用时，345 帧两小时的任务它会一直显示几秒；判断卡死看 `log_age_s`（采样一步可能几分钟，进度条几分钟才动，但日志持续写入），持续变大（>10 分钟）且 step 不变才是真停。进度读 `progress` 不读 `~left`。
- 出处：`video-motion-drive.md` §6。
