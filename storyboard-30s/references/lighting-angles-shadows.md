# 打光角度与阴影语言（灯光的"几何学"）

> 来源：经典电影摄影教材体系（American Cinematographer Manual / Film Lighting: Talks with
> Hollywood's Cinematographers 一脉的公共知识）+ ostris 1000 条 H3 语料实际词频。
> 与 lighting-presets.md（8 组成套预设）的关系：那份是"套餐"，本份是"单点语法"——
> 预设不够用时，用这里的角度词 + 阴影词自己组。

## 一、光位角度（以被摄者为钟面，摄影机在 6 点钟）

| 角度名 | 位置 | 效果 | 提示词写法 |
|---|---|---|---|
| 顺光 front light | 摄影机同轴（6点） | 平、细节全、无立体感 | flat frontal light |
| 侧顺光 / 45° key | 4-5点或7-8点，俯角约45° | **伦勃朗位**：颊部三角光斑 | key light at 45 degrees, Rembrandt triangle on the cheek |
| 正侧光 90° | 3点或9点 | 半明半暗、分裂脸、强戏剧 | hard side light splitting the face, half in shadow |
| 侧逆光 | 1-2点或10-11点 | 发丝轮廓光、面部留暗 | rim light from behind-left, hair edge glowing |
| 逆光 backlight | 12点 | 剪影、雾中光束 | backlit silhouette, halo edge, light haze |
| 顶光 top light | 正上 | 眼窝深陷、审讯感/神圣感 | harsh overhead light, eye sockets in shadow |
| 底光 underlight | 正下 | 恐怖、非自然 | underlit from below, shadows climbing upward |
| 蝴蝶光 butterfly | 正前偏高 | 鼻下蝴蝶影、 Glamour | high frontal key, butterfly shadow under the nose |

## 二、光质（硬/软）——阴影边缘的语言

| 维度 | 硬光 hard | 软光 soft |
|---|---|---|
| 阴影边缘 | 锐利、边界清晰 | 渐变、羽化 |
| 质感 | 强调纹理/毛孔/灰尘 | 抚平皮肤 |
| 情绪 | 紧张、对峙、烈日 | 温柔、阴郁天、室内漫射 |
| 提示词 | hard light, crisp shadow edges | soft diffused light, gentle shadow gradient |
| 典型来源 | 直射太阳、裸灯、手电 | 阴天、窗纱、反光板、灯箱 |

**阴影浓度词**：deep shadow / crushed blacks（死黑）→ open shadow, lifted blacks（暗部有层次）→
shadowless flat light（无影）。大佬样例里"暗部保留层次"= open shadows with detail。

## 三、阴影作为构图元素（不是瑕疵，是工具）

| 手法 | 说明 | 提示词写法 |
|---|---|---|
| 剪影 silhouette | 主体只留轮廓，身份隐藏 | subject reduced to a black silhouette against the bright window |
| 图案阴影 | 百叶窗/格栅/植物投在脸或墙上 | venetian blind shadows striping across the face; lattice window shadow on the wall; dappled leaf shadows |
| 负空间阴影 | 大面积暗部承载"未知" | the left half of the frame falls into deep shadow |
| 投影叙事 | 影子先于人物入画/影子与本体动作错位 | the shadow on the wall reaches for the door before the hand does |
| 明暗对照 chiaroscuro | 卡拉瓦乔式强对比 | chiaroscuro lighting, single source, deep blacks |
| 低照度 low-key | 整体暗、单一亮区 | low-key lighting, one pool of light on the table |
| 高调 high-key | 整体亮、几乎无影 | high-key lighting, minimal shadows, bright even exposure |

## 四、光比（key:fill ratio）——量化"戏剧程度"

| 光比 | 观感 | 适用 |
|---|---|---|
| 1:1 | 无影、证件照 | 电商图（刻意避免） |
| 2:1–3:1 | 自然、日常 | 生活纪实 |
| 4:1–8:1 | 戏剧、noir | 悬疑、情绪人像 |
| 16:1+ | 剪影、极端 | 逆光、宗教感 |
写法：`key-to-fill ratio around 4:1, fill only lifting the shadow side slightly`。

## 五、动机光 motivated lighting（纪实感的命门）

**每一盏灯都必须"有来处"**：画面里或画面外要能指认光源实体——
窗、台灯、霓虹牌、屏幕、火、车灯、月光、货架顶灯管。
- 写法：`the only light source is the open fridge, cold white spilling across her face and the dark kitchen floor`
- 禁止：无来源的棚灯感（`studio lighting` 出现在纪实风里 = 出戏）
- 大佬样例锚点：PROMPT 10 的"a narrow beam of window light"——一束窗光，这就是动机光。

## 六、语料实测词频（ostris 1000 条，H3 模型"认识"的词）

灯光高频：silhouette(23+13) > sunlight(15) > backlight(14+8) > overcast light(10) >
moonlight(7) > firelight(6) > key light(3) > golden hour(3) > candlelight(2) > high-key(2)
阴影高频：shadow(s)(40) > silhouette(36) > shade(4) > venetian(5, 百叶窗影)
**启示**：H3 对 silhouette / backlight / overcast / venetian blind shadows 这类词响应最好，
生僻灯光术语（如 split lighting）建议配一句描述性解释，别只丢术语。

## 七、混色温（color temperature mix）——夜景的灵魂

单色温 = 干净但假；纪实夜景几乎总是**冷暖对冲**：
- 室内暖钨丝 2700-3200K vs 窗外蓝调 6500-10000K
- 钠灯橙 vs LED 白 vs 霓虹品红
- 写法：`warm tungsten interior at 3000K against cold blue window light at 7500K,
  the two colors meeting across her face`
- 大佬光影预设 6/8（蓝调城市夜景光、赛博朋克对比光）本质就是混色温套路。
