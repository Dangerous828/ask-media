# reddit-1vhloyz-walter-prompt-guide

- 类型：案例原文（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SUMMARY.md

````text
# 风险揭晓｜证据交给人物反应

一次干预阻止风险，可读证据随后由有动机的镜头交接给人物反应。

## 核心机制

An urgent intervention creates conflict, a controlled visual proof makes the hidden risk undeniable, and one motivated camera handoff transfers that proof to the recipient's compact reaction.

## 推荐输入格式

`紧急干预 + 隐藏风险 + 可视证据 + 有动机镜头交接 + 简短反应`

## 简短示例

> 实验员拦住同伴触碰容器，紫外光显出内部裂纹；镜头沿容器反光移交到同伴面部，他安静地收回手并点头。

## 必须保留的结构锚点

- 先有干预冲突
- 风险通过可视证据证明
- 镜头交接有物理动机
- 反应简短且改变后续行为

## 使用方法

1. 先保留用户主体和目标，再按推荐格式补齐场景、事件链、镜头和结果。
2. 阅读 [Creative DNA](./creative-dna.json)，重新实例化变量，不做来源表面换名词。
3. 分别查看 [MiniMax H3](./prompts/minimax-h3.md) 与 [Seedance 2.0](./prompts/seedance-2.0.md) 的已验证实例。
4. GitHub 使用 GIF 快速预览；Electron 媒体包播放完整有声 MP4。

## 来源与署名

- 平台：reddit
- 作者：GrayingGamer
- 原始视频：[打开来源](https://www.reddit.com/r/StableDiffusion/comments/1vhloyz/walter_white_and_the_minimax_h3_official/)
- 模型归因：MiniMax H3（creator_claimed）

来源视频用于机制研究与引用；公开模板只保留可迁移因果，不要求复刻来源人物、道具、场景、构图、对白或标志性效果。
````

### creative-dna.json

````text
{
  "complexity": "moderate",
  "mechanism": "An urgent intervention creates conflict, a controlled visual proof makes the hidden risk undeniable, and one motivated camera handoff transfers that proof to the recipient's compact reaction.",
  "invariants": [
    {
      "id": "inv-01",
      "rule": "Establish an urgent conflict through action before revealing the proof state.",
      "purpose": "Creates an immediate question and gives the later evidence a causal reason to appear.",
      "ablation_failure": "Opening on the explanation removes tension and turns the scene into a flat demonstration.",
      "evidence_ids": [
        "beat-01",
        "beat-02"
      ]
    },
    {
      "id": "inv-02",
      "rule": "Hold the proof state visually stable long enough to be understood before the camera hands off.",
      "purpose": "Makes the evidence itself readable while keeping it integrated with performance.",
      "ablation_failure": "Moving away before the hidden condition resolves makes the intervention feel arbitrary.",
      "evidence_ids": [
        "beat-02",
        "obs-05"
      ]
    },
    {
      "id": "inv-03",
      "rule": "Use one motivated reframe to hand the last line to a contrasting second speaker.",
      "purpose": "Converts instruction into a two-person joke without wasting time on coverage.",
      "ablation_failure": "Keeping the camera on the first speaker removes the reaction payoff.",
      "evidence_ids": [
        "beat-03",
        "obs-02"
      ]
    }
  ],
  "slots": [
    {
      "name": "authority_role",
      "constraint": "A visually decisive expert with a clear reason to instruct."
    },
    {
      "name": "recipient_role",
      "constraint": "A contrasting novice or peer who can answer in one short line."
    },
    {
      "name": "proof_state",
      "constraint": "A physical condition, instrument reading, light reveal, or object state that becomes visually unambiguous without copying source typography."
    },
    {
      "name": "setting",
      "constraint": "A context-rich location readable behind a medium close subject."
    },
    {
      "name": "intervention",
      "constraint": "One brief action or line that stops the unsafe or mistaken behavior before the proof appears."
    },
    {
      "name": "reaction",
      "constraint": "One gesture and one line that resolve the conflict."
    },
    {
      "name": "camera_handoff",
      "constraint": "One pan or cut motivated by the second speaker."
    },
    {
      "name": "sound",
      "constraint": "Location ambience plus non-overlapping dialogue; no music required."
    }
  ],
  "anti_copy_exclusions": [
    "protected television characters or actor likenesses",
    "source-series wardrobe, vehicle, desert setup, or color grade",
    "source-character voices and exact dialogue",
    "exact guide title, profanity, framing, or prop typography"
  ],
  "instantiations": [
    {
      "concept": "A museum conservator stops an assistant's brush, lowers an ultraviolet inspection hood, and reveals branching fluorescent repairs before the camera follows the glow to the assistant's embarrassed recoil.",
      "prompt_seed": "An urgent hand-stop becomes justified by a stable ultraviolet proof, then the reflected glow motivates the reaction handoff."
    },
    {
      "concept": "An observatory technician blocks a trainee from opening a dome, slides one red safety filter over the sensor, and reveals a dangerous solar flare before the camera follows the red reflection to the trainee's silent step back.",
      "prompt_seed": "Conflict, optical proof, and a reflection-led camera handoff create a compact safety reversal."
    },
    {
      "concept": "A pastry chef catches a trainee's piping bag, turns a sugar thermometer toward the light, and reveals crystallization in macro before the lens rack-focuses to the trainee lowering the tray.",
      "prompt_seed": "A tactile intervention earns credibility through a stable macro proof and a focus-driven reaction handoff."
    }
  ],
  "failure_modes": [
    {
      "failure": "The proof state changes too quickly to understand.",
      "repair": "Hold the revealed condition for at least two seconds with stable light, focus, and spatial context before the handoff."
    },
    {
      "failure": "Dialogue overlaps or sounds rushed.",
      "repair": "Keep two short lines, place the speaker handoff after the first line fully ends, and remove extra actions."
    },
    {
      "failure": "The scene feels copied despite changed names.",
      "repair": "Change profession, location, wardrobe, prop category, dialogue, and camera surface while preserving only the causal timing."
    }
  ],
  "transfer_tests": [
    {
      "concept": "A museum conservator stops an assistant's brush, lowers an ultraviolet inspection hood, and reveals branching fluorescent repairs before the camera follows the glow to the assistant's embarrassed recoil.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03"
      ],
      "changed_slots": [
        "authority_role",
        "recipient_role",
        "proof_state",
        "setting",
        "intervention",
        "reaction"
      ]
    },
    {
      "concept": "An observatory technician blocks a trainee from opening a dome, slides one red safety filter over the sensor, and reveals a dangerous solar flare before the camera follows the red reflection to the trainee's silent step back.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03"
      ],
      "changed_slots": [
        "authority_role",
        "recipient_role",
        "proof_state",
        "setting",
        "sound"
      ]
    }
  ]
}
````

### locales/zh-CN.json

````text
{
  "schema_version": "public-display-locale/v1",
  "resource_kind": "case",
  "resource_id": "reddit-1vhloyz-walter-prompt-guide",
  "locale": "zh-CN",
  "source_bindings": {
    "manifest_sha256": "a5ae7ca020d300a1fefac85629c7bb5845c2e383bba21447d6d4277b2e064c53",
    "creative_dna_sha256": "a5617663d6b9fc1eee39fcd54a14864886395bfc74c9fafd913f951e4c08ad8d"
  },
  "content": {
    "title": "风险揭晓｜证据交给人物反应",
    "summary": "一次干预阻止风险，可读证据随后由有动机的镜头交接给人物反应。",
    "quick_start": {
      "input_format": "紧急干预 + 隐藏风险 + 可视证据 + 有动机镜头交接 + 简短反应",
      "recommended_input": "实验员拦住同伴触碰容器，紫外光显出内部裂纹；镜头沿容器反光移交到同伴面部，他安静地收回手并点头。",
      "required_anchors": [
        "先有干预冲突",
        "风险通过可视证据证明",
        "镜头交接有物理动机",
        "反应简短且改变后续行为"
      ],
      "usage_steps": [
        "把示例主体、场景和表层元素替换为原创概念。",
        "让每个必需锚点和 Creative DNA 不可变条件都能在画面因果链中被看见。",
        "选择 MiniMax H3 或 Seedance 2.0 模板，只填写已声明的可替换项。",
        "生成前检查时长、事件顺序、镜头连续性、声音和反复制约束。"
      ],
      "applicable_scope": [
        "一次干预阻止风险，可读证据随后由有动机的镜头交接给人物反应。",
        "能够保留全部必需锚点的原创 4–15 秒短片。",
        "需要可复用因果视频结构的 MiniMax H3 或 Seedance 2.0 项目。"
      ],
      "not_suitable_for": [
        "要求复制来源人物、场景、道具、对白或镜头顺序的任务。",
        "无法在目标时长内展示全部必需锚点的概念。",
        "缺少紧凑因果链的长篇讲解或无关多地点叙事。"
      ]
    },
    "creative_dna": {
      "complexity": "moderate",
      "mechanism": "一次紧急干预先制造冲突，稳定可见的证据证明隐藏风险，随后由有动因的镜头交接把证据传递到被干预者的克制反应。",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "在揭露证据状态之前，通过行动建立紧急冲突。",
          "purpose": "创建一个直接的问题，并为后续证据的出现提供因果理由。",
          "ablation_failure": "以解释开场会消除紧张感，并把场景变成平淡的演示。",
          "evidence_ids": [
            "beat-01",
            "beat-02"
          ]
        },
        {
          "id": "inv-02",
          "rule": "在镜头切换前，保持证据状态视觉稳定足够长的时间，以便接收者理解。",
          "purpose": "使证据本身清晰可辨，同时保持其与表演的融合。",
          "ablation_failure": "在隐藏状况解决之前离开，会让干预显得武断。",
          "evidence_ids": [
            "beat-02",
            "obs-05"
          ]
        },
        {
          "id": "inv-03",
          "rule": "用一次有叙事动因的重新取景，把最后一句交给形成反差的第二位发言者。",
          "purpose": "把指导转化成两人之间的笑点，同时避免浪费补拍覆盖镜头。",
          "ablation_failure": "将镜头始终对准第一个发言者，会削弱反应的收束效果。",
          "evidence_ids": [
            "beat-03",
            "obs-02"
          ]
        }
      ],
      "slots": [
        {
          "name": "authority_role",
          "constraint": "视觉上果断的专家，有明确的指导理由。"
        },
        {
          "name": "recipient_role",
          "constraint": "一个对比鲜明的新手或同行，可以用简短的一句话回答。"
        },
        {
          "name": "proof_state",
          "constraint": "物理条件、仪器读数、光线变化或物体状态在视觉上变得明确，无需复制源作品的排版。"
        },
        {
          "name": "setting",
          "constraint": "一个上下文丰富的场景，在中近景人物背后清晰可辨。"
        },
        {
          "name": "intervention",
          "constraint": "在证据出现之前，一个简短的动作或台词可以阻止不安全或错误的行为。"
        },
        {
          "name": "reaction",
          "constraint": "一个手势，一句话，化解矛盾。"
        },
        {
          "name": "camera_handoff",
          "constraint": "由第二位说话者推动的一次横摇或剪辑切换。"
        },
        {
          "name": "sound",
          "constraint": "场地氛围加上不重叠的对话；不需要音乐。"
        }
      ],
      "anti_copy_exclusions": [
        "受保护的电视角色或演员肖像",
        "来源剧集的服装、载具、沙漠场景设定或调色",
        "来源角色声音及原样对白",
        "原样指南标题、脏话、取景构图或道具字体设计"
      ],
      "instantiations": [
        {
          "concept": "一位博物馆文物修复师伸手拦停助理的画笔，放下紫外检查罩，显出分支状荧光修复痕迹；镜头随紫外证据完成交接，转向助理尴尬的后缩。",
          "prompt_seed": "先用稳定的紫外证据证明伸手拦停的必要性，再让反射光引导镜头交接至助理后缩的反应。"
        },
        {
          "concept": "一名天文台技术人员阻止受训者打开圆顶，在传感器上滑动一个红色安全滤光片，并在镜头跟随红色反射至受训者无声后退之前显示出危险的太阳耀斑。",
          "prompt_seed": "冲突、光学证据和以反射引导的镜头切换，创造出紧凑的安全逆转。"
        },
        {
          "concept": "糕点师接住实习生的裱花袋，把糖温计转向光线，先用微距显出结晶，再把焦点转到放下托盘的实习生。",
          "prompt_seed": "触觉干预先由稳定的微距证据获得可信度，再通过焦点转移交接反应。"
        }
      ],
      "failure_modes": [
        {
          "failure": "证明状态变化太快，难以理解。",
          "repair": "在切换之前，在稳定的光线、焦点和空间环境下，将显示的条件保持至少两秒钟。"
        },
        {
          "failure": "对话重叠或听起来很匆忙。",
          "repair": "保留两条简短台词，在第一条完全结束后进行发言者切换，并删除多余动作。"
        },
        {
          "failure": "尽管改了名字，这个场景还是感觉被复制了。",
          "repair": "改变职业、地点、服装、道具类别、对话和镜头表层元素，同时仅保留因果时间。"
        }
      ],
      "transfer_tests": [
        {
          "concept": "一位博物馆文物修复师伸手拦停助理的画笔，放下紫外检查罩，显出分支状荧光修复痕迹；镜头随紫外证据完成交接，转向助理尴尬的后缩。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03"
          ],
          "changed_slots": [
            "authority_role",
            "recipient_role",
            "proof_state",
            "setting",
            "intervention",
            "reaction"
          ]
        },
        {
          "concept": "一名天文台技术人员阻止受训者打开圆顶，在传感器上滑动一个红色安全滤光片，并在镜头跟随红色反射至受训者无声后退之前显示出危险的太阳耀斑。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03"
          ],
          "changed_slots": [
            "authority_role",
            "recipient_role",
            "proof_state",
            "setting",
            "sound"
          ]
        }
      ]
    }
  },
  "review": {
    "status": "approved",
    "method": "source-bound offline bilingual editorial pass with field, terminology, evidence-token and structure validation; mechanism-level editorial pass; curated Chinese film-language glossary pass"
  }
}
````

### locales/en.json

````text
{
  "schema_version": "public-display-locale/v1",
  "resource_kind": "case",
  "resource_id": "reddit-1vhloyz-walter-prompt-guide",
  "locale": "en",
  "source_bindings": {
    "manifest_sha256": "a5ae7ca020d300a1fefac85629c7bb5845c2e383bba21447d6d4277b2e064c53",
    "creative_dna_sha256": "a5617663d6b9fc1eee39fcd54a14864886395bfc74c9fafd913f951e4c08ad8d"
  },
  "content": {
    "title": "Risk Revelation | Evidence Handoff",
    "summary": "An intervention stops the risk, and readable evidence is then handed over to character reactions through motivated shots.",
    "quick_start": {
      "input_format": "Emergency intervention + Hidden risk + Visual evidence + Motivated camera handoff + Brief response",
      "recommended_input": "The experimenter stops the companion from touching the container, and ultraviolet light reveals internal cracks; the camera follows the container's reflection to the companion's face, where he quietly withdraws his hand and nods.",
      "required_anchors": [
        "Intervention conflict first",
        "Risk is demonstrated through visual evidence",
        "Shot handoffs have physical motivations",
        "Respond briefly and alter subsequent behavior"
      ],
      "usage_steps": [
        "Replace the example subject, setting and surface details with an original concept.",
        "Keep every required anchor and Creative DNA invariant causally visible.",
        "Choose the MiniMax H3 or Seedance 2.0 prompt and fill only the declared variable slots.",
        "Check duration, event order, camera continuity, sound and anti-copy constraints before generation."
      ],
      "applicable_scope": [
        "An intervention stops the risk, and readable evidence is then handed over to character reactions by motivated shots.",
        "Original 4–15 second concepts that can preserve every required anchor.",
        "MiniMax H3 or Seedance 2.0 projects that need a reusable causal video structure."
      ],
      "not_suitable_for": [
        "Requests that copy the source identity, setting, props, dialogue or shot order.",
        "Concepts that cannot show all required anchors inside the target duration.",
        "Long-form exposition or unrelated multi-location stories without a compact causal chain."
      ]
    },
    "creative_dna": {
      "complexity": "moderate",
      "mechanism": "An urgent intervention creates conflict, a controlled visual proof makes the hidden risk undeniable, and one motivated camera handoff transfers that proof to the recipient's compact reaction.",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "Establish an urgent conflict through action before revealing the proof state.",
          "purpose": "Creates an immediate question and gives the later evidence a causal reason to appear.",
          "ablation_failure": "Opening on the explanation removes tension and turns the scene into a flat demonstration.",
          "evidence_ids": [
            "beat-01",
            "beat-02"
          ]
        },
        {
          "id": "inv-02",
          "rule": "Hold the proof state visually stable long enough to be understood before the camera hands off.",
          "purpose": "Makes the evidence itself readable while keeping it integrated with performance.",
          "ablation_failure": "Moving away before the hidden condition resolves makes the intervention feel arbitrary.",
          "evidence_ids": [
            "beat-02",
            "obs-05"
          ]
        },
        {
          "id": "inv-03",
          "rule": "Use one motivated reframe to hand the last line to a contrasting second speaker.",
          "purpose": "Converts instruction into a two-person joke without wasting time on coverage.",
          "ablation_failure": "Keeping the camera on the first speaker removes the reaction payoff.",
          "evidence_ids": [
            "beat-03",
            "obs-02"
          ]
        }
      ],
      "slots": [
        {
          "name": "authority_role",
          "constraint": "A visually decisive expert with a clear reason to instruct."
        },
        {
          "name": "recipient_role",
          "constraint": "A contrasting novice or peer who can answer in one short line."
        },
        {
          "name": "proof_state",
          "constraint": "A physical condition, instrument reading, light reveal, or object state that becomes visually unambiguous without copying source typography."
        },
        {
          "name": "setting",
          "constraint": "A context-rich location readable behind a medium close subject."
        },
        {
          "name": "intervention",
          "constraint": "One brief action or line that stops the unsafe or mistaken behavior before the proof appears."
        },
        {
          "name": "reaction",
          "constraint": "One gesture and one line that resolve the conflict."
        },
        {
          "name": "camera_handoff",
          "constraint": "One pan or cut motivated by the second speaker."
        },
        {
          "name": "sound",
          "constraint": "Location ambience plus non-overlapping dialogue; no music required."
        }
      ],
      "anti_copy_exclusions": [
        "protected television characters or actor likenesses",
        "source-series wardrobe, vehicle, desert setup, or color grade",
        "source-character voices and exact dialogue",
        "exact guide title, profanity, framing, or prop typography"
      ],
      "instantiations": [
        {
          "concept": "A museum conservator stops an assistant's brush, lowers an ultraviolet inspection hood, and reveals branching fluorescent repairs before the camera follows the glow to the assistant's embarrassed recoil.",
          "prompt_seed": "An urgent hand-stop becomes justified by a stable ultraviolet proof, then the reflected glow motivates the reaction handoff."
        },
        {
          "concept": "An observatory technician blocks a trainee from opening a dome, slides one red safety filter over the sensor, and reveals a dangerous solar flare before the camera follows the red reflection to the trainee's silent step back.",
          "prompt_seed": "Conflict, optical proof, and a reflection-led camera handoff create a compact safety reversal."
        },
        {
          "concept": "A pastry chef catches a trainee's piping bag, turns a sugar thermometer toward the light, and reveals crystallization in macro before the lens rack-focuses to the trainee lowering the tray.",
          "prompt_seed": "A tactile intervention earns credibility through a stable macro proof and a focus-driven reaction handoff."
        }
      ],
      "failure_modes": [
        {
          "failure": "The proof state changes too quickly to understand.",
          "repair": "Hold the revealed condition for at least two seconds with stable light, focus, and spatial context before the handoff."
        },
        {
          "failure": "Dialogue overlaps or sounds rushed.",
          "repair": "Keep two short lines, place the speaker handoff after the first line fully ends, and remove extra actions."
        },
        {
          "failure": "The scene feels copied despite changed names.",
          "repair": "Change profession, location, wardrobe, prop category, dialogue, and camera surface while preserving only the causal timing."
        }
      ],
      "transfer_tests": [
        {
          "concept": "A museum conservator stops an assistant's brush, lowers an ultraviolet inspection hood, and reveals branching fluorescent repairs before the camera follows the glow to the assistant's embarrassed recoil.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03"
          ],
          "changed_slots": [
            "authority_role",
            "recipient_role",
            "proof_state",
            "setting",
            "intervention",
            "reaction"
          ]
        },
        {
          "concept": "An observatory technician blocks a trainee from opening a dome, slides one red safety filter over the sensor, and reveals a dangerous solar flare before the camera follows the red reflection to the trainee's silent step back.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03"
          ],
          "changed_slots": [
            "authority_role",
            "recipient_role",
            "proof_state",
            "setting",
            "sound"
          ]
        }
      ]
    }
  },
  "review": {
    "status": "approved",
    "method": "canonical-source offline English editorial pass with terminology and stable-token validation; title naming editorial pass"
  }
}
````

### manifest.json

````text
{
  "schema_version": "public-case/v1",
  "case_id": "reddit-1vhloyz-walter-prompt-guide",
  "slug": "direct-proof-state-handoff",
  "title": "风险揭晓｜证据交给人物反应",
  "source_title": "Walter White and the MiniMax H3 official prompting guide",
  "summary": "一次干预阻止风险，可读证据随后由有动机的镜头交接给人物反应。",
  "status": "released",
  "source_duration_seconds": 14.42,
  "target_duration_seconds": 15.0,
  "models": [
    "MiniMax H3",
    "Seedance 2.0"
  ],
  "source_ref": "source.json",
  "creative_dna_ref": "creative-dna.json",
  "summary_ref": "SUMMARY.md",
  "prompt_refs": {
    "minimax_h3": "prompts/minimax-h3.md",
    "seedance_2_0": "prompts/seedance-2.0.md"
  },
  "skill_ref": "../../../skills/direct-proof-state-handoff",
  "preview_refs": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/reddit-1vhloyz-walter-prompt-guide/preview.mp4"
  },
  "preview_paths": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/reddit-1vhloyz-walter-prompt-guide/preview.mp4"
  },
  "preview_status": {
    "gif": "available",
    "poster": "available",
    "mp4": "available_in_electron_media_pack"
  },
  "template_id": "t8c007-proof-object-reaction-handoff",
  "template_action": "selector",
  "duplicate_of": null,
  "input_format": "紧急干预 + 隐藏风险 + 可视证据 + 有动机镜头交接 + 简短反应",
  "recommended_input": "实验员拦住同伴触碰容器，紫外光显出内部裂纹；镜头沿容器反光移交到同伴面部，他安静地收回手并点头。",
  "required_anchors": [
    "先有干预冲突",
    "风险通过可视证据证明",
    "镜头交接有物理动机",
    "反应简短且改变后续行为"
  ],
  "tags": [
    "t8c007",
    "proof",
    "object",
    "reaction",
    "handoff"
  ],
  "quality": {
    "weighted_score": 4.674,
    "scale": 5,
    "anti_copy_passed": true,
    "prompt_validation": {
      "minimax_h3": true,
      "seedance_2_0": true
    },
    "release_passed": true
  },
  "created_at": "2026-08-09T01:34:53+08:00",
  "updated_at": "2026-08-09T18:06:12+08:00"
}
````

### prompts/minimax-h3.md

````text
---
schema_version: "public-prompt/v1"
case_id: "reddit-1vhloyz-walter-prompt-guide"
model: "MiniMax H3"
duration_seconds: 15
language: "en"
validation: "passed"
---

# 风险揭晓｜证据交给人物反应 — MiniMax H3

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
integrated_multimodal_description: [Shot 1] Cinematic live-action conservation-lab realism, natural skin and linen texture, quiet museum precision, soft neutral task light transitioning to controlled ultraviolet blue-violet illumination, shallow macro depth, stable hands and artifact continuity. A slow lateral slider shot crosses a quiet museum conservation table from left to right. An adult assistant in a slate linen coat brings a soft brush toward a faded botanical textile under glass. Before the bristles touch, a senior conservator in a cream lab jacket gently catches the assistant's wrist in profile and says, <d>[English in a calm adult female voice] Wait. The blue thread is not original.</d> Neither person looks at the camera. [Shot 2] At 00:04.600, Cut to a top-down three-quarter view. The conservator releases the wrist and lowers a hinged ultraviolet inspection hood over the textile. Neutral task lights dim as one violet strip switches on. The assistant's brush stays suspended outside the hood, and the faded surface remains still while the illumination settles. [Shot 3] At 00:07.400, The camera makes a slow macro push along the textile. Under ultraviolet light, a branching network of later repair stitches fluoresces electric cyan while the original fibers remain muted indigo. Hold the crisp boundary for two seconds; the conservator points once beside, never on, the glowing repair. No text, paper, direct address, or repeated command appears. [Shot 4] At 00:10.400, The lens follows a cyan reflection traveling across the acrylic shield, then rack-focuses through it to the assistant on the far side. The conservator remains only as a soft shoulder shape. The assistant slowly withdraws the brush, places it into a dry tray, lowers their chin, and says after focus settles, <d>[English in a quiet younger adult voice] I see it. Air only.</d> Hold on the reflected cyan branches crossing the assistant's protective glasses.

overall_soundscape: Low conservation-lab ventilation, soft sleeve and brush fibers, a gentle hood hinge, one ultraviolet ballast click, and clean non-overlapping dialogue from the visible speaker. The reveal is accompanied only by a subtle glassy electrical hum that stops before the final line.

non_diegetic_music: None
```

## 使用检查

- 保留因果机制与结构锚点，不复刻来源人物、地点、道具、构图或标志性效果。
- 核对主体身份、空间关系、事件先后、运镜职责与最终状态。
- 新用途应返回 [Creative DNA](../creative-dna.json) 重新实例化。
````

### prompts/seedance-2.0.md

````text
---
schema_version: "public-prompt/v1"
case_id: "reddit-1vhloyz-walter-prompt-guide"
model: "Seedance 2.0"
duration_seconds: 15
language: "zh"
validation: "passed"
---

# 风险揭晓｜证据交给人物反应 — Seedance 2.0

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
任务：文本生成新视频。
总时长约15秒，仅控制整体信息密度，不分配逐镜头秒数。
主体定义：资深修复师：成年女性、奶油色实验夹克、透明护目镜、动作轻而准确，始终称为资深修复师；成年助理：年轻成年人、石板灰亚麻外套、手持软毛刷，动作谨慎，始终称为成年助理。
镜头1：沿修复桌从左向右缓慢横移的侧面中景，不使用主观机位；成年助理把软毛刷伸向玻璃下的褪色植物纹样织物，刷毛尚未接触时，资深修复师从侧面轻轻扣住助理手腕并说：‘等一下，蓝色线不是原织物。’两人都不看镜头；织物占画面下半部，助理在右，资深修复师从左侧介入，刷毛与织物保持可见空隙；中性柔和工作灯，自然肤色与亚麻质感，织物为低饱和靛蓝和褪色植物色；<低声通风><衣袖轻擦><刷毛细响>，对白清晰且无音乐。
镜头2：切到三分之四俯拍，完整看见织物、紫外检测罩和悬停的刷子；资深修复师松开手腕并缓慢放下铰链式紫外检测罩；中性工作灯变暗，罩内一条紫色灯带点亮，成年助理把刷子停在罩外；检测罩覆盖织物中央，刷子不进入罩内，手部不遮挡织物纹理；中性光平滑过渡到蓝紫紫外光，周围环境不过暗；<铰链轻响><紫外灯启动咔嗒><轻微电气低鸣>。
镜头3：先沿织物做缓慢微距推进，稳定展示荧光修补线两秒，再跟随亚克力挡板上的青色反光并拉焦到对面的成年助理；紫外光下，后期修补线形成分叉的电青色荧光网，原织物保持暗靛蓝；资深修复师只在荧光线旁指一次且不接触。反光移动到成年助理护目镜后，成年助理慢慢收回刷子，放进干燥托盘，低头说：‘看到了，只用气流。’；微距阶段荧光边界清楚；拉焦后资深修复师只保留为虚化肩部，成年助理和托盘完整入画；电青色荧光只来自修补线及其反射，原织物结构和位置完全不变；<持续轻微电气低鸣>在拉焦前停止；第二句在画面稳定后开始，结尾留修复室底噪。
整体风格与画质：电影感真人博物馆修复室写实，自然皮肤、亚麻和古织物质感，中性工作光向受控蓝紫紫外光平滑转换，微距景深精确；稳定人物身份、手部和织物纹理；刷毛不穿透玻璃；荧光修补线位置连续；反光、跟随和拉焦有明确动机；对白不抢不叠。
约束：不得使用任何影视角色、演员肖像、系列服装、原作对白或声音模仿；不得出现沙漠、车辆、防护服、纸质指南、指向镜头、直视观众、摇晃道具、文字、字幕、Logo或水印；紫外光开启前后织物几何完全一致，只允许修补线荧光发生变化；两位说话人的对白严格串行，不增加额外切镜。
```

## 使用检查

- 保留因果机制与结构锚点，不复刻来源人物、地点、道具、构图或标志性效果。
- 核对主体身份、空间关系、事件先后、运镜职责与最终状态。
- 新用途应返回 [Creative DNA](../creative-dna.json) 重新实例化。
````

### source.json

````text
{
  "schema_version": "public-source/v1",
  "case_id": "reddit-1vhloyz-walter-prompt-guide",
  "platform": "reddit",
  "author": "GrayingGamer",
  "source_title": "Walter White and the MiniMax H3 official prompting guide",
  "source_post_id": "1vhloyz",
  "canonical_url": "https://www.reddit.com/r/StableDiffusion/comments/1vhloyz/walter_white_and_the_minimax_h3_official/",
  "published_at": null,
  "model_attribution": {
    "model": "MiniMax H3",
    "status": "creator_claimed",
    "basis": "Creator identifies the default H3 T2V workflow."
  },
  "video_reference": {
    "platform": "reddit",
    "author": "GrayingGamer",
    "post_url": "https://www.reddit.com/r/StableDiffusion/comments/1vhloyz/walter_white_and_the_minimax_h3_official/",
    "playback_mode": "source_post",
    "preview_gif": "./preview.gif",
    "preview_mp4": "media/reddit-1vhloyz-walter-prompt-guide/preview.mp4",
    "poster": "./poster.webp",
    "preview_status": {
      "gif": "available",
      "poster": "available",
      "mp4": "available_in_electron_media_pack"
    },
    "fallback_mode": "open_original_post"
  }
}
````

