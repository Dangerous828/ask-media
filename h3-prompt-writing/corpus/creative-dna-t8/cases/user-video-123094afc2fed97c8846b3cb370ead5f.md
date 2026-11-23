# user-video-123094afc2fed97c8846b3cb370ead5f

- 类型：案例原文（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SUMMARY.md

````text
# 数据折叠｜总量下钻到当前值

## 用途

用一个超大总量建立尺度，展开明细记录证明总量，再折回聚合结果并切换到当前状态值，最后只用一次克制标注锁定结论。

## 推荐输入格式

`超大总量 + 至少2条分类明细 + 聚合结果 + 相关里程碑 + 当前状态值 + 单次克制标注`

## 可直接改写的简短示例

> 一张纸艺能源账单先显示全年总量，翻开展示三条月度记录，再折叠为季度均值；侧页露出节能里程碑，最后展开当前月数值并只盖一个确认章。

## 必须保留的结构锚点

- Open with one dominant total and a compact label before showing its evidence.
- Unfold the claim into at least two itemized records with visible category separation.
- Compress the detailed records into one aggregate result before changing metric family.
- End on the current-state value and add only one restrained annotation after the value is readable.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。

## 来源

- 作者：未知作者
- 原帖：https://local.t8/user-supplied/123094afc2fed97c8846b3cb370ead5f
````

### creative-dna.json

````text
{
  "complexity": "moderate",
  "mechanism": "Open with one oversized total that calibrates scale, unfold into itemized records that prove the claim, refold those records into an aggregate result, pivot through one intermediate milestone to a current-state value, then use one restrained manual annotation to lock the conclusion.",
  "invariants": [
    {
      "id": "inv-01",
      "rule": "Open with one dominant total and a compact label before showing its evidence.",
      "purpose": "Creates immediate scale and a clear question about how the total was earned.",
      "ablation_failure": "Starting with many small records removes the hook and hierarchy.",
      "evidence_ids": [
        "beat-01",
        "obs-01",
        "obs-02"
      ]
    },
    {
      "id": "inv-02",
      "rule": "Unfold the claim into at least two itemized records with visible category separation.",
      "purpose": "Turns a large headline into checkable evidence.",
      "ablation_failure": "A second big number without records feels like another unsupported claim.",
      "evidence_ids": [
        "beat-02",
        "obs-03",
        "obs-04"
      ]
    },
    {
      "id": "inv-03",
      "rule": "Compress the detailed records into one aggregate result before changing metric family.",
      "purpose": "Rewards the detail pass with a simplified summary state.",
      "ablation_failure": "Jumping directly from records to the final value leaves the proof unresolved.",
      "evidence_ids": [
        "beat-03",
        "obs-05",
        "obs-06"
      ]
    },
    {
      "id": "inv-04",
      "rule": "Use one physically legible panel or carrier change to reveal an intermediate milestone from a different but related metric family.",
      "purpose": "Makes the information pivot feel causal rather than arbitrary.",
      "ablation_failure": "A plain cut between unrelated metrics obscures their relationship.",
      "evidence_ids": [
        "beat-04",
        "obs-07",
        "obs-08"
      ]
    },
    {
      "id": "inv-05",
      "rule": "End on the current-state value and add only one restrained annotation after the value is readable.",
      "purpose": "Separates the conclusion from the evidence and gives it a memorable hold.",
      "ablation_failure": "Many marks compete with the value; annotating before readability hides the conclusion.",
      "evidence_ids": [
        "beat-05",
        "obs-09",
        "obs-10"
      ]
    }
  ],
  "slots": [
    {
      "name": "headline_total",
      "constraint": "One original, truthful or explicitly fictional dominant total with a short label."
    },
    {
      "name": "record_set",
      "constraint": "At least two distinct records whose categories visibly support the headline."
    },
    {
      "name": "aggregate_result",
      "constraint": "One summary value derived from the record set."
    },
    {
      "name": "milestone_metric",
      "constraint": "One related intermediate milestone shown through a physical carrier change."
    },
    {
      "name": "current_state",
      "constraint": "One final current value, not a duplicate of the opening total."
    },
    {
      "name": "material_system",
      "constraint": "An original medium whose folds, slides, hinges or layer changes explain information transitions."
    },
    {
      "name": "annotation",
      "constraint": "One brief non-brand manual mark added only after the final value is readable."
    },
    {
      "name": "sound_family",
      "constraint": "Original tactile cues tied to each information-state change."
    }
  ],
  "anti_copy_exclusions": [
    "50+",
    "期数教程",
    "1.5W",
    "17.7",
    "3.8W",
    "4.3W",
    "source café photographs and crossed red strips",
    "source black-white-red paper system and final red brush oval"
  ],
  "instantiations": [
    {
      "concept": "A navy-and-cream river-restoration board opens on '24 RESTORED SEGMENTS', unfolds into two transparent field-record cards, compresses to '127K L SAVED', pivots through a baseline efficiency panel and ends on 'CURRENT 92%' with one copper grease-pencil check.",
      "prompt_seed": "Tactile river-restoration data story: oversized total, two field-record proofs, one aggregate saving, one hinged milestone and a current-state value with a single manual check."
    },
    {
      "concept": "A translucent museum-conservation light table starts with '80 OBJECTS STABILIZED', fans out humidity and UV exposure records on acetate, stacks them into one reduced-risk index, flips a frosted milestone pane and ends on the current safe-storage rate sealed with one wax thumbprint.",
      "prompt_seed": "Museum conservation evidence hierarchy on acetate and frosted glass, progressing from total to records to aggregate to milestone to current state, ending with one wax mark."
    }
  ],
  "failure_modes": [
    {
      "failure": "The opening contains several equal-sized figures.",
      "repair": "Choose one dominant total and one compact label."
    },
    {
      "failure": "The detail state is decorative rather than evidentiary.",
      "repair": "Give each record a distinct category and a visible relation to the headline."
    },
    {
      "failure": "The sequence skips the aggregate summary.",
      "repair": "Compress records into one result before switching metric family."
    },
    {
      "failure": "The milestone arrives through an arbitrary cut.",
      "repair": "Use one hinge, fold, slide or layer change to carry the pivot."
    },
    {
      "failure": "The final annotation obscures or repeats the value.",
      "repair": "Wait until the current value is readable, then add one restrained mark."
    }
  ],
  "transfer_tests": [
    {
      "concept": "A navy-and-cream river-restoration board opens on '24 RESTORED SEGMENTS', unfolds into two transparent field-record cards, compresses to '127K L SAVED', pivots through a baseline efficiency panel and ends on 'CURRENT 92%' with one copper grease-pencil check.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04",
        "inv-05"
      ],
      "changed_slots": [
        "headline_total",
        "record_set",
        "aggregate_result",
        "milestone_metric",
        "current_state",
        "material_system",
        "annotation",
        "sound_family"
      ]
    },
    {
      "concept": "A translucent museum-conservation light table starts with '80 OBJECTS STABILIZED', fans out humidity and UV exposure records on acetate, stacks them into one reduced-risk index, flips a frosted milestone pane and ends on the current safe-storage rate sealed with one wax thumbprint.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04",
        "inv-05"
      ],
      "changed_slots": [
        "headline_total",
        "record_set",
        "aggregate_result",
        "milestone_metric",
        "current_state",
        "material_system",
        "annotation",
        "sound_family"
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
  "resource_id": "user-video-123094afc2fed97c8846b3cb370ead5f",
  "locale": "zh-CN",
  "source_bindings": {
    "manifest_sha256": "18c88c0e9591baea02b1b3bee7e0b217701fb290cebe7af08bb9d22b7c78b67e",
    "creative_dna_sha256": "c2976ceae2e8a2e91dc33ce98aef37d75df55115c9e6ec47b5a9e4c4f5937417"
  },
  "content": {
    "title": "数据折叠｜总量下钻到当前值",
    "summary": "用一个超大总量建立尺度，展开明细记录证明总量，再折回聚合结果并切换到当前状态值，最后只用一次克制标注锁定结论。",
    "quick_start": {
      "input_format": "超大总量 + 至少2条分类明细 + 聚合结果 + 相关里程碑 + 当前状态值 + 单次克制标注",
      "recommended_input": "一张纸艺能源账单先显示全年总量，翻开展示三条月度记录，再折叠为季度均值；侧页露出节能里程碑，最后展开当前月数值并只盖一个确认章。",
      "required_anchors": [
        "展示证据前，先用一个占据视觉主导的总量与一个紧凑标签开场。",
        "把总量主张展开为至少两条逐项记录，并让类别区分清楚可见。",
        "切换指标系列前，先把明细记录折回为一个聚合结果。",
        "以当前状态值收尾；只有在数值清楚可读后，才加入一次克制标注。"
      ],
      "usage_steps": [
        "把示例主体、场景和表层元素替换为原创概念。",
        "让每个必需锚点和 Creative DNA 不可变条件都能在画面因果链中被看见。",
        "选择 MiniMax H3 或 Seedance 2.0 模板，只填写已声明的可替换项。",
        "生成前检查时长、事件顺序、镜头连续性、声音和反复制约束。"
      ],
      "applicable_scope": [
        "用一个超大总量建立尺度，展开明细记录证明总量，再折回聚合结果并切换到当前状态值，最后只用一次克制标注锁定结论。",
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
      "mechanism": "以一个超大总量开场，先校准信息量级；把它展开成能验证主张的逐项记录，再将记录折回为聚合结果；通过一个相关的中间里程碑转向当前状态值，最后只用一次克制的手动标注锁定结论。",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "展示证据前，先用一个占据视觉主导的总量与一个紧凑标签开场。",
          "purpose": "立即建立量级，并提出总量如何形成的清楚问题。",
          "ablation_failure": "从许多小记录开场，会失去吸引点与信息层级。",
          "evidence_ids": [
            "beat-01",
            "obs-01",
            "obs-02"
          ]
        },
        {
          "id": "inv-02",
          "rule": "把总量主张展开为至少两条逐项记录，并让类别区分清楚可见。",
          "purpose": "将大标题变成可检查的证据。",
          "ablation_failure": "没有明细记录支撑的第二个大数字，只会像另一项缺乏证据的主张。",
          "evidence_ids": [
            "beat-02",
            "obs-03",
            "obs-04"
          ]
        },
        {
          "id": "inv-03",
          "rule": "切换指标系列前，先把明细记录折回为一个聚合结果。",
          "purpose": "用简洁的汇总状态回报前面的细节铺陈。",
          "ablation_failure": "从明细直接跳到最终值，会让证据链悬而未决。",
          "evidence_ids": [
            "beat-03",
            "obs-05",
            "obs-06"
          ]
        },
        {
          "id": "inv-04",
          "rule": "用一次物理上清楚可读的面板或信息载体变化，揭示来自另一组相关指标的中间里程碑。",
          "purpose": "让信息转折显得有因果依据，而不是任意跳转。",
          "ablation_failure": "在无关指标间直接剪切，会掩盖它们之间的关系。",
          "evidence_ids": [
            "beat-04",
            "obs-07",
            "obs-08"
          ]
        },
        {
          "id": "inv-05",
          "rule": "以当前状态值收尾；只有在数值清楚可读后，才加入一次克制标注。",
          "purpose": "把结论与证据分开，并给最终数值留出清楚停留。",
          "ablation_failure": "多个标记会与数值争夺注意力；在数值读清前标注，会遮蔽结论。",
          "evidence_ids": [
            "beat-05",
            "obs-09",
            "obs-10"
          ]
        }
      ],
      "slots": [
        {
          "name": "headline_total",
          "constraint": "一个原创、真实可信或明确标为虚构的主导总量，并配一个短标签。"
        },
        {
          "name": "record_set",
          "constraint": "至少两条不同的记录，其类别明显支持标题。"
        },
        {
          "name": "aggregate_result",
          "constraint": "从记录集导出的一个汇总值。"
        },
        {
          "name": "milestone_metric",
          "constraint": "一个相关的中间里程碑，通过信息载体的实体变化显示。"
        },
        {
          "name": "current_state",
          "constraint": "一个最终当前值，而不是期初总计的重复值。"
        },
        {
          "name": "material_system",
          "constraint": "一种原创媒介，其折叠、滑动、铰链或分层变化能解释信息状态的转换。"
        },
        {
          "name": "annotation",
          "constraint": "仅在最终值可读后才添加一个简短的非品牌手动标记。"
        },
        {
          "name": "sound_family",
          "constraint": "与每次信息状态变化相绑定的一套原创触觉与画内提示。"
        }
      ],
      "anti_copy_exclusions": [
        "50+",
        "期数教程",
        "1.5W",
        "17.7",
        "3.8W",
        "4.3W",
        "来源咖啡馆照片和交叉的红条",
        "来源黑白红纸系统和最终的红色画笔椭圆形"
      ],
      "instantiations": [
        {
          "concept": "海军蓝和奶油色的河流恢复板在“24 RESTORED SEGMENTS”上打开，展开为两张透明的现场记录卡，压缩为“127K L SAVED”，通过基线效率面板旋转，并在“CURRENT 92％”上用一根铜色油蜡笔检查结束。",
          "prompt_seed": "触觉河流恢复数据故事：超大总数、两份现场记录证明、一份汇总节省、一个铰链里程碑和一次手动检查的当前状态值。"
        },
        {
          "concept": "一张半透明的博物馆保护灯桌以“80 OBJECTS STABILIZED”开头，在醋酸纤维上展开湿度和 UV 暴露记录，将它们堆叠成一个降低风险的索引，翻转磨砂的里程碑窗格，最后以用一个蜡指纹密封的当前安全存储率结束。",
          "prompt_seed": "博物馆关于醋酸纤维和磨砂玻璃的保护证据层次结构，从总数到记录到汇总到里程碑再到当前状态，最后以一个蜡标记结束。"
        }
      ],
      "failure_modes": [
        {
          "failure": "开场同时出现多个同等大小的数值。",
          "repair": "选择一个占主导地位的总数和一个紧凑的标签。"
        },
        {
          "failure": "细节状态是装饰性的而不是证据性的。",
          "repair": "为每条记录指定一个独特的类别以及与标题的可见关系。"
        },
        {
          "failure": "该序列会跳过聚合摘要。",
          "repair": "在切换指标系列之前将记录压缩为一个结果。"
        },
        {
          "failure": "中间里程碑通过一次任意剪辑突然出现。",
          "repair": "使用一个铰链、折叠、滑动或换层来承载枢轴。"
        },
        {
          "failure": "最终注释模糊或重复了该值。",
          "repair": "等当前值清楚可读后，再加入一个克制标记。"
        }
      ],
      "transfer_tests": [
        {
          "concept": "海军蓝和奶油色的河流恢复板在“24 RESTORED SEGMENTS”上打开，展开为两张透明的现场记录卡，压缩为“127K L SAVED”，通过基线效率面板旋转，并在“CURRENT 92％”上用一根铜色油蜡笔检查结束。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05"
          ],
          "changed_slots": [
            "headline_total",
            "record_set",
            "aggregate_result",
            "milestone_metric",
            "current_state",
            "material_system",
            "annotation",
            "sound_family"
          ]
        },
        {
          "concept": "一张半透明的博物馆保护灯桌以“80 OBJECTS STABILIZED”开头，在醋酸纤维上展开湿度和 UV 暴露记录，将它们堆叠成一个降低风险的索引，翻转磨砂的里程碑窗格，最后以用一个蜡指纹密封的当前安全存储率结束。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05"
          ],
          "changed_slots": [
            "headline_total",
            "record_set",
            "aggregate_result",
            "milestone_metric",
            "current_state",
            "material_system",
            "annotation",
            "sound_family"
          ]
        }
      ]
    }
  },
  "review": {
    "status": "approved",
    "method": "source-bound Chinese editorial pass with film-language glossary, stable-token, structure, and anti-copy validation"
  }
}
````

### locales/en.json

````text
{
  "schema_version": "public-display-locale/v1",
  "resource_kind": "case",
  "resource_id": "user-video-123094afc2fed97c8846b3cb370ead5f",
  "locale": "en",
  "source_bindings": {
    "manifest_sha256": "18c88c0e9591baea02b1b3bee7e0b217701fb290cebe7af08bb9d22b7c78b67e",
    "creative_dna_sha256": "c2976ceae2e8a2e91dc33ce98aef37d75df55115c9e6ec47b5a9e4c4f5937417"
  },
  "content": {
    "title": "Metric Fold-Down | Total, Detail, Aggregate, Current State",
    "summary": "Open with one oversized total, unfold categorized records that prove it, fold them back into an aggregate, then switch to the current-state value and use one restrained mark to lock the conclusion.",
    "quick_start": {
      "input_format": "Very large total amount + at least 2 classification details + aggregation results + related milestones + current status value + single restraint mark",
      "recommended_input": "A paper energy bill first shows the annual total, opens to display three monthly records, and then collapses to the quarterly average; the side page reveals energy-saving milestones, and finally expands the current monthly value and only stamps a confirmation stamp.",
      "required_anchors": [
        "Open with one dominant total and a compact label before showing its evidence.",
        "Unfold the claim into at least two itemized records with visible category separation.",
        "Compress the detailed records into one aggregate result before changing metric family.",
        "End on the current-state value and add only one restrained annotation after the value is readable."
      ],
      "usage_steps": [
        "Replace the example subject, setting, and surface details with an original concept.",
        "Keep every required anchor and Creative DNA invariant causally visible.",
        "Choose the MiniMax H3 or Seedance 2.0 prompt and fill only the declared variable slots.",
        "Check duration, event order, camera continuity, sound, and anti-copy constraints before generation."
      ],
      "applicable_scope": [
        "Open with one oversized total, unfold categorized records that prove it, fold them back into an aggregate, then switch to the current-state value and use one restrained mark to lock the conclusion.",
        "Original 4–15 second concepts that can preserve every required anchor.",
        "MiniMax H3 or Seedance 2.0 projects that need a reusable causal video structure."
      ],
      "not_suitable_for": [
        "Requests that copy the source identity, setting, props, dialogue, or shot order.",
        "Concepts that cannot show all required anchors inside the target duration.",
        "Long-form exposition or unrelated multi-location stories without a compact causal chain."
      ]
    },
    "creative_dna": {
      "complexity": "moderate",
      "mechanism": "Open with one oversized total that calibrates scale, unfold into itemized records that prove the claim, refold those records into an aggregate result, pivot through one intermediate milestone to a current-state value, then use one restrained manual annotation to lock the conclusion.",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "Open with one dominant total and a compact label before showing its evidence.",
          "purpose": "Creates immediate scale and a clear question about how the total was earned.",
          "ablation_failure": "Starting with many small records removes the hook and hierarchy.",
          "evidence_ids": [
            "beat-01",
            "obs-01",
            "obs-02"
          ]
        },
        {
          "id": "inv-02",
          "rule": "Unfold the claim into at least two itemized records with visible category separation.",
          "purpose": "Turns a large headline into checkable evidence.",
          "ablation_failure": "A second big number without records feels like another unsupported claim.",
          "evidence_ids": [
            "beat-02",
            "obs-03",
            "obs-04"
          ]
        },
        {
          "id": "inv-03",
          "rule": "Compress the detailed records into one aggregate result before changing metric family.",
          "purpose": "Rewards the detail pass with a simplified summary state.",
          "ablation_failure": "Jumping directly from records to the final value leaves the proof unresolved.",
          "evidence_ids": [
            "beat-03",
            "obs-05",
            "obs-06"
          ]
        },
        {
          "id": "inv-04",
          "rule": "Use one physically legible panel or carrier change to reveal an intermediate milestone from a different but related metric family.",
          "purpose": "Makes the information pivot feel causal rather than arbitrary.",
          "ablation_failure": "A plain cut between unrelated metrics obscures their relationship.",
          "evidence_ids": [
            "beat-04",
            "obs-07",
            "obs-08"
          ]
        },
        {
          "id": "inv-05",
          "rule": "End on the current-state value and add only one restrained annotation after the value is readable.",
          "purpose": "Separates the conclusion from the evidence and gives it a memorable hold.",
          "ablation_failure": "Many marks compete with the value; annotating before readability hides the conclusion.",
          "evidence_ids": [
            "beat-05",
            "obs-09",
            "obs-10"
          ]
        }
      ],
      "slots": [
        {
          "name": "headline_total",
          "constraint": "One original, truthful or explicitly fictional dominant total with a short label."
        },
        {
          "name": "record_set",
          "constraint": "At least two distinct records whose categories visibly support the headline."
        },
        {
          "name": "aggregate_result",
          "constraint": "One summary value derived from the record set."
        },
        {
          "name": "milestone_metric",
          "constraint": "One related intermediate milestone shown through a physical carrier change."
        },
        {
          "name": "current_state",
          "constraint": "One final current value, not a duplicate of the opening total."
        },
        {
          "name": "material_system",
          "constraint": "An original medium whose folds, slides, hinges or layer changes explain information transitions."
        },
        {
          "name": "annotation",
          "constraint": "One brief non-brand manual mark added only after the final value is readable."
        },
        {
          "name": "sound_family",
          "constraint": "Original tactile cues tied to each information-state change."
        }
      ],
      "anti_copy_exclusions": [
        "50+",
        "期数教程",
        "1.5W",
        "17.7",
        "3.8W",
        "4.3W",
        "source café photographs and crossed red strips",
        "source black-white-red paper system and final red brush oval"
      ],
      "instantiations": [
        {
          "concept": "A navy-and-cream river-restoration board opens on '24 RESTORED SEGMENTS', unfolds into two transparent field-record cards, compresses to '127K L SAVED', pivots through a baseline efficiency panel and ends on 'CURRENT 92%' with one copper grease-pencil check.",
          "prompt_seed": "Tactile river-restoration data story: oversized total, two field-record proofs, one aggregate saving, one hinged milestone and a current-state value with a single manual check."
        },
        {
          "concept": "A translucent museum-conservation light table starts with '80 OBJECTS STABILIZED', fans out humidity and UV exposure records on acetate, stacks them into one reduced-risk index, flips a frosted milestone pane and ends on the current safe-storage rate sealed with one wax thumbprint.",
          "prompt_seed": "Museum conservation evidence hierarchy on acetate and frosted glass, progressing from total to records to aggregate to milestone to current state, ending with one wax mark."
        }
      ],
      "failure_modes": [
        {
          "failure": "The opening contains several equal-sized figures.",
          "repair": "Choose one dominant total and one compact label."
        },
        {
          "failure": "The detail state is decorative rather than evidentiary.",
          "repair": "Give each record a distinct category and a visible relation to the headline."
        },
        {
          "failure": "The sequence skips the aggregate summary.",
          "repair": "Compress records into one result before switching metric family."
        },
        {
          "failure": "The milestone arrives through an arbitrary cut.",
          "repair": "Use one hinge, fold, slide or layer change to carry the pivot."
        },
        {
          "failure": "The final annotation obscures or repeats the value.",
          "repair": "Wait until the current value is readable, then add one restrained mark."
        }
      ],
      "transfer_tests": [
        {
          "concept": "A navy-and-cream river-restoration board opens on '24 RESTORED SEGMENTS', unfolds into two transparent field-record cards, compresses to '127K L SAVED', pivots through a baseline efficiency panel and ends on 'CURRENT 92%' with one copper grease-pencil check.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05"
          ],
          "changed_slots": [
            "headline_total",
            "record_set",
            "aggregate_result",
            "milestone_metric",
            "current_state",
            "material_system",
            "annotation",
            "sound_family"
          ]
        },
        {
          "concept": "A translucent museum-conservation light table starts with '80 OBJECTS STABILIZED', fans out humidity and UV exposure records on acetate, stacks them into one reduced-risk index, flips a frosted milestone pane and ends on the current safe-storage rate sealed with one wax thumbprint.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05"
          ],
          "changed_slots": [
            "headline_total",
            "record_set",
            "aggregate_result",
            "milestone_metric",
            "current_state",
            "material_system",
            "annotation",
            "sound_family"
          ]
        }
      ]
    }
  },
  "review": {
    "status": "approved",
    "method": "canonical-source English editorial pass with terminology, identity, and stable-token validation"
  }
}
````

### manifest.json

````text
{
  "schema_version": "public-case/v1",
  "case_id": "user-video-123094afc2fed97c8846b3cb370ead5f",
  "slug": "fold-metrics-to-current-state",
  "title": "数据折叠｜总量下钻到当前值",
  "source_title": "数据折叠｜从总量标题下钻到当前值",
  "summary": "用一个超大总量建立尺度，展开明细记录证明总量，再折回聚合结果并切换到当前状态值，最后只用一次克制标注锁定结论。",
  "status": "released",
  "source_duration_seconds": 10.125,
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
  "skill_ref": "../../../skills/fold-metrics-to-current-state",
  "preview_refs": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/user-video-123094afc2fed97c8846b3cb370ead5f/preview.mp4"
  },
  "preview_paths": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/user-video-123094afc2fed97c8846b3cb370ead5f/preview.mp4"
  },
  "preview_status": {
    "gif": "available",
    "poster": "available",
    "mp4": "available_in_electron_media_pack"
  },
  "template_id": "t8-case-fold-metrics-to-current-state-v1",
  "template_action": "selector",
  "duplicate_of": null,
  "input_format": "超大总量 + 至少2条分类明细 + 聚合结果 + 相关里程碑 + 当前状态值 + 单次克制标注",
  "recommended_input": "一张纸艺能源账单先显示全年总量，翻开展示三条月度记录，再折叠为季度均值；侧页露出节能里程碑，最后展开当前月数值并只盖一个确认章。",
  "required_anchors": [
    "Open with one dominant total and a compact label before showing its evidence.",
    "Unfold the claim into at least two itemized records with visible category separation.",
    "Compress the detailed records into one aggregate result before changing metric family.",
    "End on the current-state value and add only one restrained annotation after the value is readable."
  ],
  "tags": [
    "fold",
    "metrics",
    "to",
    "current",
    "state"
  ],
  "quality": {
    "weighted_score": 4.73,
    "scale": 5,
    "anti_copy_passed": true,
    "prompt_validation": {
      "minimax_h3": true,
      "seedance_2_0": true
    },
    "release_passed": true
  },
  "created_at": "2026-08-12T13:02:46+08:00",
  "updated_at": "2026-08-12T13:59:31+08:00"
}
````

### prompts/minimax-h3.md

````text
---
schema_version: "public-prompt/v1"
case_id: "user-video-123094afc2fed97c8846b3cb370ead5f"
model: "MiniMax H3"
duration_seconds: 15
language: "en"
validation: "passed"
---

# 数据折叠｜总量下钻到当前值 — MiniMax H3

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
integrated_multimodal_description: [Shot 1] Original tactile editorial data film, navy fiberboard, cream paper, clear acrylic records, copper accents, physically folded information hierarchy. On a navy fiberboard wall, thick cream letters read "24 RESTORED SEGMENTS" beside a small copper river icon. Use a shallow lateral move so the letter depth and cast shadows establish one dominant total before any supporting record appears. [Shot 2] At 00:02.800, The headline board opens into two clear acrylic field-record panels over an original river map. The first reads "NORTH LOOP / 86% FLOW" and the second reads "SOUTH GATE / 41% LOSS CUT"; place one photograph-free sensor diagram on each and keep both records separately readable. [Shot 3] At 00:05.800, The two acrylic records slide and stack into one compact copper-edged card reading "127K L SAVED" with two small unlabeled bar marks underneath. Settle to a frontal view so the aggregate result is simpler than the detailed panels. [Shot 4] At 00:08.800, The aggregate card hinges outward and exposes a frosted cream milestone panel reading "BASELINE 61%". A physical gauge needle sweeps once toward a hidden right-hand panel, clearly pivoting from saved volume to system efficiency. [Shot 5] At 00:11.700, The right-hand panel slides fully open to reveal thick navy type reading "CURRENT 92%". Hold the value frontally; only after it is clear, one copper grease-pencil check is drawn beneath it. Use only the declared river-restoration copy, material system and one final manual mark.

overall_soundscape: Use soft fiberboard room tone, thick paper hinge creaks, acrylic slide taps, two record-placement clicks, one compact stack lock, a gauge sweep, the final panel glide and one dry grease-pencil check; no dialogue.

non_diegetic_music: Original 96 BPM muted vibraphone, brushed snare and low plucked cello. Start with one broad pulse, add two short notes for the field records, condense to a single chord at the aggregate, pivot with a rising cello harmonic and finish on a clean restrained cadence after the manual check.
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
case_id: "user-video-123094afc2fed97c8846b3cb370ead5f"
model: "Seedance 2.0"
duration_seconds: 15
language: "zh"
validation: "passed"
---

# 数据折叠｜总量下钻到当前值 — Seedance 2.0

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
任务：文本生成一支原创15秒河流修复数据短片：先给一个大号总量，再展开两条分项证据，压缩成聚合结果，通过实体铰链切换到阶段里程碑，最后用一次手绘勾标记当前值。
总时长约15秒，仅控制整体信息密度，不分配逐镜头秒数。
镜头1：浅幅侧向滑动；海军蓝纤维板上，厚实奶油色立体字显示【24 RESTORED SEGMENTS】，旁边只有一个小型铜色河流图标；单一大号总量占主导，暂不出现支持记录；柔和侧光，海军蓝、奶油色、铜色三色体系；<板材空间底噪><一次低沉提示音>。
镜头2：斜俯三分之二视角；总量板打开成两块透明亚克力记录板，分别显示【NORTH LOOP / 86% FLOW】与【SOUTH GATE / 41% LOSS CUT】，每块只配一个原创传感器示意图；两条分项记录各自可读并共同支持总量；铜色边框强调证据层；<两次透明板展开><两次记录定位声>。
镜头3：稳定正面中近景；两块透明记录板滑动叠合，锁成一张紧凑铜边卡，显示【127K L SAVED】，下方仅保留两条无文字短柱；详细记录压缩为一个聚合结果；铜边高光稳定，背景保持海军蓝；<亚克力滑动><单次锁定>。
镜头4：固定斜侧视角；聚合卡通过可见铰链翻开，露出磨砂奶油色面板【BASELINE 61%】，机械指针只扫动一次并指向右侧隐藏面板；实体铰链承担从节水量到效率指标的切换；磨砂面板柔亮，铜色指针清楚；<铰链转动><指针扫过>。
镜头5：稳定正面特写；右侧面板完全滑开，厚实海军蓝立体字显示【CURRENT 92%】；数值清楚后，铜色油性笔只在下方画一个勾；当前值独立停留，手绘标记不遮挡文字；当前值获得最清楚的阴影层次；<面板滑开><干燥油笔一划>。
整体风格与画质：原创触感编辑数据电影，海军蓝纤维板、奶油色厚纸、透明亚克力记录、铜色机械细节；保证五级信息层次清楚、文字可读、材料连续；每镜只采用一个主要运镜。
约束：只使用当前声明的原创河流修复数据和材质系统；保持总量→分项→聚合→里程碑→当前值顺序；手绘勾只能在最终数值清楚后出现一次；只实现当前声明的新实例，不引入未声明文案、图像、配色、结构或标注形状。
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
  "case_id": "user-video-123094afc2fed97c8846b3cb370ead5f",
  "platform": "user-supplied",
  "author": "unknown",
  "source_title": "数据折叠｜总量下钻到当前值",
  "source_post_id": null,
  "canonical_url": "https://local.t8/user-supplied/123094afc2fed97c8846b3cb370ead5f",
  "published_at": null,
  "model_attribution": {
    "model": "unknown",
    "status": "unknown",
    "basis": null
  },
  "video_reference": {
    "platform": "user-supplied",
    "author": "unknown",
    "post_url": "https://local.t8/user-supplied/123094afc2fed97c8846b3cb370ead5f",
    "playback_mode": "source_post",
    "preview_gif": "./preview.gif",
    "preview_mp4": "media/user-video-123094afc2fed97c8846b3cb370ead5f/preview.mp4",
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

