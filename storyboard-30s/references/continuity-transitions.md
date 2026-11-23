# 连镜与转场（镜头之间怎么"接"）

> 来源：经典剪辑教材公共知识（cut 语法 / 180° 轴线 / J-cut & L-cut）+ ostris 语料实测。
> 大佬材料只给了单镜内部的写法，本文件补"镜头与镜头之间"的规则。

## 一、剪辑点类型（按频率排序，H3 语料实测）

| 转场 | 语料词频 | 何时用 | 提示词写法 |
|---|---|---|---|
| 硬切 cut | 绝对主流（`the camera cuts to`） | 默认选择；信息切换 | At 00:03.000, the camera cuts to ... |
| 甩镜 whip pan | 23 | 快速转场/同场景换主体 | the camera whips right, motion-blurring the street into streaks before settling on ... |
| 叠化 dissolve | 2 | 时间流逝/梦境 | the image dissolves into ... |
| 划像 wipe | 17（多为雨刷/物体划过） | 复古或物体遮挡转场 | a passing truck wipes the frame, revealing ... |
| 淡入淡出 fade | 1 | 开场/收尾 | fade in from black / fade to black |
| 匹配剪辑 match cut | — | 形状/动作相似的跨场景 | match cut from the spinning coin to the rotating wheel |

**H3 官方规范**：默认用 `the camera cuts to / the shot cuts to / the shot transitions to /
the shot changes to / the shot switches to`；dissolve/fade/wipe 仅在用户明确要求时用。

## 二、遮挡转场（invisible cut 的穷人版）

前景物体扫过画面完成转场——纪实感最强的一类：
- 行人/车辆走过镜头前：`a pedestrian crosses in front of the lens; when he clears the frame, the scene has changed to ...`
- 电梯门/车门/卷帘门开合：`the shutter rolls down, and when it rises the shop is empty`
- 人物手掌/身体掠过：`her coat sweeps across the lens`

## 三、180° 轴线（the line）——对话戏不翻车的铁律

两个对话者之间画一条想象线，**摄影机始终在线的同一侧**：
- A 永远朝画面右看，B 永远朝画面左看 → 正反打才"接得上"
- 越轴（crossing the line）= 两人突然看向同方向，观众迷失
- 提示词写法：`A faces frame-right, B faces frame-left; both shots stay on the same side of the axis`
- 刻意越轴要写动机：`the camera crosses the line as she walks past him, reversing their screen positions to mark the power shift`

## 四、视线匹配 eye-line match

切到某人看向画外 → 下一镜必须是他看的东西，且方向匹配：
- 他看画面右上方 → 被看物体在画面左下方入画
- 写法：`he looks up and off-screen right; the next shot reveals the drone descending from the upper left of the frame`

## 五、J-cut / L-cut（声画错位）——对话戏的呼吸感

- **J-cut**：下一镜的声音先进来，画面后切（`her voice begins over the shot of the empty hallway before we cut to her`）
- **L-cut**：上一镜的声音延续到下一镜画面（`his laugh carries over into the shot of the door closing`）
- H3 是音视频同生模型，声画错位要写进 overall_soundscape 与镜头描述的时序里

## 六、连贯性 checklist（相邻两镜之间）

| # | 检查 | 说明 |
|---|---|---|
| 1 | 屏幕方向一致？ | 车从左往右开，下一镜不能从右往左（除非明确掉头） |
| 2 | 景别跨级有理由？ | 远景→特写中间最好有交代，或用动机（急推/甩镜） |
| 3 | 动作接动作 match-on-action？ | 上一镜起手、下一镜完成——剪辑点藏在动作里 |
| 4 | 光线/天气连续？ | 上一镜下雨这一镜地是干的 = 穿帮 |
| 5 | 服装道具连续？ | H3 官方指南明确要求 wardrobe/objects 跨镜一致 |
| 6 | 运镜方向不打架？ | 刚向左横移，下一镜别立刻向右（除非刻意对冲） |

## 七、语料启示（ostris 1000 条）

- 高频运镜动词：pushes in(118) > arcs around(94) > static shot(91) > handheld(89) >
  trucks left(70) > pans right(55) > zooms in(39) > tilts up(37) > tracking shot(33) > POV(29)
- `handheld` 出现 89 次——**纪实感的运镜首选**，比稳态运镜更像"真的发生过"
- `coverage` 出现 19 次：多机位覆盖思维（master + singles + insert）
