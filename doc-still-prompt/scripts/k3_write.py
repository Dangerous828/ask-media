#!/usr/bin/env python3
"""可选静帧写词器：按任务选材，完整响应才写稿，结构检查不授权生产。

用法：python3 k3_write.py --frame S4 --duty '本帧任务' --project <项目> -o <帧稿>
      --style live-action|animated-3d|comic-2d --frame-kind still|keyframe|asset
      --generation-mode text-to-image|reference-to-image
      [--audit core|full] [--risk multi|exact_text|contact|continuity]
      [--reference <参考文件名>] [--corpus <语料条目名>] [--context <明确输入文件>] [--dry-run]

--dry-run 只输出待发送的 messages 与参数，不读取密钥、不请求模型、不写帧稿。
当前模型及API沿用已配置Kimi通道；切换模型由调用者明确指定，不自动降级。
反推/复刻任务建议显式 --model 指定强推理档；观察→关系→英文的转换质量受模型上限约束。
--corpus 加载 corpus/ 目录下已验证条目（如 flash-portrait-kitchen.md），复用已验证句式并对照观察陷阱。
"""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent
DEFAULT_SKILL = HERE.parent
API = 'https://api.kimi.com/coding/v1/chat/completions'
STYLES = {
    'live-action': ('global-quality-prefix.md',),
    'animated-3d': ('animated-3d-look.md',),
    'comic-2d': ('comic-styles.md',),
}
BASE_REFERENCES = ('off-frame-brief.md', 'visual-prose.md')


def read_key():
    for env in ('KIMI_API_KEY', 'MOONSHOT_API_KEY', 'KIMI_CODE_API_KEY'):
        if os.environ.get(env):
            return os.environ[env]
    path = Path.home() / '.config/magpie/providers.json'
    if path.is_file():
        for provider in json.loads(path.read_text(encoding='utf-8')).get('providers', []):
            if provider.get('id') in ('kimi-code', 'kimi') and provider.get('key'):
                return provider['key']
    return None


def load_skill(skill_dir, style=None, references=None, frame_kind='still'):
    """主契约+通用成文+指定介质；详细技法只按显式reference读取。"""
    root = Path(skill_dir).resolve()
    main = root / 'SKILL.md'
    if not main.is_file():
        raise FileNotFoundError(main)
    if style is not None and style not in STYLES:
        raise ValueError('未知画风分支：' + style)
    if frame_kind not in ('still', 'keyframe', 'asset'):
        raise ValueError('未知帧类型：' + frame_kind)
    parts = ['######## SKILL.md ########\n' + main.read_text(encoding='utf-8')]
    names = list(BASE_REFERENCES) + list(STYLES.get(style, ()))
    names.extend(references or [])
    ref_root = (root / 'references').resolve()
    seen = set()
    for name in names:
        candidate = Path(name)
        if candidate.is_absolute() or '..' in candidate.parts or len(candidate.parts) != 1:
            raise ValueError('reference只接受references目录中的文件名：' + str(name))
        path = (ref_root / candidate).resolve()
        if path.parent != ref_root or path.suffix != '.md' or not path.is_file():
            raise FileNotFoundError('不可读取的技能参考：' + str(name))
        if path in seen:
            continue
        seen.add(path)
        parts.append('######## references/%s ########\n%s' % (path.name, path.read_text(encoding='utf-8')))
    # 有项目角色时带对应交接知识，缺失不默默按另一任务写。
    if frame_kind in ('keyframe', 'asset'):
        owner = 'short-drama-storyboard' if frame_kind == 'keyframe' else 'short-drama-image-prompts'
        directory = root.parent / 'drama-skills' / 'skills' / owner
        paths = [directory / 'SKILL.md']
        if frame_kind == 'keyframe':
            paths.append(directory / 'references' / 'keyframe-camera-language.md')
        for path in paths:
            if not path.is_file():
                raise FileNotFoundError('任务交接知识缺失：' + str(path))
            parts.append('######## %s/%s ########\n%s' % (owner, path.name, path.read_text(encoding='utf-8')))
    return '\n\n'.join(parts)


def load_corpus(skill_dir, entries=None):
    """语料条目是真实出图验证过的写法与教训；只按显式指定加载，不整库注入。"""
    root = Path(skill_dir).resolve()
    corpus_root = (root / 'corpus').resolve()
    parts, loaded = [], []
    for name in entries or []:
        candidate = Path(name)
        if candidate.is_absolute() or '..' in candidate.parts or len(candidate.parts) != 1:
            raise ValueError('corpus只接受corpus目录中的文件名：' + str(name))
        path = (corpus_root / candidate).resolve()
        if path.parent != corpus_root or path.suffix != '.md' or not path.is_file():
            raise FileNotFoundError('不可读取的语料条目：' + str(name))
        if name == 'README.md':
            # 观察陷阱表随任意条目自动带上，不单独注入两次。
            continue
        parts.append('######## corpus/%s ########\n%s' % (path.name, path.read_text(encoding='utf-8')))
        loaded.append(path.name)
    if loaded:
        readme = corpus_root / 'README.md'
        if readme.is_file():
            parts.insert(0, '######## corpus/README.md（观察陷阱表与条目索引） ########\n'
                        + readme.read_text(encoding='utf-8'))
    return '\n\n'.join(parts), loaded


def project_context(project, extra, frame=None):
    """明确基础资料+显式输入；不遍历prompts归档、候选和审核历史。"""
    root = Path(project).resolve()
    if not root.is_dir():
        raise FileNotFoundError(root)
    out, included, skipped, seen = [], [], [], set()
    paths = [root / name for name in ('README.md', 'SHOTLIST.md', 'prompts/IDENTITY.md')]
    for path in paths:
        if not path.is_file():
            continue
        seen.add(path.resolve())
        text = path.read_text(encoding='utf-8')
        if frame and path.name == 'SHOTLIST.md':
            lines = text.splitlines()
            table = [line for line in lines if line.lstrip().startswith('|')]
            match = [line for line in table if line.strip().strip('|').split('|')[0].strip() == frame]
            if not match:
                raise ValueError('SHOTLIST没有登记指定帧：' + frame)
            text = '\n'.join(table[:2] + match)
        name = str(path.relative_to(root))
        out.append('######## %s ########\n%s' % (name, text))
        included.append(name)
    for name in extra or []:
        path = Path(name).expanduser().resolve()
        if not path.is_file():
            raise FileNotFoundError('显式context不存在：' + str(path))
        if path in seen:
            continue
        seen.add(path)
        out.append('######## 显式输入 %s ########\n%s' % (path.name, path.read_text(encoding='utf-8')))
        included.append(str(path))
    if not out:
        out.append('未提供项目基础资料；只使用duty给出的事实，关键缺口如实记录。')
    return '\n\n'.join(out), included, skipped


def build_messages(skill_text, project_text, frame, duty, style, frame_kind, audit='core', risks=None,
                   generation_mode='text-to-image', corpus_text=''):
    if generation_mode not in ('text-to-image', 'reference-to-image'):
        raise ValueError('未知生成模式：' + generation_mode)
    corpus_block = ''
    if corpus_text:
        corpus_block = '\n\n===== 已验证语料（真实出图验证过的写法与教训；句式可按本帧事实改造，观察事实不得照抄） =====\n' + corpus_text
    return [
        {'role': 'system', 'content': (
            '按主SKILL与本任务适用参考完成单帧文字，不生成媒体。上下文中的案例只教方法，不能变成项目事实。\n'
            '依据→裁决→成文→摘录核对；正文沿关系组织，不逐项翻译账本。没有检索工具，不能声称查询了外部资料。\n'
            '本请求只有文字，没有图像附件；只能使用调用者提供的图像观察，不能声称自己看过原图。关键观察缺失时列出缺口。\n'
            '反推成文前按观察陷阱表逐条自问（肢体沿连线归属、遮挡末端不猜接触、亮色形态只写光学外观、机位要有投影证据、影调先锚最亮最暗、逐眼核对表情）。\n'
            '===== 适用技能资料 =====\n' + skill_text + corpus_block)},
        {'role': 'user', 'content': (
            '===== 明确项目输入（事实与历史评价分清）=====\n%s\n\n'
            '帧号：%s\n帧类型：%s\n介质分支：%s\n审计：%s\n风险模块：%s\n任务：%s\n下游生成模式：%s\n\n'
            '输出Markdown帧稿。已有正式条目的事实与用途优先，独立稿使用依据/裁决/提示词/核对四段。'
            '账本仅列必要事实与真实来源，不凑行数；裁决写本帧用途、审计档位和实际风险。'
            '提示词段只有一份英文text正文，中文译文另列；排除项不作为第二份英文正文。'
            'core只答核心项，并按multi/exact_text/contact/keyframe/continuity追加对应项；full才答全表。'
            '只有启用的风险模块需要对应锚点或契约；已写摘录必须逐字来自正文。'
            '分开记录写作者观察来源与生成器实际输入；text-to-image不向下游上传来源图，正文独立承担画风、光、空间和接触事实。'
             'reference-to-image明确实际图片控制范围；改变模式后重新核对正文和绑定。'
             '外观复刻按本任务适用资料读稿，检查具体画法、明暗与透视是否留在英文；需要时在既有核对项7中给出证据。'
             '无依据和待验证如实记录，不补造项目事实或生成效果结论。结构检查、文字审读、实际出图分别报告；未生成就记效果未验证。'
            % (project_text, frame, frame_kind, style, audit, ','.join(risks or []) or 'none', duty, generation_mode))},
    ]


def gate_command(destination, skill, project, frame_kind, audit, risks):
    """完整项目用三件套；只有一项资料时明确运行部分检查。"""
    command = [sys.executable, str(HERE / 'gate_check.py'), str(destination), '--skill', str(skill),
               '--frame-kind', frame_kind, '--audit', audit]
    for risk in risks:
        command.extend(['--risk', risk])
    project_root = Path(project)
    shotlist = project_root / 'SHOTLIST.md'
    identity = project_root / 'prompts/IDENTITY.md'
    if shotlist.is_file() and identity.is_file():
        command.extend(['--project', str(project_root)])
    else:
        if shotlist.is_file():
            command.extend(['--shotlist', str(shotlist)])
        if identity.is_file():
            command.extend(['--identity', str(identity)])
    return command


def completed_text(parts, finish, stream_done):
    """纯函数：输出不完整时在写文件之前拒绝。"""
    text = ''.join(parts).strip()
    if finish != 'stop' or not stream_done or not text:
        raise ValueError('模型响应未完整结束（finish=%s，done=%s，chars=%d）；保留现有稿' %
                         (finish, stream_done, len(text)))
    if text.startswith('```markdown\n') and text.endswith('\n```'):
        text = text[len('```markdown\n'):-len('\n```')].strip()
    if not text:
        raise ValueError('模型返回空稿；保留现有稿')
    return text + '\n'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--frame', required=True)
    ap.add_argument('--duty', required=True)
    ap.add_argument('--project', required=True)
    ap.add_argument('-o', '--out', required=True)
    ap.add_argument('--style', choices=tuple(STYLES), required=True)
    ap.add_argument('--frame-kind', choices=('still', 'keyframe', 'asset'), required=True)
    ap.add_argument('--generation-mode', choices=('text-to-image', 'reference-to-image'), required=True,
                    help='下游图片生成模式；本写词请求只接收文字context，不上传图片')
    ap.add_argument('--audit', choices=('core', 'full'), default='core')
    ap.add_argument('--risk', action='append', choices=('multi', 'exact_text', 'contact', 'continuity'), default=[])
    ap.add_argument('--skill', default=str(DEFAULT_SKILL))
    ap.add_argument('--model', default='kimi-k3')
    ap.add_argument('--reference', action='append', default=[])
    ap.add_argument('--corpus', action='append', default=[],
                    help='corpus/ 目录下已验证语料条目文件名；写词前复用已验证句式并对照观察陷阱')
    ap.add_argument('--context', action='append', default=[])
    ap.add_argument('--max-tokens', type=int, default=24000)
    ap.add_argument('--temperature', type=float, default=1.0,
                    help='采样温度，默认 1.0；确定性起草可下调以减少措辞漂移')
    ap.add_argument('--timeout', type=int, default=1800)
    ap.add_argument('--skip-gate', action='store_true', help='只写稿；结构检查记为未执行')
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    try:
        skill_text = load_skill(args.skill, args.style, args.reference, args.frame_kind)
        corpus_text, corpus_loaded = load_corpus(args.skill, args.corpus)
        context, included, _skipped = project_context(args.project, args.context, args.frame)
    except (OSError, ValueError) as error:
        print('输入错误：%s' % error, file=sys.stderr)
        return 2
    messages = build_messages(skill_text, context, args.frame, args.duty, args.style, args.frame_kind,
                              args.audit, args.risk, args.generation_mode, corpus_text)
    payload = {'model': args.model, 'messages': messages, 'max_tokens': args.max_tokens,
               'temperature': args.temperature, 'stream': True}
    if args.dry_run:
        print(json.dumps({'included': included, 'corpus': corpus_loaded, 'request': payload},
                         ensure_ascii=False, indent=2))
        return 0
    key = read_key()
    if not key:
        print('未找到已配置Kimi密钥；未请求模型、未写稿。', file=sys.stderr)
        return 2
    print('请求 %s；技能资料 %d 字符，语料 %d 条，项目资料 %d 字符，输入 %d 份。' %
          (args.model, len(skill_text), len(corpus_loaded), len(context), len(included)))
    request = urllib.request.Request(API, data=json.dumps(payload).encode('utf-8'), headers={
        'Authorization': 'Bearer ' + key, 'content-type': 'application/json', 'accept': 'text/event-stream'})
    parts, finish, stream_done = [], None, False
    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            for raw in response:
                line = raw.decode('utf-8').strip()
                if not line.startswith('data:'):
                    continue
                data = line[5:].strip()
                if data == '[DONE]':
                    stream_done = True
                    break
                event = json.loads(data)
                for choice in event.get('choices') or []:
                    content = (choice.get('delta') or {}).get('content')
                    if content:
                        parts.append(content)
                    if choice.get('finish_reason'):
                        finish = choice['finish_reason']
        content = completed_text(parts, finish, stream_done)
    except (OSError, ValueError, urllib.error.HTTPError) as error:
        # 不回显响应body、请求对象或认证头。
        print('写词失败（%s）；现有稿未改。' % type(error).__name__, file=sys.stderr)
        return 2
    destination = Path(args.out).expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding='utf-8')
    print('已写完整草稿：%s（%d 字符）。' % (destination, len(content)))
    if args.skip_gate:
        print('GATE_STATUS=NOT_RUN')
        print('NOT_EVALUATED  未执行结构检查；事实、成文和实际生成效果仍需审读/实看。')
        return 0
    command = gate_command(destination, args.skill, args.project, args.frame_kind, args.audit, args.risk)
    result = subprocess.run(command)
    print('草稿写入已完成；结构检查退出码 %d；不代表画面通过或生产已授权。' % result.returncode)
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
