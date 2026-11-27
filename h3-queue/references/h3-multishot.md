# 2.14 多窗一次生成（H3 Multishot，2026-11-13 接入 h3q）

### 先判断要不要用多窗（2026-11-20 定，给后续 agent 的选路依据）

**默认单镜 `pdd`，能拆成两个单镜就拆。** 多窗不是"同机位就该用"，它只解决一件事：
同一机位、同一场景里，动作或对话必须无缝连续，拆成两段会有肉眼可见的接缝。

| 判断 | 选哪条 | 依据 |
|---|---|---|
| 这镜能不能拆成两个单镜（各自有首帧/参考） | **能拆就拆，走单镜 pdd** | 单镜走 8 步蒸馏、快于多窗记忆采样约一个量级（多窗无 pdd 版本）；带日期耗时实测格见 [`seam-transition.md`](../../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md) §0.2 multishot 行 |
| 是否同机位同场景、且接缝必须无缝（动作接力、连续对话、光影不能跳） | 才考虑 multishot | context_pin 把上一窗末 22 帧 raw latent 钉进下一窗 |
| 只是"同一个房间，先后两个动作" | **不算**，拆单镜 | 用上一镜末帧当下一镜首帧即可，EP005 002 就是这么过的 |
| 有静默窗（这一窗没人说话） | 慎用多窗 | ref2va 会给静默段编台词，调参压不住，只能后期换底噪或 guide_audio 锁音轨 |
| 创作者反馈"还是有硬切"，逐帧看机位/光影/人物大小都连续 | **先判型再动手——多窗救不了词层的缝**：查是镜内相位断（入场被压缩）还是情绪缝（切点跳档）。判型顺序见 [`seam-transition.md`](../../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md) §0.1 第 0 步、修法见 `../../h3-prompt-writing/references/failure-modes.md`，本表不复制。修完词才重出，别反复重做容器 | 经过见 [incidents.md](incidents.md) §2026-11-19/20 |

**代价要写进决策**：双窗 20 分钟以上（EP005 S-002 判废经过见 [incidents.md](incidents.md) §2026-11-19/20）；需要 `scene_video` 做场景锚，否则房间会被重画；静默窗有编台词风险。

**选路硬依据（2026-11-21 实测）**：单镜 `first_frame`（锁首帧）与 `refs`（身份板）在 adapter 层**互斥**，同 job 不可兼得（直接报错）。所以**双人同场、既要逐帧锁起帧又要双身份板的连续段，只有 multishot 一条路**（两窗各挂各的身份板）——别再试「单镜带两人」绕路。**只要起点构图接上、不要求逐帧锁**时还有第二条：末槽续接——身份板照挂，上一段真实末帧占最后一个 `reference_image` 槽（不是 `first_frame`，所以不触发上面那条互斥），正文首句 `The shot opens on the same framing as <Picture N>.`；它不继承动作，做法见 [continuity-routes.md](continuity-routes.md) §2.13。context_pin 验证状态见 [incidents.md](incidents.md) §2026-11-21（0.45.3 实测通过；容器缝与词层缝分开）。

**"同机位"本身不是用多窗的理由**——能拆就拆成单镜；多窗也管不了词层的相位断与情绪跳档，先在词层判型修词（判型顺序见 `../../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md` §0.1 第 0 步，判据见 `../../h3-prompt-writing/references/failure-modes.md`）。两则反面教材（EP005 002 双窗 26 分钟判废、EP004 006+007 两轮词层缝）经过见 [incidents.md](incidents.md) §2026-11-19/20。

### 通道与参数

同机位且确需无缝连续时，用 `--workflow multishot` 一次出两窗，接缝由模型内部处理。

**通道**：`h3qc submit --workflow multishot --frames-per-shot 226 --shot-count 2 --refs a.png,b.png,...`（`h3qc.py` 为渲染机侧私有脚本，须另行部署，见 [h3-queue §8](../SKILL.md)）
→ h3q 调用渲染机上的 `multishot_render_ref.py`（不入本仓库）→ **V2 `H3MultishotMemorySampler`（模板 `<渲染机根目录>\config\multishot-v2.json`）**。

> **2026-11-15 起 multishot = V2 取代 CORE**（操作者指令），决策经过见 [`delivery-specs.md`](delivery-specs.md) 通道状态段。现用模板 `<渲染机根目录>\config\multishot-v2.json`（MemorySampler node30 / SaveVideo node27 / SaveAudio node28、pin_frames=22），`multishot-core.json` 保留为历史。
> - **v2 内建超分不用**：`output_scale=1 / upscale_model_name=(none)`；本机 16G 发糊、更慢到出不来，要超分走成片后处理 `h3_upscale_video`（§2.11）。
> - **必须注册的多角色参考参数**（渲染器已加）：
>   - `reference_subjects`（如 `"1,1"`=2图2人 / `"3,3"`）：多角色参考不分组会被当同一人 blend。**2026-11-19 起渲染器不再自动编 `"1,1,1"`**——它以前按 refs 张数"每人一张"兜底，等于给场景锚也造了一个从不出现的"第三个人"；现在留空就交给节点默认（全部 `<Subject 1>`），并由渲染器日志告警。**V2 记忆采样器没有「这张图只当场景、不当人」的参考输入**：`reference_subjects` 只能把图片分组到 `<Subject N>`，同场连续任务里的场景锚仍会占一个 subject 名额，这一点写在 MCP/渲染器参数说明里。端到端路径：`h3qc --reference-subjects` → `params.reference_subjects` → `h3q` 白名单 → `multishot_render_ref.py --reference-subjects`。
>   - `reference_image_size`：`match`=缩到生成画布（省显存快）；`max`=参考图原生(≤2048)不缩（清晰但 shot2 offload 更重更慢，实测 2×141 双窗 max 约 12min vs match 约 9min）。**默认 match**——渲染器 `multishot_render_ref.py` 的形参缺省、adapter 未声明、MCP 未声明三处都是 `match`，任一处都不按 `max` 兜底；需要保留参考原像素时才显式传 `max`。
>   - **端到端参数路径（只有这一条）**：`h3qc submit --workflow multishot --reference-image-size match|max` → 写入 `params.reference_image_size` → `h3q.py` 白名单原样转发 → `multishot_render_ref.py --reference-image-size` → 采样器输入。跳过任一环就是静默丢弃，不要绕过 h3qc 直传渲染器。
>   - `same_scene_continuous`：**不是渲染器参数**，`h3qc/h3q/renderer` 都不认识它；它只存在于 adapter `parameters` 与 MCP 入参，必须在提交前完成校验，验不过就不提交。只在显式声明 `true` 且 `workflow=multishot` 时生效，要求同组同时具备：①至少一张已准入的**身份**参考；②一个明确的 `scene_anchor_index`（adapter 用 `reference_bindings` 的 1-based 序号；MCP 用 refs 的 1-based 序号）指向**已准入的地理/构图锚**；③bindings 的 `may_control` 写清身份职责与地理/构图职责，`must_not_control` 不得否认。换场、硬切、未声明都完全跳过这条校验，行为与引入前一致；非 multishot 作业显式 `true` 直接拒绝。
> - **场景锚首选 `scene_video`（2026-11-19 晚起端到端接通）**：同场连续时给上一镜已验收成片的
>   片段，走 `reference_video`（LoadVideo → GetVideoComponents → H3ReferenceVideo），节点把它声明为
>   「同一场景的早先时刻」，保留取景、机位距离、房间内容与色温。**不要再把场景图塞进 `refs`**：
>   记忆采样器会把 `reference_images` 里每张图都声明成「`<Subject N>` 的照片」，场景图会占掉一个
>   人物名额并把画面拉向人脸（失败经过见 [incidents.md](incidents.md) §2026-11-19 EP005 S-002）。参数：`scene_video`（片段文件）、`scene_video_start`
>   （默认 8.5 秒）、`scene_video_seconds`（默认 3.0 秒，2-4 秒足够，更多只增加每步 token 开销）。
>   音频不接，采样器自动配静音，只带房间与光线。与 `scene_anchor_index` 二选一，同给直接拒绝；
>   仍需至少一张已准入的身份参考。端到端路径：MCP `scene_video`（project 入口给项目相对路径，
>   自动转绝对并 scp 到 ComfyUI input/，**不走图片缩图管线**）→ `h3qc --scene-video` →
>   `params.scene_video` → `h3q` 白名单 → `multishot_render_ref.py --scene-video`（运行时注入
>   200/201/202 三个节点，模板保持干净）。`--model` 同日接通，可覆盖模板 checkpoint，不必再为
>   换权重复制模板；`bank_clip_frames` / `audio_pin_frames` 也已透传到同一层。
> - **`auto_chunk_ffn`（默认 on，端到端已接通）**：权重装不下时分块 FFN（chunks=2），让 DiT 保持驻留，而不是每步从内存流式加载。实测失败经过见 [incidents.md](incidents.md) §2026-11-19 EP004 v5。路径：`h3qc --auto-chunk-ffn on|off` → `params.auto_chunk_ffn` → h3q 白名单 → `multishot_render_ref.py --auto-chunk-ffn` → node 30；缺 sol-attn 时节点打印 `skipped` 并照常跑。慢的根因不是参考图：提速只有三条——①`auto_chunk_ffn` 让权重驻留；②降 `frames_per_shot`（294→226→141）；③降画布。三条都不改变叙事，只改单窗时长。
> - **多窗代价仍在**：v2 每多一窗记忆库+22帧latent 使 shot2 起必 offload，慢；单镜快、多窗长片 16G 上代价高。
> - **已知双层压缩**：上传层 `REF_LONG_EDGE=2048`（MCP `_prep_for_upload`，全档位通用）对长边>2048 的参考图仍会 PNG 下采样（如 3104 三视图板→2048）；`reference_image_size=max` 只保证 2048 内不再缩。身份参考尽量用单张≤2048 图，别塞超大拼板。

**script 格式**：一个文件，两窗之间用单独一行 `---` 分隔；每窗写自己的 `00:00.000 → 00:09.417` 时间线、对白与可见状态。
不要写 `subject_definitions:` / `integrated_multimodal_description:`（那是 Ref2VA/Base 的六段三段结构）。

> **窗口正文不要以 `[` 或 `{` 开头。** `H3MultishotMemorySampler` 用 `text.startswith("[")` 判定整份脚本是不是 JSON 数组，以 `[Shot 1] ...` 开头的窗口会被当成坏 JSON，内容本身正确也白烧（经过见 [incidents.md](incidents.md) §2026-11-19 EP004 v5 窗口以 `[` 开头）。窗口正文直接从场景/人物写起即可。
>
> **2026-11-19 起三层都会在提交前拦住这个错误**：
> ① `h3_gate.py --mode multishot`（G39 查窗口数/窗口开头/单镜段名混入，G40 逐窗查
> `<d>` 格式、`<d>` 外中文、每窗 ≤362f（15s 网格吸附后的物理帧数））；② adapter `verify_multishot_script`
> 在 SSH/上传前拒绝；③ MCP `_verify_multishot_script` 在建临时文件前拒绝。
> **多窗不再「整块豁免结构项」**——那是把检查删掉，不是适配。

> 第二窗开头**没有必须复述前一窗收尾状态的通用硬规则**。V2 `H3MultishotMemorySampler` 已在 latent 层用 `context_pin` 钉住接缝（机制见 [incidents.md](incidents.md) §2026-11-21），连续性不依赖提示词复述；只有在换机位、换主体或正文自身需要交代起点时才重述，
> 否则重复描述会与第一窗的收束句冲突。个别历史案例写过「chain boundary is a clean same-camera cut」，
> 那是该案例的写法，不是 multishot 的准入条件。

**实测（2026-11-13 EP003 001+002a）**：2×226f → 451f / 18.792s / 768×448，内部接缝 PSNR **31.9 dB**（该 451f 按 [multishot-capacity.md](multishot-capacity.md) 的总帧口径算；同一对镜头逐段生成再拼为 23.4 dB，肉眼可见人物放大约 6%、妈妈背影变宽，见 [incidents.md](incidents.md) §2026-11-19）。

**音色跨窗必须钉住（2026-11-13 EP003 005+006 实测）**：`H3MultishotSampler` 有两个开关决定音色：

- `seed_per_shot` **缺省 True**。依据是节点作者的实测原话「每窗换 seed 才跨窗保住脸；所有窗共用一个 seed
  会让脸和声音一起漂移」，本仓也见过把 False 设下去后第二窗音色变调（F0 291 → 364 Hz）。这是实测倾向，不是采样器机制约束（False 也能跑），没有特殊理由别改。
- `self_anchor_voice=True`：第一窗渲完后，它自己的音频成为后续每窗的 `<Audio 1>` 参考，音色钉在模型
  实际念出来的那一版上。实测两窗角色C F0 340 / 327 Hz（差 0.7 个半音）。第一窗要安排一句干净独白。

需要跨集、跨文件固定音色时喂外部音频：`H3MultishotSampler` 有 `voice_ref` / `voice_ref_2` / `voice_ref_3`
（AUDIO，接 `LoadAudio`），底层官方节点 `MiniMaxH3ReferenceToVideo` 也有 `ref_audios`（最多 3 条，
提示词里写 `<Audio 1>`）。`ComfyUI-H3-Multishot` 自带 `H3ReferenceAudio` 负责转 32 kHz 立体声。

**参数与限制**

| 项 | 值 |
|---|---|
| 单窗帧数 | `17k+5`，226f = 9.417s 已验证；单窗 ≤362f（15s 经 24fps/17k+5 向上吸附为 362 物理帧，与 G25 同网格口径；仅 `--frames 362` 或文件名 362f 放行，显式 `--seconds` 不共享该豁免） |
| 总帧上限 | 实测上限 **451**（总帧口径与容量核算见 [multishot-capacity.md](multishot-capacity.md)）；adapter 已放行，超限只告警不拦截（见 §2.12） |
| 输出尺寸 | 直接给 `--width/--height`（768×448），没有 pdd 二采放大；要更大走 §2.11 latent 放大 |
| 参考图 | 走 `--refs`，最后一槽放构图参考；数量可变（renderer 动态重建 ImageBatch 链） |
| 身份 | 走首窗的完整人物描述，不靠 `(Sx)` 之外的东西 |

**交付帧数不是确定值（V2 重定时）**：每窗帧数是请求值而非交付保证值，取回按下限核对；完整口径与实例见 [multishot-capacity.md](multishot-capacity.md)。

**分工**：同机位连续、请求总帧 ≤451 的段落用 multishot 一次出；换场、反打、总帧超限**建议**按 Ref2VA 逐段生成再硬切（adapter 已不再按 451 硬拦，超限会照常提交，显存风险自负）。

**闸门**：multishot 脚本用 `h3_gate --mode multishot`，由 G39/G40 检查每窗格式与时长（每窗 ≤362f——15s 经 24fps/17k+5 向上吸附后的物理帧数），G25 在 multishot 模式下不注册、不适用。
组窗前先用 gate 逐条检查每个**单镜**提示词（`--mode ref --frames <单窗帧数> --refs N`，必须 0 error）；单镜 >15s 默认被 G25 拦。
`--allow-long-video` 仅供不经 h3q 的手搓直投通道显式豁免长端 warn，h3q adapter 不透传该 flag；h3q 常规路径仍受 G25 error 兜底。

**长镜末段回灌参考图**：长镜（≥10 s）且挂角色三视图时，结尾要显式锁场景与机位，别让「两人并排微笑」成为正文的最后一句，否则后段会把参考图直接渲进成片。实测经过见 [incidents.md](incidents.md) §2026-11-13 长镜末段回灌参考图。

