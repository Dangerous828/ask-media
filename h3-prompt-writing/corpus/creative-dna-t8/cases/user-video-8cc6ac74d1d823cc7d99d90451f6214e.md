# user-video-8cc6ac74d1d823cc7d99d90451f6214e

- 类型：案例原文（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SUMMARY.md

````text
# 双人递进｜共享接触从地面升到空中峰值

## 用途

先建立两个主体的深度差，再让同一次共享接触从低位逐级升高到唯一空中峰值，最后回到地面并停留在可读的关系终态。

## 推荐输入格式

`两个身份稳定的主体 + 初始距离差 + 低位共同接触 + 至少1次中段升高 + 共享空中峰值 + 落地关系停留`

## 可直接改写的简短示例

> 两台木偶修理机从不同深度靠近，在低位共同托起一枚发光环，经过腰部与头顶两次交接后一起跃到最高点，落回地面并并肩稳住发光环。

## 必须保留的结构锚点

- Establish two stable roles and a readable depth or distance gap before contact.
- Use one committed approach to create the first low shared contact state.
- Reserve one shared airborne or otherwise clearly highest joint event as the apex.
- Return both roles to a grounded or baseline plane and hold their post-apex relationship without asserting an unsupported result.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变表面名词、风格、光影、声效与物理实现，不做来源视频换名词复刻。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。

## 来源

- 作者：未知作者
- 原帖：https://local.t8/user-supplied/8cc6ac74d1d823cc7d99d90451f6214e
````

### creative-dna.json

````text
{
  "complexity": "moderate",
  "mechanism": "Establish two visually distinct roles at different depths, let the nearer role trigger a continuous exchange whose shared contact height rises in readable stages from ground to one joint aerial apex, then return both roles to a grounded held relationship without inventing a winner.",
  "invariants": [
    {
      "id": "inv-01",
      "rule": "Establish two stable roles and a readable depth or distance gap before contact.",
      "purpose": "Makes the initiating commitment and later convergence legible.",
      "ablation_failure": "Starting in a tangled exchange removes the baseline and makes escalation hard to read.",
      "evidence_ids": [
        "beat-01",
        "obs-01",
        "obs-02"
      ]
    },
    {
      "id": "inv-02",
      "rule": "Use one committed approach to create the first low shared contact state.",
      "purpose": "Provides a measurable contact baseline rather than random action.",
      "ablation_failure": "If the first event has no shared contact, later height changes have no reference point.",
      "evidence_ids": [
        "beat-02",
        "obs-03",
        "obs-04"
      ]
    },
    {
      "id": "inv-03",
      "rule": "Raise contact amplitude or altitude through at least one intermediate exchange while role identity stays stable.",
      "purpose": "Turns repetition into a visible escalation ladder.",
      "ablation_failure": "Contacts at one unchanged height feel repetitive rather than progressive.",
      "evidence_ids": [
        "beat-03",
        "obs-05",
        "obs-06",
        "obs-12"
      ]
    },
    {
      "id": "inv-04",
      "rule": "Reserve one shared airborne or otherwise clearly highest joint event as the apex.",
      "purpose": "Gives the ladder a single unmistakable peak.",
      "ablation_failure": "Several equal peaks flatten the hierarchy and dilute the climax.",
      "evidence_ids": [
        "beat-04",
        "obs-07",
        "obs-08"
      ]
    },
    {
      "id": "inv-05",
      "rule": "Return both roles to a grounded or baseline plane and hold their post-apex relationship without asserting an unsupported result.",
      "purpose": "Closes the height arc and preserves source uncertainty.",
      "ablation_failure": "Ending during the apex feels truncated; declaring a winner invents evidence.",
      "evidence_ids": [
        "beat-05",
        "obs-09",
        "obs-10"
      ]
    }
  ],
  "slots": [
    {
      "name": "role_pair",
      "constraint": "Two original stable roles with visibly distinct silhouettes or functions."
    },
    {
      "name": "initial_gap",
      "constraint": "A readable depth, distance or level separation before the first shared action."
    },
    {
      "name": "contact_carrier",
      "constraint": "One original object, signal or task that both roles visibly affect."
    },
    {
      "name": "height_ladder",
      "constraint": "At least low, intermediate and peak shared states with continuous causal handoffs."
    },
    {
      "name": "apex_realization",
      "constraint": "One unmistakably highest joint event, not repeated spectacle."
    },
    {
      "name": "camera_grammar",
      "constraint": "Proof-oriented framing that compares the baseline, intermediate rise, apex and return."
    },
    {
      "name": "end_relationship",
      "constraint": "A held post-apex relationship that does not claim an unsupported winner or diagnosis."
    },
    {
      "name": "sound_family",
      "constraint": "Original story-world cues that distinguish low, rising, apex and settling phases."
    }
  ],
  "anti_copy_exclusions": [
    "two fantasy women in black and white dresses",
    "gold and cyan glowing swords",
    "moonlit cloud temple and pine platform",
    "the exact sword-fight choreography and final low stances"
  ],
  "instantiations": [
    {
      "concept": "Inside an original wind-tunnel laboratory, two clockwork kite technicians at different platform depths alternately catch and redirect one fabric calibration ring at rising heights, stabilize it together at the ceiling apex, then land on opposite marked platforms with the ring suspended between them.",
      "prompt_seed": "Two original clockwork kite technicians use a shared fabric calibration ring to build a low-to-high contact ladder inside a wind tunnel, culminating in one joint ceiling apex and a grounded two-platform hold."
    },
    {
      "concept": "In a flooded botanical dome, two amphibious maintenance drones begin at different water levels and alternately tap one floating sensor buoy up a sequence of spillway ledges; they meet above the top cascade to stabilize it, then settle on separate banks while the buoy remains centered.",
      "prompt_seed": "Two original amphibious maintenance drones raise one sensor buoy through staged water levels, share one aerial stabilization apex and finish on separate banks with no competition result."
    }
  ],
  "failure_modes": [
    {
      "failure": "The two roles start tangled together.",
      "repair": "Show stable identities and a readable gap before the first shared action."
    },
    {
      "failure": "The first contact is already maximal.",
      "repair": "Begin with one low baseline contact so later states can visibly rise."
    },
    {
      "failure": "Repeated events stay at one height.",
      "repair": "Assign each exchange a higher contact level or larger shared amplitude."
    },
    {
      "failure": "Several equal aerial peaks compete for attention.",
      "repair": "Reserve one unmistakably highest joint event."
    },
    {
      "failure": "The ending invents a winner or skips the return.",
      "repair": "Return both roles to the baseline plane and hold a neutral post-apex relationship."
    }
  ],
  "transfer_tests": [
    {
      "concept": "Inside an original wind-tunnel laboratory, two clockwork kite technicians at different platform depths alternately catch and redirect one fabric calibration ring at rising heights, stabilize it together at the ceiling apex, then land on opposite marked platforms with the ring suspended between them.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04",
        "inv-05"
      ],
      "changed_slots": [
        "role_pair",
        "initial_gap",
        "contact_carrier",
        "height_ladder",
        "apex_realization",
        "camera_grammar",
        "end_relationship",
        "sound_family"
      ]
    },
    {
      "concept": "In a flooded botanical dome, two amphibious maintenance drones begin at different water levels and alternately tap one floating sensor buoy up a sequence of spillway ledges; they meet above the top cascade to stabilize it, then settle on separate banks while the buoy remains centered.",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04",
        "inv-05"
      ],
      "changed_slots": [
        "role_pair",
        "initial_gap",
        "contact_carrier",
        "height_ladder",
        "apex_realization",
        "camera_grammar",
        "end_relationship",
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
  "resource_id": "user-video-8cc6ac74d1d823cc7d99d90451f6214e",
  "locale": "zh-CN",
  "source_bindings": {
    "manifest_sha256": "5d3635a4018b65b54321ea19705365329c74b0d23482975144c93bf36f932bc8",
    "creative_dna_sha256": "ef45d1521b5be61228ebfc4c69ce2f24c743390d96f7e7cec4c7b038a755d9df"
  },
  "content": {
    "title": "双人递进｜共享接触从地面升到空中峰值",
    "summary": "先建立两个主体的深度差，再让同一次共享接触从低位逐级升高到唯一空中峰值，最后回到地面并停留在可读的关系终态。",
    "quick_start": {
      "input_format": "两个身份稳定的主体 + 初始距离差 + 低位共同接触 + 至少1次中段升高 + 共享空中峰值 + 落地关系停留",
      "recommended_input": "两台木偶修理机从不同深度靠近，在低位共同托起一枚发光环，经过腰部与头顶两次交接后一起跃到最高点，落回地面并并肩稳住发光环。",
      "required_anchors": [
        "接触发生前，先建立两个身份稳定的角色，以及清楚可读的深度或距离差。",
        "以一次明确投入的接近动作，建立第一个低位共享接触状态。",
        "把一次共同腾空或其他明显最高的联合动作保留为唯一顶点。",
        "让两个角色回到地面或基准平面，并保持峰值后的关系；不得臆断来源未支持的结果。"
      ],
      "usage_steps": [
        "把示例主体、场景和表层元素替换为原创概念。",
        "让每个必需锚点和 Creative DNA 不可变条件都能在画面因果链中被看见。",
        "选择 MiniMax H3 或 Seedance 2.0 模板，只填写已声明的可替换项。",
        "生成前检查时长、事件顺序、镜头连续性、声音和反复制约束。"
      ],
      "applicable_scope": [
        "先建立两个主体的深度差，再让同一次共享接触从低位逐级升高到唯一空中峰值，最后回到地面并停留在可读的关系终态。",
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
      "mechanism": "先在不同纵深建立两个视觉上可区分的角色；由较近的角色发起一次连续交接，让双方共享接触的高度从地面经清楚阶段逐级升到唯一空中顶点；随后让两个角色回到地面并保持可读的关系终态，不臆造胜负。",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "接触发生前，先建立两个身份稳定的角色，以及清楚可读的深度或距离差。",
          "purpose": "让发起动作的明确投入以及后续汇合都清楚可读。",
          "ablation_failure": "从混乱的交流开始会消除基线，并使升级变得难以阅读。",
          "evidence_ids": [
            "beat-01",
            "obs-01",
            "obs-02"
          ]
        },
        {
          "id": "inv-02",
          "rule": "以一次明确投入的接近动作，建立第一个低位共享接触状态。",
          "purpose": "提供可测量的接触基线而不是随机动作。",
          "ablation_failure": "如果第一个事件没有共享接触，则后续的高度变化没有参考点。",
          "evidence_ids": [
            "beat-02",
            "obs-03",
            "obs-04"
          ]
        },
        {
          "id": "inv-03",
          "rule": "在角色身份保持稳定的情况下，通过至少一次中间交换提高接触幅度或高度。",
          "purpose": "将重复变成可见的升级阶梯。",
          "ablation_failure": "在一个不变的高度上的接触感觉是重复的而不是渐进的。",
          "evidence_ids": [
            "beat-03",
            "obs-05",
            "obs-06",
            "obs-12"
          ]
        },
        {
          "id": "inv-04",
          "rule": "把一次共同腾空或其他明显最高的联合动作保留为唯一顶点。",
          "purpose": "给阶梯一个明确无误的峰值。",
          "ablation_failure": "多个同等高度的峰值会压平层级并削弱高潮。",
          "evidence_ids": [
            "beat-04",
            "obs-07",
            "obs-08"
          ]
        },
        {
          "id": "inv-05",
          "rule": "让两个角色回到地面或基准平面，并保持峰值后的关系；不得臆断来源未支持的结果。",
          "purpose": "收束高度弧线，同时保留来源结果的不确定性。",
          "ablation_failure": "顶点的结局感觉被截断了；宣布获胜者发明了证据。",
          "evidence_ids": [
            "beat-05",
            "obs-09",
            "obs-10"
          ]
        }
      ],
      "slots": [
        {
          "name": "role_pair",
          "constraint": "两个原创的稳定角色，具有明显不同的轮廓或功能。"
        },
        {
          "name": "initial_gap",
          "constraint": "第一个共享操作之前的可读深度、距离或水平间隔。"
        },
        {
          "name": "contact_carrier",
          "constraint": "一个由双方角色共同影响的原创物体、信号或任务。"
        },
        {
          "name": "height_ladder",
          "constraint": "至少具有连续因果切换的低、中和峰值共享状态。"
        },
        {
          "name": "apex_realization",
          "constraint": "一次明确无误的最高联合动作，不能用多个重复奇观替代。"
        },
        {
          "name": "camera_grammar",
          "constraint": "以验证为目的的景别设计，清楚比较基线、中段上升、顶点与回落。"
        },
        {
          "name": "end_relationship",
          "constraint": "一个稳定保持的峰值后关系，不臆断没有证据支持的胜者或诊断。"
        },
        {
          "name": "sound_family",
          "constraint": "一套原创画内线索，用声音或动作提示区分低位、上升、顶点与稳定阶段。"
        }
      ],
      "anti_copy_exclusions": [
        "两个穿着黑白连衣裙的幻想女性",
        "金色和青色发光剑",
        "月光云殿松台",
        "精确的剑术编排和最后的低姿态"
      ],
      "instantiations": [
        {
          "concept": "在原创的风洞实验室内，两名发条风筝技术人员在不同的平台深度交替抓住并重定向一个上升高度的织物校准环，将其稳定在天花板顶点，然后降落在相对的标记平台上，环悬挂在它们之间。",
          "prompt_seed": "两名原创发条风筝技术人员使用共享的织物校准环在风洞内构建一个从低到高的接触梯，最终形成一个联合天花板顶点和一个接地的两个平台支撑。"
        },
        {
          "concept": "在一座被水淹没的植物穹顶中，两架两栖维护无人机从不同水位开始，轮流轻推同一个漂浮传感浮标，使其沿溢洪道台阶逐级升高；它们在最高水级上方会合并共同稳定浮标，随后分别落在两侧河岸，浮标保持在中央。",
          "prompt_seed": "两架原创两栖维护无人机在阶段性水位中升起一个传感器浮标，共享一个空中稳定顶点，并在不同的河岸上完成，没有比赛结果。"
        }
      ],
      "failure_modes": [
        {
          "failure": "这两个角色开始纠缠在一起。",
          "repair": "在第一个共享操作之前显示稳定的身份和可读的间隙。"
        },
        {
          "failure": "第一次接触已经是最大的了。",
          "repair": "从一次低基线接触开始，以便后续状态可以明显上升。"
        },
        {
          "failure": "重复的事件停留在一个高度。",
          "repair": "为每个交换分配更高的接触级别或更大的共享幅度。"
        },
        {
          "failure": "几个平等的空中山峰争夺注意力。",
          "repair": "只保留一次明确无误的最高联合动作。"
        },
        {
          "failure": "结局发明了胜利者或跳过返回。",
          "repair": "将两个角色返回到基线平面并保持中立的顶点后关系。"
        }
      ],
      "transfer_tests": [
        {
          "concept": "在原创的风洞实验室内，两名发条风筝技术人员在不同的平台深度交替抓住并重定向一个上升高度的织物校准环，将其稳定在天花板顶点，然后降落在相对的标记平台上，环悬挂在它们之间。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05"
          ],
          "changed_slots": [
            "role_pair",
            "initial_gap",
            "contact_carrier",
            "height_ladder",
            "apex_realization",
            "camera_grammar",
            "end_relationship",
            "sound_family"
          ]
        },
        {
          "concept": "在一座被水淹没的植物穹顶中，两架两栖维护无人机从不同水位开始，轮流轻推同一个漂浮传感浮标，使其沿溢洪道台阶逐级升高；它们在最高水级上方会合并共同稳定浮标，随后分别落在两侧河岸，浮标保持在中央。",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05"
          ],
          "changed_slots": [
            "role_pair",
            "initial_gap",
            "contact_carrier",
            "height_ladder",
            "apex_realization",
            "camera_grammar",
            "end_relationship",
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
  "resource_id": "user-video-8cc6ac74d1d823cc7d99d90451f6214e",
  "locale": "en",
  "source_bindings": {
    "manifest_sha256": "5d3635a4018b65b54321ea19705365329c74b0d23482975144c93bf36f932bc8",
    "creative_dna_sha256": "ef45d1521b5be61228ebfc4c69ce2f24c743390d96f7e7cec4c7b038a755d9df"
  },
  "content": {
    "title": "Shared Contact Escalation | Raise One Joint Action to an Airborne Peak",
    "summary": "Establish two stable subjects at different depths, then carry one shared contact from a low position through readable height stages to a single airborne peak. Return both subjects to the ground and hold a clear relationship state.",
    "quick_start": {
      "input_format": "Two subjects with stable identities + initial distance difference + common low-level contact + at least 1 mid-level rise + shared aerial peak + landing relationship stay",
      "recommended_input": "The two puppet repair machines approached from different depths and jointly held up a luminous ring at a low position. After two handovers at the waist and the top of the head, they jumped to the highest point together, fell back to the ground and stabilized the luminous ring side by side.",
      "required_anchors": [
        "Establish two stable roles and a readable depth or distance gap before contact.",
        "Use one committed approach to create the first low shared contact state.",
        "Reserve one shared airborne or otherwise clearly highest joint event as the apex.",
        "Return both roles to a grounded or baseline plane and hold their post-apex relationship without asserting an unsupported result."
      ],
      "usage_steps": [
        "Replace the example subject, setting, and surface details with an original concept.",
        "Keep every required anchor and Creative DNA invariant causally visible.",
        "Choose the MiniMax H3 or Seedance 2.0 prompt and fill only the declared variable slots.",
        "Check duration, event order, camera continuity, sound, and anti-copy constraints before generation."
      ],
      "applicable_scope": [
        "Establish two stable subjects at different depths, then carry one shared contact from a low position through readable height stages to a single airborne peak. Return both subjects to the ground and hold a clear relationship state.",
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
      "mechanism": "Establish two visually distinct roles at different depths, let the nearer role trigger a continuous exchange whose shared contact height rises in readable stages from ground to one joint aerial apex, then return both roles to a grounded held relationship without inventing a winner.",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "Establish two stable roles and a readable depth or distance gap before contact.",
          "purpose": "Makes the initiating commitment and later convergence legible.",
          "ablation_failure": "Starting in a tangled exchange removes the baseline and makes escalation hard to read.",
          "evidence_ids": [
            "beat-01",
            "obs-01",
            "obs-02"
          ]
        },
        {
          "id": "inv-02",
          "rule": "Use one committed approach to create the first low shared contact state.",
          "purpose": "Provides a measurable contact baseline rather than random action.",
          "ablation_failure": "If the first event has no shared contact, later height changes have no reference point.",
          "evidence_ids": [
            "beat-02",
            "obs-03",
            "obs-04"
          ]
        },
        {
          "id": "inv-03",
          "rule": "Raise contact amplitude or altitude through at least one intermediate exchange while role identity stays stable.",
          "purpose": "Turns repetition into a visible escalation ladder.",
          "ablation_failure": "Contacts at one unchanged height feel repetitive rather than progressive.",
          "evidence_ids": [
            "beat-03",
            "obs-05",
            "obs-06",
            "obs-12"
          ]
        },
        {
          "id": "inv-04",
          "rule": "Reserve one shared airborne or otherwise clearly highest joint event as the apex.",
          "purpose": "Gives the ladder a single unmistakable peak.",
          "ablation_failure": "Several equal peaks flatten the hierarchy and dilute the climax.",
          "evidence_ids": [
            "beat-04",
            "obs-07",
            "obs-08"
          ]
        },
        {
          "id": "inv-05",
          "rule": "Return both roles to a grounded or baseline plane and hold their post-apex relationship without asserting an unsupported result.",
          "purpose": "Closes the height arc and preserves source uncertainty.",
          "ablation_failure": "Ending during the apex feels truncated; declaring a winner invents evidence.",
          "evidence_ids": [
            "beat-05",
            "obs-09",
            "obs-10"
          ]
        }
      ],
      "slots": [
        {
          "name": "role_pair",
          "constraint": "Two original stable roles with visibly distinct silhouettes or functions."
        },
        {
          "name": "initial_gap",
          "constraint": "A readable depth, distance or level separation before the first shared action."
        },
        {
          "name": "contact_carrier",
          "constraint": "One original object, signal or task that both roles visibly affect."
        },
        {
          "name": "height_ladder",
          "constraint": "At least low, intermediate and peak shared states with continuous causal handoffs."
        },
        {
          "name": "apex_realization",
          "constraint": "One unmistakably highest joint event, not repeated spectacle."
        },
        {
          "name": "camera_grammar",
          "constraint": "Proof-oriented framing that compares the baseline, intermediate rise, apex and return."
        },
        {
          "name": "end_relationship",
          "constraint": "A held post-apex relationship that does not claim an unsupported winner or diagnosis."
        },
        {
          "name": "sound_family",
          "constraint": "Original story-world cues that distinguish low, rising, apex and settling phases."
        }
      ],
      "anti_copy_exclusions": [
        "two fantasy women in black and white dresses",
        "gold and cyan glowing swords",
        "moonlit cloud temple and pine platform",
        "the exact sword-fight choreography and final low stances"
      ],
      "instantiations": [
        {
          "concept": "Inside an original wind-tunnel laboratory, two clockwork kite technicians at different platform depths alternately catch and redirect one fabric calibration ring at rising heights, stabilize it together at the ceiling apex, then land on opposite marked platforms with the ring suspended between them.",
          "prompt_seed": "Two original clockwork kite technicians use a shared fabric calibration ring to build a low-to-high contact ladder inside a wind tunnel, culminating in one joint ceiling apex and a grounded two-platform hold."
        },
        {
          "concept": "In a flooded botanical dome, two amphibious maintenance drones begin at different water levels and alternately tap one floating sensor buoy up a sequence of spillway ledges; they meet above the top cascade to stabilize it, then settle on separate banks while the buoy remains centered.",
          "prompt_seed": "Two original amphibious maintenance drones raise one sensor buoy through staged water levels, share one aerial stabilization apex and finish on separate banks with no competition result."
        }
      ],
      "failure_modes": [
        {
          "failure": "The two roles start tangled together.",
          "repair": "Show stable identities and a readable gap before the first shared action."
        },
        {
          "failure": "The first contact is already maximal.",
          "repair": "Begin with one low baseline contact so later states can visibly rise."
        },
        {
          "failure": "Repeated events stay at one height.",
          "repair": "Assign each exchange a higher contact level or larger shared amplitude."
        },
        {
          "failure": "Several equal aerial peaks compete for attention.",
          "repair": "Reserve one unmistakably highest joint event."
        },
        {
          "failure": "The ending invents a winner or skips the return.",
          "repair": "Return both roles to the baseline plane and hold a neutral post-apex relationship."
        }
      ],
      "transfer_tests": [
        {
          "concept": "Inside an original wind-tunnel laboratory, two clockwork kite technicians at different platform depths alternately catch and redirect one fabric calibration ring at rising heights, stabilize it together at the ceiling apex, then land on opposite marked platforms with the ring suspended between them.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05"
          ],
          "changed_slots": [
            "role_pair",
            "initial_gap",
            "contact_carrier",
            "height_ladder",
            "apex_realization",
            "camera_grammar",
            "end_relationship",
            "sound_family"
          ]
        },
        {
          "concept": "In a flooded botanical dome, two amphibious maintenance drones begin at different water levels and alternately tap one floating sensor buoy up a sequence of spillway ledges; they meet above the top cascade to stabilize it, then settle on separate banks while the buoy remains centered.",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05"
          ],
          "changed_slots": [
            "role_pair",
            "initial_gap",
            "contact_carrier",
            "height_ladder",
            "apex_realization",
            "camera_grammar",
            "end_relationship",
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
  "case_id": "user-video-8cc6ac74d1d823cc7d99d90451f6214e",
  "slug": "raise-shared-contact-to-airborne-peak",
  "title": "双人递进｜共享接触从地面升到空中峰值",
  "source_title": "双人接触高度递进｜地面交锋到空中峰值",
  "summary": "先建立两个主体的深度差，再让同一次共享接触从低位逐级升高到唯一空中峰值，最后回到地面并停留在可读的关系终态。",
  "status": "released",
  "source_duration_seconds": 15.104,
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
  "skill_ref": "../../../skills/raise-shared-contact-to-airborne-peak",
  "preview_refs": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/user-video-8cc6ac74d1d823cc7d99d90451f6214e/preview.mp4"
  },
  "preview_paths": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/user-video-8cc6ac74d1d823cc7d99d90451f6214e/preview.mp4"
  },
  "preview_status": {
    "gif": "available",
    "poster": "available",
    "mp4": "available_in_electron_media_pack"
  },
  "template_id": "t8-case-shared-contact-height-escalation-v1",
  "template_action": "selector",
  "duplicate_of": null,
  "input_format": "两个身份稳定的主体 + 初始距离差 + 低位共同接触 + 至少1次中段升高 + 共享空中峰值 + 落地关系停留",
  "recommended_input": "两台木偶修理机从不同深度靠近，在低位共同托起一枚发光环，经过腰部与头顶两次交接后一起跃到最高点，落回地面并并肩稳住发光环。",
  "required_anchors": [
    "Establish two stable roles and a readable depth or distance gap before contact.",
    "Use one committed approach to create the first low shared contact state.",
    "Reserve one shared airborne or otherwise clearly highest joint event as the apex.",
    "Return both roles to a grounded or baseline plane and hold their post-apex relationship without asserting an unsupported result."
  ],
  "tags": [
    "shared",
    "contact",
    "height",
    "escalation"
  ],
  "quality": {
    "weighted_score": 4.707,
    "scale": 5,
    "anti_copy_passed": true,
    "prompt_validation": {
      "minimax_h3": true,
      "seedance_2_0": true
    },
    "release_passed": true
  },
  "created_at": "2026-08-12T13:02:45+08:00",
  "updated_at": "2026-08-12T13:59:31+08:00"
}
````

### prompts/minimax-h3.md

````text
---
schema_version: "public-prompt/v1"
case_id: "user-video-8cc6ac74d1d823cc7d99d90451f6214e"
model: "MiniMax H3"
duration_seconds: 15
language: "en"
validation: "passed"
---

# 双人递进｜共享接触从地面升到空中峰值 — MiniMax H3

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
integrated_multimodal_description: [Shot 1] Original tactile clockwork laboratory film, brushed aluminum wind tunnel, crimson and mint technicians, cream fabric ring, physical cable and airflow response. In a brushed-aluminum wind tunnel, one crimson clockwork kite technician stands on a near low platform and one mint technician waits on a higher rear platform. A cream fabric calibration ring hangs loose between them; keep both identities and platform depths clear. [Shot 2] At 00:03.000, The crimson technician runs two steps and taps the ring across a knee-high airflow gate. The ring catches a visible current, reaches the mint technician at low height and establishes the first shared contact state. [Shot 3] At 00:06.000, Use one continuous lateral tracking move as the technicians alternately redirect the same ring through waist-high and shoulder-high airflow gates. Each catch is higher than the last; cable tension, fabric deformation and platform identity remain consistent. [Shot 4] At 00:09.250, Cut to a low wide view. Both technicians jump from their platforms and grasp opposite ribbon tabs as the ring reaches one clear ceiling apex; hold the full bodies, ring and highest gate together for one beat. [Shot 5] At 00:11.750, Both technicians land on separate marked platforms while the ring settles, suspended and level between them. Return to a stable shared frontal view and hold the neutral completed calibration state; do not introduce any undeclared identity, prop, copy or ending event.

overall_soundscape: Use continuous wind-tunnel airflow, clockwork foot clicks, fabric flutter, four distinct gate taps, elastic ribbon tension, one airy apex pulse and two separate landing clacks; no dialogue.

non_diegetic_music: Original 112 BPM prepared-marimba and muted hand-drum pattern. Begin with separated two-note motifs, raise the register at each gate, open into one sustained bowed-cymbal chord at the apex and settle into a quiet paired cadence.
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
case_id: "user-video-8cc6ac74d1d823cc7d99d90451f6214e"
model: "Seedance 2.0"
duration_seconds: 15
language: "zh"
validation: "passed"
---

# 双人递进｜共享接触从地面升到空中峰值 — Seedance 2.0

这是 Creative DNA 的一个已验证原创实例。使用时应重新实例化主体、场景、道具和风格，同时保留案例的因果结构锚点。

## Prompt

```text
任务：文本生成一支原创15秒实验室短片：两名发条风筝技师用同一布质校准环完成从低到高的接触递进，只设置一次共享空中峰值，最后分别落回平台。
总时长约15秒，仅控制整体信息密度，不分配逐镜头秒数。
镜头1：稳定正面广角；拉丝铝风洞中，绯红技师在前方低台，薄荷绿技师在后方高台，奶油色布环松弛悬在两者之间；两名技师身份与平台纵深清楚分离；冷白实验室光，绯红与薄荷绿作为角色编码；<持续风洞气流><轻微发条待机>。
镜头2：低位侧向跟拍；绯红技师跑两步，把布环轻击穿过膝高气流门，布环变形后抵达另一角色的低位接触区；同一布环首次建立共享接触基线；冷光连续，布环边缘受风发亮；<发条脚步><布料拍击><低位门提示音>。
镜头3：单次连续横移；两名技师交替把同一布环送过腰高、肩高气流门，每次接触都比上一次更高，缆线张力和布料形变连续；平台身份不交换，布环路径逐级上升；门框依次亮起白色刻度光；<两次清楚接触><缆线张紧><布料振动>。
镜头4：低机位共享广角；两名技师同时跃起，抓住布环两侧织带，在唯一的天花高点共同稳定它，完整身体与最高气流门同框；这一事件明显高于全部前序接触；顶光短暂增强，角色颜色仍稳定；<上升风压><单次峰值脉冲>。
镜头5：回到稳定正面全景；两名技师分别落回标记平台，布环水平悬停在中间，保持中性校准完成状态，不宣布胜负；回到原基准平面并保留两角色关系；顶光恢复常态，布环稳定；<两次分离落地><布环渐停>。
整体风格与画质：原创触感发条实验室电影，拉丝铝风洞、布料与缆线的真实受力、清楚的高度递进；保持同一布环、两名技师和平台空间连续；每镜只采用一个主要运镜。
约束：只实现当前声明的原创实例，不引入未声明身份、道具、场景、文案或镜头顺序；接触高度必须低位→中位→唯一峰值清楚递进；峰值后必须回到两个分离平台并保持中性关系；不生成字幕、Logo、水印或未声明人物。
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
  "case_id": "user-video-8cc6ac74d1d823cc7d99d90451f6214e",
  "platform": "user-supplied",
  "author": "unknown",
  "source_title": "双人递进｜共享接触从地面升到空中峰值",
  "source_post_id": null,
  "canonical_url": "https://local.t8/user-supplied/8cc6ac74d1d823cc7d99d90451f6214e",
  "published_at": null,
  "model_attribution": {
    "model": "unknown",
    "status": "unknown",
    "basis": null
  },
  "video_reference": {
    "platform": "user-supplied",
    "author": "unknown",
    "post_url": "https://local.t8/user-supplied/8cc6ac74d1d823cc7d99d90451f6214e",
    "playback_mode": "source_post",
    "preview_gif": "./preview.gif",
    "preview_mp4": "media/user-video-8cc6ac74d1d823cc7d99d90451f6214e/preview.mp4",
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

