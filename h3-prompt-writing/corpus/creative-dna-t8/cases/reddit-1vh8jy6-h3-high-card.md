# reddit-1vh8jy6-h3-high-card

- 类型：案例原文（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SUMMARY.md

````text
# 一对多反转｜单一证据胜出

多个喧闹方案看似占优，单一克制信号通过校准和物理证明完成反转。

## 核心机制

A noisy system makes quantity look powerful, one restrained corrective signal interrupts it, and a physical consequence proves that calibrated clarity beats accumulation.

## 推荐输入格式

`喧闹多数 + 克制单一信号 + 校准动作 + 可见物理证明`

## 简短示例

> 五台机器人各自给出冲突读数，一枚克制的音叉信号完成校准；所有机械臂同步归零，并共同生成一个稳定透明球作为物理证明。

## 必须保留的结构锚点

- 多数方案先制造噪声或冲突
- 单一信号保持克制
- 有明确校准动作
- 最终用物理结果而非口号证明胜出

## 使用方法

1. 先保留用户主体和目标，再按推荐格式补齐场景、事件链、镜头和结果。
2. 阅读 [Creative DNA](./creative-dna.json)，重新实例化变量，不做来源表面换名词。
3. 分别查看 [MiniMax H3](./prompts/minimax-h3.md) 与 [Seedance 2.0](./prompts/seedance-2.0.md) 的已验证实例。
4. GitHub 使用 GIF 快速预览；Electron 媒体包播放完整有声 MP4。

## 来源与署名

- 平台：reddit
- 作者：AxonkaiLab
- 原始视频：[打开来源](https://www.reddit.com/r/comfyui/comments/1vh8jy6/minimax_h3_15s_t2v_in_23_minutes_using_the/)
- 模型归因：MiniMax H3（creator_claimed）

来源视频用于机制研究与引用；公开模板只保留可迁移因果，不要求复刻来源人物、道具、场景、构图、对白或标志性效果。
````

### creative-dna.json

````text
{
  "complexity": "moderate",
  "mechanism": "A noisy system makes quantity look powerful, one restrained corrective signal interrupts it, and a physical consequence proves that calibrated clarity beats accumulation.",
  "invariants": [
    {
      "id": "inv-01",
      "rule": "Show the asymmetric one-versus-many matchup before either side explains it.",
      "purpose": "Creates an immediate comparison question.",
      "ablation_failure": "If the single answer appears first, there is no reversal.",
      "evidence_ids": [
        "beat-01"
      ]
    },
    {
      "id": "inv-02",
      "rule": "Let the many-item side perform longer and occupy more space before the concise answer.",
      "purpose": "Builds apparent advantage and visual noise.",
      "ablation_failure": "Equal screen time makes the payoff predictable and weak.",
      "evidence_ids": [
        "beat-02",
        "obs-03"
      ]
    },
    {
      "id": "inv-03",
      "rule": "Give the single corrective signal a dedicated sensory close-up.",
      "purpose": "Turns a small action or object into the strongest information beat without requiring copied text or props.",
      "ablation_failure": "A wide or simultaneous reveal loses hierarchy and emphasis.",
      "evidence_ids": [
        "beat-03",
        "obs-04"
      ]
    },
    {
      "id": "inv-04",
      "rule": "End with calm control versus noisy consequence, not another explanation.",
      "purpose": "Converts the logical reversal into a visual punchline.",
      "ablation_failure": "A verbal summary repeats information and drains comic energy.",
      "evidence_ids": [
        "beat-04",
        "obs-09"
      ]
    }
  ],
  "slots": [
    {
      "name": "arena",
      "constraint": "A stable comparison space unrelated to gambling or the source saloon."
    },
    {
      "name": "many_side",
      "constraint": "One expressive character with three to five compact labeled options."
    },
    {
      "name": "one_side",
      "constraint": "One calm character with a single short answer label."
    },
    {
      "name": "many_signals",
      "constraint": "Three to five distinct controls, sounds, lights, routes, or gestures that create legible visual noise."
    },
    {
      "name": "single_answer",
      "constraint": "One visually and sonically distinct corrective action or object that carries the reversal without needing text."
    },
    {
      "name": "proof",
      "constraint": "A visible consequence showing why the concise answer wins."
    },
    {
      "name": "meltdown",
      "constraint": "Safe exaggerated reaction with no weapons or copied gesture."
    },
    {
      "name": "sound",
      "constraint": "Escalating object sounds, one reveal accent, and a short consequence sound."
    }
  ],
  "anti_copy_exclusions": [
    "legacy cartoon characters, voices, silhouettes, or franchise animation surface",
    "saloon, gambling table, gold-and-carrot stakes, or Western props",
    "source model names and exact card text",
    "pistols, smoke-cloud surrender, exact poses, and shot compositions"
  ],
  "instantiations": [
    {
      "concept": "In a whimsical calibration lab, a frantic octopus pulls five mismatched levers while a maintenance robot taps one brass tuning fork; the resonance aligns the machines and produces one perfect glass sphere.",
      "prompt_seed": "Five noisy controls lose to one calibrated resonance signal, proved by a synchronized mechanical correction."
    },
    {
      "concept": "In a nocturnal vineyard, five autonomous pruning drones chase competing light paths until one gardener strikes a pitch pipe; the swarm settles into a single measured spiral and trims one clean row.",
      "prompt_seed": "Five conflicting routes yield to one audible calibration cue, proved by coherent motion rather than a written answer."
    },
    {
      "concept": "In a kinetic paper city, five traffic towers flash different patterns until one tiny clockmaker inserts a metronome key; every paper vehicle snaps into one flowing rhythm.",
      "prompt_seed": "Five competing signals versus one timing key, proved by a city-scale choreography reset."
    }
  ],
  "failure_modes": [
    {
      "failure": "The answer appears too early.",
      "repair": "Hold it until after the many side has completed the spatial display and presentation pose."
    },
    {
      "failure": "The many-side noise becomes random rather than countable.",
      "repair": "Limit it to three to five distinct controls or signals and stage them in a clear activation sequence."
    },
    {
      "failure": "The ending copies the source meltdown.",
      "repair": "Replace weapons and smoke with a consequence native to the new arena, such as collapsing mockups, foaming food, or desynchronized lights."
    }
  ],
  "transfer_tests": [
    {
      "concept": "In a whimsical calibration lab, a frantic octopus pulls five mismatched levers while a maintenance robot taps one brass tuning fork; the resonance aligns the machines and produces one perfect glass sphere.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04"
      ],
      "changed_slots": [
        "arena",
        "many_side",
        "one_side",
        "many_signals",
        "single_answer",
        "proof",
        "meltdown"
      ]
    },
    {
      "concept": "In a nocturnal vineyard, five autonomous pruning drones chase competing light paths until one gardener strikes a pitch pipe; the swarm settles into a single measured spiral and trims one clean row.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04"
      ],
      "changed_slots": [
        "arena",
        "many_side",
        "one_side",
        "many_signals",
        "single_answer",
        "proof",
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
  "resource_id": "reddit-1vh8jy6-h3-high-card",
  "locale": "zh-CN",
  "source_bindings": {
    "manifest_sha256": "9fca06bc359cc9766d843d1516ebe3b4578eae8f7d3aafe991e87a4c4a338b4c",
    "creative_dna_sha256": "2b87a30e15bd1ad221a1cbf782fa9f7532d7a712657453b946afc37b7dbcd921"
  },
  "content": {
    "title": "一对多反转｜单一证据胜出",
    "summary": "多个喧闹方案看似占优，单一克制信号通过校准和物理证明完成反转。",
    "quick_start": {
      "input_format": "喧闹多数 + 克制单一信号 + 校准动作 + 可见物理证明",
      "recommended_input": "五台机器人各自给出冲突读数，一枚克制的音叉信号完成校准；所有机械臂同步归零，并共同生成一个稳定透明球作为物理证明。",
      "required_anchors": [
        "多数方案先制造噪声或冲突",
        "单一信号保持克制",
        "有明确校准动作",
        "最终用物理结果而非口号证明胜出"
      ],
      "usage_steps": [
        "把示例主体、场景和表层元素替换为原创概念。",
        "让每个必需锚点和 Creative DNA 不可变条件都能在画面因果链中被看见。",
        "选择 MiniMax H3 或 Seedance 2.0 模板，只填写已声明的可替换项。",
        "生成前检查时长、事件顺序、镜头连续性、声音和反复制约束。"
      ],
      "applicable_scope": [
        "多个喧闹方案看似占优，单一克制信号通过校准和物理证明完成反转。",
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
      "mechanism": "一个噪杂系统先以数量制造强势感；一次克制而明确的纠正信号将其打断，最终用可见的物理结果证明：校准后的清晰度胜过单纯堆叠。",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "在任何一方解释之前先展示不对称的一对多对决。",
          "purpose": "创建一个直接的比较问题。",
          "ablation_failure": "如果首先出现单一答案，则不会出现逆转。",
          "evidence_ids": [
            "beat-01"
          ]
        },
        {
          "id": "inv-02",
          "rule": "在简洁答案出现前，让项目繁多的一侧表演更久、占据更大的画面空间。",
          "purpose": "建立明显的优势和视觉噪音。",
          "ablation_failure": "相同的画面时长使得收束效果可预测且微弱。",
          "evidence_ids": [
            "beat-02",
            "obs-03"
          ]
        },
        {
          "id": "inv-03",
          "rule": "为单个纠正信号提供专门的感官特写。",
          "purpose": "让一个小动作或小物件成为最关键的信息节拍，同时无需复制来源文字或道具。",
          "ablation_failure": "远景揭示或一次性同时揭示，会削弱层级与重点。",
          "evidence_ids": [
            "beat-03",
            "obs-04"
          ]
        },
        {
          "id": "inv-04",
          "rule": "以冷静的控制和喧闹的结果结束，而不是另一种解释。",
          "purpose": "将逻辑反转转化为视觉笑点。",
          "ablation_failure": "口头总结会重复信息并耗尽喜剧能量。",
          "evidence_ids": [
            "beat-04",
            "obs-09"
          ]
        }
      ],
      "slots": [
        {
          "name": "arena",
          "constraint": "与赌博或源酒馆无关的稳定比较空间。"
        },
        {
          "name": "many_side",
          "constraint": "一个富有表现力的角色，带有三到五个紧凑的标签选项。"
        },
        {
          "name": "one_side",
          "constraint": "一个冷静的角色，只有一个简短的答案标签。"
        },
        {
          "name": "many_signals",
          "constraint": "三到五个不同的控件、声音、灯光、路线或手势会产生清晰的视觉噪音。"
        },
        {
          "name": "single_answer",
          "constraint": "一种视觉上和声音上不同的纠正动作或物体，无需文字即可实现逆转。"
        },
        {
          "name": "proof",
          "constraint": "一个明显的结果显示了为什么简洁的答案获胜。"
        },
        {
          "name": "meltdown",
          "constraint": "安全的夸张反应，没有武器或模仿的手势。"
        },
        {
          "name": "sound",
          "constraint": "逐步增强的物体声、一次揭示重音，以及一段简短的结果音效。"
        }
      ],
      "anti_copy_exclusions": [
        "传统卡通人物、声音、剪影或既有系列作品的动画画风",
        "酒馆、赌桌、金胡萝卜赌注或西部道具",
        "来源作品中的模型名称和原样卡面文字",
        "手枪、烟云投降，以及与来源完全相同的姿势和镜头构图"
      ],
      "instantiations": [
        {
          "concept": "在一个异想天开的校准实验室中，一只疯狂的章鱼拉动五个不匹配的杠杆，而维护机器人则敲击一个黄铜音叉；共振使机器对齐并产生一个完美的玻璃球。",
          "prompt_seed": "同步机械校正证明了五个噪声控制会输给一个校准的共振信号。"
        },
        {
          "concept": "在夜间葡萄园中，五架自主修剪无人机追逐相互竞争的光路，直到一名园丁吹响定音管；无人机群随即收束成单一螺旋，并整齐修剪完一整排葡萄藤。",
          "prompt_seed": "五条冲突路线最终让位于一个可听见的校准信号；结果由协同动作证明，而不是书面答案。"
        },
        {
          "concept": "在一座充满活力的纸城市中，五座交通塔闪烁着不同的图案，直到一个小钟表匠插入节拍器钥匙；每一辆纸质车辆都融入了一种流动的节奏。",
          "prompt_seed": "城市规模的编排重置证明了五个竞争信号与一个计时键的对比。"
        }
      ],
      "failure_modes": [
        {
          "failure": "答案出现得太早了。",
          "repair": "把答案保留到项目繁多的一侧完成空间展示与呈现姿态之后。"
        },
        {
          "failure": "项目繁多一侧的噪杂变得随机，无法再逐项辨认。",
          "repair": "将其限制为三到五个不同的控制或信号，并以清晰的激活顺序排列它们。"
        },
        {
          "failure": "结尾照搬了来源作品中的混乱崩解场面。",
          "repair": "用新场景固有的结果替换武器和烟雾，例如模型倒塌、食物起泡或灯光不同步。"
        }
      ],
      "transfer_tests": [
        {
          "concept": "在一个异想天开的校准实验室中，一只疯狂的章鱼拉动五个不匹配的杠杆，而维护机器人则敲击一个黄铜音叉；共振使机器对齐并产生一个完美的玻璃球。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04"
          ],
          "changed_slots": [
            "arena",
            "many_side",
            "one_side",
            "many_signals",
            "single_answer",
            "proof",
            "meltdown"
          ]
        },
        {
          "concept": "在夜间葡萄园中，五架自主修剪无人机追逐相互竞争的光路，直到一名园丁吹响定音管；无人机群随即收束成单一螺旋，并整齐修剪完一整排葡萄藤。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04"
          ],
          "changed_slots": [
            "arena",
            "many_side",
            "one_side",
            "many_signals",
            "single_answer",
            "proof",
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
  "resource_id": "reddit-1vh8jy6-h3-high-card",
  "locale": "en",
  "source_bindings": {
    "manifest_sha256": "9fca06bc359cc9766d843d1516ebe3b4578eae8f7d3aafe991e87a4c4a338b4c",
    "creative_dna_sha256": "2b87a30e15bd1ad221a1cbf782fa9f7532d7a712657453b946afc37b7dbcd921"
  },
  "content": {
    "title": "One-to-Many Reversal | Evidence Resolution",
    "summary": "Multiple noisy proposals appear to be dominant, but a single restrained signal completes the reversal through calibration and physical proof.",
    "quick_start": {
      "input_format": "Noisy Majority + Restrained Single Signal + Calibrated Action + Visible Physical Proof",
      "recommended_input": "Each of the five robots provided conflicting readings, and a restrained tuning fork signal completed the calibration; all robotic arms synchronized to zero simultaneously, and collectively generated a stable transparent ball as physical proof.",
      "required_anchors": [
        "Most solutions begin by creating noise or conflict",
        "A single signal remains restrained",
        "There is a clear calibration action",
        "Ultimately, physical results prove victory rather than slogans."
      ],
      "usage_steps": [
        "Replace the example subject, setting and surface details with an original concept.",
        "Keep every required anchor and Creative DNA invariant causally visible.",
        "Choose the MiniMax H3 or Seedance 2.0 prompt and fill only the declared variable slots.",
        "Check duration, event order, camera continuity, sound and anti-copy constraints before generation."
      ],
      "applicable_scope": [
        "Multiple noisy options appear to dominate until a single restrained signal completes the reversal through calibration and physical proof.",
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
      "mechanism": "A noisy system makes quantity look powerful, one restrained corrective signal interrupts it, and a physical consequence proves that calibrated clarity beats accumulation.",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "Show the asymmetric one-versus-many matchup before either side explains it.",
          "purpose": "Creates an immediate comparison question.",
          "ablation_failure": "If the single answer appears first, there is no reversal.",
          "evidence_ids": [
            "beat-01"
          ]
        },
        {
          "id": "inv-02",
          "rule": "Let the many-item side perform longer and occupy more space before the concise answer.",
          "purpose": "Builds apparent advantage and visual noise.",
          "ablation_failure": "Equal screen time makes the payoff predictable and weak.",
          "evidence_ids": [
            "beat-02",
            "obs-03"
          ]
        },
        {
          "id": "inv-03",
          "rule": "Give the single corrective signal a dedicated sensory close-up.",
          "purpose": "Turns a small action or object into the strongest information beat without requiring copied text or props.",
          "ablation_failure": "A wide or simultaneous reveal loses hierarchy and emphasis.",
          "evidence_ids": [
            "beat-03",
            "obs-04"
          ]
        },
        {
          "id": "inv-04",
          "rule": "End with calm control versus noisy consequence, not another explanation.",
          "purpose": "Converts the logical reversal into a visual punchline.",
          "ablation_failure": "A verbal summary repeats information and drains comic energy.",
          "evidence_ids": [
            "beat-04",
            "obs-09"
          ]
        }
      ],
      "slots": [
        {
          "name": "arena",
          "constraint": "A stable comparison space unrelated to gambling or the source saloon."
        },
        {
          "name": "many_side",
          "constraint": "One expressive character with three to five compact labeled options."
        },
        {
          "name": "one_side",
          "constraint": "One calm character with a single short answer label."
        },
        {
          "name": "many_signals",
          "constraint": "Three to five distinct controls, sounds, lights, routes, or gestures that create legible visual noise."
        },
        {
          "name": "single_answer",
          "constraint": "One visually and sonically distinct corrective action or object that carries the reversal without needing text."
        },
        {
          "name": "proof",
          "constraint": "A visible consequence showing why the concise answer wins."
        },
        {
          "name": "meltdown",
          "constraint": "Safe exaggerated reaction with no weapons or copied gesture."
        },
        {
          "name": "sound",
          "constraint": "Escalating object sounds, one reveal accent, and a short consequence sound."
        }
      ],
      "anti_copy_exclusions": [
        "legacy cartoon characters, voices, silhouettes, or franchise animation surface",
        "saloon, gambling table, gold-and-carrot stakes, or Western props",
        "source model names and exact card text",
        "pistols, smoke-cloud surrender, exact poses, and shot compositions"
      ],
      "instantiations": [
        {
          "concept": "In a whimsical calibration lab, a frantic octopus pulls five mismatched levers while a maintenance robot taps one brass tuning fork; the resonance aligns the machines and produces one perfect glass sphere.",
          "prompt_seed": "Five noisy controls lose to one calibrated resonance signal, proved by a synchronized mechanical correction."
        },
        {
          "concept": "In a nocturnal vineyard, five autonomous pruning drones chase competing light paths until one gardener strikes a pitch pipe; the swarm settles into a single measured spiral and trims one clean row.",
          "prompt_seed": "Five conflicting routes yield to one audible calibration cue, proved by coherent motion rather than a written answer."
        },
        {
          "concept": "In a kinetic paper city, five traffic towers flash different patterns until one tiny clockmaker inserts a metronome key; every paper vehicle snaps into one flowing rhythm.",
          "prompt_seed": "Five competing signals versus one timing key, proved by a city-scale choreography reset."
        }
      ],
      "failure_modes": [
        {
          "failure": "The answer appears too early.",
          "repair": "Hold it until after the many side has completed the spatial display and presentation pose."
        },
        {
          "failure": "The many-side noise becomes random rather than countable.",
          "repair": "Limit it to three to five distinct controls or signals and stage them in a clear activation sequence."
        },
        {
          "failure": "The ending copies the source meltdown.",
          "repair": "Replace weapons and smoke with a consequence native to the new arena, such as collapsing mockups, foaming food, or desynchronized lights."
        }
      ],
      "transfer_tests": [
        {
          "concept": "In a whimsical calibration lab, a frantic octopus pulls five mismatched levers while a maintenance robot taps one brass tuning fork; the resonance aligns the machines and produces one perfect glass sphere.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04"
          ],
          "changed_slots": [
            "arena",
            "many_side",
            "one_side",
            "many_signals",
            "single_answer",
            "proof",
            "meltdown"
          ]
        },
        {
          "concept": "In a nocturnal vineyard, five autonomous pruning drones chase competing light paths until one gardener strikes a pitch pipe; the swarm settles into a single measured spiral and trims one clean row.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04"
          ],
          "changed_slots": [
            "arena",
            "many_side",
            "one_side",
            "many_signals",
            "single_answer",
            "proof",
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
  "case_id": "reddit-1vh8jy6-h3-high-card",
  "slug": "stage-one-signal-reversal",
  "title": "一对多反转｜单一证据胜出",
  "source_title": "The H3 High Card — one 15-second local T2V",
  "summary": "多个喧闹方案看似占优，单一克制信号通过校准和物理证明完成反转。",
  "status": "released",
  "source_duration_seconds": 15.125,
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
  "skill_ref": "../../../skills/stage-one-signal-reversal",
  "preview_refs": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/reddit-1vh8jy6-h3-high-card/preview.mp4"
  },
  "preview_paths": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/reddit-1vh8jy6-h3-high-card/preview.mp4"
  },
  "preview_status": {
    "gif": "available",
    "poster": "available",
    "mp4": "available_in_electron_media_pack"
  },
  "template_id": "t8c006-clarity-over-quantity-reversal",
  "template_action": "selector",
  "duplicate_of": null,
  "input_format": "喧闹多数 + 克制单一信号 + 校准动作 + 可见物理证明",
  "recommended_input": "五台机器人各自给出冲突读数，一枚克制的音叉信号完成校准；所有机械臂同步归零，并共同生成一个稳定透明球作为物理证明。",
  "required_anchors": [
    "多数方案先制造噪声或冲突",
    "单一信号保持克制",
    "有明确校准动作",
    "最终用物理结果而非口号证明胜出"
  ],
  "tags": [
    "t8c006",
    "clarity",
    "over",
    "quantity",
    "reversal"
  ],
  "quality": {
    "weighted_score": 4.748,
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
case_id: "reddit-1vh8jy6-h3-high-card"
model: "MiniMax H3"
duration_seconds: 15
language: "en"
validation: "passed"
---

# 一对多反转｜单一证据胜出 — MiniMax H3

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
integrated_multimodal_description: [Shot 1] Original stylized stop-motion animation with tactile brass, frosted glass, painted wood, soft felt characters, visible handcrafted imperfections, amber work lights, cyan instrument glow, precise object continuity, and no resemblance to any existing cartoon franchise. A descending crane shot enters a tall circular calibration lab where five glass machines ring a brass turntable. A small felt octopus operator skitters around the outer rail and grabs five mismatched colored levers at once; a compact cream maintenance robot waits motionless on the central platform beside one brass tuning fork. The frame is radial rather than confrontational, with no table game, cards, labels, or direct address. [Shot 2] At 00:02.200, The camera begins a clockwise orbit around the machinery as the octopus yanks the five levers in a countable sequence. Each lever activates a different failure: one piston chatters, one belt runs backward, one bell rings too fast, one blue lamp strobes, and one glass tube fills with harmless silver bubbles. The five rhythms overlap while the robot remains still at the center. [Shot 3] At 00:07.400, Match-cut to an extreme macro close-up of the robot's two padded fingers lifting the single brass tuning fork. It taps the fork once against a wooden block. The fork vibrates visibly in shallow focus and releases one clean circular cyan resonance ripple; every competing machine sound drops out for a half-beat. [Shot 4] At 00:10.200, The camera rides the cyan resonance ripple outward in a fast low tracking move. As it reaches each machine, the backward belt reverses, the piston adopts the same tempo, the bell slows, the strobe becomes a steady glow, and the bubbles arrange into one rising helix. The corrections propagate clockwise with clear cause before effect; the octopus releases the levers and watches the sequence travel. [Shot 5] At 00:12.700, Cut to a low three-quarter view of the central output nozzle. The synchronized machines exhale one perfectly round translucent glass sphere that rolls into a felt cradle without bouncing. In the deep background all five mechanisms pulse together; the octopus slowly lowers five limp arms while the robot catches the fading tuning-fork vibration with one fingertip. Hold on the single flawless result.

overall_soundscape: Warm workshop room tone; five deliberately different mechanical rhythms accumulate in order, then drop to near-silence for one pure tuning-fork tone. A cyan resonance whoosh travels clockwise, the five mechanisms lock into a shared pulse, and the finished glass sphere lands with one delicate crystalline tick.

non_diegetic_music: No melody; use only a very soft low marimba pulse after synchronization, subordinate to the mechanical rhythm and ending before the final glass tick.
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
case_id: "reddit-1vh8jy6-h3-high-card"
model: "Seedance 2.0"
duration_seconds: 15
language: "zh"
validation: "passed"
---

# 一对多反转｜单一证据胜出 — Seedance 2.0

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
任务：文本生成新视频。
总时长约15秒，仅控制整体信息密度，不分配逐镜头秒数。
主体定义：章鱼操作员：原创小型毛毡章鱼，砖红色身体、八条短臂，动作急促，始终称为章鱼操作员；维护机器人：原创奶油白小型机器人，圆角外壳、青色单眼灯，动作克制，始终称为维护机器人。
镜头1：下降式摇臂广角，落到圆形实验室的轻俯视构图；五台玻璃机械环绕黄铜转台；章鱼操作员沿外圈快速移动，同时抓住五根颜色不同的控制杆，维护机器人在中央平台的黄铜音叉旁保持静止；采用环形放射构图，不形成左右对峙；五台机器间距清楚，中央平台完整可见；琥珀工作灯照亮黄铜和涂漆木材，青色仪表光穿过磨砂玻璃，保持手工定格质感；<温暖工坊底噪><五根控制杆依次咔嗒>。
镜头2：顺时针环绕五台机械，运动平稳且依次经过每个故障点；章鱼操作员按顺序拉下五根控制杆：活塞急促抖动、传送带反向、铃铛过快、蓝灯频闪、玻璃管涌出安全银色气泡；五种节奏逐层叠加，维护机器人仍在圆心不动；每种故障只属于一台机器，环绕方向与激活顺序一致，不互相穿模；五个故障点用局部青蓝亮点区分，整体琥珀曝光不变；<活塞抖动><反向皮带><快铃><继电器频闪><气泡声>依次叠加。
镜头3：匹配切到极近微距，浅景深锁住维护机器人的两根软垫手指和黄铜音叉；维护机器人把唯一一只黄铜音叉轻敲木块；音叉持续可见振动，释放一圈纯净青色共振波，其他机械声短暂停止半拍；音叉位于画面中心，共振波完整离开画框，不出现任何文字或卡片；黄铜高光温暖，共振波为单一纯净青色，背景柔化；<单次木块轻敲><纯净音叉长音><半拍近静音>。
镜头4：贴地低位跟随青色共振波，沿圆环顺时针快速滑行；共振波依次触达五台机械：反向皮带恢复、活塞进入同一节拍、铃声减速、频闪变恒亮、气泡排列成上升螺旋；每项校正都严格先接触后改变，章鱼操作员松开控制杆；波纹路线与前一镜环绕方向一致，五次校正互不遮挡，中央平台始终作为方向锚点；青色波纹移动时短暂照亮黄铜边缘，机器恢复后仪表光统一；<顺时针移动的共振呼啸><五种机械声逐个锁入同一节拍>。
镜头5：切到中央输出口的低位三分之四近景，镜头稳定；同步后的五台机器共同吐出一颗透明、浑圆、无接缝的玻璃球，玻璃球滚入毛毡托槽后停止；背景五台机器同频脉动，章鱼操作员缓慢垂下五条手臂，维护机器人用一根手指接住音叉余振；玻璃球沿唯一轨道进入托槽，不弹跳；人物留在后景，不遮挡成品；玻璃球折射琥珀与青色双光，成品成为唯一高亮焦点；<同步机械低脉冲><玻璃球滚动><落槽时一声清脆晶体轻响>。
整体风格与画质：原创手工定格动画，黄铜、磨砂玻璃、涂漆木材和毛毡角色触感清楚，琥珀工作灯与青色仪表光形成稳定对比；五台机器身份与环形位置稳定，故障和校正顺序可数，共振波严格触发因果，音叉不变形，最终玻璃球完整清透。
约束：不得模仿任何现有卡通人物、系列造型、声音或动画签名；不得出现场酒馆、赌博、卡片、金钱、胡萝卜、枪械、烟雾、模型品牌名、Logo、字幕、水印或任何可见文字；五台机器必须空间独立，校正严格按顺时针顺序传播；不得增加对白、爆炸、倒塌笑点或无信息价值的切镜。
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
  "case_id": "reddit-1vh8jy6-h3-high-card",
  "platform": "reddit",
  "author": "AxonkaiLab",
  "source_title": "The H3 High Card — one 15-second local T2V",
  "source_post_id": "1vh8jy6",
  "canonical_url": "https://www.reddit.com/r/comfyui/comments/1vh8jy6/minimax_h3_15s_t2v_in_23_minutes_using_the/",
  "published_at": null,
  "model_attribution": {
    "model": "MiniMax H3",
    "status": "creator_claimed",
    "basis": "Creator describes the built-in H3 workflow, native audio, and single generation."
  },
  "video_reference": {
    "platform": "reddit",
    "author": "AxonkaiLab",
    "post_url": "https://www.reddit.com/r/comfyui/comments/1vh8jy6/minimax_h3_15s_t2v_in_23_minutes_using_the/",
    "playback_mode": "source_post",
    "preview_gif": "./preview.gif",
    "preview_mp4": "media/reddit-1vh8jy6-h3-high-card/preview.mp4",
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

