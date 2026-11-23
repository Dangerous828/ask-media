#!/usr/bin/env python3
"""检查「<文件> §N」式指向的目标文件里是否真有该编号的标题。

check_references.py 只验文件是否存在，验不了「这个文件里到底有没有 §2.8」——
补丁类提交删节/改节号后，指针会指向一个不存在的编号，而读者看不出来。

用法：python3 scripts/check_section_refs.py [--verbose]
退出码：0 无悬空；1 有悬空。
"""
import argparse
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 形如 `xxx.md` §2.8 / xxx.md 的 §2.8 / xxx.md §2.8
PAT = re.compile(r'([A-Za-z0-9_\-./]+\.md)`?\s*(?:的\s*)?§\s*(\d+(?:\.\d+)*)')
HEAD = r'^#{{1,4}}\s*{num}(?!\d)(?!\.\d)'


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    bad = []
    checked = 0
    os.chdir(ROOT)
    for path in glob.glob("**/*.md", recursive=True):
        if ".git" in path:
            continue
        try:
            text = io.open(path, encoding="utf-8").read()
        except OSError:
            continue
        for m in PAT.finditer(text):
            tgt, num = m.group(1), m.group(2)
            cands = [os.path.normpath(os.path.join(os.path.dirname(path), tgt)),
                     os.path.normpath(tgt)]
            resolved = next((c for c in cands if os.path.exists(c)), None)
            if resolved is None:
                continue          # 文件本身不存在 → 归 check_references.py 管
            try:
                body = io.open(resolved, encoding="utf-8").read()
            except OSError:
                continue
            checked += 1
            if not re.search(HEAD.format(num=re.escape(num)), body, re.M):
                line = text[:m.start()].count("\n") + 1
                bad.append((f"{path}:{line}", tgt, num, resolved))

    print(f"检查编号指向 {checked} 处，悬空 {len(bad)} 处")
    for loc, tgt, num, resolved in bad:
        print(f"  {loc}  →  {tgt} §{num}（{resolved} 里没有 §{num} 标题）")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
