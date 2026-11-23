---
name: concat-video
version: 1.2.0
description: 用 Concat（headless MCP）剪视频：拼接、转场、字幕、水印、关键帧、特效、导出成片。当用户要"剪视频/加转场/上字幕/打水印/出成片"，或点名 concat / mcp__concat 工具，或要把素材自动装配成可交付 MP4 时使用。不生成 AI 视频素材（归 short-drama-produce；AI 视频提示词与出片走 h3-prompt-writing / h3-video-gate / h3-queue），不做创意提示词；只处理已有媒体文件的剪辑。项目里有 `剧集/<EP>/剪辑单.md`（短剧项目）时不用本技能，转 short-drama-edit。
---

# Concat 视频剪辑（headless MCP）

Concat 是 Rust 原生剪辑器，自带 MCP server：agent 通过工具面完成真实时间线编辑并本地导出
MP4，无需打开 GUI，也不依赖系统 ffmpeg 的字幕滤镜（文字与转场由其自有 GPU 合成器渲染）。

## 入口判断

- 本会话已有 `mcp__concat__*` 工具 → 直接用。
- 没有 → 用 Bash 起 stdio 进程：`~/.local/bin/concat-mcp headless`
  （JSON-RPC over stdin/stdout，握手 `initialize` → `notifications/initialized` → `tools/call`）。
- 已接线位置：DSH profile `cordis.patch.yml` 的 `mcp-concat` 条目；Qoder `~/.qoder-cn/mcp.json`。

## 准备期借用知识

文档准备、导演与场记可提前读取剪辑方法及本技能的能力/素材余量限制，用于安排可执行的接法；不因此提前创建工程或装配。效果目录不等于动作匹配、视线承接、反应切、声桥等剪辑组织方法，也不要求用满效果。短剧准备与条件交接见 [语料机制与剪辑准备](../drama-skills/skills/short-drama/references/mechanism-preparation.md)，实际短剧交付仍由 short-drama-edit 维护。纯已有素材执行不另起创作流程；要补素材或改镜头职责/起终态时回对应 owner。

## 标准流程（每个工程都走这条）

1. `project_create`：`{location, name, video:{width,height,rateNum,rateDen}}`。
   返回的 `path`（= `location/name` 文件夹）是后续所有工具的工程句柄。
2. `media_import`：`{path, file:<绝对路径>}` 逐个导入，`createdId` 即 `mediaId`。
3. `clips_add_sequence`：`{path, mediaIds:[...], start:0}` 按序铺满最低空轨；
   单条插入用 `clip_add`（`trackId` 可先 `track_add` 拿新轨）。
4. 叠加层（顺序敏感，先读后改）：
   - **转场**：`clip_update` `{clipId:<后一段>, patch:{transitionIn:{id,duration}}}`。
     内置切型 `cross-fade / fade-black / fade-white / push / zoom / wipe-left / wipe-right`；
     花哨转场走效果目录：`effects_list {kind:"transition"}` 现有 22 个 `concat.*`
     （blur-dissolve、glitch-warp、whip-pan、cube、iris、light-leak-flash…），
     同样填进 `transitionIn.id`。
   - **字幕**：`captions_add` `{captions:[{start,end,text}], style:{color,fontSize…}, offsetY}`。
     `offsetY` 是相对画面中心的帧高分数：0.35 底部（默认）、-0.35 顶部。中文直接可用。
   - **水印**：logo 图片 `media_import` → `clip_add` 到上层轨 →
     `clip_transform` `{offsetX,offsetY,scale}`（分数偏移，正=右/下；scale 1=满幅，
     角标水印约 `scale 0.15, offsetX 0.36, offsetY -0.40`）→ `clip_update` 把该 clip
     `volume:0` 静音（图片素材默认 5 秒时长，用 `clip_trim` 对齐片长）。
5. `project_save` → `export_start` `{path, output, codec:"h264", crf:20}` →
   `export_wait` `{job, timeoutSeconds}`。`state:"done"` 且 `frame==total` 才算导出成功。
6. 验收：`preview_frame` `{path, time, width, height}` 返回 **image content block**
   （PNG base64，不在 JSON text 里，解析时取 `content[type=="image"]`）；
   或落盘成片后用 `ffprobe` 核对时长/分辨率。

## 铁律

- **时间线读法**：`timeline_read` 的片段在 `timeline.clips` 平铺数组（含 kind/id/start/end/track），
  不在 lanes/tracks 下——解析错键会静默漏掉片段。
- **headless 写域**：只允许写 `$HOME` 下；素材与工程放 home 内，或设 `CONCAT_MCP_ROOTS`。
- **工程锁**：一个工程文件夹同时只能被一个进程打开（窗口打开时 headless 会拒绝，反之亦然）。
- **导出超时**：渲染是分钟级，MCP 客户端侧 `toolCallTimeoutMs` 要 ≥600000（DSH 条目已配）。
- 编辑只在 `project_save` 后落盘；未保存的修改随 `project_close(save:false)` 丢弃。
- **交付尺寸随素材自动判定**：装配脚本的输出 `scale=WxH` 不写死成 1024×576。素材做过 latent 放大或像素超分（任一段宽>1024）时自动取 1536×864，否则 1024×576，无需手工设 `CONCAT_OUT_SIZE`（显式设环境变量仍可覆盖）；硬编码会把高分辨率在输出层缩回去，等于白放大；画幅不一致先 pad/crop 到同一比例，不强拉。评估画质收益必须在同一输出尺寸下做 A/B（见 `h3-queue/SKILL.md` §2.15）。
- **cross-fade 是按切点启用的工具，不是全量规则**：跨镜头接缝的柔化用 `xfade` 视频 + `acrossfade` 音频。本机实测（2026-11-15 S2↔S3）：同一对镜头硬切帧间 MAD 76.59，cross-fade d=0.25 压到 15.93（降 79%）——技术上确实更平滑。但**场切/反打/回主位这些"硬切"是导演意图，默认不加 cross-fade**（加了会毁掉切的节奏）；只有剪辑明确要求柔化某个缝时才启用。同段内多窗接缝（模型内部从上一窗真实末帧续起）ΔYAVG 仅 1.3，本就不用处理。实现：`concat.py` 的 `DISSOLVE` 字典按切点加条目（默认空）。
- **颜色/亮度校正放循环外，对成片做单一全局目标**：逐段各自调色会在每个接缝留下亮度、对比与细节台阶（Multishot SETTINGS.md 实测三镜内纹理 +142%、亮度 +18%）。重复边界帧必须裁，音频 40 ms weld 要另补偿，否则累计 A/V desync（见 `h3-queue/SKILL.md` §2.16）。
- **本机离线实测（2026-11-15，R10）**：同一镜内连续两半，逐段 GRADE 在接缝 t=3.000s 的 YAVG step **+12.484**（全局归一 +0.475，26.3×）、单帧跳变 −11.938、接缝两帧 PSNR **24.54 dB**（全局 28.93 / 无调色 29.15）、Y-MAD 是镜内 9.96 倍，台阶主要落在 Y 通道；三版 A/V 均 6.000000s / 144 v 帧 / 282 a 帧 / 48 kHz，差 0 ms。缩略图下台阶会变不明显，判据须看原尺寸并排。

## 转场要真出效果：双向余量 + 零间隙（2026-10-20 实测定论）

`cross-fade / push / zoom` 走导出期的 `overlap()`：**借用源素材余量做真实重叠**，会让成片变短。
它同时要求三件事，缺一条就静默退化（转场"看起来像重影"、时长一分不少）：

1. **同轨相邻**：前段 `end` 与后段 `start` 之差 < 半帧。留了间隙 = 转场被丢弃。
2. **后段有头部余量**：`sourceStart > 0`，否则 `lead=0`，只剩单边淡入。
3. **前段有尾部余量**：`素材时长 - sourceStart - 片段时长 > 0`，否则尾段用定格帧凑，观感发死。

AI 生成素材（H3 等）通常首尾用满、零余量，必须先在源上补余量。已验证可用的完整配方：

```
1) ffmpeg 预补余量：tpad 首尾各 clone 0.8s（视频）+ adelay/apad，重编码 crf16
2) clip_add 逐个按精确 start 落位（**必须带 trackId**，否则 invalid type null）
3) clip_trim edge=start delta=0.8 ripple=true   # 收头：sourceStart 抬到 0.8，后段自动前移
4) clip_trim edge=end   delta=-0.8 ripple=true  # 收尾：腾出尾部余量并保持相邻
5) clip_update patch={transitionIn:{id,duration}}
6) 验收：成片时长应 ≈ 素材内容和 - Σ转场时长；相等就说明转场没生效
```

判据：**成片变短才是真重叠**。`fade-black/fade-white` 是例外——它们走「前段淡出+后段淡入」
各占一半、**不缩短时间线**，不需要余量；适合明场/暗场转场（如"现实→电视世界"的段落切换）。
`wipe-*` 是 shape 型扫过，同样建议配余量。

`clip_add` 单轨会自动吸附到最近空位（`nearest_free_start`），同轨重叠被禁止；
`clips_move` 只能移到空闲位置，别指望用它压掉 0.6s 间隙——**用 ripple 收边**才是正解。

## 环境事实（2026-10-19 实测）

- 本机二进制：`~/.local/bin/concat-mcp`（main@0.2.8 自编译，release，54MB）。
  官方 0.2.7 dmg 的 `concat` **没有** `--mcp` 入口（该功能 10-18 才进 main）；
  官方发布 ≥0.2.8 dmg 后可换回：`<App>/Contents/MacOS/concat --mcp headless`。
- 端到端验收样例：`~/concat-demo/`（工程 Proj、成片 final2.mp4、对比图与 e2e 脚本）。
- 真实项目实战：`~/Code/kTool/example-project/交付/ep01_cut/`（《角色D与咕角色C嘎》EP01 17 镜套剪，
  65.17s 素材 → 58.8s 成片，16 处转场真重叠；`build_v9.py` 是可直接复用的装配脚本）。
- 42 个工具的完整清单与参数：会话内 `tools/list` 现取现用，勿凭记忆猜参数名。

## AI 生成素材的接缝工作流（2026-11-03 实测，30s 一镜到底复刻）

两段 AI 独立生成的视频拼接，拼接帧处必然存在「纹理噪声 + 光流场模式」双重突变——
叠化、硬拼、变速都只能缓解不能根治。本轮四种实施的实测结论：

| 实施 | 实测观感 | 适用 |
|---|---|---|
| crossfade 0.4–0.5s（**有人物帧**） | 人物半透明重影（双重曝光）=转场特效感 | ❌ 人物帧禁用 |
| crossfade（**全屏色块帧**，红裙/纯色占满） | 无鬼影，不可见 | ✅ 唯一安全的叠化 |
| 硬拼 d=0（两侧≈同一画面） | 画面连续但「顿一下」 | 纹理突变仍在 |
| 硬拼 + 接缝后段变速压平 | 光流峰值可压平（9.8→5.9），重复帧微顿 | 缓解手段 |

**推论：长运动（飞出/坠落/穿越）内部绝不拆段**——本地容量档 15s 内优先压缩前段保一镜（节点 length 可到 3600f，但 16G 实测 362f 是安全上限）；
必须拆段时接缝只落在**全屏遮挡帧**或**全屏色块帧**上。

### 光流速率匹配工作流（接缝必修）

```python
# 接缝两侧各取 0.65s，LK 光流 + estimateAffinePartial2D 测每帧运动量 px/帧
# 比值 0.8–1.25 → 可硬拼；接缝后段有生成自带的加减速 → split+speed 压平
# 例：L03B 生成自带 0.75–1.2s 加速冲刺（4.6→9.8 px/帧），
#     clips_split 两刀 + clip_speed 0.6 → 曲线 4.3→2.8→1.9→1.7 单调缓减
```

### 实操坑（本轮踩过的）

- **`project_open` 自动载入 media bin**——同一文件重复 `media_import` 会分配新 id（m1→m5→m7…），
  旧 id 报 `That media is no longer in the bin`。用 open/import 响应里的 `createdId` 或 bin 现有 id。
- **编辑不 `project_save` 就退出 = 全部丢失**（含 clips_add_sequence/trim/speed）——headless 进程
  退出即崩失；先 save 再起 export。
- **`export_start` 的 job 随进程死**——`export_wait` 必须与 `export_start` 同一会话；进程 terminate
  后 `export_wait` 报 `no job: notFound`。
- **`preview_frame` 是接缝目检神器**——渲染前就能取拼接帧 PNG（image content block），
  配合逐帧 MAD 检测（`MAD>20 且 hcorr<0.9`=硬切）先验后导。
- **变速会改变 clip 时长**：`clip_speed` 后 `timeline_read` 核实总长与后续 clip 位置（自动 ripple）。
- 长片头段（26s）预拼建议直接 ffmpeg xfade（转场配方简单时），concat 专做需要精细
  split/speed/preview 的接缝试验——两者混用，各取所长。
