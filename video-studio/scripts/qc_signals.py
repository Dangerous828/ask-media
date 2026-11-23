#!/usr/bin/env python3
"""qc_signals.py — 介质/氛围信号（四带查不出来的那一半）。

为什么需要这个脚本
------------------
四带（死黑/暗灰/中间调/高光）只测亮度分布，对「介质」完全盲。实测证据：

| 图               | 死黑 | 暗灰 | 中间调 | 高光 | 小亮块 | 最大亮块% |
|------------------|------|------|--------|------|--------|-----------|
| 官方 ref_grid01  | 0.0  | 4.9  | 84.8   | 10.3 | **519**| 4.99      |
| example-project S09     | 0.5  | 4.1  | 90.7   | 4.7  | **106**| 2.36      |

S09 四带两档全 PASS、目检可用，但小亮块只有官方的 1/5 —— 四带看不出「粒子密度」这一维。

三个信号（全部**相对判定**，无绝对阈值）
--------------------------------------
1. 小亮块密度  `>200` 连通块中面积 `<0.02%` 画幅的**个数** → 粒子/代码流/火花
2. 最大亮块%   `>200` 最大连通块占画幅比 → 体积光/大光源是否成面
3. 高频/小亮块 Laplacian 均值 ÷ 小亮块数 → 比值异常高 = 噪点/脏图告警

**必须归一化到 464×256 再算。** 块数类信号对分辨率敏感，
不同尺寸直接比是分辨率伪影，不是内容差异。

**跨题材量级差 3–5.5 倍**（实测 官方 393 / ours9 130 / example-project 72），
所以绝对阈值必然误判，一律与基准帧比。

被否决的信号（别再试）
--------------------
- **纵深离散**（各横条锐度离散度）：实测官方 0.192 最低、可用组 0.539 最高，
  **方向与假设相反**，「有纵深 → 离散大」不成立。
- **高频能量单用**：off_pipe 高频 31.60 高于官方 ref_grid01 的 22.30，但它是废片
  （暗灰 45.6%）。噪点与粒子在此信号上不可分，只能与小亮块成对使用。
- **色相集中绝对门控**：组均值看似可分，但 example-project S09 单张偏低且完全可用。
  只能做同场景跨镜漂移量，不做单帧质量门。

用法
----
    python3 qc_signals.py <图片或目录> --baseline <基准图 或 基准目录>
    python3 qc_signals.py shot.png --baseline <项目>/qc/baselines/cartoon3d/best.png
    python3 qc_signals.py <目录> --baseline <基准> --json

退出码
------
    0  检查完成（默认 advisory 模式下 ok 恒真，低于基准只写进 advisory，不返回 1）
    1  仅 --strict 门控模式下有信号低于基准容差（介质不足 / 脏图）；默认模式永不返回 1
    2  参数错误或基准缺失（**不给 --baseline 一律拒绝运行**）
"""
import argparse
import json
import sys
from pathlib import Path

import cv2
import numpy as np

# 归一化尺寸：块数类信号必须在此尺寸下计算，否则跨分辨率不可比
NORM_W, NORM_H = 464, 256

# 亮度阈值与块面积上限
BRIGHT_THR = 200
SMALL_BLOCK_FRAC = 0.0002     # 0.02% 画幅

# 相对容差：候选 / 基准
#
# ⚠️ 实测教训（2026-10-22，本机复验）——不要把这些信号当门控：
#
# 先用「单张 best.png 当基准、候选须 ≥基准×0.7」判**已知好**的两个集合，结果
# 官方 9 格只有 2/9 PASS、example-project（目检 9/9 可用）只有 4/9 PASS。
# 追因：**同题材好图的组内极差本来就有 3.7–6.5 倍**
#   · 官方 9 格小亮块逐张：175 253 280 291 328 506 519 547 639
#   · example-project 逐张：      20 20 50 51 68 98 100 106 131
# 0.7 容差要求组内极差 <1.43 倍，数学上必误杀。
#
# 更关键：**好/差两组的区间是重叠的**
#   · 官方（好）min = 175；ours9（差）max = 318
#   · ours9 里有 3/9 张的小亮块数 ≥ 官方最差者
#   · 若拿「官方 min=175」当 FAIL 线，会误杀 example-project 9/9（其 min=20）
#
# 结论：小亮块密度只在**同题材、同镜型**内才有弱区分力，跨题材绝对不可比。
# 因此本脚本的定位是 **告警（advisory）**：默认只报告偏差，不作 PASS/FAIL 门控。
# 需要门控时用 --strict，并自担误杀风险。
TOL_SMALL_BLOCKS = 0.50      # 告警线：候选 < 基准中位数 ×0.50 → 提示介质可能不足
TOL_MAX_BLOCK = 0.50         # 告警线：最大亮块 < 基准中位数 ×0.50
RATIO_DIRTY = 4.0            # 告警线：高频/小亮块 比 > 基准中位数 ×4 → 提示噪点/脏

IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp", ".tif", ".tiff"}


def _load_norm(path: Path) -> np.ndarray:
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"无法读取: {path}")
    if img.ndim == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    if img.ndim == 2:
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    return cv2.resize(img, (NORM_W, NORM_H), interpolation=cv2.INTER_AREA)


def signals(path: Path) -> dict:
    """算三个介质信号。全部在归一化 464x256 上计算。"""
    img = _load_norm(path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    mask = (gray > BRIGHT_THR).astype(np.uint8)
    n_lab, _lab, stats, _cent = cv2.connectedComponentsWithStats(mask, 8)
    total = gray.shape[0] * gray.shape[1]

    areas = [int(stats[i, cv2.CC_STAT_AREA]) for i in range(1, n_lab)]
    small_blocks = sum(1 for a in areas if a < total * SMALL_BLOCK_FRAC)
    max_block_pct = (max(areas) / total * 100) if areas else 0.0

    lap = float(np.abs(cv2.Laplacian(gray.astype(np.float32), cv2.CV_32F)).mean())
    # 高频/小亮块比：小亮块为 0 时用 1 兜底，避免除零放大
    dirty_ratio = lap / max(small_blocks, 1)

    return {
        "path": str(path),
        "size_orig": _orig_size(path),
        "small_blocks": int(small_blocks),
        "max_block_pct": round(float(max_block_pct), 3),
        "high_freq": round(lap, 3),
        "dirty_ratio": round(float(dirty_ratio), 4),
    }


def _orig_size(path: Path):
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        return [0, 0]
    return [int(img.shape[1]), int(img.shape[0])]


def resolve_baseline(p: Path):
    """基准可以是：单张图 / 一组图的目录 / 含 best.png 的档目录。

    返回 (基准统计 dict, 说明文本)。目录一律取**全部图的分布**（中位数），
    不用单张——单张做基准会被组内极差（实测 3.7–6.5 倍）放大成误杀。
    """
    if p.is_file():
        s = signals(p)
        return {**s, "n": 1, "kind": "single"}, f"单张 {p.name}（建议改用一组图）"
    if p.is_dir():
        imgs = sorted(q for q in p.iterdir() if q.suffix.lower() in IMG_EXT)
        # 档目录里常只有 best.png；它的同级若有更多图则全部纳入
        if not imgs:
            raise ValueError(f"基准目录内无图: {p}")
        rows = [signals(q) for q in imgs]
        return {
            "n": len(rows), "kind": "set",
            "small_blocks": int(np.median([r["small_blocks"] for r in rows])),
            "max_block_pct": round(float(np.median([r["max_block_pct"] for r in rows])), 3),
            "high_freq": round(float(np.median([r["high_freq"] for r in rows])), 3),
            "dirty_ratio": round(float(np.median([r["dirty_ratio"] for r in rows])), 4),
            "spread": {
                "small_blocks_min": min(r["small_blocks"] for r in rows),
                "small_blocks_max": max(r["small_blocks"] for r in rows),
            },
            "_rows": [r["path"] for r in rows],
        }, f"{len(rows)} 张的中位数 {p}"
    raise ValueError(f"基准不存在: {p}")


def compare(cand: dict, base: dict, strict: bool = False) -> dict:
    """与基准比，全部用相对量。

    strict=False（默认）：只告警，ok 恒为 True，问题写进 `advisory`。
    strict=True：低于容差即判 not ok（**自担误杀风险**，见文件头实测说明）。
    """
    checks = {}

    def add_small():
        b = base["small_blocks"]
        if b <= 0:
            return {"value": cand["small_blocks"], "baseline": 0, "ratio": None,
                    "ok": True, "advisory": None,
                    "why": "基准无小亮块，此信号对本档不适用（记录用）"}
        r = cand["small_blocks"] / b
        low = r < TOL_SMALL_BLOCKS
        return {"value": cand["small_blocks"], "baseline": b, "ratio": round(r, 3),
                "min_ratio": TOL_SMALL_BLOCKS,
                "ok": (not strict) or (not low),
                "advisory": ("粒子/介质密度可能不足（低于基准中位数 50%）" if low else None),
                "why": "粒子/介质密度不足" }

    def add_max():
        b = base["max_block_pct"]
        if b <= 0:
            return {"value": cand["max_block_pct"], "baseline": 0, "ratio": None,
                    "ok": True, "advisory": None,
                    "why": "基准无大亮块，此信号对本档不适用（记录用）"}
        r = cand["max_block_pct"] / b
        low = r < TOL_MAX_BLOCK
        return {"value": cand["max_block_pct"], "baseline": b, "ratio": round(r, 3),
                "min_ratio": TOL_MAX_BLOCK,
                "ok": (not strict) or (not low),
                "advisory": ("体积光/大光源可能未成面（低于基准中位数 50%）" if low else None),
                "why": "体积光/大光源未成面"}

    def add_dirty():
        b = base["dirty_ratio"]
        if b <= 0:
            return {"value": cand["dirty_ratio"], "baseline": 0, "ratio": None,
                    "ok": True, "advisory": None, "why": "基准比值为 0，跳过"}
        r = cand["dirty_ratio"] / b
        high = r > RATIO_DIRTY
        return {"value": cand["dirty_ratio"], "baseline": b, "ratio": round(r, 3),
                "max_ratio": RATIO_DIRTY,
                "ok": (not strict) or (not high),
                "advisory": ("高频相对小亮块异常高，疑似噪点/脏图而非粒子" if high else None),
                "why": "噪点/脏图"}

    checks["small_blocks"] = add_small()
    checks["max_block_pct"] = add_max()
    checks["dirty_ratio"] = add_dirty()
    return checks


def main() -> int:
    ap = argparse.ArgumentParser(description="介质/氛围信号（相对基准判定）")
    ap.add_argument("targets", nargs="+", help="图片路径或目录")
    ap.add_argument("--baseline", required=True,
                    help="基准图或基准目录（必需：本脚本无默认档，见文件头说明）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="把告警升级为门控（低于容差即 FAIL）。默认只告警——"
                         "实测好/差两组区间重叠，绝对门控会误杀，见文件头说明")
    args = ap.parse_args()

    try:
        base, base_desc = resolve_baseline(Path(args.baseline))
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("ERROR: 必须提供 --baseline（基准图或一组图的目录）。"
              "绝对阈值在跨题材时数学上必错（实测差 3–5.5 倍），故本脚本拒绝无基准运行。",
              file=sys.stderr)
        return 2

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

    results = []
    for f in files:
        try:
            cand = signals(f)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        checks = compare(cand, base, strict=args.strict)
        results.append({**cand, "checks": checks,
                        "advisories": [c["advisory"] for c in checks.values() if c.get("advisory")],
                        "pass": all(c["ok"] for c in checks.values())})

    if args.json:
        print(json.dumps({"baseline": base, "strict": args.strict, "results": results},
                         ensure_ascii=False, indent=1))
    else:
        mode = "门控(strict)" if args.strict else "告警(advisory，默认)"
        print(f"基准: {base_desc}  {mode}")
        print(f"      小亮块 {base['small_blocks']}  最大亮块 {base['max_block_pct']}%  "
              f"高频/块 {base['dirty_ratio']}"
              + (f"  组内范围 {base['spread']['small_blocks_min']}–{base['spread']['small_blocks_max']}"
                 if base.get("spread") else ""))
        print(f"{'文件':<32}{'小亮块':>8}{'比':>7}{'最大亮块%':>10}{'比':>7}{'高频/块':>9}{'比':>7}  提示")
        n_adv = 0
        for r in results:
            c = r["checks"]
            def rs(k):
                v = c[k]["ratio"]
                return "—" if v is None else f"{v:.2f}"
            adv = r["advisories"]
            if adv:
                n_adv += 1
            tag = ("告警: " + "; ".join(a.split("（")[0] for a in adv)) if adv else "—"
            print(f"{Path(r['path']).name:<32}{r['small_blocks']:>8}{rs('small_blocks'):>7}"
                  f"{r['max_block_pct']:>10}{rs('max_block_pct'):>7}"
                  f"{r['dirty_ratio']:>9}{rs('dirty_ratio'):>7}  {tag}")
        print(f"\n有告警 {n_adv} / {len(results)}")
        print(f"告警线：小亮块 <基准×{TOL_SMALL_BLOCKS}  最大亮块 <基准×{TOL_MAX_BLOCK}  "
              f"高频/块 >基准×{RATIO_DIRTY}（全部相对）")
        print("⚠️ 本信号组**默认只告警不门控**：实测好/差两组区间重叠（官方 min=175 vs "
              "ours9 max=318），\n   拿绝对线会误杀 example-project 9/9。要门控请加 --strict 并自担误杀风险。")

    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())