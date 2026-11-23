# -*- coding: utf-8 -*-
"""Submit one PDD graph and watch it to completion.

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
COMFY_OUT = r"E:\ComfyUI\ComfyUI_windows_portable\ComfyUI\output"


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
    d = json.load(open(graph_path, encoding="utf-8"))
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
        if time.time() - t0 > 7200:
            print("TIMEOUT after %.0fs peak=%.2f" % (time.time() - t0, peak), flush=True)
            return 1
        time.sleep(2)

    wall = time.time() - t0
    st = entry.get("status") or {}
    print("status=%s wall=%.1fs peak=%.2f GiB" % (st.get("status_str"), wall, peak), flush=True)

    outs = []
    for node in (entry.get("outputs") or {}).values():
        for key in ("images", "videos", "gifs"):
            for g in node.get(key) or []:
                if str(g.get("filename", "")).endswith(".mp4"):
                    outs.append(g)
    saved = ""
    if outs:
        g = outs[0]
        src = os.path.join(COMFY_OUT, g.get("subfolder", ""), g["filename"])
        dst = os.path.join(OUT, eid + ".mp4")
        shutil.copyfile(src, dst)
        saved = dst
        print("saved %s %d bytes" % (dst, os.path.getsize(dst)), flush=True)

    meta = {"id": eid, "status": st.get("status_str"), "wall": round(wall, 1),
            "peak_gib": round(peak, 2), "prompt_id": pid,
            "width": geo.get("w"), "height": geo.get("h"),
            "frames": geo.get("len"), "nfe": geo.get("nfe"),
            "msgs": [str(m)[:300] for m in (st.get("messages") or [])[-3:]]}
    json.dump(meta, open(os.path.join(OUT, eid + ".meta.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print("META " + json.dumps(meta, ensure_ascii=False)[:500], flush=True)
    return 0 if saved else 1


if __name__ == "__main__":
    sys.exit(main())
