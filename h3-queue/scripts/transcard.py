#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""转场卡：A 的真实末帧 + B 的真实首帧 -> FL2VA 中间段 C，并可选拼成 A+C+B。

为什么要这个脚本：pdd_lu（草稿档）的渲染器 pdd_render_ref.py 没有
--first-frame/--last-frame，h3q 也不转发，任务会照样 exit 0 但产出纯文生视频
（2026-11-22 实测：同一对首尾帧、同 107f、同 seed，pdd_lu 产物首帧 vs 指定首帧
MAD 43.0，默认分支 3.86）。所以转场卡必须落到默认分支（h3_render_ref.py 的
i2va/fl2va 图）：提交时不带 --workflow。

用法：
  python3 transcard.py --before A.mp4 --after B.mp4 --prompt-file c.txt \
      --frames 107 --width 576 --height 992 --seed 42 --out-dir ./tc

  # 出片后拼成 A+C+B（各去掉接缝处重复的一帧）
  python3 transcard.py ... --assemble
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

# 主名 H3Q_SSH_HOST / H3Q_REMOTE_PY，旧名 H3Q_HOST / H3Q_PY 作兼容别名（新名优先）。
HOST = os.environ.get("H3Q_SSH_HOST") or os.environ.get("H3Q_HOST", "")


def _require_host():
    missing = [k for k, v in [
        ("H3Q_SSH_HOST/H3Q_HOST", HOST), ("H3Q_REMOTE_PY/H3Q_PY", REMOTE_PY),
        ("H3Q_REMOTE_CLI", REMOTE_CLI), ("H3Q_COMFY_INPUT", COMFY_INPUT),
        ("H3Q_REMOTE_ROOT", REMOTE_ROOT),
    ] if not v]
    if missing:
        raise SystemExit(
            "缺少远端环境变量: " + ", ".join(missing) + "。"
            "渲染机的路径全部由环境变量提供，本脚本不内置默认机器。"
        )
REMOTE_PY = os.environ.get("H3Q_REMOTE_PY") or os.environ.get("H3Q_PY", "")
REMOTE_CLI = os.environ.get("H3Q_REMOTE_CLI", "")
COMFY_INPUT = os.environ.get("H3Q_COMFY_INPUT", "")
REMOTE_ROOT = os.environ.get("H3Q_REMOTE_ROOT", "")
def _default_gate_path():
    """闸门默认路径：优先本仓库同布局的相对路径，再退回常见的中枢安装位置。"""
    candidates = (
        # 本仓库 scripts/ 的上一级就是技能根，h3-video-gate 与其平级。
        Path(__file__).resolve().parents[2] / "h3-video-gate/scripts/h3_gate.py",
        Path.home() / ".skills/hub/h3-video-gate/scripts/h3_gate.py",
    )
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    # 都不存在时返回仓库相对路径，让 gate_check 明确报错，而不是静默跳过。
    return str(candidates[0])


GATE = os.environ.get("H3Q_GATE", _default_gate_path())


def log(msg: str) -> None:
    print("[transcard] " + msg, flush=True)


def run(argv, check=True, timeout=None, capture=True):
    res = subprocess.run(argv, capture_output=capture, text=True,
                         encoding="utf-8", errors="replace", timeout=timeout)
    if check and res.returncode:
        raise RuntimeError("command failed (%s): %s\n%s" % (
            res.returncode, " ".join(map(str, argv)), (res.stderr or "")[:800]))
    return res


def ssh(cmd: str, timeout=None, check=True):
    _require_host()
    return run(["ssh", HOST, cmd], timeout=timeout, check=check)


def scp_up(local, remote, timeout=180):
    return run(["scp", str(local), "%s:%s" % (HOST, remote)], timeout=timeout)


def scp_down(remote, local, timeout=600):
    return run(["scp", "%s:%s" % (HOST, remote), str(local)], timeout=timeout)


def extract_edge(video: Path, edge: str, target: Path) -> Path:
    """取真实首帧/末帧，原始像素不缩放（这些就是交付像素）。"""
    if edge == "last":
        expr = "select=eq(n\\,%d)" % (probe_frames(video) - 1)
    else:
        expr = "select=eq(n\\,0)"
    target.parent.mkdir(parents=True, exist_ok=True)
    run(["ffmpeg", "-v", "error", "-y", "-i", str(video),
         "-vf", expr, "-vframes", "1", str(target)])
    if not target.is_file() or target.stat().st_size == 0:
        raise RuntimeError("取帧失败: %s (%s)" % (video, edge))
    return target


def probe_frames(video: Path) -> int:
    res = run(["ffprobe", "-v", "error", "-select_streams", "v",
               "-count_frames", "-show_entries", "stream=nb_read_frames",
               "-of", "csv=p=0", str(video)])
    return int(res.stdout.strip().splitlines()[0])


def frame_mad(a: Path, b: Path) -> float:
    """两帧平均绝对差（0-255）；越小越接近。"""
    code = (
        "import sys,numpy as np;from PIL import Image;"
        "a=np.asarray(Image.open(sys.argv[1]).convert('RGB'),dtype=np.float32);"
        "b=np.asarray(Image.open(sys.argv[2]).convert('RGB'),dtype=np.float32);"
        "b=b if a.shape==b.shape else np.asarray("
        "Image.open(sys.argv[2]).convert('RGB').resize((a.shape[1],a.shape[0])),dtype=np.float32);"
        "print(round(float(np.abs(a-b).mean()),2))"
    )
    res = run([sys.executable, "-c", code, str(a), str(b)])
    return float(res.stdout.strip())


def gate_check(prompt_file: Path, frames: int) -> str:
    # 闸门缺失是硬错误，不允许静默跳过——否则 --skip-gate 这个显式开关形同虚设。
    if not Path(GATE).is_file():
        raise RuntimeError(
            "h3_gate 闸门脚本不存在: %s。请设 H3Q_GATE 指向实际部署的 h3_gate.py；"
            "只有显式 --skip-gate 才能跳过闸门。" % GATE)
    res = run([sys.executable, GATE, str(prompt_file), "--mode", "base",
               "--frames", str(frames)], check=False)
    out = (res.stdout + res.stderr).strip()
    if res.returncode:
        raise RuntimeError("h3_gate 拒绝提示词(exit %s)：\n%s" % (res.returncode, out[-2000:]))
    return "gate pass"


def _remote_q(value: str) -> str:
    """把值包成远端命令里的双引号串；先拒绝引号/元字符，防止跳出引用注入。"""
    if not isinstance(value, str) or any(c in value for c in ('"', "'", "&", "|", ";", "`", "$", "\n", "\r")):
        raise ValueError("远端参数含不允许的字符: %r" % value)
    return '"%s"' % value


def _idem_key(label: str, seed: int, frames: int, ff_name: str, lf_name: str) -> str:
    """幂等键含身份信息 + 两帧文件名哈希；重投/脚本重跑不会重复提交。"""
    digest = hashlib.sha256(
        ("%s|%d|%d|%s|%s" % (label, seed, frames, ff_name, lf_name)).encode("utf-8")
    ).hexdigest()[:16]
    return "tc-%s-s%d-f%d-%s" % (
        re.sub(r"[^A-Za-z0-9_-]+", "-", label)[:24] or "transcard", seed, frames, digest)


def submit(prompt_remote: str, ff_name: str, lf_name: str, frames: int,
           width: int, height: int, seed: int, slug: str, label: str) -> str:
    """不带 --workflow：走默认分支 h3_render_ref.py（i2va/fl2va 图）。"""
    for value, name in ((width, "width"), (height, "height")):
        if value % 32:
            raise ValueError("%s=%s 必须是 32 的倍数" % (name, value))
    for name, value in (("first-frame", ff_name), ("last-frame", lf_name), ("slug", slug)):
        if not re.fullmatch(r"[A-Za-z0-9_.\-]+", value):
            raise ValueError("%s 只能含 ASCII 字母数字/点/下划线/连字符: %r" % (name, value))
    argv = [_remote_q(REMOTE_PY), "-s", _remote_q(REMOTE_CLI), "submit", "--kind", "video",
            "--prompt-file", _remote_q(prompt_remote),
            "--slug", _remote_q(slug), "--version", "v1",
            "--seed", str(seed), "--width", str(width), "--height", str(height),
            "--frames", str(frames), "--sol-profile", "off",
            "--first-frame", _remote_q(ff_name), "--last-frame", _remote_q(lf_name),
            "--label", _remote_q(label),
            "--idem-key", _remote_q(_idem_key(label, seed, frames, ff_name, lf_name))]
    res = ssh(" ".join(argv), timeout=120)
    m = re.search(r"\bjob\s+([0-9a-f]{8,32})\b", res.stdout, re.I)
    if not m:
        raise RuntimeError("提交无 job id: %s" % (res.stdout + res.stderr)[:400])
    return m.group(1)


def wait_job(jid: str, timeout_s: int = 3600) -> dict:
    t0 = time.time()
    last = ""
    while time.time() - t0 < timeout_s:
        res = ssh(" ".join(['"%s"' % REMOTE_PY, "-s", '"%s"' % REMOTE_CLI,
                            "show", jid]), check=False)
        try:
            state = json.loads(res.stdout)
        except json.JSONDecodeError:
            time.sleep(5)
            continue
        st = state.get("state")
        if st != last:
            log("job %s -> %s" % (jid, st))
            last = st
        if st in ("done", "failed", "cancelled"):
            return state
        time.sleep(5)
    raise RuntimeError("等待超时 %ss（job %s 仍在跑，用 h3qc show 跟进）" % (timeout_s, jid))


def remote_media(state: dict) -> str:
    raw = (state.get("output") or "").strip()
    if raw.startswith("COPY_OF_RECORD "):
        record = raw[len("COPY_OF_RECORD "):].strip()
        # 用 json.dumps 生成字符串字面量，避免路径含单引号时跳出引用注入。
        code = ("import json;print(json.load(open(%s,encoding='utf-8'))"
                "['comfy_output'])" % json.dumps(record))
        out = ssh("%s -c %s" % (_remote_q(REMOTE_PY), _remote_q(code))).stdout.strip()
        return out.replace("\\", "/")
    if raw.startswith("OUTPUT "):
        return raw[len("OUTPUT "):].strip().replace("\\", "/")
    if raw.lower().endswith(".mp4"):
        return raw.replace("\\", "/")
    raise RuntimeError("job 完成但没有可下载产物: %r" % raw)


def assemble(a: Path, c: Path, b: Path, out: Path) -> Path:
    """A + C + B；C 首帧与 A 末帧、C 末帧与 B 首帧各重合，各去掉一帧。"""
    work = out.parent
    cl = work / "_concat.txt"
    # A 全段；C 去掉首帧（与 A 末帧重合）；B 去掉首帧（与 C 末帧重合）
    c_tail = work / "_c_tail.mp4"
    b_tail = work / "_b_tail.mp4"
    # 去首帧后必须 setpts 重打时间戳：否则被去掉的首帧位置会留空，
    # 经 concat demuxer -c copy 拼接时出现 1 帧时间戳间隙/错位。
    drop_first_vf = "select=gte(n\\,1),setpts=N/FRAME_RATE/TB"
    run(["ffmpeg", "-v", "error", "-y", "-i", str(c),
         "-vf", drop_first_vf,
         "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", str(c_tail)])
    run(["ffmpeg", "-v", "error", "-y", "-i", str(b),
         "-vf", drop_first_vf,
         "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", str(b_tail)])
    for p in (a, c_tail, b_tail):
        run(["ffmpeg", "-v", "error", "-y", "-i", str(p),
             "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p",
             "-c:a", "aac", "-b:a", "192k", str(work / ("_n_" + p.stem + ".mp4"))])
    parts = [work / ("_n_" + p.stem + ".mp4") for p in (a, c_tail, b_tail)]
    with open(cl, "w", encoding="utf-8") as fh:
        for p in parts:
            fh.write("file '%s'\n" % p)
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
         "-i", str(cl), "-c", "copy", str(out)])
    for p in parts + [c_tail, b_tail, cl]:
        try:
            p.unlink()
        except OSError:
            pass
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="转场卡：A 末帧 + B 首帧 -> FL2VA 中间段 C")
    ap.add_argument("--before", required=True, help="A 段视频（取真实末帧）")
    ap.add_argument("--after", required=True, help="B 段视频（取真实首帧）")
    ap.add_argument("--prompt-file", required=True, help="C 的 base 三段提示词")
    ap.add_argument("--frames", type=int, required=True, help="C 的帧数（17k+5，最短 107）")
    ap.add_argument("--width", type=int, required=True)
    ap.add_argument("--height", type=int, required=True)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--label", default="transcard")
    ap.add_argument("--out-dir", default="./transcard-out")
    ap.add_argument("--assemble", action="store_true", help="出片后拼 A+C+B")
    ap.add_argument("--skip-gate", action="store_true")
    ap.add_argument("--dry-run", action="store_true", help="只取帧、跑闸门，不提交")
    args = ap.parse_args()

    a, b = Path(args.before), Path(args.after)
    for p in (a, b):
        if not p.is_file():
            raise SystemExit("找不到视频: %s" % p)
    if (args.frames - 5) % 17:
        raise SystemExit("frames=%d 不是 17k+5（最短 107 / 4.458s）" % args.frames)
    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", args.label)[:40] or "transcard"

    log("取真实边界帧（原始像素，不缩放）")
    ff_local = extract_edge(a, "last", out_dir / "A_last.png")
    lf_local = extract_edge(b, "first", out_dir / "B_first.png")
    log("A 末帧 %s / B 首帧 %s" % (ff_local.name, lf_local.name))

    prompt = Path(args.prompt_file).expanduser()
    if not prompt.is_file():
        raise SystemExit("找不到提示词: %s" % prompt)
    gate_note = "gate skipped" if args.skip_gate else gate_check(prompt, args.frames)
    log(gate_note)

    if args.dry_run:
        log("dry-run：不提交。帧已备好，可直接用 h3qc submit 提交")
        return 0

    ff_remote = "tc-ff-%s.png" % slug
    lf_remote = "tc-lf-%s.png" % slug
    for local, name in ((ff_local, ff_remote), (lf_local, lf_remote)):
        scp_up(local, "%s/%s" % (COMFY_INPUT.replace("\\", "/"), name))

    workdir = "%s/%s" % (REMOTE_ROOT.replace("\\", "/"), slug)
    ssh('if not exist "%s" mkdir "%s"' % (workdir.replace("/", "\\"),
                                          workdir.replace("/", "\\")), timeout=60)
    prompt_remote = "%s/prompt.txt" % workdir
    scp_up(prompt, prompt_remote)

    jid = submit(prompt_remote.replace("/", "\\"), ff_remote, lf_remote,
                 args.frames, args.width, args.height, args.seed, slug, args.label)
    log("已提交 job %s（默认分支 FL2VA，不带 --workflow）" % jid)

    state = wait_job(jid)
    if state.get("state") != "done":
        raise SystemExit("job %s 失败：%s" % (jid, state.get("note") or state.get("output")))
    media = remote_media(state)
    c_local = out_dir / ("C_%s_%df.mp4" % (slug, args.frames))
    scp_down(media, c_local)
    if not c_local.is_file() or c_local.stat().st_size == 0:
        raise SystemExit("产物下载失败: %s" % media)
    log("C 已取回: %s (%d bytes)" % (c_local, c_local.stat().st_size))

    # 两端验收：C 的首/末帧必须锁在指定的两帧上
    c_first = extract_edge(c_local, "first", out_dir / "C_first.png")
    c_last = extract_edge(c_local, "last", out_dir / "C_last.png")
    mad_ff = frame_mad(c_first, ff_local)
    mad_lf = frame_mad(c_last, lf_local)
    log("两端 MAD: 首 %.2f / 末 %.2f（<10 视为锁住）" % (mad_ff, mad_lf))
    # MAD 门限：≥10 视为没锁住（docstring 记录的失败案例 MAD 43.0），
    # 不继续 assemble，写结果 JSON 并 exit 1 供调用方判定。
    mad_ok = max(mad_ff, mad_lf) < 10.0
    if not mad_ok:
        print(json.dumps({
            "job": jid, "c": str(c_local), "mad_first": mad_ff, "mad_last": mad_lf,
            "mad_ok": False, "assemble": None, "gate": gate_note,
            "error": "MAD >= 10：首尾帧未锁住，不拼接",
        }, ensure_ascii=False, indent=2))
        return 1

    if args.assemble:
        joined = assemble(a, c_local, b, out_dir / ("%s-A+C+B.mp4" % slug))
        log("拼好: %s (%d 帧)" % (joined, probe_frames(joined)))

    print(json.dumps({
        "job": jid, "c": str(c_local), "mad_first": mad_ff, "mad_last": mad_lf,
        "mad_ok": True,
        "assemble": str(out_dir / ("%s-A+C+B.mp4" % slug)) if args.assemble else None,
        "gate": gate_note,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
