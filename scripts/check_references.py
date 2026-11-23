#!/usr/bin/env python3
"""check_references.py — 校验公开文档里的路径引用。

范围：所有 SKILL.md、所有 references/ 下的文档、仓库根文档（AGENTS.md / SHORT-DRAMA-ROUTING.md / README.md）。

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

EXTS = {'.md', '.py', '.json', '.txt', '.sh', '.ps1', '.yml', '.yaml', '.jsonl'}

SKIP_DIR = {'.git', '__pycache__', '.pytest_cache', 'node_modules'}

# 项目产物 / 现场生成文件：不检查
PROJECT_ARTIFACT = re.compile(
    r'^(剧集|审查|设定集|项目开发|制作成果|交付|输入|关键帧|创作文档|文档|素材|'
    r'剧本|视觉设定|导演|分镜|图片提示词|视频提示词|剪辑单|场记|白模|MEASURED-|'
    r'bgm/|镜头表/|片段/|画布/|原始资料/|chapters/|h3-demo-repro/|design-system/)'
)
# 渲染机占位符与外部环境
PLACEHOLDER = re.compile(r'^[<$_~]|^[A-Za-z]:[\\/]|^https?://|^ftp://')

CANDIDATE = re.compile(
    r'`([^`\n]+?\.(?:' + '|'.join(e[1:] for e in EXTS) + r'))`'
    r'|\]\(([^)\s]+\.(?:' + '|'.join(e[1:] for e in EXTS) + r'))\)'
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
    """判断相对路径 rel 是否命中任一 .gitignore 规则。"""
    for pat in patterns:
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
    parts = rel.split(os.sep)
    if rel in ('AGENTS.md', 'SHORT-DRAMA-ROUTING.md', 'README.md'):
        return True
    if parts[-1] == 'SKILL.md':
        return True
    return 'references' in parts


basename_index = defaultdict(list)
for rel in all_files:
    basename_index[os.path.basename(rel)].append(rel)

broken = []
checked = 0
for rel in sorted(all_files):
    if not rel.endswith('.md') or not in_scope(rel):
        continue
    dirn = os.path.dirname(rel)
    with open(os.path.join(ROOT, rel), encoding='utf-8') as fh:
        text = fh.read()
    for lineno, line in enumerate(text.splitlines(), 1):
        for m in CANDIDATE.finditer(line):
            ref = m.group(1) or m.group(2)
            checked += 1
            if (' ' in ref or '*' in ref or '\\' in ref or '<' in ref or '>' in ref
                    or PLACEHOLDER.match(ref) or PROJECT_ARTIFACT.match(ref)
                    or '/' not in ref):
                continue
            if os.path.exists(os.path.join(ROOT, dirn, ref)):
                continue
            norm = os.path.normpath(ref)
            if norm in all_files:
                continue
            if len(basename_index.get(os.path.basename(ref), [])) == 1:
                continue
            broken.append(f"{rel}:{lineno}  {ref}")

print(f"检查引用 {checked} 条，断链 {len(broken)} 处")
for b in broken:
    print("  " + b)
sys.exit(1 if broken else 0)
