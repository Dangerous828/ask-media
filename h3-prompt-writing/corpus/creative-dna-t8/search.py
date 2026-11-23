#!/usr/bin/env python3
import json,sys,os
from pathlib import Path
BASE=Path(__file__).resolve().parent
rows=json.loads((BASE/"catalog.json").read_text(encoding="utf-8"))
args=[a for a in sys.argv[1:] if not a.startswith("--")]
limit=20
if "--limit" in sys.argv:
    try: limit=int(sys.argv[sys.argv.index("--limit")+1])
    except Exception: pass
if not args:
    print("用法：python3 search.py 关键词 [关键词...] [--limit N]")
    print("例：python3 search.py 身份 情绪 停顿")
    sys.exit(0)
def score(r):
    blob=" ".join([r["titleZh"],r["titleEn"],r["mechanism"],r["summary"]," ".join(r["tags"])," ".join(r["applicable"])]).lower()
    return sum(blob.count(k.lower()) for k in args)
hits=[r for r in rows if score(r)>0]
hits.sort(key=lambda r:-score(r))
print(f"命中 {len(hits)} 条，显示前 {min(limit,len(hits))} 条：")
for r in hits[:limit]:
    p=BASE/r["path"]
    print(f"- {r['titleZh']} [{r['kind']}] {'OK' if p.exists() else 'MISSING'}")
    if r["mechanism"]: print("  机制："+r["mechanism"][:130])
    print("  原文："+str(p))
