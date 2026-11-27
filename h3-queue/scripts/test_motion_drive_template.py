"""动作驱动图模板与 video-motion-drive.md 的一致性。

2026-11-27 实测发现：文档写「节点 3 的 text 留空、不要写 low quality, blurry,
distorted」，而模板里正好写着那句。照模板用的人必然违反文档，而且没有测试守。
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "h3-queue/templates/video_motion_drive_graph.json"


class MotionDriveTemplateTests(unittest.TestCase):
    def graph(self) -> dict:
        document = json.loads(TEMPLATE.read_text(encoding="utf-8"))
        return document.get("graph") or document

    def test_negative_slot_is_empty_under_cfg_one(self) -> None:
        """cfg 1.0 下没有负向分支，负向槽必须留空。

        写了词只会制造「配了负向」的错觉——这句判断出自
        `references/video-motion-drive.md`，模板必须与它一致。
        """
        graph = self.graph()
        self.assertEqual(graph["3"]["inputs"]["text"], "")
        self.assertEqual(graph["6"]["inputs"]["cfg"], 1.0)

    def test_placeholders_and_wiring_match_the_doc(self) -> None:
        raw = TEMPLATE.read_text(encoding="utf-8")
        for slot in ("{{PROMPT}}", "{{IDENTITY_IMAGE}}", "{{ACTION_VIDEO}}", "{{PREFIX}}"):
            self.assertIn(slot, raw)
        graph = self.graph()
        # 动作走槽 0，音轨走槽 1——接错槽就是「只拿动作、声音让模型自己编」。
        self.assertEqual(graph["5"]["inputs"]["ref_videos.ref_video_0"], ["31", 0])
        self.assertEqual(graph["5"]["inputs"]["ref_video_audios.ref_video_audio_0"], ["31", 1])
        self.assertEqual(graph["4"]["inputs"]["lora_name"], "Motion_Repair_V2.safetensors")
        self.assertEqual(graph["4"]["inputs"]["strength_model"], 0.7)

    def test_length_is_on_the_17k_plus_5_grid(self) -> None:
        graph = self.graph()
        length = graph["5"]["inputs"]["length"]
        self.assertEqual((length - 5) % 17, 0, f"{length} 不在 17k+5 上")


if __name__ == "__main__":
    unittest.main()
