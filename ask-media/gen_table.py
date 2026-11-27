#!/usr/bin/env python3
"""从 chain.json 生成 ask-media/SKILL.md 的阶段表。

改阶段只改 chain.json，然后跑：
    python3 gen_table.py

它会重写 SKILL.md 里 <!-- CHAIN:START --> 与 <!-- CHAIN:END --> 之间的内容，
其余部分一字不动。运行后自检：JSON 里每个阶段与技能都必须在生成的表里出现。
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CHAIN = os.path.join(HERE, "chain.json")
SKILL = os.path.join(HERE, "SKILL.md")

START = "<!-- CHAIN:START -->"
END = "<!-- CHAIN:END -->"


def render(chain):
    rows = [
        "| # | 阶段 | 产出文档 | 步骤 owner |",
        "|---|---|---|---|",
    ]
    for st in chain["chain"]:
        skills = " / ".join(f"`{n['skill']}`" for n in st["nodes"])
        raw = st.get("doc")
        if not raw:
            doc = "—"
        elif "`" in raw:
            # doc 自带反引号（如「剧本.md `## 分镜` + 场记.md」）：原样输出，
            # 再包一层会把整串变成同一段代码，嵌套反引号渲染即断。
            doc = raw
        else:
            doc = f"`{raw}`"
        rows.append(f"| {st['no']} | **{st['stage']}** | {doc} | {skills} |")
    return "\n".join(rows)


HUB = os.path.dirname(HERE)   # 仓库根（HERE 是 ask-media 本身）


def skill_exists(name):
    """技能真实存在：套件外直接在 hub 下，短剧套件在 drama-skills/skills 下。"""
    return (os.path.isdir(os.path.join(HUB, name))
            or os.path.isdir(os.path.join(HUB, "drama-skills", "skills", name)))


def selfcheck(chain, table):
    """两层检查：生成结果覆盖 JSON；JSON 里的技能在盘上真实存在。"""
    bad = []
    for st in chain["chain"]:
        if f"| {st['no']} | **{st['stage']}** |" not in table:
            bad.append(f"阶段缺失: {st['no']} {st['stage']}")
        for n in st["nodes"]:
            if f"`{n['skill']}`" not in table:
                bad.append(f"技能未进表: {n['skill']}")
            if not skill_exists(n["skill"]):
                bad.append(f"技能不存在于盘上: {n['skill']}")
    for n in chain.get("bypass", {}).get("nodes", []):
        if not skill_exists(n["skill"]):
            bad.append(f"旁路技能不存在: {n['skill']}")
    for n in chain.get("standalone", []):
        if not skill_exists(n["skill"]):
            bad.append(f"不进链技能不存在: {n['skill']}")
    if bad:
        print("校验失败：", file=sys.stderr)
        for b in bad:
            print("  " + b, file=sys.stderr)
        sys.exit(1)


def main():
    with open(CHAIN, encoding="utf-8") as f:
        chain = json.load(f)

    table = render(chain)
    selfcheck(chain, table)

    with open(SKILL, encoding="utf-8") as f:
        src = f.read()

    i, j = src.find(START), src.find(END)
    if i < 0 or j < 0:
        print(f"SKILL.md 缺少 {START} / {END} 标记", file=sys.stderr)
        sys.exit(1)

    out = src[: i + len(START)] + "\n" + table + "\n" + src[j:]
    changed = out != src
    if changed:
        with open(SKILL, "w", encoding="utf-8") as f:
            f.write(out)

    print(f"{len(chain['chain'])} 阶段 · 表{'已更新' if changed else '无变化'}")


if __name__ == "__main__":
    main()
