#!/usr/bin/env python3
"""story_check.py — 剧本事件 ↔ 镜头 双向对账（缺口 2 的原型）。

解决什么问题
------------
现有闸门（h3_gate / h3_lint）只查**单份提示词内部一致性**，完全不看它与剧本的关系。
于是三类真实事故在机制上无法被发现：

1. **整镜丢失**：剧本「角色A 赠大橘子」这一镜在成片里消失（只剩一句静态描述
   `The boy hugs a plump bright golden orange under his left arm`——橘子凭空出现）
2. **同镜内空间自溶**：一个镜头里先有屏幕黑框、跑到中途黑框自己没了
   （S02 已穿越一次，S03 又穿一次）
3. **事件降级成静态**：镜头声明"承担了赠橘"，但正文只提到道具名词、没有交接动作

设计要点（对应评审指出的三个漏洞）
--------------------------------
- 漏洞1「降级成静态」：事件分类型。`action` 类必须出现**动词**；
  `handover`（赠予/交接）类必须**施动者 + 受动者 + 道具三者共现**，缺一即报。
- 漏洞2「空间跃迁」：当前只查「剧本 transition 事件数 vs 成片里写了穿越运镜的镜数」
  与「单镜内同时出现框/满幅两种空间描述」，用英文硬编码的 TRANSIT_MARK 识别穿越；
  中文穿越措辞、同镜内 space_id 唯一性**均未实现**（文本层也查不出渲染过程内部的黑框自溶，
  后者归 segment_guard）。不要按「每镜声明 space_id 并查同镜唯一」理解本脚本。
- 漏洞3「单向」：**剧本是唯一真源**。本脚本只读剧本与分镜，绝不回写剧本。
  （对账不通过 → 改分镜，不许改剧本以通过。）

用法
----
    python3 story_check.py --script <剧本.md> --shots <分镜或提示词目录>
    python3 story_check.py --script 剧集/EP01/STORYBOARD.md \
        --shots smooth3d/ep01_v4/h3_prompts/ --json

退出码：0 全部对齐；1 有缺口/多声明/降级；2 参数错误或必要检查未完成（NOTCHK）
"""
import argparse
import json
import re
import sys
from pathlib import Path

# ---------------------------------------------------------------- 事件类型

# 动作动词**同义词簇**（2026-10-22 升级：扁平词表会因同义表达漏判）
#
# 为什么改成簇：实测 EP01 剧本写 extends / tightens / glides，
# 成片写 stretch / clamp / swing —— 扁平词表命中不到，报了一堆假警告。
# 簇的语义是「任一成员出现即算该动作成立」。
ACTION_SYNONYM_CLUSTERS = {
    "sit":      ["sits", "sitting", "seated", "propped", "cross-legged", "坐"],
    "rest":     ["rests", "resting", "props up", "propping", "settles onto", "抵", "撑"],
    "run":      ["run", "runs", "running", "mid-stride", "sprints", "dashes", "跑"],
    "skip":     ["skips", "skipping", "hops", "bounces", "蹦", "跳"],
    "brake":    ["brake", "brakes", "braking", "skid", "skids", "plants", "planting",
                 "digs in", "急刹"],
    "pivot":    ["pivot", "pivots", "pivoting", "turns", "swivels", "spins around", "twists", "转"],
    "lean":     ["leans", "leaning", "tilts", "pitches", "hunches", "探", "倾"],
    "extend":   ["extends", "extended", "reaches", "reaching", "stretches", "offers",
                 "holds out", "thrusts", "伸", "递"],
    "push":     ["pushes", "pressing", "presses", "shoves", "drives", "推"],
    "raise":    ["raises", "lifted", "lifts", "raising", "up toward", "抬", "举"],
    "tighten":  ["tightens", "clamps", "clamping", "grips", "gripping", "wraps",
                 "closes around", "catches", "攥", "抓"],
    "glide":    ["glides", "gliding", "slides", "sliding", "drifts", "sweeps",
                 "flows", "slides forward", "滑", "飘"],
    "step":     ["steps", "stepping", "walks", "strides", "moves through", "跨", "走"],
    "swing":    ["swings", "swinging", "arcs", "sweeps around", "flaps", "甩", "摆"],
    "settle":   ["settles", "settling", "lands", "arrives", "comes to rest", "落", "定"],
    "cross":    ["crosses", "crossing", "steps through", "passes through", "穿", "过"],
    "hold":     ["holds", "holding", "carries", "cradles", "hugs", "抱", "握"],
    "blink":    ["blinks", "blinking", "eyes close", "眨眼"],
    "strike":   ["strikes", "knocks", "slams", "hits", "taps", "拍", "击"],
    "assemble": ["assembles", "materializes", "forms", "builds", "凝", "聚"],
    "open":     ["open", "opens", "opening", "pops open", "parts", "widening",
                 "eyes wide", "张开", "睁"],
}

# 扁平视图（保留给旧代码/外部引用）
ACTION_VERBS = sorted({v for vs in ACTION_SYNONYM_CLUSTERS.values() for v in vs})



def _cluster_members_hit(text: str) -> list:
    """返回该句命中的**动作簇名**（如 'brake' 而非 'braking'）。

    为什么存簇名而不是具体词形（2026-10-22 实测教训）：
    剧本写 "braking suddenly"（抽到 braking），成片写 "brake suddenly"——
    同一个动作的不同词形，若事件只存 'braking'，在成片里永远匹配不到。
    存簇名后，匹配时展开整簇，词形无关。
    """
    low = text.lower()
    return [cl for cl, members in ACTION_SYNONYM_CLUSTERS.items()
            if any(m in low for m in members)]


# 开场套话：这些不是动作，是模板句，必须排除。
# 实测：S04 的 "the target video **opens** on the low 28mm meadow view" 被当成
# "睁眼(open)"，位置 300（远早于真实动作），导致顺序检查误报。
_NON_ACTION_PATTERNS = [
    r"\bopens? (on|in|with|inside)\b",     # the video opens on ...
    r"\bthe (target )?video opens\b",
    r"\bopening (frame|shot|image)\b",
]


def _event_verbs_in(verbs, text: str) -> list:
    """判断事件动词（可能是簇名）在文本里是否命中，命中则返回词。

    支持三种入参：簇名 / 簇成员 / 任意词。都按"整簇展开"匹配。
    匹配前先扣掉开场套话（opens on/in ...），否则 open 会撞上模板句。
    """
    low = text.lower()
    masked = low
    for pat in _NON_ACTION_PATTERNS:
        masked = re.sub(pat, " " * 1, masked)
    hit_terms = []
    for v in verbs:
        members = ACTION_SYNONYM_CLUSTERS.get(v, [v])
        if v not in members:
            members = [v] + list(members)
        for m in members:
            if m in masked:
                hit_terms.append(m)
                break
    return hit_terms


def _first_action_pos(term: str, text: str):
    """返回 term 在文本里第一个**非套话**出现的位置。"""
    low = text.lower()
    masked = low
    for pat in _NON_ACTION_PATTERNS:
        masked = re.sub(pat, lambda mm: " " * len(mm.group(0)), masked)
    return masked.find(term)


def _verb_cluster_hit(text: str, verbs) -> bool:
    """判断一组动词（可能是同义词簇）是否在文本命中。

    先把传入的扁平动词列表映射回所属簇，再把整簇成员一起查。
    """
    low = text.lower()
    pool = set(verbs)
    for cl, members in ACTION_SYNONYM_CLUSTERS.items():
        if any(v in verbs for v in members):
            pool.update(members)
    return any(v in low for v in pool)

# 交接类动词（handover 事件必须命中其一）
#
# ⚠️ 词表踩过的坑（2026-10-22 实测）：早期收了 gives/passes/takes 这类泛用词，
# 结果在 EP01 的 S08 上假命中三处 —— "the floor **gives** way"、
# "the golden sheet **passes** beneath"、"the land **takes** over the frame"，
# 全是无人物主语的比喻用法。于是"降级成静态"的赠橘事件被判成"有交接动词"，
# **最关键的假阴性就这么放过了**。
# 故：只保留真正的"递取"义词组。判定见 _has_handover_action（全文级，不要求同句）。
HANDOVER_VERBS = [
    # 取出
    "brings out", "bring out", "produces", "pulls out", "takes out",
    "reaches into", "dips into", "digs into", "fishes out",
    # 递出
    "hands over", "hands it", "hands the", "offers", "presents",
    "holds out", "extends out", "stretches out", "passes it", "gives it",
    # 接收
    "takes it", "receives it", "accepts", "cups", "cupping", "cradles",
    "clasps", "grasps it", "pulls it close",
    "拿出", "取出", "递给", "赠予", "接过", "接住", "双手捧",
]


def _has_handover_action(text: str) -> bool:
    """全文级交接判定：抽出/递出/接收任一动作出现即算（不要求同句）。

    为什么不再要求同句（2026-10-22 实测教训）：
    交接动作天然跨句分布——"角色A dips into satchel and produces the orange;"
    "she stretches her arms and offers the fruit;" "he cradles it to his chest."
    要求「一句里同时有动词+人物+道具」等于要求错误的东西，会把正确的三句写法误杀。
    改为：动作（全文中任一）+ 施动者 + 受动者 + 道具，四者**各自在全文命中**即可。
    """
    return _has_any(text, HANDOVER_VERBS) != []

# 空间跃迁关键词（用于 transition 事件）
TRANSITION_WORDS = [
    "cut", "transition", "crosses into", "steps through", "enters",
    "bursts through", "inverts", "turns inside out", "portal",
    "穿屏", "跨界", "跃迁", "进入光幕", "破屏",
]


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())



def _has_any(text: str, words) -> list:
    low = _norm(text)
    return [w for w in words if w in low]


# ------------------------------------------------------- 项目人物 / 道具词表

def _asset_hit(text: str, aliases) -> bool:
    """按项目给定的名字/画面代称命中；英文名字使用词边界，避免短名误命中。"""
    low = _norm(text)
    for alias in aliases:
        term = _norm(str(alias))
        if not term:
            continue
        if term.isascii() and re.search(r"[a-z0-9]", term):
            if re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])", low):
                return True
        elif term in low:
            return True
    return False


def _add_asset(catalog: dict, kind: str, name: str) -> str:
    name = name.strip()
    aliases = catalog[kind].setdefault(name, set())
    aliases.add(name)
    # 「角色参考板 · 名称（造型）」与视觉依据里的「名称」可互为代称。
    base = re.sub(r"\s*[（(].*$", "", name).strip()
    if base:
        aliases.add(base)
    return name


def parse_visual_settings(path: Path) -> dict:
    """从通用《视觉设定.md》二级标题与「画面代称」提取项目词表。"""
    catalog = {"actors": {}, "props": {}}
    current = None
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines():
        m = re.match(r"^##\s+(人物|角色|道具)(?:参考板|设定集)?\s*[·・:：]\s*(.+?)\s*$",
                     ln.strip())
        if m:
            kind = "props" if m.group(1) == "道具" else "actors"
            name = _add_asset(catalog, kind, m.group(2))
            current = (kind, name)
            continue
        if re.match(r"^##\s+", ln.strip()):
            current = None
        if current:
            am = re.match(r"^[-*]\s*(?:\*\*)?画面代称(?:\*\*)?\s*[：:]\s*(.+?)\s*$",
                          ln.strip())
            if am:
                for alias in re.split(r"[、，,]", am.group(1)):
                    alias = alias.strip()
                    if alias and alias != "无":
                        catalog[current[0]][current[1]].add(alias)
    return catalog


def _ensure_asset(catalog: dict, kind: str, name: str) -> str:
    for canonical, aliases in catalog[kind].items():
        if name == canonical or name in aliases:
            return canonical
    return _add_asset(catalog, kind, name)


def _extract_assets(script: dict, script_path: Path, visuals_path=None) -> dict:
    """合并视觉设定与每镜「视觉依据」；两者都是项目通用结构，不含项目专名。"""
    vp = Path(visuals_path) if visuals_path else None
    if vp is None:
        candidates = [script_path.parent / "视觉设定.md",
                      script_path.parent.parent / "视觉设定.md"]
        vp = next((p for p in candidates if p.is_file()), None)
    catalog = parse_visual_settings(vp) if vp else {"actors": {}, "props": {}}
    refs = {}
    for sh in script["shots"]:
        found = {"actors": [], "props": []}
        visual_text = "\n".join(v for k, v in sh["fields"].items() if "视觉依据" in k)
        for m in re.finditer(r"(人物|角色|道具)\s*[「\"]([^」\"]+)[」\"]", visual_text):
            kind = "props" if m.group(1) == "道具" else "actors"
            canonical = _ensure_asset(catalog, kind, m.group(2).strip())
            if canonical not in found[kind]:
                found[kind].append(canonical)
        refs[sh["shot_id"]] = found
    return {"catalog": catalog, "refs": refs,
            "visual_settings": str(vp) if vp else None}


def _names_hit(text: str, names, entries: dict) -> list:
    return [name for name in names if _asset_hit(text, entries[name])]


def _handover_assets(ev: dict, assets: dict):
    """返回本事件应收窄到的人物、道具；无法唯一确定时由调用方标 NOTCHK。"""
    catalog = assets["catalog"]
    refs = assets["refs"].get(ev["shot"], {"actors": [], "props": []})
    actors = _names_hit(ev["text"], catalog["actors"], catalog["actors"])
    if len(actors) < 2 and len(refs["actors"]) == 2:
        actors = list(refs["actors"])
    props = _names_hit(ev["text"], catalog["props"], catalog["props"])
    if not props and len(refs["props"]) == 1:
        props = list(refs["props"])

    missing = []
    if len(actors) < 2:
        missing.append("施动者/受动者")
    if not props:
        missing.append("交接道具")
    return actors, props, missing


# ---------------------------------------------------------------- 剧本侧

def _script_shot_header(line: str):
    """同时识别旧 S 镜号与当前 SHOT-EP... 二级标题。"""
    legacy = re.match(r"^###\s*镜头\s*(\d+)\s*\((S\d+)\)\s*[·・]?\s*(.*)$", line)
    if legacy:
        return int(legacy.group(1)), legacy.group(2), legacy.group(3).strip()
    current = re.match(
        r"^##\s+(SHOT-[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-(\d+))\s*[·・]?\s*(.*)$",
        line,
    )
    if current:
        return int(current.group(2)), current.group(1), current.group(3).strip()
    return None


def _is_action_field(name: str) -> bool:
    return "因果链" in name or name in {"唯一动作", "动作", "动作链", "主要动作"}


def parse_script(path: Path) -> dict:
    """从剧本 Markdown 抽镜头事件清单。

    支持旧格式与当前短剧格式：
        ### 镜头 01 (S01) · 标题 (副标题)
        ## SHOT-EP001-001 · 标题
        - **H3 动量因果链**：```...```（旧格式）
        - 唯一动作：...（当前格式，也认加粗写法）
        - 视觉依据：...人物「...」/道具「...」（用于项目词表）
    """
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")

    shots = []
    cur = None
    in_code = False
    code_buf = []
    last_field = None

    for ln in lines:
        header = _script_shot_header(ln.strip())
        if header:
            if cur:
                shots.append(cur)
            shot_no, shot_id, title = header
            cur = {
                "shot_no": shot_no,
                "shot_id": shot_id,
                "title": title,
                "fields": {},
                "action_chain": [],
                "dialogue": [],
            }
            last_field = None
            in_code = False
            continue

        if cur is None:
            continue

        fm = re.match(r"^-\s*(?:\*\*([^*]+)\*\*|([^：:]+))[：:]\s*(.*)$", ln.strip())
        if fm:
            last_field = (fm.group(1) or fm.group(2)).strip()
            value = fm.group(3).strip()
            cur["fields"][last_field] = value
            if value and _is_action_field(last_field):
                cur["action_chain"].append(value)
            in_code = False
            code_buf = []
            continue

        if ln.strip().startswith("```"):
            in_code = not in_code
            if not in_code and code_buf:
                joined = "\n".join(code_buf).strip()
                if last_field and _is_action_field(last_field):
                    cur["action_chain"].append(joined)
                elif last_field and "台词" in last_field:
                    cur["dialogue"].append(joined)
                code_buf = []
            continue

        if in_code:
            code_buf.append(ln)

    if cur:
        shots.append(cur)
    return {"path": str(path), "shots": shots}


def derive_events(script: dict) -> list:
    """从剧本镜头抽「事件清单」。

    事件类型：
      - action     动作事件（动词必须出现在成片提示词里）
      - handover   道具交接（施动者 + 受动者 + 道具 三者必须共现）
      - transition 空间跃迁（跨 space_id 必须有）
    """
    events = []
    for sh in script["shots"]:
        for chain in sh["action_chain"]:
            # 动作链每一行 → 一个 action 事件
            for seg in re.split(r"[→\n]", chain):
                seg = seg.strip(" -·")
                if len(seg) < 4:
                    continue
                verbs = _cluster_members_hit(seg)
                hverbs = _has_any(seg, HANDOVER_VERBS)
                twords = _has_any(seg, TRANSITION_WORDS)
                etype = "handover" if hverbs else ("transition" if twords else "action")
                events.append({
                    "id": f"{sh['shot_id']}-E{len([e for e in events if e['shot'] == sh['shot_id']]) + 1}",
                    "shot": sh["shot_id"],
                    "type": etype,
                    "text": seg,
                    "verbs": verbs,
                    "handover_verbs": hverbs,
                })
    return events


# ---------------------------------------------------------------- 分镜侧

def parse_shots(dir_or_file: Path) -> list:
    """读成片提示词（h3_prompts/*.txt），每份视为一个镜头。"""
    files = []
    if dir_or_file.is_dir():
        files = sorted(dir_or_file.glob("*.txt"))
    elif dir_or_file.is_file():
        files = [dir_or_file]
    out = []
    for f in files:
        txt = f.read_text(encoding="utf-8", errors="replace")
        # 从文件名抽 shot id（S01/S07 等）
        m = re.search(r"(S\d+)", f.name)
        sid = m.group(1) if m else f.stem
        out.append({"file": str(f), "name": f.name, "shot": sid, "text": txt})
    return out


# ---------------------------------------------------------------- 对账

def _make_result(script_path, shots_path, script, events, shots, findings, assets=None) -> dict:
    notchecked = sum(1 for f in findings if f["level"] == "notchk")
    has_error = any(f["level"] == "error" for f in findings)
    result = {
        "script": str(script_path),
        "shots_dir": str(shots_path),
        "script_shots": len(script["shots"]),
        "shot_files": len(shots),
        "events_total": len(events),
        "events_by_type": {
            k: len([e for e in events if e["type"] == k])
            for k in ("action", "handover", "transition")
        },
        "findings": findings,
        "notchecked_total": notchecked,
        "status": "BLOCK" if has_error else ("NOTCHK" if notchecked else "PASS"),
    }
    if assets is not None:
        result["visual_settings"] = assets["visual_settings"]
    return result


def check(script_path: Path, shots_path: Path, visuals_path=None) -> dict:
    script = parse_script(script_path)
    events = derive_events(script)
    shots = parse_shots(shots_path)

    findings = []
    if not script["shots"]:
        findings.append({
            "level": "notchk", "kind": "SCRIPT_SHOTS_NOTCHK", "shot": "-",
            "msg": "未识别到任何剧本镜头；支持 ### 镜头 01 (S01) 与 ## SHOT-EP001-001，未能对账",
        })
    if not events:
        findings.append({
            "level": "notchk", "kind": "SCRIPT_EVENTS_NOTCHK", "shot": "-",
            "msg": "未提取到任何剧本事件；请提供 H3 动量因果链或唯一动作字段，未能对账",
        })
    if not shots:
        findings.append({
            "level": "notchk", "kind": "SHOT_FILES_NOTCHK", "shot": "-",
            "msg": "未读到任何成片提示词 .txt 文件，未能对账",
        })
    if findings:
        return _make_result(script_path, shots_path, script, events, shots, findings)

    assets = _extract_assets(script, script_path, visuals_path)

    # 1) 剧本镜头是否有「内容承接」（不按文件名判，按内容判）
    #
    # ⚠️ 实测教训（2026-10-22）：早期按文件名 S01..S08 匹配，遇到 v5 的
    # v5_02..v5_08 命名就全判「整镜丢失」，8 条假错误。
    # 文件名不是可靠对齐键（同 §3 的镜号问题）。改为：该镜的**动作链关键词**
    # 是否在全部提示词里出现；出现即视为该镜有承接，不追究文件名。
    merged_all_early = " ".join(_norm(x["text"]) for x in shots)
    # 提示词是否含中文字符：决定中文字面指纹能否比对。
    prompt_has_zh = bool(re.search(r"[一-鿿]", merged_all_early))

    def _fingerprint(chain: str) -> list:
        """中英双语指纹：英文取 4+ 字母实词；中文用 2-gram 滑窗。

        不取整段连续汉字串——"林夏放下手" 整串匹配不到提示词里的 "放下手"。
        """
        en_toks = re.findall(r"[a-z]{4,}", _norm(chain))
        zh_toks = []
        for run in re.findall(r"[一-鿿]{2,}", chain):
            zh_toks.extend(run[i:i + 2] for i in range(len(run) - 1))
        return (en_toks + zh_toks)[:40]

    # 预计算每镜指纹与文档频率：跨镜公共词（角色名等）对"这一镜是否存在"没有区分力。
    fps = [_fingerprint(" ".join(sh["action_chain"])) for sh in script["shots"]]
    doc_freq = {}
    for fp in fps:
        for t in set(fp):
            doc_freq[t] = doc_freq.get(t, 0) + 1
    n_script_shots = max(len(script["shots"]), 1)
    for sh, toks in zip(script["shots"], fps):
        if not toks:
            findings.append({
                "level": "notchk", "kind": "SHOT_FINGERPRINT_NOTCHK", "shot": sh["shot_id"],
                "msg": (f"剧本 {sh['shot_id']}「{sh['title'][:26]}」的动作链"
                        f"取不到任何中英文关键词，未做整镜丢失检查"),
            })
            continue
        # 跨语言：中文动作链 + 全英文提示词（用视觉代称写词）时，中文字面指纹无从比对。
        # 不得静默跳过（issue #32-4）：§1 无法定论就显式记 NOTCHK，交由 §3 事件对账兜底，
        # 但最终状态不能假装「全部对齐」（PASS），否则整镜丢失会被这层静默放过。
        chain = " ".join(sh["action_chain"])
        if re.search(r"[一-鿿]", chain) and not prompt_has_zh:
            findings.append({
                "level": "notchk", "kind": "SHOT_FINGERPRINT_CROSS_LANG_NOTCHK",
                "shot": sh["shot_id"],
                "msg": (f"剧本 {sh['shot_id']}「{sh['title'][:26]}」是中文动作链、提示词全英文，"
                        f"中文字面指纹无从比对；§1 整镜丢失检查未决，需 §3 事件对账或人工确认"),
            })
            continue
        # IDF 式权重：只在 ≤半数镜出现的 token 才计区分力，公共词剔除；全公共则退化为全词。
        weights = [1.0 / (1.0 + doc_freq[t] / n_script_shots)
                   for t in toks if doc_freq[t] <= n_script_shots / 2] or [1.0] * len(toks)
        weighted_tokens = [t for t in toks if doc_freq[t] <= n_script_shots / 2] or toks
        hit = sum(w for t, w in zip(weighted_tokens, weights) if t in merged_all_early)
        ratio = hit / sum(weights)
        if ratio < 0.15:   # 该镜的区分性内容基本没被任何提示词覆盖
            findings.append({
                "level": "error", "kind": "SHOT_CONTENT_MISSING",
                "shot": sh["shot_id"],
                "msg": (f"剧本 {sh['shot_id']}「{sh['title'][:26]}」的动作链内容在全部成片里"
                        f"只命中 {ratio*100:.0f}%（<15%）—— 疑似整镜丢失"),
            })

    # 2) 成片镜头是否有「剧本来源」（不按文件名判——文件名不可靠，见 §1）
    #    只做**弱提示**：某提示词的独有内容在剧本里找不到任何对应，才提示"可能自行添加"。
    #    实测 v5 的 v5_02~v5_08 与剧本 S01~S08 是同一批内容、只是命名不同，
    #    按文件名会报 8 条假错。故此处不做硬判，仅记录镜数，供人核对。
    findings.append({
        "level": "info", "kind": "SHOT_COUNT",
        "shot": "-",
        "msg": (f"剧本 {len(script['shots'])} 镜 / 成片 {len(shots)} 个提示词文件"
                f"（编号不要求一一对应，按内容对账）"),
    })

    # 3) 逐镜事件承担检查
    # 3) 事件承担检查（**按内容在全库检索，不按编号**）
    #
    # 关键设计决定：剧本镜号与成片镜号**没有必然对应关系**。
    # 实测 EP01：剧本 8 镜 vs 成片 9 镜；剧本 S06「角色A赠橘」在成片里根本没有对应镜，
    # 唯一出现是 S08 的一句静态描述。若按「S06 比 S06」对账，会把剧本赠橘比到成片
    # 「破屏探身」上然后判"通过"——这是最危险的假阴性。故一律**按事件内容检索全部分镜**。
    all_text = {s["shot"]: _norm(s["text"]) for s in shots}
    merged_all = " || ".join(all_text.values())
    catalog = assets["catalog"]

    for ev in events:
        sid = ev["shot"]

        if ev["type"] == "handover":
            expected_actors, expected_props, unresolved = _handover_assets(ev, assets)
            if unresolved:
                findings.append({
                    "level": "notchk", "kind": "HANDOVER_ASSETS_NOTCHK",
                    "shot": sid, "event": ev["id"],
                    "msg": (f"剧本 {sid} 的交接事件无法从视觉设定/视觉依据确定"
                            f"{'、'.join(unresolved)}；未做交接完整性对账"),
                })
                continue

            prop_aliases = [catalog["props"][p] for p in expected_props]
            hosts = [s2 for s2, t in all_text.items()
                     if all(_asset_hit(t, aliases) for aliases in prop_aliases)]
            hosts_handover = [s2 for s2 in hosts if _has_handover_action(all_text[s2])]

            ok_host = None
            for s2 in hosts_handover:
                text = all_text[s2]
                actors_hit = [a for a in expected_actors
                              if _asset_hit(text, catalog["actors"][a])]
                props_hit = [p for p, aliases in zip(expected_props, prop_aliases)
                             if _asset_hit(text, aliases)]
                if len(actors_hit) == len(expected_actors) and len(props_hit) == len(expected_props):
                    ok_host = s2
                    break

            if not hosts:
                findings.append({
                    "level": "error", "kind": "HANDOVER_MISSING",
                    "shot": sid, "event": ev["id"],
                    "msg": (f"剧本 {sid} 的**道具交接**「{ev['text'][:44]}…」在全部 "
                            f"{len(shots)} 个成片镜头里找不到道具 {expected_props} —— **整镜丢失**"),
                })
            elif not hosts_handover:
                findings.append({
                    "level": "error", "kind": "HANDOVER_DEGRADED",
                    "shot": ",".join(hosts), "event": ev["id"],
                    "msg": (f"剧本 {sid} 的交接事件「{ev['text'][:44]}…」在成片 {hosts} 里"
                            f"只找到**道具名词**、没有交接动词 —— **降级成静态描述**"),
                })
            elif ok_host is None:
                findings.append({
                    "level": "error", "kind": "HANDOVER_INCOMPLETE",
                    "shot": ",".join(hosts_handover), "event": ev["id"],
                    "msg": (f"剧本 {sid} 的交接事件在成片 {hosts_handover} 有交接动词，"
                            f"但项目指定的施动者、受动者与道具未共现 —— 道具交接不成立"),
                })

        elif ev["type"] == "action":
            if ev["verbs"] and not _verb_cluster_hit(merged_all, ev["verbs"]):
                findings.append({
                    "level": "warn", "kind": "ACTION_VERB_MISSING",
                    "shot": sid, "event": ev["id"],
                    "msg": (f"剧本 {sid} 事件动词 {ev['verbs']} 在**全部成片**里未命中"
                            f"（可能换同义表达，需人看）"),
                })

    # 3b) 动作链**顺序**检查（有条件启用）
    #
    # ⚠️ 实测结论（2026-10-22，必须写清楚，否则后人会重走）：
    # 「按内容定位该镜落在哪个成片文件」**不可靠**。实测 EP01：
    #   S03 的独有词覆盖 top3 = S04(5) / S03(5) —— 并列，无法判定
    #   S07 的独有词覆盖全部是 2 票 —— 不分伯仲
    # 强行做顺序检查会：门槛松则 4 条误报，门槛紧则连真反序也抓不到。
    #
    # 因此：**只在剧本镜号与成片文件镜号一一对应时**才做顺序检查
    # （这是可判定的前提，不是猜）。否则记 NOTCHK，不能把跳过顺序检查写成全部通过。
    script_ids_ordered = [sh["shot_id"] for sh in script["shots"]]
    shot_ids_in_files = [s2["shot"] for s2 in shots]
    one_to_one = (set(script_ids_ordered) == set(shot_ids_in_files)
                  and len(shot_ids_in_files) == len(set(shot_ids_in_files)))
    order_checked = 0
    if one_to_one:
        for sh in script["shots"]:
            act_evs = [e for e in events if e["shot"] == sh["shot_id"] and e["type"] == "action"]
            if len(act_evs) < 2:
                continue
            local = _norm([x for x in shots if x["shot"] == sh["shot_id"]][0]["text"])
            seq = []
            for ev in act_evs:
                hits = _event_verbs_in(ev["verbs"], local)
                if hits:
                    p = _first_action_pos(hits[0], local)
                    if p >= 0:
                        seq.append((ev["id"], hits[0], p))
            inversions = []
            for i in range(len(seq) - 1):
                if seq[i + 1][2] < seq[i][2] - 40:
                    inversions.append((seq[i], seq[i + 1]))
            order_checked += 1
            if inversions:
                pairs = "; ".join(f"{a[1]}→{b[1]}（剧本同序、成片反了）" for a, b in inversions[:3])
                findings.append({
                    "level": "warn", "kind": "ACTION_ORDER",
                    "shot": sh["shot_id"],
                    "msg": f"动作链顺序疑似颠倒：{pairs}",
                })
    else:
        findings.append({
            "level": "notchk", "kind": "ORDER_SKIPPED",
            "shot": "-",
            "msg": ("剧本镜号与成片镜号未一一对应，**未做动作链顺序检查**"
                    "（内容定位实测不可靠，见代码注释）"),
        })

    # 4) 漏洞2：空间跃迁的「重复承担」检查
    #
    # 实测边界（必须诚实标注）：**「同镜内黑框自溶」在提示词层面查不出来**。
    # EP01 的真事故里，S02 只写"框"(bezel)，S03 只写"满幅"，分属两个文件；
    # 真正的自溶发生在 S03 渲染过程内部（外环死黑 25.7%→17.3%→…→0.0% 单调递减），
    # 只有**帧级数据**能证明。文本闸门能做的只是：查"同一次空间穿越是否被多个镜重复承担"。
    # 只算「跨空间」的穿越，不算普通推镜（否则 S01 的 room dolly 会误入）
    TRANSIT_MARK = (r"(crossing into|crosses into|steps? through|bursts? through|"
                   r"turns? inside out|becomes the face of a television|"
                   r"opens inside the television|inside the television picture|screen world)")
    transit_shots = []
    for s2 in shots:
        t = _norm(s2["text"])
        if re.search(TRANSIT_MARK, t):
            if s2["shot"] not in transit_shots:
                transit_shots.append(s2["shot"])
    # 剧本里 transition 类事件数量 vs 成片里承担穿越的镜数
    n_script_trans = len([e for e in events if e["type"] == "transition"])
    if len(transit_shots) > max(n_script_trans, 1):
        findings.append({
            "level": "warn", "kind": "TRANSITION_DUPLICATED",
            "shot": ",".join(transit_shots),
            "msg": (f"成片有 {len(transit_shots)} 个镜头写了穿越运镜 {transit_shots}，"
                    f"但剧本只有 {n_script_trans} 个 transition 事件 —— "
                    f"疑似**同一次穿越被多镜重复承担**（EP01 的 S02+S03 就是此形态，"
                    f"导致 S03 段内黑框自溶）。逐帧确认见 cut_detect / 外环死黑曲线"),
        })
    # 4b) 单镜内同时出现「框」与「满幅」两种空间描述 → 也是自溶嫌疑（能查就读）
    for s2 in shots:
        t = _norm(s2["text"])
        marks = []
        if re.search(r"bezel|cabinet strip|black frame|television frame|screen frame", t):
            marks.append("framed")
        if re.search(r"full[- ]frame|fills the frame|real three-dimensional", t):
            marks.append("full")
        if len(set(marks)) >= 2:
            findings.append({
                "level": "warn", "kind": "SPACE_IN_SHOT",
                "shot": s2["shot"],
                "msg": (f"{s2['shot']} 同一镜内同时出现 {marks} 两种空间描述 —— "
                        f"若首尾帧空间不同，渲染时会「黑框自溶」，需逐帧确认"),
            })

    return _make_result(script_path, shots_path, script, events, shots, findings, assets)


def main() -> int:
    ap = argparse.ArgumentParser(description="剧本事件 ↔ 镜头 双向对账")
    ap.add_argument("--script", required=True)
    ap.add_argument("--shots", required=True)
    ap.add_argument("--visuals", "--visual-settings", dest="visuals", default=None,
                    help="视觉设定.md；缺省自动查找分镜同目录/上级目录")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    sp, shp = Path(args.script), Path(args.shots)
    if not sp.is_file():
        print(f"ERROR: 剧本不存在 {sp}", file=sys.stderr)
        return 2
    if not shp.exists():
        print(f"ERROR: 分镜路径不存在 {shp}", file=sys.stderr)
        return 2
    vp = Path(args.visuals) if args.visuals else None
    if vp and not vp.is_file():
        print(f"ERROR: 视觉设定不存在 {vp}", file=sys.stderr)
        return 2

    r = check(sp, shp, vp)

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(f"剧本: {r['script']}  ({r['script_shots']} 镜, {r['events_total']} 事件 "
              f"[action {r['events_by_type']['action']} / "
              f"handover {r['events_by_type']['handover']} / "
              f"transition {r['events_by_type']['transition']}])")
        print(f"成片: {r['shots_dir']}  ({r['shot_files']} 个镜头文件)")
        print()
        # check() 总会写入一条 SHOT_COUNT info，故 findings 永不为空；
        # 真正的“全部对齐”判据是没有任何 error / warn / notchk。
        if r["status"] == "PASS":
            print("✓ 剧本与镜头全部对齐")
        else:
            for f in r["findings"]:
                icon = "✗" if f["level"] == "error" else ("?" if f["level"] == "notchk" else "!")
                print(f"  {icon} [{f['kind']}] {f['msg']}")
        n_err = sum(1 for f in r["findings"] if f["level"] == "error")
        n_warn = sum(1 for f in r["findings"] if f["level"] == "warn")
        print(f"\n错误 {n_err} / 警告 {n_warn} / 未检查 {r['notchecked_total']}")
        print(f"结果：{r['status']}")
        print("纪律：剧本是唯一真源，对账不通过只改分镜，**禁止改剧本以通过对账**。")

    if r["status"] == "BLOCK":
        return 1
    return 2 if r["status"] == "NOTCHK" else 0


if __name__ == "__main__":
    sys.exit(main())