#!/usr/bin/env python3
"""ref_guard.py — 参考图提交前检查（专拦「拼版参考图被当构图模板」）。

为什么需要
----------
实测：本地 Qwen Image 2.1 在「短词（264 字）+ 挂拼版参考图（角色四视图 + 场景板）」
条件下曾观察到「人脸贴片」——模型把参考图的**版面**当成了构图模板复现（小样本实测观察（样本与复现命令未随公开版发布））。
换长词、去掉参考图、或改宫格结构都能消除，但**最省事的是别把拼版图喂进去**。
本脚本就做这一件事：在提交前把拼版图拦下来。

适用语境（2026-10-30 补，勿外推）
--------------------------------
本判据只针对**静帧出图**（Qwen Image 等 i2i/文生图）：那里拼版图的版面会被当成构图模板复现。
**H3 视频的 Ref2VA 不适用本判据**：多视图板在 Ref2VA 里是合法的身份来源（同一个 `<Subject N>`
可引用多张图；官方模型图像上限 9 张），把正/侧/背几格当身份参考是正确用法，不是"拼版风险"。
同一张图在两条链路里的身份不同：静帧里可能是构图模板，Ref2VA 里是身份卡。判定前先问"这张图进哪条链路"。

**2026-11-01 创作者裁决：层1「贯穿线」判据停用**
--------------------------------------------
门框、墙线、栏杆等画面自身的长直线会被误判成拼版分割线（本项目 001 门口场景板实测误拦）。
创作者要求彻底去掉该判据，视频模态也不例外。`span_lines()` / `edge_contact()` 作为
兼容契约保留，但不再参与判定，`span_lines` 对外恒为 0。现在只剩「多主体面板」告警
（first_frame 链路阻断，其余链路不阻断）。

**2026-10-30 现场复测（本机真实资产，两条判据均失效）**
----------------------------------------------------------------
拿本项目实际在用的两张图跑：`example_turnaround_v1.jpg`（AI 无缝四视图）与一张
带明显分栏的场景资产板（2560×1440）——**贯穿线 0 条、多主体面板 0 个，三条链路全部 PASS**。
结论：这套图像判据对"AI 生成的无缝拼版"基本不产生信号。它拦得住的只是**官方那种带显式
分割线的拼版**（下表 81% 那一行），而那类图在短剧项目里极少当参考喂。

⇒ 因此本脚本的定位改成**参考图体检 + 链路提示**，不再把图像判据当准入闸：
   - **2026-11-01：层1「贯穿线」判据已停用**（误杀门框/墙线/栏杆等画面自身长直线），任何链路都不阻断；
   - `--chain still`（默认）：多主体面板只告警；
   - `--chain ref2va`：多视图板是**合法身份来源**，多主体面板只告警；
   - `--chain first_frame`：首/尾帧必须是单画面，多主体面板命中才阻断（模式语义，不是图像判据）；
   - 任何链路下，挂了参考就核对 `--prompt` 里的**版面压制句**——那才是真正拦得住的东西。

实测有效性（2026-10-22 分来源标定，同一套样本跑两层判据）
----------------------------------------------------------
本判据的有效性**高度依赖参考图的来源**，必须分开看：

| 样本集 | n | 层1 贯穿线（阻断） | 层2 多主体面板（告警） | 两层合计 |
|---|---|---|---|---|
| 官方带线拼版（props/characters/grid） | 227 | **184 = 81.1%** | 8 = 3.5% | 186 = 81.9%（两层合计，按去重计） |
| **AI 生成的无缝三视图 / 表情板** | 18 | **0 = 0%** ⚠️ | **11 = 61.1%** | 11 = 61.1% |
| 单张成品 / 关键帧（不该命中） | 12 | 0 | 0 | **0（无误报）** |
| example-project 其他产物（不该命中） | 506 | 20 = 4.0% | 41 = 8.1% | 57 = 11.3%（两层合计，按去重计） |

⇒ 关键结论：**贯穿线只对「带显式分割线的拼版」有效（81%）；
对「AI 生成的无缝三视图」全军覆没（0/18）。**

而实际提交里喂进去的参考图，**恰恰是后者**——角色三视图是 Qwen 出的图，
面板之间无分割线、背景同为纯色，Canny 在分割处出不来边缘。
所以「过 ref_guard」≠「参考图安全」。这一条必须记住。

误拦（贯穿线命中但并非拼版）20/506 的来源：画面自身的长直线
（电视边框、墙线、天花板灯带、上下黑边 banner），不是分割线 ——
单靠几何直线**无法区分**这两者。

原表（本机 5 个已知样本）仍然成立，只是**它测的全是带线的官方样本**：

| 样本                       | 贯穿线 | 判定 |
|----------------------------|--------|------|
| 角色四视图（拼版）          |   4    | 拦 ✓ |
| 道具三视图（拼版）          |  12    | 拦 ✓ |
| 9 宫格合成（拼版）          |   7    | 拦 ✓ |
| 单张角色图（单主体，5504px）|   0    | 放 ✓ |
| example-project S09（单帧）        |   0    | 放 ✓ |
| **场景四视图（拼版）**      | **0**  | **漏 ⚠️** |

（旧稿此处写「16/488」，为另一统计窗口；以本文件上方实测表的 20/506 为准，两次统计窗口不同，未复算。）误拦来源：画面自身的长直线（电视边框、墙线、天花板灯带、上下黑边 banner），
不是分割线 —— 单靠几何直线**无法区分**这两者。

判据试错记录（全部否决，别重走）
------------------------------
| 备选判据 | 结果 | 否决原因 |
|---|---|---|
| `maxLineGap` 8→10 | 官方样本拦住率没涨，非拼版误拦 20→27 | 放大阈值只是多抓画面自身的线 |
| `maxLineGap` 8→24 | 误拦 114/535（21%） | 同上，严重不可用 |
| 标准 `HoughLines` + 端点覆盖校验 | 单张成品误拦 9/12 | 水平结构（地平线、家具线）全被当分割线 |
| 边缘投影覆盖率（列/行覆盖率≥0.8） | 合成拼版可拦，真实三视图仍 0/18，且误拦成品 | 覆盖率与内容线冲突 |
| 裁掉四周纯色边框后再测 | `atan_ref_netcafe` 从 2 条降到 1 条 | 黑边只是误报来源之一，裁了仍漏判真拼版 |
| 「规则 N 等分网格规整度」σ/μ | 场景四视图 0.067 vs 单帧 S09 0.081 | 范围重叠，加了只会误杀单帧 |

⇒ 因此本脚本定位是**兜底提示**，不是完备门控：
   层1（贯穿线）已于 2026-11-01 停用；现在只有层2多主体面板告警，不阻断。
   **最终仍需人工/多模态过一眼「这张参考图是不是多主体拼版」。**
   **通过 ≠ 安全**，不要把 exit 0 当成放行凭证。

第二层：「多主体面板」告警（专补无缝拼接，只提醒不阻断）
--------------------------------------------------------
既然线抓不到无缝拼版，换一条与线无关的信号：**画面里有几个大小相近的主体**。
角色三视图 = 3 个几乎等大的角色并排；单张成品 = 1 个主体。

实测（与上表同一批样本）：

| 组 | n | 本层告警 |
|---|---|---|
| AI 生成无缝三视图 / 表情板 | 18 | **11 = 61.1%**（层1 为 0%，完全互补） |
| 单张成品 / 关键帧 | 12 | **0**（不误报） |
| example-project 其他产物 | 506 | 41 = 8.1% |

⇒ 与贯穿线**互补**：贯穿线在无缝三视图上 0/18，本告警补到 11/18。
⇒ 但它**只做告警不做阻断**：非拼版仍有 8.1% 命中（双人/群体/道具同框都会中招），
   拿它阻断会误杀。判据是背景差分 + 连通域，对「同色背景上的多主体」有效，
   对「复杂背景里的多人」无效。
⇒ 剩下的 7/18（表情板 n=1 或主体不等大）机器判不出来，只能人眼。

其他三条硬规则（同样实测支持）
----------------------------
2. **纵横比同向**：竖图参考不得用于横画幅目标（实测「单人全身竖图 → 人物彻底消失」）。
   ⇒ 这条比贯穿线**可靠得多**，是本脚本目前最有价值的判据。
3. **长边压到 768 + JPEG q80**：压后画面更干净（参考图噪点不再被放大）。
4. **主体不贴边**：曾试「画框边缘非背景像素 >60% → 主体被切到画框外」，
   实测单张正常图也能到 91–100%，判据不可分，**已删**。需要真检测器才能做。

用法
----
    python3 ref_guard.py <参考图...> [--target-aspect 16:9] [--json]
退出码：0 全部通过；1 有拦截项；2 参数错误
"""
import argparse
import json
import sys
from pathlib import Path

# Windows 控制台默认 GBK，emoji/中文 print 会 UnicodeEncodeError 直接崩，
# 退出码 1 会被 h3qg 误判成「闸门拦截」。先把 stdout 钉成 UTF-8。
for _s in (sys.stdout, sys.stderr):
    try:
        _s.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

try:
    import cv2
    import numpy as np
except ImportError as e:
    sys.stderr.write(
        "ERROR: 缺少依赖 %s。ref_guard 需要 opencv-python + numpy，"
        "请先 pip install opencv-python-headless numpy 再运行。\n" % e.name
    )
    sys.exit(2)

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}

SPAN_RATIO = 0.80        # 【已停用 2026-11-01】贯穿线长度阈值；span_lines() 不再参与判定
SPAN_THICK = 0.03        # 视为「近似水平/垂直」的厚度容差
LONG_SIDE_MAX = 768      # 参考图长边上限
EDGE_BAND = 0.02         # 贴边检测的边框带宽


def _load(path: Path):
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"无法读取: {path}")
    if img.ndim == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return img


def span_lines(gray):
    """【已停用 2026-11-01，仅为兼容契约保留】找贯穿画幅的近似水平/垂直线。

    门框/墙线/栏杆等画面自身的长直线会被误判成拼版分割线，创作者裁决停用该判据。
    本函数不再参与 check() 判定，对外 `span_lines` 计数恒为 0。
    """
    h, w = gray.shape
    edges = cv2.Canny(gray, 50, 150)
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100,
                            minLineLength=int(min(h, w) * SPAN_RATIO), maxLineGap=8)
    hits = []
    if lines is None:
        return hits
    for l in np.asarray(lines).reshape(-1, 4):
        x1, y1, x2, y2 = (int(v) for v in l)
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        if dx > w * SPAN_RATIO and dy < h * SPAN_THICK:
            hits.append({"dir": "H", "len": dx, "of": w})
        elif dy > h * SPAN_RATIO and dx < w * SPAN_THICK:
            hits.append({"dir": "V", "len": dy, "of": h})
    return hits


def edge_contact(gray: np.ndarray) -> float:
    """【弱提示，未参与判定】画面四边窄带里非背景像素占比（主体贴边的弱信号）。

    实测单张正常角色图也能到 91–100%，判据不可分，保留仅为兼容契约，不参与 check()。
    """
    h, w = gray.shape
    b = max(1, int(min(h, w) * EDGE_BAND))
    med = float(np.median(gray))
    bands = [gray[:b, :], gray[-b:, :], gray[:, :b], gray[:, -b:]]
    vals = []
    for band in bands:
        vals.append(float((np.abs(band.astype(np.float32) - med) > 25).mean() * 100))
    return max(vals) if vals else 0.0


def multi_subject_panels(gray: np.ndarray,
                         min_pct: float = 0.02,
                         cv_max: float = 0.35,
                         sum_min_pct: float = 30.0):
    """数「大小相近的多个主体」——专补无缝拼接的三视图（贯穿线抓不到的那种）。

    判据：背景 = 画面四角的中位亮度；与背景差 >35 的像素算内容；
    形态学整理后取连通域，只留面积 > 画幅 min_pct 的，再要求：
      · 主体数 ≥ 2
      · 面积变异系数 σ/μ < cv_max（各面板**几乎等大** → 是摆版，不是构图）
      · 合计占画幅 > sum_min_pct
    三条同时成立才告警。只告警、不阻断——非拼版仍有 8.1% 命中（41/506，见文件头实测表）。
    """
    h, w = gray.shape
    qh, qw = max(1, h // 12), max(1, w // 12)
    corners = np.concatenate([gray[:qh, :qw].ravel(), gray[:qh, -qw:].ravel(),
                              gray[-qh:, :qw].ravel(), gray[-qh:, -qw:].ravel()])
    bg = float(np.median(corners))
    m = (np.abs(gray.astype(np.float32) - bg) > 35).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((7, 7), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((25, 25), np.uint8))
    n, _lab, st, _c = cv2.connectedComponentsWithStats(m, 8)
    tot = float(h * w)
    big = sorted([int(st[i, cv2.CC_STAT_AREA]) for i in range(1, n)
                  if st[i, cv2.CC_STAT_AREA] > tot * min_pct], reverse=True)
    if len(big) < 2:
        return {"n": len(big), "cv": None, "sum_pct": round(sum(big) * 100.0 / tot, 1)}
    cv_ = float(np.std(big) / np.mean(big))
    sum_pct = sum(big) * 100.0 / tot
    return {"n": len(big), "cv": round(cv_, 3), "sum_pct": round(sum_pct, 1),
            "panel": bool(cv_ < cv_max and sum_pct > sum_min_pct)}


CHAINS = {"still", "ref2va", "first_frame"}

SUPPRESS_PATTERNS = (
    "no grid lines", "no split screen", "no panels", "no panel borders",
    "one continuous frame", "single continuous frame", "one subject in one",
    "do not reproduce panels", "not a storyboard", "only the character",
    "不输出分格", "没有分格线", "单人单画面",
)


def prompt_suppresses_layout(text: str) -> bool:
    low = text.lower()
    return any(p in low for p in SUPPRESS_PATTERNS)


def check(path: Path, target_aspect=None, chain="still", prompt_text="") -> dict:
    chain = chain if chain in CHAINS else "still"
    img = _load(path)
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    issues = []
    warns = []

    # 2026-11-01：层1「贯穿线」判据已按创作者要求停用（误杀门框/墙线等），不再参与判定。
    # span_lines() 作为兼容契约保留，恒不命中；只保留多主体面板判据。
    hits = []   # span_lines(gray) 已停用：恒为空，对外 span_lines 计数恒为 0
    ms = multi_subject_panels(gray)

    if ms.get("panel"):
        msg = (f"画面里有 {ms['n']} 个**大小相近**的主体（面积变异系数 {ms['cv']}，"
               f"合计占画幅 {ms['sum_pct']}%）→ 疑似无缝拼接的多视图面板")
        if chain == "first_frame":
            # 首帧/尾帧是闸门：并排多主体会被直接画进画面，必须 BLOCK。
            # 降为告警会放行废片（issue #32-1 回归），故此链路恢复阻断。
            issues.append(msg + "；作首帧/尾帧时并排多主体会被直接画进画面")
        elif chain == "still":
            warns.append(msg + "（历史实测：贯穿线判据对这种图 0/18 全漏，靠本条兜；仍不阻断，请人眼确认）")
        else:
            warns.append(msg + "；Ref2VA 里这是标准身份卡形态，确认只取身份不取版面即可")

    # 图像判据对 AI 无缝拼版实测 0 检出（本机四视图与资产板各测一次，贯穿线均为 0），
    # 所以真正的抓手在正文：挂了参考就核对"有没有说明用途/压制版面"。
    # still 是静帧拼版复现风险最高的链路（h3qg.py 图片提交走 still），同样核对。
    # 任何链路只要传了 --prompt，就核对版面压制句。
    if prompt_text:
        if not prompt_suppresses_layout(prompt_text):
            warns.append("正文里没有版面压制句（no grid lines / no split screen / "
                         "one continuous frame）。若这批图含多视图板或分镜板，"
                         "模型可能把版面画进画面；单张人物图可忽略本条")
    else:
        warns.append("未传 --prompt：无法核对正文是否说明了参考用途与版面压制。"
                     "挂多视图板或分镜板时这条必须查（图像判据漏检率极高）")

    if target_aspect:
        try:
            tw, th = (float(x) for x in target_aspect.split(":"))
            tgt = tw / th
            cur = w / h
            if (cur > 1) != (tgt > 1):
                issues.append(f"参考图 {w}x{h}（{'横' if cur > 1 else '竖'}）"
                              f"与目标画幅 {target_aspect}（{'横' if tgt > 1 else '竖'}）**不同向**"
                              f"—— 实测「单人全身竖图用于横画幅」会导致人物彻底消失")
        except (ValueError, ZeroDivisionError):
            warns.append(f"--target-aspect 格式不对（应如 16:9），本条跳过")

    long_side = max(w, h)
    if long_side > LONG_SIDE_MAX:
        warns.append(f"长边 {long_side}px > {LONG_SIDE_MAX}px：若这是身份板/资产板，建议压到 "
                     f"{LONG_SIDE_MAX}px + JPEG q80；若是首帧、起始状态或构图参考，保持无损原尺寸，不要压")

    # 注：曾加过「画框边缘非背景像素占比 >60% → 疑似主体被切到画框外」的弱提示，
    # 实测无效——单张正常角色图也能到 91-100%（背景本身不是纯色），
    # 判据不可分，已删除。主体贴边检测需要真检测器，见文件头说明。

    return {
        "path": str(path),
        "size": [w, h],
        "span_lines": len(hits),
        "chain": chain,
        "issues": issues,
        "warns": warns,
        "pass": not issues,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="参考图体检（层1贯穿线判据已停用；层2多主体面板 first_frame 阻断、其余告警）")
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--target-aspect", default=None, help="目标画幅，如 16:9")
    ap.add_argument("--chain", default="still", choices=sorted(CHAINS),
                    help="这张图进哪条链路：still=静帧出图（默认，最严）/ "
                         "ref2va=H3 多槽参考（身份卡与 storyboard 合法）/ "
                         "first_frame=首帧或尾帧（必须是单画面）")
    ap.add_argument("--prompt", default=None,
                    help="提示词文件路径；给了就核对正文是否含版面压制句")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    files = []
    for t in args.targets:
        p = Path(t)
        if p.is_dir():
            files += sorted(q for q in p.iterdir() if q.suffix.lower() in IMG_EXT)
        elif p.is_file():
            files.append(p)
        else:
            print(f"ERROR: 不存在 {p}", file=sys.stderr)
            return 2
    if not files:
        print("ERROR: 没有可检查的文件", file=sys.stderr)
        return 2

    prompt_text = ""
    if args.prompt:
        try:
            prompt_text = Path(args.prompt).read_text(encoding="utf-8")
        except OSError as e:
            print(f"ERROR: 读不到 prompt 文件 {args.prompt}: {e}", file=sys.stderr)
            return 2

    results = []
    for f in files:
        try:
            results.append(check(f, args.target_aspect, args.chain, prompt_text))
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for r in results:
            w, h = r["size"]
            print(f"{Path(r['path']).name}  ({w}x{h})  贯穿线 {r['span_lines']}  "
                  f"{'PASS' if r['pass'] else 'REJECT'}")
            for i in r["issues"]:
                print(f"   ✗ {i}")
            for x in r["warns"]:
                print(f"   ! {x}")
        n_rej = sum(1 for r in results if not r["pass"])
        n_panel = sum(1 for r in results
                      if any("大小相近" in x for x in r["issues"] + r["warns"]))
        print(f"\n需拦截 {n_rej} / {len(results)}；多主体面板命中 {n_panel} / {len(results)}")
        print("⚠️ 层1「贯穿线」阻断判据已于 2026-11-01 移除（它误杀门框/墙线/栏杆等画面自身长直线）。")
        print("   层2「多主体面板」在 first_frame 链路阻断（首帧并排多主体会被画进画面），"
              "其余链路只告警；通过 exit 0 **不等于**参考图安全。")
        print("   ⇒ 拼版/多主体仍需人眼确认，剩余 7/18 机器判不出。")

    return 1 if any(not r["pass"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())