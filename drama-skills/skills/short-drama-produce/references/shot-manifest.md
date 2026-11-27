# 生产清单（shot manifest）

**它是什么**：一集一份的 YAML/JSON 生产绑定文件。只承载「资产 → 词稿标签 → 通道槽位 → 提交参数」，不承载剧情、台词、分镜正文或提示词正文。

**为什么需要它**：同一张场景板在不同文档里可能同时是 `<Picture 1>`、`<Subject 3>`、`<Video 1>`。这些编号各自是**词稿局部**的，但投递单、brief、提示词三处各抄一份就会读成互相矛盾。清单把每个镜头的 technique 与 bindings 绑在一起，让标签只有一个所有者。

**边界**：
- 创作真相仍是 Markdown：剧本、视觉设定、导演、分镜、图片提示词、视频提示词。
- 清单是**生产 build file**，不是第七份创作文档。它可以用脚本从现有文档生成或回填，但不反向改写创作文档。
- 提示词正文仍由 `$short-drama-video-prompts` / `$short-drama-image-prompts` 持有；清单只引用文件路径，不复制正文。
- 通道能力（workflow、refs、scene_video、voice_ref）由 `h3-queue` 持有；清单只声明本次用了哪些槽位，不重定义能力。
- 闸门只查格式；清单查「标签与绑定是否对得上」。两者都过才提交。

## 归类与路由

| 层 | 持有什么 | 不持有什么 |
|---|---|---|
| `short-drama-storyboard` | shot ID、镜长、画面证明计划 | 生产绑定、通道参数 |
| `short-drama-video-prompts` | 提示词正文、H3 的 `<Picture/Subject/Video/Audio>` 写法 | 资产版本、提交参数 |
| `h3-queue` | workflow/refs/scene_video/voice_ref 的能力与实读方法 | 本项目哪张图对应哪个标签 |
| **`short-drama-produce`（本文件）** | **资产版本、shot technique、绑定、提交参数、校验规则** | 剧情、台词、提示词正文 |
| `h3-video-gate` | 格式/标签/时间线/算术 | 绑定语义、资产哈希 |

清单放在 `剧集/<EP>/制作清单.yaml`（或 `.json`）。一集一份；跨集共享的资产在各自清单里用同一 `asset id` 引用。

## 顶层结构

```yaml
schema: shot-manifest/v1
plan:
  id: EP001-plan-v1
  status: active            # active | archived
  supersedes: EP001-single-shot-v1
project: {id: example-project, episode: EP001, fps: 24}
canvas: {width: 576, height: 1024, declared_aspect: "9:16"}

assets: {}                  # 见「资产」
shots: []                   # 见「镜头」
```

`declared_aspect` 是项目声明；`canvas` 是本次实际生成画布。清单只校验声明格式，不发明容差阈值；两者是否一致由人判断，不擅自改项目声明。

## 资产

```yaml
assets:
  ASSET-IDENTITY-A:
    kind: identity          # identity | scene | prop | style | action | audio | clip | keyframe
    admission: {status: accepted, ref: "审查/look/example.look.json"}
    versions:
      - version: 1
        path: assets/identity-a.png
        sha256: "<64-hex>"
        previous_path: assets/old-name.png   # 可选，改名追溯
```

- `id` 稳定、永不复用；`asset@version` 指定版本，省略版本取最大版本号。
- `sha256` 必填；`validate` 与实际文件比对，不一致拒绝。草稿期可用 `--allow-missing-hash` 降级为 warning。
- `kind` 只描述资产类型，不描述它在某镜里的职责。职责写在 `bindings[].role`。
- `admission` 与 `审查/look/*.look.json` 的准入状态一致：`accepted` / `creator_original` / `reviewed` / `unset`。`unset` 默认 error，`reviewed` 是 warning；草稿期可用 `--allow-unadmitted` 把 `unset` 降为 warning。
- admission 只对 **active shot 实际绑定** 的资产强制；没有被任何 active shot 使用的设计参考可以留在 `assets` 里，不强制准入。
- `kind: keyframe` 用来标起始帧/构图帧；它仍按 `bindings[].role` 决定在镜头里的职责。

## 镜头与绑定

```yaml
shots:
  - id: S1
    shot_id: SHOT-EXAMPLE-01
    technique: ref2va        # ref2va | frame_ref2va | i2va | fl2va | multishot | motion_drive | t2va
    status: active           # active | archived
    origin_plan: EP001-single-shot-v1
    prompt: prompts/shot-01.txt
    frames: 121
    bindings:
      - asset: ASSET-SCENE@1
        role: scene
        ref_slot: 1
        label: Scene board
        prompt_label: "<Picture 1>"
        subject_label: "<Subject 3>"
        may_control: [scene, environment, layout]
        must_not_control: [identity, face]
      - asset: ASSET-IDENTITY-A@1
        role: identity
        ref_slot: 2
        label: Identity A
        prompt_label: "<Picture 2>"
        subject_label: "<Subject 1>"
        may_control: [identity, face, character]
        must_not_control: [composition, lighting]
      - asset: ASSET-IDENTITY-B@1
        role: identity
        ref_slot: 3
        label: Identity B
        prompt_label: "<Picture 3>"
        subject_label: "<Subject 2>"
        may_control: [identity, face, character]
        must_not_control: [composition, lighting]
    submit:
      workflow: ref2va
      engine: pdd
      tier: draft
      width: 576
      height: 1024
      refs_order: [ASSET-SCENE, ASSET-IDENTITY-A, ASSET-IDENTITY-B]
```

### technique 与必填槽位

| technique | 用途 | 必填 bindings | 禁止 | `submit.workflow` |
|---|---|---|---|---|
| `ref2va` | 单镜参考图（默认） | 至少一个 reference 类（`identity`/`scene`/`prop`/`style`）；每个 reference 带 `ref_slot` + `prompt_label` + `subject_label` | `first_frame` / `last_frame` / `video_label` | `ref2va` 或 `pdd_lu` |
| `frame_ref2va` | 首帧 + 身份参考（词稿 `<Picture 1>`=首帧、`<Picture 2/3>`=身份板） | 恰好一个 reference 类带 `semantic: first_frame`；至少一个 `identity` reference；所有 reference 带 `ref_slot` + `prompt_label`；identity 带 `subject_label` | provider `first_frame`/`last_frame`；`scene_video`/`action_video`/`audio` | `ref2va` 或 `pdd_lu` |
| `i2va` | 单首帧 | 恰好一个 `first_frame` | `last_frame`；额外 reference 类（`identity`/`scene`/`prop`/`style`）；多首帧 | `ref2va` |
| `fl2va` | 首尾帧 | 恰好一个 `first_frame` + 一个 `last_frame` | 额外 reference 类（`identity`/`scene`/`prop`/`style`）；多首/多尾 | `fl2va` |
| `multishot` | N 窗容器（N≥2） | `ref_slot` 从 1 连续；每个 reference 带 `subject_label`；`scene_video` 最多一个 | 任何 `prompt_label`（`<Picture N>`）；`first_frame` / `last_frame` | `multishot` |
| `motion_drive` | 动作驱动直投 | 一个 `action_video`；至少一个 `identity`；`audio` 可选 | H3 的 `prompt_label` / `subject_label` | `motion_drive` |
| `t2va` | 纯文生 | 无 | 任何 binding | `ref2va` |

`technique` 是判别键。校验器只允许该 technique 声明的槽位；多一个槽位就报错，不静默忽略。窗口数的当前上限由 `h3-queue` 的 adapter/MCP 实读决定；清单只要求 ≥2，不在文档里缓存上限。

**词稿段式也由 `technique` 决定**，`prepare` 会拦错配：

**`t2va` 能不能真跑，取决于档案的 `supported_generation_modes` 有没有 `text`。**本地 h3q 通道档案没有 `text`（只有 `first_frame` / `first_last_frame` / `reference`），所以在那条通道上别用 `t2va` 排生产——清单允许这个值，不等于当前通道执行得出。依据见 `short-drama-video-prompts/references/seam-transition.md` §三 与 `short-drama-storyboard/SKILL.md`「不含 `text` 时不提供改走文生视频」。

### 连续性优先：先选路，再选 technique

同一场、同一段连续动作（连续对话、动作接力、光影不能跳），**先按接缝阶梯选路**，
别在「首帧接力」和「末帧当参考」之间二选一——那是跳过前两步之后的备选：

| 情况 | 用什么 | 身份参考 |
|---|---|---|
| 一次生成装得下 | 单镜（`ref2va` / `frame_ref2va`） | 照挂 |
| 装不下，但同机位同场景、接缝必须无缝 | **多窗容器 `multishot`**（潜空间接力） | **照挂**（每个 reference 带 `subject_label` 即可）。但一组参考图整段共用：后段才出场的角色，他的板会污染前面几窗；道具图同理。切分边界要么画在他出场之前，要么接受提前入画（`seam-transition.md` §6.4.1） |
| 两段各自出片、同空间、机位或站位有变 | **转场卡**（A 真实末帧 + B 真实首帧 → FL2VA 中段） | A/B 各自保留 full-reference |
| 两段各自出片，身份要保、起点要接上 | **Ref2VA 末槽**（末帧放最后一个参考槽 + 固定首句） | **照挂** |
| 跨场景 / 不需无缝 / 不重挂身份 | 首帧接力 | 会丢身份参考 |
| 必须重挂身份又接不上 | 改机位重出，别设计「接着上一段」 | 照挂 |

**「多帧参考」不是这条链路上的可选通道**：按 `frame_idx` 把多张静帧钉到时间线（ComfyUI 的
`Add Guide` / Multiframe Reference）当前**没有接入口**——adapter 的视频 workflow 只有
`ref2va` / `multishot` / `fl2va`，清单 schema 也没有对应字段。它是 `h3-queue` 的超分/longshot
合同里记录的能力，要用得先在通道侧接上，别在选路时把它当现成选项。

**`i2va` 不是连续性手段**：它只接受一个首帧，且禁止任何额外 reference——用它接上一镜，
等于同时丢掉身份板和场景板。它只适合「本来就只有一个起始图、不需要身份锁」的镜。

判据四项、各种手法的实测数字、转场卡的投递约束，都在
[`short-drama-video-prompts/references/seam-transition.md`](../../short-drama-video-prompts/references/seam-transition.md) §0.1 与 §0.4。
本表只做入口，不复制数值。

| technique | 词稿段式 |
|---|---|
| `ref2va` / `frame_ref2va` / `motion_drive` | 六段（`subject_definitions` → `summary` → `retention_analysis` → `detailed_description` → `overall_soundscape` → `non_diegetic_music`） |
| `t2va` / `i2va` / `fl2va` | 三段（`integrated_multimodal_description` → `overall_soundscape` → `non_diegetic_music`） |
| `multishot` | **不写段名**：一文件多窗，窗间单独一行 `---`，每窗只写正文。首行以 `[` 或 `{` 开头、或出现 `subject_definitions:` 这类段名，闸门 G39 直接报错（段名只属于单镜正文） |

`h3_gate.py --mode auto` 是**按文件自己判段**的：一份三段式词稿在 auto 下永远判成 base 并
顺利通过，哪怕这一镜挂着身份图、本该写六段。闸门不比对 `technique`，清单只查字段，
`creator_markdown_check` 不查段名——所以段式错配只有 `prepare` 拦得住，别指望闸门。
（段式定义与各段写法归 `h3-video-gate/SKILL.md` 与 `h3-prompt-writing` 持有，此处只记对应关系。）

`multishot` 的 `frames_per_shot` 必须是 17k+5（H3 自动对齐会吃掉零头），校验器按 `SUBMIT021` 硬拦，
adapter 同样 fail closed；先用 `h3-queue/scripts/frames.py` 算。`h3-video-gate` 的 G12 只报 warn——
它是通用提示词检查器，不知道你选的部署；帧格的硬约束在清单校验与 adapter 两层。

`frame_ref2va` 的首帧是**词稿语义**，不是 provider 的 `--first-frame`：binding 的 `role` 仍写 reference 类（`identity`/`scene`/`prop`/`style`），另加 `semantic: first_frame`；`plan` 仍按 `--refs` 送图，不传 `--first-frame`。这样「首帧 + 身份板」的混合词稿可以表达，又不会把 provider 分支误切到 i2va。

例：`role: scene` + `semantic: first_frame` + `prompt_label: "<Picture 1>"` 是首帧；`role: identity` + `<Picture 2>` / `<Subject 1>` 是身份板。`plan` 会把它们都放进 `--refs`，并提示「不传 --first-frame」。

### binding 字段

| 字段 | 必填 | 说明 |
|---|---|---|
| `asset` | 是 | `id` 或 `id@version` |
| `role` | 是 | `identity` / `scene` / `prop` / `style` / `first_frame` / `last_frame` / `scene_video` / `action_video` / `audio` |
| `semantic` | 否 | `first_frame` / `last_frame` / `composition` / `start` / `pose_proof` / `end`；`frame_ref2va` 的首帧 binding 必填 `first_frame` |
| `label` | 否 | 人类可读标签；默认用 asset id |
| `prompt_label` | `ref2va`/`frame_ref2va` 的 reference 类与 `first_frame`/`last_frame` | 词稿里的 `<Picture N>`；`multishot`/`motion_drive` 禁止 |
| `subject_label` | `ref2va`/`frame_ref2va` 的 reference 类、`multishot` 的 reference 类 | 词稿里的 `<Subject N>`；`frame_ref2va` 的首帧 binding 可省，identity 必填；`first_frame`/`last_frame` 可选 |
| `video_label` | 视 technique | 词稿里的 `<Video N>` |
| `audio_label` | 否 | 词稿里的 `<Audio N>` |
| `ref_slot` | `ref2va`/`frame_ref2va`/`multishot` 的 reference 类 | 1-based，连续；`refs_order` 按它排 |
| `may_control` / `must_not_control` | 是 | 控制边界，写入 job 的 reference_bindings |
| `start` / `seconds` | scene_video | 片段起点与长度 |

`i2va`/`fl2va` 只带首/尾帧；额外 `identity`/`scene` 参考不在本地 h3q 的端点分支里，清单直接拒绝。

`status: archived` 的镜头跳过校验，`plan` 会拒绝它；用于已并入别的镜、但词稿/资产还在的旧 shot。`plan.status: archived` 时整份 plan 也不出命令。

映射到 `production_tool.py` job 时：`identity` / `scene` / `prop` / `style` → `reference_image`；`first_frame` → `first_frame`；`last_frame` → `last_frame`；`audio` → `reference_audio`；`scene_video` / `action_video` 只走 h3qc / motion-drive 直投，不走本地 h3q 的 job binding role。

## submit

`submit` 只写本次提交参数，不写通道能力：

```yaml
submit:
  workflow: multishot
  engine: pdd
  tier: draft
  width: 576
  height: 1024
  frames_per_shot: 61
  shot_count: 2
  reference_subjects: "1,2"
  reference_image_size: match
  auto_chunk_ffn: "on"
  voice_ref: voices/a.wav
  voice_ref_2: voices/b.wav
  refs_order: [ASSET-IDENTITY-A, ASSET-IDENTITY-B]
  output: 剧集/EP001/制作成果/_草稿/MS-01/example.mp4
```

- `frames` / `frames_per_shot` / `shot_count` 必须与 shot 的帧数一致。
- `refs_order` 必须等于按 `ref_slot` 排出的 asset 顺序。
- `reference_subjects` 是**逗号分隔的字符串**（如 `"1"` 或 `"1,2"`），不是 YAML 列表——
  每项是正整数，项数必须等于 refs 数，第 i 项表示第 i 张参考图按哪个 `<Subject N>` 声明。
  写成 `[1]` 会报 `must be positive integers`。
- `ref2va` / `i2va` / `fl2va` 下，`identity`/`scene`/`prop`/`style` 类的 binding **必须同时带
  `prompt_label` 与 `subject_label`**（缺了报 `BIND015`/`BIND016`）；`multishot` 只要 `subject_label`。
- `first_frame` / `last_frame` 的 binding **也必须带 `prompt_label`**（如 `<Picture 1>`/`<Picture 2>`），
  缺了报 `BIND018`——首尾帧在词稿里同样是以 Picture 形式被引用的。
- 所有 binding（含 `first_frame`/`last_frame`）都要写 `may_control` 与 `must_not_control` 两段非空文本，
  首尾帧通常写 `may_control: [composition]`、`must_not_control: [identity]`。
- `submit.reference_subjects` **只用于 multishot**；其他 technique 写了报 `SUBMIT019`。
- 所有 `prompt_label` 与 `subject_label` 都必须**原样出现在该镜 prompt 正文里**（报 `PROMPT006`）。
- 每个 binding 的 `subject_label`（如 `<Subject 1>`）必须**原样出现在该镜 prompt 正文里**，
  否则报 `binding labels not in prompt`——挂了图却没在正文提到，等于没挂。
- binding 与 `剧本.md` 的 `- 输入参考图：REF-...` **逐字段一致**才算匹配（`slot_id`/`order`/`path`/
  `label`/`may_control`/`must_not_control`）：剧本里 `label` 必须等于清单 binding 的 `label`，
  `控制/不得控制` 两边都要用同一套英文枚举（`identity`/`face`/`composition`/`lighting` 等），
  一边写中文一边写英文会报 `job reference bindings do not match`。
### 同一镜的三处对照（一个镜挂身份的完整写法）

同一条参考在三份文件里各写一次，**必须逐字对齐**：剧本那一行、清单的 binding、正文里的标签。
下面是一个镜的同一份数据写成三处，照着填，不要各写一套。

`剧集/<EP>/剧本.md`「## 分镜」里的该镜：
```
- 输入参考图：REF-ASSET-HER（顺序：1）· 输入/identity-her.png《她的身份板》（用途：身份；控制：identity、face；不得控制：composition、lighting）
```

`剧集/<EP>/制作清单.yaml` 的该镜 `bindings`：
```yaml
    bindings:
      - asset: ASSET-HER@1
        role: identity
        ref_slot: 1
        label: 她的身份板
        prompt_label: "<Picture 1>"
        subject_label: "<Subject 1>"
        may_control: [identity, face]
        must_not_control: [composition, lighting]
```

`剧集/<EP>/脚本/motion_*.txt` 正文里要真的出现这两个标签：
```
[Shot 1] <Subject 1>, the woman shown in <Picture 1>, stands at the window ...
```

对照关系：`REF-ASSET-HER`↔`角色`（`slot_id` 由 `asset` 推出）、`顺序：1`↔`ref_slot: 1`、
路径逐字相同、`《她的身份板》`↔`label`、`控制`↔`may_control`、`不得控制`↔`must_not_control`。
两边控制范围都写**英文枚举**；一边中文一边英文，`prepare` 会以
`job reference bindings do not match` 拒绝，而 `creator_markdown_check` 不会拦——错到准备文件才暴露。

- `width` / `height` 必须是 32 的倍数。
- `voice_ref` / `voice_ref_2` 只在 `multishot` 下有效；其他 workflow 出现即报错。
- `gate_rate` 可选；不写就用闸门缺省，清单不缓存速率。
- `seed` 可选正整数；`plan` 会拼成 `--seed`。
- `remote_prompt` / `remote_refs` 可选：把项目相对路径映射到渲染机 ASCII 名；不写则 `plan` 输出 `<REMOTE_...>` 占位。
- `idem_key` 可选：一 job 一个，禁止复用；`plan` 会拼成 `--idem-key`。

## 接缝

`seams` 是可选顶层列表，只表达结构，不替代场记/导演的观感判断：

```yaml
seams:
  - id: S1-S2
    kind: inter
    from: S1
    to: S2
    join: interval
    gap_seconds: 1.0
  - id: MS-01-inner
    kind: inner
    shot: MS-01
    at_frame: 209
    join: continuous
```

- `inner` 只用于 `technique: multishot`：`shot` 必填，`at_frame` 等于 `frames_per_shot`（1-based），`join` 只能是 `continuous`，不能带 `gap_seconds`。
- `inter` 用 `from`/`to`，两者必须是不同 shot；`join` 取 `hard_cut` / `interval` / `j_cut` / `l_cut`，不能 `continuous`；`interval` 必须带 `gap_seconds`。
- `inter` 的 `reason` 取 `none` / `scene_change` / `time_jump` / `action_bridge` / `sound_bridge` / `identity_bridge` / `coverage_cut`。
- **同一场里的硬切必须写明理由**（`SEAM021`）：`reason: none` 会被拒。刻意的分镜覆盖（正反打、反应镜、插入特写）写 `coverage_cut`；有时间跳跃写 `time_jump`；有动作/声音/身份承接写对应的 `*_bridge`。
  依据：接缝阶梯第 1 步是「能连续就连续」，硬切是同场连续动作的**备选**而不是默认；不写理由就分不出「刻意切」和「没想过」。手法阶梯见 `short-drama-video-prompts/references/seam-transition.md` §0.1。
- 不要求清单覆盖所有相邻镜；只校验写出来的接缝。接缝的观感与「有没有用错」仍由人看。

## 台账字段（ledger）

台账只承载**生产数据与判断引用**，不定义故事状态。杯在不在台、哪只手扶杯、发丝别没别耳后属于剧本/场记/分镜的连续性 prose，不进本 schema；项目真要机检，自带扩展，validator 不把它当必填。

```yaml
shots:
  - id: S1
    doc_path: 剧集/EP001/剧本.md
    doc_id: 剧集/EP001/剧本.md#SHOT-EP001-01
    img_doc: 剧集/EP001/脚本/image/IMG-EP001-01-START.txt
    motion_doc: 剧集/EP001/脚本/motion_01.txt
    motion_id: MOTION-EP001-01
    img_ids: [IMG-EP001-01-START]
    kf_ids: [KF-01-START]
    timecode: {in_s: 0.0, out_s: 4.0}
    group: {scene: EP001-SC001, mode: single, seam_reason: none, note_ref: 剧集/EP001/剧本.md#接缝说明}
    reference_assets: [ASSET-IDENTITY-A, ASSET-SCENE-01]
    keyframes:
      - id: KF-01-START
        img_id: IMG-EP001-01-START
        role: start          # start|composition|pose_proof|end
        at_s: 0.0
        read: R1
        asset: ASSET-KF-01-START@1
        media_state: accepted # accepted|not_generated|stale|rejected
        audit: core           # core|optional
        prompt_ref: 剧集/EP001/脚本/image/IMG-EP001-01-START.txt
        basis_refs: [ASSET-IDENTITY-A, ASSET-SCENE-01, CARD-EP001-SC001-01]
        basis_note_ref: 审查/EP001-创作依据.md#IMG-EP001-01-START
        control_ref: 审查/EP001-创作依据.md#IMG-EP001-01-START
        proves_reads: [R1]
        evidence_refs: [审查/look/example.look.json]
        anchor: false
        decision_refs: [审查/EP001-决策.md#DEC-EP001-001]
seams:
  - id: S1-S2
    kind: inter
    from: S1
    to: S2
    join: interval
    gap_seconds: 1.0
    reason: action_bridge
    note_ref: 剧集/EP001/剧本.md#接缝说明
    reason_detail_ref: 审查/EP001-创作依据.md#seam-01
decisions:
  - id: DEC-EP001-001
    subject: KF-01-START.canonical
    field: state
    value: cup=on_table
    alternatives: [cup=in_hand]
    reason_code: creator_alignment
    refs: [审查/EP001-创作依据.md#DEC-EP001-001]
    status: accepted
conflicts:
  - id: CONF-EP001-001
    shot: S1
    field: position
    values: [outside, inside]
    refs: [剧集/EP001/剧本.md, 剧集/EP001/脚本/image/IMG-EP001-01-START.txt]
    status: unresolved
drift:
  - id: DRIFT-EP001-001
    kind: prompt_body
    refs: [剧集/EP001/脚本/motion_01_ref2va.txt, 审查/EP001-创作依据.md#video-doc]
    status: unresolved
qc:
  status: pending
  checks:
    - {id: KF-01-START, status: pass, evidence_ref: 审查/look/example.look.json}
```

- `doc_path` / `doc_id` / `img_doc` / `motion_doc` 必须存在；`doc_id` 的 `#anchor` 必须存在。
- `timecode` 是数字；`keyframes[].at_s` 是**镜内时刻**（与 `### 观众 reads` 同一把尺），不是全片累计时间；`group.scene` 是 `EPxxx-SCxxx`；`mode` 是 `single`/`continuous`/`interval`/`hard_cut`/`j_cut`/`l_cut`；`seam_reason` 只取结构枚举。
- `keyframes[].proves_reads` 只收 `R<n>`；`basis_note_ref` / `control_ref` / `evidence_refs` / `decision_refs` 的文件与 `#anchor` 必须存在；`basis_refs` 只收 `ASSET-*` / `LOCK-*` / `VF-*` / `CARD-*`。
- `seams[].reason` 只表达结构；叙事理由写 `note_ref` / `reason_detail_ref`，不进枚举。
- `decisions` / `conflicts` / `drift` / `qc.checks` 只写 ID、状态、引用；`reason_code` 是固定枚举，细节在 refs 指向的证据档。
- 不再接受 `basis` / `proves`（字符串）/ `controls` / `note` / `reference_note`；这些是 prose，进 `审查/` 或 `创作方向`。`state` 不是本契约的字段；项目自定义扩展不参与通用校验。

## 校验器

```bash
python3 {技能目录}/scripts/shot_manifest.py validate <project> --manifest 剧集/EP001/制作清单.yaml [--allow-unadmitted]
python3 {技能目录}/scripts/shot_manifest.py plan <project> --manifest 剧集/EP001/制作清单.yaml --shot S1 [--allow-unadmitted]
```

`validate` 检查：

1. 资产路径存在、SHA256 一致、`kind` 合法、准入状态已登记；`unset` 默认 error，`reviewed` warning，`--allow-unadmitted` 可把 `unset` 降为 warning。
2. 每个 technique 的必填/禁止槽位；`frame_ref2va` 必须恰好一个 `semantic: first_frame`。
3. 每份词稿里的 `<Picture N>` / `<Subject N>` / `<Video N>` / `<Audio N>` 与 bindings **双向 diff**：词稿里出现但 bindings 没有 → 报错；bindings 有但词稿没有 → 报错；同一标签绑定两次 → 报错。
4. `multishot` 词稿里出现 `<Picture N>` → 报错（V2 不读 Picture）。
5. `refs_order` / `reference_subjects` / `frames` / `width` / `height` / `seed` 的自洽。
6. `origin_plan` 不是当前 `plan.id` 的镜头：warning「旧方案复用，需重新核对绑定」；`status: archived` 的镜头跳过校验，`plan` 拒绝。
7. `seams` 的 `inner`/`inter`、`join`、`from`/`to`/`shot`/`at_frame` 结构自洽；不判断观感。
8. ledger：`doc_path`/`doc_id`/`img_doc`/`motion_doc`、`timecode`/`group`、`keyframes` 的角色/时间/`prompt_ref`/`basis_refs`/`basis_note_ref`/`control_ref`/`proves_reads`/`evidence_refs`/`decision_refs`、`seams` 的 `note_ref`/`reason_detail_ref`、`decisions`/`conflicts`/`drift`/`qc.checks`，以及 prose 字段拒绝。
9. 项目自定义的 `state` 扩展不参与通用校验；连续性状态由剧本/场记/分镜 prose 负责。

`plan` 先校验全部 **active** shot；archived 跳过。有 error 就不出命令；`--allow-unadmitted` 只用于预演，生产不要带。输出该镜的闸门命令与提交命令；命令从清单生成，不再手写。`--json` 输出 `{shot, gate, submit, notes}`，供其他脚本消费。

## 迁移顺序

1. 先给一集建清单，只填资产、shots、bindings、submit。
2. 跑 `validate`，把现有投递单里手写的 `Picture/Subject/Video` 编号全部改成清单指针。
3. 跑 `plan`，用生成的闸门/提交命令替换投递单里的手写命令。
4. 跑 `h3_gate.py` 与 `plan` 的 gate 命令，两者不一致就不提交。
5. 方案变更（如 Ref2VA → multishot）时改 `plan.id` 与相关 shot 的 `technique`，旧 shot 标 `origin_plan`；`validate` 会点出未重新核对的旧绑定。

## 非目标

- 不替代 `h3_gate.py`：闸门查格式，清单查绑定。
- 不替代 `production_tool.py`：清单是 preflight，job 仍是执行单元。
- 不引入 USD/OTIO 的时间模型或层叠合成；只用它们的「资产版本 + 引用完整性 + 判别联合」三个概念。
- 不把清单当创作真相；剧情/台词/分镜正文改在 Markdown，改完再更新清单。
