#!/usr/bin/env python3
"""build_prompt.py — 把 profile 与镜头层拼成一条提示词。

只做两件事：
  ① profile 的正向锚词前置
  ② 扫镜头描述，出现全局调色词就报错退出（色彩权归 profile 独占）

【定位】本脚本是**可选的自用拼装器**，不是提示词规范：实测散文首行写风格词
有效、剥离成脚本前置锚词反而失效（`结论-提示词体系适用性.md` §二/§四）。
因此**画风/风格词不拦**（R1 已废弃），只拦会整体改变画面调子的全局调色词；
「实体+发光色」（金色粒子/霓虹蓝数据流）是描述发光实体，不在此列。

拼接顺序：profile【正向锚词】 → 镜头层（【规避】不进词流，只作拦截规则）
（R1b：cfg=1.0 无负向通道，规避清单拼进正向会引入被排除的概念。）

用法：
    python3 build_prompt.py --profile 3d_anime --shot shot.txt
    python3 build_prompt.py --profile 3d_anime --shot shot.txt --out prompt.txt
    python3 build_prompt.py --profile 3d_anime --shot shot.txt --check-only

退出码：
    0  成功
    1  镜头层含全局调色词，或【可见光源】槽含暗类词
    2  参数或文件错误
"""
import argparse
import re
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent
PROFILES_DIR = SKILL_DIR / "profiles"

# 只禁「全局调色类」词。放开「实体+发光色」——
# 官方最优词里 golden particles / neon blue data streams / luminescent code
# 恰恰是附着在发光实体上的，正是 R3b 要的"哪片表面被光铺满"。
# 禁令一旦覆盖 golden/blue，就等于禁止描述光。
COLOR_WORDS = [
    # 全局调色类（禁）
    "色温", "色调", "调色", "配色", "色盘", "色系", "色彩",
    "暖调", "冷调", "暖色系", "冷色系", "高明度", "低饱和", "高饱和", "饱和度",
    "滤镜", "褪色", "低饱和冷色", "重饱和",
    # 英文
    "color grade", "colour grade", "color palette", "colour palette",
    "color scheme", "color tone", "colour tone", "color temperature",
    "warm-toned", "cool-toned", "desaturated", "oversaturated",
    "filter", "tint",
]

# 实体 + 发光色：允许（不列入禁用）。示例：
#   金色粒子 / 暖光 / 冷光 / 蓝色光带 / 霓虹 / 微光 / 亮起 / 透光
# 判断标准：这个词描述的是「某个在发光的实体」，不是「整幅画面的调子」。
#
# 画风/风格词（3D / cartoon / style / cinematic / 写实 / 卡通 …）**不再拦截**：
# 实测这类词写在散文首行正是真实项目出好图的关键，R1 禁令已废弃
# （`结论-提示词体系适用性.md` §二/§四、`HANDOFF-接手必读.md` §三推翻 1）。
# 把 profile 的【规避】真正并进「拦截表」的设想也未落地——规避清单只作审查提示，
# 不参与本脚本的机械硬判，故此处不再保留一份画风词禁用表。

# 允许的例外：这些词在本项目里是「叙事事实」而非色彩/调色描述
# 例如剧本要求"她穿红裙子"——这是角色设定，应从 profile 或资产设定走
ALLOWLIST = [
    "红绿灯",      # 环境实体
    "白炽灯",      # 光源实体（写"可见光源"槽时允许）
    "蓝牙",
]

# ---------------------------------------------------------------- profile 解析


def load_profile(name: str) -> dict:
    """从 profiles/<name>.md 提取六槽。缺任一必填槽则报错。"""
    path = PROFILES_DIR / f"{name}.md"
    if not path.exists():
        avail = [p.stem for p in PROFILES_DIR.glob("*.md")]
        raise FileNotFoundError(
            f"profile 不存在: {path}\n可用: {', '.join(avail) or '（无）'}"
        )
    text = path.read_text(encoding="utf-8")

    def section(title: str) -> str:
        """抓 ### 【title】 到下一个 ### 或 --- 之间的内容。"""
        # 标题形如 "### 【正向锚词】（说明文字）" —— 允许 】后有任意后缀
        m = re.search(
            rf"^###\s*【{re.escape(title)}】[^\n]*\n(.*?)(?=^###\s*【|^---|\Z)",
            text, re.M | re.S,
        )
        return m.group(1).strip() if m else ""

    # 正向锚词：优先从代码块里取
    anchor_block = section("正向锚词")
    m = re.search(r"```(?:text)?\n(.*?)\n```", anchor_block, re.S)
    anchors = (m.group(1) if m else anchor_block).strip()
    anchors = anchors.replace("\n", " ").strip().rstrip("，,")

    avoid_block = section("规避")
    m = re.search(r"```(?:text)?\n(.*?)\n```", avoid_block, re.S)
    avoids = (m.group(1) if m else avoid_block).strip()
    avoids = avoids.replace("\n", " ").strip().rstrip("，,")

    media = section("媒介").split("\n\n")[0].strip()

    profile = {
        "name": name,
        "media": media,
        "anchors": anchors,
        "avoids": avoids,
    }
    missing = [k for k in ("anchors", "avoids") if not profile[k]]
    if missing:
        raise ValueError(f"profile 缺槽: {', '.join(missing)}（{path}）")
    return profile


# ---------------------------------------------------------------- R2：可见光源不许写暗
# 只写在 SKILL.md 里而脚本不执行 = 没有这条纪律。
# 实测：第一轮根因是写了"夜色"，暗部 78%。
DARK_WORDS = [
    "暗", "黑暗", "夜色", "夜空", "夜里", "夜晚", "深夜", "黄昏", "暮色",
    "void", "darkness", "dark", "black", "pitch",
]


def check_visible_light(shot_text: str) -> list[tuple[str, int]]:
    """【可见光源】槽内禁止出现暗类词。返回 [(词, 行号)]。"""
    hits = []
    for lineno, line in enumerate(shot_text.splitlines(), 1):
        if "可见光源" not in line:
            continue
        for w in DARK_WORDS:
            # 英文词用词边界，避免 black 命中 blackboard / dark 命中 darkness 之外的误伤
            if w.isascii() and re.search(r"[a-z]", w):
                if re.search(rf"\b{re.escape(w.lower())}\b", line.lower()):
                    hits.append((w, lineno))
            elif w.lower() in line.lower():
                hits.append((w, lineno))
    return hits


# ---------------------------------------------------------------- 禁用词检查


def find_forbidden(shot_text: str) -> list[tuple[str, str, int]]:
    """返回 [(词, 类别, 行号)]。只拦全局调色词；画风词不在此列（R1 已废弃）。"""
    hits = []
    for lineno, line in enumerate(shot_text.splitlines(), 1):
        scan = line
        for w in ALLOWLIST:
            scan = scan.replace(w, " ")
        low = scan.lower()
        for w in COLOR_WORDS:
            if w.lower() in low:
                # 英文词要求词边界，避免 "filter" 命中 "filtered" 之类误报
                if w.isascii() and not re.search(rf"\b{re.escape(w)}\b", low):
                    continue
                hits.append((w, "色彩", lineno))
    return hits


# ---------------------------------------------------------------- 拼装前处理

# 五槽标签是给写词人看的清单，不进模型。【画幅】是渲染参数，也不进提示词。
SLOT_LABELS = ["景别机位", "主体", "可见光源", "环境密度", "画幅"]


def strip_slot_labels(shot_text: str) -> str:
    """剥掉【槽名】标签与【画幅】整行，只留内容。"""
    out = []
    for ln in shot_text.splitlines():
        line = ln.strip()
        if not line:
            continue
        # 【画幅】整行丢弃（渲染参数）
        if re.match(r"^【画幅】", line):
            continue
        # 其余槽标签剥掉，保留内容。标签可能出现在行首或行中（写词人夹在句中），两处都剥。
        for lab in SLOT_LABELS:
            line = re.sub(rf"【{lab}】[：:]?\s*", "", line)
        if line:
            out.append(line)
    return "；".join(out)


# ---------------------------------------------------------------- 拼接


def build(profile: dict, shot_text: str) -> str:
    """profile 正向锚词 → 镜头层。

    【规避】不参与拼接、也不被脚本读取。cfg=1.0 没有负向通道，任何否定文本都会被按正向渲染
    （实测：删掉一句 `not empty darkness but`，亮度 24.2→65.4）。
    profile 的【规避】只作人工审查提示；脚本只拦内置的全局调色词表（find_forbidden / COLOR_WORDS），
    不把 avoids 并进词表，也不进词流。
    """
    shot = strip_slot_labels(shot_text)
    parts = [profile["anchors"], shot]
    return "，".join(p.rstrip("。.") for p in parts if p) + "。"


# ---------------------------------------------------------------- main


def main() -> int:
    ap = argparse.ArgumentParser(description="profile + 镜头层 → 提示词")
    ap.add_argument("--profile", required=True, help="profiles/ 下的文件名（不含 .md）")
    ap.add_argument("--shot", required=True, help="镜头层文本文件")
    ap.add_argument("--out", help="输出文件；省略则打 stdout")
    ap.add_argument("--check-only", action="store_true", help="只做禁用词检查，不拼提示词")
    args = ap.parse_args()

    try:
        profile = load_profile(args.profile)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2

    shot_path = Path(args.shot)
    if not shot_path.exists():
        print(f"ERROR: 镜头文件不存在: {shot_path}", file=sys.stderr)
        return 2
    shot_text = shot_path.read_text(encoding="utf-8")

    dark = check_visible_light(shot_text)
    if dark:
        print("FAIL: 【可见光源】槽含暗类词（R2：必须指出哪个实体在发光）", file=sys.stderr)
        for w, ln in dark:
            print(f"  行{ln}  [暗]  {w}", file=sys.stderr)
        print("\n改法：写成「X 在发光，照亮了 Y」，不要写「夜色/暗处/void」。",
              file=sys.stderr)
        return 1

    hits = find_forbidden(shot_text)
    if hits:
        print("FAIL: 镜头层含全局调色词（色彩权归 profile 独占；画风词不拦）", file=sys.stderr)
        for w, kind, ln in hits:
            print(f"  行{ln}  [{kind}]  {w}", file=sys.stderr)
        print(
            "\n改法：把全局调色词从镜头层删掉，改由 profile 提供；\n"
            "      描述「金色粒子 / 霓虹蓝光带」这类发光实体不受限。",
            file=sys.stderr,
        )
        return 1

    if args.check_only:
        print(f"PASS: 镜头层无全局调色词（画风词不拦；profile={args.profile}）")
        return 0

    prompt = build(profile, shot_text)
    if args.out:
        Path(args.out).write_text(prompt + "\n", encoding="utf-8")
        print(f"OK  写入 {args.out}  ({len(prompt)} 字符)")
    else:
        print(prompt)
    return 0


if __name__ == "__main__":
    sys.exit(main())
