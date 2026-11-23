#!/usr/bin/env python3
"""storyboard-30s 分镜表闸门：交稿前的机械检查。

用法:
    python3 storyboard_gate.py <分镜文件.md> [--skill <技能目录或 SKILL.md>]

为什么要有这个脚本：分镜表的翻车方式与单帧提示词同构——"承认该填的栏，然后跳过"。
文字要求可以被自述绕过，退出码不行。**这是交稿硬闸：退出码 0 才允许交稿，任一 FAIL 都必须改到 0 再交。**

校验项（只覆盖能机械判定的结构与字数，与 SKILL.md 硬规则同源但不包含主观表演项）：
  1. 片头四项：【场景】【角色】【道具】【节拍】齐不齐（【改编来源】可选）；
  2. 逐镜表：镜N + 时间区间写法合法，区间首尾相接、无重叠无空隙，
     累计满【节拍】声明的总时长；镜数与【节拍】中的显式声明一致（不设默认镜数配额）；
  3. 每镜景别、运镜取自词库逐字（允许"运镜｜起幅…｜落幅…｜动机…"或"运镜，从景别A至景别B"组合）；
     若用 ｜ 分隔，必须同时写出起幅、落幅与动机三段；
  4. 每镜台词字数上限按公式 `字数 ≤ int((镜长秒 - 0.5) × 4.1)`（与 h3-video-gate G18 同口径）：
     2s→6 字 / 3s→10 字 / 4s→14 字 / 5s→18 字 / 7s→26 字 / 10s→38 字；
  5. 「分镜总表」节存在，六列齐全（镜/职责/台词/道具进出/生成方式/跨镜连续物），
     每个镜号已登记，道具进出格式 名（进场镜→退场镜），生成方式取值合法；
  6. 「切点契约表」「生成单元表」「连续性账」三节齐全，字段无空栏，生成单元覆盖全部镜号，
     切点连接方式必须是视线/声音/动作/反应接之一；
  7. 自检清单逐条 yes/no/NA（条目号从 SKILL.md 动态解析）：判 no 直接 FAIL，
     NA 必须给理由/证据。自检里的 dB 数值、音频四段内容、光影动机等主观项本脚本不判，
     由人按 SKILL 自检 16/17/27 逐条核对；"与自检一同源"指条目号与是否作答，不指替人判主观项。
"""
import io
import os
import re
import sys

# 景别 / 运镜词库（与 references/shot-vocabulary.md 逐字一致；改动必须两边同步）
SHOT_SIZES = ["大特写", "特写", "近景", "中近景", "中景", "中全景", "全景", "远景"]
MOVES = ["固定机位（带轻微自然呼吸抖动）", "固定机位", "缓慢匀速向前推进", "缓慢匀速向后拉开",
         "水平左右横移", "垂直上下摇摄", "水平摇摄", "升降", "360° 缓慢环绕镜头", "斯坦尼康跟拍",
         "手持跟拍"]
GEN_WAYS = ("文生图", "首帧图生视频", "参考图定向", "不动图", "—", "无", "")
SUMMARY_COLUMNS = ["镜", "职责", "台词", "道具进出", "生成方式", "跨镜连续物"]
PROP_MOVE_RE = re.compile(r"[^（）()]+[（(][^（）()]*→[^（）()]*[）)]")
CJK = re.compile(r"[一-鿿]")

NUM = r"(\d+(?:\.\d+)?)"
SHOT_RE = re.compile(r"^镜\s*(\d+)\s+" + NUM + r"\s*[-–~～]\s*" + NUM + r"\s*秒")
CHARS_PER_SECOND = 4.1   # 与 h3-video-gate G18 同口径
EPS = 1e-6


def read(path):
    return io.open(path, encoding="utf-8").read()


def parse_header(text, problems):
    """片头四项 + 节拍声明。返回 (总时长秒, 声明镜数或 None)。"""
    total, declared = None, None
    for label in ("场景", "角色", "道具", "节拍"):
        if not re.search(r"^【%s】\s*\S" % label, text, re.M):
            problems.append("片头缺【%s】（或冒号后为空）——四项齐是硬规则" % label)
    m = re.search(r"^【节拍】\s*(.+)$", text, re.M)
    if m:
        body = m.group(1)
        mt = re.search(r"(\d+(?:\.\d+)?)\s*[sS秒]", body)
        if mt:
            total = float(mt.group(1))
        else:
            problems.append("【节拍】里读不出总时长（要写 30s·11镜·… 这种带秒数的）")
        mn = re.search(r"(\d+)\s*镜", body)
        if mn:
            declared = int(mn.group(1))
    return total or 30, declared


def parse_shots(text, problems):
    """逐镜块 -> [(镜号, 起秒, 止秒, 块文本)]。"""
    lines = text.splitlines()
    shots = []
    for i, line in enumerate(lines):
        m = SHOT_RE.match(line.strip())
        if not m:
            continue
        end = len(lines)
        for j in range(i + 1, len(lines)):
            if SHOT_RE.match(lines[j].strip()):
                end = j
                break
        shots.append((int(m.group(1)), float(m.group(2)), float(m.group(3)),
                      "\n".join(lines[i:end])))
    return shots


def field(block, name):
    m = re.search(r"^%s[:：]\s*(.+)$" % name, block, re.M)
    return m.group(1).strip() if m else None


def check_shots(shots, total, declared, problems):
    if not shots:
        problems.append("一个镜都没有（要 镜N  时间区间 起手的逐镜块）")
        return
    nums = [s[0] for s in shots]
    if nums != list(range(1, len(nums) + 1)):
        problems.append("镜号必须从 1 连续编号到 N（实得：%s）" % nums)
    expect = declared
    if expect is not None and len(shots) != expect:
        problems.append("镜数 %d 与【节拍】声明的 %d 镜不一致" % (len(shots), expect))
    # 时间区间：首尾相接、无重叠、满总时长
    prev_end, spans = 0, []
    for n, a, b, block in shots:
        if abs(a - prev_end) > EPS:
            problems.append("镜%d 区间 %g-%g 秒没有接在上一镜结尾 %g 秒上（首尾相接是硬规则）"
                            % (n, a, b, prev_end))
        if b <= a:
            problems.append("镜%d 区间 %g-%g 秒不是正长度" % (n, a, b))
        spans.append((n, a, b, block))
        prev_end = b
    if abs(prev_end - total) > EPS:
        problems.append("时间区间累计 %g 秒，【节拍】声明总时长 %g 秒（%g≠%g）"
                        % (prev_end, total, prev_end, total))
    # 每镜字段
    for n, a, b, block in spans:
        dur = b - a
        size = field(block, "景别")
        if not size:
            problems.append("镜%d 缺「景别：」栏" % n)
        else:
            head = re.split(r"[，,｜|]", size)[0].strip()
            if head not in SHOT_SIZES:
                problems.append("镜%d 景别「%s」不在景别词库（%s）" % (n, head, "/".join(SHOT_SIZES)))
        move = field(block, "运镜")
        if not move:
            problems.append("镜%d 缺「运镜：」栏" % n)
        else:
            first = re.split(r"[，,｜|]", move)[0].strip()
            if first not in MOVES:
                problems.append("镜%d 运镜「%s」不在运镜词库（%s）" % (n, first, "/".join(MOVES)))
            # ｜ 分隔写法必须写全「起幅→落幅→动机」三段；只写词库词不算设计（SKILL 运镜硬规则 1）
            if "｜" in move or "|" in move:
                missing = [k for k in ("起幅", "落幅", "动机") if k not in move]
                if missing:
                    problems.append("镜%d 运镜用了 ｜ 分隔却缺 %s（要求：词库词｜起幅…｜落幅…｜动机…）"
                                    % (n, "、".join(missing)))
        line = field(block, "台词")
        if line is None:
            problems.append("镜%d 缺「台词：」栏（无台词也要写 无）" % n)
        else:
            chars = len(CJK.findall(line))
            # 与 G18 同口径：字数 ÷ 4.1 + 0.5 秒反应余量 不超过镜长
            cap = max(0, int((dur - 0.5) * CHARS_PER_SECOND))
            if chars > cap:
                problems.append("镜%d 台词 %d 字超出 %g 秒镜的上限 %d 字（按 %.1f 字/秒 + 0.5 秒余量；%s…）"
                                % (n, chars, dur, cap, CHARS_PER_SECOND, line[:20]))


def check_summary(text, shots, problems):
    """分镜总表节：六列、镜号登记、道具进出、生成方式。"""
    m = re.search(r"^#{1,6}.*分镜总表.*$", text, re.M)
    if not m:
        problems.append("缺「分镜总表」节（与 doc-still-prompt 共用的六列契约，没有它写词没有依据）")
        return
    block = text[m.end():]
    nxt = re.search(r"^#{1,6}", block, re.M)
    if nxt:
        block = block[:nxt.start()]
    rows = [l for l in block.splitlines() if l.strip().startswith("|")
            and not re.match(r"^\s*\|[\s\-:|]+\|\s*$", l)]
    if not rows:
        problems.append("分镜总表是空的（要一张六列表格）")
        return
    header = [c.strip() for c in rows[0].strip().strip("|").split("|")]
    for col in SUMMARY_COLUMNS:
        if col not in header:
            problems.append("分镜总表列头缺「%s」（固定六列：%s）"
                            % (col, " / ".join(SUMMARY_COLUMNS)))
    idx = {c: header.index(c) for c in SUMMARY_COLUMNS if c in header}
    registered = set()
    for r in rows[1:]:
        cells = [c.strip() for c in r.strip().strip("|").split("|")]
        if not cells or not re.match(r"^(镜)?\d+$", cells[0].replace("S", "").replace("镜", "")):
            continue
        registered.add(re.sub(r"^(镜|S|s)", "", cells[0]))
        if "道具进出" in idx and idx["道具进出"] < len(cells):
            pm = cells[idx["道具进出"]]
            if pm and pm not in ("—", "-", "无"):
                rest = PROP_MOVE_RE.sub("", pm)
                if rest.strip("、，,;； \t"):
                    problems.append("总表道具进出格式不合规：「%s」要求 名（进场镜→退场镜）" % pm)
        if "生成方式" in idx and idx["生成方式"] < len(cells):
            gw = cells[idx["生成方式"]]
            if gw not in GEN_WAYS:
                problems.append("总表生成方式取值非法：「%s」（合法值：文生图 / 首帧图生视频 / 参考图定向 / 不动图）" % gw)
    for n, _a, _b, _blk in shots:
        if str(n) not in registered:
            problems.append("分镜总表没有登记镜%d（逐镜表里的每一镜都要进总表）" % n)


def section_block(text, heading):
    m = re.search(r"^#{1,6}.*%s.*$" % re.escape(heading), text, re.M)
    if not m:
        return None
    block = text[m.end():]
    nxt = re.search(r"^#{1,6}", block, re.M)
    return block[:nxt.start()] if nxt else block


def table_rows(block):
    return [l for l in block.splitlines() if l.strip().startswith("|")
            and not re.match(r"^\s*\|[\s\-:|]+\|\s*$", l)]


def cells_of(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def empty_cell(value):
    return value.strip() in ("", "—", "-", "待定", "TBD", "tbd")


def check_continuity_tables(text, shots, problems):
    """切点契约表、生成单元表、连续性账：三表必须存在、字段齐全、无空栏、覆盖全镜。"""
    shot_numbers = [str(n) for n, _a, _b, _blk in shots]
    specs = [
        ("切点契约表", ["切点", "前镜末状态", "后镜起状态", "连接方式", "新增信息", "不切的后果"]),
        ("生成单元表", ["生成单元", "包含剪辑镜", "生成模式", "参考方式", "单元起止状态", "接缝验证"]),
        ("连续性账", ["主体", "身份视图", "服装/持物", "屏幕方向", "主光源/边界陈设", "起状态", "止状态"]),
    ]
    for heading, required in specs:
        block = section_block(text, heading)
        if block is None:
            problems.append("缺「%s」节（连续性为硬规则，不因片长或单场景豁免）" % heading)
            continue
        rows = table_rows(block)
        if len(rows) < 2:
            if heading == "切点契约表" and len(shots) <= 1:
                if not rows:
                    problems.append("「%s」缺表头；单镜也要保留表头并写「无跨镜切点」" % heading)
                continue
            problems.append("「%s」没有数据行（表头之外至少一条）" % heading)
            continue
        header = cells_of(rows[0])
        for col in required:
            if col not in header:
                problems.append("「%s」缺列「%s」（要求：%s）" % (heading, col, " / ".join(required)))
        idx = {c: header.index(c) for c in required if c in header}
        seen_cuts, covered = set(), set()
        for row in rows[1:]:
            cells = cells_of(row)
            for col, i in idx.items():
                if i >= len(cells) or empty_cell(cells[i]):
                    problems.append("「%s」存在空栏：%s（行：%s）" % (heading, col, row[:80]))
            if heading == "切点契约表" and "切点" in idx and idx["切点"] < len(cells):
                cut = cells[idx["切点"]]
                if cut in seen_cuts:
                    problems.append("切点契约表重复登记切点「%s」" % cut)
                seen_cuts.add(cut)
                if cut in ("无", "—", "-"):
                    continue
                if "连接方式" in idx and idx["连接方式"] < len(cells):
                    link = cells[idx["连接方式"]]
                    if not any(k in link for k in ("视线", "声音", "动作", "反应")):
                        problems.append("切点「%s」连接方式必须是 视线接/声音接/动作接/反应接 之一（实得：%s）"
                                        % (cut, link))
            if heading == "生成单元表" and "包含剪辑镜" in idx and idx["包含剪辑镜"] < len(cells):
                covered.update(re.findall(r"\d+", cells[idx["包含剪辑镜"]]))
        if heading == "生成单元表" and covered:
            missing = [n for n in shot_numbers if n not in covered]
            if missing:
                problems.append("生成单元表没有覆盖全部剪辑镜，缺：%s" % ", ".join(missing))
            if len(rows) - 1 < 2:
                # 单生成单元是合法结构；只有多镜才要求接缝行
                pass


def checklist_ids(md_text):
    ids, seen = [], set()
    in_cl = False
    for line in md_text.splitlines():
        if re.match(r"^#{1,6}.*自检清单", line):
            in_cl = True
            continue
        if in_cl and re.match(r"^#{1,6}", line):
            break
        if not in_cl:
            continue
        m = re.match(r"^\|\s*(\d+)\s*\|", line)
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            ids.append(m.group(1))
    return ids


def check_acceptance(text, skill_path, problems):
    if not skill_path or not os.path.exists(skill_path):
        problems.append("找不到 SKILL.md，无法校验自检清单（用 --skill 指定技能目录）")
        return
    ids = checklist_ids(read(skill_path))
    if not ids:
        problems.append("闸门无法从 SKILL.md 解析出自检清单条目号，不许当作通过")
        return
    m = re.search(r"^#{1,6}.*自检.*$", text, re.M)
    block = text[m.end():] if m else ""
    nxt = re.search(r"^#{1,6}", block, re.M)
    if nxt:
        block = block[:nxt.start()]
    answered = set()
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 3 or not re.match(r"^\d+$", cells[0]):
            continue
        answered.add(cells[0])
        # 列序固定：第 0 列编号 / 第 1 列检查项文本 / 最后一列才是答案。
        # 旧实现把第 1 列（检查项文本）当答案列，文本里出现 "no…" 就会误报。
        answer = cells[-1].strip()
        low = answer.lower()
        if low == "no" or low.startswith("no ") or low in ("否", "n"):
            problems.append("自检第 %s 条判 no —— 任何一条 no 都必须改到 yes 再交" % cells[0])
        elif low.startswith("na") or low.startswith("n/a"):
            rest = re.sub(r"^n/?a\s*", "", answer, flags=re.I).strip()
            extra = " ".join(cells[3:]) if len(cells) > 3 else ""
            why = (rest + " " + extra).strip()
            if len(why) < 8 and "`" not in why:
                problems.append("自检第 %s 条判 NA 却没给理由或证据" % cells[0])
    missing = [i for i in ids if i not in answered]
    if missing:
        problems.append("自检漏答 %d 条：%s（不适用的也要写 NA＋理由）"
                        % (len(missing), ", ".join(missing[:20])))


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    path = argv[0]
    skill_arg = argv[argv.index("--skill") + 1] if "--skill" in argv else None
    if not os.path.exists(path):
        print("FAIL  分镜文件不存在：%s" % path)
        return 1
    skill_path = os.path.join(skill_arg, "SKILL.md") if skill_arg and os.path.isdir(skill_arg) else skill_arg
    if not skill_path or not os.path.exists(skill_path):
        cand = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md")
        skill_path = cand if os.path.exists(cand) else None

    text = read(path)
    problems = []
    total, declared = parse_header(text, problems)
    shots = parse_shots(text, problems)
    check_shots(shots, total, declared, problems)
    check_summary(text, shots, problems)
    check_continuity_tables(text, shots, problems)
    check_acceptance(text, skill_path, problems)

    print("== %s ==" % os.path.basename(path))
    for p in problems:
        print("FAIL  " + p)
    if problems:
        print("\n共 %d 个 FAIL：闸门未过，这份分镜表不许交稿。" % len(problems))
        return 1
    print("PASS  片头齐、区间相接满时长、镜数合规、景别运镜逐字、台词字数达标、总表六列齐、切点/生成单元/连续性账齐全、自检无漏答。允许交稿。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
