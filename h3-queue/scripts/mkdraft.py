# -*- coding: utf-8 -*-
"""mkdraft.py -- build a draft+upscale PDD graph for any shot.

This is the locked draft ladder (decided 2026-10-20, measured on this box):

    pass 1   1024x576  PDD nfe=8 euler        ~167 s
    upscale  latent 3D -> 1536x864 (1.5x)      (included below)
    pass 2   1536x864  PDD nfe=8 denoise=0.5   (included below)
    ---------------------------------------------------------------
    total                                     446.6 s measured

The point of this ladder: pass 1 fixes the composition, so what you approve in
the draft is what the upscale refines. Rendering straight at 1344x768 gives a
*different* frame (measured: same seed, different background/mountains), so a
draft at another resolution would not preview the master.

Usage (on the render box, from its workflow directory):
  python -s mkdraft.py --out <graph.json> --prompt-file <p.txt>
                       [--ref0 a.png] [--ref1 b.png]
                       [--seed 1017] [--frames 243] [--tag myshot]
                       [--no-upscale]      # pass-1 only (plain 1024x576 draft)
"""
import argparse
import json
import os

TEMPLATE = os.environ.get("H3Q_TEMPLATE", "03_submit_pdd_xiuxian_draft.json")

W1, H1 = 1024, 576          # locked draft tier
W2, H2 = 1536, 864          # 1.5x upscale target, both /32


def walk(obj):
    if isinstance(obj, dict):
        if "class_type" in obj:
            yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def add_upscale(g):
    """Insert latent-upscale + partial-denoise pass. Returns the new sampler id."""
    ids = {}
    for nid, n in g.items():
        if isinstance(n, dict) and "class_type" in n:
            ids.setdefault(n["class_type"], nid)

    need = ("SamplerCustomAdvanced", "BasicGuider", "KSamplerSelect", "RandomNoise")
    miss = [k for k in need if k not in ids]
    if miss:
        raise SystemExit("template is missing nodes: %s" % miss)

    g["300"] = {"class_type": "LTXVSeparateAVLatent",
                "inputs": {"av_latent": [ids["SamplerCustomAdvanced"], 0]}}
    g["301"] = {"class_type": "MinimaxH3LatentUpscaler3D",
                "inputs": {"latent": ["300", 0],
                           "model_name": "minimax_h3_latent_upscaler_3d_fp16.safetensors",
                           "mode": "target dimensions",
                           "mode.width": W2, "mode.height": H2,
                           "align": 32,
                           "enable_temporal_chunking": True,
                           "force_unload": True,
                           "device": "cuda", "precision": "fp16"}}
    g["302"] = {"class_type": "LTXVConcatAVLatent",
                "inputs": {"video_latent": ["301", 0], "audio_latent": ["300", 1]}}
    g["303"] = {"class_type": "MiniMaxH3PDDAccScheduler",
                "inputs": {"nfe": "8", "denoise": 0.5}}
    g["304"] = {"class_type": "SamplerCustomAdvanced",
                "inputs": {"noise": [ids["RandomNoise"], 0],
                           "guider": [ids["BasicGuider"], 0],
                           "sampler": [ids["KSamplerSelect"], 0],
                           "sigmas": ["303", 0],
                           "latent_image": ["302", 0]}}
    for _nid, n in g.items():
        if not isinstance(n, dict):
            continue
        ct = n.get("class_type")
        if ct in ("VAEDecode", "VAEDecodeAudio"):
            n["inputs"]["samples"] = ["304", 0]
    return "304"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--ref0", default="")
    ap.add_argument("--ref1", default="")
    ap.add_argument("--seed", type=int, default=1017)
    ap.add_argument("--frames", type=int, default=243)
    ap.add_argument("--tag", default="draft_lu")
    ap.add_argument("--no-upscale", action="store_true")
    a = ap.parse_args()

    d = json.load(open(TEMPLATE, encoding="utf-8"))
    g = d["graph"]
    prompt = open(a.prompt_file, encoding="utf-8").read().strip()
    if not prompt:
        raise SystemExit("empty prompt file: %s" % a.prompt_file)

    loads = [nid for nid, n in g.items()
             if isinstance(n, dict) and n.get("class_type") == "LoadImage"]
    loads.sort(key=lambda x: int(x) if x.isdigit() else 0)

    refs = [r for r in (a.ref0, a.ref1) if r]
    if len(refs) > len(loads):
        raise SystemExit("template has %d ref slots, got %d" % (len(loads), len(refs)))
    for nid, name in zip(loads, refs):
        g[nid]["inputs"]["image"] = name

    for n in walk(g):
        if n["class_type"] == "MiniMaxH3ReferenceToVideo":
            n["inputs"]["prompt"] = prompt
            n["inputs"]["width"] = W1
            n["inputs"]["height"] = H1
            n["inputs"]["length"] = a.frames
        elif n["class_type"] == "RandomNoise":
            n["inputs"]["noise_seed"] = a.seed
        elif n["class_type"] == "SaveVideo":
            n["inputs"]["filename_prefix"] = "video/%s" % a.tag

    ladder = "pass1 %dx%d nfe=8" % (W1, H1)
    if not a.no_upscale:
        add_upscale(g)
        ladder += " -> latent 1.5x -> %dx%d nfe=8 denoise=0.5" % (W2, H2)

    d["id"] = a.tag
    os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
    json.dump(d, open(a.out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("written: %s  (%d bytes)" % (a.out, os.path.getsize(a.out)))
    print("ladder : %s" % ladder)
    print("prompt : %d chars from %s" % (len(prompt), a.prompt_file))
    print("refs   : %s  seed=%s frames=%s" % (refs or "(none)", a.seed, a.frames))


if __name__ == "__main__":
    main()
