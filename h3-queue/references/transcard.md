# 转场卡：两镜之间插一段中间段 C

> 适用：A、B 两段已各自出片，同一空间、机位或站位有变，装不进同一次生成。
> 做法：取 A 的**真实末帧**做 `first_frame`、B 的**真实首帧**做 `last_frame`，走 FL2VA 生成 C；成片 A + C + B，接缝各去掉一帧重复。
> 判据（同一场景/同一光位/同一集合/一段连续运动能走完）与分流顺序见 `../../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md` §0.4。本文只管怎么跑通。

## 一条命令跑完

**帧数约束**：必须是 `17k+5`，最小值就是网格最低档 5f。**107f（4.458s）是推荐值，不是技术下限**——它够装一段完整的过渡动作；短于它只告警不拦。2026-11-27 实测 22f(0.92s) 与 39f(1.63s) 两端 MAD 都 <10（22f 4.16/3.40；39f 4.34/3.62），五条整片 39f 的记录见 `incidents.md` §2026-11-27「EP005 五缝转场卡 39f」。短卡的代价不是锁不住，是装不下动作：词稿里只能写一次落座/收手这类一拍结束的位移，别写走位或多拍动作。

**两端帧的准入前提**：C 的首帧来自 A 的真实末帧、末帧来自 B 的真实首帧，两张都必须先过 look 准入
（measure → review → approve `--use reference`），脚本不替走。抽帧图要挂 `--derived-from <成片>`，
而**派生帧的父媒体必须先 approved**——所以 B 那一镜本身得先整段验收过；从没做过整段验收的镜
（典型是最末一镜）要先补 measure/review/approve，再回头批它的首帧，否则抽帧 approve 报
「父媒体未获批准」exit 2。

下面的 `剧集/…`、`脚本/…`、`制作成果/…` 都是**项目侧路径**（按项目根填），不是本仓文件。

```bash
python3 ../scripts/transcard.py \
  --before 剧集/EP0xx/制作成果/video/A.mp4 \
  --after  剧集/EP0xx/制作成果/video/B.mp4 \
  --prompt-file <项目>/脚本/transcard_107f.txt \
  --frames 107 --width 576 --height 992 --seed 42 \
  --label ep0xx-tc1 --out-dir 制作成果/_草稿/转场卡 \
  --assemble
```

脚本做的事：取真实边界帧（原始像素、不缩放）→ 跑 `h3_gate --mode base` → 传 ComfyUI `input/`（裸文件名）→ 提交默认分支 → 轮询 → scp 取回 → 量两端 MAD → 可选拼 A+C+B。

- **幂等**：`submit()` 自动带 `--idem-key`（由 label、seed、frames 与两端帧文件名哈希组成），脚本重跑 / 超时重投不会重复提交。符合三条硬纪律第 3 条。
- **闸门默认路径**：按部署配置的闸门脚本路径（本仓默认 `../../h3-video-gate/scripts/h3_gate.py`）；可用 `H3Q_GATE` 显式指定。**闸门脚本缺失时直接报错退出，不静默跳过**——要跳过只能显式传 `--skip-gate`。
- `--dry-run` 只取帧和过闸门，不提交；`--skip-gate` 跳过闸门。
- **拼 A+C+B 会重编码全片**：A、C、B 三段统一 libx264 crf16 + aac 192k 再 concat，A、B 作为已交付成片也经历一次有损往返；去掉重复首帧后加 `setpts=N/FRAME_RATE/TB` 重打时间戳，避免拼接处 1 帧间隙。要零损失需另走无重编码装配（以实际部署的剪辑链为准）。

## 分支：必须走默认分支，不能带 `--workflow`

| 分支 | 渲染器 | 首帧 | 首尾帧 | 说明 |
|---|---|---|---|---|
| 默认（不带 `--workflow`） | `h3_render_ref.py` | ✅ i2va | ✅ fl2va | **转场卡走这条** |
| `lu2` | `lu_render_ref.py` | ✅ | ✅ | 可选，两段式 |
| `spark` | `spark_render_ref.py` | ✅ | ✅ | 可选 |
| `pdd_lu` | `pdd_render_ref.py` | ❌ | ❌ | **草稿档**，渲染器没有首尾帧参数 |

`pdd_lu` 是 pdd 的 `tier=draft`，日常出片用它；但它做不了首尾帧——2026-11-22 实测同一对首尾帧、同 107f、同 seed 42：pdd_lu 产物首帧与指定首帧 MAD **43.0**，默认分支 **3.86**。所以转场卡不挂草稿档，走默认分支。

三个入口已按输入自动分流，带 `first_frame` 就不会落到 pdd_lu：`h3_generate_video`（MCP）、`short_drama_h3q_adapter`（项目 produce）、以及本脚本。

## 词稿：base 三段

C 是新增片段，用 base 三段（`integrated_multimodal_description` / `overall_soundscape` / `non_diegetic_music`），不写 `subject_definitions`。

只写 A 末态到 B 首态之间那一段连续运动，**不重写两端已有状态**；C 内不放台词（音频独立生成，两端都不连）。

## 项目内使用：两端帧要先过参考准入

项目活（short-drama-produce 那条路）的参考图**一律**要过 `short-drama-review` 的参考准入：`look_check.py assess` → `review` → `approve --use reference`。首帧和尾帧同样是参考图，**没有例外**——直接把它们塞给 adapter，`ref_gate` 会回 `reference_not_accepted`（2026-11-22 实测）。

所以项目内的顺序是：

1. 抽真实边界帧（`seam_check.py --extract <video> --frame last/first --to <png>`）
2. 两帧走 `look_check.py measure/assess` → `review` → `approve --use reference`
3. 再提交（adapter 或 `transcard.py` 都行）

`transcard.py` 是通道级工具，**不替你走过这道准入**——它不会拦你，但拿它绕过项目准入同样是违规。项目外的单次试验（不产出项目资产）才可以直接用它。

## 两端验收：量 MAD

脚本出片后自动量：C 首帧 vs 指定的 A 末帧、C 末帧 vs 指定的 B 首帧。**<10 视为锁住**（实测正常锁定在 3.7–3.9）。

不锁就是输入没进去——先确认提交时没带 `--workflow pdd_lu`、两帧传的是 `input/` 里的裸文件名。

## 中段能力边界（2026-11-22 实测）

**转场卡保两端 + 中段身份与空间，不保中段的表情、说话人分配和动作路径**；要这几样就把 A→B 的动作拆进一次生成（multishot 或单镜加长），别指望中间段还原。逐帧实测经过见 [incidents.md](incidents.md) §2026-11-22 转场卡中段。

## 验收清单

1. 两端 MAD < 10（脚本输出）
2. 中段并排看：身份/服装/空间/光位一致（`seam_check.py` 或直接拼图）
3. 中段无台词口型错位、无字幕、无画内文字
4. 拼好后按 `seam_check.py` 量两条接缝的画质与亮度跳变；接缝处声音走声音桥（`seam-transition.md` §4.5 #20）
