#!/usr/bin/env python3
"""gate_check.py 的回归用例：改闸门脚本后必须跑这个。

用法: python3 tests/run_cases.py

用例分两类，断言的是**退出码**：
  pass 类 = 走完流程的合格交付物 → 期望 0
  fail 类 = 故意留的缺陷（跳过闸门 / 否定式补丁 / 账本空格）→ 期望非 0

结构与引用按退出码核对；语义样本核对提示状态，不声称由脚本评价自然成文。
"""
import io
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
GATE = os.path.join(os.path.dirname(HERE), "scripts", "gate_check.py")
SKILL = os.path.dirname(HERE)

LEDGER_OK = """| # | 画外事实（查证所得） | 必须显影的像素 | 出处 | 存疑/降级 |
|---|---|---|---|---|
| 1 | 两三岁幼儿，无户外生计 | `full cheek padding, fine pores` | 项目设定 | — |
| 2 | 夏季晴暖，短袖 | `a faint sheen of sweat under his nose` | 项目设定 | 不写月份 |
| 3 | 午后偏晚，低太阳 | `the afternoon sun comes from frame left` | 场景板判读 | 角度目视推断 |
| 4 | 家常短袖短裤，散热 | `soft cotton cloth reading matte` | 身份段 | — |
| 5 | 约 2–3 岁 chibi | `an oversized round head on a small body` | 身份段 | 牙齿未查，不写牙 |
| 6 | 坐着把一大挂面塞进嘴 | `his cheeks bowed outward from the mouthful inside` | 颊肌功能（StatPearls） | — |
| 7 | 手—碗壁、唇—面、碗—桌面 | `his fingers curved around the bowl's side, the bowl's foot ring pressed into a soft contact shadow` | 接触形变规则 | — |
| 8 | 唯一光源=画面左外太阳 | `a pinhead catchlight of the sun with a broad sky reflection behind it` | catchlight 规则 | 色温估值 4500K |
| 9 | 镜头贴着桌面近端桌沿 | `the tabletop edge nearest the lens melts into soft blur` | 景深靠距离差 | 虚拟 50mm |
| 10 | 吃到一半的外卖碗 | `a red oil smear on the bowl's rim, the chopstick tips darkened with use` | 道具做旧原则 | — |
"""

BODY_OK = """```text
A vertical 9:16 still rendered in a modern 3D animated feature style, physically based
shading, subsurface scattering on skin, global illumination with soft bounce, shallow
depth of field from a virtual 50mm lens. He sits there with the deep satisfaction of a
toddler mid-meal, his torso angled toward the bowl, his head tipped down toward the noodles,
his eyes fixed on the noodles in the bowl, one hand holding the rim of a round white ceramic bowl that sits flat on the
tabletop, the bowl filled with broth up to just below the rim, white rice noodles
submerged in that broth under a floating layer of glossy red chilli oil, his chopsticks
lifting one bundle of those same noodles out of that same bowl to his open mouth, the
loose ends still trailing back down through the broth and dripping. The low afternoon sun
comes from frame left, raking across his forehead plane, his shadow side picking up a soft
green bounce off the lawn, a cool rim light tracing his scalp. His cheeks are bowed
outward from the mouthful inside, the smile pushing each lower lid up until each eye reads
as a short happy arc, fine creases fanning from the outer corners, his brow resting low and
easy. The lens sits just above the near edge of the tabletop, so that wood edge is a soft
blur, his face and the noodles at his mouth the single sharpest point, the tree line behind
him falling into blur. the white paint of the tabletop worn through to pale wood at one
corner. no text, no watermark, no flat 2D cartoon shading. physically based shading, global
illumination bounce, soft contact shadows, filmic color grade, shallow depth of field.
```"""

CAMERA_LOCK = "- 机位锁｜位置：桌面近端略高处｜camera_en：The lens sits just above the near edge of the tabletop"
PERSON_LOCK = ("- 人物构图：幼儿｜身体：朝向碗｜头部：低头朝面｜视线目标：碗里的面｜"
               "body_en：his torso angled toward the bowl｜head_en：his head tipped down toward the noodles｜"
               "gaze_en：his eyes fixed on the noodles in the bowl")
CAMERA_LANGUAGE = ("- 镜头语言：中近景｜斜侧 3/4，无轴线｜平视｜标准｜构图：幼儿位于画面中部偏右，"
                   "前景是桌面近端，背景树线虚化，左侧留出呼吸空间｜焦点：幼儿的眼睛与碗里的面清晰，"
                   "桌面边缘与背景柔化｜帧相位：起幅")

CHECKLIST_IDS = ["L0_1", "L0_2", "L0_3", "L0_4", "0c", "0f", "5b", "6c", "7", "9", "12", "13", "14", "15", "16"]


def acceptance(extra_na=True):
    rows = ["| # | 检查项 | 结论 | 证据 |", "|---|---|---|---|"]
    for cid in CHECKLIST_IDS:
        na = cid in ("14", "15", "16")
        if na and extra_na:
            rows.append("| %s | 条目 | NA：本镜单主体、室内无窗、无遮挡织物、非真人分支、无跨镜交接 |" % cid)
        else:
            rows.append("| %s | 条目 | yes | 见第 3 节正文 |" % cid)
    for i in range(1, 8):
        rows.append("| A%d | 分支追加项 | yes | 见正文 |" % i)
    return "\n".join(rows)


def good_doc(**over):
    head = over.get("head", "## S9 · 测试帧\n")
    return "\n".join([
        head,
        "### 1. 画外账本", LEDGER_OK,
        "### 2. 裁决", "帧类型：keyframe\n用途：composition\n身份段只给眼球的尺寸与反光基线，眼裂开度交给本镜的肌肉句。\n" + CAMERA_LOCK + "\n" + PERSON_LOCK + "\n" + CAMERA_LANGUAGE,
        "### 3. 提示词", BODY_OK,
        "### 4. 验收单", acceptance(),
        "", ""])


CASES = [
    # (名称, 内容, 期望是否通过)
    ("合格交付物（走完四段）", good_doc(), True),

    ("只有提示词，没走闸门", """## S9
### 3. 提示词
```text
A vertical 3D animated still of a boy eating noodles with chopsticks, happy face.
```
""", False),

    ("正文用否定式补丁 nothing else", good_doc().replace(
        "no text, no watermark, no flat 2D cartoon shading.",
        "no text, no watermark, no flat 2D cartoon shading. Nothing else on the rim, "
        "and only one bowl."), False),

    ("正文用对比式否定 rather than", good_doc().replace(
        "his brow resting low and\neasy",
        "his brow resting low and easy rather than\nraised"), False),

    ("账本出处列留空", good_doc(head="### 1. 画外账本\n").replace(
        "| 6 | 坐着把一大挂面塞进嘴 | `his cheeks bowed outward from the mouthful inside` | 颊肌功能（StatPearls） | — |",
        "| 6 | 坐着把一大挂面塞进嘴 | `his cheeks bowed outward from the mouthful inside` |  | — |"), False),

    ("账本只填三行", good_doc().replace(LEDGER_OK, "\n".join(
        LEDGER_OK.splitlines()[:6])), False),

    ("英文正文没包围栏", good_doc().replace("```text\n", "").replace("\n```", ""), False),

    ("同级提示词段不能藏第二份英文正文", good_doc().replace(
        "### 4. 验收单", "### 唯一英文正文\n```text\nA second conflicting candidate.\n```\n\n### 4. 验收单"), False),

    ("中文译文含英文术语不是第二正文", good_doc().replace(
        "### 4. 验收单", "中文译文：\n```text\n幼儿捧着 BOWL-A，画面使用 physically based shading。\n```\n\n### 4. 验收单"), True),

    ("半角文字契约必须启用精确文字审计", good_doc().replace(
        "帧类型：keyframe\n", "帧类型：keyframe\n- 文字契约:SIGN｜exact：开业｜位置：招牌\n").replace(
        "no text, no watermark", "a sign reading \"开门\", no text, no watermark"), False,
     ["--audit", "core"]),

    ("验收单结论留空", good_doc().replace("| 0c | 条目 | yes | 见第 3 节正文 |",
                                          "| 0c | 条目 |  |  |"), False),

    ("验收单整张没填", good_doc().replace(acceptance(), "| # | 检查项 | 结论 | 证据 |\n|---|---|---|---|"), False),

    ("判 no 却没抄原句", good_doc().replace("| 7 | 条目 | yes | 见第 3 节正文 |",
                                          "| 7 | 条目 | no | 略 |"), False),

    ("正文用 nothing 式补丁（背景无更亮处）", good_doc().replace(
        "corner. no text, no watermark",
        "corner. nothing in the background brighter than his cheek, no text, no watermark"), False),

    ("账本写在提示词之后", "\n".join([
        "## S9", "### 3. 提示词", BODY_OK,
        "### 1. 画外账本", LEDGER_OK,
        "### 2. 裁决", "略", "### 4. 验收单", acceptance(), ""]), False),

    ("缺裁决段", "\n".join([
        "## S9", "### 1. 画外账本", LEDGER_OK,
        "### 3. 提示词", BODY_OK, "### 4. 验收单", acceptance(), ""]), False),

    ("L0 地基失守：反重力侧滑漂移", good_doc().replace(
        "He sits there with",
        "He reels backward with other palm on floor, body slanted at 45 degree drifting on the floor"), False),

    ("L0 地基失守：中腰横切腰斩", good_doc().replace(
        "toddler mid-meal, his torso angled",
        "toddler mid-meal, the tabletop slices the frame horizontally in half, dividing the frame into upper sky and lower grass, squashing the bowl flat, his torso angled"), False),

    ("L0 地基失守：长挑杆机械崩塌", good_doc().replace(
        "his chopsticks\nlifting one bundle",
        "using a giant scallion like a long fishing pole to push the bag with chopsticks lifting one bundle"), False),

    ("缺光源实体（光凭空打）", good_doc().replace(
        "The low afternoon sun\ncomes from frame left, raking across his forehead plane, his shadow side picking up a soft\ngreen bounce off the lawn",
        "The light\nfalls evenly across his face, his shadow side staying readable"), False),

    ("open shadows 复数属于有效明暗关系", good_doc().replace(
        "his shadow side", "his shaded side").replace(
        "soft contact shadows", "open shadows"), True),

    ("人物镜无表演态度锚点句", good_doc().replace(
        "deep satisfaction of a\ntoddler mid-meal", "hands resting"), False),

    ("缺情绪词的人工偏差记录不等于结构失败", good_doc().replace(
        "deep satisfaction of a\ntoddler mid-meal", "hands resting").replace(
        "| 13 | 条目 | yes | 见第 3 节正文 |",
        "| 13 | 条目 | no | `the bowl filled with broth up to just below the rim` 已定稿冻结帧，原句备案 |"), True),

    ("gaze drifting 不是肢体漂移（L0.2 不误伤视线移动）", good_doc().replace(
        "He sits there with", "His gaze drifting to the bowl, he sits there with"), True),

    ("人物镜缺机位锁与人物构图", good_doc().replace(CAMERA_LOCK + "\n" + PERSON_LOCK, ""), False),
    ("人物镜缺机位锁", good_doc().replace(CAMERA_LOCK + "\n", ""), False),
    ("人物镜缺逐人构图与视线锁", good_doc().replace("\n" + PERSON_LOCK, ""), False),
    ("视线目标只写不看镜头", good_doc().replace("视线目标：碗里的面", "视线目标：不看镜头"), False),
    ("视线英文锚点没有进入真实正文", good_doc().replace(
        "his eyes fixed on the noodles in the bowl, one hand", "his eyes wandering, one hand"), False),
    ("普通人物镜擅自直视镜头", good_doc().replace(
        "his eyes fixed on the noodles in the bowl", "his eyes looking directly at the camera"), False),
    ("有叙事裁决的直视镜头可写", good_doc().replace(
        "his eyes fixed on the noodles in the bowl", "his eyes looking directly at the camera").replace(
        "视线目标：碗里的面", "视线目标：镜头（有意直视：人物主动打破第四面墙）"), True),
    ("同一人物的构图锁不能重复", good_doc().replace(
        CAMERA_LOCK + "\n" + PERSON_LOCK, CAMERA_LOCK + "\n" + PERSON_LOCK + "\n" + PERSON_LOCK), False),
    ("关键帧缺七项镜头语言锚点", good_doc().replace("\n" + CAMERA_LANGUAGE, ""), False),
    ("镜头语言只有景别单词", good_doc().replace(CAMERA_LANGUAGE, "- 镜头语言：中景"), False),
    ("镜头语言缺焦点与帧相位", good_doc().replace(
        CAMERA_LANGUAGE, "- 镜头语言：中近景｜斜侧 3/4，无轴线｜平视｜标准｜构图：幼儿位于画面中部偏右，前景是桌面近端，背景树线虚化"), False),
    ("镜头语言把否定当视线目标", good_doc().replace(
        "斜侧 3/4，无轴线", "斜侧 3/4，不看镜头"), False),
]


# 这些是语义审读样本。不得把词面或行数误报当成确定性结构错误。
REVIEW_NAMES = ['正文用否定式补丁 nothing else', '正文用对比式否定 rather than', '正文用 nothing 式补丁（背景无更亮处）', 'L0 地基失守：反重力侧滑漂移', 'L0 地基失守：中腰横切腰斩', 'L0 地基失守：长挑杆机械崩塌']
STRUCTURE_ONLY_NAMES = ['正文用否定式补丁 nothing else', '正文用对比式否定 rather than', '正文用 nothing 式补丁（背景无更亮处）', 'L0 地基失守：反重力侧滑漂移', 'L0 地基失守：中腰横切腰斩', 'L0 地基失守：长挑杆机械崩塌', '账本只填三行', '缺光源实体（光凭空打）', '人物镜无表演态度锚点句']
CASES = [tuple([case[0], case[1], True] + list(case[3:]))
         if case[0] in STRUCTURE_ONLY_NAMES else case for case in CASES]


# 同一幅画面的关系可跨字段共处一句；锚点仍须在真实正文中逐字定位。
RELATIONAL_BODY = """```text
Rendered in a modern 3D animated feature style, a boy sits with deep satisfaction over
his meal. The lens sits just above the near edge of the tabletop, catching his torso angled
toward the bowl, his head tipped down toward the noodles and his eyes fixed on the noodles
in the bowl, where white noodles rest inside broth held by a ceramic bowl on the worn wood.
The afternoon sun comes from frame left across his cheek; the shaded side picks up a soft
bounce from the lawn, while the table edge falls into soft blur beneath his sharp face.
```"""
RELATIONAL_BODY = " ".join(RELATIONAL_BODY.splitlines()).replace("```text ", "```text\n").replace(" ```", "\n```")
RELATIONAL_DOC = good_doc().replace(BODY_OK, RELATIONAL_BODY)
CASES.extend([
    ("关系成文：同一句提供四字段的短语证据", RELATIONAL_DOC, True),
    ("摘录比对只归一化空白，不强制完整句", RELATIONAL_DOC.replace(
        "his head tipped down toward the noodles and", "his head tipped\n down toward the noodles and"), True),
])
for anchor, missing in (
    ("The lens sits just above the near edge of the tabletop", "A tabletop viewpoint"),
    ("his torso angled toward the bowl", "his torso angled forward"),
    ("his head tipped down toward the noodles", "his head tipped down"),
    ("his eyes fixed on the noodles in the bowl", "his eyes fixed on the meal"),
):
    CASES.append(("改稿未同步证据：" + anchor, RELATIONAL_DOC.replace(
        RELATIONAL_BODY, RELATIONAL_BODY.replace(anchor, missing)), False))


# L0 是否否决与是否抄出证据是两件事；普通与 strict 都应阻断。
for cid in ("L0_1", "L0_2", "L0_3", "L0_4"):
    for strict in (False, True):
        bad = good_doc().replace(
            "| %s | 条目 | yes | 见第 3 节正文 |" % cid,
            "| %s | 条目 | no | `He sits there with` 已冻结帧，原句证据完整 |" % cid)
        CASES.append(("%s 判 no 有原句证据%s仍阻断" %
                      (cid, " strict " if strict else " "), bad, False,
                      ["--strict"] if strict else []))
CASES.append(("反向检查项判 no 不等于 L0 否决", good_doc().replace(
    "| 0c | 条目 | yes | 见第 3 节正文 |",
    "| 0c | 条目 | no | `physically based shading` 没有靠地域符号硬凑 |"), True))


SHOTLIST_OK = """| 镜 | 职责 | 台词 | 道具进出 | 生成方式 | 跨镜连续物 |
|---|---|---|---|---|---|
| S9 | 建立镜头：单人用餐环境 | — | 白瓷碗（S9→S9） | 文生图 | 白瓷碗 |
"""

IDENTITY_OK = """# 身份段唯一权威

## 幼儿
> presence: He, his, boy
```text
A vertical 9:16 still rendered in a modern 3D animated feature style, physically based
shading, subsurface scattering on skin, global illumination with soft bounce, shallow
depth of field from a virtual 50mm lens.
```
"""


def build_project(root):
    io.open(os.path.join(root, "SHOTLIST.md"), "w", encoding="utf-8").write(SHOTLIST_OK)
    os.makedirs(os.path.join(root, "prompts"), exist_ok=True)
    io.open(os.path.join(root, "prompts", "IDENTITY.md"), "w", encoding="utf-8").write(IDENTITY_OK)


# --project 模式用例：需要真实项目目录，在 main() 里建临时项目再跑
PROJECT_CASES = [
    ("project：三件套齐全 → PASS", good_doc(), True, {}),
    ("project：缺 SHOTLIST.md", good_doc(), False, {"no_shotlist": True}),
    ("project：帧号未登记", good_doc(), False, {"shotlist": SHOTLIST_OK.replace("| S9 |", "| S8 |")}),
    ("project：身份段与 IDENTITY.md 不一致", good_doc().replace(
        "physically based\nshading, subsurface scattering on skin", "physically based\nshading, extra purple backpack on the child"), False, {}),
    ("project：冻结备注不能吞掉真实身份差异", good_doc().replace(
        "physically based\nshading, subsurface scattering on skin", "physically based\nshading, extra purple backpack on the child").replace(
        "| 14 | 条目 | NA：本镜单主体、室内无窗、无遮挡织物、非真人分支、无跨镜交接 |",
        "| 14 | 条目 | no | `modern 3D animated feature style` 已定稿冻结帧备案 |"), False, {}),
    ("project：道具进出格式不合规", good_doc(), False,
     {"shotlist": SHOTLIST_OK.replace("白瓷碗（S9→S9）", "白瓷碗")}),
    ("project：生成方式取值非法", good_doc(), False,
     {"shotlist": SHOTLIST_OK.replace("| 文生图 |", "| 随手画 |")}),
]


VIEW_FULL = "角色A wears a black penguin hood, a white belly patch and orange slippers."
VIEW_REAR = "角色A wears a black penguin hood and orange slippers."
VIEW_LIBRARY = IDENTITY_OK + "\n## 角色A\n> presence: 角色A\n```text\n" + VIEW_FULL + "\n```\n### 背面\n> identity: 角色A\n> view: rear\n```text\n" + VIEW_REAR + "\n```\n"

def view_doc(anchor=VIEW_REAR, declaration="身份视图：角色A=rear"):
    return good_doc().replace("### 2. 裁决\n", "### 2. 裁决\n" + declaration + "\n").replace(
        "no text, no watermark", anchor + " no text, no watermark")

PROJECT_CASES.extend([
    ("project：空身份库不能作为免检", good_doc(), False, {"identity": "# 身份库\n"}),
    ("project：已登记背面锚点可用，无需补出正脸", view_doc(), True, {"identity": VIEW_LIBRARY}),
    ("project：未知视图不能绕过身份", view_doc(declaration="身份视图：角色A=unknown"), False, {"identity": VIEW_LIBRARY}),
    ("project：未登记角色不能借视图放行", view_doc(declaration="身份视图：Other=rear"), False, {"identity": VIEW_LIBRARY}),
    ("project：视图不能隐式放宽默认完整身份", view_doc(declaration=""), False, {"identity": VIEW_LIBRARY}),
    ("project：完整身份默认仍可用", view_doc(anchor=VIEW_FULL, declaration=""), True, {"identity": VIEW_LIBRARY}),
    ("project：登记视图仍必须引用锚点", view_doc(anchor="角色A wears a red penguin hood."), False, {"identity": VIEW_LIBRARY}),
    ("project：重复视图选择阻断", view_doc(declaration="身份视图：角色A=rear\n身份视图：角色A=full"), False, {"identity": VIEW_LIBRARY}),
    ("project：不在场角色和其视图不强制入画", good_doc(), True, {"identity": VIEW_LIBRARY}),
    ("project：冻结备案不掩盖未登记视图", view_doc(declaration="身份视图：角色A=unknown").replace(
        "| 14 | 条目 | NA：本镜单主体、室内无窗、无遮挡织物、非真人分支、无跨镜交接 |",
        "| 14 | 条目 | no | `角色A wears a black penguin hood` 已冻结帧备案 |"), False, {"identity": VIEW_LIBRARY}),
])


def run_one(name, content, expect_pass, extra_argv=None, fname="S9.md"):
    root = tempfile.mkdtemp(prefix="gatecase_")
    path = os.path.join(root, fname)
    with io.open(path, "w", encoding="utf-8") as fh:
        fh.write(content)
    try:
        r = subprocess.run([sys.executable, GATE, path, "--skill", SKILL] + (extra_argv or []),
                            capture_output=True, text=True)
        got_pass = (r.returncode == 0)
        ok = got_pass == expect_pass
        if got_pass:
            ok = ok and "NOT_EVALUATED" in r.stdout
        if name in REVIEW_NAMES:
            ok = ok and "WARN  " in r.stdout
        print("%s  %-40s 期望 %s → 实得 %s（exit=%d）" % (
            "OK  " if ok else "BAD ", name,
            "PASS" if expect_pass else "FAIL",
            "PASS" if got_pass else "FAIL", r.returncode))
        if not ok:
            print("     " + (r.stdout or "").strip().replace("\n", "\n     ")[:900])
        return ok
    finally:
        import shutil
        shutil.rmtree(root, ignore_errors=True)


def main():
    failed = 0
    for case in CASES:
        name, content, expect_pass = case[:3]
        extra_argv = case[3] if len(case) > 3 else None
        if not run_one(name, content, expect_pass, extra_argv):
            failed += 1
    for name, content, expect_pass, opts in PROJECT_CASES:
        root = tempfile.mkdtemp(prefix="gateproj_")
        try:
            if not opts.get("no_shotlist"):
                io.open(os.path.join(root, "SHOTLIST.md"), "w", encoding="utf-8").write(
                    opts.get("shotlist", SHOTLIST_OK))
            if "shotlist" not in opts:
                os.makedirs(os.path.join(root, "prompts"), exist_ok=True)
                io.open(os.path.join(root, "prompts", "IDENTITY.md"), "w", encoding="utf-8").write(opts.get("identity", IDENTITY_OK))
            if not run_one(name, content, expect_pass, ["--project", root]):
                failed += 1
        finally:
            import shutil
            shutil.rmtree(root, ignore_errors=True)
    print("\n%d/%d 用例符合预期" % (len(CASES) + len(PROJECT_CASES) - failed,
                                 len(CASES) + len(PROJECT_CASES)))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
