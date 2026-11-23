#!/usr/bin/env python3
"""单帧文字结构与引用检查，不评价画面质量或授权生产。

用法：python3 gate_check.py <帧稿> [--skill <技能目录>] [--frame-kind still|keyframe|asset]
      [--project <独立SHOTLIST/IDENTITY项目>] [--identity <身份库>] [--shotlist <分镜总表>]

确定性错误返回1：正文缺失/多候选、必要来源或核对项缺失、摘录漂移、身份引用不一致。
词面风险仅提示重读，不证明动作不成立。七项镜头语言仅对镜头静帧必需。
已有其它项目布局显式传来源路径，不为检查重建文档。退出码0仅表示这些结构检查未发现错误；
事实、自然成文、画风、实际参考和生成效果均需审读/实看，并在结果中记为未评估。
"""
import argparse
import io
import os
import re
import sys

REQUIRED_SECTIONS = [
    ("账本", r"账本|必要依据|依据"),
    ("裁决", r"裁决|制作元数据|从正文摘录"),
    ("提示词", r"提示词|prompt|英文正文"),
    ("验收单", r"验收单|自检(清单)?|文字核对表"),
]
CORE_CHECKLIST_IDS = ("L0_1", "L0_4", "0f", "9", "12", "16")
RISK_CHECKLIST_IDS = {
    "multi": ("0c", "6c"),
    "exact_text": ("5b",),
    "contact": ("L0_2", "0c"),
    "keyframe": ("L0_3", "6c", "15"),
    "continuity": ("14", "15"),
}
RISK_KINDS = ("multi", "exact_text", "contact", "continuity")
AUDIT_PROFILES = ("core", "full")

# 正文里的"禁令式补丁"（长期规矩：不靠否定词修图，一律回改成正在发生什么）
BODY_NEGATIVES = [
    r"\bno\s+person\b", r"\bno\s+people\b", r"\bnothing\s+else\b", r"\bno\s+other\b",
    r"\bnot\s+(?:a\s+)?[\w-]+\s+but\b", r"\brather\s+than\b", r"\binstead\s+of\b",
    r"\bonly\s+(?:one|two|three)\s+(?:eye|eyes|bowl|bowls|person|people|boy|girl)\b",
    r"\bwithout\s+(?:a|an|any)\s+[\w-]+", r"\bno\s+second\b",
    r"\bnothing\b", r"\bbut\s+not\s+into\b", r"\bno\s+one\s+else\b",
]

# 允许的排除项：风格排除 + 介质缺陷（off-frame-brief.md 第四节划的边界）
# L0 地基刚性红线：自动化阻断高危反物理、腰斩构图与极端多体机械
L0_HAZARDS = [
    ("L0.2 反重力肢体漂移", re.compile(r"\b(drifting\s+(?:across|on|along)\s+the\s+(?:floor|ground)|slanted\s+at\s+45|reels\s+backward\s+with\s+other\s+palm|sliding\s+across\s+the\s+floor|breakdance)\b", re.I)),
    ("L0.3 竖屏画幅中腰横切腰斩", re.compile(r"\b(slices\s+the\s+frame\s+horizontally|table\s+dividing\s+the\s+frame\s+into\s+upper|board\s+cutting\s+across\s+the\s+center|squashing\s+the\s+bowl\s+flat)\b", re.I)),
    ("L0.4 极端多体机械杠杆/长挑杆", re.compile(r"\b(giant\s+scallion\s+like\s+a\s+long\s+fishing\s+pole|fishing\s+pole\s+to\s+push|rigid\s+fishing\s+rod|lever\s+pole\s+suspending)\b", re.I)),
]

ALLOWED_EXCLUSIONS = re.compile(
    r"\bno\s+(?:text|watermark|logo|caption|letters?|signage|cgi|3d\s+render|cartoon|"
    r"flat\s+2d|anime|plastic|mushroom|extra\s+(?:fingers|limbs|arms|hands)|missing[\w\s]*|"
    r"blur|noise|jpeg|banding|over-?sharpen\w*|studio\s+lighting|blown-?out\w*|"
    r"dead\s+black|lens\s+flare|vignette|bokeh\s+balls|duplicate|clone|flipped|mirrored)\w*",
    re.I)

CJK = re.compile(r"[\u3400-\u9fff]")
ID_RE = re.compile(r"^([0-9]+[a-z]?[0-9]?|A[0-9]+|L[0-3]_[0-9]+)$")

# 人物词仅用于提示存在人物字段的可能；不证明完整出场或情绪。
PERSON_MARKERS = re.compile(
    r"\b(boy|girl|mother|father|man|woman|men|women|toddler|baby|kid|child|"
    r"he|she|his|her|him)\b", re.I)

# 构图与视线是实际输入契约，不只是验收单里的自述。每个人物的英文锚点
# 必须在真正提交的正文里逐字出现；正面直视只有明确叙事意图时才合法。
CAMERA_LOCK_RE = re.compile(r"^[-*+]\s*机位锁｜(.+)$", re.M)
PERSON_COMPOSITION_RE = re.compile(r"^[-*+]\s*人物构图：([^｜\n]+)｜(.+)$", re.M)
# 镜头静帧的七项取景字段；见短剧分镜技能 references/keyframe-camera-language.md。
# 它必须和机位锁/人物构图一起落在裁决段，保证帧级取景（景别、角度、高度、
# 焦段、构图、焦点、帧相位）在写词时已被选择，而不是留给模型默认值。
CAMERA_LANGUAGE_RE = re.compile(r"^[-*+]\s*镜头语言：(.+)$", re.M)
CAMERA_LANGUAGE_SLOTS = (
    "景别", "水平角度", "机位高度", "焦段意图", "构图", "焦点", "帧相位",
)
CAMERA_LANGUAGE_FRAMINGS = (
    "大远景", "远景", "全景", "中全景", "中近景", "中景",
    "近景", "特写", "大特写", "插入特写",
)
CAMERA_LANGUAGE_ANGLES = ("正面", "斜侧", "正侧", "后斜侧", "背面", "轴线")
CAMERA_LANGUAGE_HEIGHTS = ("地平", "低", "仰", "平视", "高", "俯", "顶视")
CAMERA_LANGUAGE_FOCALS = ("广角", "标准", "长焦")
CAMERA_LANGUAGE_PHASES = ("起幅", "中段", "落幅", "固定单帧", "姿势瞬间")
DIRECT_GAZE_RE = re.compile(
    r"\b(?:look(?:ing|s)?|gaz(?:e|es|ing)|star(?:e|es|ing))(?:\s+[\w-]+){0,3}\s+"
    r"(?:at|into|toward(?:s)?)\s+(?:the\s+)?(?:camera|lens|viewer)\b"
    r"|\beyes?\s+(?:are\s+|were\s+)?(?:turned\s+)?(?:at|toward(?:s)?)\s+(?:the\s+)?"
    r"(?:camera|lens|viewer)\b", re.I)
NEGATIVE_GAZE_RE = re.compile(
    r"不看|没看|不要看|禁止看|避免看|而非|而不是|not\s+looking|avoid\s+looking|away\s+from",
    re.I)

# SHOTLIST 固定列（与 storyboard-30s 的分镜总表共用同一份契约）
SHOTLIST_COLUMNS = ["镜", "职责", "台词", "道具进出", "生成方式", "跨镜连续物"]
GEN_WAYS = ("文生图", "首帧图生视频", "参考图定向", "不动图", "—", "无", "")
PROP_MOVE_RE = re.compile(r"[^（）()]+[（(][^（）()]*→[^（）()]*[）)]")


def read(path):
    with io.open(path, encoding="utf-8") as handle:
        return handle.read()


def skill_md(arg):
    if arg and os.path.isdir(arg):
        return os.path.join(arg, "SKILL.md")
    return arg


def _head_ok(title, pat):
    """关键词必须落在标题正文开头（去掉编号后前 10 字）。
    否则「### 4. 验收单（每个 no 抄出提示词原句）」会把提示词段抢走。"""
    head = re.sub(r"^[\d.]+\s*[.、]?\s*", "", title.strip()).strip("*（( ").replace("**", "")
    # 形如 `# prompts/S4.md` 的文件名式大标题不是段落标题，否则 "prompt" 会被误匹配
    if re.match(r"^[\w./\\-]*\.(md|txt|json|py|html)$", head, re.I):
        return False
    return bool(re.search(pat, head[:10], re.I))


def _all_headings(text):
    """[(start, end, level, title), …] 按出现顺序。"""
    out = []
    for m in re.finditer(r"^(#{1,6})[ \t]*(.+)$", text, re.M):
        out.append((m.start(), m.end(), len(m.group(1)), m.group(2)))
    return out


def _section_spans(text, pat):
    """返回全部同级语义段；正文延伸到下一个同级或更高级标题。"""
    heads = _all_headings(text)
    spans = []
    for idx, (s, e, lvl, title) in enumerate(heads):
        if not _head_ok(title, pat):
            continue
        stop = len(text)
        for ns, ne, nlvl, _t in heads[idx + 1:]:
            if nlvl <= lvl:
                stop = ns
                break
        spans.append((s, stop, text[e:stop]))
    return spans


def _section_span(text, pat):
    """兼容单段调用；正文唯一性检查必须改用 section_candidates 逐段核对。"""
    spans = _section_spans(text, pat)
    if not spans:
        return None
    s, _stop, body = max(spans, key=lambda item: len(item[2].strip()))
    return s, body


def section_candidates(text, pat):
    """返回非嵌套的同级候选段，避免父标题与子标题重复计算同一正文。"""
    selected = []
    for start, stop, body in _section_spans(text, pat):
        if selected and start < selected[-1][0]:
            continue
        selected.append((stop, body))
    return [body for _stop, body in selected]


def section(text, pat):
    r = _section_span(text, pat)
    return r[1] if r else None


def decision_text(text):
    """裁决与拆开的摘录段使用同一读取口径。"""
    return "\n".join(filter(None, [section(text, r"裁决|制作元数据"), section(text, r"从正文摘录")]))


def section_pos(text, pat):
    """第一个**有非空正文**的匹配标题位置；`# prompts/S4.md` 这种文件路径式
    大标题下面紧跟子标题、自身无正文，不会被当成提示词段起点。"""
    heads = _all_headings(text)
    for idx, (s, e, lvl, title) in enumerate(heads):
        if not _head_ok(title, pat):
            continue
        stop = len(text)
        for ns, ne, nlvl, _t in heads[idx + 1:]:
            if nlvl <= lvl:
                stop = ns
                break
        if text[e:stop].strip():
            return s
    return -1


def checklist_ids(md_text):
    """从 SKILL.md 的自检清单表抓条目号（| 0b | … |），保证验收单与技能同源。"""
    ids, seen = [], set()
    in_checklist = False
    for line in md_text.splitlines():
        if re.match(r"^#{1,6}.*(自检清单|自检)$", line):
            in_checklist = True
            continue
        if in_checklist and re.match(r"^#{1,6}", line):
            break
        if not in_checklist:
            continue
        m = re.match(r"^\|\s*([0-9]+[a-z]?[0-9]?|A[0-9]+|L[0-3]_[0-9]+)\s*\|", line)
        if m and m.group(1) not in seen:
            seen.add(m.group(1))
            ids.append(m.group(1))
    return ids


def english_bodies(section_text):
    """英文围栏可含引号内精确中文；含非引用中文的围栏属于译文而非第二正文。"""
    if not section_text:
        return []
    bodies = []
    for match in re.finditer(r"```[a-zA-Z]*\n(.*?)```", section_text, re.S):
        body = match.group(1)
        unquoted = re.sub(r'"[^"\n]*"|“[^”\n]*”|「[^」\n]*」|『[^』\n]*』', "", body)
        if re.search(r"[A-Za-z]", body) and not CJK.search(unquoted):
            bodies.append(body)
    return bodies


def bare_english(section_text, fenced):
    """提示词段里没有围栏、却有成串英文 → 裸正文（与中文混排，无法整段复制提交）。"""
    if not section_text or fenced:
        return []
    return [s for s in (l.strip() for l in section_text.splitlines())
            if len(s) > 120 and not CJK.search(s) and re.match(r"[A-Za-z]", s)]


def check_ledger(text, problems):
    """只要求实际记录的必要事实有来源，不规定十行或推测查证深度。"""
    ledger = section(text, r"账本|必要依据|依据")
    if not ledger:
        return
    rows = [line for line in ledger.splitlines()
            if line.strip().startswith("|") and not re.match(r"^\s*\|[\s\-:|]+\|\s*$", line)]
    if len(rows) < 2:
        problems.append("账本缺少必要事实与来源记录")
        return
    header = [cell.strip() for cell in rows[0].strip().strip("|").split("|")]
    source_index = next((i for i, name in enumerate(header) if "出处" in name or "来源" in name), None)
    pixel_index = next((i for i, name in enumerate(header) if any(w in name for w in ("像素", "可见", "显影"))), None)
    if source_index is None or pixel_index is None:
        problems.append("账本需要可见结果与来源列；不从备注或降级列猜出处")
        return
    for index, row in enumerate(rows[1:], 1):
        cells = [cell.strip() for cell in row.strip().strip("|").split("|")]
        if len(cells) <= max(source_index, pixel_index):
            problems.append("账本第 %d 行缺少可见结果或来源列" % index)
            continue
        if cells[pixel_index] in ("", "-", "—"):
            problems.append("账本第 %d 行可见结果空；不可见/不适用请说明范围" % index)
        if cells[source_index] in ("", "-", "—"):
            problems.append("账本第 %d 行来源/出处空；设计选择、观察和待验证须如实记录" % index)


def check_body(text, problems, warnings):
    """返回围栏内英文正文（逐字），供 main 做态度/IDENTITY 比对；检查本体仍只往
    problems/warnings 里追加。"""
    psecs = section_candidates(text, r"提示词|prompt|英文正文")
    fenced = []
    bare = []
    for psec in psecs:
        section_fenced = english_bodies(psec)
        fenced.extend(section_fenced)
        bare.extend(bare_english(psec, section_fenced))
    if len(fenced) > 1:
        problems.append("提示词段存在多个英文正文候选，必须明确唯一实际提交正文")
        return ""
    body = "\n".join(fenced)
    if bare:
        problems.append("英文正文没包在 ```text 围栏里（与中文混排，无法整段复制提交）：%s…"
                        % bare[0][:60])
    if not body.strip():
        problems.append("没有可提交的英文正文块（提示词段需要 ```text 围栏；可含引号内的精确非英文文字）")
        return ""
    for name, pat in L0_HAZARDS:
        hit = pat.search(body)
        if hit:
            warnings.append("需审读姿态/几何词面「%s」（%s）；词面不证明物理失效，按实际瞬间与支撑关系判断"
                            % (hit.group(0), name))

    for pat in BODY_NEGATIVES:
        for hit in re.finditer(pat, body, re.I):
            token = hit.group(0).lower()
            # 豁免只针对 `no X` / `no the X` 这类**排除项本身**（风格与介质缺陷合法）。
            # rather than / nothing / but not into 没有合法用法，绝不因为附近
            # 出现 "no text" 就跟着放行。
            if token.startswith("no ") or token.startswith("only ") or token.startswith("without "):
                window = body[max(0, hit.start() - 4):hit.end() + 40]
                if ALLOWED_EXCLUSIONS.search(window):
                    continue
            seg = body[max(0, hit.start() - 40):hit.end() + 40].replace("\n", " ")
            warnings.append("需审读数量/比较/否定「%s」是否符合本帧且表达清楚（…%s…）"
                            % (hit.group(0), seg.strip()[:86]))
    # 千问规则只在帧稿自己声明了千问通道时启用；没声明就不套，避免对其他通道的稿子报噪声。
    if QWEN_DECLARED_RE.search(text):
        check_qwen_style(body, warnings)
    return body


# 千问成文规则（SKILL.md「千问（Qwen-Image）成文结构」第 7/8 条与长度、排除项）。
# 全部只给 WARN：词面不证明画面失败，PASS/FAIL 语义不变。
QUALITY_WORDS_RE = re.compile(
    r"\b(?:masterpiece|8k|4k|highly\s+detailed|ultra[- ]?detailed|award[- ]winning|best\s+quality|"
    r"trending\s+on\s+artstation|hyper[- ]?realistic)\b", re.I)
ASPECT_IN_BODY_RE = re.compile(
    r"\b(?:\d{3,4}\s*[x×]\s*\d{3,4}|\d{1,2}\s*:\s*\d{1,2}\s+(?:aspect|ratio|frame|format|vertical|horizontal|portrait|landscape)|"
    r"(?:vertical|horizontal|portrait|landscape|square)\s+(?:frame|format|composition|orientation|aspect)|"
    r"aspect\s+ratio)\b", re.I)
BODY_EXCLUSION_RE = re.compile(
    r"\bno\s+(?:text|watermark|logo|caption|signature|blur|noise|jpeg|extra\s+(?:fingers|limbs|arms|hands))\b", re.I)
QWEN_WORDS_TRUNCATE = 400
QWEN_DECLARED_RE = re.compile(r"(?:通道|引擎|channel|engine)[^\n]{0,40}(?:qwen|千问)|qwen[- ]?image", re.I)


def check_qwen_style(body, warnings):
    if not body or not body.strip():
        return
    # 引号内的精确画面文字不参与质量词/画幅判断
    plain = re.sub(r'"[^"\n]*"|“[^”\n]*”', " ", body)
    hit = QUALITY_WORDS_RE.search(plain)
    if hit:
        warnings.append("正文含质量词「%s」：千问官方明令不写，且可能被画成画面文字；删掉，用具体可见描述代替" % hit.group(0))
    hit = ASPECT_IN_BODY_RE.search(plain)
    if hit:
        warnings.append("正文含画幅/分辨率词「%s」：画幅走 --size 参数，不进正文" % hit.group(0))
    excl = BODY_EXCLUSION_RE.findall(plain)
    if len(excl) >= 3:
        warnings.append("正文含 %d 项排除词（%s…）：排除项走 --negative，正文只陈述存在什么"
                        % (len(excl), "、".join(sorted(set(x.lower() for x in excl)))[:50]))
    words = len(re.findall(r"[A-Za-z]+(?:['’\-][A-Za-z]+)*", plain))
    # 只报超长：>400 词贴着 512 token 截断线，后半段可能等于没写（SKILL.md 长度段）。
    # 偏短不报：简单静帧、空镜、资产图本来就短，真实语料里偏短占绝大多数，报了没有信息量。
    if words > QWEN_WORDS_TRUNCATE:
        warnings.append("正文英文 %d 词，超过 %d 词：千问编码器约 512 token 上限（英文约 1.3 token/词），"
                        "后半段可能被截断；非千问通道可忽略" % (words, QWEN_WORDS_TRUNCATE))
    # 逗号堆叠：SD 式标签串，而不是成句的描述
    for sent in re.split(r"(?<=[.!?])\s+|\n", plain):
        parts = [x.strip() for x in sent.split(",")]
        if len(parts) >= 8 and sum(1 for x in parts if len(x.split()) <= 3) >= 6:
            warnings.append("出现逗号堆叠的标签串（「%s…」）：千问原生语体是成句描述，不是 SD 式标签" % sent.strip()[:50])
            break


def _composition_fields(raw, owner, required, problems):
    """Parse full-width bar separated key:value fields without guessing blanks."""
    fields = {}
    for part in raw.split("｜"):
        if "：" not in part:
            problems.append("%s 的字段缺少全角冒号：%s" % (owner, part.strip()))
            continue
        key, value = part.split("：", 1)
        key, value = key.strip(), value.strip()
        if key in fields:
            problems.append("%s 的字段重复：%s" % (owner, key))
        fields[key] = value
    for key in required:
        if not fields.get(key):
            problems.append("%s 缺少 %s" % (owner, key))
    return fields


def _require_english_anchor(fields, key, owner, body, problems):
    anchor = fields.get(key, "")
    if not anchor:
        return
    if CJK.search(anchor):
        problems.append("%s 的 %s 必须是可逐字投影到正文的英文锚点" % (owner, key))
    if re.sub(r"\s+", " ", anchor) not in re.sub(r"\s+", " ", body):
        problems.append("%s 的 %s 没有逐字进入实际英文正文：%s" % (owner, key, anchor))


def check_camera_language(text, problems, required=False):
    """镜头静帧需要七项取景字段；普通静帧/资产不要求，已提供则检查结构。

    「中景」「特写」单独一个词不算完成；七项分别是景别、水平角度（轴线侧/
    无轴线）、机位高度、焦段意图、构图、焦点、帧相位。锚点只投影分镜已接受
    的事实，不能在同一行里新增人物位置、朝向或动作。
    """
    decision = decision_text(text)
    hits = list(CAMERA_LANGUAGE_RE.finditer(decision))
    if not hits and not required:
        return
    if len(hits) != 1:
        problems.append(
            "镜头静帧裁决必须且只能有一条「镜头语言：…」七项取景字段；实际为 %d 条" % len(hits)
        )
        return
    raw = hits[0].group(1).strip()
    parts = [part.strip() for part in raw.split("｜")]
    if len(parts) != len(CAMERA_LANGUAGE_SLOTS):
        problems.append("镜头语言必须正好七项（实际 %d 项）：%s" % (len(parts), raw[:120]))
        return
    values = []
    for index, (slot, part) in enumerate(zip(CAMERA_LANGUAGE_SLOTS, parts)):
        if index < 4:
            value = part
        else:
            prefix = slot + "："
            if not part.startswith(prefix):
                problems.append("镜头语言第 %d 项缺少「%s」" % (index + 1, prefix))
                value = ""
            else:
                value = part[len(prefix):].strip()
        if not value:
            problems.append("镜头语言「%s」为空" % slot)
        values.append(value)
    # 只验证结构与明显错栏，不以词长/固定摄影词表裁定语义。
    if len(values) == 7 and NEGATIVE_GAZE_RE.search(values[1]):
        problems.append("镜头语言水平角度混入了否定式视线；朝向和视线分别记录")


def check_composition_locks(text, body, problems, frame_kind="keyframe", audit="full", modules=None):
    """按帧型/风险核对机位与逐人关系；实际存在的锚点始终校验。"""
    modules = set(modules or ())
    decision = decision_text(text)
    has_people = bool(PERSON_MARKERS.search(body) or PERSON_COMPOSITION_RE.search(decision))
    # 人物词只决定是否要求补字段；已提供的锚点和显式风险契约始终核对。
    cameras = list(CAMERA_LOCK_RE.finditer(decision))
    people = list(PERSON_COMPOSITION_RE.finditer(decision))
    if frame_kind == "keyframe" or (audit == "full" and has_people):
        if len(cameras) != 1:
            problems.append("该机位审计必须且只能有一条「机位锁」；实际为 %d 条" % len(cameras))
    if has_people and (audit == "full" or "multi" in modules or frame_kind == "keyframe"):
        if not people:
            problems.append("该人物审计缺少「人物构图」；每个可见人物各写一条，脸/眼不可见也要显式登记")
    if "multi" in modules:
        declared_match = re.search(r"^(?:[-*+]\s*)?出场[：:]\s*([^\n]+)$", decision, re.M)
        declared = {name.strip() for name in re.split(r"[,，、]", declared_match.group(1)) if name.strip()} if declared_match else set()
        locked = {match.group(1).strip() for match in people}
        if not declared:
            problems.append("multi 审计须用「出场：甲,乙」登记本帧全部可见人物")
        elif declared != locked:
            problems.append("multi 出场与人物构图不一致：出场=%s；构图=%s" % (
                ",".join(sorted(declared)), ",".join(sorted(locked))))
    for match in cameras:
        owner = "机位锁"
        fields = _composition_fields(match.group(1), owner, ("位置", "camera_en"), problems)
        anchor = fields.get("camera_en", "")
        if anchor.upper() == "NA":
            note = fields.get("位置", "")
            if frame_kind == "keyframe":
                problems.append("镜头静帧的 camera_en 不能为NA；须沿用上游实际取景")
            elif not any(word in note for word in ("非必要", "无需", "未指定", "只要求")):
                problems.append("普通静帧的 camera_en=NA 须说明未指定且非必要的原因")
        else:
            _require_english_anchor(fields, "camera_en", owner, body, problems)
    seen = set()
    intentional_direct_gaze = False
    for match in people:
        name = match.group(1).strip()
        owner = "人物构图「%s」" % name
        if name in seen:
            problems.append("%s 重复；同一人物只能有一条构图与视线锁" % owner)
        seen.add(name)
        fields = _composition_fields(
            match.group(2), owner,
            ("身体", "头部", "视线目标", "body_en", "head_en", "gaze_en"), problems)
        target = fields.get("视线目标", "")
        if NEGATIVE_GAZE_RE.search(target):
            problems.append("%s 的视线目标只有否定/排除：%s；必须写实际看向的唯一对象" % (owner, target))
        direct_intent = "镜头" in target and "有意直视：" in target
        if "镜头" in target and not direct_intent:
            problems.append("%s 把镜头作为视线目标，但没有写明（有意直视：<叙事理由>）" % owner)
        if direct_intent:
            intentional_direct_gaze = True
        if DIRECT_GAZE_RE.search(fields.get("gaze_en", "")) and not direct_intent:
            problems.append("%s 的 gaze_en 直视镜头/观众，但该人物没有有意直视裁决" % owner)
        for key, fact in (("body_en", "身体"), ("head_en", "头部"), ("gaze_en", "视线目标")):
            if fields.get(key, "").upper() == "NA":
                note = fields.get(fact, "")
                has_unseen_reason = any(word in note for word in ("不可见", "框外", "背向", "裁切"))
                has_nonessential_reason = any(word in note for word in ("非必要", "无需", "未指定", "只要求"))
                if not note or not (has_unseen_reason or has_nonessential_reason):
                    problems.append("%s 的 %s 为NA，但%s没有不可见或非必要的原因" % (owner, key, fact))
                continue
            _require_english_anchor(fields, key, owner, body, problems)
    if DIRECT_GAZE_RE.search(body) and not intentional_direct_gaze:
        problems.append("英文正文出现直视镜头/观众，但裁决没有「视线目标：镜头（有意直视：<叙事理由>）」")


def parse_verdict(cell):
    """从一格读出结论。技能允许两种写法：
      独立结论列  ->  `yes` / `no` / `NA`
      结论＋理由同格 ->  `NA：本镜没有窗` / `no（不适用）` / `yes（部分）`
    返回 (token, inline_reason) 或 None。"""
    v = cell.strip().strip("*` ").lower()
    if not v:
        return None
    m = re.match(r"^(yes|no|na|n/a|不适用|部分)(?=$|[\s（(：:、,，).。-])", v)
    if not m:
        return None
    token = m.group(1)
    if token == "n/a":
        token = "na"
    rest = v[m.end():].strip(" \t（）()：:、,，.。-*`")
    return token, rest


def check_acceptance(text, skill_path, problems, audit="full", modules=None):
    """core按风险模块选项；full答全表，已填写的其它项仍全部校验。"""
    modules = set(modules or ())

    if not skill_path:
        return {}
    ids = checklist_ids(read(skill_path))
    if not ids:
        problems.append("闸门无法从 SKILL.md 解析出自检清单条目号（技能章节标题与脚本脱节），"
                        "本次无法校验验收单完整性 —— 修脚本或改标题，不许当作通过")
    block = section(text, r"验收单|自检(清单)?|文字核对表") or ""
    answered = {}
    for line in block.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2 or not ID_RE.match(cells[0]):
            continue
        cid = cells[0]
        # 结论列位置不固定：模板四列 = #|检查项|结论|证据，实际也写成三列
        # #|结论|证据，甚至"NA：理由"同格。取第一个读得出结论的格。
        vi, parsed = None, None
        for k in range(1, len(cells)):
            got = parse_verdict(cells[k])
            if got:
                vi, parsed = k, got
                break
        if parsed is None:
            problems.append("验收单第 %s 条没给出结论（要写 yes / no / NA，"
                            "不适用也要写明 NA＋理由，留空与漏审无法区分）" % cid)
            continue
        verdict, inline_reason = parsed
        if cid in answered:
            problems.append("验收单第 %s 条重复，不能覆盖前一结论" % cid)
        answered[cid] = verdict
        why = " ".join(cells[vi + 1:]).strip() or inline_reason
        if verdict == "na" and not why:
            problems.append("验收单第 %s 条NA缺少适用性理由" % cid)
        if verdict == "no":
            if cid in ("L0_1", "L0_2", "L0_3", "L0_4"):
                problems.append("【L0 一票否决】验收单第 %s 条判 no；证据完整或冻结帧备案均不能放行" % cid)
            if not why or why in ("略", "见正文", "见第3节"):
                problems.append("验收单第 %s 条判 no 却没有具体证据或缺失原因" % cid)
    if ids:
        required = set(CORE_CHECKLIST_IDS)
        for module in modules:
            required.update(RISK_CHECKLIST_IDS.get(module, ()))
        required_ids = list(ids) if audit == "full" else [i for i in ids if i in required]
        missing = [i for i in required_ids if i not in answered]
        if missing:
            problems.append("%s 验收单漏答 %d 条：%s（不适用的也要写 NA＋理由）"
                            % (audit, len(missing), ", ".join(missing[:14])))
    if not answered:
        problems.append("验收单没有逐条 yes/no/NA（表格没填 = 没自审）")
    return answered


# ---- --project 项目级三件套契约（v1.4.0） ----


def _norm_ws(s):
    """空白归一化：所有连续空白压成一个空格，供逐字包含判断。"""
    return re.sub(r"\s+", " ", s).strip()


def check_project(text, frame_file, project, body, problems, warnings, identity_path=None, shotlist_path=None, independent=True):
    """项目级硬契约，传了 --project 就必须全满足，任何一项不过 = FAIL。
    a. SHOTLIST.md：存在、固定六列、本帧号已登记、道具进出格式、生成方式取值；
    b. 所选权威身份锚点必须在正文中逐字存在。
    independent=False时只核对显式传入的来源，不要求创建独立项目布局。"""
    # --- SHOTLIST ---
    sl_path = shotlist_path or (os.path.join(project, "SHOTLIST.md") if independent else None)
    if sl_path and not os.path.isfile(sl_path):
        problems.append("项目级契约 a 失守：%s 不存在（先写分镜总表再写帧词，顺序不可颠倒）" % sl_path)
    elif sl_path:
        sl = read(sl_path)
        header_line = next((l for l in sl.splitlines() if l.strip().startswith("|")), "")
        header_cells = [c.strip() for c in header_line.strip().strip("|").split("|")]
        for col in SHOTLIST_COLUMNS:
            if col not in header_cells:
                problems.append("SHOTLIST.md 列头缺「%s」（固定六列：%s）"
                                % (col, " / ".join(SHOTLIST_COLUMNS)))
        stem = os.path.splitext(os.path.basename(frame_file))[0]
        frame_id = stem
        rows = [l for l in sl.splitlines() if l.strip().startswith("|")
                and not re.match(r"^\s*\|[\s\-:|]+\|\s*$", l)]
        mine = None
        for r in rows[1:]:
            cells = [c.strip() for c in r.strip().strip("|").split("|")]
            if cells and cells[0] == frame_id:
                mine = cells
                break
        if mine is None:
            problems.append("SHOTLIST.md 没有登记本镜 %s（帧号取自文件名；未登记 = 这镜不在分镜里）" % frame_id)
        else:
            def col(name):
                return mine[header_cells.index(name)] if name in header_cells and header_cells.index(name) < len(mine) else ""
            pm = col("道具进出")
            if pm and pm not in ("—", "-", "无"):
                # 先抠出所有合规的 名（进→退） 段，剩下的只允许分隔符（顿号/逗号/空白）——
                # 不能先按逗号切再逐段验：说明性后缀「（S1→S1，袋内）」里的逗号不是分项符。
                rest = PROP_MOVE_RE.sub("", pm)
                if rest.strip("、，,;； \t"):
                    problems.append("SHOTLIST 道具进出格式不合规：「%s」要求逐项 名（进场镜→退场镜），"
                                    "残余无法解析：「%s」" % (pm, rest.strip()[:60]))
            gw = col("生成方式")
            if gw not in GEN_WAYS:
                problems.append("SHOTLIST 生成方式取值非法：「%s」（合法值：文生图 / 首帧图生视频 / 参考图定向 / 不动图）" % gw)

    # --- IDENTITY ---
    # 契约：IDENTITY.md 每个角色段落在 ```text 围栏里；段落下方的
    # `> presence: 词1, 词2` 行声明出场标记（正文命中任一标记 = 该角色在本镜，
    # 身份段必须逐字出现）。没声明 presence 的段落 = 每一镜都必须出现。
    id_path = identity_path or (os.path.join(project, "prompts", "IDENTITY.md") if independent else None)
    if id_path and not os.path.isfile(id_path):
        problems.append("项目级契约 b 失守：%s 不存在（身份段唯一权威文件）" % id_path)
    elif id_path and body:
        check_identity_views(read(id_path), body, decision_text(text), problems)


def check_identity_views(id_text, body, decision, problems):
    """默认逐字核对完整身份；显式视角仅能选用同一权威库已登记的锚点。"""
    records = identity_records(id_text)
    if not records:
        problems.append("身份库没有可核验的英文 text 锚点，不能将空检查当作通过")
        return
    library = {}
    for key, view, seg, markers in records:
        if not markers:
            problems.append("身份 %s 缺少 presence 出场标记，不能在未点名时默认必入每帧" % key)
        library.setdefault(key.casefold(), []).append((view, seg, markers))
    choices = {}
    for key, view in re.findall(r"^身份视图[：:]\s*([^=\n]+)=\s*([^\s=]+)\s*$", decision, re.M):
        key, view = key.strip().casefold(), view.casefold()
        if key in choices:
            problems.append("身份视图重复声明：%s" % key)
        choices[key] = view
        if key not in library:
            problems.append("身份视图引用未登记角色：%s" % key)
    norm_body = _norm_ws(body)
    for key, records in library.items():
        full = [r for r in records if r[0] == "full"]
        if not full:
            problems.append("身份视图库缺少 full 基线：%s" % key)
            continue
        markers = [m for _v, _s, ms in full for m in ms] + [key]
        if key not in choices and not any(
                re.search(r"\b%s\b" % re.escape(m), body, re.I) for m in markers):
            continue
        view = choices.get(key, "full")
        selected = [r for r in records if r[0] == view]
        if not selected:
            problems.append("身份视图未在 IDENTITY.md 登记：%s=%s" % (key, view))
            continue
        for _view, seg, _markers in selected:
            if _norm_ws(seg) not in norm_body:
                probe = " ".join(_norm_ws(seg).split()[:12])
                problems.append("身份段与 IDENTITY.md 不一致：%s=%s 缺少「%s…」；"
                                "使用权威库对应锚点，不能借视角声明改衣换脸" % (key, view, probe[:120]))


def identity_records(id_text):
    """角色标题拥有身份；子标题注册同一角色的可见视角，库总标题不产身份。"""
    out = []
    heads = _all_headings(id_text)
    parent_key = ""
    parent_markers = []
    for idx, (_start, end, level, title) in enumerate(heads):
        stop = heads[idx + 1][0] if idx + 1 < len(heads) else len(id_text)
        block = id_text[end:stop]
        def tag(name):
            hit = re.search(r"^>\s*%s\s*[:：]\s*(.+)$" % name, block, re.M | re.I)
            return hit.group(1).strip() if hit else ""
        own_markers = [w.strip() for w in re.split(r"[,，、]", tag("presence")) if w.strip()]
        explicit_key = tag("identity")
        view = tag("view").casefold() or "full"
        if view == "full" and not explicit_key:
            parent_key = title.strip()
            parent_markers = own_markers
        key = explicit_key or parent_key or (own_markers[0] if own_markers else title.strip())
        markers = own_markers or parent_markers
        for seg in english_bodies(block):
            out.append((key, view, seg, markers))
    return out


def identity_segments(id_text):
    """保留原接口：返回完整身份段和出场标记，视角子段不作为完整身份。"""
    return [(seg, markers) for _key, view, seg, markers in identity_records(id_text) if view == "full"]


def resolve_audit(text, frame_kind, requested=None, requested_risks=None):
    """CLI是风险下限；文稿结构可升级，keyframe始终启用帧型模块。"""
    decision = decision_text(text)
    declared = re.search(r"(?:审计档位|审计)[：:]\s*(core|full)\b", decision, re.I)
    audit = requested or (declared.group(1).lower() if declared else None)
    if declared and requested and audit != declared.group(1).lower():
        raise ValueError("--audit与裁决中的审计档位冲突")
    risk_match = re.search(r"^(?:[-*+]\s*)?风险[：:]\s*([^\n]+)$", decision, re.M)
    risks = set(requested_risks or ())
    if risk_match:
        risks.update(x.strip() for x in re.split(r"[,，、\s]+", risk_match.group(1)) if x.strip())
    unknown = risks - set(RISK_KINDS)
    if unknown:
        raise ValueError("未知风险模块：" + ",".join(sorted(unknown)))
    if frame_kind == "keyframe":
        risks.add("keyframe")
    if not audit:
        block = section(text, r"验收单|自检(清单)?|文字核对表") or ""
        answered = set(re.findall(r"^\|\s*(L[0-3]_[0-9]+|0c|0f|5b|6c|7|9|12|13|14|15|16)\s*\|", block, re.M))
        audit = "full" if len(answered) == 15 else "core"
    if re.search(r"出场[：:]", decision) or (audit != "full" and len(PERSON_COMPOSITION_RE.findall(decision)) > 1):
        risks.add("multi")
    if re.search(r"文字契约[：:]", decision):
        risks.add("exact_text")
    if re.search(r"接触契约[：:]", decision):
        risks.add("contact")
    return audit, risks


def check_risk_contracts(text, body, modules, problems):
    """精确文字逐字核对；接触关系保留实例/部位/可见性供语义审读。"""
    decision = decision_text(text)
    if "exact_text" in modules:
        hits = re.findall(r"^[-*+]\s*文字契约[：:]([^\n]+)$", decision, re.M)
        if not hits:
            problems.append("exact_text 审计缺少「文字契约」")
        for raw in hits:
            contract_id, separator, field_text = raw.partition("｜")
            if not separator or not contract_id.strip():
                problems.append("文字契约需要ID与字段：ID｜exact：…")
                continue
            fields = _composition_fields(field_text, "文字契约", ("exact",), problems)
            exact = fields.get("exact", "")
            if exact and exact not in body:
                problems.append("精确文字没有逐字进入英文正文：%s" % exact)
    if "contact" in modules:
        hits = re.findall(r"^[-*+]\s*接触契约[：:]([^\n]+)$", decision, re.M)
        if not hits:
            problems.append("contact 审计缺少「接触契约」")
        for raw in hits:
            contract_id, separator, field_text = raw.partition("｜")
            if not separator or not contract_id.strip():
                problems.append("接触契约需要ID与字段：ID｜主体：…｜对象：…")
                continue
            fields = _composition_fields(field_text, "接触契约", ("主体", "对象", "关系", "可见性"), problems)
            if fields.get("可见性") in ("不可见", "未指定") and "NA" not in raw and "非必要" not in raw:
                problems.append("关键接触的可见性不可缺省；不可见须标NA并回上游确认是否影响制作")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frame_file")
    parser.add_argument("--strict", action="store_true")
    parser.add_argument("--skill")
    parser.add_argument("--project")
    parser.add_argument("--identity")
    parser.add_argument("--shotlist")
    parser.add_argument("--frame-kind", choices=("still", "keyframe", "asset"))
    parser.add_argument("--audit", choices=AUDIT_PROFILES)
    parser.add_argument("--risk", action="append", choices=RISK_KINDS, default=[])
    args = parser.parse_args()
    frame_file, strict, skill_arg, project = args.frame_file, args.strict, args.skill, args.project

    if not os.path.exists(frame_file):
        print("FAIL  帧文件不存在：%s" % frame_file)
        return 1
    if project and not os.path.isdir(project):
        print("FAIL  --project 指向的目录不存在：%s" % project)
        return 1
    text = read(frame_file)
    problems, warnings = [], []

    for name, pat in REQUIRED_SECTIONS:
        if section_pos(text, pat) < 0:
            problems.append("缺「%s」段（没有以它开头的标题）" % name)

    check_ledger(text, problems)
    body = check_body(text, problems, warnings)
    decision = decision_text(text)
    declared = re.search(r"帧类型[：:]\s*([A-Za-z]+)", decision)
    frame_kind = args.frame_kind or (declared.group(1) if declared else "still")
    if frame_kind not in ("still", "keyframe", "asset"):
        problems.append("未知帧类型：%s" % frame_kind)
    if declared and args.frame_kind and frame_kind != declared.group(1):
        problems.append("--frame-kind与裁决中的帧类型冲突")
    try:
        audit, modules = resolve_audit(text, frame_kind, args.audit, args.risk)
    except ValueError as error:
        print("FAIL  " + str(error))
        return 1
    if frame_kind == "keyframe" and not re.search(r"(?:\brole|用途)\s*[：:]\s*(?:composition|start|pose_proof|end|构图|起始帧|姿势|终点)\b", decision, re.I):
        problems.append("镜头静帧须在裁决中明确 role/用途：composition/start/pose_proof/end")
    check_camera_language(text, problems, required=frame_kind == "keyframe")
    check_composition_locks(text, body, problems, frame_kind=frame_kind, audit=audit, modules=modules)
    check_risk_contracts(text, body, modules, problems)

    skill_path = skill_md(skill_arg) if skill_arg else None
    if skill_arg and (not skill_path or not os.path.exists(skill_path)):
        # 显式指定了技能目录却解析不到 SKILL.md：绝不静默换一份清单来判，
        # 否则"用哪版规格校验"会漂移，PASS 就失去意义。
        print("FAIL  --skill 指向的路径里没有 SKILL.md：%s" % skill_arg)
        return 1
    if not skill_path or not os.path.exists(skill_path):
        cand = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "SKILL.md")
        skill_path = cand if os.path.exists(cand) else None
    answered = {}
    if skill_path:
        answered = check_acceptance(text, skill_path, problems, audit=audit, modules=modules)
    else:
        warnings.append("找不到 SKILL.md，跳过验收单条目完整性比对（用 --skill 指定技能目录）")

    i_ledger = section_pos(text, r"账本|必要依据|依据")
    i_prompt = section_pos(text, r"提示词|prompt|英文正文")
    if i_ledger >= 0 and i_prompt >= 0 and i_ledger > i_prompt:
        problems.append("画外账本写在提示词之后 —— 顺序反了，等于先写词再补表")

    identity_path, shotlist_path = args.identity, args.shotlist
    if project or identity_path or shotlist_path:
        check_project(text, frame_file, project or os.path.dirname(os.path.abspath(frame_file)), body,
                      problems, warnings, identity_path, shotlist_path, independent=bool(project))

    print("== %s ==" % os.path.basename(frame_file))
    print("PROFILE frame_kind=%s audit=%s modules=%s frame_kind_source=%s" % (
        frame_kind, audit, ",".join(sorted(modules)) or "none",
        "cli" if args.frame_kind else ("document" if declared else "assumed")))
    for p in problems:
        print("FAIL  " + p)
    for w in warnings:
        print("WARN  " + w)
    if problems:
        print("GATE_STATUS=FAIL")
        print("\n共 %d 个结构/引用问题；须处理或明确核对适用性，脚本不裁定生产授权。" % len(problems))
        return 1
    print("CHECKS_RUN %s%s" % (audit, "+" + "+".join(sorted(modules)) if modules else ""))
    print("CHECKS_SKIPPED 未选择的可选风险模块；未声明不等于不存在风险")
    print("GATE_STATUS=PASS")
    print("PASS  本次声明范围内的结构与引用检查未发现错误。")
    print("NOT_EVALUATED  事实真实性、完整人数、表演、自然成文、画风与生成效果；需审读/实看。")
    if strict and warnings:
        print("REVIEW_REQUIRED  --strict：存在需人工审读提示，不能用凑词清除。")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
