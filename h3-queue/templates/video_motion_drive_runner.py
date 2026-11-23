# 视频动作驱动 一次性投递 runner（Windows 侧）。提交一次、轮询 /history、按 SaveVideo 节点取回产物。
# 用法见 references/video-motion-drive.md §5。WD/GRAPH 等路径按任务改。
# 本 runner 直连 ComfyUI 127.0.0.1:8199（默认端口 8188，8199 为渲染机本机自定义端口），
# 不经 h3q 队列：无准入控制、无幂等、不与其他 GPU 任务互斥，属 h3-queue 三条硬纪律的
# 明文例外。仅限动作驱动这条通道（h3q 不支持视频动作参考），且须满足 §2 的人工门禁：
# 确认 GPU 空闲、单次提交不重试、创作者已明确批准耗时。不可挪作常规出图/出视频。
import json, os, sys, time, shutil, subprocess, traceback, urllib.request, urllib.error

BASE = "http://127.0.0.1:8199"
# 默认 "."：launch_detached.ps1 以 -WorkDir 作为 CurrentDirectory 启动本脚本，
# 图与产物都放在该工作目录。若设成 "motion_drive_delivery" 会与文档里
# -WorkDir <ComfyUI根>\motion_drive_delivery 的配方拼成两级嵌套、找不到 graph.json。
# 也可用 MOTION_DRIVE_WD 显式指定绝对路径覆盖。
WD = os.environ.get("MOTION_DRIVE_WD", ".")
GRAPH = os.path.join(WD, "graph.json")
STATUS = os.path.join(WD, "status.json")
OUTPUT_ROOT = os.environ.get("COMFYUI_OUTPUT", "ComfyUI/output")
TARGET = os.path.join(WD, "motion-drive-output.mp4")
META = os.path.join(WD, "motion-drive-output.meta.json")
SAVE_NODE = "11"
# 实测 345f 动作驱动跑 7000s（约 1.94h）；默认 3h 上限，可用 MOTION_DRIVE_TIMEOUT 覆盖。
POLL_TIMEOUT = int(os.environ.get("MOTION_DRIVE_TIMEOUT", "10800"))


def api(path, data=None, timeout=60):
    body = json.dumps(data).encode("utf-8") if data is not None else None
    req = urllib.request.Request(BASE + path, data=body,
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
        return json.loads(raw or b"null")
    except urllib.error.HTTPError as e:
        return {"_http_error": e.code, "_body": e.read().decode("utf-8", "replace")[:3000]}
    except Exception as e:
        return {"_error": repr(e)}


def status(**kw):
    cur = {}
    if os.path.exists(STATUS):
        try:
            cur = json.load(open(STATUS, encoding="utf-8"))
        except Exception:
            pass
    cur.update(kw)
    cur["updated"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    tmp = STATUS + ".tmp"
    json.dump(cur, open(tmp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    os.replace(tmp, STATUS)


def vram_gib():
    try:
        out = subprocess.check_output(
            ["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"],
            text=True, timeout=20)
        return float(out.split()[0]) / 1024.0
    except Exception:
        return 0.0


def main():
    status(phase="starting", wall_start=time.time())
    graph = json.load(open(GRAPH, encoding="utf-8"))["graph"]
    t0 = time.time()
    r = api("/prompt", {"prompt": graph, "client_id": "motion-drive-delivery"})
    if not isinstance(r, dict) or "prompt_id" not in r:
        status(phase="SUBMIT_FAIL", submitted=False, response=r, wall=round(time.time()-t0, 1))
        print("SUBMIT_FAIL", r, flush=True)
        return 1
    pid = r["prompt_id"]
    status(phase="submitted", submitted=True, prompt_id=pid,
           submit_response=r, wall_start=t0)
    print("SUBMITTED", pid, flush=True)

    peak = 0.0
    ticks = 0
    while True:
        peak = max(peak, vram_gib())
        h = api("/history/" + pid, timeout=30)
        q = api("/queue", timeout=30)
        ticks += 1
        if ticks % 6 == 0 or (isinstance(h, dict) and pid in h):
            state = "unknown"
            if isinstance(q, dict):
                running = len(q.get("queue_running") or [])
                pending = len(q.get("queue_pending") or [])
                state = "running=%d pending=%d" % (running, pending)
            status(phase="monitoring", elapsed=round(time.time()-t0, 1),
                   peak_gib=round(peak, 2), queue=state,
                   history_ready=bool(isinstance(h, dict) and pid in h))
        if isinstance(h, dict) and pid in h:
            break
        if time.time() - t0 > POLL_TIMEOUT:
            status(phase="POLL_TIMEOUT", elapsed=round(time.time() - t0, 1),
                   peak_gib=round(peak, 2))
            print("POLL_TIMEOUT after %ss (prompt_id=%s, 查 /history 与 /queue)" %
                  (POLL_TIMEOUT, pid), flush=True)
            return 1
        if isinstance(h, dict) and "_error" in h and ticks > 5:
            status(phase="HISTORY_ERROR", history_response=h)
        time.sleep(5)

    wall = time.time() - t0
    entry = h[pid]
    st = entry.get("status", {}) or {}
    outs = entry.get("outputs", {}) or {}
    cands = []
    for nid, nodeouts in outs.items():
        for key in ("videos", "images", "gifs"):
            for g in (nodeouts.get(key) or []):
                fn = g.get("filename", "")
                if not fn.lower().endswith(".mp4"):
                    continue
                if g.get("type", "output") != "output":
                    continue
                src = os.path.join(OUTPUT_ROOT, g.get("subfolder", ""), fn)
                if os.path.exists(src):
                    cands.append({"node": nid, "key": key, "src": src,
                                  "filename": fn, "subfolder": g.get("subfolder", ""),
                                  "type": g.get("type", "output"), "size": os.path.getsize(src),
                                  "meta": g})
    result = {
        "prompt_id": pid,
        "status_str": st.get("status_str"),
        "wall_s": round(wall, 1),
        "peak_gib": round(peak, 2),
        "candidates": [{k: v for k, v in c.items() if k != "meta"} for c in cands],
        "messages": [str(m)[:500] for m in (st.get("messages") or [])[-6:]],
    }
    chosen = None
    for c in cands:
        if c["node"] == SAVE_NODE:
            chosen = c
            break
    # 不做 cands[0] 兜底：LoadVideo 会把输入动作视频也列进 images，任意取第一个
    # 恰好可能取到输入视频（文档 §5 警告过的坑）。找不到 SaveVideo 节点产物就报错。
    if chosen is None:
        result["warning"] = ("no SaveVideo(node %s) product in /history outputs; "
                             "不取兜底候选，避免误取输入动作视频" % SAVE_NODE)
        with open(META, "w", encoding="utf-8") as fh:
            json.dump(result, fh, ensure_ascii=False, indent=2)
        status(phase="NO_SAVEVIDEO_OUTPUT", **result)
        print("NO_SAVEVIDEO_OUTPUT", result["warning"], flush=True)
        return 1
    shutil.copyfile(chosen["src"], TARGET)
    result["output_local"] = TARGET
    result["output_size"] = os.path.getsize(TARGET)
    result["chosen"] = {k: v for k, v in chosen.items() if k != "meta"}
    json.dump(result, open(META, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    status(phase="FINISHED", **result)
    print("FINISHED", json.dumps(result, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception:
        status(phase="RUNNER_EXCEPTION", traceback=traceback.format_exc()[-3000:])
        print(traceback.format_exc(), flush=True)
        sys.exit(1)
