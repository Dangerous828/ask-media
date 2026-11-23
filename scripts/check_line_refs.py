#!/usr/bin/env python3
"""检查「<文件>:<行号>」式指向的行号是否越界。

check_references.py 只验文件在不在，check_section_refs.py 验 §N 节号；
这一层验行号。文件被删减后，行号指针最容易失效，而读者看不出来——
打开文件翻到那一行，看到的是别的段落。

它只能挡「越界」（行号 > 文件行数）。「行号在界内但指向的内容已经变了」
查不出来：那需要理解语义，本脚本不做，只能靠改动时人工复核。

用法：python3 scripts/check_line_refs.py
退出码：0 无越界；1 有越界。
"""
import glob
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAT = re.compile(r'`([A-Za-z0-9_./\-]+\.(?:md|txt|py|json|sh|ps1)):(\d+)(?:-(\d+))?`')
# 历史档整份豁免（与 check_references.py 的 ARCHIVE_DOC 同口径）
ARCHIVE = re.compile(r'(MEASURED-|HANDOFF-|结论-)')


def main() -> int:
    os.chdir(ROOT)
    bad, checked = [], 0
    for path in glob.glob("**/*.md", recursive=True):
        if ".git" in path or ARCHIVE.search(path) or "creative-dna-t8" in path:
            continue
        try:
            text = io.open(path, encoding="utf-8").read()
        except OSError:
            continue
        for m in PAT.finditer(text):
            tgt, start, end = m.group(1), int(m.group(2)), m.group(3)
            cands = [os.path.normpath(os.path.join(os.path.dirname(path), tgt)),
                     os.path.normpath(tgt)]
            resolved = next((c for c in cands if os.path.exists(c)), None)
            if resolved is None:
                continue          # 文件不存在 → 归 check_references.py 管
            try:
                total = len(io.open(resolved, encoding="utf-8").read().split("\n"))
            except OSError:
                continue
            checked += 1
            hi = max(start, int(end)) if end else start
            if hi > total:
                line = text[:m.start()].count("\n") + 1
                bad.append(f"{path}:{line}  →  {tgt}:{start}{'-' + end if end else ''}"
                           f"（{resolved} 仅 {total} 行）")

    print(f"检查行号指向 {checked} 处，越界 {len(bad)} 处")
    for b in bad:
        print("  " + b)
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
