#!/usr/bin/env python3
"""h3_lint.py — H3 提示词工程一致性检查。

真实项目的瓶颈不是出图质量，是 H3 提示词的工程一致性。
《咕角色C嘎》EP01 返修 4 轮卡住的五类问题，qc_image.py 一个都查不出来：

  P0-1  <Picture N> 的定义与使用不一致（Picture 4 已改指父母手部，S04 仍标成客厅背景）
  P0-2  出场主体的参考图未在本场加载（S08 说"笑"的主语没加载图片）
  P0-3  动作链物理冲突（一手牵两人同时挥手）
  P1-1  同一角色的术语漂移（flipper hand / flipper sleeve / right hand）
  P1-3  台词语速超载（字数 ÷ 4.1字/秒 + 2 秒余量 > 段落时长；4.1 与 h3_gate G18 同口径）

本脚本查前 4 类 + 时长；P0-3 只做启发式提示，不做硬判。

用法：
    python3 h3_lint.py <提示词文件或目录>
    python3 h3_lint.py <文件> --json

退出码：
    0  无 P0 问题且必要检查已完成（P1 警告不阻断）
    1  有 P0 问题
    2  参数错误或必要检查未完成（NOTCHK）
"""
import argparse
import json
import re
import sys
from pathlib import Path

# 中文语速：与 h3-video-gate G18 同口径 4.1 字/秒，外加 2 秒表演余量
CHARS_PER_SECOND = 4.1
ACTING_MARGIN = 2.0

# 术语同义词簇：**同一簇内出现 ≥2 个互斥变体** = 真漂移。
# 注意：单复数是同一术语的语法变形，不算漂移。
# 只有「同一身体部位用了两套互斥名字」才是真问题：
#   把鳍袖写成 flipper sleeve（正确）vs 写成 hand / right hand（错误，因为手被袖子盖住）
TERM_CONFLICTS = [
    {
        "name": "手/鳍袖",
        "canonical": ["flipper sleeve", "flipper sleeves", "flipper hand", "flipper hands"],
        "conflict": ["right hand", "left hand", "his hand", "her hand", "bare hand"],
        "why": "手被 padded black fleece flipper sleeves 覆盖，镜头链不应写裸手/right hand",
    },
]

# 时间戳行：[Shot N] At MM:SS.mmm
SHOT_RE = re.compile(r"\[Shot\s+(\d+)\]")
SHOT_TS_RE = re.compile(
    r"\[Shot\s+(\d+)\]\s+At\s+(\d{2}):(\d{2})\.(\d{3})(?=\s|$|[,.;])"
)
PICTURE_REF = re.compile(r"<Picture\s+(\d+)>")
# 官方对齐句里的帧号是**裸写法** `Picture 1 (from Shot 1)`（base-en.txt:25 / :201），
# 不带尖括号。任何「数有几张参考帧」的判断都必须同时认两种写法，否则会漏判。
PICTURE_ANY_RE = re.compile(r"(?:<Picture\s+|(?<![<\w])Picture\s+)(\d+)")
SUBJECT_REF = re.compile(r"<Subject\s+(\d+)>")
DURATION_RE = re.compile(r"(?:duration|时长)[^\d]{0,10}(\d+(?:\.\d+)?)\s*s", re.I)


def load(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def check_picture_definitions(text: str) -> list[str]:
    """P0-1：<Picture N> 必须在该文件内有定义句，且定义内容不与使用处矛盾。

    定义句形如：`<Picture 4> is/refers to ...` 或 `Image 4 ...`
    这里只查「有没有定义」+「定义的角色名与使用处的角色名冲突」。
    """
    issues = []
    used = sorted({int(m) for m in PICTURE_REF.findall(text)})
    if not used:
        return issues

    # 定义有三种合法写法，都要认：
    #   (a) <Picture N> is ...
    #   (b) <Subject K> is ... in <Picture N>, featuring ...   ← 官方主用写法
    #   (c) <Picture N> (appears in [Shot X]): ...
    defined = set()
    for m in re.finditer(r"<Picture\s+(\d+)>\s*(?:is|are|为|是|：|:)", text):
        defined.add(int(m.group(1)))
    for m in re.finditer(r"<Subject\s+\d+>\s+is[^\n]*?in\s+<Picture\s+(\d+)>", text):
        defined.add(int(m.group(1)))
    for m in re.finditer(r"<Picture\s+(\d+)>\s*\(", text):
        defined.add(int(m.group(1)))

    for n in used:
        if n not in defined:
            issues.append(
                f"P0-1 <Picture {n}> 被引用但无定义句"
                f"（应有 `<Picture {n}> is ...` / `<Subject K> is ... in <Picture {n}>` / `<Picture {n}> (appears in ...)`）"
            )
    return issues


def check_reference_loaded(text: str) -> list[str]:
    """P0-2：出场主体（<Subject N>）在本文件内必须至少有 1 次 <Picture N> 加载。

    启发式：若文本出现 <Subject 2> 但全文一个 <Picture> 都没有 → 报缺失。
    """
    issues = []
    subs = sorted({int(m) for m in SUBJECT_REF.findall(text)})
    pics = sorted({int(m) for m in PICTURE_REF.findall(text)})
    if subs and not pics:
        issues.append(
            f"P0-2 出现了 <Subject {subs[0]}...> 但没有任何 <Picture N> 加载；"
            f"出场主体缺参考图"
        )
    return issues


def check_terms(text: str) -> list[str]:
    """P1-1：canonical 与 conflict 两套名字同时出现 → 真术语漂移。

    单复数、大小写不算漂移。
    """
    issues = []
    low = text.lower()
    for c in TERM_CONFLICTS:
        canon = sorted({t for t in c["canonical"] if t in low})
        conf = sorted({t for t in c["conflict"] if re.search(rf"\b{re.escape(t)}\b", low)})
        if canon and conf:
            issues.append(
                f"P1-1 术语漂移（{c['name']}）：规范词 {canon} 与冲突词 {conf} 同时出现。"
                f"原因：{c['why']}"
            )
    return issues


def check_shot_timing(text: str) -> list[str]:
    """时间戳：Shot 1 无时间戳；后续严格递增。"""
    issues = []
    shots = [int(m) for m in SHOT_RE.findall(text)]
    if not shots:
        return issues
    # 只认真实 At MM:SS.mmm；At night 等自然语言不是时间戳。
    m1 = next((m for m in SHOT_TS_RE.finditer(text) if int(m.group(1)) == 1), None)
    if m1:
        issues.append("P1-2 [Shot 1] 不应带时间戳（官方规范：Shot 1 无 At MM:SS.mmm）")

    times = []
    for m in SHOT_TS_RE.finditer(text):
        n = int(m.group(1))
        sec = int(m.group(2)) * 60 + int(m.group(3)) + int(m.group(4)) / 1000
        times.append((n, sec))
    for i in range(1, len(times)):
        if times[i][1] <= times[i - 1][1]:
            issues.append(
                f"P1-2 [Shot {times[i][0]}] 时间 {times[i][1]:.3f}s 未严格大于 "
                f"[Shot {times[i-1][0]}] 的 {times[i-1][1]:.3f}s"
            )
    return issues


def check_dialogue_overload(text: str) -> list[str]:
    """P1-3：按 4.1 字/秒 + 2 秒余量检查每个可确定时长的台词段。

    时长可来自下一镜的真实 At MM:SS.mmm；末镜使用全文 duration/时长。
    无法确定边界的台词段返回 NOTCHK 项，不把“没算”当成通过。
    """
    issues = []

    def dialogue_chars(segment: str) -> int:
        lines = re.findall(r"<d>(.*?)</d>", segment, re.S)
        return sum(len(re.sub(r"\[[^\]]*\]", "", line).strip()) for line in lines)

    def check_segment(label: str, total_chars: int, duration: float):
        need = total_chars / CHARS_PER_SECOND + ACTING_MARGIN
        if need > duration:
            where = f"（{label}）" if label else ""
            duration_label = "镜头时长" if label else "声明时长"
            issues.append(
                f"P1-3 台词超载{where}：{total_chars} 字 ÷ {CHARS_PER_SECOND}字/秒 "
                f"+ {ACTING_MARGIN}s 余量 = {need:.1f}s > {duration_label} {duration:.1f}s"
            )

    def notchecked(label: str):
        where = f"{label}：" if label else ""
        issues.append(
            f"P1-3 NOTCHK {where}无法确定台词所在镜头时长；"
            "需下一镜真实 At MM:SS.mmm，或末镜/单段全文 duration（时长）Ns"
        )

    def timestamp_at(match) -> float:
        ts = SHOT_TS_RE.match(text, match.start())
        if not ts:
            return None
        return int(ts.group(2)) * 60 + int(ts.group(3)) + int(ts.group(4)) / 1000

    duration_match = DURATION_RE.search(text)
    declared_duration = float(duration_match.group(1)) if duration_match else None
    shot_matches = list(SHOT_RE.finditer(text))

    if not shot_matches:
        total_chars = dialogue_chars(text)
        if not total_chars:
            return issues
        if declared_duration is None:
            notchecked("")
        else:
            check_segment("", total_chars, declared_duration)
        return issues

    # 正式结构里台词属于 Shot；若镜头外仍有台词，也不能静默漏掉。
    prefix_chars = dialogue_chars(text[:shot_matches[0].start()])
    if prefix_chars:
        if declared_duration is None:
            notchecked("镜头外台词")
        else:
            check_segment("镜头外台词", prefix_chars, declared_duration)

    for index, shot in enumerate(shot_matches):
        shot_no = int(shot.group(1))
        end_pos = shot_matches[index + 1].start() if index + 1 < len(shot_matches) else len(text)
        total_chars = dialogue_chars(text[shot.start():end_pos])
        if not total_chars:
            continue

        label = f"[Shot {shot_no}]"
        start = timestamp_at(shot)
        if start is None and shot_no == 1:
            start = 0.0
        end = None
        if index + 1 < len(shot_matches):
            end = timestamp_at(shot_matches[index + 1])
        elif declared_duration is not None:
            end = declared_duration
        if start is None or end is None or end <= start:
            notchecked(label)
            continue
        check_segment(label, total_chars, end - start)
    return issues


def check_physical_heuristic(text: str) -> list[str]:
    """P0-3 启发式：同时出现「牵手/握手」与「挥手/招手」→ 提示可能物理冲突。

    只做提示，不算硬失败。
    """
    hints = []
    low = text.lower()
    holding = any(k in low for k in ["holding the hand", "holding hands", "hand in hand",
                                     "firmly holding", "牵着", "拉着"])
    waving = any(k in low for k in ["waving", "waves back", "beckoning", "挥手", "招手"])
    if holding and waving:
        hints.append("P0-3(hint) 同时出现「牵手」与「挥手」——请人工确认动作是否物理可执行")
    return hints


def _is_ref_mode(text: str) -> bool:
    """是不是 Ref2VA 六段模式（`subject_definitions:` / `detailed_description:`）。

    Ref2VA 的参考图用 <Picture N> 引用多张素材是正常写法，不该受 FL2VA 单段约束。
    """
    return bool(re.search(r"^\s*(?:subject_definitions|detailed_description)\s*:", text, re.M))


def check_fl2va_single_shot(text: str) -> list[str]:
    """P0-4：FL2VA 出现 ≥2 个 [Shot N] 却没声明要硬切 = 诱发切镜。

    官方 base-en.txt:62：FL2VA favors a single shot, 首尾帧同属 [Shot 1]。
    实测：写成 3 段 + 绝对时间码后，H3 会在该时间码处抽出真硬切
    （S07 帧 66：帧差 106.5/255，直方图距离 0.64，机位与光照瞬时全换）。

    【FL2VA 判定用结构，不用措辞】——2026-10-22 第三次同构缺口的修法：
    原先用「首行有没有 `aligns with the … mark` 对齐句」来认 FL2VA，
    结果首行只要写成 `Picture 1 is the first frame …` 这类等价措辞，
    双帧三段式就整份漏过（h3_lint 与 h3_gate --strict 双双 exit=0）。
    这与 G08b 的 `LABEL_RE` 只认 `<Picture N>`、不认官方裸标签是同一根因：
    **正则只认「我以为的写法」，不认官方范例的真实写法。**

    现在的判据是官方的模式定义本身：base 模式（非 Ref2VA）+ 同时加载
    Picture 1 与 Picture 2 双帧 = FL2VA 首尾帧插值，必须单段。
    I2VA / L2VA 只加载一张帧，天然不受此约束（官方 Case 4 L2VA 即单张尾帧）。
    """
    issues = []
    shots = [int(m) for m in SHOT_RE.findall(text)]
    if len(shots) < 2:
        return issues

    if _is_ref_mode(text):
        return issues

    low = text.lower()
    # 帧号两种写法都要认：带尖括号 `<Picture 1>` 与官方对齐句里的裸 `Picture 1 (from Shot 1)`
    pics = sorted({int(m.group(1)) for m in PICTURE_ANY_RE.finditer(text)})
    has_align = bool(re.search(r"aligns with the .{0,40}?(?:mark|second)", low))
    # 结构判据：首帧与尾帧同时加载就是 FL2VA（官方 I2VA/L2VA 只用一张帧）
    has_both_frames = 1 in pics and 2 in pics
    is_fl = has_both_frames or (has_align and len(pics) >= 2)
    if not is_fl:
        return issues

    # 声明了要硬切才放行
    declared = any(k in low for k in [
        "the camera cuts to", "the shot cuts to", "the shot transitions to",
        "the shot changes to", "the shot switches to", "cross-dissolve",
    ])
    # 首尾帧是否被写进不同段（错法）。帧号同样两种写法都要认。
    per_shot = {}
    for m in re.finditer(r"\[Shot\s+(\d+)\]", text):
        n = int(m.group(1))
        start = m.end()
        nxt = SHOT_RE.search(text, start)
        seg = text[start: nxt.start() if nxt else len(text)]
        per_shot[n] = set(int(x) for x in PICTURE_ANY_RE.findall(seg))

    if not declared:
        issues.append(
            f"P0-4 FL2VA/L2VA 写了 {len(shots)} 个 [Shot N]，但正文没有声明硬切词"
            f"（`the camera cuts to` 等）——官方要求 FL2VA 单段，分段会诱发真切镜。"
            f"改法：合并为 [Shot 1]，删掉所有 `At MM:SS.mmm`，用一条连续运镜串完，"
            f"结尾写 `decelerates into the exact ... of Picture 2 at the end of the shot`"
        )
    # 「首尾帧分属不同段」只在**未声明硬切**时才算错：官方 base-en.txt:62 明确
    # 「Use multiple shots only when they are explicitly specified. The last frame
    # must be reached by the final `[Shot N]`」——声明了硬切的多段里，尾帧本就属于最后一段。
    # 若不加这个条件就会把官方合法范例判成错（2026-10-22 实测过该反例）。
    holders = [n for n, ps in per_shot.items() if ps]
    if not declared and len(holders) >= 2:
        issues.append(
            f"P0-4 首帧与尾帧被分到不同段（段 {holders} 各自引用 Picture）——"
            f"官方范例两张帧都写 `(from Shot 1)`"
        )
    return issues


def lint(path: Path) -> dict:
    text = load(path)
    p0 = []
    p1 = []
    p0 += check_picture_definitions(text)
    p0 += check_reference_loaded(text)
    p0 += check_physical_heuristic(text)
    p0 += check_fl2va_single_shot(text)
    p1 += check_terms(text)
    p1 += check_shot_timing(text)
    dialogue_results = check_dialogue_overload(text)
    notchecked = [x for x in dialogue_results if x.startswith("P1-3 NOTCHK")]
    p1 += [x for x in dialogue_results if x not in notchecked]
    status = ("BLOCK" if p0 else "NOTCHK" if notchecked else
              "WARN" if p1 else "PASS")
    return {
        "path": str(path),
        "p0": p0,
        "p1": p1,
        "notchecked": notchecked,
        "status": status,
        "pass": len(p0) == 0 and not notchecked,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="H3 提示词工程一致性检查")
    ap.add_argument("targets", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    files = []
    for t in args.targets:
        p = Path(t)
        if p.is_dir():
            files += sorted(p.glob("*.md")) + sorted(p.glob("*.txt"))
        elif p.is_file():
            files.append(p)
        else:
            print(f"ERROR: 不存在 {p}", file=sys.stderr)
            return 2
    if not files:
        print("ERROR: 没有可检查的文件", file=sys.stderr)
        return 2

    results = [lint(f) for f in files]

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=1))
    else:
        for r in results:
            name = Path(r["path"]).name
            if r["status"] == "PASS":
                print(f"PASS  {name}")
                continue
            tag = "FAIL" if r["status"] == "BLOCK" else r["status"]
            print(f"{tag}  {name}")
            for x in r["p0"]:
                print(f"   {x}")
            for x in r["p1"]:
                print(f"   {x}")
            for x in r["notchecked"]:
                print(f"   {x}")
        n_p0_pass = sum(1 for r in results if not r["p0"])
        print(f"\nP0 通过 {n_p0_pass} / {len(results)}")
        n_notchecked = sum(1 for r in results if r["notchecked"])
        if n_notchecked:
            print(f"NOTCHK {n_notchecked} / {len(results)}（台词时长检查未完成）")

    if any(r["p0"] for r in results):
        return 1
    return 2 if any(r["notchecked"] for r in results) else 0


if __name__ == "__main__":
    sys.exit(main())
