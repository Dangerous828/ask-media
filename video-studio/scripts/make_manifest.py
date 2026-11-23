#!/usr/bin/env python3
"""make_manifest.py — 为产物生成可追溯 manifest。

产物散落 /tmp 时无法复核（出图后立刻调用本脚本、落进项目目录即可避免）。
每条 manifest 冻结 profile / 脚本 / 提示词 / 图片的 SHA-256，供事后追溯。

用法：
    python3 make_manifest.py --out <manifest.json> --profile 3d_anime \
        --prompt <prompt.txt> --image <img.png> [--image ...] [--note "..."]
"""
import argparse, hashlib, json, sys
from datetime import datetime, timezone
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--profile", required=True)
    ap.add_argument("--prompt", action="append", default=[], help="可多次传")
    ap.add_argument("--image", action="append", default=[], help="可多次传")
    ap.add_argument("--seed", type=int)
    ap.add_argument("--size")
    ap.add_argument("--note", default="")
    args = ap.parse_args()

    profile_path = SKILL_DIR / "profiles" / f"{args.profile}.md"
    if not profile_path.exists():
        print(f"ERROR: profile 不存在: {profile_path}", file=sys.stderr)
        return 2

    entry = {
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "profile": args.profile,
        "profile_sha256": sha256(profile_path),
        "build_prompt_sha256": sha256(SKILL_DIR / "scripts" / "build_prompt.py"),
        "qc_image_sha256": sha256(SKILL_DIR / "scripts" / "qc_image.py"),
        "seed": args.seed,
        "size": args.size,
        "note": args.note,
        "prompts": [{"path": str(p), "sha256": sha256(Path(p))} for p in args.prompt],
        "images": [{"path": str(p), "sha256": sha256(Path(p))} for p in args.image],
    }
    # --prompt / --image 的路径不存在时给出干净报错（exit 2），不要抛未捕获的 FileNotFoundError traceback。
    for p in list(args.prompt) + list(args.image):
        if not Path(p).is_file():
            print(f"ERROR: 文件不存在: {p}", file=sys.stderr)
            return 2

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    existing = []
    if out.exists():
        try:
            existing = json.loads(out.read_text(encoding="utf-8"))
            if isinstance(existing, dict):
                existing = [existing]
        except Exception:
            existing = []
    existing.append(entry)
    out.write_text(json.dumps(existing, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"OK 追加 1 条到 {out}（共 {len(existing)} 条）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
