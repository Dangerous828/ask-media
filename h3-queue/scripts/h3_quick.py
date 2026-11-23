# -*- coding: utf-8 -*-
"""h3_quick.py -- 快捷出片：一条命令选档位，不用碰 lib_workflow.py。

依赖（不随本仓库发布）：lib_workflow.py 是渲染机侧私有定制脚本，须另行取得并放在
本脚本同目录；缺它则在 import 处报 ImportError。本脚本直连 ComfyUI 8199（默认
8188，本机自定义端口），仅供离线研究、不部署、不调用；真实生产走 h3q 队列。

在渲染机（Windows）上、ComfyUI 的内嵌 python 下运行：
  <ComfyUI 内嵌 python.exe> -s h3_quick.py ^
     --tier draft|hq|ref8|ref6 --prompt-file P --first-frame F ^
     [--refs a.png,b.png] [--width 768 --height 1344 --frames 107 --seed 11] ^
     [--slug myshot] [--dry-run] [--submit]

模式由档位决定（draft/hq=i2va，ref8/ref6=ref2va），不另设 --mode。

档位定义：
  draft  = fl2va_turbo_Q4_K_M.gguf（你原来的草稿档，4bit + turbo 烘焙）  仅 i2va/t2va
  hq     = fl2va_pruned_w6a8.safetensors + fl2v_turbo_8step_v1.0_768p     仅 i2va/t2va
  ref8   = ref2va_pruned_int8_convrot.safetensors（8bit，生产在用）       仅 ref2va
  ref6   = ref2va_pruned_w6a8.safetensors + ref2v_turbo_8step_v1.1_768p   仅 ref2va
"""
import sys, os, re, json, argparse, time, urllib.request, urllib.error

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))  # lib_workflow 与本脚本同目录
import lib_workflow as W

PORT = 8199
BASE = "http://127.0.0.1:%d" % PORT

TIERS = {
    "draft": {
        "mode": "i2va",
        "unet": "minimax_h3_fl2va_turbo_Q4_K_M.gguf",
        "lora": None,
        "steps": 8,
        "loader": "gguf",
    },
    "hq": {
        "mode": "i2va",
        "unet": "minimax_h3_fl2va_pruned_w6a8.safetensors",
        "lora": "minimax_h3_fl2v_turbo_8step_v1.0_768p_comfyui_bf16.safetensors",
        "steps": 8,
        "loader": "safetensors",
    },
    "ref8": {
        "mode": "ref2va",
        "unet": "minimax_h3_ref2va_pruned_int8_convrot.safetensors",
        "lora": None,
        "steps": 20,
        "loader": "safetensors",
    },
    "ref6": {
        "mode": "ref2va",
        "unet": "minimax_h3_ref2va_pruned_w6a8.safetensors",
        "lora": "minimax_h3_ref2v_turbo_8step_v1.1_768p_comfyui_bf16.safetensors",
        "steps": 8,
        "loader": "safetensors",
    },
}


def api(path, payload=None, timeout=120):
    data = None
    headers = {}
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(BASE + path, data=data, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, "HTTP %s: %s" % (e.code, e.read().decode("utf-8", "replace")[:1200])
    except Exception as e:
        return None, str(e)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", required=True, choices=sorted(TIERS))
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--first-frame", default="")
    ap.add_argument("--refs", default="", help="逗号分隔（仅 ref2va）")
    ap.add_argument("--width", type=int, default=768)
    ap.add_argument("--height", type=int, default=1344)
    ap.add_argument("--frames", type=int, default=107)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--steps", type=int, default=0, help="0=用档位默认")
    ap.add_argument("--slug", default="quick")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--submit", action="store_true")
    a = ap.parse_args()

    tier = TIERS[a.tier]
    # slug 消毒：只留安全字符，防止拼进 prefix / 输出文件名时越界或注入。
    slug = re.sub(r"[^A-Za-z0-9_-]+", "-", a.slug).strip("-")[:60] or "quick"
    prompt = open(a.prompt_file, encoding="utf-8").read()
    prefix = "h3studio/%s_%s" % (slug, a.tier)
    steps = a.steps or tier["steps"]

    if tier["mode"] == "i2va":
        if not a.first_frame:
            sys.exit("tier %s 需要 --first-frame" % a.tier)
        g = W.build_i2va(a.width, a.height, a.frames, prompt, prefix,
                         a.first_frame, seed=a.seed, steps=steps)
    else:
        refs = [r.strip() for r in a.refs.split(",") if r.strip()]
        if not refs:
            sys.exit("tier %s 需要 --refs" % a.tier)
        g = W.build_ref2va(a.width, a.height, a.frames, prompt, prefix, refs,
                           seed=a.seed, steps=steps)

    # 换底模
    if tier["loader"] == "gguf":
        g["1"] = {"class_type": "UnetLoaderGGUFAdvanced",
                  "inputs": {"unet_name": tier["unet"], "dequant_dtype": "default",
                             "patch_dtype": "default", "patch_on_device": False}}
    else:
        g["1"] = {"class_type": "UNETLoader",
                  "inputs": {"unet_name": tier["unet"], "weight_dtype": "default"}}

    # 挂 LoRA
    if tier["lora"]:
        g["30"] = {"class_type": "LoraLoaderModelOnly",
                   "inputs": {"model": ["1", 0], "lora_name": tier["lora"],
                              "strength_model": 1.0}}
        g["6"]["inputs"]["model"] = ["30", 0]

    print("TIER=%s  mode=%s  unet=%s  lora=%s  steps=%d  %dx%d f=%d seed=%d"
          % (a.tier, tier["mode"], tier["unet"], tier["lora"] or "none",
             steps, a.width, a.height, a.frames, a.seed), flush=True)

    if a.dry_run:
        print(json.dumps({"prompt": g}, ensure_ascii=False, indent=2))
        return 0

    if not a.submit:
        print("(grab a --submit to actually render, or --dry-run to print the graph)")
        return 0

    res, err = api("/prompt", {"prompt": g, "client_id": "h3quick-" + a.tier})
    if err:
        print("SUBMIT_FAIL " + err)
        return 1
    if not isinstance(res, dict) or not res.get("prompt_id"):
        print("SUBMIT_FAIL 响应缺少 prompt_id: %s" % str(res)[:500])
        return 1
    pid = res["prompt_id"]
    print("queued pid=" + pid, flush=True)

    t0 = time.time()
    peak = 0.0
    entry = None
    # 7000s 级长任务（动作驱动）会远超 1h；默认放宽到 3h，可用 H3Q_QUICK_TIMEOUT 覆盖。
    poll_timeout = int(os.environ.get("H3Q_QUICK_TIMEOUT", "10800"))
    while time.time() - t0 < poll_timeout:
        out, _ = api("/history/" + pid, timeout=30)
        if out and pid in out:
            entry = out[pid]
            break
        st, _ = api("/system_stats", timeout=20)
        if st:
            try:
                d = st["devices"][0]
                peak = max(peak, (d["vram_total"] - d["vram_free"]) / (1024 ** 3))
            except Exception:
                pass
        time.sleep(5)

    if not entry:
        print("TIMEOUT")
        return 2

    paths = []
    for _, nd in (entry.get("outputs") or {}).items():
        for v in (nd.get("images") or []) + (nd.get("videos") or []) + (nd.get("gifs") or []):
            if v.get("filename"):
                paths.append((v.get("subfolder") or "", v["filename"]))

    meta = {
        "tier": a.tier, "mode": tier["mode"], "unet": tier["unet"], "lora": tier["lora"],
        "steps": steps, "width": a.width, "height": a.height, "frames": a.frames,
        "seed": a.seed, "wall_seconds": round(time.time() - t0, 1),
        "peak_vram_gib": round(peak, 2), "prompt_id": pid,
        "outputs": paths, "workflow": g,
    }
    out_dir = os.environ.get("H3Q_OUT_DIR", "renders")
    os.makedirs(out_dir, exist_ok=True)
    mp = os.path.join(out_dir, "quick_%s.json" % slug)
    with open(mp, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)
    print("META " + mp)
    for sub, fn in paths:
        print("OUTPUT " + (sub + "/" if sub else "") + fn)
    return 0


if __name__ == "__main__":
    sys.exit(main())
