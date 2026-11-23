# 六宫格配置驱动分镜-灯火之城EP01-001

- 验证状态：来源项目实际产物（DM-001 完整跑完 25 集，含分镜图、角色图与成片提交）；本地通道未测
- 来源：[zhaihao118/Micro-Drama-Skills](https://github.com/zhaihao118/Micro-Drama-Skills) `projects/DM-001_dhgt/episodes/EP01/storyboard_config.json`，目标通道 Seedance（图片走 Gemini API）
- 形态：**一个真实运行过的"配置→提示词"工作流案例**，不是规范

## 这套流程长什么样（EP01 真实数据）

**氛围块**（集级，中文，人读）：
```json
"atmosphere": {
  "overall_mood": "神秘而温暖的奇幻世界初印象，暖色调灯火与冷色调夜空形成对比",
  "color_palette": ["#F5A623", "#2C3E50", "#E67E22"],
  "lighting": "夜晚，灯塔和心灯发出的暖橙色光芒照亮周围，背景是深蓝色星空",
  "weather": "晴朗夜晚，微风"
}
```

**整集视频 prompt**（一段英文，机器读，逐字保留）：
```text
Anime style, night scene of a fantastical lantern city built around towering lighthouses. Warm orange glowing orbs float near every person's chest. A young girl with long brown hair in a low ponytail walks through cobblestone streets, her amber eyes reflecting the countless lights. She enters a lighthouse workshop filled with glass jars containing flickering lantern flames. She carefully holds a dim, almost extinguished heart lantern in her hands, her expression gentle and focused. Warm golden lighting from lanterns contrasts with deep blue night sky. Studio Ghibli inspired, detailed backgrounds, no subtitles, cinematic camera movements.
```

**六宫格之一（第 1 格，0.0–2.5s）**——中文场景描述给分镜图，英文 ai_image_prompt 给生图模型：
```json
{
  "grid_number": 1, "time_start": 0.0, "time_end": 2.5,
  "scene_description": "灯塔城全景俯瞰。夜空下，数十座灯塔矗立在错落有致的城镇中，每座灯塔顶部散发温暖的橙色光芒。街道上行人心灯闪烁，如地上的星河。",
  "camera": {"type": "远景", "movement": "缓慢下推", "angle": "俯视渐变为平视"},
  "ai_image_prompt": "anime wide shot, fantastical city at night with dozens of tall lighthouses glowing warm orange, cobblestone streets below with tiny figures each having a floating glowing orb near their chest, deep blue starry sky, Studio Ghibli style, warm color palette, cinematic composition"
}
```

另有 `bgm`（mood 描述＋风格关键词）、`connection`（与上/下集的钩子）、每格 `sfx` 与 `dialogue`。

## 值得吸收的写法（观察到，非规则）

- **双色账本**：氛围块中文给人读（含色板十六进制值），prompt 英文给模型——和我们的中文账本＋英文正文同构；色板 hex 是它没有的：三个具体色值比"暖色调"更能锁配色。
- **集级一段式视频 prompt**：整集 15 秒写成一个段落，靠场景推进（走进城→进工坊→持灯特写）而不是时间码切分——与我们 MOTION 逐镜正文是两个粒度，适合整段氛围戏；动作精确交接仍需逐镜。
- **逐格 ai_image_prompt 是场景级短句**（`anime wide shot, …, cinematic composition`），每格自带景别＋主体＋环境＋风格四件，不用引用其他格——六宫格分镜图各自独立可生成。
- `no subtitles` 写进正文尾部——Seedance 通道的实用写法（该案例条件下成立）。

## 边界

- 目标通道 Seedance＋Gemini 生图；本地 H3 走六段方言、本地 Qwen 走英文四层契约，此案例的格式**不可照搬**，吸收的是结构思路。
- 25 集×30 秒的工业量产定位，与我们的单镜精修定位不同；批量出片优先时可参考它，逐镜验收时用我们的链路。
- 每格 2.5 秒等分——那是它的节奏选择，不是通用规律。

## 复用指引

做"批量分镜图＋整段氛围视频"类任务时参考此结构：氛围块（含色板 hex）→ 集级一段式 prompt → 六宫格逐格独立短 prompt。需要精确动作/台词卡点时回到我们的 MOTION 逐镜链路，两套按镜头性质混用。
