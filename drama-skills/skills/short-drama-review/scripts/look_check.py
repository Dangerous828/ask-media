#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""画风验收：把生成媒体与项目已登记的画风基准帧并排量化比较，并记录人工复核。

机械层计算全幅统计信号；只有景别、主体比例、景深等可比时才用于质量筛查。
可比性默认 unknown，统计异常不自动归因为画风退化。不同构图须记录原因，
再由独立 reviewer 实看相同材质和六项内容。画幅不符仍为硬失败。

用法:
    python3 look_check.py measure <project> --media <视频或图片...> \
        [--baseline <基准图...>] [--derived-from <父媒体>] [--kind scene|asset]
    # 独立人物/道具/地点资产板用 --kind asset：不与完整场景基准比较，直接读原图人工验收。
    python3 look_check.py review <project> --media <文件> [--scope shot|final_cut] \
        --reviewer <名字> --script <剧本> --storyboard <分镜> --prompt <提示词> \
        --reference <参考图...> --look-technical PASS|FAIL|UNVERIFIED \
        --identity-costume ... --hand-limb-contact ... --action-spatial-continuity ... \
        --dialogue-lip-sync ... --audio-voice ... --evidence <检查项=实际观察>（六项各一次）
    python3 look_check.py approve <project> --media <文件> --use edit|reference \
        --reviewer <名字> --note <看到了什么> [--story-pass --story-note <剧情层结论>] \
        [--creator-ack]
    python3 look_check.py reject  <project> --media <文件> --reviewer <名字> --note <原因>
    python3 look_check.py status  <project> --media <文件>

报告写到 <project>/审查/look/<媒体的项目相对路径>.look.json（镜像目录，不同集同名文件不冲突）。
基准来自 剧集/*/视觉设定.md 或 视觉设定.md 的「## 画风基准」小节
`- LOOK-...：<项目相对路径>《名称》` 行，且小节内必须有 `- 认可依据：` 行（创作者认可的记录）。

批准语义（REV-15/16）：
- `--use edit`：画风通过，可入选剪辑；
- `--use reference`：还可作为下一次生成的参考；必须同时 `--story-pass`（剧情层已逐帧核对通过）。
复核记录只追加不覆盖；重新 measure 保留历史。被拒的媒体自动把所有 derived_from 指向它的
报告标为 superseded。逐镜/整片须由实际另起、未参与生产的 reviewer 先记录六项审查；
reviewer 字段只作归属，工具不证明流程独立。自审不能批准；资产板自审 reference 仍需
创作者 `--creator-ack`。ASR 只辅助定位，不能证明精确台词、口型或声线。

退出码：0 = 机械 PASS；1 = WARN；2 = FAIL / 拒绝批准；3 = 输入错误。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

MINIMUM_PYTHON = (3, 9)
if sys.version_info < MINIMUM_PYTHON:
    raise SystemExit("look_check.py requires Python 3.9 or newer")

import numpy as np

W, H = 512, 288           # 统一分析尺寸（16:9）；竖屏素材按比例另算
SAMPLES = 8               # 每条视频均匀抽样帧数
BLOCK = 16                # 平涂检测块大小
FLAT_STD = 2.0            # 块内亮度标准差低于此视为平涂（未经渲染的纯色面）
SCHEMA = "look-check/2"
ACCEPTED_SCHEMAS = {"look-check/1", "look-check/2"}
ASPECT_TOLERANCE = 0.02   # 候选与基准宽高比相对差超过此值即判 FAIL（画幅不符）

# 指标都相对基准，不是跨项目绝对值。阈值覆盖 handsome-livestream 与《九门·山海志》
# 创作者实看接受的场景、景别和光态范围；只拦截更极端的模糊、纹理丢失、平涂与色彩偏移。
THRESHOLDS = {
    "sharpness_ratio": {"warn": 0.20, "fail": 0.15},       # 越低越糊
    "detail_ratio": {"warn": 0.45, "fail": 0.35},          # 中高频纹理能量
    "flat_increase": {"warn": 0.05, "fail": 0.10},         # 平涂块占比增加量
    "histogram_distance": {"warn": 0.65, "fail": 0.75},    # Bhattacharyya，色彩与影调分布
    "saturation_shift": {"warn": 0.60, "fail": 0.75},      # 相对变化幅度
}
WARNS_TO_FAIL = 2          # 两项及以上同时 WARN 视为整体退化
COMPARISONS = ("unknown", "comparable", "different-framing")
REVIEW_SCOPES = ("shot", "final_cut")
REVIEW_CHECK_NAMES = (
    "look_technical",
    "identity_costume",
    "hand_limb_contact",
    "action_spatial_continuity",
    "dialogue_lip_sync",
    "audio_voice",
)
REVIEW_VERDICTS = ("PASS", "FAIL", "UNVERIFIED", "N/A")
# 静帧没有音轨也没有口型，这两项在逐镜静帧上不成立。让 reviewer 填 PASS 等于
# 让脚本替不存在的媒体背书；允许显式 N/A 才是诚实的记录。
AUDIO_DEPENDENT_CHECKS = ("dialogue_lip_sync", "audio_voice")
ASR_LIMIT = "ASR 只辅助定位，不能证明精确台词、口型或声线；这些项必须对照剧本观看并回听。"

LOOK_LINE = re.compile(r"^-\s*(LOOK-[A-Za-z0-9_-]+)\s*[：:]\s*(.+?)《")
BASIS_LINE = re.compile(r"^-\s*认可依据\s*[：:]\s*\S")


def _probe_size(path: Path) -> tuple[int, int, float]:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
         "stream=width,height:format=duration", "-of", "json", str(path)],
        capture_output=True, text=True, check=True).stdout
    info = json.loads(out)
    stream = info["streams"][0]
    duration = float(info.get("format", {}).get("duration") or 0.0)
    return int(stream["width"]), int(stream["height"]), duration


def _frames(path: Path) -> list[np.ndarray]:
    """解码为若干张统一尺寸的 RGB float 数组。图片返回 1 帧，视频均匀抽 SAMPLES 帧。"""
    width, height, duration = _probe_size(path)
    w, h = (W, H) if width >= height else (H, W)
    times = [0.0]
    if duration > 0.5:
        times = [duration * (i + 0.5) / SAMPLES for i in range(SAMPLES)]
    frames = []
    for t in times:
        cmd = ["ffmpeg", "-v", "error"]
        if duration > 0.5:
            cmd += ["-ss", f"{t:.3f}"]
        cmd += ["-i", str(path), "-frames:v", "1", "-vf", f"scale={w}:{h}:flags=area",
                "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
        data = subprocess.run(cmd, capture_output=True, check=True).stdout
        if len(data) >= w * h * 3:
            frames.append(np.frombuffer(data[: w * h * 3], np.uint8)
                          .reshape(h, w, 3).astype(np.float32))
    if not frames:
        raise ValueError(f"无法解码画面：{path}")
    return frames


def _gray(rgb: np.ndarray) -> np.ndarray:
    return rgb @ np.array([0.299, 0.587, 0.114], np.float32)


def _laplacian_var(g: np.ndarray) -> float:
    lap = (-4 * g[1:-1, 1:-1] + g[:-2, 1:-1] + g[2:, 1:-1] + g[1:-1, :-2] + g[1:-1, 2:])
    return float(lap.var())


def _detail_energy(g: np.ndarray) -> float:
    """去掉低频（4x 降采样再放大）后的残差能量，反映纹理与细节密度。"""
    h, w = g.shape
    h4, w4 = h // 4 * 4, w // 4 * 4
    g = g[:h4, :w4]
    low = g.reshape(h4 // 4, 4, w4 // 4, 4).mean(axis=(1, 3))
    low = np.repeat(np.repeat(low, 4, axis=0), 4, axis=1)
    return float(np.abs(g - low).mean())


def _flat_ratio(g: np.ndarray) -> float:
    h, w = g.shape
    hb, wb = h // BLOCK, w // BLOCK
    blocks = g[: hb * BLOCK, : wb * BLOCK].reshape(hb, BLOCK, wb, BLOCK).std(axis=(1, 3))
    return float((blocks < FLAT_STD).mean())


def _saturation(rgb: np.ndarray) -> float:
    mx, mn = rgb.max(axis=2), rgb.min(axis=2)
    return float(np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0).mean())


def _histogram(rgb: np.ndarray) -> np.ndarray:
    q = (rgb // 32).astype(np.int32)
    idx = q[..., 0] * 64 + q[..., 1] * 8 + q[..., 2]
    hist = np.bincount(idx.ravel(), minlength=512).astype(np.float64)
    return hist / hist.sum()


def _stats(frames: list[np.ndarray]) -> dict:
    grays = [_gray(f) for f in frames]
    return {
        "sharpness": float(np.median([_laplacian_var(g) for g in grays])),
        "detail": float(np.median([_detail_energy(g) for g in grays])),
        "flat": float(np.median([_flat_ratio(g) for g in grays])),
        "saturation": float(np.median([_saturation(f) for f in frames])),
        "luma": float(np.median([g.mean() for g in grays])),
        "histogram": np.mean([_histogram(f) for f in frames], axis=0),
    }


def _bhattacharyya(a: np.ndarray, b: np.ndarray) -> float:
    bc = float(np.sum(np.sqrt(a * b)))
    return float(np.sqrt(max(0.0, 1.0 - bc)))


def _grade(name: str, value: float) -> str:
    t = THRESHOLDS[name]
    lower_is_bad = name in ("sharpness_ratio", "detail_ratio")
    if lower_is_bad:
        return "FAIL" if value < t["fail"] else "WARN" if value < t["warn"] else "PASS"
    return "FAIL" if value > t["fail"] else "WARN" if value > t["warn"] else "PASS"


def compare(base: dict, cand: dict) -> dict:
    metrics = {
        "sharpness_ratio": cand["sharpness"] / max(base["sharpness"], 1e-6),
        "detail_ratio": cand["detail"] / max(base["detail"], 1e-6),
        "flat_increase": cand["flat"] - base["flat"],
        "histogram_distance": _bhattacharyya(base["histogram"], cand["histogram"]),
        "saturation_shift": abs(cand["saturation"] - base["saturation"])
        / max(base["saturation"], 1e-6),
    }
    grades = {k: _grade(k, v) for k, v in metrics.items()}
    order = {"PASS": 0, "WARN": 1, "FAIL": 2}
    verdict = max(grades.values(), key=order.get)
    if verdict == "WARN" and list(grades.values()).count("WARN") >= WARNS_TO_FAIL:
        verdict = "FAIL"
    return {"metrics": {k: round(v, 4) for k, v in metrics.items()},
            "grades": grades, "verdict": verdict}


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def rel(root: Path, path: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError as exc:
        raise ValueError(f"媒体必须在项目内：{path}") from exc


def report_path(root: Path, relative: str) -> Path:
    """镜像项目相对路径，避免不同集同名文件互相覆盖。"""
    return root / "审查" / "look" / f"{relative}.look.json"


def _episode_key(path: Path, root: Path) -> str:
    """`剧集/<EP>/…` 返回 <EP>；项目级文件返回空串。"""
    try:
        relative = path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        relative = path.as_posix()
    match = re.match(r"^剧集/([^/]+)/", relative)
    return match.group(1) if match else ""


def baselines_for_media(root: Path, media: list[Path]) -> list[Path]:
    """只取与媒体同一集的基准；集内没登记才退项目级，**不跨集借基准**。

    原来把所有 `剧集/*/剧本.md` 的基准汇总成一个池子，第二集没登记基准时会静默
    拿第一集的图去判——换场景的第二集会被判「画风不符」，看起来像新一集坏了。
    """
    entries = [item for item in baseline_entries(root) if item.get("basis")]
    episodes = {_episode_key(path, root) for path in media} - {""}
    if len(episodes) == 1:
        episode = next(iter(episodes))
        same = [item for item in entries if item.get("episode") == episode]
        if same:
            return _dedup_baselines(root, same)
    project_level = [item for item in entries if not item.get("episode")]
    return _dedup_baselines(root, project_level)


def _dedup_baselines(root: Path, items: list[dict]) -> list[Path]:
    result: list[Path] = []
    seen: set[Path] = set()
    for item in items:
        path = root / item["path"]
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result


def baseline_entries(root: Path) -> list[dict]:
    """登记的基准：[{path, basis}]；basis 为同小节的认可依据是否存在。"""
    entries: list[dict] = []
    for doc in sorted(root.glob("视觉设定.md")) + sorted(root.glob("剧集/*/视觉设定.md")):
        in_section = False
        section: list[dict] = []
        has_basis = False
        for line in doc.read_text(encoding="utf-8").splitlines() + ["## END"]:
            if line.startswith("## "):
                if in_section:
                    for item in section:
                        item["basis"] = has_basis
                    entries.extend(section)
                in_section = line.strip().startswith("## 画风基准")
                section, has_basis = [], False
                continue
            if not in_section:
                continue
            stripped = line.strip()
            match = LOOK_LINE.match(stripped)
            if match:
                section.append({"id": match.group(1), "path": match.group(2).strip(),
                                "episode": _episode_key(doc, root)})
            elif BASIS_LINE.match(stripped):
                has_basis = True
    return entries


def baselines_from_project(root: Path) -> list[Path]:
    """**池化**表单：把每一集登记的基准汇总成一个列表，不分归属。

    生产路径不要用它——按媒体所在集取基准走 `baselines_for_media`，
    否则第二集会静默借到第一集的基准。这里只给「收集了哪些条目」这类单元测试用。
    """
    result: list[Path] = []
    seen: set[Path] = set()
    for item in baseline_entries(root):
        if not item["basis"]:
            continue
        path = root / item["path"]
        if path in seen:
            continue
        seen.add(path)
        result.append(path)
    return result


def _contact_sheet(base: Path, media: Path, target: Path) -> None:
    """左列基准、右列候选，三行（候选取 25%/50%/75% 时刻），按候选比例统一，不压扁。"""
    width, height, duration = _probe_size(media)
    cw, ch = (640, int(640 * height / width) // 2 * 2) if width >= height else \
        (int(640 * width / height) // 2 * 2, 640)
    inputs = ["-i", str(base)]
    for frac in (0.25, 0.5, 0.75):
        if duration > 0.5:
            inputs += ["-ss", f"{duration * frac:.3f}", "-i", str(media)]
        else:
            inputs += ["-i", str(media)]
    fit = f"scale={cw}:{ch}:force_original_aspect_ratio=decrease,pad={cw}:{ch}:(ow-iw)/2:(oh-ih)/2"
    graph = f"[0:v]{fit},split=3[b0][b1][b2];" + "".join(
        f"[{i + 1}:v]{fit},trim=end_frame=1[c{i}];" for i in range(3)
    ) + "[b0][c0][b1][c1][b2][c2]xstack=inputs=6:layout=0_0|w0_0|0_h0|w0_h0|0_h0+h0|w0_h0+h0"
    target.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", graph,
                    "-frames:v", "1", "-q:v", "3", str(target)], check=True)


def _load(path: Path) -> dict | None:
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema") not in ACCEPTED_SCHEMAS:
        raise ValueError(f"不是 look_check 报告：{path}")
    return data


def _save(path: Path, report: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _executors(root: Path, relative: str) -> set[str]:
    """生产运行记录里产出该文件的执行者（job 的 parameters.executor，若有）。"""
    found: set[str] = set()
    runs = root / ".short-drama" / "production" / "runs"
    jobs = root / ".short-drama" / "production" / "jobs"
    for run in runs.glob("*/*.json") if runs.is_dir() else []:
        try:
            record = json.loads(run.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not any(o.get("path") == relative for o in record.get("outputs") or []):
            continue
        for job in jobs.glob("*.json") if jobs.is_dir() else []:
            try:
                data = json.loads(job.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            if data.get("job_id") == record.get("job_id"):
                executor = (data.get("parameters") or {}).get("executor")
                if isinstance(executor, str) and executor.strip():
                    found.add(executor.strip())
    return found


def current_review(report: dict) -> dict:
    """最近一条复核；v1 报告的单条 visual_review 视为历史第一条。"""
    history = report.get("reviews")
    if history:
        return history[-1]
    legacy = report.get("visual_review") or {}
    return legacy if legacy.get("status") else {"status": "pending"}


def _best_baseline(base_stats: list[tuple[Path, dict]], cand: dict) -> tuple[Path, dict]:
    """多光态基准时选色彩分布最近的一张比较，而不是混成一锅。"""
    return min(base_stats, key=lambda item: _bhattacharyya(item[1]["histogram"], cand["histogram"]))


def _measure_assets(root: Path, media: list[Path], derived_from: Path | None) -> int:
    """Standalone identity/prop/location boards need human review, not scene metrics."""
    missing = [str(path) for path in media if not path.is_file()]
    if missing:
        print("文件不存在：" + "，".join(missing), file=sys.stderr)
        return 3
    parent = rel(root, derived_from) if derived_from is not None else None
    if derived_from is not None and not derived_from.is_file():
        print(f"父媒体不存在：{derived_from}", file=sys.stderr)
        return 3
    for path in media:
        if path.suffix.casefold() not in {".png", ".jpg", ".jpeg", ".webp"}:
            print(f"资产板验收只接受图片；视频请用场景验收：{path}", file=sys.stderr)
            return 3
        relative = rel(root, path)
        target = report_path(root, relative)
        previous = _load(target)
        if previous and previous.get("kind", "scene") != "asset":
            print(f"{relative} 已有场景验收报告，不能改报资产板绕过场景指标。", file=sys.stderr)
            return 3
        width, height, _ = _probe_size(path)
        history = list(previous.get("reviews") or []) if previous else []
        if previous and not history and (previous.get("visual_review") or {}).get("status"):
            history.append(previous["visual_review"])
        sha = _sha256(path)
        if history and history[-1].get("media_sha256") not in (None, sha):
            history.append({"status": "pending", "at": _now(), "media_sha256": sha,
                            "note": "文件字节已变化，旧复核不再适用"})
        report = {
            "schema": SCHEMA,
            "kind": "asset",
            "measured_at": _now(),
            "media": relative,
            "media_sha256": sha,
            "size": [width, height],
            "derived_from": parent if parent else (previous or {}).get("derived_from"),
            "baseline": None,
            "baseline_sha256": None,
            "mechanical": {"verdict": "NOTCHK", "metrics": {}, "grades": {}},
            "contact_sheet": None,
            "reviews": history,
            "scope": "独立人物/道具/地点资产板：不与完整场景基准比较；必须直接读原图，人工核对身份、视图、文字、裁切与可用性。",
        }
        _save(target, report)
        print(json.dumps({"media": relative, "kind": "asset", "verdict": "NOTCHK",
                          "report": rel(root, target),
                          "note": "直接读原图做人工验收；本项没有机械画质结论"}, ensure_ascii=False))
    return 1


def measure(root: Path, media: list[Path], baseline: list[Path],
            derived_from: Path | None = None, kind: str = "scene",
            comparison: str = "unknown", comparison_note: str = "") -> int:
    if kind == "asset":
        return _measure_assets(root, media, derived_from)
    if kind != "scene":
        raise ValueError(f"未知验收类别：{kind}")
    if comparison not in COMPARISONS:
        raise ValueError("invalid comparison status")
    if comparison != "unknown" and len(comparison_note.strip()) < 8:
        raise ValueError("comparison requires a note describing observed framing, scale and depth of field")
    if not baseline:
        print("没有可用画风基准：在《视觉设定.md》「## 画风基准」登记已批准的原生画面，"
              "并写 `- 认可依据：创作者 <日期> …`；或用 --baseline 指定。", file=sys.stderr)
        return 3
    missing = [str(p) for p in [*baseline, *media] if not p.is_file()]
    if missing:
        print("文件不存在：" + "，".join(missing), file=sys.stderr)
        return 3
    parent = None
    if derived_from is not None:
        parent = rel(root, derived_from)
        if not derived_from.is_file():
            print(f"父媒体不存在：{derived_from}", file=sys.stderr)
            return 3
    base_stats = []
    for path in baseline:
        width, height, _ = _probe_size(path)
        stats = _stats(_frames(path))
        stats["aspect"] = width / height
        base_stats.append((path, stats))
    order = {"PASS": 0, "WARN": 1, "NOTCHK": 1, "FAIL": 2}
    worst = 0
    for path in media:
        relative = rel(root, path)
        width, height, _ = _probe_size(path)
        cand = _stats(_frames(path))
        chosen, base = _best_baseline(base_stats, cand)
        result = compare(base, cand)
        result["statistical_verdict"] = result["verdict"]
        if comparison != "comparable":
            result["verdict"] = "NOTCHK"
        aspect_delta = abs(width / height - base["aspect"]) / base["aspect"]
        result["metrics"]["aspect_delta"] = round(aspect_delta, 4)
        result["grades"]["aspect_delta"] = "FAIL" if aspect_delta > ASPECT_TOLERANCE else "PASS"
        if aspect_delta > ASPECT_TOLERANCE:
            result["verdict"] = "FAIL"
        target = report_path(root, relative)
        sheet = target.with_name(target.name.replace(".look.json", "-vs-baseline.jpg"))
        _contact_sheet(chosen, path, sheet)
        previous = _load(target)
        history = list(previous.get("reviews") or []) if previous else []
        if previous and not history and (previous.get("visual_review") or {}).get("status"):
            history.append(previous["visual_review"])
        sha = _sha256(path)
        comparison_record = {"status": comparison, "note": comparison_note.strip()}
        measurement_id = hashlib.sha256(json.dumps({
            "media": sha, "baseline": _sha256(chosen), "comparison": comparison_record,
            "mechanical": result, "thresholds": THRESHOLDS,
        }, sort_keys=True).encode()).hexdigest()
        measurement_history = list((previous or {}).get("measurement_history") or [])
        if previous and previous.get("measurement_id") != measurement_id:
            measurement_history.append({k: previous.get(k) for k in (
                "measured_at", "measurement_id", "media_sha256", "baseline", "baseline_sha256",
                "comparison", "mechanical", "thresholds",
            )})
            if history:
                history.append({"status": "pending", "at": _now(), "media_sha256": sha,
                                "note": "测量依据或可比性已变化，需要重新独立审查"})
        if history and history[-1].get("media_sha256") not in (None, sha):
            history.append({"status": "pending", "at": _now(), "media_sha256": sha,
                            "note": "文件字节已变化，旧复核不再适用"})
        report = {
            "schema": SCHEMA,
            "kind": "scene",
            "comparison": comparison_record,
            "measurement_id": measurement_id,
            "measurement_history": measurement_history,
            "assessments": list((previous or {}).get("assessments") or []),
            "measured_at": _now(),
            "media": relative,
            "media_sha256": sha,
            "size": [width, height],
            "derived_from": parent if parent else (previous or {}).get("derived_from"),
            "baseline": rel(root, chosen),
            "baseline_sha256": _sha256(chosen),
            "mechanical": result,
            "thresholds": THRESHOLDS,
            "contact_sheet": rel(root, sheet),
            "reviews": history,
            "assessments": list((previous or {}).get("assessments") or []),
            "scope": "全幅统计只在可比条件下用于筛查；NOTCHK不证明画风通过。身份、手部、文字、剧情需独立实审。",
        }
        _save(target, report)
        print(json.dumps({"media": relative, **result,
                          "report": rel(root, target), "contact_sheet": report["contact_sheet"]},
                         ensure_ascii=False))
        worst = max(worst, order[result["verdict"]])
    return worst


def _children(root: Path, relative: str) -> list[Path]:
    base = root / "审查" / "look"
    if not base.is_dir():
        return []
    found = []
    for path in base.rglob("*.look.json"):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if data.get("derived_from") == relative:
            found.append(path)
    return found


def _cascade_reject(root: Path, relative: str, reason: str, seen: set[str]) -> list[str]:
    """父媒体被拒：所有派生报告标 superseded，并递归向下。"""
    touched = []
    for child_path in _children(root, relative):
        child = _load(child_path)
        if child is None or child["media"] in seen:
            continue
        seen.add(child["media"])
        child.setdefault("reviews", []).append({
            "status": "superseded", "at": _now(), "media_sha256": child["media_sha256"],
            "note": f"上游 {relative} 已被拒：{reason}",
        })
        _save(child_path, child)
        touched.append(child["media"])
        touched += _cascade_reject(root, child["media"], reason, seen)
    return touched


def _review_input(root: Path, raw: str, label: str) -> str:
    path = Path(raw)
    if not path.is_absolute():
        path = root / path
    if not path.is_file():
        raise ValueError(f"{label} 不是可读文件：{raw}")
    return rel(root, path)


def audio_verdict_problem(
    verdicts: dict[str, str], still_media: bool
) -> tuple[str, int] | None:
    """Check the two audio-dependent verdicts against the media kind.

    Split out of ``assess`` so the rule can be tested without a measured
    report: the question "may this verdict be used here" is pure, and it is the
    part that used to force a fabricated PASS on stills.
    """
    for name in AUDIO_DEPENDENT_CHECKS:
        if verdicts[name] == "N/A" and not still_media:
            return f"{name} 只有静帧才能记 N/A；动态媒体必须实听判定。", 3
    return None


def review_verdict_problem(
    verdicts: dict[str, str], still_media: bool, *, require_pass: bool = False
) -> tuple[str, int] | None:
    """Shared six-check validity for recording, approval and edit consumption."""
    if set(verdicts) != set(REVIEW_CHECK_NAMES):
        return "六个检查项必须完整，不能缺项或增加未知项。", 3
    for name, verdict in verdicts.items():
        if verdict not in REVIEW_VERDICTS:
            return f"{name} 检查项状态无效。", 3
        if verdict == "N/A" and name not in AUDIO_DEPENDENT_CHECKS:
            return f"{name} 不能记 N/A；只有静帧的口型与声线可记 N/A。", 3
    problem = audio_verdict_problem(verdicts, still_media)
    if problem:
        return problem
    if require_pass and any(value not in {"PASS", "N/A"} for value in verdicts.values()):
        return "六个检查项必须全部 PASS；FAIL 或 UNVERIFIED 均不能批准。", 2
    return None


def _is_still(path: Path) -> bool:
    """True when the media has no audio stream (a still, or a silent clip).

    Read from the container rather than the extension: a .mp4 with no audio is
    still a frame, and a .png is neither.
    """
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff", ".bmp"}:
        return True
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries",
         "stream=index", "-of", "json", str(path)],
        capture_output=True, text=True, check=False).stdout
    try:
        return not json.loads(out).get("streams")
    except json.JSONDecodeError:
        return False


def _evidence(items: list[str]) -> dict[str, str]:
    evidence: dict[str, str] = {}
    for item in items:
        name, separator, text = item.partition("=")
        if not separator or name not in REVIEW_CHECK_NAMES:
            raise ValueError(f"--evidence 必须是 CHECK=观察记录，CHECK 为 {', '.join(REVIEW_CHECK_NAMES)}")
        if name in evidence:
            raise ValueError(f"检查项 {name} 的 --evidence 重复")
        if len(text.strip()) < 8:
            raise ValueError(f"检查项 {name} 必须写明至少 8 个字符的实际观察")
        evidence[name] = text.strip()
    missing = [name for name in REVIEW_CHECK_NAMES if name not in evidence]
    if missing:
        raise ValueError("缺少检查项观察记录：" + ", ".join(missing))
    return evidence


def assess(root: Path, media: Path, scope: str, reviewer: str,
           script: str, storyboard: str, prompt: str, references: list[str],
           verdicts: dict[str, str], evidence_items: list[str]) -> int:
    """保存 reviewer 的逐项观察；reviewer 字符串只作归属，不证明流程独立。"""
    if scope not in REVIEW_SCOPES:
        raise ValueError(f"未知审查范围：{scope}")
    if not reviewer.strip():
        raise ValueError("reviewer 不能为空")
    if scope == "final_cut" and reviewer.strip() in _shot_reviewers(root):
        print("整片必须换另一名全新 reviewer；不得沿用任何逐镜 reviewer。", file=sys.stderr)
        return 3
    relative = rel(root, media)
    target = report_path(root, relative)
    report = _load(target)
    if report is None:
        print(f"没有 look 报告：先 measure {relative}", file=sys.stderr)
        return 3
    if report.get("kind", "scene") != "scene":
        print("资产板不是逐镜/整片审查；请直接读原图做资产人工复核。", file=sys.stderr)
        return 3
    if report["media_sha256"] != _sha256(media):
        print("文件在 measure 之后被改过；重新 measure 再审。", file=sys.stderr)
        return 3
    sheet = report.get("contact_sheet")
    if not sheet or not (root / sheet).is_file():
        print("缺少画风对比图；重新 measure 并先读对比图。", file=sys.stderr)
        return 3
    evidence = _evidence(evidence_items)
    unknown = set(verdicts) - set(REVIEW_CHECK_NAMES)
    missing = set(REVIEW_CHECK_NAMES) - set(verdicts)
    if unknown or missing:
        raise ValueError(f"检查项不完整：missing={sorted(missing)}, unknown={sorted(unknown)}")
    if any(verdicts[name] not in REVIEW_VERDICTS for name in REVIEW_CHECK_NAMES):
        raise ValueError("每个检查项只能是 PASS、FAIL、UNVERIFIED 或 N/A")
    problem = review_verdict_problem(verdicts, _is_still(media))
    if problem is not None:
        message, code = problem
        print(message, file=sys.stderr)
        return code
    if (report.get("comparison", {}).get("status") == "unknown"
            and verdicts["look_technical"] == "PASS"):
        print("可比性尚未确认：实看对比图后用 measure --comparison 与 --comparison-note 记录依据，或将画风记为 UNVERIFIED。", file=sys.stderr)
        return 3
    entry = {
        "at": _now(),
        "scope": scope,
        "reviewer": reviewer.strip(),
        "reviewer_attribution_only": True,
        "independence": "process_isolation_required",
        "media_sha256": report["media_sha256"],
        "measurement_id": report.get("measurement_id"),
        "inputs": {
            "media": relative,
            "references": [_review_input(root, item, "参考图") for item in references],
            "script": _review_input(root, script, "剧本"),
            "storyboard": _review_input(root, storyboard, "分镜"),
            "prompt": _review_input(root, prompt, "提示词"),
            "contact_sheet": sheet,
        },
        "checks": {name: {"status": verdicts[name], "evidence": evidence[name]}
                   for name in REVIEW_CHECK_NAMES},
        # 静帧没有音轨：这两项即使在报告里写着 PASS，也不是本帧的证据。
        # 显式标出来，避免后来的人把"六项全绿"读成"口型和声线也验过了"。
        "not_applicable": (list(AUDIO_DEPENDENT_CHECKS)
                           if _is_still(media) else []),
        "asr_limit": ASR_LIMIT,
    }
    statuses = [verdicts[name] for name in REVIEW_CHECK_NAMES]
    overall = ("FAIL" if "FAIL" in statuses
               else "UNVERIFIED" if "UNVERIFIED" in statuses
               else "PASS")
    entry["verdict"] = overall
    report.setdefault("assessments", []).append(entry)
    _save(target, report)
    print(json.dumps({"report": rel(root, target), "assessment": entry}, ensure_ascii=False))
    return {"PASS": 0, "UNVERIFIED": 1, "FAIL": 2}[overall]


def _current_assessment(report: dict, reviewer: str, scope: str) -> dict | None:
    for entry in reversed(report.get("assessments") or []):
        if (entry.get("reviewer") == reviewer.strip() and entry.get("scope") == scope
                and entry.get("media_sha256") == report.get("media_sha256")
                and entry.get("measurement_id") == report.get("measurement_id")):
            return entry
    return None


def _shot_reviewers(root: Path) -> set[str]:
    base = root / "审查" / "look"
    found: set[str] = set()
    for path in base.rglob("*.look.json") if base.is_dir() else []:
        try:
            report = _load(path)
        except (OSError, ValueError, json.JSONDecodeError):
            continue
        for entry in (report or {}).get("assessments") or []:
            if entry.get("scope") == "shot" and isinstance(entry.get("reviewer"), str):
                found.add(entry["reviewer"])
    return found


def _ref_gate():
    """Load the stdlib acceptance gate lazily; it owns the reuse criteria."""
    global _REF_GATE
    if _REF_GATE is None:
        import importlib.util
        path = Path(__file__).with_name("ref_gate.py")
        spec = importlib.util.spec_from_file_location("short_drama_ref_gate_shared", path)
        if spec is None or spec.loader is None:
            raise ImportError(f"shared reference gate missing: {path}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        _REF_GATE = module
    return _REF_GATE


_REF_GATE = None


def review(root: Path, media: Path, status: str, reviewer: str, note: str,
           use: str | None = None, story_pass: bool = False, story_note: str = "",
           creator_ack: bool = False, scope: str = "shot") -> int:
    relative = rel(root, media)
    path = report_path(root, relative)
    report = _load(path)
    if report is None:
        print(f"没有 look 报告：先 measure {relative}", file=sys.stderr)
        return 3
    if report["media_sha256"] != _sha256(media):
        print("文件在 measure 之后被改过；重新 measure 再复核。", file=sys.stderr)
        return 3
    if len(note.strip()) < 8:
        print("复核必须写明在对比图里实际看到了什么（材质、光、纹理、人物质感）。", file=sys.stderr)
        return 3
    mechanical_override = False
    if status == "approved" and report["mechanical"]["verdict"] == "FAIL":
        if not creator_ack:
            print("机械 FAIL 需要创作者实看后显式使用 --creator-ack 豁免；否则退化素材必须重做。",
                  file=sys.stderr)
            return 2
        mechanical_override = True
    entry = {"status": status, "reviewer": reviewer.strip(), "note": note.strip(),
             "at": _now(), "media_sha256": report["media_sha256"]}
    if report.get("measurement_id"):
        entry["measurement_id"] = report["measurement_id"]
    structured = report.get("kind", "scene") == "scene"
    assessment = None
    if structured:
        if scope not in REVIEW_SCOPES:
            print("场景媒体审查范围只能是 shot 或 final_cut。", file=sys.stderr)
            return 3
        assessment = _current_assessment(report, reviewer, scope)
        if assessment is None:
            print("没有当前媒体字节、同一 reviewer 与范围的逐项审查；先运行 review。", file=sys.stderr)
            return 3
        entry.update({"scope": scope, "assessment_at": assessment["at"],
                      "independence": "process_isolation_required"})
    if status == "approved":
        if use not in ("edit", "reference"):
            print("批准必须写明用途：--use edit（仅入剪辑）或 --use reference（可作下一代参考）。",
                  file=sys.stderr)
            return 3
        if structured and assessment["verdict"] != "PASS":
            print("六个检查项必须全部 PASS；FAIL 或 UNVERIFIED 均不能批准"
                  "（静帧的口型与声线记 N/A，不算 UNVERIFIED）。", file=sys.stderr)
            return 2
        if structured:
            try:
                verdicts = {name: assessment["checks"][name]["status"] for name in REVIEW_CHECK_NAMES}
            except (KeyError, TypeError):
                print("当前 assessment 缺少完整六项检查记录。", file=sys.stderr)
                return 3
            has_audio_na = any(verdicts[name] == "N/A" for name in AUDIO_DEPENDENT_CHECKS)
            problem = review_verdict_problem(
                verdicts, _is_still(media) if has_audio_na else False, require_pass=True)
            if problem:
                print(problem[0], file=sys.stderr)
                return problem[1]
        if structured and scope == "final_cut" and use != "edit":
            print("整片只能批准 --use edit；reference 权限只适用于逐镜素材。", file=sys.stderr)
            return 3
        if use == "reference" and (not story_pass or len(story_note.strip()) < 8):
            print("--use reference 要求剧情层也已逐帧核对通过：加 --story-pass 与 --story-note。",
                  file=sys.stderr)
            return 3
        parent = report.get("derived_from")
        if parent:
            parent_report = _load(report_path(root, parent))
            parent_review = current_review(parent_report) if parent_report else {}
            if parent_review.get("status") != "approved":
                print(f"派生自 {parent}，但父媒体未获批准；父媒体先过验收。", file=sys.stderr)
                return 2
            if use == "reference":
                # 批准派生帧作参考时，父媒体本身也要当前有效：同一字节、
                # 当前测量、reference 用途与剧情层。判据归 ref_gate，一处维护。
                gate = _ref_gate()
                try:
                    parent_digest = gate.sha256_file(root, parent)
                    problem = gate.reference_problem(root, parent, parent_digest, "frame")
                except (gate.InputError, OSError) as exc:
                    print(f"派生自 {parent}，但父媒体当前无法读取：{exc}", file=sys.stderr)
                    return 2
                if problem:
                    print(f"派生自 {parent}，但父媒体当前不能作为参考：{problem}",
                          file=sys.stderr)
                    return 2
        executors = _executors(root, relative)
        external_scene = structured and not executors
        self_review = reviewer.strip() in executors or (not structured and not executors)
        if structured and self_review:
            print("逐镜/整片必须由未参与生产的全新 reviewer 审查；reviewer 字段本身不构成独立证明。",
                  file=sys.stderr)
            return 2
        if external_scene and not creator_ack:
            print("外部生图没有本地执行者；创作者实看后须显式使用 --creator-ack 批准。",
                  file=sys.stderr)
            return 2
        entry.update({"use": use, "story_pass": bool(story_pass), "story_note": story_note.strip(),
                      "self_review": self_review, "creator_ack": bool(creator_ack)})
        if external_scene:
            entry["provenance"] = "external_no_local_executor"
        if mechanical_override:
            entry["mechanical_override"] = True
    report.setdefault("reviews", []).append(entry)
    report.pop("visual_review", None)
    _save(path, report)
    cascaded = _cascade_reject(root, relative, note.strip(), {relative}) if status == "rejected" else []
    print(json.dumps({"report": rel(root, path), "review": entry, "superseded": cascaded},
                     ensure_ascii=False))
    return 0


def status(root: Path, media: Path) -> int:
    relative = rel(root, media)
    report = _load(report_path(root, relative))
    if report is None:
        print(json.dumps({"media": relative, "status": "unmeasured"}, ensure_ascii=False))
        return 2
    latest = current_review(report)
    print(json.dumps({"media": relative, "verdict": report["mechanical"]["verdict"],
                      "review": latest}, ensure_ascii=False))
    return 0 if latest.get("status") == "approved" else 2


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="画风验收（相对已批准基准）")
    sub = parser.add_subparsers(dest="command", required=True)
    m = sub.add_parser("measure")
    m.add_argument("project")
    m.add_argument("--media", nargs="+", required=True)
    m.add_argument("--baseline", nargs="*", default=None)
    m.add_argument("--kind", choices=("scene", "asset"), default="scene",
                   help="scene=场景帧/视频；asset=独立人物、道具、地点资产板")
    m.add_argument("--derived-from", default=None,
                   help="这张图从哪条生成媒体抽出/派生（抽帧、裁切、二次处理必填）")
    m.add_argument("--comparison", choices=COMPARISONS, default="unknown",
                   help="实看后声明全幅可比性；未知或不同构图只报告统计信号")
    m.add_argument("--comparison-note", default="", help="景别、主体比例、景深可比或不可比的观察依据")
    a = sub.add_parser("review", help="记录逐镜/整片六项人工审查；不授予 edit/reference 权限")
    a.add_argument("project")
    a.add_argument("--media", required=True)
    a.add_argument("--scope", choices=REVIEW_SCOPES, default="shot")
    a.add_argument("--reviewer", required=True)
    a.add_argument("--script", required=True, help="实际核对的剧本文件")
    a.add_argument("--storyboard", required=True, help="实际核对的分镜文件")
    a.add_argument("--prompt", required=True, help="实际核对的提示词文件")
    a.add_argument("--reference", nargs="+", required=True, help="实际读取的参考图，至少一张")
    for check_name in REVIEW_CHECK_NAMES:
        a.add_argument("--" + check_name.replace("_", "-"), choices=REVIEW_VERDICTS, required=True)
    a.add_argument("--evidence", action="append", required=True, metavar="CHECK=观察记录",
                   help="六项各写一次实际观察；ASR 不能作为精确台词/口型/声线的唯一证据")
    for name in ("approve", "reject"): 
        r = sub.add_parser(name)
        r.add_argument("project")
        r.add_argument("--media", required=True)
        r.add_argument("--reviewer", required=True)
        r.add_argument("--note", required=True)
        r.add_argument("--scope", choices=REVIEW_SCOPES, default="shot")
        if name == "approve":
            r.add_argument("--use", choices=("edit", "reference"), required=True)
            r.add_argument("--story-pass", action="store_true")
            r.add_argument("--story-note", default="")
            r.add_argument("--creator-ack", action="store_true",
                           help="创作者实看确认：资产板自审、外部生图或全部场景机械 FAIL 豁免；本地生产者自审不可豁免")
    st = sub.add_parser("status")
    st.add_argument("project")
    st.add_argument("--media", required=True)
    args = parser.parse_args(argv)
    try:
        root = Path(args.project)
        if args.command == "measure":
            baseline = ([Path(p) for p in args.baseline] if args.baseline
                        else baselines_for_media(root, [Path(p) for p in args.media]))
            return measure(root, [Path(p) for p in args.media], baseline,
                           Path(args.derived_from) if args.derived_from else None,
                           kind=args.kind, comparison=args.comparison,
                           comparison_note=args.comparison_note)
        if args.command == "status":
            return status(root, Path(args.media))
        if args.command == "review":
            verdicts = {name: getattr(args, name) for name in REVIEW_CHECK_NAMES}
            return assess(root, Path(args.media), args.scope, args.reviewer,
                          args.script, args.storyboard, args.prompt, args.reference,
                          verdicts, args.evidence)
        if args.command == "approve":
            return review(root, Path(args.media), "approved", args.reviewer, args.note,
                          use=args.use, story_pass=args.story_pass,
                          story_note=args.story_note, creator_ack=args.creator_ack,
                          scope=args.scope)
        return review(root, Path(args.media), "rejected", args.reviewer, args.note,
                      scope=args.scope)
    except (subprocess.CalledProcessError, ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"look_check 失败：{exc}", file=sys.stderr)
        return 3



if __name__ == "__main__":
    raise SystemExit(main())
