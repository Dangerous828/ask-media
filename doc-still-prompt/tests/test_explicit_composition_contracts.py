#!/usr/bin/env python3
"""显式构图契约不依赖人物词识别；普通静帧未提供锚点仍可成立。"""
import importlib.util
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('explicit_still_gate', ROOT / 'scripts/gate_check.py')
gate = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(gate)


class ExplicitCompositionContracts(unittest.TestCase):
    def check(self, body, decision='', frame_kind='still', modules=()):
        problems = []
        gate.check_composition_locks('### 裁决\n' + decision, body, problems,
                                     frame_kind=frame_kind, audit='core', modules=set(modules))
        return problems

    def test_ordinary_still_and_asset_can_omit_optional_anchors(self):
        for kind in ('still', 'asset'):
            for body in ('A red bowl on a wooden table.', 'Two foxes sit beside the river.'):
                with self.subTest(kind=kind, body=body):
                    self.assertEqual(self.check(body, frame_kind=kind), [])

    def test_supplied_empty_scene_camera_anchor_must_be_in_body(self):
        decision = '- 机位锁｜位置：俯视桌面｜camera_en：An overhead view'
        for kind in ('still', 'asset'):
            with self.subTest(kind=kind):
                problems = self.check('A red bowl on a wooden table.', decision, kind)
                self.assertTrue(any('camera_en' in p and '正文' in p for p in problems), problems)
                self.assertEqual(self.check('An overhead view of a red bowl on a wooden table.',
                                            decision, kind), [])

    def test_supplied_empty_scene_camera_na_still_needs_reason(self):
        problems = self.check('A red bowl on a wooden table.',
                              '- 机位锁｜位置：俯视桌面｜camera_en：NA')
        self.assertTrue(any('NA' in p for p in problems), problems)
        self.assertEqual(self.check('A red bowl on a wooden table.',
                                    '- 机位锁｜位置：机位未指定且非必要｜camera_en：NA'), [])

    def test_explicit_multi_requires_records_for_animals(self):
        body = 'Two foxes sit beside the river.'
        for kind in ('still', 'asset'):
            with self.subTest(kind=kind):
                problems = self.check(body, '出场：红狐,蓝狐', kind, ('multi',))
                self.assertTrue(any('出场与人物构图不一致' in p for p in problems), problems)

    def test_explicit_multi_without_declaration_fails_for_animals(self):
        problems = self.check('Two foxes sit beside the river.', modules=('multi',))
        self.assertTrue(any('出场' in p for p in problems), problems)

    def test_matching_animal_records_need_no_optional_camera(self):
        body = 'The red fox faces the blue fox, which faces the red fox beside the river.'
        decision = '''出场：红狐,蓝狐
- 人物构图：红狐｜身体：面向蓝狐｜头部：未指定且非必要｜视线目标：未指定且非必要｜body_en：The red fox faces the blue fox｜head_en：NA｜gaze_en：NA
- 人物构图：蓝狐｜身体：面向红狐｜头部：未指定且非必要｜视线目标：未指定且非必要｜body_en：which faces the red fox｜head_en：NA｜gaze_en：NA'''
        self.assertEqual(self.check(body, decision, modules=('multi',)), [])
        problems = self.check(body, decision.replace('出场：红狐,蓝狐', '出场：红狐,蓝狐,白狐'),
                              modules=('multi',))
        self.assertTrue(any('出场与人物构图不一致' in p for p in problems), problems)


if __name__ == '__main__':
    unittest.main()
