#!/usr/bin/env python3
"""check_references.py — 校验公开文档里的路径引用。

范围：仓库内全部 .md 文档（含 SKILL.md、references/、根文档、语料、实测记录与索引）。

对每条引用（markdown 链接与反引号路径）依次尝试：
  1. 相对所在文件目录解析；
  2. 相对仓库根解析；
  3. 文件名在全仓**唯一**匹配（同名多于一个视为断链，需写清相对路径）。
三者都失败 → 断链。

跳过（不算引用）：
  - 命令行示例（含空格 / 解释器开头）、URL、环境变量、通配符；
  - 渲染机占位符（<...>、Windows 盘符）；
  - 项目产物路径（剧集/审查/设定集/项目开发/... 等现场生成的文件）；
  - 无斜杠的裸文件名（正文提及，非链接）；
  - .gitignore 排除的文件（按根目录 .gitignore 的简单 glob 规则解析）。

用法：python3 scripts/check_references.py   （退出码 0 = 无断链）
"""
import fnmatch
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXTS = {'.md', '.py', '.json', '.txt', '.sh', '.ps1', '.yml', '.yaml', '.jsonl',
        '.gz', '.zip', '.tar', '.7z', '.csv'}

SKIP_DIR = {'.git', '__pycache__', '.pytest_cache', 'node_modules'}

# 项目产物 / 现场生成文件：不检查
# 历史档（MEASURED- / HANDOFF- / 结论-）：整体豁免链接检查。
# 理由：这些档保留当时的仓外/私有路径原貌（/tmp/*、ep01_v4/*、创作者决策/* 等），
# 随文档改写会破坏史料。
# CHANGELOG 不再整份豁免：它的条目照抄了当时的仓内路径，错一个前缀读者就跟丢；
# 历史条目按「写入时的事实」对待，但仍要求指向本仓真实存在的文件（或明确标注仓外）。
ARCHIVE_DOC = re.compile(r'(MEASURED-|HANDOFF-|结论-)')
# 上游 vendored 仓库有意未收录的夹具目录（引用有效于上游、本仓豁免）
UPSTREAM_FITTURE = re.compile(
    r'^(\.\./)*(examples|evaluations|tests|tools|\.clawhub|\.agents|\.config|\.short-drama|'
    r'\.release|Delivery|delivery)/'
)
# T8 语料卡：上游原文逐字收录（卡片头注明来源），其内部路径属上游结构。
T8_CORPUS = re.compile(r'h3-prompt-writing.corpus.creative-dna-t8.(cards|cards-community|cases)/')
# 根级豁免：除逐字收录的语料卡，此正则实际也命中本地检索台账 INDEX.md /
# MASTER-INDEX.md / PRODUCTION-INTEGRATION.md。三者由本仓维护，正文按上游原文列出
# 其声明为死链的路径作阅读说明（references/summary.md、references/template.md、
# ../creative-dna.json），属文档内容而非待解析引用；移出豁免实测新增 3 处此类误报，
# 故一并覆盖。
T8_ROOT_CARDS = re.compile(r'h3-prompt-writing.corpus.creative-dna-t8.[^.]+\.md$')

PROJECT_ARTIFACT = re.compile(
    r'^(剧集|审查|设定集|项目开发|制作成果|交付|输入|关键帧|创作文档|文档|素材|'
    r'剧本|视觉设定|导演|分镜|图片提示词|视频提示词|剪辑单|场记|白模|MEASURED-|'
    r'bgm/|镜头表/|片段/|画布/|原始资料/|chapters/|h3-demo-repro/|design-system/)'
)
# 正文里未加反引号的裸路径（形如 a/b/c.md，前后不是标识符字符）。
# 这类写法同样会误导读者，必须一并解析；早期版本只看反引号与链接，
# 「来源：workbench/skills/x.md」这种整句裸路径因此全被漏掉。
BARE_PATH = re.compile(
    r'(?<![\w`/.\-\[])((?:[A-Za-z0-9_.\-]+/)+[A-Za-z0-9_.\-]+\.(?:'
    + '|'.join(e[1:] for e in EXTS) + r'))(?![\w`)\]])'
)
# 渲染机占位符与外部环境
PLACEHOLDER = re.compile(r'^[<$_~]|^[A-Za-z]:[\\/]|^https?://|^ftp://')

# markdown 链接目标
LINK = re.compile(r'\]\(([^)\s]+)\)')
# 反引号内容（任意内容，逐个 token 解析）
BACKTICK = re.compile(r'`([^`\n]+)`')
# 命令示例里的单个路径 token（含斜杠、以已知扩展名结尾）。
# 含空格的整段命令不做整段解析，但其中每个路径 token 必须逐个解析——
# 早期版本整段跳过含空格的内容，命令行里的错误路径因此全部漏检。
PATH_TOKEN = re.compile(
    r'(?<![\w/.-])([A-Za-z0-9_.\-]+(?:/[A-Za-z0-9_.\-]*)*\.(?:'
    + '|'.join(e[1:] for e in EXTS) + r'))(?![\w])'
)


def load_ignore_patterns():
    """读取根 .gitignore：注释/空行忽略，末尾斜杠按目录前缀匹配，其余按 fnmatch。"""
    path = os.path.join(ROOT, '.gitignore')
    if not os.path.exists(path):
        return []
    patterns = []
    with open(path, encoding='utf-8') as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patterns.append(line)
    return patterns


def is_ignored(rel, dirs, patterns):
    """判断相对路径 rel 是否命中 .gitignore。规则按「后规则优先」：
    从最后一条往前找，第一条匹配（含 ! 否定）即决定结果。"""
    for pat in reversed(patterns):
        neg = pat.startswith('!')
        p = pat[1:] if neg else pat
        if not p:
            continue
        p = p.lstrip('/')
        if p.endswith('/'):
            hit = rel == p.rstrip('/') or rel.startswith(p)
        elif '/' in p:
            hit = fnmatch.fnmatch(rel, p)
        else:
            hit = any(fnmatch.fnmatch(part, p) for part in dirs + [os.path.basename(rel)])
        if hit:
            return not neg
    return False


ignore_patterns = load_ignore_patterns()
all_files = set()
for dirpath, dirnames, filenames in os.walk(ROOT):
    dirnames[:] = [d for d in dirnames if d not in SKIP_DIR]
    for name in filenames:
        rel = os.path.relpath(os.path.join(dirpath, name), ROOT)
        parts = rel.split(os.sep)
        if is_ignored(rel, parts[:-1], ignore_patterns):
            continue
        all_files.add(rel)


def in_scope(rel):
    """检查范围 = 仓库内全部 .md 文档（SKILL.md、references/、根文档、
    语料与实测记录等一律纳入；跳过规则负责排除命令示例与占位符）。"""
    return True


basename_index = defaultdict(list)
for rel in all_files:
    basename_index[os.path.basename(rel)].append(rel)

broken = []
checked = 0
for rel in sorted(all_files):
    if not rel.endswith('.md') or not in_scope(rel):
        continue
    if ARCHIVE_DOC.search(rel):
        continue
    if T8_CORPUS.search(rel) or T8_ROOT_CARDS.match(rel):
        continue
    dirn = os.path.dirname(rel)
    with open(os.path.join(ROOT, rel), encoding='utf-8') as fh:
        text = fh.read()
    for lineno, line in enumerate(text.splitlines(), 1):
        refs = []          # markdown 链接 + 反引号里的每个路径 token
        for m in LINK.finditer(line):
            ref = m.group(1)
            # 链接可能带页内锚点（file.md#section）：校验时只看文件部分。
            # 不剥离会让每个带锚点的链接都被判成断链（纯工具误报）。
            refs.append(ref.split('#', 1)[0])
        for m in BACKTICK.finditer(line):
            inner = m.group(1)
            if inner.startswith(('http://', 'https://', 'ftp://')):
                continue
            # 反引号内容一律按路径 token 逐个解析——不要求「整段以扩展名结尾」。
            # 早期只匹配「整段就是一条路径」的写法，`python x.py a/b.txt --refs 3`
            # 这类以参数结尾的命令整段被漏掉，其中的错误路径因此全部逃检。
            refs.extend(t.group(1) for t in PATH_TOKEN.finditer(inner))
        # 正文裸路径：抹掉反引号内容、链接目标与 URL 后，剩下的路径写法也要解析
        plain = re.sub(r'`[^`]*`', ' ', line)
        plain = re.sub(r'\]\([^)]*\)', ' ', plain)
        plain = re.sub(r'https?://\S+', ' ', plain)
        refs.extend(m.group(1) for m in BARE_PATH.finditer(plain))
        for ref in refs:
            checked += 1
            if ('*' in ref or '\\' in ref or '<' in ref or '>' in ref
                    or '{' in ref
                    or PLACEHOLDER.match(ref) or PROJECT_ARTIFACT.match(ref)
                    or '/' not in ref):
                continue
            if rel.startswith('drama-skills') and UPSTREAM_FITTURE.match(ref):
                continue
            if os.path.exists(os.path.join(ROOT, dirn, ref)):
                continue
            norm = os.path.normpath(ref)
            if norm in all_files:
                continue
            # 套件根相对：drama-skills 文档里以技能名为首段的路径，实际在 drama-skills/skills/ 下
            suite_ref = os.path.join('drama-skills', 'skills', norm)
            if suite_ref in all_files:
                continue
            # 带套件容器前缀的写法：skills/<...> → drama-skills/skills/<...>
            if norm.startswith('skills/'):
                if os.path.join('drama-skills', norm) in all_files:
                    continue
            # CHANGELOG 等档里的技能相对写法（short-drama-write/SKILL.md）
            if os.path.join('drama-skills', 'skills', norm) in all_files:
                continue
            # 不再做 basename 兜底：它会把「目录写错、文件名恰好唯一」的引用
            # 误判为有效（曾掩盖 21 处 workbench/skills/*.md 错目录）。正文里
            # 无斜杠的裸文件名已在上面跳过，不依赖这条兜底。
            broken.append(f"{rel}:{lineno}  {ref}")

print(f"检查引用 {checked} 条，断链 {len(broken)} 处")
for b in broken:
    print("  " + b)
sys.exit(1 if broken else 0)
