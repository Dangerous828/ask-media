# -*- coding: utf-8 -*-
"""Static-validate a graph against the live /object_info before submitting.

直连 ComfyUI 127.0.0.1:8199（默认端口 8188，8199 为渲染机本机自定义端口），
但**只读 /object_info、不提交任何任务**，因此不违反 h3q 队列纪律；用于提交前
静态核对节点是否注册、输入是否齐全、连线是否可达 Save*。真正的提交仍走 h3q。
"""
import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8199"


def walk(obj):
    if isinstance(obj, dict):
        if "class_type" in obj:
            yield obj
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def main(path):
    try:
        with open(path, encoding="utf-8") as fh:
            d = json.load(fh)
    except (OSError, ValueError) as e:
        print("VALIDATE_FAIL: 读不到图 %s: %s" % (path, e))
        return 1
    g = d.get("graph") or d
    try:
        with urllib.request.urlopen(BASE + "/object_info", timeout=30) as r:
            objs = json.loads(r.read())
    except (urllib.error.URLError, OSError, ValueError) as e:
        print("VALIDATE_FAIL: 取不到 /object_info: %s" % e)
        return 1
    problems = []

    nodes = {}
    for nid, n in (g.items() if isinstance(g, dict) else []):
        if isinstance(n, dict) and "class_type" in n:
            nodes[str(nid)] = n

    for nid, n in sorted(nodes.items(), key=lambda kv: int(kv[0]) if kv[0].isdigit() else 0):
        ct = n["class_type"]
        spec = objs.get(ct)
        if spec is None:
            problems.append("node %s: class '%s' NOT registered" % (nid, ct))
            continue
        inp = spec.get("input") or {}
        req = inp.get("required") or {}
        opt = inp.get("optional") or {}
        ins = n.get("inputs") or {}
        for name in req:
            if name not in ins:
                problems.append("node %s [%s]: required input '%s' missing" % (nid, ct, name))
        for name, cfg in req.items():
            if not isinstance(cfg, list) or not cfg or name not in ins:
                continue
            kind = cfg[0]
            val = ins[name]
            is_link = isinstance(val, list) and len(val) == 2
            if isinstance(kind, list):          # COMBO of literal options
                if not is_link and val not in kind:
                    problems.append("node %s [%s]: %s=%r not in options %s"
                                    % (nid, ct, name, val, kind[:5]))
        # link targets must exist
        for name, val in ins.items():
            if isinstance(val, list) and len(val) == 2 and isinstance(val[0], str) and val[0].isdigit():
                if val[0] not in nodes:
                    problems.append("node %s [%s]: input '%s' links to missing node %s"
                                    % (nid, ct, name, val[0]))

    # unreachable-to-output check: every node must feed a Save* or a PreviewImage
    # (草稿图以 PreviewImage 结尾，没有 Save*，不能判「全部节点孤儿」)。
    outputs = [nid for nid, n in nodes.items()
               if n["class_type"].startswith("Save") or n["class_type"] == "PreviewImage"]
    reach = set()
    stack = list(outputs)
    while stack:
        cur = stack.pop()
        if cur in reach or cur not in nodes:
            continue
        reach.add(cur)
        for val in (nodes[cur].get("inputs") or {}).values():
            if isinstance(val, list) and len(val) == 2 and isinstance(val[0], str) and val[0].isdigit():
                stack.append(val[0])
    orphans = sorted(set(nodes) - reach, key=lambda x: int(x) if x.isdigit() else 0)
    if orphans:
        problems.append("orphan nodes (not reachable from any Save*/PreviewImage): %s" % orphans)

    if problems:
        print("VALIDATE_FAIL")
        for p in problems:
            print("  -", p)
        return 1
    print("VALIDATE_OK  %d nodes, %d reachable from Save*/PreviewImage" % (len(nodes), len(reach)))
    return 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python validate.py <graph.json>")
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
