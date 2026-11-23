#!/usr/bin/env python3
"""qc_image.py — 出图验收。三件套指标 + 画幅校验，退出码门控。

为什么不用「暗部占比 gray<50」：那个量纲在惩罚正常中间调。
Toonflow visualStyles.md 要的是「亮暗过渡柔和、暗部不死黑」，对应的是死黑占比。

三件套：
  死黑占比   gray < 16       目标 < 5%
  中间调占比 50 ≤ gray < 200  目标 > 60%
  灰度熵                     防平化护栏（为降暗部把画面写平，熵会掉）

用法：
    python3 qc_image.py <图片> --qc-profile cartoon3d
    python3 qc_image.py <目录> --qc-profile cartoon3d --baseline <基准目录> --json

自测（档位必须显式给，--baseline 不替代 --qc-profile）：
    python3 qc_image.py <图片> --baseline <基准目录> ; echo $?   # 期望退出码 2，列出 6 个档位

退出码：
    0  全部通过
    1  有图片未通过
    2  参数或文件错误
"""
import argparse
import json
import sys
from pathlib import Path

try:
    import cv2
    import numpy as np
except ImportError:
    print("ERROR: 需要 opencv-python 与 numpy", file=sys.stderr)
    sys.exit(2)

# 阈值（官方 Gemini 9 格实测：死黑均值 0.4%、中间调 84.8%、高光 10.3%）
#
# 为什么加「高光」这一项：本地全部产物 >200 占比 ≤3.4%，官方 10.3%。
# 我此前只盯死黑，把像素从 <16 搬进了 16–50，从未搬进 >200 ——
# 造出的是「均匀暗灰雾」，不是「被照亮的表面」（r3b：死黑 4.7% 达标，
# 但 16–50 飙到 71.5%、中间调仅 22.1%）。
# 真正要控的是直方图形状：16–50 压低，>200 抬起来。
#
# 阈值按画风分档。依据：
#   virtual-void（官方 Gemini 9 格「发光虚空」）: 死黑 0.0 / 暗灰 4.9 / 中间调 84.8 / 高光 10.3
#   cartoon3d（角色C EP01 21 张真实关键帧）    : 死黑 P50 0.5 / 暗灰 P50 6.3 / 中间调 P50 74.1 / 高光 P50 16.0
# 角色C是 3D 卡通+暖柔光，高光天然多（P10–P90 = 3.2%–45.8%），用虚空的 5–12% 卡它必然大面积误判。
PROFILES = {
    "virtual-void": {          # 发光虚空 / 大远景外景
        "dead_black_max": 5.0,
        "dark_gray_max": 15.0,
        "midtone_min": 60.0,
        "highlight_min": 5.0,
        "highlight_max": 12.0,
    },
    "cartoon3d": {             # 3D 卡通 / 暖柔光（角色C档）
        "dead_black_max": 5.0,
        "dark_gray_max": 15.0,
        "midtone_min": 55.0,   # 角色C P50 74.1，留余量
        "highlight_min": 5.0,
        "highlight_max": 28.0, # 角色C P50 16.0（P75 35.3 高于此线，故 28 只覆盖半数左右，按项目基准复核）
    },
    "interior": {              # 室内中近景（数据不足，暂用宽松档）
        "dead_black_max": 10.0,
        "dark_gray_max": 30.0, # 室内墙地顶天然暗灰多
        "midtone_min": 40.0,
        "highlight_min": 2.0,
        "highlight_max": 30.0,
    },
    # 以下两档来自《示例项目》EP01 v4 的 9 段成片实测（1312x736，各段首帧+中帧）。
    # 教训：单一全局档会把「场景本身的性质」当成缺陷——
    #   S01 客厅逆光窗 高光 32.1%（合法，窗就是过曝的）
    #   S08 航拍远山   暗灰 17.5-24.3%（合法，山体背光面）
    #   S09 双手挡屏   高光 3.6%（合法，画面被手掌压暗）
    # 这三类必须各自成档，否则门控变成噪声。
    "interior-backlit": {      # 室内 + 大面积过曝窗 / 门口强光
        "dead_black_max": 5.0,
        "dark_gray_max": 15.0,
        "midtone_min": 50.0,
        "highlight_min": 5.0,
        "highlight_max": 38.0, # 逆光窗可到 ~35%，超 40% 才是真的糊成白
    },
    "aerial-landscape": {      # 航拍 / 远景地景（山体背光面天然暗灰）
        "dead_black_max": 5.0,
        "dark_gray_max": 28.0, # 实测 17.5-24.3，取 28 留余量
        "midtone_min": 50.0,
        "highlight_min": 8.0,
        "highlight_max": 30.0,
    },
    "screen-occluded": {       # 主体大面积遮挡画面（手/门框/前景物压屏）
        "dead_black_max": 5.0,
        "dark_gray_max": 15.0,
        "midtone_min": 55.0,
        "highlight_min": 1.0,  # 遮挡物占大量像素时高光天然偏低
        "highlight_max": 28.0,
    },
}
# ---------------------------------------------------------------- 混合策略（2026-10-22 实测）
# 四带四指标不该用同一套判法。实测本片「目检 9/9 可用」的图，各指标片内极差差别极大：
#   死黑 22.3x / 暗灰 4.7x / 中间调 1.7x / 高光 7.2x
# 死黑与高光在同一部片里天然从 0 跨到 30+（外景 vs 室内特写），倍数判无意义；
# 暗灰/中间调片内较稳，可比。故：死黑/高光 → 绝对红线；暗灰/中间调 → 相对本片中位。
# 实测通过率：绝对档 3/9、默认档 1/9、本混合策略 9/9（目检 9/9 可用）。
HYBRID = {
    "dead_black_catastrophe": 40.0,
    "highlight_overexposed": 60.0,
    "dark_gray_rel_max": 3.0,
    "midtone_rel_min": 0.6,
}


def hybrid_check(bands: dict, base_bands: dict) -> dict:
    """分指标混合判据。base_bands = 本片基准（一组图的中位数）。"""
    db, dg = bands["lt16"], bands["b16_50"]
    md, hi = bands["b50_200"], bands["gt200"]
    checks = {
        "dead_black": {"value": db, "max": HYBRID["dead_black_catastrophe"],
                       "ok": db <= HYBRID["dead_black_catastrophe"],
                       "why": "死黑超灾难线（绝对：片内极差22x，倍数不可比）"},
        "highlight": {"value": hi, "max": HYBRID["highlight_overexposed"],
                      "ok": hi <= HYBRID["highlight_overexposed"],
                      "why": "高光过曝（绝对：片内极差7x，倍数不可比）"},
    }
    b_dg = base_bands.get("b16_50", 0) or 0
    if b_dg > 0:
        r = dg / b_dg
        checks["dark_gray"] = {"value": dg, "baseline": round(b_dg, 1),
                               "ratio": round(r, 2), "max_ratio": HYBRID["dark_gray_rel_max"],
                               "ok": r <= HYBRID["dark_gray_rel_max"],
                               "why": "暗灰超本片中位 %.1fx" % HYBRID["dark_gray_rel_max"]}
    else:
        checks["dark_gray"] = {"value": dg, "ok": True, "ratio": None, "why": "基准暗灰0，跳过"}
    b_md = base_bands.get("b50_200", 0) or 0
    if b_md > 0:
        r = md / b_md
        checks["midtone"] = {"value": md, "baseline": round(b_md, 1),
                             "ratio": round(r, 2), "min_ratio": HYBRID["midtone_rel_min"],
                             "ok": r >= HYBRID["midtone_rel_min"],
                             "why": "中间调低于本片中位 %.1fx" % HYBRID["midtone_rel_min"]}
    else:
        checks["midtone"] = {"value": md, "ok": True, "ratio": None, "why": "基准中调0，跳过"}
    return checks


# 仅作 measure()/基准加载的函数默认参数值；main() 要求显式给 --qc-profile 或 --baseline，
# 不会静默套用。保留常量是为了兼容直接调用 measure() 的旧脚本，不代表存在「默认档」。
DEFAULT_PROFILE = "virtual-void"

# 灾难线（任何档都必须过）：死黑 ≤40%。熵不作门控，只作记录。
CATASTROPHE_DEAD_BLACK = 40.0
# 实测熵 vs 死黑 r=-0.836、vs 亮度 +0.831、vs 中间调 +0.788，
# 它和明暗分布是同一根轴：熵低不是因为「平」，而是因为「暗」。故不设熵门控。

# 画幅：H3 canvas 边长须为 32 倍数
CANVAS_MULTIPLE = 32

# 目标图与基准图共用同一扩展名集合；基准加载曾接受 .jpeg/.webp 而目录扫描只认 .png/.jpg，
# 导致同目录下的 .jpeg 基准图被静默漏检。
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp"}

# 边框黑边归因环带宽度（占短边比例）。仅记录，不做门控。
BORDER_RING_FRACTION = 0.06


def measure(path: Path, profile: str = DEFAULT_PROFILE) -> dict:
    img = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if img is None:
        raise ValueError(f"无法读取: {path}")
    # 去 alpha
    if img.ndim == 3 and img.shape[2] == 4:
        img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    h, w = img.shape[:2]
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    hist = cv2.calcHist([gray], [0], None, [256], [0, 256]).ravel()
    p = hist / hist.sum()
    entropy = float(-(p[p > 0] * np.log2(p[p > 0])).sum())

    dead = float((gray < 16).mean() * 100)
    dark_gray = float(((gray >= 16) & (gray < 50)).mean() * 100)
    mid = float(((gray >= 50) & (gray < 200)).mean() * 100)
    highlight = float((gray >= 200).mean() * 100)
    dark50 = float((gray < 50).mean() * 100)   # 旧指标，仅记录，不做门控

    # 边框黑边归因：画面内有电视/门框/画框等嵌入式遮挡时，纯黑像素几乎全部
    # 落在外围环带，内区并不脏。仅记录并给判定线索，不参与 pass 计算。
    # 实测依据：S03 电视内嵌首帧 dead 8.48%，6% 外环 31.04%、内区 3.57%；
    # 同镜末帧边框出画后 dead 0.91%，外环 0.00%、内区 1.10%。
    ring = np.zeros((h, w), dtype=bool)
    band = max(1, int(min(h, w) * BORDER_RING_FRACTION))
    ring[:band, :] = True
    ring[-band:, :] = True
    ring[:, :band] = True
    ring[:, -band:] = True
    dead_mask = gray < 16
    border_dark = {
        "ring_fraction": BORDER_RING_FRACTION,
        "dead_in_ring": round(float(dead_mask[ring].mean() * 100), 2),
        "dead_in_inner": round(float(dead_mask[~ring].mean() * 100), 2),
        "inner_ok": bool(dead_mask[~ring].mean() * 100 <= PROFILES[profile]["dead_black_max"]),
    }

    T = PROFILES[profile]
    checks = {
        "dead_black": {"value": round(dead, 2), "max": T["dead_black_max"],
                       "ok": dead <= T["dead_black_max"]},
        "dark_gray": {"value": round(dark_gray, 2), "max": T["dark_gray_max"],
                      "ok": dark_gray <= T["dark_gray_max"]},
        "midtone": {"value": round(mid, 2), "min": T["midtone_min"],
                    "ok": mid >= T["midtone_min"]},
        "highlight": {"value": round(highlight, 2), "min": T["highlight_min"],
                      "max": T["highlight_max"],
                      "ok": T["highlight_min"] <= highlight <= T["highlight_max"]},
        "catastrophe": {"value": round(dead, 2),
                        "ok": dead <= CATASTROPHE_DEAD_BLACK},
        "canvas_w32": {"value": w, "ok": w % CANVAS_MULTIPLE == 0},
        "canvas_h32": {"value": h, "ok": h % CANVAS_MULTIPLE == 0},
    }
    return {
        "path": str(path),
        "qc_profile": profile,
        "size": [w, h],
        "luma_mean": round(float(gray.mean()), 2),
        "bands": {"lt16": round(dead, 2), "b16_50": round(dark_gray, 2),
                  "b50_200": round(mid, 2), "gt200": round(highlight, 2)},
        "legacy_dark50": round(dark50, 2),
        "border_dark": border_dark,
        "entropy": round(entropy, 2),
        "checks": checks,
        "pass": all(c["ok"] for c in checks.values()),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="出图验收：三件套指标 + 画幅校验")
    ap.add_argument("targets", nargs="+", help="图片路径或目录")
    ap.add_argument("--json", action="store_true", help="输出 JSON")
    ap.add_argument("--qc-profile", default=None, choices=list(PROFILES),
                    help="按画风分档取阈值（必填其一：本参数或 --baseline；无默认档）")
    ap.add_argument("--baseline", default=None,
                    help="本片基准目录（一组图的中位数）。给了就走分指标混合判据，"
                         "实测比绝对档准（本片 9/9 vs 3/9）")
    args = ap.parse_args()

    # 档位必须显式给；--baseline 只提供本片基准，不能替代档位，也不推导档位。
    # **禁止静默套用某个题材的默认档**：给 --baseline 但不给 --qc-profile 时曾静默
    # fallback 到 virtual-void，与「不再静默套默认档」矛盾，现改为显式报错。
    # 实测教训（2026-10-22）：原先 DEFAULT_PROFILE="virtual-void"（赛博发光虚空档，
    # 高光上限 12%）会静默套到 3D 卡通片上 —— 同一批 9 张图默认档只有 1/9 PASS，
    # 而正确档 3/9、人工目检 9/9 可用。静默误判比不跑更危险。
    if args.qc_profile is None:
        print("ERROR: 必须显式指定 --qc-profile <档>；--baseline 只提供本片基准，"
              "不能替代档位。", file=sys.stderr)
        print("       本脚本不再提供默认档：阈值与题材绑定，套错档会静默误判。", file=sys.stderr)
        print("       可用档: " + ", ".join(PROFILES), file=sys.stderr)
        print("       项目侧建议: <项目>/qc/profile.json 声明本片档位，"
              "<项目>/qc/baselines/<档>/ 放基准产物。", file=sys.stderr)
        return 2

    profile = args.qc_profile

    files = []
    for t in args.targets:
        p = Path(t)
        if p.is_dir():
            files += sorted(q for q in p.iterdir() if q.suffix.lower() in IMG_EXT)
        elif p.is_file():
            files.append(p)
        else:
            print(f"ERROR: 不存在: {p}", file=sys.stderr)
            return 2

    if not files:
        print("ERROR: 没有可检查的图片", file=sys.stderr)
        return 2

    # 基准中位数（给了 --baseline 才走混合判据）
    base_bands = None
    if args.baseline:
        bdir = Path(args.baseline)
        bfiles = (sorted(q for q in bdir.iterdir() if q.suffix.lower() in IMG_EXT)
                  if bdir.is_dir() else ([bdir] if bdir.is_file() else []))
        if not bfiles:
            print(f"ERROR: 基准路径无图: {bdir}", file=sys.stderr)
            return 2
        brows = []
        for bf in bfiles:
            try:
                brows.append(measure(bf, profile)["bands"])
            except ValueError as e:
                print(f"ERROR: 基准读取失败 {bf}: {e}", file=sys.stderr)
                return 2
        base_bands = {k: float(np.median([r[k] for r in brows]))
                      for k in ("lt16", "b16_50", "b50_200", "gt200")}

    results = []
    for f in files:
        try:
            r = measure(f, profile)
        except ValueError as e:
            print(f"ERROR: {e}", file=sys.stderr)
            return 2
        if base_bands is not None:
            hc = hybrid_check(r["bands"], base_bands)
            # 混合判据只替换四带指标；画幅（32 倍数）与灾难线是通道级硬约束，必须保留，
            # 否则 --baseline 模式下 canvas_w32/canvas_h32 检查会消失、非法画幅静默通过。
            for k in ("canvas_w32", "canvas_h32", "catastrophe"):
                if k in r["checks"]:
                    hc[k] = r["checks"][k]
            r["checks"] = hc
            r["pass"] = all(c["ok"] for c in hc.values())
            r["qc_mode"] = "hybrid"
        else:
            r["qc_mode"] = "absolute"
        results.append(r)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        print(f"{'文件':<30}{'<16':>6}{'16-50':>7}{'50-200':>8}{'>200':>6}{'熵':>6}{'画幅':>13}  判定")
        for r in results:
            c = r["checks"]
            w, h = r["size"]
            flag = "PASS" if r["pass"] else "FAIL"
            bad = [k for k, v in c.items() if not v["ok"]]
            note = f"  ← {','.join(bad)}" if bad else ""
            print(f"{Path(r['path']).name:<30}{c['dead_black']['value']:>6.1f}"
                  f"{c['dark_gray']['value']:>7.1f}{c['midtone']['value']:>8.1f}"
                  f"{c['highlight']['value']:>6.1f}{r['entropy']:>6.2f}"
                  f"{w:>6}x{h:<6}  {flag}{note}")
        n_pass = sum(1 for r in results if r["pass"])
        print(f"\n通过 {n_pass} / {len(results)}")
        if base_bands is not None:
            print(f"模式 [hybrid+baseline] 死黑<={HYBRID['dead_black_catastrophe']}%(绝对)  "
                  f"高光<={HYBRID['highlight_overexposed']}%(绝对)  "
                  f"暗灰<=本片中位x{HYBRID['dark_gray_rel_max']}  "
                  f"中调>=本片中位x{HYBRID['midtone_rel_min']}")
            print(f"  基准中位: 死黑 {base_bands['lt16']:.1f} 暗灰 {base_bands['b16_50']:.1f} "
                  f"中调 {base_bands['b50_200']:.1f} 高光 {base_bands['gt200']:.1f}")
            print("  实测依据: 本片 9 张目检可用, 绝对档只过 3/9, 本混合判据 9/9")
        else:
            T = PROFILES[profile]
            print(f"档位 [{profile}]（显式指定·绝对）死黑<={T['dead_black_max']}%  "
                  f"16-50<={T['dark_gray_max']}%  中间调>={T['midtone_min']}%  "
                  f"高光 {T['highlight_min']}-{T['highlight_max']}%")
            print("⚠️ 绝对档会按指标自身噪声误杀（实测本片 3/9）。建议加 --baseline 走混合判据。")

    return 0 if all(r["pass"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
