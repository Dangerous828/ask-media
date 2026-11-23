# 2.7 出图接口与参数透传

当前默认与画布规则统一见 §2「出图（Qwen Image 2.1）」。基础模型保持 `qwen_image_2.1_int8_convrot`。

| 入口 | 图片参数契约 |
|---|---|
| `h3q_img.py` | `STEPS_T2I=40` / `STEPS_REF=45` / `DEFAULT_CFG=3.5` / `DEFAULT_LORAS=none`；`steps=0` 按是否带参考选择步数；`--size` 指定真实采样画布，`--resolution 0` 按原参考尺寸编码并对齐 32；输出保留采样画幅，不自动中心裁切 |
| `h3q.py` / `h3qc.py` | image 分支透传 `cfg` / `negative` / `steps` / `loras` / `resolution` / `alpha`；保留数值 `seed=0`、`steps=0`、`resolution=0` |
| MCP `h3_generate_image` / `h3_generate_project_image` | schema 暴露并显式透传上述参数；缺省 `cfg=3.5` / `steps=0` / `loras=none` / `resolution=0`。部署覆盖键为 `H3Q_IMAGE_CFG` / `H3Q_IMAGE_STEPS` / `H3Q_IMAGE_LORAS` / `H3Q_IMAGE_RESOLUTION`，尺寸由 `H3Q_IMAGE_SIZE` 指定 |

真实提交经队列；例如：

```bash
$PY -s $CLI submit --kind image \
  --prompt-file '<渲染机根目录>\prompts\s1.txt' \
  --out '<渲染机产物目录>\s1.png' --size 2k-9x16 \
  --cfg 3.5 --steps 0 --loras none --resolution 0 --seed 0 \
  --negative 'text, watermark, logo' \
  --label 'S1 定妆' --idem-key 's1-still-seed0'
```

`--alpha 1` 可输出 RGBA。自定义 LoRA 使用自己的推荐 steps/CFG，显式传入 `loras`；`--fast` 仅为兼容参数，由渲染器忽略。历史测量见 [基础模型实测记录](still-standard-tier-20261105.md)，记录中的耗时与画质结论仅适用于对应实验。


