# 生图标准档实测：40 步 / CFG 3.5（2026-11-05）

> **状态（2026-11-07）：历史档记录，仅显式回退（`--loras none --steps 40 --cfg 3.5`）时参考。**
> 现行缺省档已换 Turbo LoRA 8 步 / CFG 1.0（创作者指令，见 SKILL.md §2.7）；现行档下
> `cfg=1` 无负向通道，排除项写正文正向，`--negative` 会被静默丢弃。

本机 win-desktop（RTX 5070 Ti 16GB），Qwen Image 2.1 `qwen_image_2.1_int8_convrot`，
ComfyUI 8199，无 LoRA。用于核对"标准档为什么是 40 步 / CFG 3.5"，
以及**CFG 与负向通道的关系**——这两件事常被分开谈，实际是同一件事。

## 一、A/B 实测（同 seed、同提示词）

提示词：红纸灯笼（`a red paper lantern ... visible paper fiber texture and bamboo rib structure`），
768×1344，seed 4242。

| 档 | 步数 | CFG | 耗时 | 画面 |
|---|---|---|---|---|
| A | 25 | 1.0 | 10.0 s | 纸面偏平、竹骨横向纹理糊、整体发灰 |
| **B** | **40** | **3.5** | **26.0 s** | 纸纤维颗粒、竹骨结构清晰、明暗过渡有层次 |

像素量化（同一提示词、同一 seed）：

| 指标 | A（25/1.0） | B（40/3.5） |
|---|---|---|
| 灯体区水平+垂直梯度 | 9.13 | **11.10（+22%）** |
| 全图平坦区占比（\|dx\|<1） | 0.590 | **0.467** |
| 全图亮度均值 | 31.1 | 37.7 |

结论：B 在纹理与层次上是可见增益，代价是约 **2.6 倍**耗时。

## 二、CFG 1.0 不是"保守"，是关掉了负向通道

渲染器原文（`h3q_img.py`）：

```python
"negative_prompt": negative if cfg > 1.0 else "",
```

也就是说：

- `cfg > 1`（现行标准档 3.5）：`--negative` 写进采样，负向槽**真实参与**。
- `cfg = 1`：negative 被**静默丢弃**，写什么都等于没写。

因此"CFG 1.0 但想靠 negative 排除文字/水印"这种组合不成立。要排除项，必须
`cfg > 1` 并且把清单交给 `--negative`；要极快，就用 `cfg 1.0` 并接受画面更平、
且不再有排除能力。

## 三、蒸馏（Turbo / 草稿）档已退役

`models/loras/qwen_image_2.1_turbo_lora_avg_rank_178_bf16.safetensors`（871 MB）与
`models/diffusion_models/qwen_image_2.1_turbo_int8_convrot.safetensors`（6.9 GB）
已移入 `E:\ComfyUI\_archived-turbo\`，**未删除**。

配套代码处理：`h3q_img.py` 不再定义 `TURBO_LORA` / `STEPS_FAST`，也不再自动挂 LoRA；
`--fast` 仍被 argparse 接受但**被忽略**（保留仅为兼容旧命令行，不因残留脚本报错）。
MCP `h3_generate_image` 的 `fast` 参数已移除。

⚠️ 退役时若只删权重而保留 `--fast` 的自动挂载逻辑，`fast=1` 会构造一个引用不存在
LoRA 的 graph，提交必然失败；且 `--fast 1` 与 `cfg 3.5` 组合本身也是矛盾的
（蒸馏档要求 CFG=1）。两处已一并清理。

## 四、原生 2K 与 RGBA

- **原生 2K 画布**：`2k-1x1=2048x2048`、`2k-3x4=1792x2400`、`2k-4x3=2400x1792`、
  `2k-2x3=1696x2528`、`2k-3x2=2528x1696`、`2k-9x16=1536x2752`、`2k-16x9=2752x1536`。
  模型按这些尺寸训练，细节来自真实推理而非放大；显存与耗时随之大涨。
- **RGBA 透明输出**：`--alpha 1` 把保存链路从 `SaveImage` 换成
  `SplitImageWithAlpha` → `SaveImageWithAlpha`（Qwen-Image-2.1 是 4 通道 VAE，但 `VAEDecode` 只吐 RGB，
  必须单独拆 alpha）。

  ⚠️ **别用"文件是 RGBA 模式"当验收依据**：ComfyUI 的 `SaveImage` 本来就写 RGBA PNG，
  只是 alpha 恒为 253–255（实测四种样张全部相同）。真正的差别在**节点**，
  以及内容里有没有可透明区域——用一张白底素材/贴图去验才有意义，
  普通满画幅静帧看起来会和不开时一模一样。

## 五、复现命令

```bash
# 标准档（默认）
python -s E:\H3-Studio\scripts\h3q_img.py --prompt-file P.txt --out O.png --size 768x1344

# 2K + 透明
python -s E:\H3-Studio\scripts\h3q_img.py --prompt-file P.txt --out O.png --size 2k-9x16 --alpha 1

# 排除项（需 cfg>1，默认 3.5 已满足）
python -s E:\H3-Studio\scripts\h3q_img.py --prompt-file P.txt --out O.png --negative 'text, watermark'
```

实测收尾：改后跑真实出图 `queued ... steps=40 lora=- ... saved ... 1491238 bytes in 27.1s`，
确认标准档生产链路正常。
