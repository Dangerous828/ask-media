# -*- coding: utf-8 -*-
"""拉片：接触印片 + 自动切点检测（opencv，无AI）。
用法: python extract_shots.py <video> [--start S] [--end E] [--step 3] [--thresh 9] [--merge 0.6]
产物: <video同目录>/frames_<名>/contact_*.jpg ；stdout 打印切点区间（需人工核对归并）。
可选 --rep-frames 另产原分辨率代表帧、shots.json 与原片拆解.md 骨架。"""
import sys, os, argparse, cv2, numpy as np
import json, shutil, subprocess


def find_ffmpeg():
    exe = shutil.which("ffmpeg")
    for candidate in ("/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg"):
        if exe is None and os.access(candidate, os.X_OK):
            exe = candidate
    if exe is None:
        raise RuntimeError("找不到 ffmpeg，无法抽取原分辨率代表帧；请先安装 ffmpeg")
    return exe


def extract_rep_evidence(video, bounds, rep_dir, prefix, ffmpeg):
    """为每个有效镜头抽中点原分辨率帧；全部成功后才写清单与骨架。"""
    shots = [(i, bounds[i], bounds[i + 1]) for i in range(len(bounds) - 1)
             if bounds[i + 1] > bounds[i]]
    if not shots:
        raise RuntimeError("没有可抽取代表帧的有效镜头；请检查视频、起止时间与切点参数")
    if os.path.basename(prefix) != prefix or prefix in (".", ".."):
        raise ValueError("--prefix 只能文件名前缀，不能包含目录")
    os.makedirs(rep_dir, exist_ok=True)
    records = []
    for index, start, end in shots:
        shot_id = "%s%02d" % (prefix, index + 1)
        filename = shot_id + ".jpg"
        dst = os.path.join(rep_dir, filename)
        midpoint = (start + end) / 2
        r = subprocess.run(
            [ffmpeg, "-y", "-v", "error", "-ss", "%.6f" % midpoint,
             "-i", video, "-frames:v", "1", "-q:v", "2", dst],
            capture_output=True, text=True, timeout=120,
        )
        if r.returncode != 0 or not os.path.isfile(dst) or os.path.getsize(dst) == 0:
            raise RuntimeError("%s 中点 %.3fs 代表帧抽取失败：%s" % (
                shot_id, midpoint, (r.stderr or "ffmpeg 未产出文件").strip()[-300:]))
        records.append({"id": shot_id, "start": round(start, 6), "end": round(end, 6),
                        "duration": round(end - start, 6), "midpoint": round(midpoint, 6),
                        "frame_path": os.path.abspath(dst)})
    manifest = os.path.join(rep_dir, "shots.json")
    with open(manifest, "w", encoding="utf-8") as fo:
        json.dump({"video": os.path.abspath(video), "shots": records}, fo,
                  ensure_ascii=False, indent=2)
        fo.write("\n")
    lines = ["# 原片拆解", "", "- 来源原片：%s" % os.path.abspath(video),
             "- 镜数：%d" % len(records), "",
             "> 自动证据仅含入出点、中点代表帧与镜数；其余字段须核对原片、OCR 与 ASR 后填写。", ""]
    for rec in records:
        lines += ["## %s" % rec["id"], "",
                  "- 入点（秒）：%.3f" % rec["start"],
                  "- 出点（秒）：%.3f" % rec["end"],
                  "- 代表帧路径：./%s.jpg" % rec["id"],
                  "- 一句话内容：待填", "- 景别与机位：待填", "- 画面人物：待填",
                  "- 说话人与台词（逐字）：待填", "- 关键道具与状态：待填", "- 运镜：待填", ""]
    lines += ["## 整体画风观察", "", "- 介质、光色、材质、景深：待填（无法确认写“不确定”）", ""]
    skeleton = os.path.join(rep_dir, "原片拆解.md")
    with open(skeleton, "w", encoding="utf-8") as fo:
        fo.write("\n".join(lines))
    return manifest, skeleton


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video"); ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=1e9); ap.add_argument("--step", type=float, default=3.0)
    ap.add_argument("--thresh", type=float, default=9.0); ap.add_argument("--merge", type=float, default=0.6)
    ap.add_argument("--rep-frames", help="可选：逐镜中点原分辨率代表帧、shots.json 与拆解骨架的输出目录")
    ap.add_argument("--prefix", default="SRC-", help="代表帧与镜头 ID 前缀（默认 SRC-）")
    a = ap.parse_args()
    a.video = os.path.abspath(a.video)  # Windows 下 cv2 用相对+中文路径会读到错误的帧数
    ffmpeg = find_ffmpeg() if a.rep_frames else None
    rep_dir = os.path.abspath(a.rep_frames) if a.rep_frames else None
    base = os.path.splitext(os.path.basename(a.video))[0]
    out = os.path.join(os.path.dirname(os.path.abspath(a.video)), "frames_" + base)
    os.makedirs(out, exist_ok=True)
    cap = cv2.VideoCapture(a.video); fps = cap.get(cv2.CAP_PROP_FPS)
    if not np.isfinite(fps) or fps <= 0: fps = 24
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
    duration = frame_count / fps if np.isfinite(frame_count) and frame_count > 0 else 0.0
    t0 = max(0.0, a.start); t1 = min(a.end, duration)
    thumbs = []; t = t0
    while t < t1:
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); r, f = cap.read()
        if r:
            th = cv2.resize(f, (222, 120)); cv2.rectangle(th, (0, 0), (46, 16), (0, 0, 0), -1)
            cv2.putText(th, "%.0f" % t, (3, 12), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 255), 1)
            thumbs.append(th)
        t += a.step
    cols = 8
    for gi in range(0, len(thumbs), 40):
        ch = thumbs[gi:gi + 40]; rows = (len(ch) + cols - 1) // cols
        sheet = np.full((rows * 120, cols * 222, 3), 20, np.uint8)
        for i, im in enumerate(ch):
            r, c = divmod(i, cols); sheet[r*120:(r+1)*120, c*222:(c+1)*222] = im
        ok, enc = cv2.imencode(".jpg", sheet, [cv2.IMWRITE_JPEG_QUALITY, 86])
        if ok:  # cv2.imwrite 在 Windows 中文路径下静默失败，必须 imencode 后自写文件
            with open(os.path.join(out, "contact_%d.jpg" % (gi // 40)), "wb") as fo:
                fo.write(enc.tobytes())
    f0, f1 = int(t0 * fps), int(t1 * fps); cap.set(cv2.CAP_PROP_POS_FRAMES, f0)
    prev = None; cuts = []; idx = f0
    while idx < f1:
        r, f = cap.read()
        if not r: break
        g = cv2.cvtColor(cv2.resize(f, (160, 90)), cv2.COLOR_BGR2GRAY)
        if prev is not None and np.abs(g.astype(int) - prev).mean() > a.thresh:
            cuts.append(idx / fps)
        prev = g; idx += 1
    cap.release()
    m = []
    for ts in cuts:
        if m and ts - m[-1] < a.merge: continue
        m.append(ts)
    bounds = [t0] + m + [t1]
    with open(os.path.join(out, "cuts.txt"), "w", encoding="utf-8") as fo:
        for i in range(len(bounds) - 1):
            fo.write("%.2f\t%.2f\t%.2f\n" % (bounds[i], bounds[i+1], bounds[i+1] - bounds[i]))
    rep_outputs = None
    if rep_dir:
        rep_outputs = extract_rep_evidence(a.video, bounds, rep_dir, a.prefix, ffmpeg)
    print("# %s  %.1f-%.1fs  contact -> %s" % (base, t0, t1, out))
    print("# %d cuts (thresh %.1f, merge %.1fs) - verify/merge on contact sheet:" % (len(m), a.thresh, a.merge))
    for i in range(len(bounds) - 1):
        print("  S%d: %.1f-%.1f  (%.1fs)" % (i + 1, bounds[i], bounds[i+1], bounds[i+1] - bounds[i]))
    if rep_outputs:
        print("# representative frames -> %s" % rep_dir)
        print("# shot manifest -> %s" % rep_outputs[0])
        print("# remake skeleton -> %s" % rep_outputs[1])
if __name__ == "__main__":
    try: sys.stdout.reconfigure(encoding="utf-8")
    except Exception: pass
    try:
        main()
    except (RuntimeError, ValueError, OSError, subprocess.SubprocessError) as exc:
        print("❌ 拉片失败：%s" % exc, file=sys.stderr)
        sys.exit(2)
