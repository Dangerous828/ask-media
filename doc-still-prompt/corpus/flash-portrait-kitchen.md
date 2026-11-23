# 真人摄影-厨房自拍闪光人像-001

- 验证状态：**通过**（纯文生图两轮后达成基本复刻）
- 通道：本地 h3q · Qwen Image 2.1，1088×1408，seed 42，cfg 4.5（r1 为 3.5），40 步标准档，无参考图
- 出图证据：仅本地验证，对比图未随公开版发布

## 原图观察

- 成像：随手快照质感，低照度细颗粒，画面边缘略软；肤色灰粉、低饱和，脸胸有中间调
- 机位：明显俯视——可见发髻头顶、肩胸上表面、裙摆下的大腿；前景台面切过底边
- 光：正面直闪，鼻梁/奶油/钢丝局部强高光，光迅速衰减进暗棕灰背景
- 关键道具投影：握柄手从画面左上边缘进入，手柄与钢丝向右下斜伸，奶油丝球悬在胸前、下巴左下方（**不是**脸旁）
- 人物：黑色高盘发、齐刘海、黑叶形发夹金椭圆；灰缎吊带裙黑蕾丝边、心形链坠；左脸颊与左胸有奶油

## 实际英文（r2 提交原文）

```text
A raw amateur snapshot with a smartphone-like look in a vertical three-by-four frame: a steep close high-angle view looking down over the top of her messy bun and her shoulders, her tilted-up face and hair crowding the upper frame, her foreshortened forearms, dress and upper thighs pressed toward the lens above the counter that cuts across the bottom edge.

The young East Asian woman leans far forward over the counter toward the camera. Glossy black hair is gathered into a high slightly messy bun with straight bangs and long side locks; a black leaf-shaped clip with a small gold oval sits above her left ear. Her large dark brown eyes look straight into the lens, double eyelids, a soft lower-lid highlight, long lashes; her skin is smooth and softly rendered in muted grey-pink tones, pink blush on her cheeks, glossy pink-red closed lips. White cream smears her left cheek beside the mouth and the upper left of her chest.

She wears a grey satin slip dress with thin spaghetti straps, a deep neckline edged in black lace and a short body-hugging skirt; subdued highlights follow the horizontal and diagonal folds of the grey fabric, and a thin dark chain with a small heart pendant rests on her collarbone. Her right hand enters from the upper-left corner of the frame gripping the black handle of a metal balloon whisk with steel wire loops; the whisk slopes diagonally down and to the right to a cream-coated wire head suspended in front of her chest, below and to the viewer's left of her chin. Her left hand lies flat on the pale speckled counter at the lower right, fingers spread, taking her weight.

The kitchen behind her is dim: a red stand mixer with a red-and-white striped bowl on the left counter, a black night window with white mullions, a stainless sink and faucet behind her shoulder, bottles and a blue-and-white carton on the right counter, a bag of flour and a clear container of white powder cropped at the lower left. Direct on-camera flash flattens her face and chest into bright planes with hard specular points on her nose, lips, the cream and the steel wires; the light falls off hard into the dark brown-grey room behind her. Fine low-light grain and a faint haze soften the whole frame, the shot feels casual and unpolished, edges slightly soft.
```

## 出图结果（r2）

俯角、发顶/肩胸上表面、近前景压迫感、暗厨房、灰粉中间调、细颗粒、打蛋器左上入画斜向右下、丝球位置、左手撑台——全部成立。剩余差异：背景整体略亮于原图、厨房物件稍多入画、颗粒略弱。

## 教训

**起作用的句子（有出图证据）**：

- `a steep close high-angle view looking down over the top of her messy bun` — r1 写 `just above her eye level` 时出图机位平；改成显式"看发顶"后 r2 俯角成立。**陡峭程度要用可见证据（看得见头顶）承载，不用模糊角度词**。
- `the whisk slopes diagonally down and to the right to a cream-coated wire head suspended in front of her chest, below and to the viewer's left of her chin` — r1 写 `beside her face` 时出图打蛋器举到脸旁；写全斜向路径+终点相对下巴的位置后成立。**决定构图的前景道具必须写完整几何路径，不用笼统方位**。
- `muted grey-pink tones` + `subdued highlights` — r1 写 `bright, slightly overexposed planes` + `broad wet sheen` 时出图过亮过润；换成中间调+局部高光后影调对上。**先定最亮最暗锚点，局部高光不得放大为整体状态**。
- cfg 3.5→4.5 对正文跟随度有可见提升（同 seed 同正文对比），但这是单次观察，不是定律。代价是构图服从度下降，出图后要核构图锚点。本条实测时点的缺省档即 `cfg=3.5`、`loras=none`（现行缺省以实现实读为准，见 `h3-queue` 出图章节）。

**r1 的错误归因**：

- 机位角度写浅 → 陷阱"机位角度写浅"
- 整体过曝+湿亮 → 陷阱"影调写偏"
- `shot on a phone`、`beauty-filter finish` 是无证据设备断言 → 改成 `smartphone-like look`（类比而非事实）

## 复用指引

写"暗环境+直闪+近距自拍/俯拍人像"类纯文生图时，本条目正文可作为句式骨架直接改造：保留斜向道具路径句、俯视投影句、中间调影调句的结构，替换具体人物/场景事实。
