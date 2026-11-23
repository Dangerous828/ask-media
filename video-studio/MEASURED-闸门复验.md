# MEASURED · 闸门复验（2026-10-22 15:08–15:45，EP01 v4 交接之后）

> 触发：收到 `/tmp/HANDOFF-ep01v4-20261022.md` 终态交接。按「实跑验证，不静默改写」的纪律，
> 把文档声明逐条对盘复核。**结论：文档四条元经验全部成立，但它点名的「闸门已补齐」只补了一半。**
> 本轮实测出第 3、4 处缺口，与已修的 1、2 **同一根因**。数字全部可由文末命令复现。

---

## 一、复验通过的部分（不重复展开，只记证据位置）

| 文档声明 | 复验结果 |
|---|---|
| 成片 1099 帧 / 9/9 单段式 / 段内硬切 0 / 8 接缝 7 连续 + 1 反转 | ✅ `python3 tools/cut_detect.py` 全量复现，逐段 mad 与接缝表与文档一致 |
| S01→S02 接缝 20.37 → **1.83**（比 1.07） | ✅ 实测 seam_mad=1.83 比=1.07 ok |
| S08 连续升摇 mad 36.8 不被误判成切 | ✅ 实测 mad_max=36.80，cuts=[] |
| `cut_detect.py` 已修 `-fps_mode passthrough` | ✅ `tools/cut_detect.py:18-22`；三片解出帧数 == 容器 nb_frames（1099/1034/192 全一致） |
| 版本溯源：v4s 九段都跑在修好的单段式提示词上 | ✅ 九段「提示词 mtime ≤ 渲染 mtime」全部 OK（见文末命令） |
| P0-4 退出码语义（三段 exit=1 / 单段 exit=0） | ✅ 用文档的 `/tmp/lintchk/multi.txt` 复造，exit=1 / exit=0 成立 |
| G08b 裸标签误报已修 | ✅ `h3_gate.py:76,553` 有 `LABEL_RE_ANY`；带 `--frames` 后项目文件不再报 G08b |
| ask-studio 已停用 | ✅ `内部归档（未随公开版发布）` 存在；AGENTS.md 规则 8 已改写 |

**判据本身踩过的四个坑**（复现任何逐帧分析前必读）：

| # | 坑 | 后果 | 修法 |
|---|---|---|---|
| 1 | 全局阈值把运镜误判成切点 | S08 升镜连续 20–35 十几帧，报出 7 个假切点 | 改孤立性判据（邻域半宽 5、倍数 4.0、全局 median+3σ）。**「整段都在动」不是切，「孤零零一帧跳」才是切** |
| 2 | 只看峰值 | S05 的 38.7 比某些真切点还高却不是切（快速转身+运动模糊，呈爬升→下降包络） | **必须看邻域形状**：单帧阶跃 vs 包络 |
| 3 | ffmpeg 默认 vsync 补帧 | 容器 `nb_frames=1065` 却解出 1066 帧，切点整体偏移 1，把真实 20.37 掩盖成 0.36 | 必须加 `-fps_mode passthrough`，并核对 `nb_frames` |
| 4 | 接缝用绝对阈值 | S01 段内中位 0.57，S02 中位 9.18，同一个 3.5 在两段意义完全不同 | 用**局部动量比** = `seam_mad / max(前段尾12帧中位, 后段头12帧中位)` |

**v4 成片战报的完整数字**（用户原话一并保留）：

| 项 | 结果 |
|---|---|
| 用户评价 | 「真的好很多喔，但是转场还是要看 h3 那边的处理，大问题真的基本都没有了」；「不管机位连贯性效果很好，说明新 skill 很好，运镜也都还算合理」 |
| 「新 skill」所指 | v4 方法论（`ep01_v4/METHOD.md` 规则 1–5），不是本 skill 的拼装脚本 |
| 硬切数 | **7 → 1**（唯一的 1 个是刻意设计的反转硬切） |
| 关键帧目检 | **9/9 可用** |
| 四件套严格通过 | 3/9（阈值口径问题，见 `MEASURED-Opus六信号复验.md` §4.1 / §11） |
| 锚点链 | 8 个转场逐条验证，S06 与 S01 轴线完全复现 |
| 全片 | 1099 帧 / 45.79 s / 24 fps / 1312×736 |
| 段内硬切 | **0（9/9 段）** |
| 段间接缝 | 8 个：**7 个连续**（动量比 ≤ 1.37），1 个设计切 |
| 首尾帧落点 | 9/9 段均落在指定参考帧（差 2.16–6.03） |

**v4 的连续性方法论：锚点链**。相邻两镜必须共享一个可指认的锚点，三选一：

1. 同一机位轴（如 S01→S02 都是 35mm/45°，只推不切）
2. 同一前景物（如 S05→S06 沙发/玩具篮/电视柜位置与 S01 一致）
3. 同一运动方向（如 S02→S03 都是向北前移）

v4 的 8 个转场全部落在其中一类，**S06 与 S01 的三件陈设位置完全复现是全片最硬验证**。

**文档 §二 的四条元经验，本轮又被印证了一次**（见下面第 3、4 处缺口）——
它们不是抽象总结，是还能继续复现故障的活判据。

---

## 二、FL2VA 多段式诱发真硬切：物理实测 + 两处闸门缺口

### 2.0 事故现场（完整经过）

S07 原提示词写成三段式（`[Shot 1]` / `[Shot 2] At 00:01.200` / `[Shot 3] At 00:02.800`），
H3 在**帧 66 = 2.75 s，正好对上 `At 00:02.800`** 产生真硬切：
相邻帧亮度差 **106.5/255**、直方图距离 **0.64**，机位与光照瞬时全换。

A/B 对照（同种子 **5071**、同首尾帧、同 **107 帧**）：

| 项 | A：三段式 | B：单段式 |
|---|---|---|
| 帧 66→67 `mad` | **106.53** | **18.79** |
| 段内切点 | **1** | **0** |

A 版重渲一次**完全复现**（切点帧号与 top5 完全一致）⇒ 确定性缺陷，不是采样噪声。
**同一批里另外 5 段也写成三段式但没触发**：这是概率性诱发，不是稳定复现——
所以「这次没炸」不能当通过。

官方依据（`references/official/base-en.txt:62`）：

> FL2VA generally favors a **single shot** so the model can interpolate continuously
> from the first frame to the last frame. Use multiple shots only when they are
> **explicitly specified**.

官方 8 秒范例（`base-en.txt:201`）两张帧都标 `(from Shot 1)`，正文只有 `[Shot 1]`；
首尾帧同属一段，运镜与动作在段内用连续语写。收尾用
`decelerates into the exact spacing … of Picture 2 at the end of the shot`。
**只有真要硬切才分段**，且按官方 §4.2 用 `the camera cuts to`；
「只改景别或轻微角度优先用运镜，不要切」（`base-en.txt:92`）。

判据：FL2VA/L2VA 出现 2 个及以上 `[Shot N]`，必须先回答「这些切点是我真的要的硬切吗」，
不是就改单段。判据要结构或相对、不要措辞或绝对阈值（同批踩过的坑见下文缺口 3/4）。

### 缺口 3：`h3_lint.py` P0-4 用「措辞」认 FL2VA ⇒ 换个等价写法就整份漏过

**复现条件（关键：文件必须结构完整，否则被别的规则先挡下，掩盖缺口）**

```bash
# 双帧 + 三段式，首行写成 "Picture 1 is the first frame ..." 而不是官方那句 "aligns with the ... mark"
python3 ../scripts/h3_lint.py /tmp/lintchk2/full1.txt          # 修复前 exit=0 ✗
python3 h3-video-gate/scripts/h3_gate.py /tmp/lintchk2/full1.txt --frames 107 --strict   # 修复前 exit=0 ✗
```

**根因**：P0-4 的判据是 `has_align = re.search(r"aligns with the .{0,40}?(?:mark|second)", low)`，
且 `is_fl = has_align and len(pics) >= 2`。首行只要换一种等价措辞，`has_align` 即为假，
`is_fl` 连带为假，**函数直接 return**——多段 FL2VA（真会诱发切镜的那个缺陷）无声放行。
这与已修的 G08b「`LABEL_RE` 只认 `<Picture N>`、不认官方裸 `Picture 1`」是**同一个根因**：
正则只认「我以为的写法」，不认官方范例的真实写法。

**修法**：判据从「措辞」改为「结构」。

```python
def _is_ref_mode(text):   # Ref2VA 六段不受 FL2VA 单段约束
    return bool(re.search(r"^\s*(?:subject_definitions|detailed_description)\s*:", text, re.M))

pics = {…PICTURE_ANY_RE…}                 # 尖括号与裸写法都认（新增模块级常量）
is_fl = (1 in pics and 2 in pics) or (has_align and len(pics) >= 2)
```

即：**非 Ref2VA + 同时加载 Picture 1 与 Picture 2 = FL2VA**，对齐句措辞不再参与判定。

**顺带修掉一个反向缺陷**：原先「首尾帧分属不同段」无条件报 P0，会把
官方 `base-en.txt:62` 允许的「显式声明硬切的多段」（尾帧本就属于最后一段）判成违规。
现改为 `if not declared and len(holders) >= 2`。这是元经验 2「判据必须相对/局部」在闸门侧的同构体。

### 缺口 4：`h3_gate.py` 完全没有 FL2VA 单段检查，且 G21 也只认尖括号

- `grep` 全文无 FL2VA 单段规则 ⇒ 三段式 FL2VA 在 `--strict` 下 **exit=0「全部检查通过」**。
  交接文档说「9/9 PASS」时用的正是 `h3_lint`，`h3_gate` 这条路根本没查过——**一条闸门补了，另一条还是空的**。
- `rule_g21` 的触发条件是 `if not re.search(r"<Picture \d+>", doc.text): return`。
  而项目 S01–S08 全部写的是裸 `Picture 1`（`grep -oE "<Picture [0-9]+>" S07_FL2VA.txt` → 0 命中）。
  ⇒ **决定性对照**：拿项目原件删掉对齐首行做成 `s07_noalign.txt`，裸标签版 `exit=0`（漏检），
  同一内容 `sed` 换成尖括号版立刻报 G21。同一份稿子，标签写法决定闸门走不走。

**修法**
- 新增 **G28**（`("G28", ("base",), rule_g28, "FL2VA 首尾帧必须单段(官方 base-en.txt:62)")`），
  与 P0-4 同判据：base 模式 + Picture 1/2 双帧 + ≥2 个 `[Shot N]` + 未声明硬切 ⇒ error。
- `rule_g21` 触发改用已有的 `LABEL_RE_ANY`；报错文案「用了 `<Picture N>`」订正为「用了 Picture 参考帧(带尖括号或官方裸写法)」。

---

## 三、验证矩阵（修复后实跑）

| 用例 | 期望 | h3_lint | h3_gate --strict |
|---|---|---|---|
| `/tmp/lintchk/multi.txt`（官方裸对齐句 + 三段式） | 拦 | **exit=1** | 拦 ✓ |
| `full1.txt`（等价措辞 + 双帧三段式，结构完整） | 拦 | **exit=1**（修前 0） | **exit=1**（修前 0） |
| `s07_noalign.txt`（裸标签 + 缺对齐首行） | 拦 | — | **G21 命中**（修前 exit=0） |
| `official_single.txt`（单段式） | 放行 | exit=0 | 无 G28/G21 ✓ |
| `legal_multishot.txt`（官方允许的声明硬切多段） | 放行 | exit=0 | **无 G28** ✓ |
| `i2va_multi_1pic.txt` / `l2va_multi.txt`（单帧多段） | 放行 | exit=0 | **无 G28** ✓ |
| `ref_multi.txt`（Ref2VA 六段多段） | 放行 | 不受此规则 | **无 G28** ✓ |
| 项目 S01–S09（9 个真实文件） | 不误报 | **9/9 PASS** | G28/G21 命中 0 |
| gate 自带夹具 6 个 | 不误报 | 6/6 PASS | `pytest tests/` **28 passed** |

测试已从 22 → **28**：新增 `Fl2vaSingleShotAndBareLabel` 6 条（G28 拦/三种合法不误报、G21 裸标签拦/官方裸对齐句不误报）。

> 写新用例时我自己先踩了一次：`test_g28_does_not_hit_i2va_single_frame` 起初失败——
> 我在「I2VA」用例的正文里又引用了 Picture 2，那结构上就是 FL2VA，G28 报得对。
> **是测试写错，不是闸门写错**，改成单帧正文后通过。这类「误报测试自己先错」值得记住。

---

## 四、交接文档没提的两个文件（已查明性质，等创作者定）

`video/` 里有两个比 `animatic_v4s.mp4`(12:12) 更新、但文档与 `H3_TRANSITION_MEASURED.md` 均未记载的产物：

| 文件 | 时间 | 性质（实测） |
|---|---|---|
| `s09_trimmed_handsonly_110f.mp4` | 14:24 | `ss09_v4s_v1_175frames.mp4` 的**前 110 帧**（逐帧对位差 0.29–0.52，同源重编码） |
| `animatic_v5_audiocut.mp4` | 14:34 | **= v4s 前 924 帧 + 上述 110 帧**（前 924 帧与 v4s 差 mean 0.0089/max 0.54）；1034 帧 / 43.08 s / 带 aac |

**它改变了 §六 的第 1 项状态**，且带一个此前没记的副作用：

1. **S08→S09 那个全片唯一硬切没有被消掉**：v5 里仍是 `seam_mad=69.88 / 比 41.34 = CUT`，
   全片切点仍 = [924]。即 v5 **不是**「S09 反转的替代方案」，只是把 S09 截短。
2. **裁掉的正是设计好的渐隐收尾**。S09 提示词写的是
   `At 00:04.500 … the picture inside fades smoothly toward dark while the hands remain lit` +
   `cutting abruptly to silence on the third impact and leaving one faint piano note in the dark`。
   实测屏幕区亮度 110→174 帧 **137.88 → 54.83（降 60.2%）**，渐隐确实渲染出来了，
   但 v5 停在第 109 帧——**「淡到黑 + 一颗钢琴余音」的落点整个被剪掉**，结尾落在最亮处。

⇒ 「handsonly」这名字像是想让 S09 只留手部、不做渐隐，但成片现在**硬停在亮帧上**。
这两点都需要创作者判断，不是我能替他定的，已单独提问。

---

## 五、复现命令

```bash
# 帧级复现全部接缝与切点
cd <本地项目目录>/example-project/smooth3d/ep01_v4/tools && python3 cut_detect.py

# 闸门退出码（P0-4 / G28 / G21）
python3 ../scripts/h3_lint.py /tmp/lintchk2/full1.txt;         echo $?   # 1
python3 ../scripts/h3_lint.py /tmp/lintchk2/official_single.txt; echo $? # 0
python3 h3-video-gate/scripts/h3_gate.py /tmp/lintchk2/full1.txt --frames 107 --strict
# 在仓库根执行，先进入 h3-video-gate/
cd h3-video-gate && python3 -m pytest tests/ -q                                   # 28 passed

# 版本溯源（提示词 mtime ≤ 渲染 mtime）
cd <本地项目目录>/example-project/smooth3d/ep01_v4/h3_prompts && stat -f '%Sm %N' -t '%H:%M:%S' *_*.txt

# 回滚
mv ../scripts/h3_lint.py.bak-20261022-1518 ../scripts/h3_lint.py
mv h3-video-gate/scripts/h3_gate.py.bak-20261022-1523 h3-video-gate/scripts/h3_gate.py
```

**备份**：`h3_lint.py.bak-20261022-1518`、`h3_gate.py.bak-20261022-1523`（改前原件，md5 已核对）。
（`h3_gate.py` 另有本日上午 G08b 修复留下的 `.bak-20261022-105458`。）

---

## 六、给下一位的一句话

补闸门时**两条闸门要同时补、并拿官方范例原文当测试集**：
这次 P0-4 补了 `h3_lint` 却没补 `h3_gate`，而 `h3_lint` 那条又用「措辞」而不是「结构」判 FL2VA，
于是「9/9 PASS」这个结论实际上是建立在一道空闸门上的。判据只要依赖某一句固定措辞，
等价改写就能绕过去——把它换成结构量（模式 + 加载了哪几张帧）。
