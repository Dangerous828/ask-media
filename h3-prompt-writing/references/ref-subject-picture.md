# Ref2VA 的 Subject / Picture 分工与挂图纪律

混合参考（多图、身份板、场景板、分镜板）写错标签时读本文。六段字段与 retention 语法仍以 [ref-en.txt](ref-en.txt) 为准；本文只补官方分工、能力上限与本地实测边界。

## 0. 先分清这两个标签在管什么（本节是判据，不是格式）

两个标签问的是**两个不同问题**，答错一个就必然乱用：

| 标签 | 它回答的问题 | 它管的是 |
|---|---|---|
| `<Subject N>` | **画面里要出现什么东西** | 可见内容本身：人、动物、物体、场景/环境、服装、道具、界面、特效、风格、动作、表情、姿势 |
| `<Picture N>` | **哪张图直接充当某个时刻的画面** | 那张图自己就是首帧／关键帧／尾帧／编辑后关键帧／构图锚，或整段的分镜规划板 |

一句话判据：**图是"素材来源"还是"画面本体"。**

- 图只用来告诉我们"这个人长什么样／这个地方什么布局／这个风格什么味道"——**素材来源，走 `<Subject N>`**，图在 Subject 定义句里当来源被引用。
- 图本身就是第 0 秒、就是某一刻的构图、就是结尾那张——**画面本体，才建独立 `<Picture N>`**。

官方原文（ref-en.txt:68）把这条写成反规则：

> If an image is used only to define a character, scene, costume, or style, do not create a standalone picture entry. Instead, cite the image source inside the corresponding `<Subject N>` definition.

**所以身份板永远不进 Picture。** 它是"这个人长什么样"的素材，不是任何一帧的画面。把它写成 `<Picture 2> is the three-view character sheet that fixes …` 就是把它当成了画面本体——模型会理解成"第 2 秒附近该出现一张三视图板"，于是画面里长出板子、或人物被替换成板上的样子。

同理：场景板、风格图、道具参考板——只要它自己不是某一帧，都走 Subject。

### 一个 Subject 可以吃多张图，不必拆成多个标签

官方原文（ref-en.txt:48）：*One subject may be defined by multiple reference assets, and one reference asset may provide multiple subjects.*

正／侧／背／表情多格身份板，是**同一个人的多个来源**，合并成一句；不是"三个人"。拆成多个独立 Picture 的后果是模型当成多个实体（多出人，或某角色整段消失）。

```text
<Subject 2> is the fluffy white Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>, with thick white fur, pointed ears, a dark nose, and a curved tail.
```

注意这个官方示例里 `<Picture 2..4>` **全部被吸收进 Subject 定义**，`subject_definitions` 里没有任何独立 Picture 行——和上面那条反规则完全一致。

### 编号不必连续，只按类内出现顺序

`<Video N>` 与 `<Audio N>` 各自独立编号，不跨类配对（ref-en.txt:110）。`<Subject N>`／`<Picture N>` 同理：**编号只表示这一类里第几个，不表示时间顺序、不要求连续、不要求张数对等**。

不要为了"凑连续"把身份板硬塞成 Picture 来填空——那是本末倒置。有多少真帧锚就写几个 Picture。

## 能力上限（官方模型文档）

| 输入 | 上限 |
|---|---|
| 图像 | **≤ 9 张** |
| 视频 | ≤ 3 段，每段 2–15s，总长 ≤ 15s |
| 音频 | ≤ 3 段，必须与图/视频同用，不能单独作输入 |
| 混合输入文件总数 | **≤ 12 个** |

本地 `lib_workflow.py::build_ref2va` 用 `ref_images.ref_image_%d` 循环建槽位，**入口侧不设数量上限**。因此「挂三张以上就崩」是写法与素材问题，不是能力天花板；遇到崩先查本文第 3 节，不要先减图。

**入口上限 vs 实践上限（两层，别混）**：上表是官方模型的硬能力上限，入口侧又不对张数设卡；但**同框身份图 ≤2 张是本项目实践出的可操作上限**（§3 与 §5.3），目的是避免多张独立身份图把模型带成"多出人/角色消失"。这不是模型硬上限，而是出片稳定的写法纪律：第 3 个起的角色用冻结文字身份段，确需全部锁死就拆镜。入口允许挂更多张 ≠ 同框该挂更多张。

## 1. `<Subject N>` 管"可见内容"，可以引用多张图

官方原文：*One subject may be defined by multiple reference assets, and one reference asset may provide multiple subjects.*

多视图（正/侧/背/表情几格）就是同一个 Subject 的多个来源，**合并成一行**：

```text
<Subject 2> is the fluffy white Samoyed in <Picture 2>, <Picture 3>, and <Picture 4>, with thick white fur, pointed ears, a dark nose, and a curved tail.
```

## 2. `<Picture N>` 只留给五类席位

官方原文：*Use a standalone `<Picture N>` when the reference image itself serves as a shot's first frame, keyframe, last frame, edited keyframe, or composition anchor.*

反规则（同节）：*If an image is used only to define a character, scene, costume, or style, do not create a standalone picture entry. Instead, cite the image source inside the corresponding `<Subject N>` definition.*

分镜板有专属句式，必须写清「映射哪几镜 + 提供什么规划信息」：

```text
<Picture 3> is a storyboard reference for [Shot 1] and [Shot 2], defining their viewpoint, subject placement, and shot order.
```

正文里只在它起作用的那个镜头引用标签，不要只写在开头。

## 3. 三类常见写错的症状 → 改法

| 症状 | 常见错因 | 改法 |
|---|---|---|
| 多出一个人/动物，或某角色整段消失 | 把同一角色的多视图拆成多个独立 `<Picture N>`，模型当成多个实体；或同框挂了 3 张以上各自独立的身份图 | 多视图合并进一个 `<Subject N>`；同框身份图控在 2 张以内，其余角色写冻结的文字身份段；仍需要全锁死就拆镜生成 |
| 开场状态错、画面从"结果态"起 | 把身份板/场景板/结果态写成 `is the first frame`、`begins from <Picture N>`、`pose and expression fully_preserved` | 这类图只做身份/环境来源；要锁开场就提供真正起始帧，或写清"本镜起始状态"并删掉首帧措辞 |
| 画风/构图/光影被参考图带着跑 | 只写了"参考这张图"，没声明它捐什么、不捐什么 | 逐张写清保留维度，并套用下面的捐与不捐句式 |

官方"只捐身份"的措辞模板（可直接借用）：

```text
Use character reference image 1 only for identity mapping. The reference image donates identity anchors only:
recognizable face silhouette, hairstyle, relative facial proportions, and distinctive personal traits.
It does not donate photographic realism, skin texture, lighting, camera quality, or the original image style.
Do not swap identity with other characters.
```

## 3b. 身份靠图锁，不靠正文堆字

挂对身份板之后，正文**不要再把外貌特征逐句复述**。官方 ref-en.txt:246 的要求是：

> At the first clear appearance of an important `<Subject N>`, describe its referenced characteristics, position in the frame, and current action within what is actually visible in the shot. Continue using the same label in later shots without redefining what the label represents.

即：**首次清晰出现时提一次**（特征＋画面位置＋当前动作，且限于这一镜真看得见的部分），之后**只用标签，不重新定义**。

写四遍「深棕齐肩发、蓬松、散开披在肩上、未束起、自然垂落」这种堆叠，不是在锁身份——身份已经由身份板的像素锁住了，重复只会占用注意力、并在"模型要画背影"时跟它打架（实测：堆得越多，模型越容易把头发拢成一小揪，因为它把这段当成需要"执行"的动作）。**图已经给的东西，文字不再重复。**

对照写法：

```text
# 错：正文反复复述身份特征
At 00:01.000 <Subject 2>, the younger woman in the bright yellow knotted T-shirt and ripped denim shorts, enters ... Her dark chestnut shoulder-length hair is soft and voluminous, worn loose and down, falling freely over her shoulders, hair left untied and flowing.
At 00:04.200 ... the younger woman's dark chestnut shoulder-length hair soft and voluminous, worn loose and down, falling freely over her shoulders, hair left untied and flowing, its ends settling naturally down her back ...

# 对：首次出现提一次可见特征+位置+动作，之后只用标签
At 00:01.000 <Subject 2> enters from frame left, back to the lens, her yellow T-shirt filling the lower frame as she walks away down the lane.
At 00:04.200 the two women turn together and walk away, <Subject 2> on the left, both seen from behind.
```

## 4. 任务类型二选一，并在 retention 里注明

| 类型 | 含义 | 用于 |
|---|---|---|
| `keyframe completion` | 图当具体帧锚 | 首帧 / 关键帧 / 尾帧 / 编辑后关键帧 |
| `reference generation` | 图提供生成指导，不当具体帧 | 角色、场景、风格、动作、运镜、**分镜** |

## 5. 挂图清单（写词前逐项确认）

1. 每个角色只有一张身份卡；多视图在卡内，不拆图。
2. 身份图写进 `<Subject N>`，`<Picture N>` 只在它当帧或当分镜时出现。
3. 同框身份图 ≤ 2 张；第三角色起用文字身份段。
4. 分镜板当参考时写了映射镜头与规划信息；分格线、面板箭头等不得进入正文可复制范围。
5. 画风另给风格锚，不从身份图继承；光位写 `Lighting baseline`，不从身份图继承。
6. 文件名与 `<Picture N>` 顺序一一对应，上传顺序与正文标注一致（闸门 `--refs` 会核对张数与标注数）。
7. **剧情道具挂不挂，看它有没有手上动作。** 被递出、接住、抱住、打开、吃掉、换手或状态改变的，按 `<Subject N>` 挂一张道具板（形制/尺度/材质/当前状态）；只是摆着不动的布景道具退回场景卡地标，不单挂。
   - 道具板的职责只到"这件东西长什么样"，不控位置与构图——否则板上的居中陈列会被搬进画面。
   - 官方图像上限是 9 张，挂几张本身不是门槛；真正的互斥在**同框身份图 ≤2 张**（见清单第 3 条）和正文注意力分配。道具板进来时，优先压缩角色张数或让场景只做文字描述，别把"1 构图 + 3 角色"照抄一遍再加道具。
   - 本机实测（EP01 M05）：金橘在 10 秒里被递、被接、被抱住、抱着跑，四张预算给了 1 构图 + 3 角色，道具没有位子，只能靠正文写死"约十二厘米、饱满、橙皮"。成片成立，但那是一次走运的文字描述，**跨集复用没有像素锚点**——同一件道具在下一集要重现时，先补 plate 再写词。
