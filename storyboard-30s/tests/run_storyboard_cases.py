#!/usr/bin/env python3
"""storyboard_gate.py 的回归用例：改闸门脚本或 SKILL.md 自检清单后必须跑这个。

用法: python3 tests/run_storyboard_cases.py

断言的是退出码：pass 类期望 0，fail 类期望非 0。
"""
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(os.path.dirname(HERE), "scripts", "storyboard_gate.py")
SKILL = os.path.dirname(HERE)

SIZES = ["近景", "特写", "中景", "中全景", "近景", "特写", "中景", "中全景", "近景", "远景"]
MOVES = ["固定机位（带轻微自然呼吸抖动）", "缓慢匀速向前推进", "固定机位（带轻微自然呼吸抖动）",
         "水平左右横移", "斯坦尼康跟拍", "缓慢匀速向前推进", "固定机位（带轻微自然呼吸抖动）",
         "缓慢匀速向后拉开", "斯坦尼康跟拍", "缓慢匀速向后拉开"]
LINES = ["你来了。", "无", "我等了三天。", "无", "指尖在抖。", "为什么现在说？",
         "无", "因为我不敢。", "无", "无"]


def shot_block(n, a, b, size=None, move=None, line=None):
    return "\n".join([
        "镜%d  %d-%d秒" % (n, a, b),
        "景别：%s" % (size or SIZES[n - 1]),
        "运镜：%s" % (move or MOVES[n - 1]),
        "画面内容：她把碗放下，抬眼，停顿半拍。",
        "台词：%s" % (line if line is not None else LINES[n - 1]),
        "特效 / 音效：无",
        "分镜光影：窗光从左前方 45° 入射，阴影羽化。",
        "",
    ])


def good_doc(total=30, nshots=10, beat=None, summary=True, acceptance=True,
             tables=True, sizes=None, moves=None, lines=None):
    if beat is None:
        beat = "%ds·%d镜·渐快收尾" % (total, nshots)
    parts = ["# 测试片段", "",
             "【场景】老厨房", "【角色】阿禾", "【道具】白瓷碗（镜1→镜10）",
             "【节拍】%s" % beat, "",
             "## 片头与逐镜表", ""]
    durs = [3, 2, 3, 3, 2, 3, 3, 3, 4, 4][:nshots]
    scale = total / sum(durs)
    durs = [max(1, round(d * scale)) for d in durs]
    durs[-1] += total - sum(durs)
    a = 0
    for n in range(1, nshots + 1):
        b = a + durs[n - 1]
        parts.append(shot_block(n, a, b,
                                size=(sizes[n - 1] if sizes else None),
                                move=(moves[n - 1] if moves else None),
                                line=(lines[n - 1] if lines else None)))
        a = b
    if summary:
        rows = ["| 镜 | 职责 | 台词 | 道具进出 | 生成方式 | 跨镜连续物 |",
                "|---|---|---|---|---|---|"]
        for n in range(1, nshots + 1):
            rows.append("| %d | 关系推进 | %s | 白瓷碗（%d→%d） | 文生图 | 白瓷碗 |"
                        % (n, LINES[n - 1] if n - 1 < len(LINES) else "无", 1, nshots))
        parts += ["## 分镜总表", ""] + rows + [""]
    if tables:
        cuts = ["| 切点 | 前镜末状态 | 后镜起状态 | 连接方式 | 新增信息 | 不切的后果 |",
                "|---|---|---|---|---|---|"]
        for n in range(1, nshots):
            cuts.append("| S%d→S%d | 前一拍动作完成 | 下一拍从接触处继续 | 动作接 | 观众读到新反应 | 动作重复或断裂 |"
                        % (n, n + 1))
        if nshots == 1:
            cuts.append("| 无 | 无跨镜切点 | 无跨镜切点 | 动作接 | 单镜连续表演 | 不适用 |")
        units = ["| 生成单元 | 包含剪辑镜 | 生成模式 | 参考方式 | 单元起止状态 | 接缝验证 |",
                 "|---|---|---|---|---|---|",
                 "| G1 | %s | 单镜连续生成 | 角色板 + 场景板 | 起：坐下；止：放下碗 | 与相邻单元动作相位并排 |"
                 % "、".join(str(n) for n in range(1, nshots + 1))]
        continuity = ["| 主体 | 身份视图 | 服装/持物 | 屏幕方向 | 主光源/边界陈设 | 起状态 | 止状态 |",
                      "|---|---|---|---|---|---|---|",
                      "| 阿禾 | 登记视图 | 围裙；右手端碗 | 面向画面右 | 左窗日光；木桌 | 站立 | 坐下放碗 |"]
        parts += ["## 切点契约表", ""] + cuts + [""]
        parts += ["## 生成单元表", ""] + units + [""]
        parts += ["## 连续性账", ""] + continuity + [""]
    if acceptance:
        ids = parse_ids()
        rows = ["| # | 检查项 | 结论 |", "|---|---|---|"]
        for cid in ids:
            rows.append("| %s | 条目 | yes |" % cid)
        parts += ["## 自检", ""] + rows + [""]
    return "\n".join(parts)


def parse_ids():
    import re
    ids, in_cl = [], False
    for line in io.open(os.path.join(SKILL, "SKILL.md"), encoding="utf-8").read().splitlines():
        if re.match(r"^#{1,6}.*自检清单", line):
            in_cl = True
            continue
        if in_cl and re.match(r"^#{1,6}", line):
            break
        if in_cl:
            m = re.match(r"^\|\s*(\d+)\s*\|", line)
            if m:
                ids.append(m.group(1))
    return ids


def run_one(name, content, expect_pass):
    root = tempfile.mkdtemp(prefix="sbcase_")
    path = os.path.join(root, "sb.md")
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    try:
        r = subprocess.run([sys.executable, GATE, path, "--skill", SKILL],
                           capture_output=True, text=True)
        got = r.returncode == 0
        ok = got == expect_pass
        print("%s  %-44s 期望 %s → 实得 %s（exit=%d）" % (
            "OK  " if ok else "BAD ", name,
            "PASS" if expect_pass else "FAIL",
            "PASS" if got else "FAIL", r.returncode))
        if not ok:
            print("     " + (r.stdout or r.stderr or "").strip().replace("\n", "\n     ")[:900])
        return ok
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)


CASES = [
    ("合格分镜表（10 镜 30 秒）", good_doc(), True),
    ("片头缺【节拍】", good_doc().replace("【节拍】30s·10镜·渐快收尾\n", ""), False),
    ("时间区间有空隙（镜2 从第4秒起）", good_doc().replace("镜2  3-5秒", "镜2  4-5秒"), False),
    ("累计不满 30 秒（末镜 26-28）", good_doc().replace("镜10  26-30秒", "镜10  26-28秒"), False),
    ("缺少总时长声明仍阻断", good_doc(nshots=8, beat="无信息"), False),
    ("用户覆盖：15 秒 7 镜（节拍声明）→ 放行", good_doc(total=15, nshots=7, beat="15s·7镜·匀速"), True),
    ("景别自造词", good_doc(sizes=["超大近特"] + SIZES[1:]), False),
    ("中近景与大特写属于词库", good_doc(sizes=["中近景", "大特写"] + SIZES[2:]), True),
    ("运镜带起幅落幅动机（｜分隔）", good_doc(moves=["缓慢匀速向前推进｜起幅：两人中景｜落幅：手部近景｜动机：注意转向刀"] + MOVES[1:]), True),
    ("运镜自造词", good_doc(moves=["甩镜头"] + MOVES[1:]), False),
    ("小数秒区间不丢镜", good_doc(total=10, nshots=2, beat="10s·2镜").replace("镜1  0-5秒", "镜1  0-3.5秒").replace("镜2  5-10秒", "镜2  3.5-10秒"), True),
    ("2 秒镜塞 10 字台词", good_doc(lines=["你来了。", "我等了你整整三天三夜。"] + ["无"] * 8), False),  # 镜2=2秒, "我等了三天。"6字→超6字上限? 见下
    ("缺分镜总表节", good_doc(summary=False), False),
    ("缺切点契约/生成单元/连续性账", good_doc(tables=False), False),
    ("切点连接方式非法", good_doc().replace("| 动作接 |", "| 随便切 |", 1), False),
    ("生成单元漏覆盖镜号", good_doc().replace("| G1 | 1、2、3、4、5、6、7、8、9、10 |", "| G1 | 1、2、3 |"), False),
    ("连续性账空栏", good_doc().replace("| 阿禾 | 登记视图 |", "| 阿禾 |  |", 1), False),
    ("总表道具进出格式错", good_doc().replace("白瓷碗（1→10）", "白瓷碗"), False),
    ("总表生成方式取值非法", good_doc().replace("| 文生图 |", "| 随手画 |"), False),
    ("自检漏答（整张没填）", good_doc(acceptance=False), False),
    ("30秒8镜未声明镜数，不因默认配额阻断", good_doc(nshots=8, beat="30s·完整表演"), True),
    ("30秒单镜连续表演，未声明镜数", good_doc(nshots=1, beat="30s·连续等待"), True),
    ("显式声明9镜却交付8镜仍阻断", good_doc(nshots=8, beat="30s·9镜·渐快"), False),
]


def main():
    # 用例9：把 2 秒镜（镜2）的台词换成 10 字
    bad_line = LINES[:]
    bad_line[1] = "你终于肯来见我了"  # 8 字 > 6
    CASES[8] = ("2 秒镜塞 8 字台词", good_doc(lines=bad_line), False)
    failed = sum(0 if run_one(*c) else 1 for c in CASES)
    print("\n%d/%d 用例符合预期" % (len(CASES) - failed, len(CASES)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
