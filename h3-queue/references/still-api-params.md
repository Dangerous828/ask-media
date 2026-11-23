# 2.7 出图接口与参数透传

画布规则与出图章节统一见 §2「出图（Qwen Image 2.1）」。基础模型保持 `qwen_image_2.1_int8_convrot`。

**缺省值不在本文写死**：以渲染机实读为准——`h3q_img.py` 顶部常量（步数/CFG/LoRA 缺省）、`h3qc submit --help`、
MCP `h3_generate_image` schema 与部署覆盖键 `H3Q_IMAGE_*`。数值型实测依据见
[still-standard-tier](still-standard-tier-20261105.md)（2026-11-05 快照）。

| 入口 | 图片参数契约 |
|---|---|
| `h3q_img.py` | 缺省步数（文生图 / 带参考各一档）、缺省 CFG 与 LoRA 以脚本顶部常量为准（`STEPS_T2I` / `STEPS_REF` / `DEFAULT_CFG` / `DEFAULT_LORAS`）；`steps=0` 按是否带参考选择步数档；`--size` 指定真实采样画布，`--resolution 0` 按原参考尺寸编码并对齐 32；输出保留采样画幅，不自动中心裁切 |
| `h3q.py` / `h3qc.py` | image 分支透传 `cfg` / `negative` / `steps` / `loras` / `resolution` / `alpha`；保留数值 `seed=0`、`steps=0`、`resolution=0` |
| MCP `h3_generate_image` / `h3_generate_project_image` | schema 暴露并显式透传上述参数；cfg/steps/loras/resolution 的缺省由部署决定，以 MCP schema 与覆盖键实读为准。部署覆盖键为 `H3Q_IMAGE_CFG` / `H3Q_IMAGE_STEPS` / `H3Q_IMAGE_LORAS` / `H3Q_IMAGE_RESOLUTION`，尺寸由 `H3Q_IMAGE_SIZE` 指定 |

真实提交经队列；下面是一次**显式传参**示例（数值为 2026-11-23 实读示例，不是缺省声明）：

```bash
$PY -s $CLI submit --kind image \
  --prompt-file '<渲染机根目录>\prompts\s1.txt' \
  --out '<渲染机产物目录>\s1.png' --size 2k-9x16 \
  --cfg 3.5 --steps 0 --loras none --resolution 0 --seed 0 \
  --negative 'text, watermark, logo' \
  --label 'S1 定妆' --idem-key 's1-still-seed0'
```

`--alpha 1` 可输出 RGBA。自定义 LoRA 使用自己的推荐 steps/CFG，显式传入 `loras`；`--fast` 仅为兼容参数，由渲染器忽略。历史测量见 [基础模型实测记录](still-standard-tier-20261105.md)，记录中的耗时与画质结论仅适用于对应实验。


