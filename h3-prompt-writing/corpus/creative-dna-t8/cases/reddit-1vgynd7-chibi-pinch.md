# reddit-1vgynd7-chibi-pinch

- 类型：案例原文（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SUMMARY.md

````text
# 二维角色｜真人接触三级反应

真实世界一次接触触发平面角色的三级反应，并以媒介自身的变化收尾。

## 核心机制

A single flat 2D character shares a locked photoreal environment with a real hand; one small cross-medium contact causes a three-stage readable reaction that ends in a medium-specific impossible effect.

## 推荐输入格式

`平面角色 + 真实场景 + 一次跨媒介接触 + 三级反应 + 媒介专属结尾`

## 简短示例

> 书桌贴纸上的纸片机器人被真人手指轻触：先轻颤，再鼓起并喷出纸屑火花，最后整张桌垫折成通往它的纸桥。

## 必须保留的结构锚点

- 平面与真实媒介同框
- 只有一次关键接触
- 反应至少三级升级
- 结尾由平面媒介自身完成

## 使用方法

1. 先保留用户主体和目标，再按推荐格式补齐场景、事件链、镜头和结果。
2. 阅读 [Creative DNA](./creative-dna.json)，重新实例化变量，不做来源表面换名词。
3. 分别查看 [MiniMax H3](./prompts/minimax-h3.md) 与 [Seedance 2.0](./prompts/seedance-2.0.md) 的已验证实例。
4. GitHub 使用 GIF 快速预览；Electron 媒体包播放完整有声 MP4。

## 来源与署名

- 平台：reddit
- 作者：Devajyoti1231
- 原始视频：[打开来源](https://www.reddit.com/r/StableDiffusion/comments/1vgynd7/2d_chibi_girl_added_just_a_pinch_minimax_h3/)
- 模型归因：MiniMax H3（creator_claimed）

来源视频用于机制研究与引用；公开模板只保留可迁移因果，不要求复刻来源人物、道具、场景、构图、对白或标志性效果。
````

### creative-dna.json

````text
{
  "complexity": "moderate",
  "mechanism": "A single flat 2D character shares a locked photoreal environment with a real hand; one small cross-medium contact causes a three-stage readable reaction that ends in a medium-specific impossible effect.",
  "invariants": [
    {
      "id": "inv-01",
      "rule": "Keep exactly one flat animated character inside an otherwise photoreal, stable environment.",
      "purpose": "Makes the mixed-medium anomaly instantly legible.",
      "ablation_failure": "Multiple animated elements blur the boundary and weaken the hook.",
      "evidence_ids": [
        "beat-01",
        "obs-02"
      ]
    },
    {
      "id": "inv-02",
      "rule": "Show real-to-animated contact before the reaction begins.",
      "purpose": "Provides a causal bridge between media layers.",
      "ablation_failure": "A reaction without contact feels like an unrelated animation loop.",
      "evidence_ids": [
        "beat-02",
        "obs-04"
      ]
    },
    {
      "id": "inv-03",
      "rule": "Escalate in three readable states: neutral, discomfort, impossible payoff.",
      "purpose": "Lets the audience track cause and intensity without cuts.",
      "ablation_failure": "Jumping directly to the final effect removes anticipation and acting.",
      "evidence_ids": [
        "beat-03",
        "beat-04"
      ]
    },
    {
      "id": "inv-04",
      "rule": "Keep the camera locked and let contact, expression, and effects move attention.",
      "purpose": "Protects spatial continuity between real and animated layers.",
      "ablation_failure": "Camera movement makes contact alignment harder to read.",
      "evidence_ids": [
        "obs-07",
        "obs-08"
      ]
    }
  ],
  "slots": [
    {
      "name": "photoreal_arena",
      "constraint": "A stable real location with clear depth and one interaction surface."
    },
    {
      "name": "flat_character",
      "constraint": "One original 2D paper- or sticker-like adult mascot, visually distinct from the source."
    },
    {
      "name": "real_agent",
      "constraint": "One live-action hand or tool entering from a consistent edge."
    },
    {
      "name": "contact_object",
      "constraint": "A small real object whose motion can visibly cross the medium boundary."
    },
    {
      "name": "sensation",
      "constraint": "A simple cause such as cold, static, scent, or weight, not source heat/chili."
    },
    {
      "name": "reaction_states",
      "constraint": "Three visually distinct but causally continuous poses."
    },
    {
      "name": "payoff_effect",
      "constraint": "An original safe effect appropriate to the new sensation."
    },
    {
      "name": "sound",
      "constraint": "Real location ambience plus contact-synced foley and one effect accent."
    }
  ],
  "anti_copy_exclusions": [
    "source girl character, hairstyle, clothes, face, outline, or childlike proportions",
    "source kitchen, wok, food, seasoning jar, spoon interaction, and camera composition",
    "chili or heat tasting, lateral tear jets, red forehead, and fire breathing",
    "exact reaction timing and source visual effects"
  ],
  "instantiations": [
    {
      "concept": "A flat 2D alpine-fox sticker at a real tea counter receives one drop of mint extract, sips, shivers, and exhales a small frost cloud that freezes a spoon.",
      "prompt_seed": "One real mint drop crosses into a flat sticker character's cup, causing a three-stage cold reaction and a spoon-freezing payoff."
    },
    {
      "concept": "A flat 2D robot sticker at a real workbench receives one drop of lubricant, tests a hinge, spins with the over-loose joint, and stops with a dizzy status-light pattern.",
      "prompt_seed": "One real lubricant drop causes a clear neutral-to-surprise-to-spin reaction in a flat robot sticker."
    },
    {
      "concept": "A flat 2D botanist sticker in a real greenhouse touches one pollen grain, sneezes through two escalating poses, and releases a tiny animated cloud shaped like leaves.",
      "prompt_seed": "A real pollen contact triggers a three-stage sticker-character sneeze and an original leaf-cloud payoff."
    }
  ],
  "failure_modes": [
    {
      "failure": "The animated character no longer looks flat against the real scene.",
      "repair": "Keep constant paper thickness, a crisp outline, planar deformation, and a consistent contact shadow."
    },
    {
      "failure": "The reaction begins before contact.",
      "repair": "Hold neutral expression through the contact frame, then delay the first change by a short readable beat."
    },
    {
      "failure": "The adaptation still feels like the source spicy-food gag.",
      "repair": "Change arena, character category, contact object, sensation, palette, reaction graphics, and final effect together."
    }
  ],
  "transfer_tests": [
    {
      "concept": "A flat 2D alpine-fox sticker at a real tea counter receives one drop of mint extract, sips, shivers, and exhales a small frost cloud that freezes a spoon.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04"
      ],
      "changed_slots": [
        "photoreal_arena",
        "flat_character",
        "contact_object",
        "sensation",
        "reaction_states",
        "payoff_effect"
      ]
    },
    {
      "concept": "A flat 2D robot sticker at a real workbench receives one drop of lubricant, tests a hinge, spins with the over-loose joint, and stops with a dizzy status-light pattern.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04"
      ],
      "changed_slots": [
        "photoreal_arena",
        "flat_character",
        "real_agent",
        "contact_object",
        "sensation",
        "payoff_effect"
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
  "resource_id": "reddit-1vgynd7-chibi-pinch",
  "locale": "zh-CN",
  "source_bindings": {
    "manifest_sha256": "e17d2e299af27b1cf75d10e7d284babff6d550db68d55afe634b1a233099a16f",
    "creative_dna_sha256": "ed8631e6ac8fad89a7c56ac94eb4a4d0d91b33c73e90ae72a659fe5337bb8de3"
  },
  "content": {
    "title": "二维角色｜真人接触三级反应",
    "summary": "真实世界一次接触触发平面角色的三级反应，并以媒介自身的变化收尾。",
    "quick_start": {
      "input_format": "平面角色 + 真实场景 + 一次跨媒介接触 + 三级反应 + 媒介专属结尾",
      "recommended_input": "书桌贴纸上的纸片机器人被真人手指轻触：先轻颤，再鼓起并喷出纸屑火花，最后整张桌垫折成通往它的纸桥。",
      "required_anchors": [
        "平面与真实媒介同框",
        "只有一次关键接触",
        "反应至少三级升级",
        "结尾由平面媒介自身完成"
      ],
      "usage_steps": [
        "把示例主体、场景和表层元素替换为原创概念。",
        "让每个必需锚点和 Creative DNA 不可变条件都能在画面因果链中被看见。",
        "选择 MiniMax H3 或 Seedance 2.0 模板，只填写已声明的可替换项。",
        "生成前检查时长、事件顺序、镜头连续性、声音和反复制约束。"
      ],
      "applicable_scope": [
        "真实世界一次接触触发平面角色的三级反应，并以媒介自身的变化收尾。",
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
      "mechanism": "单个平面 2D角色与真人手共享固定机位下的写实环境；一个小的跨媒介接触会引起三阶段的清晰可辨的反应，最终导致媒介特有的超现实效果。",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "在一个写实且稳定的环境中仅保留一个平面动画角色。",
          "purpose": "使混合媒介异常立即清晰可见。",
          "ablation_failure": "多个动画元素模糊了边界，削弱了吸引力。",
          "evidence_ids": [
            "beat-01",
            "obs-02"
          ]
        },
        {
          "id": "inv-02",
          "rule": "在反应开始之前显示真人与动画角色之间的接触。",
          "purpose": "在媒介层之间提供因果桥梁。",
          "ablation_failure": "没有接触的反应感觉就像一个不相关的动画循环。",
          "evidence_ids": [
            "beat-02",
            "obs-04"
          ]
        },
        {
          "id": "inv-03",
          "rule": "升级为三种清晰可辨的状态：中性、不适、不可能收束效果。",
          "purpose": "让观众无需剪辑就能追踪原因和强度。",
          "ablation_failure": "直接跳转到最终效果会消除预期和表演。",
          "evidence_ids": [
            "beat-03",
            "beat-04"
          ]
        },
        {
          "id": "inv-04",
          "rule": "保持固定机位，让接触、表情和效果引起注意。",
          "purpose": "保持真人层与动画层之间的空间连续性。",
          "ablation_failure": "相机的移动使接触对准更难以读取。",
          "evidence_ids": [
            "obs-07",
            "obs-08"
          ]
        }
      ],
      "slots": [
        {
          "name": "photoreal_arena",
          "constraint": "一个稳定的真实位置，具有清晰的深度和一个交互表面。"
        },
        {
          "name": "flat_character",
          "constraint": "一种原创的2D纸质或贴纸状成人吉祥物，在视觉上与来源不同。"
        },
        {
          "name": "real_agent",
          "constraint": "一只真人手或工具从一致的边缘进入。"
        },
        {
          "name": "contact_object",
          "constraint": "一个小的真实物体，其运动可以明显地跨越媒介边界。"
        },
        {
          "name": "sensation",
          "constraint": "原因保持单一，例如寒冷、静电、气味或重量；不要复刻来源样片的辣味或高温刺激。"
        },
        {
          "name": "reaction_states",
          "constraint": "三个视觉上不同但因果上连续的姿势。"
        },
        {
          "name": "payoff_effect",
          "constraint": "适合新感觉的原创安全效果。"
        },
        {
          "name": "sound",
          "constraint": "真实的位置氛围加上接触同步拟音和一种效果强调音。"
        }
      ],
      "anti_copy_exclusions": [
        "来源女孩角色、发型、服装、面部、轮廓或幼童化身体比例",
        "来源厨房、炒锅、食物、调料罐、勺子互动、相机构图",
        "辣椒或灼热味觉、横向喷射的泪柱、额头发红或喷火",
        "与来源作品完全相同的反应时序和视觉特效"
      ],
      "instantiations": [
        {
          "concept": "真实茶饮柜台上的平面 2D 高山狐狸贴纸接到一滴薄荷提取液，先小口啜饮，再发抖，最后呼出一小团霜雾并冻住一把勺子。",
          "prompt_seed": "一滴来自真实世界的薄荷提取液落入平面贴纸角色的杯中，引发中性、寒颤、霜雾爆发三个连续状态，并以冻住勺子收尾。"
        },
        {
          "concept": "真实工作台上的平面 2D 机器人贴纸接受一滴润滑剂，测试铰链，随着过度松动的接头旋转，并以令人眼花缭乱的状态灯图案停止。",
          "prompt_seed": "现实层的一滴润滑剂落到平面机器人贴纸上，引发中性、惊讶、失控旋转三个清楚阶段。"
        },
        {
          "concept": "现实温室中的平面 2D 植物学家贴纸接触一粒花粉，经历两次逐步加剧的喷嚏姿势，最后释放一小团叶片状动画云。",
          "prompt_seed": "现实层的一粒花粉触发贴纸角色的三阶段喷嚏反应，并以原创叶片状云团收尾。"
        }
      ],
      "failure_modes": [
        {
          "failure": "动画角色在真实场景中看起来不再平坦。",
          "repair": "保持恒定的纸张厚度、清晰的轮廓、平面变形和一致的接触阴影。"
        },
        {
          "failure": "反应在接触之前就开始了。",
          "repair": "通过接触发生的画面保持中性表情，然后通过短的清晰可辨的短暂停顿延迟第一次变化。"
        },
        {
          "failure": "这次改编仍像在照搬来源作品中的辛辣食物笑点。",
          "repair": "一起更改场景、角色类别、接触对象、感觉、调色板、反应图形和最终效果。"
        }
      ],
      "transfer_tests": [
        {
          "concept": "真实茶饮柜台上的平面 2D 高山狐狸贴纸接到一滴薄荷提取液，先小口啜饮，再发抖，最后呼出一小团霜雾并冻住一把勺子。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04"
          ],
          "changed_slots": [
            "photoreal_arena",
            "flat_character",
            "contact_object",
            "sensation",
            "reaction_states",
            "payoff_effect"
          ]
        },
        {
          "concept": "真实工作台上的平面 2D 机器人贴纸接受一滴润滑剂，测试铰链，随着过度松动的接头旋转，并以令人眼花缭乱的状态灯图案停止。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04"
          ],
          "changed_slots": [
            "photoreal_arena",
            "flat_character",
            "real_agent",
            "contact_object",
            "sensation",
            "payoff_effect"
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
  "resource_id": "reddit-1vgynd7-chibi-pinch",
  "locale": "en",
  "source_bindings": {
    "manifest_sha256": "e17d2e299af27b1cf75d10e7d284babff6d550db68d55afe634b1a233099a16f",
    "creative_dna_sha256": "ed8631e6ac8fad89a7c56ac94eb4a4d0d91b33c73e90ae72a659fe5337bb8de3"
  },
  "content": {
    "title": "2D Character | Contact Reaction Progression",
    "summary": "A single contact with the real world triggers a three-stage reaction in the 2D character and ends with a change in the medium itself.",
    "quick_start": {
      "input_format": "Flat character + real scene + a cross-media contact + three-stage reaction + media-specific ending",
      "recommended_input": "The paper robot on the desk sticker is touched by a real finger: it first trembles, then swells up and sprays out paper confetti sparks, and finally the entire desk pad folds into a paper bridge leading to it.",
      "required_anchors": [
        "Flat and real media in the same frame",
        "Only one critical contact",
        "At least three escalating reaction stages",
        "The ending is completed by the flat medium itself"
      ],
      "usage_steps": [
        "Replace the example subject, setting and surface details with an original concept.",
        "Keep every required anchor and Creative DNA invariant causally visible.",
        "Choose the MiniMax H3 or Seedance 2.0 prompt and fill only the declared variable slots.",
        "Check duration, event order, camera continuity, sound and anti-copy constraints before generation."
      ],
      "applicable_scope": [
        "A single contact with the real world triggers a three-stage reaction in the 2D character and ends with a change in the medium itself.",
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
      "mechanism": "A single flat 2D character shares a locked photoreal environment with a real hand; one small cross-medium contact causes a three-stage readable reaction that ends in a medium-specific impossible effect.",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "Keep exactly one flat animated character inside an otherwise photoreal, stable environment.",
          "purpose": "Makes the mixed-medium anomaly instantly legible.",
          "ablation_failure": "Multiple animated elements blur the boundary and weaken the hook.",
          "evidence_ids": [
            "beat-01",
            "obs-02"
          ]
        },
        {
          "id": "inv-02",
          "rule": "Show real-to-animated contact before the reaction begins.",
          "purpose": "Provides a causal bridge between media layers.",
          "ablation_failure": "A reaction without contact feels like an unrelated animation loop.",
          "evidence_ids": [
            "beat-02",
            "obs-04"
          ]
        },
        {
          "id": "inv-03",
          "rule": "Escalate in three readable states: neutral, discomfort, impossible payoff.",
          "purpose": "Lets the audience track cause and intensity without cuts.",
          "ablation_failure": "Jumping directly to the final effect removes anticipation and acting.",
          "evidence_ids": [
            "beat-03",
            "beat-04"
          ]
        },
        {
          "id": "inv-04",
          "rule": "Keep the camera locked and let contact, expression, and effects move attention.",
          "purpose": "Protects spatial continuity between real and animated layers.",
          "ablation_failure": "Camera movement makes contact alignment harder to read.",
          "evidence_ids": [
            "obs-07",
            "obs-08"
          ]
        }
      ],
      "slots": [
        {
          "name": "photoreal_arena",
          "constraint": "A stable real location with clear depth and one interaction surface."
        },
        {
          "name": "flat_character",
          "constraint": "One original 2D paper- or sticker-like adult mascot, visually distinct from the source."
        },
        {
          "name": "real_agent",
          "constraint": "One live-action hand or tool entering from a consistent edge."
        },
        {
          "name": "contact_object",
          "constraint": "A small real object whose motion can visibly cross the medium boundary."
        },
        {
          "name": "sensation",
          "constraint": "A simple cause such as cold, static, scent, or weight, not source heat/chili."
        },
        {
          "name": "reaction_states",
          "constraint": "Three visually distinct but causally continuous poses."
        },
        {
          "name": "payoff_effect",
          "constraint": "An original safe effect appropriate to the new sensation."
        },
        {
          "name": "sound",
          "constraint": "Real location ambience plus contact-synced foley and one effect accent."
        }
      ],
      "anti_copy_exclusions": [
        "source girl character, hairstyle, clothes, face, outline, or childlike proportions",
        "source kitchen, wok, food, seasoning jar, spoon interaction, and camera composition",
        "chili or heat tasting, lateral tear jets, red forehead, and fire breathing",
        "exact reaction timing and source visual effects"
      ],
      "instantiations": [
        {
          "concept": "A flat 2D alpine-fox sticker at a real tea counter receives one drop of mint extract, sips, shivers, and exhales a small frost cloud that freezes a spoon.",
          "prompt_seed": "One real mint drop crosses into a flat sticker character's cup, causing a three-stage cold reaction and a spoon-freezing payoff."
        },
        {
          "concept": "A flat 2D robot sticker at a real workbench receives one drop of lubricant, tests a hinge, spins with the over-loose joint, and stops with a dizzy status-light pattern.",
          "prompt_seed": "One real lubricant drop causes a clear neutral-to-surprise-to-spin reaction in a flat robot sticker."
        },
        {
          "concept": "A flat 2D botanist sticker in a real greenhouse touches one pollen grain, sneezes through two escalating poses, and releases a tiny animated cloud shaped like leaves.",
          "prompt_seed": "A real pollen contact triggers a three-stage sticker-character sneeze and an original leaf-cloud payoff."
        }
      ],
      "failure_modes": [
        {
          "failure": "The animated character no longer looks flat against the real scene.",
          "repair": "Keep constant paper thickness, a crisp outline, planar deformation, and a consistent contact shadow."
        },
        {
          "failure": "The reaction begins before contact.",
          "repair": "Hold neutral expression through the contact frame, then delay the first change by a short readable beat."
        },
        {
          "failure": "The adaptation still feels like the source spicy-food gag.",
          "repair": "Change arena, character category, contact object, sensation, palette, reaction graphics, and final effect together."
        }
      ],
      "transfer_tests": [
        {
          "concept": "A flat 2D alpine-fox sticker at a real tea counter receives one drop of mint extract, sips, shivers, and exhales a small frost cloud that freezes a spoon.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04"
          ],
          "changed_slots": [
            "photoreal_arena",
            "flat_character",
            "contact_object",
            "sensation",
            "reaction_states",
            "payoff_effect"
          ]
        },
        {
          "concept": "A flat 2D robot sticker at a real workbench receives one drop of lubricant, tests a hinge, spins with the over-loose joint, and stops with a dizzy status-light pattern.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04"
          ],
          "changed_slots": [
            "photoreal_arena",
            "flat_character",
            "real_agent",
            "contact_object",
            "sensation",
            "payoff_effect"
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
  "case_id": "reddit-1vgynd7-chibi-pinch",
  "slug": "create-cross-medium-reaction",
  "title": "二维角色｜真人接触三级反应",
  "source_title": "2D chibi girl added ‘Just a Pinch’ — MiniMax H3",
  "summary": "真实世界一次接触触发平面角色的三级反应，并以媒介自身的变化收尾。",
  "status": "released",
  "source_duration_seconds": 10.154,
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
  "skill_ref": "../../../skills/create-cross-medium-reaction",
  "preview_refs": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/reddit-1vgynd7-chibi-pinch/preview.mp4"
  },
  "preview_paths": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/reddit-1vgynd7-chibi-pinch/preview.mp4"
  },
  "preview_status": {
    "gif": "available",
    "poster": "available",
    "mp4": "available_in_electron_media_pack"
  },
  "template_id": "t8c005-cross-medium-contact-reaction",
  "template_action": "selector",
  "duplicate_of": null,
  "input_format": "平面角色 + 真实场景 + 一次跨媒介接触 + 三级反应 + 媒介专属结尾",
  "recommended_input": "书桌贴纸上的纸片机器人被真人手指轻触：先轻颤，再鼓起并喷出纸屑火花，最后整张桌垫折成通往它的纸桥。",
  "required_anchors": [
    "平面与真实媒介同框",
    "只有一次关键接触",
    "反应至少三级升级",
    "结尾由平面媒介自身完成"
  ],
  "tags": [
    "t8c005",
    "cross",
    "medium",
    "contact",
    "reaction"
  ],
  "quality": {
    "weighted_score": 4.693,
    "scale": 5,
    "anti_copy_passed": true,
    "prompt_validation": {
      "minimax_h3": true,
      "seedance_2_0": true
    },
    "release_passed": true
  },
  "created_at": "2026-08-09T01:34:52+08:00",
  "updated_at": "2026-08-09T18:06:11+08:00"
}
````

### prompts/minimax-h3.md

````text
---
schema_version: "public-prompt/v1"
case_id: "reddit-1vgynd7-chibi-pinch"
model: "MiniMax H3"
duration_seconds: 15
language: "en"
validation: "passed"
---

# 二维角色｜真人接触三级反应 — MiniMax H3

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
integrated_multimodal_description: [Shot 1] Mixed-media live action with one original flat 2D paper-sticker adult alpine-fox mascot, a photoreal quiet tea counter, soft winter daylight, crisp planar character deformation, stable white sticker outline, consistent contact shadow, cool cyan accents, and no resemblance to existing characters. A continuous locked medium shot frames a photoreal wooden tea counter beside a softly lit winter window. Exactly one animated element exists: an original flat 2D paper-sticker adult alpine-fox mascot standing upright on the counter, wearing a plain navy scarf and holding a small photoreal ceramic cup with both flat paws. A real adult hand enters slowly from frame right holding a clear glass dropper above the cup. [Shot 2] At 00:03.000, The hand squeezes exactly one pale blue mint drop. The droplet falls through the real air, lands visibly in the tea, and creates one small circular ripple. The sticker fox watches the drop, waits for the ripple to settle, then raises the cup and takes one careful sip. The real hand withdraws along the same path and leaves frame. [Shot 3] At 00:07.000, The fox lowers the cup. First reaction state: its eyes widen, ears lift, and shoulders rise in one small shiver. A faint cyan tint appears only on the nose. The flat body and white sticker outline remain stable against the photoreal counter. [Shot 4] At 00:09.600, Second reaction state: the fox shivers twice with larger planar side-to-side motion, pulls the navy scarf tight, and chatters its teeth. Thin frost traces grow from the edge of the ceramic cup toward the handle while the cup rattles lightly against the counter. Do not add tears, heat glow, or flame. [Shot 5] At 00:12.100, Final reaction state: the fox takes one breath and exhales a compact translucent frost cloud toward a photoreal metal teaspoon resting on a saucer at frame left. Frost visibly travels across the spoon from bowl to handle and stops. The fox freezes in embarrassed surprise, then gives one tiny sheepish smile while the camera holds the mixed-media result to the end.

overall_soundscape: Quiet tea-room ambience with distant wind outside the window, one soft drop into liquid, a ceramic sip, two escalating paper-like shivers, light cup chatter, a short airy frost exhale, and a delicate metal crystallization sound.

non_diegetic_music: Minimal soft marimba notes with wide spacing, stopping during the frost exhale and ending on one light bell tone.
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
case_id: "reddit-1vgynd7-chibi-pinch"
model: "Seedance 2.0"
duration_seconds: 15
language: "zh"
validation: "passed"
---

# 二维角色｜真人接触三级反应 — Seedance 2.0

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
任务：文本生成新视频。
总时长约15秒，仅控制整体信息密度，不分配逐镜头秒数。
主体定义：二维北极狐：原创成年纸贴吉祥物，扁平白色纸边、深蓝围巾、动作始终是平面形变，始终称为二维北极狐；真实手：成年人的真实右手，只从画面右侧进入并沿原路径离开。
镜头1：连续固定中景，不切镜；真实木质茶饮台靠近冬日窗户，唯一二维动画元素是一只原创成年纸贴北极狐，围深蓝围巾，双爪抱着小型真实陶瓷杯；真实右手从右侧缓慢伸入，拿透明滴管悬在杯口上方；北极狐位于画面中右，金属茶匙与茶碟位于左侧前景，滴管路径和角色脸不重叠；柔和冬日侧光，写实背景保持中性暖木色，二维角色仅有克制青蓝点色；<窗外很远的风声><安静茶室底噪>。
镜头2：保持固定中景；真实手只挤出一滴淡蓝薄荷液，液滴穿过真实空气落入茶中，形成一个小圆形涟漪；二维北极狐等涟漪停下后举杯小口喝下，真实手沿原路径退出；液滴、杯口和角色视线形成清楚因果线，杯子始终不穿过纸贴双爪；液滴只带很淡的冷蓝，不改变全场曝光；<单滴入水声><轻微陶瓷饮用声>。
镜头3：保持固定中景；第一段反应：北极狐放下杯子，眼睛睁大、耳朵抬起、肩膀小幅抖一次，只有鼻尖出现淡青色；第二段反应：身体以平面方式左右抖两次，拉紧围巾并轻轻打颤，杯沿薄霜向把手缓慢生长；角色始终站在同一点，纸边和接触阴影稳定，茶匙尚未结霜；冷蓝逐步增加但不污染写实背景肤色和木色；<一次轻抖纸声><两次更明显的纸片抖动><杯子轻碰桌面声>。
镜头4：保持固定中景，结尾停留；北极狐吸一口气，向左侧真实金属茶匙呼出一小团半透明冷雾；薄霜从匙面依次扩展到匙柄后停止，北极狐先尴尬僵住，再露出很小的不好意思笑容，保持到结束；冷雾只连接角色嘴部和左侧茶匙，不遮挡角色眼睛，不蔓延到其他物体；霜晶反射淡青光，其他颜色和曝光保持稳定；<短促冷雾呼气声><细小金属结晶声><最后一声轻铃>。
整体风格与画质：真人写实与单一原创二维纸贴角色混合，固定机位，冬日柔光，平面形变和接触阴影稳定，青蓝冷感点色；真实液滴路径清楚，纸贴角色厚度和轮廓稳定，反应分三段可读，霜冻从角色效果准确回到真实茶匙。
约束：不得模仿任何现有角色或来源女孩造型，角色必须是原创成年纸贴北极狐；不得出现厨房、炒锅、熟食、辣椒、红色调料、喂食、螺旋眼、横向泪流、发热红光、喷火、文字、Logo、字幕或水印；全程固定机位，除真实手、液滴、杯子和茶匙结霜外其他写实物体保持稳定；只允许一滴薄荷液和一个二维动画角色。
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
  "case_id": "reddit-1vgynd7-chibi-pinch",
  "platform": "reddit",
  "author": "Devajyoti1231",
  "source_title": "2D chibi girl added ‘Just a Pinch’ — MiniMax H3",
  "source_post_id": "1vgynd7",
  "canonical_url": "https://www.reddit.com/r/StableDiffusion/comments/1vgynd7/2d_chibi_girl_added_just_a_pinch_minimax_h3/",
  "published_at": null,
  "model_attribution": {
    "model": "MiniMax H3",
    "status": "creator_claimed",
    "basis": "Model is named in the post title."
  },
  "video_reference": {
    "platform": "reddit",
    "author": "Devajyoti1231",
    "post_url": "https://www.reddit.com/r/StableDiffusion/comments/1vgynd7/2d_chibi_girl_added_just_a_pinch_minimax_h3/",
    "playback_mode": "source_post",
    "preview_gif": "./preview.gif",
    "preview_mp4": "media/reddit-1vgynd7-chibi-pinch/preview.mp4",
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

