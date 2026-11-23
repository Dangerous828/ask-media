#!/usr/bin/env python3
"""任务分支与真实输入边界；不以词表分数评价提示词画面质量。"""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest import mock
import contextlib
import io
import json

ROOT = Path(__file__).resolve().parents[1]


def load(name, file):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / file)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gate = load('still_gate', 'gate_check.py')
writer = load('still_writer', 'k3_write.py')


class TaskBoundaries(unittest.TestCase):
    def test_landscape_does_not_require_containers_skin_or_optical_jargon(self):
        text = '''### 3. 提示词
```text
A flat ink drawing of a distant mountain above a broad white river, the dark ridge fading into pale grey mist.
```
'''
        problems, warnings = [], []
        gate.check_body(text, problems, warnings)
        self.assertEqual(problems, [])

    def test_ordinary_still_does_not_require_keyframe_anchor(self):
        problems = []
        gate.check_camera_language('### 2. 裁决\n独立静帧，按既定构图。', problems)
        self.assertEqual(problems, [])

    def test_two_candidate_english_bodies_are_ambiguous(self):
        text = '''### 3. 提示词
```text
A red cup rests on a wooden table under window light, shot on film.
```
```text
A blue cup rests on the same table under window light, shot on film.
```
'''
        problems, warnings = [], []
        gate.check_body(text, problems, warnings)
        self.assertTrue(any('正文' in p and ('多个' in p or '唯一' in p) for p in problems))

    def test_nested_prompt_heading_does_not_duplicate_its_parent_body(self):
        text = '''## 提示词
### 唯一英文正文
```text
A red cup rests on a wooden table.
```
'''
        problems, warnings = [], []
        gate.check_body(text, problems, warnings)
        self.assertEqual(problems, [])

    def test_translation_and_quoted_exact_text_are_distinguished(self):
        text = '''### 提示词
```text
A sign reads "开业" beside a red cup.
```
```text
招牌写着开业，旁边是 red cup。
```
'''
        problems, warnings = [], []
        body = gate.check_body(text, problems, warnings)
        self.assertEqual(problems, [])
        self.assertIn('A sign reads "开业"', body)

    def test_same_semantic_sections_are_accepted(self):
        text = '''### 1. 必要依据
| 事实/选择 | 本帧可见结果 | 来源及状态 |
|---|---|---|
| 纸面山水 | 白河与墨山 | 测试设计 |
### 2. 裁决
独立静帧。
### 3. 唯一英文正文
```text
2D ink drawing of a pale river beside a dark mountain.
```
### 4. 文字核对表
| # | 结论 | 证据或原因 |
|---|---|---|
| L0_1 | yes | 纸面山水 |
| L0_2 | NA：空镜 | 无人物 |
| L0_3 | yes | 横向纸面 |
| L0_4 | yes | 山河关系 |
| 0c | NA：空镜 | 无人物 |
| 0f | yes | 白河墨山 |
| 5b | yes | 平面留白 |
| 6c | NA：空镜 | 无人物 |
| 7 | yes | 水墨介质 |
| 9 | yes | 无负向 |
| 12 | yes | 唯一正文 |
| 13 | NA：空镜 | 无表演 |
| 14 | NA：单帧 | 无多帧 |
| 15 | NA：单帧 | 无连续物 |
| 16 | yes | 测试设计 |
'''
        problems, warnings = [], []
        gate.check_ledger(text, problems)
        gate.check_body(text, problems, warnings)
        self.assertEqual(problems, [])

    def test_unknown_source_is_not_replaced_with_notes_column(self):
        rows = '| # | 事实 | 像素 | 出处 | 存疑/降级 |\n|---|---|---|---|---|\n'
        rows += ''.join('| %d | 已定事实 | visible wall | — | 待查，不能冒充出处 |\n' % i for i in range(1, 11))
        problems = []
        gate.check_ledger('### 1. 账本\n' + rows, problems)
        self.assertTrue(any('出处' in p or '来源' in p for p in problems))

    def test_style_context_does_not_load_every_branch(self):
        text = writer.load_skill(str(ROOT), style='comic-2d')
        self.assertIn('comic-styles.md', text)
        self.assertNotIn('######## references/eye-anatomy-catchlight.md', text)
        self.assertNotIn('######## references/animated-3d-look.md', text)
        self.assertNotIn('######## references/portrait-light-laws.md', text)

    def test_reconstruction_reference_is_available_without_other_media_branches(self):
        text = writer.load_skill(str(ROOT), style='comic-2d',
                                 references=['appearance-reconstruction.md'])
        self.assertIn('######## references/appearance-reconstruction.md', text)
        self.assertIn('######## references/comic-styles.md', text)
        self.assertNotIn('######## references/global-quality-prefix.md', text)

    def test_generation_mode_is_explicit_in_actual_dry_run_payload(self):
        for mode in ('text-to-image', 'reference-to-image'):
            with self.subTest(mode=mode), tempfile.TemporaryDirectory() as tmp:
                output = Path(tmp) / 'not-written.md'
                argv = ['k3_write.py', '--frame', 'S1', '--duty', 'test', '--project', tmp,
                        '-o', str(output), '--style', 'comic-2d', '--frame-kind', 'still',
                        '--generation-mode', mode, '--dry-run']
                captured = io.StringIO()
                with mock.patch('sys.argv', argv), contextlib.redirect_stdout(captured), \
                     mock.patch.object(writer, 'read_key', side_effect=AssertionError('credentials')), \
                     mock.patch.object(writer.urllib.request, 'urlopen', side_effect=AssertionError('network')):
                    self.assertEqual(writer.main(), 0)
                messages = json.loads(captured.getvalue())['request']['messages']
                self.assertIn('下游生成模式：' + mode, messages[1]['content'])
                self.assertIn('结构检查、文字审读、实际出图', messages[1]['content'])
                self.assertIn('写作者观察来源', messages[1]['content'])
                self.assertFalse(output.exists())

    def test_missing_generation_mode_does_not_choose_for_the_caller(self):
        with tempfile.TemporaryDirectory() as tmp:
            argv = ['k3_write.py', '--frame', 'S1', '--duty', 'test', '--project', tmp,
                    '-o', str(Path(tmp) / 'out.md'), '--style', 'comic-2d',
                    '--frame-kind', 'still', '--dry-run']
            with mock.patch('sys.argv', argv), contextlib.redirect_stderr(io.StringIO()), \
                 mock.patch.object(writer, 'read_key', side_effect=AssertionError('credentials')):
                with self.assertRaises(SystemExit) as raised:
                    writer.main()
            self.assertEqual(raised.exception.code, 2)

    def test_unregistered_reference_path_is_rejected(self):
        with self.assertRaises((ValueError, FileNotFoundError)):
            writer.load_skill(str(ROOT), style='comic-2d', references=['../../AGENTS.md'])

    def test_corpus_entry_loads_with_trap_table_and_without_sweeping_the_library(self):
        corpus_text, loaded = writer.load_corpus(str(ROOT), ['flash-portrait-kitchen.md'])
        self.assertEqual(loaded, ['flash-portrait-kitchen.md'])
        self.assertIn('######## corpus/README.md', corpus_text)
        self.assertIn('######## corpus/flash-portrait-kitchen.md', corpus_text)
        self.assertIn('观察陷阱表', corpus_text)
        self.assertIn('steep close high-angle view', corpus_text)
        # 索引表会列出全部条目名，但未指定条目的正文不得整篇注入。
        self.assertNotIn('# 2D插画-绘画性动漫双人缠斗-001', corpus_text)

    def test_corpus_paths_are_confined_to_the_corpus_directory(self):
        for bad in ('../AGENTS.md', '/etc/hosts', 'sub/dir/entry.md'):
            with self.subTest(bad=bad), self.assertRaises((ValueError, FileNotFoundError)):
                writer.load_corpus(str(ROOT), [bad])

    def test_corpus_is_injected_into_the_dry_run_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / 'not-written.md'
            argv = ['k3_write.py', '--frame', 'S1', '--duty', 'test', '--project', tmp,
                    '-o', str(output), '--style', 'live-action', '--frame-kind', 'still',
                    '--generation-mode', 'text-to-image', '--dry-run',
                    '--corpus', 'flash-portrait-kitchen.md']
            captured = io.StringIO()
            with mock.patch('sys.argv', argv), contextlib.redirect_stdout(captured), \
                 mock.patch.object(writer, 'read_key', side_effect=AssertionError('credentials')), \
                 mock.patch.object(writer.urllib.request, 'urlopen', side_effect=AssertionError('network')):
                self.assertEqual(writer.main(), 0)
            payload = json.loads(captured.getvalue())
            self.assertEqual(payload['corpus'], ['flash-portrait-kitchen.md'])
            system = payload['request']['messages'][0]['content']
            self.assertIn('已验证语料', system)
            self.assertIn('观察陷阱', system)
            self.assertIn('肢体沿连线归属', system)
            self.assertFalse(output.exists())

    def test_project_loader_does_not_sweep_archives_or_other_frames(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'README.md').write_text('CURRENT_PROJECT_FACT', encoding='utf-8')
            (root / 'prompts').mkdir()
            (root / 'prompts' / '001.md').write_text('UNRELATED_OLD_FRAME', encoding='utf-8')
            (root / 'prompts' / '审核历史.md').write_text('REJECTED_DRAFT_RULE', encoding='utf-8')
            text, included, skipped = writer.project_context(tmp, [])
            self.assertIn('CURRENT_PROJECT_FACT', text)
            self.assertNotIn('UNRELATED_OLD_FRAME', text)
            self.assertNotIn('REJECTED_DRAFT_RULE', text)

    def test_missing_explicit_context_is_not_silently_skipped(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises((ValueError, FileNotFoundError)):
                writer.project_context(tmp, [str(Path(tmp) / 'missing.md')])


class ExecutionBoundaries(unittest.TestCase):
    def test_complete_response_required(self):
        for finish, done in [('length', True), ('stop', False), (None, True)]:
            with self.subTest(finish=finish, done=done), self.assertRaises(ValueError):
                writer.completed_text(['partial draft'], finish, done)
        self.assertEqual(writer.completed_text(['complete draft'], 'stop', True), 'complete draft\n')

    def test_truncated_stream_keeps_existing_file(self):
        class Response:
            def __enter__(self):
                return iter([
                    b'data: {"choices":[{"delta":{"content":"incomplete draft"},"finish_reason":"length"}]}\n',
                    b'data: [DONE]\n'])
            def __exit__(self, *args):
                return False
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'S9.md'
            out.write_text('ACCEPTED_EXISTING_DRAFT', encoding='utf-8')
            argv = ['k3_write.py', '--frame', 'S9', '--duty', 'test', '--project', tmp,
                    '-o', str(out), '--style', 'comic-2d', '--frame-kind', 'still',
                    '--generation-mode', 'text-to-image']
            with mock.patch('sys.argv', argv), mock.patch.object(writer, 'read_key', return_value='offline-placeholder'), \
                 mock.patch.object(writer.urllib.request, 'urlopen', return_value=Response()) as request, \
                 contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                result = writer.main()
            self.assertEqual(result, 2)
            self.assertEqual(request.call_count, 1)
            self.assertEqual(out.read_text(encoding='utf-8'), 'ACCEPTED_EXISTING_DRAFT')

    def test_dry_run_does_not_read_credentials_or_request(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'draft.md'
            argv = ['k3_write.py', '--frame', 'S9', '--duty', 'single ink landscape', '--project', tmp,
                    '-o', str(out), '--style', 'comic-2d', '--frame-kind', 'still',
                    '--generation-mode', 'text-to-image', '--dry-run']
            capture = io.StringIO()
            with mock.patch('sys.argv', argv), mock.patch.object(writer, 'read_key', side_effect=AssertionError('credential access')), \
                 mock.patch.object(writer.urllib.request, 'urlopen', side_effect=AssertionError('network access')), \
                 contextlib.redirect_stdout(capture):
                self.assertEqual(writer.main(), 0)
            payload = json.loads(capture.getvalue())
            self.assertEqual(len(payload['request']['messages']), 2)
            self.assertFalse(out.exists())

    def test_unseen_head_and_eyes_do_not_add_face(self):
        body = 'The lens is level with the bowl. Her right hand holds the white bowl.'
        text = '''### 2. 裁决
- 机位锁｜位置：与碗同高｜camera_en：The lens is level with the bowl
- 人物构图：Maya｜身体：右手持碗｜头部：不可见（手部裁切）｜视线目标：不可见（眼睛裁切）｜body_en：Her right hand holds the white bowl｜head_en：NA｜gaze_en：NA
'''
        problems = []
        gate.check_composition_locks(text, body, problems)
        self.assertEqual(problems, [])
        bad = []
        gate.check_composition_locks(text.replace('不可见（眼睛裁切）', '看碗'), body, bad)
        self.assertTrue(any('gaze_en' in issue for issue in bad))

    def test_named_visible_subject_uses_registered_partial_identity(self):
        identity = '''## Maya
> presence: Maya
```text
Maya is 30 with short black hair.
```
### 手部
> identity: Maya
> view: right_hand
```text
her hand and dark blue shirt cuff
```
'''
        body = "Maya's right hand holds a metal spoon; only her hand and dark blue shirt cuff are visible."
        problems = []
        gate.check_identity_views(identity, body, '身份视图：Maya=right_hand', problems)
        self.assertEqual(problems, [])
        missing = []
        gate.check_identity_views(identity, body, '身份视图：Maya=unknown', missing)
        self.assertTrue(missing)

    def test_unknown_frame_kind_is_rejected(self):
        text = '''### 1. 账本
| 事实 | 可见结果 | 出处 |
|---|---|---|
| 杯子 | red cup | 测试设计 |
### 2. 裁决
帧类型：unknown
### 3. 提示词
```text
A red cup rests on a table.
```
### 4. 验收单
| # | 结论 | 证据 |
|---|---|---|
| 9 | yes | 无独立负向槽 |
'''
        result, output = run_gate(text, '--audit', 'core')
        self.assertEqual(result, 1)
        self.assertIn('未知帧类型：unknown', output)

    def test_only_selected_shotlist_row_is_injected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'SHOTLIST.md').write_text('| 镜 | 职责 |\n|---|---|\n| S1 | UNRELATED_SHOT |\n| S9 | CURRENT_SHOT |\n', encoding='utf-8')
            text, _, _ = writer.project_context(tmp, [], frame='S9')
            self.assertIn('CURRENT_SHOT', text)
            self.assertNotIn('UNRELATED_SHOT', text)


def run_gate(text, *extra):
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / 'frame.md'
        path.write_text(text, encoding='utf-8')
        argv = ['gate_check.py', str(path), '--skill', str(ROOT), *extra]
        capture = io.StringIO()
        with mock.patch('sys.argv', argv), contextlib.redirect_stdout(capture):
            result = gate.main()
        return result, capture.getvalue()


def audit_doc(body, rows, decision='', ledger=None):
    return '''### 必要依据
%s
### 裁决
帧类型：still
%s
### 唯一英文正文
```text
%s
```
### 文字核对表
| # | 结论 | 证据或原因 |
|---|---|---|
%s
''' % (ledger or '| 事实 | 可见结果 | 来源 |\n|---|---|---|\n| 测试主体 | 当前画面 | 合成测试输入 |', decision, body, rows)


CORE_ROWS = '''| L0_1 | yes | 身份与来源一致 |
| L0_4 | yes | 无未裁决冲突 |
| 0f | yes | 事实进入唯一正文 |
| 9 | NA：无参考或负向槽 | 本例不使用 |
| 12 | yes | 唯一正文与译文已核对 |
| 16 | yes | 合成输入可追溯 |'''


class RiskProfileBoundaries(unittest.TestCase):
    def test_core_single_person_still_needs_no_four_anchors(self):
        result, output = run_gate(audit_doc('A woman sits on a wooden chair beside a window.', CORE_ROWS, '审计：core'))
        self.assertEqual(result, 0, output)
        self.assertIn('audit=core', output)
        self.assertIn('modules=none', output)

    def test_multi_requires_every_declared_person_lock(self):
        body = 'A mother on frame left faces her daughter on frame right; the daughter looks down at a bowl.'
        locks = '''审计：core
风险：multi
出场：母亲,女儿
- 人物构图：母亲｜身体：朝女儿｜头部：非必要，正文用相向关系表达｜视线目标：女儿；独立目光短语非必要｜body_en：A mother on frame left faces her daughter on frame right｜head_en：NA｜gaze_en：NA
- 人物构图：女儿｜身体：朝母亲｜头部：非必要，低头由身体摘录承载｜视线目标：碗；独立目光短语非必要｜body_en：the daughter looks down at a bowl｜head_en：NA｜gaze_en：NA'''
        rows = CORE_ROWS + '\n| 0c | yes | 两人归属明确 |\n| 6c | yes | 两人关系已核对；非必要方向NA |'
        result, output = run_gate(audit_doc(body, rows, locks))
        self.assertEqual(result, 0, output)
        missing = locks.replace('出场：母亲,女儿', '出场：母亲,女儿,父亲')
        result, output = run_gate(audit_doc(body, rows, missing))
        self.assertEqual(result, 1)
        self.assertIn('出场与人物构图不一致', output)

    def test_exact_non_english_text_is_allowed_and_verbatim(self):
        decision = '审计：core\n风险：exact_text\n- 文字契约：sign_1｜exact：开业｜位置：门楣'
        rows = CORE_ROWS + '\n| 5b | yes | 招牌文字逐字一致 |'
        result, output = run_gate(audit_doc('The shop sign reads "开业" above the door.', rows, decision))
        self.assertEqual(result, 0, output)
        result, output = run_gate(audit_doc('The shop sign reads "开门" above the door.', rows, decision))
        self.assertEqual(result, 1)
        self.assertIn('精确文字没有逐字进入英文正文', output)

    def test_contact_contract_preserves_part_object_and_visibility(self):
        decision = '审计：core\n风险：contact\n- 接触契约：bowl_1｜主体：女儿左手｜对象：近处碗BOWL-A｜关系：勺在碗上方｜可见性：手、勺和碗沿可见'
        rows = CORE_ROWS + '\n| L0_2 | yes | 当前接触相位明确 |\n| 0c | yes | 左手与BOWL-A归属明确 |'
        result, output = run_gate(audit_doc('Her left hand holds a spoon above the near bowl.', rows, decision))
        self.assertEqual(result, 0, output)
        result, output = run_gate(audit_doc('Her left hand holds a spoon above the near bowl.', rows, '审计：core\n风险：contact'))
        self.assertEqual(result, 1)
        self.assertIn('缺少「接触契约」', output)

    def test_camera_na_is_for_nonessential_still_not_keyframe(self):
        body = 'A woman sits by the window.'
        text = '### 裁决\n- 机位锁｜位置：未指定且非必要｜camera_en：NA'
        problems = []
        gate.check_composition_locks(text, body, problems, frame_kind='still', audit='core', modules=set())
        self.assertEqual(problems, [])
        gate.check_composition_locks(text, body, problems, frame_kind='keyframe', audit='core', modules={'keyframe'})
        self.assertTrue(any('camera_en' in problem for problem in problems))

    def test_keyframe_without_people_still_requires_camera_lock(self):
        problems = []
        gate.check_composition_locks('### 裁决\n用途：composition', 'A pale mountain beside a river.', problems,
                                    frame_kind='keyframe', audit='core', modules={'keyframe'})
        self.assertTrue(any('机位锁' in problem for problem in problems))

    def test_na_cannot_use_the_question_as_its_reason(self):
        result, output = run_gate(audit_doc('A red cup on a table.', CORE_ROWS.replace('| 9 | NA：无参考或负向槽 | 本例不使用 |', '| 9 | NA |  |')))
        self.assertEqual(result, 1)
        self.assertIn('NA缺少适用性理由', output)

    def test_alias_sections_cannot_reverse_fact_and_body_order(self):
        text = '''### 唯一英文正文
```text
A red cup on a table.
```
### 必要依据
| 事实 | 可见结果 | 来源 |
|---|---|---|
| 杯子 | 红色 | 合成输入 |
### 裁决
帧类型：still
### 文字核对表
''' + CORE_ROWS
        result, output = run_gate(text)
        self.assertEqual(result, 1)
        self.assertIn('顺序反了', output)


class WriterProfileBoundaries(unittest.TestCase):
    def test_writer_passes_audit_and_risks_to_model(self):
        messages = writer.build_messages('SKILL', 'INPUT', 'S1', '一只杯子', 'live-action', 'still',
                                         audit='core', risks=['exact_text', 'contact'])
        self.assertIn('审计：core', messages[1]['content'])
        self.assertIn('风险模块：exact_text,contact', messages[1]['content'])
        self.assertIn('只有启用的风险模块', messages[1]['content'])

    def test_writer_runs_available_partial_project_sources(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'SHOTLIST.md').write_text('| 镜 |\n|---|\n| S1 |', encoding='utf-8')
            command = writer.gate_command(root / 'frame.md', ROOT, root, 'still', 'core', ['contact'])
            self.assertIn('--shotlist', command)
            self.assertNotIn('--project', command)
            self.assertNotIn('--identity', command)
            self.assertEqual(command[command.index('--risk') + 1], 'contact')

    def test_writer_uses_full_project_only_when_both_sources_exist(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / 'SHOTLIST.md').write_text('| 镜 |\n|---|---|\n| S1 | x |', encoding='utf-8')
            (root / 'prompts').mkdir()
            (root / 'prompts/IDENTITY.md').write_text('identity', encoding='utf-8')
            command = writer.gate_command(root / 'frame.md', ROOT, root, 'still', 'core', [])
            self.assertIn('--project', command)
            self.assertNotIn('--shotlist', command)
            self.assertNotIn('--identity', command)

class QwenStyleWarnings(unittest.TestCase):
    """千问成文规则只给 WARN，且只在帧稿声明千问通道时启用。"""

    def warns(self, body):
        w = []
        gate.check_qwen_style(body, w)
        return w

    def test_quality_word_and_aspect_warn(self):
        w = self.warns('The image is a photograph of a woman, masterpiece, 8K. A vertical 9:16 frame composition.')
        self.assertTrue(any('质量词' in x for x in w))
        self.assertTrue(any('画幅' in x for x in w))

    def test_quoted_text_not_flagged(self):
        w = self.warns('A sign reading "8K masterpiece" hangs over the door of a shop.')
        self.assertFalse(any('质量词' in x for x in w))

    def test_short_body_not_flagged(self):
        self.assertEqual(self.warns('A flat ink drawing of a distant mountain above a white river.'), [])

    def test_overlong_body_warns(self):
        w = self.warns('The image is a warm photograph of a woman at a window. ' * 60)
        self.assertTrue(any('超过' in x for x in w))

    def test_single_exclusion_tail_not_flagged(self):
        self.assertFalse(any('排除词' in x for x in self.warns('A woman at a window in warm light. no text')))

    def test_only_runs_when_qwen_declared(self):
        self.assertTrue(gate.QWEN_DECLARED_RE.search('- 通道：本地 h3q · Qwen Image 2.1'))
        self.assertFalse(gate.QWEN_DECLARED_RE.search('- 通道：Kling 图生视频'))


if __name__ == '__main__':
    unittest.main()
