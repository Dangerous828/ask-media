# 转场卡：两镜之间插一段中间段 C

> 适用：A、B 两段已各自出片，同一空间、机位或站位有变，装不进同一次生成。
> 做法：取 A 的**真实末帧**做 `first_frame`、B 的**真实首帧**做 `last_frame`，走 FL2VA 生成 C；成片 A + C + B，接缝各去掉一帧重复。
> 判据（同一场景/同一光位/同一集合/一段连续运动能走完）与分流顺序见 `drama-skills/skills/short-drama-video-prompts/references/seam-transition.md` §0.4。本文只管怎么跑通。

## 一条命令跑完

```bash
python3 ~/.skills/hub/h3-queue/scripts/transcard.py \
  --before 剧集/EP0xx/制作成果/video/A.mp4 \
  --after  剧集/EP0xx/制作成果/video/B.mp4 \
  --prompt-file 脚本/transcard_107f.txt \
  --frames 107 --width 576 --height 992 --seed 42 \
  --label ep0xx-tc1 --out-dir 制作成果/_草稿/转场卡 \
  --assemble
```

脚本做的事：取真实边界帧（原始像素、不缩放）→ 跑 `h3_gate --mode base` → 传 ComfyUI `input/`（裸文件名）→ 提交默认分支 → 轮询 → scp 取回 → 量两端 MAD → 可选拼 A+C+B。

`--dry-run` 只取帧和过闸门，不提交；`--skip-gate` 跳过闸门。

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

拿同一镜头的真实中间段当 ground truth 逐帧比（EP002 SHOT-03 f120→f226 vs 生成的 107 帧）：

- 中段 MAD 中位 **23.9**，全片在 22–27 之间**平坦地高**，不单调从 A 走向 B，中间就切到一个新状态。
- 身份、发型、服装、巷子、光位都对；**表情与说话人不对**（原片 S1 笑着说话、S2 静听，生成的 C 里 S1 转头朝镜、S2 张嘴）。

所以：**转场卡保两端 + 中段身份与空间，不保中段的表情、说话人分配和动作路径**。要这几样就把 A→B 的动作拆进一次生成（multishot 或单镜加长），别指望中间段还原。

## 验收清单

1. 两端 MAD < 10（脚本输出）
2. 中段并排看：身份/服装/空间/光位一致（`seam_check.py` 或直接拼图）
3. 中段无台词口型错位、无字幕、无画内文字
4. 拼好后按 `seam_check.py` 量两条接缝的画质与亮度跳变；接缝处声音走声音桥（`seam-transition.md` §4.5 #20）
