# 风格预设工具箱-Micro-Drama十式-001

- 验证状态：来源项目实际使用（示例项目按 anime 风格走完全流程）；本地通道未测
- 来源：[zhaihao118/Micro-Drama-Skills](https://github.com/zhaihao118/Micro-Drama-Skills) 的 visual_styles.json（上游仓库 `.config/` 目录下文件，未随本仓收录），作者将其注入 storyboard_config 与 AI 生成提示词
- 用法定位：**工具箱，不是规则**。每行是一个可选起笔词汇包，按项目挑选、按通道调整；没有任何一行是"必须"。

## 十套风格后缀（逐字保留）

| 风格 | prompt_suffix 原文 |
|---|---|
| 电影质感 | `shot on Panavision Sphero 65 and Hasselblad Lenses, Vision3 500T 5219, ND0.6, Diffusion Filter 1/4, cinematic film grain, shallow depth of field` |
| 经典动漫 | `anime style, cel shading, vibrant colors, soft glow, Studio Ghibli inspired, hand-drawn aesthetic` |
| 赛博朋克 | `shot on RED Monstro 8K VV, cyberpunk neon lighting, Pro Mist 1/4 filter, high contrast, teal and orange color grading, rain-soaked reflections` |
| 水墨国风 | `Chinese ink painting style, shuimo, traditional watercolor wash, flowing brushstrokes, muted earth tones with splashes of vermillion, misty atmosphere` |
| 韩剧氛围 | `shot on Sony VENICE 2, Korean drama aesthetic, warm soft lighting, shallow depth of field, golden hour glow, dreamy bokeh` |
| 暗黑悬疑 | `shot on ARRI ALEXA 65, Kodak Vision3 500T, dark thriller atmosphere, high contrast chiaroscuro lighting, desaturated colors` |
| 港风复古 | `shot on Kodak Vision3 500T, Cooke Anamorphic lens, vintage Hong Kong cinema style, warm tungsten lighting, film grain` |
| 武侠大片 | `shot on Panavision Millennium DXL2, Kodak Vision3 250D, wuxia martial arts epic, sweeping landscapes, dramatic overhead lighting` |
| 甜蜜恋爱 | `shot on Canon C500 Mark II, romantic soft focus, warm pastel tones, dreamy lens flare, cherry blossom petals, gentle backlight` |
| 纪实写实 | `shot on Sony FX6, documentary style, handheld camera, natural lighting, S-Cinetone color science, realistic skin tones` |

每行原始 JSON 还带 `camera / film_stock / filter / focal_length / aperture` 五个结构化字段（如电影质感 = Panavision Sphero 65 + Vision3 500T + ND0.6 + 65mm + f/2.0），方便换算成具体镜头语言而不是硬贴后缀。

## 为什么这是"正确吸收"的形态

上一轮从同一批仓库吸收时，产出了"禁用 XX""必须 YY"的硬约束。这个文件展示了另一种可能：**把风格知识做成可挑选的词汇表**——十行后缀每行都自洽（机型＋胶片＋滤镜＋观感词成套出现），挑一行是加法，不选也没有损失。

## 边界

- 后缀面向 Seedance/Gemini 时代的通道；本地 Qwen 未测，H3 视频正文另有方言（介质开场句），后缀只可取词汇不可整串粘贴。
- **千问正文不能用这里任何一行**：千问是段落体 caption 模型，逗号标签堆叠会退化成无主语的标签串；且赛博朋克那行的 `8K` 是官方明令禁止的质量词，会被画成画面里的文字。要给千问用，把想要的观感翻译成一两句完整句子（`a washed-out faded palette with a faint green cast`），不要贴后缀。
- 观感词部分（`dreamy bokeh`、`misty atmosphere`）是通用词汇；器材部分（`Vision3 500T`）在无真实拍摄时是风格类比，不是事实——与我们"器材未经来源确认只写可见效果"的写法相容：用作风格触发词可以，当作画面内事实陈述则不对。
- `Studio Ghibli inspired` 含作者名类比——商用注意 IP 边界。

## 复用指引

定画风阶段：把这表当菜单给创作者挑（或按题材推荐两三行）；选定后取该行词汇作为该项目的风格触发词起点，再按实际通道和已验收画风调整。换风格 = 换行，不叠加多行。
