# 一场 6 镜戏的接缝方案（本地 h3q · MiniMax H3 · 竖屏）

这份示例回答"干净上下文的 agent 读完规范后，应该交出一份什么样的接缝方案"。
它**不是**一份完整的《视频提示词.md》，只演示一件事：把一场戏的每一个切点从
"是什么性质"推到最后写进正文的那一句英文。

> ⚠️ **这份示例的切点选法早于 2026-11-05 的七组实测，其中三处用到的手法后来被判为不可靠**
> （#9 match on action 两处、#3 前景擦除一处）。**示例仍然保留，是因为它的"推理格式"是对的——
> 每个切点写清性质、手法、通道、成本、时间账、声音。但手法选择要看 `../references/seam-transition.md` §一 的
> 实测优先级，不要照抄这里的 #9 与 #3。** 正确做法：能并进容器就并；必须拆段时用真实末帧接力。

对照：真实项目 `example-project`。同一个场景（深夜小馆、女子偷吃蛋糕被男友抓住），
6 镜、竖屏 768×1344、本地 h3q。那一轮的三对接缝实测：

| 接缝 | structure_mad | edge_agreement | 跳变倍率 | 实际是什么 |
|---|---|---|---|---|
| 001→002 | 1.7 | +0.93 | 1.2× | 接上了 |
| 002→003 | 40.4 | −0.02 | 31.3× | 分镜本来就要求从正面中近景**换成过肩俯视**，差值是设计结果 |
| 003→004 | 45.4 | −0.01 | 31.7× | 真断裂：背景从暖色室内变成窗外青蓝夜景，他的位置与高度全换 |

**这个对照最有用的地方不是"三刀里坏了两刀"，而是"同样 40+ 的数字，一刀是设计、一刀是事故"。**
本示例演示的就是怎么让每一刀都能说清自己属于哪一种。

规范来源：[段间接缝](../references/seam-transition.md)。任何一条与它冲突时以它为准。

---

## 零、开工前先写下来三件事

写第一句正文之前，先把这三行钉在文档开头。缺任何一行，后面的手法选择都是猜的。

```text
目标通道：本地 h3q · supported_generation_modes = first_frame / first_last_frame / reference
          无文生、无参考视频、无参考音频；音色不能跨段锁
画幅与帧网格：9:16 · 768×1344 · 17k+5 @24fps
可用手法：seam-transition.md §3 表中标 ✅ 的，加标 ⚠️ 的 3 种（第 7、17、18 条，各带条件）
不可用：#19 参考视频 —— 不写这种方案
有条件：#17 首帧接力、#18 首尾帧配对 —— 都要整段放弃 full-reference，见 seam-transition §4.4
```

**为什么必须先写**：这套档案是本示例所有手法选择的依据。能力会变（2026-11-05 通道补上了首尾帧，
第 18 条就从"不可用"改成"有条件"），所以每次写方案都要重读档案、重判表格，不要背上一轮的结论。
本场所以不用首尾帧：六个镜每一镜都绑着角色板与地点板，而首尾帧与 `reference_image` 互斥——
用了首尾帧就没有身份图，这一场的连续性是靠身份图撑的。

---

## 一、这 6 镜要分成几个生成单元

镜数不等于生成次数。先排单元，再排接缝。

| 单元 | 成员 | 时长 | 容器 | 依据 |
|---|---|---|---|---|
| **U1** | SHOT-01 她一个人偷吃 | 7s（175f） | 单镜 | 独立表演段，起止状态闭合 |
| **U2** | SHOT-02 奶油滴落 | 6s（吸附至 158f / 6.583s） | 独立生成 | 机位从三分之四改到近景，需要新构图参考 |
| **U3** | SHOT-03 他走到身后 + SHOT-04 她的手停在半空 | 4.2 + 3.2 = 7.4s（吸附至 192f / 8.000s） | **多镜容器** | 同场、同一绑定链、时间连续；两人关系只能在一个容器里建立 |
| **U4** | SHOT-05 窗玻璃反光里她看见他 | 6s（吸附至 158f / 6.583s） | 独立生成 | 换机位到正面特写 |
| **U5** | SHOT-06 她决定，按下叉子 | 5s（吸附至 124f / 5.167s） | 独立生成 | 收尾镜，独立终点 |

**U3 装容器的理由**：SHOT-03（他俯身说话）与 SHOT-04（她的反应）之间那一切，
必须让观众看见"他还在她耳边"和"她的手停在半空"同时成立。拆成两次独立生成，
两段的两人距离、光位、椅背位置会各漂一次，而这一刀正好是全片的转折点。

**容器内切点不需要遮挡**：同一次生成没有身份与空间漂移（见规范 §5）。写遮挡是浪费 0.5 秒。

---

## 二、逐个切点的方案

每个切点按固定的七项写。缺一项就等于没做设计。

### 切点 A：SHOT-01 → SHOT-02（同场换机位，只换景别）

| 项 | 内容 |
|---|---|
| 性质 | 同一段时间、同一空间，只换机位（三分之四中景 → 近景） |
| 手法 | **#9 match on action**（动作同帧换视角） |
| 通道 | ✅ 可用：两次独立生成 + 两段正文对到同一拍 |
| 成本层 | **L-A 写词**，零次生成 |
| 前段末状态 | 她把挖好的一大团奶油举到胸口高度，笑容还在 |
| 后段起状态 | 同一高度、同一团奶油、同一只手，笑还没收 |
| 新增信息 | 景别推近，看清奶油在叉尖上开始倾斜 |
| 不切的后果 | 观众看不出奶油是怎么开始滑落的 |
| 时间成本 | 0 秒（match on action 不占时长） |
| 声音 | 两段 `overall_soundscape` 共用同一句底声：`the low steady hum of the two lit pendant lamps above the table` |

前段正文末句（写在 SHOT-01 的 `detailed_description` 里）：

```text
At 00:06.000 she digs a much larger curl of cream, the tines loaded and the top of it already leaning,
and lifts it to chest height, still smiling into the empty room; she holds it at chest height at 00:07.100.
```

后段正文首句（写进 SHOT-02 的 `detailed_description`，从段首开始）：

```text
[Shot 1] Her right hand is already holding the short three-tined wooden-handled fork at chest height at 00:00.000,
the loaded curl of cream leaning off the tines, her smile still on her mouth; the cream keeps leaning and the peak stretches.
```

**注意这三件事，缺一个 match on action 就不成立**：
- 两段都写"胸口高度"，不写"举起中"或"已在嘴边"；
- 两段都写"同一只手、同一把叉"（三齿木柄），因为这是两段各自的参考图之外唯一能对上的东西；
- 两段的底声是同一句。

**核对**：生成 SHOT-02 之前，跑 §四的命令，确认并排图上"手的高度、叉的角度、笑的程度"三项一致。
不一致时改的是后段首句的相位，不是加过渡。

---

### 切点 B：SHOT-02 → SHOT-03（换机位 + 他从背后进入）

| 项 | 内容 |
|---|---|
| 性质 | 同场换机位，但多了一个新人物入画。**这是本项目真正出事的那一刀** |
| 手法 | **#16 插入镜 + #3 前景擦除**（两步，见下） |
| 通道 | ✅ 可用 |
| 成本层 | **L-A 写词**（插入镜单独生成一段，算一次生成） |
| 前段末状态 | 近景，她的脸与锁骨，白色奶油珠在皮肤上 |
| 后段起状态 | 过肩中景，画面右侧前景是他的肩与手臂 |
| 新增信息 | 有人在她身后；他的手落在椅背上 |
| 不切的后果 | 观众不知道他什么时候进来的，后面的"被抓"就没有重量 |
| 时间成本 | 插入镜自带 2s；后段不需要额外余量 |
| 声音 | 他的脚步先在插入镜里入画，\(J\)-cut 到后段 |

**为什么不能直接硬切过去**：SHOT-02 是正面近景（她的脸占满画面），SHOT-03 是她右后方的过肩
（她的侧脸只占左三分之一）。两段的机位轴、主体位置、背景层次全部不同，直接接会被读成
"换了个地方"，这正是事故现场发生的事——桌面、吊灯、道具、外套四样全变，观众没有任何线索
把这两个画面连成同一个房间。

**做法**：在两者之间插一个 2 秒的交代镜，把观众的眼睛从"她的脸"带到"这个房间"。

插入镜（第 16 条，单独一次生成，`L-C` 因为它是一次真实生成）：

```text
[Shot 1] A vertical 9:16 photoreal live-action insert of the white plate on the pale wooden table,
the cream crater and the single loose strawberry in the lower half of frame,
the wine-red silk cardigan hanging on the chair back at frame right, softly defocused;
the warm pendant lamp glows above and the pale wood grain stays visible for the whole shot.
```

插入镜同时交代了四件后面必须对上的东西：**白色盘子、浅木桌面、椅背上的酒红开衫、吊灯在上方**。
SHOT-03 的正文必须逐字复述这四件，观众才会把两段认成同一个房间。

SHOT-03 首句：

```text
[Shot 1] A vertical 9:16 photoreal live-action shot from behind and above her right side at standing height,
looking down about fifteen degrees; frame left holds her near profile with her shoulders drawn up,
frame right foreground holds his forearm and shoulder in a dark-grey pinstripe shirt with the sleeve rolled to mid-forearm,
and between them the same white plate on the same pale wooden table, the wine-red cardigan still hanging on the same chair back,
the warm pendant lamp still glowing from above.
```

**这四件"同一"必须写出来，不能指望模型记住**：`the same white plate` / `the same pale wooden table` /
`the same chair back` / `the warm pendant lamp still glowing from above`。
规范称之为"共享锚点，两边都要写"。只在一边写的锚点不成立。

**核对**：这对接缝的四项（同一个人 / 同一空间 / 同一造型 / 同一道具状态）在事故项目里全部不合格。
本题的防线是插入镜 + 四件逐字复述，核对的落点是：盘子的形状与凹坑、桌面木色、开衫颜色、
吊灯的相对位置。任一项对不上就重出 SHOT-03（L-C），不要往下走。

---

### 切点 C：SHOT-03 → SHOT-04（同容器内的换视角）

| 项 | 内容 |
|---|---|
| 性质 | 同一次生成内的切点（U3 容器） |
| 手法 | **#13 硬切**，切点带叙事动机（他的手按住椅背） |
| 通道 | ✅ 可用（`[Shot N] At MM:SS.mmm`） |
| 成本层 | **L-A 写词**（同一份正文里改） |
| 前三镜末状态 | 他的嘴贴在她耳边说话，她的肩胛锁紧 |
| 后镜起状态 | 她的侧脸特写，手停在半空 |
| 新增信息 | 她的反应（不是他的动作） |
| 不切的后果 | 观众听不到台词，只看他说话的背影 |
| 时间成本 | 0 秒（硬切不占时长） |
| 声音 | 共享同一条音轨；台词不跨切点 |

```text
[Shot 2] At 00:04.200, the shot cuts to a tight side angle on her face as his line ends,
her jaw tight, her knuckles pale on the fork handle and the fork stopped in mid-air at chest height.
```

**这里不需要遮挡，也不该有**。容器内共享同一次采样，身份与空间不会漂；
写一个 0.5 秒的遮挡只是白白吃掉她反应的半秒。

**容器内切点的唯一要求是动机**：`as his line ends` 就是动机——声音落点给了这一刀的理由。
写不出动机的切点应该并回上一镜。

**已知代价**：容器内不带关键帧的切点会偏 0.5–1 秒。所以这一切的证据落在台词结束，
而不是某个需要精确卡点的动作中间。

---

### 切点 D：SHOT-04 → SHOT-05（换机位到正面特写）

| 项 | 内容 |
|---|---|
| 性质 | 同场换机位，视线方向是关键 |
| 手法 | **#11 视线引导（eyeline match）** |
| 通道 | ✅ 可用 |
| 成本层 | **L-A 写词** |
| 前段末状态 | 她的眼睛向下，盯着盘子 |
| 后段起状态 | 她的眼睛已经抬到画左的玻璃反光上 |
| 新增信息 | 她在反光里看见了他 |
| 不切的后果 | 观众不知道她发现了他，后面的"决定"没有根据 |
| 时间成本 | 0 秒 |
| 声音 | 他的呼吸声在后段先入 0.3s（J-cut），剪辑层做 |

前段末句：

```text
From 00:02.800 to 00:03.200 her eyes stay down on the plate, her chin level, her lids low.
```

后段首句：

```text
[Shot 1] Her eyes are already lifted to the narrow vertical band of window glass at frame left at 00:00.000,
her chin still level, her pupils tracking the pale defocused shape of a man's half face in the reflection.
```

**必须两边都写视线落点**：前段写"眼睛向下看盘子"，后段写"眼睛已经在画左的玻璃上"。
只写一边，模型会自己决定她看哪里。

**失败迹象**：后段的目标在画右（反了）——这是越轴，观众会读成两个人在对视。
出片后如果发现反了，改的是后段的机位方向（`L-C`），不是措辞。

---

### 切点 E：SHOT-05 → SHOT-06（情绪转折，收尾）

| 项 | 内容 |
|---|---|
| 性质 | 同场、时间连续，情绪从恐惧转为决定 |
| 手法 | **#23 光线变化** + **#9 match on action** |
| 通道 | ✅ 可用 |
| 成本层 | **L-A 写词** |
| 前段末状态 | 她盯着反光里的他，嘴角开始上扬 |
| 后段起状态 | 同一个笑，但她已经在放下叉子 |
| 新增信息 | 她做了一个决定 |
| 不切的后果 | 从"看见"到"决定"之间没有可见的转折 |
| 时间成本 | 光线变化 **0.3–0.5s**，从 SHOT-06 的动作预算里扣 |
| 声音 | 叉子落在盘上的瓷响跨过切点（#28 声音匹配） |

前段末句：

```text
At 00:05.000 the corners of her eyes crease first, and at 00:05.500 one side of her mouth curves into a slow, certain smile
while her eyes stay locked on the reflection, the cool cyan rim from the glass moving slightly across her cheekbone.
```

后段首句（注意：**动作预算已经从 5s 扣掉 0.4s 过渡**）：

```text
[Shot 1] The same slow, certain smile is already on her mouth at 00:00.000.
At 00:00.300 the pendant lamp above the table flickers once and drops to a deep ember,
the whole room collapsing into one warm pool, then the filament catches and the light floods back at 00:00.700.
From 00:00.700 she sets the short three-tined wooden-handled fork down on the white plate,
the ceramic click landing at 00:01.400, her palm flat on the table by 00:02.200.
```

**时间账**：SHOT-06 是 5s，光线变化占 0.4s，剩下 4.6s 做"放下叉子 + 抬头"。
动作原本需要 5.2s 时，**不压动作**——改法是砍掉一个多余动作，或把这一镜加长到 6s（吸附至 158f / 6.583s）。
压动作会让模型赶词、把人手画成残影。

**注意事件含义**：这里要亮灯，所以写 `the filament catches and the light floods back`；若来源要求灯不再亮，就保留该边界。正向改写不能把已确认事件改成相反结果，G36也不要求消除所有否定。

---

## 三、这份方案的时间与声音总账

### 时间账

| 镜 | 时长 | 过渡占用 | 可表演时长 | 对白/动作装得下？ |
|---|---|---|---|---|
| SHOT-01 | 7.0s | 0 | 7.0s | 够（无对白，四个动作节拍） |
| SHOT-02 | 6.0s | 0 | 6.0s | 够（奶油滴落 2.6s + 反应 2.6s） |
| SHOT-03 | 4.2s（容器内） | 0 | 4.2s | 够（台词 6 字 ≈ 1.5s，剩 2.7s 表演） |
| SHOT-04 | 3.2s（容器内） | 0 | 3.2s | 够（纯反应，无台词） |
| SHOT-05 | 6.0s | 0 | 6.0s | 够 |
| SHOT-06 | 5.0s | 0.4s（光线） | 4.6s | **紧**：放下叉子 + 抬头 = 4.6s，正好；再加动作就要加到 6s |
| 插入镜 | 2.0s | 0 | 2.0s | 够（静物，只有一处光） |

**插入镜的 2 秒不是免费的**：它让这一场从 35.4s 变成 37.4s。写方案时这一句要交给创作者决定，
不能自己加。

### 声音账

| 接缝 | 声音手法 | 写在哪 |
|---|---|---|
| A | 共用底声（吊灯嗡鸣） | 两段 `overall_soundscape` 首句 |
| B | 他的脚步先入（J-cut） | 插入镜末句 + SHOT-03 首句 |
| C | 共享音轨，台词不跨切点 | 同一次生成，`<scenetrans>` 只在确实要跨时用 |
| D | 他的呼吸先入 0.3s（J-cut） | 剪辑层 |
| E | 叉子落盘的瓷响跨切点（#28） | 两段 `overall_soundscape` 用同一个 `ceramic click` |

**跨段对白绝不断开**：本场唯一的台词（`这么晚，偷吃？`）整句在 SHOT-03 的容器内，
不跨生成段。本地通道每段重新生成人声，跨段会换音色。

---

## 四、交稿前怎么核

对每一对相邻生成段（A、B、D、E 四处；C 在容器内部，不需要跨段核对）：

```bash
python3 <本技能目录>/scripts/seam_check.py \
  --before 剧集/EP001/制作成果/video/MOTION-EP001-001-draft.mp4 \
  --after  剧集/EP001/制作成果/video/MOTION-EP001-002-draft.mp4 \
  --out 审查/seam --label 001-to-002
```

然后**打开图，自己做完这四步**（脚本不判定）：

1. `<label>-side-by-side.jpg`：四行逐项看，写下具体特征；
2. `<label>-grid.jpg`：确认最大差异格与第 1 步的观察一致；
3. 回答"合理切镜还是接不上"；
4. 写进「接缝契约」表。

参考读数（同一批素材实测，仅作量级参照，**不是阈值**）：

| 关系 | structure_mad | edge_agreement | 跳变倍率（分母 = 段内单帧最大跳变） |
|---|---|---|---|
| 这一刀接上了（001→002） | 1.7 | +0.93 | **1.2×**（1.40） |
| 这一刀是设计好的换机位（002→003） | 40.4 | −0.02 | **31.3×**（1.29） |
| 这一刀换了空间（003→004） | 45.4 | −0.01 | **31.7×**（1.43） |
| 对照：004 段自己内部首末（持续推镜） | 47.5 | +0.01 | —— |

最后一行是这份示例最重要的一条：**段内的合法运动可以比失败的接缝更"大"**（47.5 vs 45.4）。
所以看到大数字时，先回第 1 步打开图，而不是直接判失败；而倍率（1.2× vs 31×）能把两种情况分开，
前提是分母取**段内单帧最大跳变**——取首末漂移的话，004 段的 47.5 会把真接缝除成 0.9 倍。

---

## 五、这份方案与事故现场的差别

| | 事故现场 | 本方案 |
|---|---|---|
| 生成单元 | 6 镜 = 6 次独立生成 | 5 个单元（其中一个装 2 镜容器） |
| 切点设计 | 每镜各自独立起链，接缝"留给剪辑" | 每个切点有性质、手法、通道、成本层、时间与声音账 |
| 共享锚点 | 无（两段各写各的） | 盘 / 桌面 / 椅背 / 吊灯四件逐字复述 |
| 核对方式 | 逐段单独看 | 相邻段取真实末帧与首帧并排看 + 四行判断表 |
| 结果 | 003→004 真断裂；002→003 虽然是设计好的换机位，但当时也没写明动机 | 每一刀要么有锚点、要么有动机、要么本来就该切 |

最后一行是关键：**每段内部都可以是合格的，接起来才是废的。**
