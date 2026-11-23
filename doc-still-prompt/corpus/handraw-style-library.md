# 风格图鉴库-handraw-style-001

- 验证状态：**本地 Qwen 抽测 3 条通过**（2026-11-07，1344×768 / seed 42；出图证据仅本地验证，对比图未随公开版发布）；368 条全库未逐条测。当时通道条件已变更；现行缺省档以实现实读为准，见 `h3-queue` 出图章节（本条抽测时点为 `cfg=3.5`、`loras=none`）
- 来源：[yang0/handraw-style](https://github.com/yang0/handraw-style)（MIT + 署名要求，作者 yang0），主分支 `master`
- 取材方式：只取**文字**。图片仅用于观察与 OCR 核对，不入库、不搬运
- 用法定位：**选款菜单，不是写作规范**。它回答"想要哪一种画法"，不回答"这一帧怎么受光、怎么接触"

## 库的实际内容（实测数字，非宣传语）

| 库 | 条数 | 编号 | 每条带什么 |
|---|---|---|---|
| 画风 | **368** | `FA-001`…`FI-034`（九组 FA/FB/FC/FD/FE/FF/FG/FH/FI） | `reference`（人名或品牌）、`generation_name`（英文风格名）、`traits`（中文特征串，平均 59 字） |
| 图型 | **170** | `SC-024`/`IG-038`/`SB-071`/`IP-013`/`EC-024` | 中文排版提示词全文（独立 `.md`），可直接拼接 |
| 主题色 | **36** | `C-01`…`C-36`（六组） | 中英色名 + 一句情绪句 + 一行 `prompt_en` |

分布：FA 40 / FB 66 / FC 32 / FD 42 / FE 68 / FF 17 / FG 25 / FH 44 / FI 34。FI 组是**品牌与摄影师**而非手绘（Apple、MUJI、Vogue、Avedon、McCurry、王家卫、韦斯·安德森等）。

`traits` 可用度实测：**traits 为空 20 条、不足 25 字 123 条**，真正能当特征串用的 **225 条**。`FI-031`（淘宝电商图）、`FI-032`（iPhone 随手拍）的 traits 为 0 字。

## 图像文字的 OCR 实测边界（2026-11-07，619 张图，tesseract chi_sim+eng）

这条必须先看，它决定"能不能照抄图上的字"：

| 类别 | 张数 | 英文可读 | 中文可读 |
|---|---|---|---|
| 风格卡 `images/individual/**` | 404 | **161**（多为作者人名） | **12** |
| 排版卡 `images/layouts/**` | 173 | 14 | **142** |
| 色卡 `images/colors/**` | 42 | 29 | 33 |

- **风格卡上的中文特征几乎读不出来**（12/404）。图上只有"作者名 + 英文风格名"两行大字；中文特征串是 `styles.json` 里的字段，不在图上。想知道某条风格的特征，读 JSON，不要指望 OCR。
- **排版卡正相反**：中文提示词被烧进图里，放大 3 倍后 142/173 可读，抽到 657 条可用中文文案（如 `SB-001 规则网 等分的规整网格，画面大小一致`）。
- 作者名会被稳定误识：`Jean-Jacques Sempé` → `Jean-Jacques 3empe`。**人名不可作为逐字核对的依据**。

## 本地抽测（三条，真出图）

同一通道、同 seed、同尺寸，验证"把中文特征串转成英文可见关系"能否驱动画风。

### 1 · FA-003 极细钢笔城市小品（Sempé）

原 traits：`极细钢笔线、小人物大空间、大量留白、温柔法式都市幽默。`

实际英文（节选）：
```
drawn with an extremely fine steel-pen line that varies in weight and occasionally breaks
Two thirds of the sheet stays untouched white paper
black ink, one pale silver-grey wash and a single warm red accent confined to the scarf
```

出图结果：**通过**。细钢笔线、路灯光影、右侧建筑只留淡灰晕与竖向窗线、整张纸留白约三分之二、红围巾是唯一暖色点——四项特征全部落实，人物确实"小"。没有出现照片感或厚涂。

教训（指向具体句子）：
- `Two thirds of the sheet stays untouched white paper` 是留白真正起作用的句子。只写 `大量留白`/`much negative space` 不告诉模型"多大比例"，这一条直接给占比。
- `a single warm red accent confined to the scarf` 把"少量点色"落到位。**本案中把点色绑到唯一承载物后，模型才没在多处撒色**——不绑定会怎样，本条没测。
- `varying in weight and occasionally breaks` 比 `fine line` 更像真实钢笔；只写 `fine` 容易得到均匀矢量线。

### 2 · FG-001 80 年代末赛博 OVA 赛璐珞（OscarAI）

原 traits：`80年代末日本黑暗赛博朋克OVA赛璐珞动画风、锐利手绘勾线、浓郁阴郁的丙烯手绘背景、高对比度硬光影、冷艳魅惑的女性肖像与黄金时代动画胶片质感。`

实际英文（节选）：
```
a flat pale cel tone with one hard-edged shadow plane down the centre of the face and neck; the shadow edge is completely crisp, no gradient
the background is hand-painted acrylic on board: dark teal and indigo, coarse brush texture
the wall never brighter than the lit side of her face
```

出图结果：**通过**。赛璐珞平涂、面部单块硬边阴影、锐利勾线、暗青底加笔触、黑发顶部细青边——都成立。背景压暗关系也守住了。

教训：
- `one hard-edged shadow plane … completely crisp, no gradient` 是赛璐珞与"3D 打光"的分界线。写 `cel shading` 单独不够，模型会加渐变。
- 本案里 `flat` 与 `hard-edged` 是成对用的：前者管色块，后者管边界。只用其一的效果未测。
- 上一行 `the wall never brighter than the lit side of her face` 用**两处表面的相对亮度**守住影调，比写 `low key` 有效——这与 `param-compare-gas-plate.md` 里"CFG 4.5 让画面变亮压不住 Low-key"是同一类问题的正向写法。

### 3 · FA-039 火柴人（手绘火柴人漫画）

原 traits 已写成规定（头身比、线条构成、五官形状），是全库少见的**可执行规格**。

实际英文（节选）：
```
a small circle head about one third of the body height, limbs and torso formed by single thin black lines meeting at simple angles
The posture reads through the tilt of the spine and the direction of the four limbs rather than through anatomy
Background is very low detail: one thin ground line and a single simple rectangle suggesting a doorway
```

出图结果：**通过**。真火柴人骨架、圆头占比约 1/3、四肢单线、点状眼加短线嘴、上身一块平涂青色、背景只有一条地平线和一扇门框、大片空纸。

教训：
- **比例写成数值（`about one third of the body height`）比形容"头偏小"可靠**。这是全库最值得借的写法。
- `rather than through anatomy` 这类"用 A 而不用 B"的正向对照，能让模型放弃解剖，效果比负向词稳。
- 背景那句 `one thin ground line and a single simple rectangle` 证明：**背景"极简"要写成几张具体的线**，写 `minimal background` 模型会自己加物件。

## 迁移到本技能写法时的取舍

1. **中文 traits 不能直接进英文正文**。它是选款依据；正文要按本技能 L1–L3 把它拆成可见关系（线型、色层、光影边界、留白占比、承载物）。上面三条抽测就是这三种拆法的样本。
2. **traits 里的负向片段要剔掉**。实测 368 条中 **56 条**含 `避免/不要/不准/禁止/不得/杜绝/不追求/不形成`（如 `避免统一的可爱微笑`）。这些不能进正文；要改写成"表情偏冷脸、尴尬或突然夸张"这类正向描述——这类句子在同一条 traits 里往往本来就有。确实需要压制的伪影走 `--negative`（本机 `cfg=3.5`、`loras=none`，负向槽有效）。
3. **人名当风格触发词是类比，不是事实**。`Jean-Jacques Sempé`、`Wong Kar-wai` 在正文里只能作为风格类比；本技能"器材与作者未经来源确认只写可见效果"仍适用。商用注意肖像/风格模仿的边界。
4. **同一主题换风格 = 换一条，不叠加**。库的设计就是单选；把两三条 traits 拼进一段正文会互相抵消（尤其 `超大留白` 撞 `密集排布`）。
5. **图型（SC/IG/SB/IP/EC）是另一层**，管构图与文字层级，不管画法。要出图文卡时先定图型再定风格；`SC-021` 属于"需要设计决策"的高维图型，不是模板直拼。

## 复用指引

- 定画风阶段：拿这份表当菜单给创作者挑编号；选中后取该条 `generation_name` + 正向 traits，按上面三条样本的拆法写成本项目正文。
- 想验证某条是否适合本地通道：先按 `p1/p2/p3` 的方式写 150–180 词英文，单张试出图；不要整库批量试。
- 与 `style-presets-micro-drama.md` 的分工：那份是**现成可粘的英文后缀**（影视器材向），这份是**选款菜单 + 拆法**（插画/摄影风格向）。两者都不要整串灌进 H3 视频正文。
