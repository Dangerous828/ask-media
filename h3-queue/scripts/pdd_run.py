# -*- coding: utf-8 -*-
"""Submit one PDD graph and watch it to completion（离线研究/手工应急直投通道）。

本脚本直连 ComfyUI 127.0.0.1:8199（默认端口是 8188，8199 为渲染机本机自定义），
绕过 h3q 队列：不获准入控制、无幂等、不与队列互斥。**不部署、不调用**；真实生产一律
走 h3q（见 ../SKILL.md）。仅在队列停机、且创作者明确授权时的手工应急才可用本脚本，
且必须自己确认 GPU 空闲（脚本会等 idle）。

Waits until ComfyUI has nothing running or pending, so it never preempts a job
that is already rendering. Then submits, samples nvidia-smi every 2 s for the
VRAM peak, and saves the mp4 plus a meta json.

  python -s pdd_run.py <graph.json> <out_dir>
"""
import json
import os
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8199"
# 必须设为渲染机上 ComfyUI 的实际 output 绝对路径。本脚本不提供默认值：相对路径
# "ComfyUI/output" 只在 ComfyUI 根目录作为当前目录运行时成立，换目录运行会拷错地方。
if not os.environ.get("COMFYUI_OUTPUT"):
    sys.exit("必须设置 COMFYUI_OUTPUT 为渲染机 ComfyUI 的实际 output 绝对路径"
             "（默认相对路径只在一个特定工作目录成立，故不再提供默认值）")
COMFY_OUT = os.environ["COMFYUI_OUTPUT"]
# 等渲染超时：7000s 级长任务（动作驱动）会逼近 2h，默认放宽到 6h，与等空闲一致。
RENDER_TIMEOUT = int(os.environ.get("H3Q_RENDER_TIMEOUT", "21600"))


def api(path, payload=None, timeout=60):
    req = urllib.request.Request(
        BASE + path,
        data=json.dumps(payload).encode() if payload else None,
        headers={"Content-Type": "application/json"})
    try:
        return json.loads(urllib.request.urlopen(req, timeout=timeout).read() or b"null")
    except urllib.error.HTTPError as e:
        return {"_err": e.read().decode("utf-8", "replace")[:1500]}
    except Exception as e:                                    # noqa: BLE001
        return {"_err": "%s: %s" % (type(e).__name__, e)}


def used_gib():
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            text=True).split()[0]
        return float(out) / 1024.0
    except Exception:                                         # noqa: BLE001
        return 0.0


def wait_idle(max_wait=21600):
    """Hold until the box is free. Never preempt another render."""
    t0 = time.time()
    while time.time() - t0 < max_wait:
        q = api("/queue", timeout=20)
        # 查询失败时「查不到」不等于「空闲」：绝不把未知当空闲去抢占别人的渲染。
        if "_err" in q:
            print("  queue 查询失败（%s），视为未知、继续等待，不抢占渲染"
                  % str(q["_err"])[:200], flush=True)
            time.sleep(15)
            continue
        running = len(q.get("queue_running") or [])
        pending = len(q.get("queue_pending") or [])
        if running == 0 and pending == 0:
            return True
        print("  busy (running=%d pending=%d) %.0fs, waiting..."
              % (running, pending, time.time() - t0), flush=True)
        time.sleep(15)
    return False


def main():
    if len(sys.argv) < 3:
        print("usage: pdd_run.py <graph.json> <out_dir>")
        return 2
    graph_path, OUT = sys.argv[1], sys.argv[2]
    os.makedirs(OUT, exist_ok=True)
    with open(graph_path, encoding="utf-8") as fh:
        d = json.load(fh)
    for k in ("id", "graph"):
        if k not in d:
            print("graph 缺少键: %s" % k, flush=True)
            return 2
    eid = d["id"]
    graph = d["graph"]

    # report the geometry we are about to ask for
    def walk(obj):
        if isinstance(obj, dict):
            if "class_type" in obj:
                yield obj
            for v in obj.values():
                yield from walk(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from walk(v)

    geo = {}
    for n in walk(graph):
        if n["class_type"] == "MiniMaxH3ReferenceToVideo":
            geo = {"w": n["inputs"]["width"], "h": n["inputs"]["height"],
                   "len": n["inputs"]["length"]}
        if n["class_type"] == "MiniMaxH3PDDAccApply":
            geo["nfe"] = n["inputs"]["nfe"]
    print("graph: %s" % graph_path, flush=True)
    print("geometry: %sx%s len=%s nfe=%s" % (geo.get("w"), geo.get("h"),
                                             geo.get("len"), geo.get("nfe")), flush=True)

    print("waiting for ComfyUI to be idle ...", flush=True)
    if not wait_idle():
        print("gave up waiting for an idle box", flush=True)
        return 3

    api("/free", {"unload_models": True, "free_memory": True}, timeout=120)
    time.sleep(4)
    print("idle. vram_used=%.2f GiB" % used_gib(), flush=True)

    t0 = time.time()
    r = api("/prompt", {"prompt": graph, "client_id": "pdd-run"})
    if "_err" in r or "prompt_id" not in r:
        print("SUBMIT_FAIL", json.dumps(r, ensure_ascii=False)[:1200], flush=True)
        return 1
    pid = r["prompt_id"]
    print("submitted prompt_id=%s" % pid, flush=True)

    peak = 0.0
    entry = None
    while True:
        peak = max(peak, used_gib())
        h = api("/history/" + pid, timeout=30)
        if h and isinstance(h, dict) and pid in h:
            entry = h[pid]
            break
        if time.time() - t0 > RENDER_TIMEOUT:
            print("TIMEOUT after %.0fs peak=%.2f" % (time.time() - t0, peak), flush=True)
            return 1
        time.sleep(2)

    wall = time.time() - t0
    st = entry.get("status") or {}
    print("status=%s wall=%.1fs peak=%.2f GiB" % (st.get("status_str"), wall, peak), flush=True)

    # ComfyUI 的 H3 产物可能是 .mp4/.webm/.mov，后缀不能写死。
    VIDEO_EXT = (".mp4", ".webm", ".mov")
    outs = []
    for node in (entry.get("outputs") or {}).values():
        for key in ("images", "videos", "gifs"):
            for g in node.get(key) or []:
                if str(g.get("filename", "")).lower().endswith(VIDEO_EXT):
                    outs.append(g)
    saved = ""
    if outs:
        g = outs[0]
        # subfolder/filename 来自服务端，拒绝绝对路径与 ..，防止拷出 COMFY_OUT/OUT。
        subfolder = g.get("subfolder", "") or ""
        filename = g["filename"]
        src_base = os.path.realpath(COMFY_OUT)
        src = os.path.realpath(os.path.join(src_base, subfolder, filename))
        if not (src == src_base or src.startswith(src_base + os.sep)):
            print("产物路径越界，拒绝拷贝: %r / %r" % (subfolder, filename), flush=True)
            return 1
        ext = os.path.splitext(filename)[1].lower()
        dst = os.path.join(OUT, eid + ext)
        shutil.copyfile(src, dst)
        saved = dst
        print("saved %s %d bytes" % (dst, os.path.getsize(dst)), flush=True)

    meta = {"id": eid, "status": st.get("status_str"), "wall": round(wall, 1),
            "peak_gib": round(peak, 2), "prompt_id": pid,
            "width": geo.get("w"), "height": geo.get("h"),
            "frames": geo.get("len"), "nfe": geo.get("nfe"),
            "msgs": [str(m)[:300] for m in (st.get("messages") or [])[-3:]]}
    with open(os.path.join(OUT, eid + ".meta.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, ensure_ascii=False, indent=1)
    print("META " + json.dumps(meta, ensure_ascii=False)[:500], flush=True)
    return 0 if saved else 1


if __name__ == "__main__":
    sys.exit(main())
