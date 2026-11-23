# H3 案例笔记（项目实测记录，不是通用规则）

这里存放从具体项目和复刻任务里沉淀的实测与做法。每一节都带着当时项目的具体物件（灯笼、红裙、
宴席、门楼）、参数和一次性的数字。它们是**证据与启发**，不是可以原样套用的槽位，也不是每次写词
的必读材料。

使用方式：遇到同类问题时，先读该节开头的适用条件；取方法，不取物件。把示例里的灯笼、红裙、门楼换成本镜
自己的东西，句子才是在描述本镜，而不是在复述另一部片。`SKILL.md` 里每一节都保留了抽象后的原则和指向本文件的入口。

写进正文前的两道检查：

1. 这一节的前提（连续飞行、一镜到底复刻、宴席人群、门洞场景……）本镜真的成立吗？
2. 我要抄的句子里，有没有只属于那部片的名词？有就换掉。

## 目录

- A · 连续飞行镜的运动复刻（贴地飞行、光流量化）
- B · 暖灯笼复刻的光色观测与假设
- C · 遮挡转场：完整手法、自检与失败模式
- D · 跨段拼接的顿挫与鬼影（叠化 / 硬拼 / 变速的实测）
- E · T8 Creative DNA 结构
- F · 打戏配方（短剧冲突戏）
- G · 一镜到底的多空间状态链与人群表演（宴席复刻）
- H · 门 / 容器状态锁与起始帧几何语义

---

## A · 连续飞行镜的运动复刻（适用条件）

以下经验只用于已要求全程飞行或连续推进的复刻镜头。普通表演、观察和反应镜可以固定机位，由人物或物体承担运动；不为每帧位移或光流分数添加无关运镜。先遵守本镜导演意图，再选运动参照与幅度。

### 事故记录（可复现的量化）

一条 30s 连续飞行片的复刻，我用"跟拍"一类词写运镜，成片实测：

| 秒 | 源片运动量 | 我的运动量 | 差距 |
|---|---|---|---|
| 0 | 4.88 | **0.30** | 我几乎静止 |
| 1 | 7.85 | **0.26** | 同上 |
| 9–11 | 7.43/5.25/7.16 | **1.60/1.95/2.11** | 不到一半 |
| 19 | 7.52 | **1.65** | 同上 |
| 25–26 | 6.23/6.96 | **2.15/3.00** | 同上 |

全片平均：源片 6.91，我的 5.79（**84%**），且有 11 个秒位不到源片一半。

### 根因：把"低机位自主推进"写成了"跟拍主体"

错：`A low tracking shot rides behind two women`
—— 模型理解成"相机跟着那两个人"，于是人走得慢，相机就慢；人停下，相机就停。

对：`THE CAMERA IS ALMOST ON THE FLOOR AND IS FLYING FORWARD THE WHOLE TIME: it sits barely
a hand's width above the polished stone, tipped a few degrees up, and it never stops moving
forward and drifting steadily to the left, so the floor sweeps past underneath`

差别：**前者以主体为参照，后者以地面为参照**。以地面为参照，模型才会为了"地面扫过"而持续前进。

### 连续飞行复刻内的三条写法

1. **明写"从不停止"**。加 `never stopping, never settling, never holding still for a single
   frame`。只写 `the camera moves` 不够——模型会给一个每秒动 2px 的"移动"。
2. **用地面/前景做运动参照**，不要用主体。
   `the floor sweeps past underneath` / `the railing slides through the lower foreground`
   比 `the camera follows her` 有效得多。
3. **贴地机位要写清"下半幅全是地面"**。这既锁定机位高度，又给了运动参照物。

### 怎么量化验收

用光流测逐秒运动量，与源片对齐（脚本见下方）。判据：

- 同构图连续飞行复刻中，任一秒运动明显低于源片时回看是否丢失所需运动；不能据此否决普通固定镜头。
- 贴地飞行段，水平位移应达到 **每帧 −5 ~ −20px**（640×360 尺度）
- 全片平均运动量应在源片 **±20%** 以内

```python
import cv2, numpy as np
def motion_per_sec(frames):          # frames: 灰度图列表
    prev=None; res=[]
    for g in frames:
        if prev is not None:
            p0=cv2.goodFeaturesToTrack(prev,400,0.01,8)
            if p0 is not None and len(p0)>12:
                p1,st,_=cv2.calcOpticalFlowPyrLK(prev,g,p0,None)
                ok=st.flatten()==1
                if ok.sum()>12:
                    M,_=cv2.estimateAffinePartial2D(
                        p0[ok].reshape(-1,1,2), p1[ok].reshape(-1,1,2), method=cv2.RANSAC)
                    if M is not None:
                        res.append(abs(M[0,2])+abs(M[1,2]))   # |dx|+|dy|
        prev=g
    return res
```

### 失败模式（加进 failure-modes）

- 只写 `tracking shot` / `follows her` 不写"从不停止" → 相机跟着主体走走停停；
- 没有运动参照物（地面/前景栏杆） → 模型给一个原地小抖动的伪运动；
- 贴地镜头没写"下半幅是地面" → 机位被抬到人眼高，低机位感全失；
- 多段拼接时每段机位高度/速度不一致 → 拼起来像几段不同片子。

---

## B · 暖灯笼复刻的光色观测与假设（实测 2026-10-20）

**适用条件**：复刻源片里的暖灯笼与冷夜空。下表是该案例核对光色时的分组，不限制其他项目的光源、色温或表面颜色。
同一组暖光写了两个色温与成片波动在本例中同时出现；这只是待验证假设，多变量观测尚不能证明因果。

| 案例分组 | 本片归属 | 本片写法 |
|---|---|---|
| **暖人族** | 纸灯笼、烛台、灯柱、门缝透光、红绸透光 | 统一暖光描述；出现过 2600K 与 2400K 两值的稿件 |
| **冷空族** | 夜空、廊外、门外夜、月光 | 单独记录冷夜空，如 7500K |

源片实测暖灯笼 Δ+20~+76、夜空 Δ−11~−14，两者共存。其他项目若有已确认的多种暖光、冷色表面或光色变化，继续遵守其账本。

### 事故记录

某 30s 片 A 段，同一段里写了 `about 2600K`（走廊）和 `about 2400K`（市集）。
成片实测段内亮度标准差 **9.8**，而同区间源片只有 **3.0**——波动是源片的 3.3 倍。

另一处写了 `the brightness pulsing with the rhythm of the turns`（亮度随旋转脉动），
主动要求亮度变化，而源片该处亮度平稳。成片 B2 段标准差 **22.4** vs 源片 **13.4**。

### 对照账本核对

1. 色温按实际光源、空间与状态核对；同源同态冲突才回查上游。两个暖光色温本身不是错误，不能为统一数值删改合法光源。
2. 光变必须有上游依据。源片平稳而正文额外写 `brightness pulsing` 是本例的不一致；账本明确的开关灯、闪烁、经过照明区等因果光变仍保留，并写清触发、时刻与结果。`flashing`、`brightens then dims`、`exposure shifting` 也按此核对。
3. 中性地面与冷夜空是本片事实。其他场景按已接受的表面色彩和受光写，冷色地面、墙面、木构件均可成立；RGB 等比只是一种描述中性的句式，没有与色名写法的受控对比证据。
4. 同一时刻同一表面的描述保持相容；确有颜色或受光变化时，分别注明时刻与原因。

### 假设的验证边界

本例的机位、空间、运动、提示词与光源描述等变量未被单独控制。上面的标准差只能报告观测差异，不能归因为同族两个色温。要验证该假设，需同一输入、seed、时长与其他正文，仅改变该色温描述，比较相同区域和时间窗的亮度曲线；验证前不把色温数量用作强制改词条件。

### 怎么在源片里核对

把「中性表面」与「暖光」分开量（前者是地面/墙/木，后者是最亮的灯笼像素）：

```bash
# 中性表面：低饱和、中低亮度像素的 R-B
# 暖光：最亮 5% 像素的 R-B
```

实测基准（这条片子）：
- 中性表面 Δ(R−B) = **−2.8 ~ +1.6**（几乎绝对中性）
- 暖光 Δ = **+20 ~ +76**（单调渐变，不来回跳）
- 冷空 Δ = **−11 ~ −14**

这些范围只描述本片采样区域；其他项目应按其场景色彩、受光和可比区域另行比较，不能用这里的 ±3 判定色偏。

### 分段生成的光色连续性（实测 2026-11-03，30s 一镜复刻）

- 全片三段独立生成（暖橙灯笼单一族），分段间光色实测连续：暖光 Δ(R−B) 全程 +20~+76 同族单调，接缝处无色温跳变。
- **该次写法**：每段提示词用同一套暖源描述词（`warm red-orange light` / `warm orange lanterns`），没有具体 K 值或第二个暖源，冷色写在 `dark night sky`；这是该片记录，不限制其他场景。
- 起始帧（静帧）与视频首帧的光色也保持同族——静帧用同一批风格词生成，段间衔接时光色不跳。
- 若分段间出现色温差，优先在剪辑侧对拼接点做 1–2 帧色彩拉平，而不是重生成。

---

## C · Occlusion Transitions (实测 2026-10-20，win-desktop · H3 · 24fps · 1248×704)

场景要换、但**不能留下切点**时，用「遮挡扫过」代替转场。观感上比后期叠化/擦除更干净，
因为遮挡期间画面信息量趋近于零，模型换成什么都看不见。

### 为什么比后期转场好（实测数据）

遮挡帧的**色彩标准差反而下降**（画面被单一色块占满）：

| 时刻 | 帧差 | 亮度 | 色彩标准差 | 状态 |
|---|---|---|---|---|
| 2.3s | 24.9 | 64.3 | 44.9 | 红裙占满画面 |
| 2.6s | 11.0 | 24.2 | 38.5 | 露出新场景 |
| 2.8s | 5.3 | 33.1 | 39.6 | 稳定 |

后期叠化要混两个**都有细节**的画面，混合期必然露重影；遮挡期没有细节可露。

### 四要素（缺一不可）

| # | 要素 | 例（红裙扫过） | 例（红绸滑开） |
|---|---|---|---|
| 1 | **遮挡物是什么**（具体名词，不写「转场」） | `the vermilion skirt and a passing shoulder` | `a vast sheet of vermilion-orange silk` |
| 2 | **从哪个方向来、往哪个方向走** | `sweep across the lens from the right` | `slides away to the left` |
| 3 | **遮挡到什么程度** | `swallow the frame` | `fills most of the picture` |
| 4 | **露出的是什么** | `the corridor behind it becomes a lantern-packed market` | `to reveal the hall's side bay` |

**再加一句镜头没停**：`the camera travels on through that sweep, one unbroken move, as …`。
这句是关键——不写它，模型会把遮挡当成镜头结束。

> ⚠️ **不要写成 `without cutting`。** 那是本文件自己禁止的否定句形态（H3 在 cfg 1 没有负向分支，
> `without cutting` 里的 `cut` 照样进入正向条件），实测过 `h3_gate.py` 会报 G36。
> 正向等价写法：`the camera travels on through that sweep, one unbroken move, as he clears frame right`
> （2026-11-05 实测 exit 0，0 warn）。

### 完整句式模板

```text
At <时间>, <遮挡物> <动作> across the lens from <方向> and <遮挡程度>,
and the camera travels on through that sweep, one unbroken move, as <遮挡物> clears:
<遮挡前所在场景> becomes <遮挡后所在场景>.
```

起幅即遮挡（用于接上一段）时改成：

```text
It opens buried in <遮挡物>, <遮挡物> sweeping across the lens from <方向> so close
that it fills most of the picture. The camera travels on and <遮挡物> slides away
to <方向>, clearing to reveal <露出的场景>.
```

### 硬规则

1. **遮挡转场里不写 `cut` 词**。`the camera cuts to` / `the shot transitions to` 都是硬切指令；
   遮挡转场只写 `the camera travels on`。（真要硬切时反过来必须写 `the camera cuts to`，见 G28。）
2. **遮挡物必须具体**。写「某物扫过」无效，要写清是什么（红裙、红绸、灯笼、肩膀、人群）。
3. **必须给方向**。只说 `sweeps across the lens` 不给 from/to，模型会让遮挡物随机停留。
4. **必须写露出什么**。不写的话模型可能露出完全无关的场景。
5. **遮挡程度要够**。`swallow the frame` / `fills most of the picture` 才够；
   写 `passes in front of the camera` 会只遮住一部分，接缝露出来。

### 什么时候能用

| 条件 | 说明 |
|---|---|
| 跨段拼接 | 两段独立生成时，接缝必须藏在遮挡帧里；找**色彩标准差最低**的那一帧。若有生成层接力（§Generation-Layer Relay），优先接力 |
| 段落界 | 源片本身若无硬切，段内场景转换一律用遮挡 |
| 主镜头要换空间 | 从 A 空间到 B 空间，中间插一个近处物体扫过 |

**不能用的场合**：需要精确控制转场时刻（遮挡时刻由模型自己决定，偏差可达 ±0.5s）、
需要保留遮挡物细节（遮挡期是纯色块）、两场景光比差极大（亮度会跳，需后期调色拉平）。

### 怎么在源片里找可用的遮挡点

```bash
# 逐帧算色彩标准差，最低的几个时刻就是遮挡帧
ffmpeg -v error -i source.mp4 -vf scale=160:90 -fps_mode passthrough -y /tmp/f%04d.png
python3 -c "
import glob,numpy as np
from PIL import Image
for p in sorted(glob.glob('/tmp/f*.png')):
    a=np.asarray(Image.open(p).convert('RGB'),np.float32)
    print(p.split('/')[-1], a.mean(), a.std())
" | sort -k3 -n | head -10
```

标准差 < 30 且亮度均匀的帧，就是可藏接缝的位置。

### 自检（脚本化，句子级而非全文关键词）

按**句子**判，不按全文关键词判——四个要素常分散在同一句里的不同位置，
全文 grep 会误判（实测：`sweep across the frame and swallow it for a beat,
and when they clear the camera has carried on into a night courtyard` 这一句同时含四要素，
但用「全文分别搜方向词/程度词/露出词」会判失败）。

```python
import re
# 逐句扫描：只要有一句同时满足 (遮挡物 + 动作) 与 (露出)，就算合规
def occlusion_ok(text):
    OBJ  = r'(skirt|silk|cloth|robe|sleeve|shoulder|crowd|lantern|curtain|blind|door|leaves)'
    MOVE = r'(sweep|swept|slides?|passed?|glide|swallow|fills?|covered|across the (frame|lens))'
    OUT  = r'(becomes?|reveal|clearing|when they clear|carried on into|opens? (in)?to|into a)'
    for sent in re.split(r'(?<=[.;])\s+', text):
        if re.search(OBJ, sent, re.I) and re.search(MOVE, sent, re.I) and re.search(OUT, sent, re.I):
            return True, sent[:90]
    return False, ''
```

**注意**：「门缝渐开」类衔接（`the doors part, the gap widens, the hall opens up beyond`）
不属于遮挡扫过，不该套这套四要素；它属于**同空间推进**，只要不写 cut 词即可。

### 失败模式（加进 failure-modes）

- 写了遮挡但没写「镜头没停」→ 拍成一个静止画面被挡住又露出，像黑场；
- 遮挡物写成抽象词（`a blur` / `a wipe`）→ 模型给出失焦色块，不像实物；
- 遮挡程度不足（`passes before the lens`）→ 只挡住画面一角，接缝露出来；
- 在需要精确时刻的段落用遮挡 → 遮挡发生时刻不可控，节奏对不上。

---

## D · 接缝实施边界：跨段拼接的顿挫与鬼影（实测 2026-11-03，win-desktop · h3q · 24fps · 1344×768）

**两段独立生成的视频，拼接帧处必然存在「纹理噪声 + 光流场模式」的双重突变。** 30s 一镜到底复刻中实测四种接缝实施：

| 实施方式 | 实测结果 | 结论 |
|---|---|---|
| crossfade 叠化 0.4–0.5s（**有人物帧**） | 人物与前景**半透明重影**（双重曝光），观感=转场特效 | **人物帧禁止叠化** |
| crossfade 叠化（**全屏无细节色块帧**，如红裙遮镜占满画面） | 无鬼影，接缝不可见 | ✅ 叠化只用于全屏色块帧 |
| 硬拼 d=0（拼接帧两侧≈同一画面，光流速率比 1.02） | 画面连续，但**仍可感知「顿一下」** | 纹理/运动模式突变不可被画面连续性掩盖 |
| 硬拼 + 接缝后段变速压平（clips_split + clip_speed 0.6–0.72） | 光流峰值 9.8→5.9 可压平，曲线单调化，但重复帧有微顿 | 缓解不根治 |

**推论（硬规则）：**

1. **成片上的长运动（飞出/坠落/穿越/追赶）不拆段**——两段独立生成的运动衔接顿挫无法用任何后期手段消除（叠化、硬拼、变速全试过）。注意区分「成片拆」和「生成拆」：生成可以拆，前提是走潜空间接力（见 §Generation-Layer Relay），不能用剪辑层拼。
2. 本地单次容量档 15s（16G 容量/训练范围；节点 length 可到 3600f），超长一镜优先**压缩前段保一镜**（实测：中堂段 7.2s 压到 4s，让「中堂→拐角→飞出→灯海」15.08s 一镜生成成功，六个空间状态全部按时间轴执行）。
3. **必须在剪辑层拆段时**，接缝只允许落在两类帧上：**全屏遮挡帧**（信息量≈0）或**全屏色块帧**（红裙扫镜）。这是剪辑层手段；生成层接力（§Generation-Layer Relay）不依赖画面遮挡。
4. 光流速率匹配工作流：接缝两侧各取 0.65s 窗口测每帧运动量（LK 光流 + estimateAffinePartial2D），比值 0.8–1.25 内可硬拼；接缝后段有生成自带的加速/减速时，用剪辑侧 split+speed 压平到与原片速度曲线一致。
5. 两段构图完全不匹配时叠化直接判为「硬切/割裂」——先对齐首尾帧，再谈接缝。

---

## E · T8 Creative DNA Structure (from `minimax-h3-prompt-skill-T8`, MIT code + CC BY 4.0 content)

A second, complementary prompt architecture. Where the official six-section format fixes
*fields*, Creative DNA fixes *causal mechanism*. Use it when a brief describes a repeatable
beat pattern (a greeting, a reveal, a chase payoff) rather than a one-off scene.

Each DNA case is a folder with `SKILL.md` + `references/summary.md` + `references/template.md`:

- **Mechanism** — one sentence naming the reusable causal chain (e.g. "five small state
  changes: side orientation → direct gaze → downward pause → peak smile → open recovery").
- **Invariants** (`inv-01…`) — mandatory anchors, each with three lines: `Rule`, `Purpose`,
  and **`Failure if removed`**. The failure line is what makes the structure testable: if a
  draft drops an invariant, you can name exactly what breaks.
- **Variable Slots** — a table of what MUST change per new execution (`lead_subject`,
  `setting`, `causal_carrier`, `state_change`, `camera_grammar`, `payoff`, `sound_family`).
  Rule: change all slots together; never reskin by swapping nouns only.
- **Anti-Copy Boundary** — explicit list of source-specific things forbidden in the new prompt.
- **Transfer Tests** — 2+ worked re-instantiations, each listing which invariants were
  preserved and which slots changed. Read these before writing: they show the intended
  distance from the source.
- **Model Skeletons** — separate compile targets for MiniMax H3 (three fields) and
  Seedance 2.0 (Chinese paragraph form). Never leak one model's field syntax into the other.

**Writing an H3 prompt in DNA style** (what to put in `detailed_description`):

1. Open with the mechanism sentence so the model knows the beats form one chain.
2. Make every beat inherit velocity from the previous one — state the weight transfer or
   momentum handoff explicitly ("no beat starts from a standstill").
3. Fix 1–2 spatial anchors in frame (a plant at the right edge, a level window line) so
   rotations and moves are measurable against them.
4. Put visible evidence of each state change in the *feet or contact points*, not only the
   arms ("the right heel lifts an inch so the shift is visible in the feet").
5. End on a held settle, not a cut mid-motion.

**Measured 2026-10-18 (five variants, same content, PDD 8-step draft tier, seed 1017):**
corrected reading — the baseline six-section prompt **also executed its written turn** (a full
360° pivot), so "turning" is not what distinguishes the DNA style. What V4 (DNA prose) added
was *articulation*: the pivot showed a lifted heel / single-foot weight transfer instead of a
flat-footed compass spin, and the clip ended on a held payoff (smile + open arms) rather than
a neutral settle. The explicit `reference_anchors` field block (V2/V3) **disturbed the set
dressing** (a floor lamp and side cabinet appeared that were not in the baseline) without
improving motion. Therefore: use the DNA *prose* techniques above (weight transfer in the
feet, momentum inheritance, held settle); do **not** emit a literal `reference_anchors:`
block — fold spatial anchors into the scene description instead. The official Pixar suffix
(V1) showed no measurable gain on an already-stylized Q-version character; keep it only when
the brief asks for a look change. **n=1 per variant — treat as direction, not law; re-test
before codifying.**

Corpus: hundreds of cases under `skills/` in the T8 repo (7.3 GB total incl. videos — fetch
only `SKILL.md` + `references/` per case). Two worked examples archived locally at
`prod1017/community/vendor_promptskill/case1` and `case2`. Tested as experiment V4
(`eval_prompt/V4_t8_dna.txt`) against the plain six-section baseline V0.

---

## F · Fight Choreography Recipe (from director-skills action-fight-prompt, 2026-11)

短剧打脸/冲突/追逐戏专属配方，四条铁律（`craft_default`，按需启用）：

1. **时序拆段**：15 秒以上的打戏先拆成 2–3 秒的阶段，每阶段一组主动作，
   `[Shot k]` 切点显式标出；一个阶段只干一件事。
2. **动作因果链**：相邻阶段必须是物理因果——对手前冲 → 女主借惯性转身。
   每个动作要能回答「上一个动作给了它什么条件」；孤立动作是瞬移/穿模的根源。
3. **环境反馈**：每阶段至少一处——尘土、火星、犁沟、裂纹。它告诉模型
   力量从哪里来（写在 `integrated_multimodal_description`，对应音效进 `overall_soundscape`）。
4. **资产锁定**：开头独立句声明脸/发型/服装/武器/比例全程不变；
   双角色分别写 `<Picture N> = 女主`、`<Picture M> = 对手`。

**打击感四环**（写接触那一拍时按序给全）：

```text
力量来源（腰部发力/蹬地）→ 接触瞬间材质反应（金属→火星、甲壳→碎屑、沙地→犁沟）
→ 位移后果（偏转半寸/后退半步）→ 环境反馈（尘土扬起）
```

力量从身体写起，不是手臂凭空挥动。**微慢动作给具体时长**（约 0.2–0.3 秒后立刻恢复
正常速度，每段最多一次）；结尾必须铺垫下一轮（对手重新起身/下一波逼近）。
无配乐打戏显式写 `non_diegetic_music: N/A` 并在声景保留力量声/材质声/生物声三层。
（来源：director-skills action-fight-prompt 四条铁律 + camera-and-impact 词库，MIT。）

---

## G · Multi-Space Long-Take State Chain（实测 2026-11-03，win-desktop · h3q · 24fps · 14.59s 定稿）

**适用边界**：本地容量档单次 ≤15s、空间可以连续走通。超过 15s 或必须分次生成时，先读 §Shot Joining: Three Layers——不要在剪辑层硬拼。

**单次生成内 6 个空间状态的连续切换是可行的**：14.59s 一镜实测（红裙遮镜→中堂宴席→红楼梯→二楼回廊→拐角→飞出建筑→灯海收尾），全部按时间轴执行、逐帧无内部切点。**以下示例即创作者定稿版正文的时间轴**（`nb-H-oneshot.mp4`，draft1/draft2 同文），后续 12.4s 压缩变体已作废。

### 写法（逐秒状态链）

每段一句 `From X to Y seconds` + **空间 + 在场人物的具体动作 + 镜头与人物的关系**，空间转换由镜头运动本身完成（不写任何转场词）：

```text
From 1 to 4 seconds the camera stays low and moves forward between long banquet tables:
<人群具体动作清单>.
From 4 to 5.5 seconds he reaches the red-lacquered staircase and climbs,
the red railing sliding past the lower foreground.
From 5.5 to 7.5 seconds on the second-floor gallery he walks past <回廊人群动作>,
approaching the corner where the gallery opens to the night.
From 7.5 to 9 seconds at the corner the waiter turns right and walks out of the
left edge; the camera does not follow him — it passes over his shoulder, glides over
the red railing and flies out of the building in one continuous motion.
From 9 to 11 seconds red lanterns sweep through the foreground and dark tiled
rooftops slide past and fall away below.
From 11 to 14.5 seconds the vast carpet of warm amber city lights unfolds gently...
```

### 硬规则

1. 每段的**空间锚点**（楼梯/栏杆/拐角/屋顶）必须具体到可画；只写"he walks on"会让空间并成一片。
2. 长镜头后半段（>10s）给**收尾句**（`settles into a steady wide shot`），否则模型在时长末尾自行加减速。
3. **帧数注意**：>300 帧（12.5s）走 `final` 时用 split 引擎（默认，`--tile-size 0`），311/362 帧已实测通过；只有显式回退 `--upscale-engine legacy3d` 才会 shape mismatch。多段接下段时，下段 `--first-frame` 取上段末帧，不要用分镜关键帧。
4. 中堂等人群段压时长时，砍的是镜头数量不是动作密度——每秒至少保留一类具体互动动作。**但压缩版要先过创作者验收**：本例 12.4s 压缩版未经确认即作废，定稿以创作者实看的采样为准。


### Crowd Vitality: Action Lists Beat Abstraction（实测 2026-11-03）

**抽象情绪词（`laughing and talking`）在 H3 人群上一律落实为「微笑站立缓慢漂移」**（AI 摆拍感）。
实测有效的是**具体动词清单**——把「手舞足蹈/欢呼雀跃」翻译成可画的大幅度动作：

```text
young singing girls and banquet hostesses in bright orange-red, pink, plum and cream
silk robes entertain the diners — they lean flirtatiously against the guests'
shoulders, wave their wide silk sleeves playfully, tilt their heads and giggle
behind raised hands, sway as they pour wine into tilted cups, tease the diners with
coquettish gestures and play drinking games with them, while male guests raise cups
and roar with laughter and some stand up to bow in toast
```

配套两句框架句（实测有效）：

```text
...sleeves and hair ornaments brushing close past the lens;
every person interacts with the people around them, none of them looks toward the lens.
```

- 前句制造前景遮挡穿行感（沉浸），后句消除「全员面向镜头微笑」的 AI 摆拍感。
- 围坐与站走要写明混合（`seated guests...while a dense stream of standing guests walks
  and weaves between the tables`），只写 stands 会全员罚站。

### 否定词分级

已并入 `SKILL.md` 的 *否定词分级*（通则，不是案例）。

---

## H · Gate/Container State Locking + 起始帧几何语义（实测 2026-11-03）

**门「先开了又关上」的根因链**（用户逐帧发现，两次返工才定位）：

1. 起始帧尽头是一个**黑色矩形门洞** → 模型读成「门开着」；
2. 正文又要求 `fully closed` → 模型为凑状态**生硬演绎一段关门动作**（1.5–4.5s 开着→关上）；
3. 正文再要求 6s 开门 → 第二次开门。观众看到「门开了又关」。

### 正解三件套（实测有效）

1. **起始帧**：尽头只允许「远处渐暗的建筑轮廓」——静帧正文写 `The courtyard depth fades into
   warm darkness with distant building silhouettes only — no gate, no door frame, no
   rectangular doorway anywhere`（场景/几何类否定，实测有效）。
2. **正文首现式**：`a tall crimson gate tower ... appears ahead for the first time at 4.5
   seconds; until this moment no gate of any kind is visible`——门在首次出现前不存在于画面。
3. **状态肯定式**：`The two thick door leaves stand fully closed and stay closed... the doors
   are pushed open from inside`——状态链只写一次开启，开门动力写明（`from inside`）。

静帧与视频的正文必须用同一套几何描述——静帧有门洞而视频正文说没有，模型会两头听。
