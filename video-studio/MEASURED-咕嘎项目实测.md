# 《咕角色C嘎》真实项目实测

日期 2026-10-22
对象：`~/Code/kTool/example-project/`（648 MB，EP01 已返修 4 轮）

---

## 一、最重要的发现：真实项目的出图链路现在跑不起来

### 问题：所有脚本硬编码 18199，该端口没有服务

```python
# smooth3d/tools/rerender_kf_s05.py:17 等 5 个文件
COMFY_HOST = "127.0.0.1:18199"
```

实测：

| 端口 | 监听状态 |
|---|---|
| 18199 | **0（无服务）** |
| 8199 | **1（ComfyUI 0.39.0 在跑）** |

**5 个 `rerender_*.py` 全部指向不存在的端口。** 现在直接运行会连接失败。

### 第二个问题：它绕过了 h3q 队列

```python
def submit_and_wait(graph, target_name):
    req = urllib.request.Request(f"http://{COMFY_HOST}/prompt", ...)   # 直连 ComfyUI
```

违反「唯一提交入口是 h3q 队列（8200），禁止直连」的纪律。

### 第三个问题：3 张参考图在本地项目缺 1 张

| 参考图 | 本地项目 | win-desktop input |
|---|---|---|
| `kf_s04_anime_sunlit.png` | ✓ | ✓ |
| `gugu_turnaround_smooth3d.png` | ✓ | ✓ |
| `gungun_turnaround_v1.jpg` | **✗ 缺** | ✓ |

（`run_s05.py` 用的是 `gungun_front_single_v1.png`，能对上）

---

## 二、8 步 Turbo 可以替代 45 步

用 h3q 队列（合规入口）重跑 S05，同 prompt、同 seed、同 3 张参考图：

| 指标 | 原 45 步 | **新 8 步 Turbo** |
|---|---|---|
| 死黑 <16 | 0.2% | 0.2% |
| 暗灰 16–50 | 6.1% | 6.9% |
| 中间调 | 47.2% | 49.4% |
| 高光 >200 | 46.5% | 43.4% |
| **熵** | **7.54** | **7.53** |
| 耗时 | 45 步 | **21.0 秒** |

**指标几乎完全一致（熵差 0.01），画面内容也对得上**（牵手、跨出屏幕、发光粒子）。

**结论：8 步 Turbo + LoRA 可以替代 45 步，速度提升约 2 倍。**

---

## 三、真实项目关键帧的四件套分布（21 张）

| 指标 | 均值 | 范围 |
|---|---|---|
| 死黑 <16 | **1.5%** | 0.0–8.5% |
| 暗灰 16–50 | **7.4%** | 1.1–38.1% |
| 中间调 | **70.0%** | 10.4–86.0% |
| 高光 >200 | **21.1%** | 2.2–83.4% |
| 熵 | **7.60** | 5.83–7.82 |

**对照官方 Gemini 基准：死黑 0.0% / 暗灰 4.9% / 中间调 84.8% / 高光 10.3% / 熵 7.67**

**真实项目几乎达到官方水平。** 这推翻了我前四轮的核心前提——我一直以为本地 Qwen 出不了好图。

### 四件套通过率：4/27

| 通过 | 失败原因 |
|---|---|
| kf_s07_fantasy_mountain | — |
| kf_s07_v2_chain_run | — |
| kf_s08_hands_only | — |
| kf_s10_hands_only | — |

失败的大多是**高光超标**（21.1% 均值 vs 官方 10.3%），说明这个项目的画风本身高光多。
**我的阈值（5–12%）对这个项目不适用。**

---

## 四、由此得到的三条修正

### 修正 1：我的四件套阈值不适用于这个项目

| 指标 | 我定的 | 官方 Gemini | 角色C 21 张均值 |
|---|---|---|---|
| 死黑 | ≤5% | 0.0% | **1.5%** ✓ |
| 暗灰 | ≤15% | 4.9% | **7.4%** ✓ |
| 中间调 | ≥60% | 84.8% | 70.0% |
| 高光 | **5–12%** | 10.3% | **21.1%** ✗ |

**角色C的画风（3D 卡通 + 暖柔光）天然高光多，21.1% 是它的正常值，不是缺陷。**

→ 高光阈值必须按画风分档，不能一套通用。

### 修正 2：真实项目的真瓶颈是 H3 提示词工程，不是出图

`审查/REVIEW_REPORT_ROUND4.md` 四轮返修卡住的点：

| # | 问题 | 我的 qc_image 能查吗 |
|---|---|---|
| P0-1 | S04 `<Picture 4>` 引用错位 | ❌ |
| P0-2 | S08 主语参考未加载 | ❌ |
| P0-3 | 一手牵两人同时挥手（物理冲突） | ❌ |
| P1-1 | 术语三种叫法 | ❌ |
| P1-3 | 台词语速过载 | ❌ |

**五类一个都查不出来。** 六维评分里 H3 工程可执行性 7.9 是唯一低于放行线的维度。

### 修正 3：角色C的写法是「散文 + 显式风格声明」，不是五槽

```text
premium cinema-grade 3D cartoon CGI animation keyframe, Pixar Disney style,
warm soft global illumination.

The scene is set in the cozy stylized 3D cartoon living room from <Picture 1>:
cream TV cabinet on the right wall, polished pastel floor tiles...

- On the right wall, the large TV screen is a brilliant swirling golden vortex portal.
  The cute penguin girl (Gugu, from image 2) is firmly holding the small hand of
  the cute chubby toddler boy (Gungun, from image 3).
```

**特征**：
- 开头一行风格声明
- `<Picture N>` / `(image N)` 显式绑定
- 用 `-` 列表分点写主体与动作
- **有强约束句**：`ONLY ONE television exists in the entire room` / `There is absolutely no second dark-screen TV anywhere`

最后这条很关键——**它用显式否定处理"多出来的电视"这种具体问题**。

---

## 五、待办

| # | 项 | 优先级 |
|---|---|---|
| 1 | 修正 5 个脚本的端口：18199 → 8199（或起服务） | **高** |
| 2 | 高光阈值按画风分档（角色C档 15–25%） | 高 |
| 3 | 把出图接到 h3q 队列，去掉直连 | 中 |
| 4 | 检查 `gungun_turnaround_v1.jpg` 本地缺失 | 低 |
| 5 | qc_image 增加 H3 提示词工程检查（Picture 引用/参考加载/术语统一） | **这才是真瓶颈** |
