# 连贯画面正文

本文件用于把已确定的本帧事实写成模型能读的画面。项目事实以剧本、分镜、权威身份、已接受参考和创作者决定为准。以下示例只说明写法，不是项目帧稿或已验证的生成配方。

## 成文与摘录

1. 先在账本和裁决确定人数、区域、身份、状态、机位、身体、头部与视线目标。区分本帧必要可见事实、不可见项和生产备注。
2. 找到本帧的核心关系，例如“驾驶者隔着车窗看价格牌”。用这条关系连起主体、目标和空间，再沿接触、受光与材质展开。同一对象的姿态、衣料和高光可共处一句。
3. 保留所选权威身份原文，写出其余画面。句子可以长短交替，也可以换主语；每次转向另一对象时，读者应知道它与前文的联系。简单的相邻、遮挡、承托关系可直接写，无须每句都加 because 或 so。
4. 当前条目需要英文证据锚点时，从成文中摘取 camera_en、body_en、head_en、gaze_en 的连续短语。保留足够的对象与方向信息，避免仅摘 `turned` 或 `to the left`。同一句可以提供多个字段的证据；不可见头眼按真实范围记不适用，不补画。
5. 忠实译成中文，再回查事实覆盖。必要事实漏了就修画面关系；排除项、后期用途、未来动作和跨镜持续要求各留在其说明中。
6. 沿用当前 IMG/SHOT 正式条目的同一正文，不因使用本页另建平行稿。frame role、镜内时刻、七项中文镜头字段属于说明层；正文表达其中本帧可见的取景和瞬间状态。composition 可在声明的镜内瞬间，只有作为 first_frame 的 start 对应0s；pose_proof 与 end 各守自己的时刻。

完成判据：单独读英文能定位谁在做什么、看哪里、谁与谁接触、重要物件在哪及如何受光；回看审计又能逐项指出证据。成文不承担保证扩散模型精确执行的职责。

## 把生产要求落实为可见结果

| 审计或制作说明中的要求 | 英文正文表达什么 | 核对边界 |
|---|---|---|
| 牌面留给后期贴价格 | 牌面当前的颜色、空白面、边框与分隔结构，例如 `a pale, unlettered price panel within a dark metal border`。 | “后期贴字”留在制作说明；当前确为无字面才能写 unlettered。 |
| 本场加油机恒在画右 | 本机位中加油机相对车窗、人物或立柱的位置与可见范围。 | “恒在”是跨镜纪律；换机位后重新投影屏幕方向，不能照搬上一镜左右。 |
| 牌面恰好三道带 | 保留三块的数量事实，并写上下边界、分隔线、宽高与间距。 | 数量与比例服从实际设定；不能把“等高”“等距”当默认值，也不能声称几何保证计数。 |
| 门洞在画框外 | 当前镜头实际朝向及画面被什么填满；已有空间支持时可写沙发后连续的墙面。 | 相机背对门、墙为白色等都须有依据。画外门的位置可留在裁决，不反复把门名写入正文。 |
| 屏幕不要太亮 | 屏幕与主体受光部位的相对亮度、亮区落点，例如 `the screen sits two stops below his lit jaw`。 | 档差来自已定光比或明确的设计选择；同一帧所有亮度关系要一致。 |

这些是表达转换，不是禁词表。`three`、`frame left`、`off-screen` 可准确表达数量、相对位置或视线目标；它们须有本帧依据，并与空间关系共同工作。画面反复不执行时，核对完整输入、参考机位与实际输出，再判断是否需要调整方案。

三等分牌面的几何片段，**仅在已接受设计为等高等宽、细横隔条时适用**：

```text
The tall rectangular panel holds three equally wide, equally tall pale fields stacked vertically; two narrow dark crossbars span the panel from border to border at one-third and two-thirds of its height.
```

若设计不等分，按实际结构写比例。关键数字、文字与精确分栏仍需看实际出图验收。

## 连贯片段与证据摘录

**示例事实**：静帧取自副驾驶座、驾驶者右侧平视；人物坐在驾驶位，躯干朝前，头转向左窗，目光落在窗外价格牌；左前方顶棚灯照下颌，屏幕低两档。示例暂用 `the driver` 作已知主体指代；正式帧稿须先引用项目所选的权威身份原文。本段仅演示关系连接，不是完整四段交付物。

```text
From the passenger seat at the driver's eye level, the view catches the driver seated with his torso facing the windshield, his head turned toward the left window and his eyes fixed on the price panel outside it. Cold canopy light enters from the front left through that window and catches his jaw, while the dashboard screen sits two stops below his lit jaw. Across the same pool of light, his grey knit sweater breaks the glow into a soft, uneven texture and the vinyl steering-wheel rim carries a narrow reflection.
```

中文译文：从副驾驶座、与驾驶者眼睛同高的位置看过去，驾驶者坐在座位上，躯干朝向前挡风玻璃，头转向左侧车窗，目光落在窗外的价格牌上。冷色顶棚灯光从左前方穿过车窗，照到他的下颌；仪表台屏幕比受光的下颌低两档。同一片光落在灰色针织毛衣上，被织纹打散成柔和、不均匀的表面亮度，乙烯基方向盘圈则留下一道窄反光。

裁决中的证据摘录可写为：

```text
camera_en：From the passenger seat at the driver's eye level
body_en：the driver seated with his torso facing the windshield
head_en：his head turned toward the left window
gaze_en：his eyes fixed on the price panel outside it
```

四个锚点都来自成文；第一句话同时交代机位、坐姿、身体、头部与视线，第二、三句沿同一束光连接下颌、屏幕、毛衣和方向盘。这里的成文质量由关系是否清楚判断，不由句长、主语数或某个连接词判断。

## 分支中的关系成文

以下是局部写法示例，身份与机位均假定已由项目给定。数字、光比和表面细节只在有作用时加入，不构成配额。

**3D 玩具角色持杯**：手与杯沿接触，材质差异跟着同一动作写；玩具表面不补皮肤SSS或发丝。

```text
The small painted figure cups the handle against its rounded palm, its other hand supporting the base. Light from the doorway stretches a broad reflection over the glazed cup and a smaller, duller patch across the figure's painted wrist.
```

**2D 硬边赛璐璐人物看屏幕**：表演由头眼与色块承担，屏幕可以是亮区，不为脸最亮改曝光。

```text
In a cel-shaded frame, she leans toward the screen, her head lowered and her eyes fixed on the pale symbol at its center. A hard-edged blue shadow divides the sleeve at her bent elbow; the screen's light color field stands clear against the darker desk.
```

2D水彩或厚涂可选柔边与渐变，不能把该示例的硬边推广成全部二维规则。画面需要多人/证据同时可读时选择相应清晰范围，平面化构图也不必补三层景深。

## 读稿时查什么

- 遮住账本，只读英文：能否画出核心空间关系？有没有漏掉本帧必要事实？
- 看相邻句：换主语时有没有空间、动作、接触或受光联系？是否把无关履历、后期用途写成画面？
- 看重复：身份、姿态和构图是否为不同核对项反复写了同一个事实？
- 看细节：每种材质和表情是否属于当前景别可读的内容？数字是否有来源或明确设计依据？
- 看摘录：四个字段是否真在提交正文中，且足以证明各自事实？改稿后是否同步？

将问题修回对应的关系，不靠加强语气、重复方位或再加一层清单收尾。
