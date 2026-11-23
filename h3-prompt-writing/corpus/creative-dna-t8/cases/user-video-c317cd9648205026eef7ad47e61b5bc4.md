# user-video-c317cd9648205026eef7ad47e61b5bc4

- 类型：案例原文（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SUMMARY.md

````text
# 四角框域｜手势扩场、箭头峰值与收束

## 用途

双手先定义四个受控角点，让注册框域从掌间逐级扩展到房间尺度；最大状态才加入方向图形与地面响应，随后由同一双手收束并恢复普通环境。

## 推荐输入格式

`明确成年原创控制者 + 稳定注册环境 + 四个手势角点 + 至少三种框域尺寸 + 晚段有界信息峰值 + 主动收束与基线回归`

## 可直接改写的简短示例

> 成年博物馆修复师在胡桃木地图桌前用四枚黄铜磷光角点拉出框域；只有框内纸张变成象牙色黏土等高线浮雕，框域从地图扩到档案柜，后段路线向量达到峰值，再收回掌心并让真实标本标签翻动一次。

## 必须保留的结构锚点

- 激活前先建立一名明确成年原创控制者、稳定注册环境和未激活的双手。
- 手部几何必须先于活动角点形成，每个角或边始终绑定清楚可见的指尖或手部轨迹。
- 变化严格限制在注册框域内，人物身份、空间锚点和边界两侧位置不得漂移。
- 至少用三种框域尺寸证明同一规则；最大信息密度留到后段，再主动收束并完整回到基线。

## 去重与来源

- 本案是稳定模板 `t8-case-hand-bounded-local-medium-window-v1` 的独立证据变体，复用既有 selector，不新增下拉项。
- 来源：用户自制并授权公开分发的完整 MP4。
- 模型与原版提示词：未知/未提供；库内双模型提示词是独立编译结果。
- 源视频不作为模型参考上传。
````

### creative-dna.json

````text
{
  "complexity": "moderate",
  "mechanism": "A stable photoreal baseline becomes a reversible proof surface: visible hands first assign four coupled corners, a registered bounded field grows through multiple sizes while preserving the controller and environment, the largest late state gains denser directional or material information, and the same hands collapse the field to restore the baseline.",
  "invariants": [
    {
      "id": "inv-01",
      "rule": "Establish one clearly adult original controller, one stable registered environment and visibly inactive hands before the bounded field activates.",
      "evidence_ids": [
        "obs-01",
        "obs-04",
        "beat-01"
      ],
      "ablation_failure": "Without a neutral baseline, the later frame cannot prove that the environment changed under user control."
    },
    {
      "id": "inv-02",
      "rule": "Make hand geometry precede every active corner and keep each corner or edge visibly coupled to fingertips or hand trajectories.",
      "evidence_ids": [
        "obs-04",
        "obs-05",
        "beat-02"
      ],
      "ablation_failure": "If corners appear independently, the central hand-to-field causality becomes decorative rather than operational."
    },
    {
      "id": "inv-03",
      "rule": "Keep the transformed or intensified state bounded by one registered moving field while preserving identity and spatial anchors across its edge.",
      "evidence_ids": [
        "obs-06",
        "obs-09",
        "beat-03",
        "beat-04"
      ],
      "ablation_failure": "If the change leaks beyond the field or registration drifts, the effect stops reading as a controllable local window."
    },
    {
      "id": "inv-04",
      "rule": "Show at least three materially different field sizes or corner configurations that obey the same coupling and containment rule.",
      "evidence_ids": [
        "obs-05",
        "obs-11",
        "beat-02",
        "beat-03",
        "beat-05"
      ],
      "ablation_failure": "One static rectangle is merely an overlay; progressive rule-consistent states prove reusable control."
    },
    {
      "id": "inv-05",
      "rule": "Reserve the largest and most information-dense graphic state for a late apex after the containment rule is already legible.",
      "evidence_ids": [
        "obs-10",
        "obs-14",
        "obs-18",
        "beat-04"
      ],
      "ablation_failure": "If maximum spectacle arrives before the rule, the mechanism becomes noisy and the escalation has nowhere to go."
    },
    {
      "id": "inv-06",
      "rule": "Visibly contract or dismiss the field and end with the same controller and environment restored in the baseline medium.",
      "evidence_ids": [
        "obs-08",
        "obs-09",
        "obs-13",
        "beat-05",
        "beat-06"
      ],
      "ablation_failure": "Without a controlled return, reversibility and completion are not demonstrated."
    }
  ],
  "slots": [
    {
      "name": "adult_controller",
      "description": "One clearly adult original controller with three stable appearance anchors and readable hands."
    },
    {
      "name": "registered_environment",
      "description": "A stable original space with lines and objects that make field registration easy to verify."
    },
    {
      "name": "corner_system",
      "description": "Four original markers or material corners visibly attached to the controlling hands."
    },
    {
      "name": "bounded_state",
      "description": "A local visual or informational state that can intensify without leaking beyond the declared field."
    },
    {
      "name": "proof_sizes",
      "description": "At least three distinct field sizes or configurations, each obeying the same causal rule."
    },
    {
      "name": "apex_content",
      "description": "The largest late-stage coverage with a more information-dense but still bounded proof state."
    },
    {
      "name": "return_confirmation",
      "description": "A clean collapse followed by one stable baseline confirmation."
    },
    {
      "name": "sound_family",
      "description": "Original activation, stretch, lock, apex and release cues; source audio semantics are not reused."
    }
  ],
  "anti_copy_exclusions": [
    "Do not reproduce the source performer, face, hair, wardrobe or body proportions.",
    "Do not reuse the source bedroom, posters, furniture or framing choreography.",
    "Do not copy the cyan/magenta corner design, arrows, radial strokes, floor splashes or exact gesture sequence.",
    "Do not claim a source prompt, creator identity, generating model or semantic soundtrack because none was supplied."
  ],
  "instantiations": [
    {
      "concept": "Archive relief-inspection window",
      "description": "A clearly adult museum conservator in a map archive draws four brass-phosphor corners; only the enclosed shelves and document table become animated clay topographic relief, expanding through three field sizes before collapsing and leaving one real paper label gently flipped.",
      "changed_slots": [
        "adult_controller",
        "registered_environment",
        "corner_system",
        "bounded_state",
        "proof_sizes",
        "apex_content",
        "return_confirmation",
        "sound_family"
      ]
    },
    {
      "concept": "Ceramic kiln thermal blueprint",
      "description": "A clearly adult ceramic engineer in a quiet kiln hall binds four ceramic light tabs; only the bounded kiln and vessel region becomes layered thermal blueprint glass, reaches a late heat-flow apex, then retracts to the untouched workshop as one real kiln gauge settles.",
      "changed_slots": [
        "adult_controller",
        "registered_environment",
        "corner_system",
        "bounded_state",
        "proof_sizes",
        "apex_content",
        "return_confirmation",
        "sound_family"
      ]
    }
  ],
  "failure_modes": [
    {
      "failure": "The effect activates before the hands define the field.",
      "repair": "Show the complete hand/corner relationship first, then let the bounded state appear."
    },
    {
      "failure": "The field floats away from its controllers.",
      "repair": "Bind every corner to a visible fingertip or hand-edge trajectory through all scale changes."
    },
    {
      "failure": "The transformed state leaks into the full scene.",
      "repair": "Keep hard containment at the moving boundary and preserve the exterior baseline."
    },
    {
      "failure": "Scale changes feel like unrelated overlays.",
      "repair": "Use the same corner physics and registered environment across at least three progressive sizes."
    },
    {
      "failure": "The apex cannot resolve.",
      "repair": "Delay maximum information density until late, then visibly contract before the baseline confirmation."
    }
  ],
  "transfer_tests": [
    {
      "concept": "Archive relief-inspection window",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04",
        "inv-05",
        "inv-06"
      ],
      "changed_slots": [
        "adult_controller",
        "registered_environment",
        "corner_system",
        "bounded_state",
        "proof_sizes",
        "apex_content",
        "return_confirmation",
        "sound_family"
      ],
      "finding": "The archive, brass-phosphor corners, clay relief, document proofs, label residue and original sound family change every surface while the hand-bound growth/apex/return mechanism remains legible."
    },
    {
      "concept": "Ceramic kiln thermal blueprint",
      "result": "pass",
      "preserved_invariant_ids": [
        "inv-01",
        "inv-02",
        "inv-03",
        "inv-04",
        "inv-05",
        "inv-06"
      ],
      "changed_slots": [
        "adult_controller",
        "registered_environment",
        "corner_system",
        "bounded_state",
        "proof_sizes",
        "apex_content",
        "return_confirmation",
        "sound_family"
      ],
      "finding": "The kiln, ceramic tabs, thermal glass, heat-flow proof, gauge payoff and sound family preserve the causal topology without retaining source identity, room, graphics or gestures."
    }
  ]
}
````

### locales/zh-CN.json

````text
{
  "schema_version": "public-display-locale/v1",
  "resource_kind": "case",
  "resource_id": "user-video-c317cd9648205026eef7ad47e61b5bc4",
  "locale": "zh-CN",
  "source_bindings": {
    "manifest_sha256": "a5017e2f1422e0dc80f146bf3f9d88cf141078ba8bb7a9743834837c30274bdb",
    "creative_dna_sha256": "4498f6801bdca630459c148b303e64a8524fc649f5b4a38bb509dceb17a8fd61"
  },
  "content": {
    "title": "四角框域｜手势扩场、箭头峰值与收束",
    "summary": "双手先定义四个受控角点，让注册框域从掌间逐级扩展到房间尺度；最大状态才加入方向图形与地面响应，随后由同一双手收束并恢复普通环境。",
    "quick_start": {
      "input_format": "明确成年原创控制者 + 稳定注册环境 + 四个手势角点 + 至少三种框域尺寸 + 晚段有界信息峰值 + 主动收束与基线回归",
      "recommended_input": "成年博物馆修复师在胡桃木地图桌前用四枚黄铜磷光角点拉出框域；只有框内纸张变成象牙色黏土等高线浮雕，框域从地图扩到档案柜，后段路线向量达到峰值，再收回掌心并让真实标本标签翻动一次。",
      "required_anchors": [
        "激活前先建立一名明确成年原创控制者、稳定注册环境和未激活的双手。",
        "手部几何必须先于活动角点形成，每个角或边始终绑定清楚可见的指尖或手部轨迹。",
        "变化严格限制在注册框域内，人物身份、空间锚点和边界两侧位置不得漂移。",
        "至少用三种框域尺寸证明同一规则；最大信息密度留到后段，再主动收束并完整回到基线。"
      ],
      "usage_steps": [
        "保留用户给出的主体与目标，补齐环境、角点系统、框域状态、尺寸证明、峰值和回归。",
        "先建立基线，再让双手几何触发四角框域。",
        "分别选择 MiniMax H3 或 Seedance 2.0 模板，只填写声明的变量槽位。",
        "生成前检查角点耦合、边界注册、尺寸差异、晚段峰值、完整回归、声音和反复制距离。"
      ],
      "applicable_scope": [
        "双手先定义四个受控角点，让注册框域从掌间逐级扩展到房间尺度；最大状态才加入方向图形与地面响应，随后由同一双手收束并恢复普通环境。",
        "适合 4–15 秒内能清楚建立基线、至少三次框域验真、晚段峰值和完整回归的原创视觉机制短片。",
        "适合需要稳定注册证明局部变化规则的 MiniMax H3 与 Seedance 2.0 项目。"
      ],
      "not_suitable_for": [
        "要求复制来源人物、房间、服装、角点配色、箭头、泼彩或精确手势的任务。",
        "无法保持框域内外空间注册，或希望直接进行无边界全画面换风格的概念。",
        "没有可见手势控制、没有尺寸证明或不需要回归原状态的松散效果展示。"
      ]
    },
    "creative_dna": {
      "complexity": "moderate",
      "mechanism": "稳定写实基线变成一块可逆验真面：清楚可见的双手先指定四个耦合角点，注册框域在保持控制者与环境不变的前提下经过多种尺寸逐级扩张；最大晚段状态增加更密集的方向或材质信息，最后由同一双手收束并恢复基线。",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "有界框域激活前，先建立一名明确成年的原创控制者、一个稳定注册环境，以及清楚可见的未激活双手。",
          "evidence_ids": [
            "obs-01",
            "obs-04",
            "beat-01"
          ],
          "ablation_failure": "缺少中性基线时，后续框域无法证明环境变化确实受控制者支配。"
        },
        {
          "id": "inv-02",
          "rule": "让手部几何先于每个活动角点形成，并让每个角或边始终清楚绑定指尖或手部轨迹。",
          "evidence_ids": [
            "obs-04",
            "obs-05",
            "beat-02"
          ],
          "ablation_failure": "如果角点独立出现，核心的手势到框域因果关系就会从可操作机制退化为装饰。"
        },
        {
          "id": "inv-03",
          "rule": "把转换或强化状态严格限制在一个注册移动框域内，同时保持身份以及边界两侧空间锚点不变。",
          "evidence_ids": [
            "obs-06",
            "obs-09",
            "beat-03",
            "beat-04"
          ],
          "ablation_failure": "如果变化泄漏到框域之外或注册漂移，效果就不再像一个可控的局部窗口。"
        },
        {
          "id": "inv-04",
          "rule": "至少展示三种有实质差异的框域尺寸或角点配置，并让它们遵守同一耦合与包含规则。",
          "evidence_ids": [
            "obs-05",
            "obs-11",
            "beat-02",
            "beat-03",
            "beat-05"
          ],
          "ablation_failure": "一个静态矩形只是叠加层；只有逐级变化且始终遵守规则的状态，才能证明控制可复用。"
        },
        {
          "id": "inv-05",
          "rule": "在包含规则已经清楚后，才把最大、信息最密集的图形状态留给晚段峰值。",
          "evidence_ids": [
            "obs-10",
            "obs-14",
            "obs-18",
            "beat-04"
          ],
          "ablation_failure": "如果最大视觉奇观早于规则出现，机制会变得嘈杂，递进也失去空间。"
        },
        {
          "id": "inv-06",
          "rule": "清楚收缩或关闭框域，并以同一控制者和同一环境恢复基线媒介结束。",
          "evidence_ids": [
            "obs-08",
            "obs-09",
            "obs-13",
            "beat-05",
            "beat-06"
          ],
          "ablation_failure": "没有受控回归，就无法证明可逆性与完整结束。"
        }
      ],
      "slots": [
        {
          "name": "adult_controller",
          "description": "一名明确成年的原创控制者，具有三项稳定外观锚点和清楚可见的双手。"
        },
        {
          "name": "registered_environment",
          "description": "一个原创稳定空间，其线条和物体能让框域注册易于验证。"
        },
        {
          "name": "corner_system",
          "description": "四个原创标记或实体角点，并且清楚连接控制它们的双手。"
        },
        {
          "name": "bounded_state",
          "description": "一种可以逐步增强、但不会泄漏到既定框域之外的局部视觉或信息状态。"
        },
        {
          "name": "proof_sizes",
          "description": "至少三种不同的框域尺寸或配置，并且全部遵守同一因果规则。"
        },
        {
          "name": "apex_content",
          "description": "后段最大的覆盖范围，具有更高信息密度但仍保持有界的验真状态。"
        },
        {
          "name": "return_confirmation",
          "description": "一次干净收束，随后给出一个稳定的基线确认。"
        },
        {
          "name": "sound_family",
          "description": "原创激活、拉伸、锁定、峰值与释放声响；不复用来源音频语义。"
        }
      ],
      "anti_copy_exclusions": [
        "不得复制来源表演者、面孔、发型、服装或身体比例。",
        "不得复用来源卧室、海报、家具或构图调度。",
        "不得复制青色/洋红角点设计、箭头、放射线、地面泼彩或精确手势顺序。",
        "不得声称存在来源提示词、创作者身份、生成模型或语义声音轨，因为这些证据均未提供。"
      ],
      "instantiations": [
        {
          "concept": "档案浮雕检视窗口",
          "description": "一名明确成年的博物馆修复师在地图档案室里画出四个黄铜磷光角点；只有框内书架和文献桌变成动态黏土等高线浮雕，框域经过三种尺寸扩张后收束，并让一张真实纸标签轻轻翻动。",
          "changed_slots": [
            "adult_controller",
            "registered_environment",
            "corner_system",
            "bounded_state",
            "proof_sizes",
            "apex_content",
            "return_confirmation",
            "sound_family"
          ]
        },
        {
          "concept": "陶瓷窑炉热力蓝图",
          "description": "一名明确成年的陶瓷工程师在安静窑炉大厅里绑定四个陶瓷光片；只有框内窑炉和器皿区域变成分层热力蓝图玻璃，晚段达到热流峰值，再收回到未改变的工坊，并让一个真实窑炉仪表归稳。",
          "changed_slots": [
            "adult_controller",
            "registered_environment",
            "corner_system",
            "bounded_state",
            "proof_sizes",
            "apex_content",
            "return_confirmation",
            "sound_family"
          ]
        }
      ],
      "failure_modes": [
        {
          "failure": "双手尚未定义框域，效果就提前激活。",
          "repair": "先完整展示双手与角点的关系，再让有界状态出现。"
        },
        {
          "failure": "框域脱离控制者漂移。",
          "repair": "在所有尺寸变化中，把每个角绑定到清楚可见的指尖或手部边线轨迹。"
        },
        {
          "failure": "转换状态泄漏到整个场景。",
          "repair": "在移动边界保持硬性包含，并维持框外基线。"
        },
        {
          "failure": "尺寸变化看起来像互不相关的叠加层。",
          "repair": "至少用三种渐进尺寸，并始终保持同一角点物理与注册环境。"
        },
        {
          "failure": "峰值无法收束。",
          "repair": "把最大信息密度推迟到后段，并在基线确认前清楚收缩。"
        }
      ],
      "transfer_tests": [
        {
          "concept": "档案浮雕检视窗口",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05",
            "inv-06"
          ],
          "changed_slots": [
            "adult_controller",
            "registered_environment",
            "corner_system",
            "bounded_state",
            "proof_sizes",
            "apex_content",
            "return_confirmation",
            "sound_family"
          ],
          "finding": "档案室、黄铜磷光角点、黏土浮雕、文献验真、标签残留和原创声音家族更换了全部表面，同时手势框域扩张、峰值与回归机制仍然清楚。"
        },
        {
          "concept": "陶瓷窑炉热力蓝图",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05",
            "inv-06"
          ],
          "changed_slots": [
            "adult_controller",
            "registered_environment",
            "corner_system",
            "bounded_state",
            "proof_sizes",
            "apex_content",
            "return_confirmation",
            "sound_family"
          ],
          "finding": "窑炉、陶瓷光片、热力玻璃、热流验真、仪表结果和声音家族保留了因果拓扑，同时不保留来源身份、房间、图形或手势。"
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
  "resource_id": "user-video-c317cd9648205026eef7ad47e61b5bc4",
  "locale": "en",
  "source_bindings": {
    "manifest_sha256": "a5017e2f1422e0dc80f146bf3f9d88cf141078ba8bb7a9743834837c30274bdb",
    "creative_dna_sha256": "4498f6801bdca630459c148b303e64a8524fc649f5b4a38bb509dceb17a8fd61"
  },
  "content": {
    "title": "Four-Corner Field | Hand Expansion, Graphic Apex, Collapse",
    "summary": "Assign four hand-coupled corners before growing a registered field from palm scale to room scale; reserve directional graphics and floor response for the largest late state, then collapse the field with the same hands and restore the baseline.",
    "quick_start": {
      "input_format": "Clearly adult original controller + stable registered environment + four hand-bound corners + at least three field sizes + late bounded information apex + active collapse and baseline return",
      "recommended_input": "At a walnut map table, a clearly adult museum conservator stretches a field from four brass-phosphor fingertip corners. Only the enclosed paper becomes ivory clay topography; the field grows from map to archive scale, reaches a late route-vector apex, collapses into the palms, and leaves one real specimen label flipping once.",
      "required_anchors": [
        "Establish one clearly adult original controller, a stable registered environment, and inactive hands before activation.",
        "Hand geometry must precede every active corner, and each corner or edge must remain attached to a visible fingertip or hand trajectory.",
        "Keep every changed state inside the registered field while preserving identity, spatial anchors, and cross-edge alignment.",
        "Prove one rule with at least three field sizes; reserve maximum information density for late, then actively collapse and return completely to baseline."
      ],
      "usage_steps": [
        "Preserve the user's subject and objective, then fill the environment, corner system, bounded state, size proofs, apex, and return.",
        "Establish the baseline first, then let the hand geometry trigger the four-corner field.",
        "Choose the MiniMax H3 or Seedance 2.0 template and fill only declared variable slots.",
        "Before generation, check corner coupling, boundary registration, size differences, late apex, complete return, sound, and anti-copy distance."
      ],
      "applicable_scope": [
        "Assign four hand-coupled corners before growing a registered field from palm scale to room scale; reserve directional graphics and floor response for the largest late state, then collapse the field with the same hands and restore the baseline.",
        "Original 4–15 second mechanism films that establish a baseline, prove at least three field states, reserve a late apex, and return completely.",
        "MiniMax H3 or Seedance 2.0 projects that use stable registration to prove bounded change."
      ],
      "not_suitable_for": [
        "Requests to copy the source identity, room, wardrobe, corner palette, arrows, splashes, or exact gestures.",
        "Concepts that cannot preserve cross-edge registration or that require an unbounded full-frame takeover.",
        "Loose effect showcases without visible hand control, scale proof, or a return to baseline."
      ]
    },
    "creative_dna": {
      "complexity": "moderate",
      "mechanism": "A stable photoreal baseline becomes a reversible proof surface: visible hands first assign four coupled corners, a registered bounded field grows through multiple sizes while preserving the controller and environment, the largest late state gains denser directional or material information, and the same hands collapse the field to restore the baseline.",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "Establish one clearly adult original controller, one stable registered environment and visibly inactive hands before the bounded field activates.",
          "evidence_ids": [
            "obs-01",
            "obs-04",
            "beat-01"
          ],
          "ablation_failure": "Without a neutral baseline, the later frame cannot prove that the environment changed under user control."
        },
        {
          "id": "inv-02",
          "rule": "Make hand geometry precede every active corner and keep each corner or edge visibly coupled to fingertips or hand trajectories.",
          "evidence_ids": [
            "obs-04",
            "obs-05",
            "beat-02"
          ],
          "ablation_failure": "If corners appear independently, the central hand-to-field causality becomes decorative rather than operational."
        },
        {
          "id": "inv-03",
          "rule": "Keep the transformed or intensified state bounded by one registered moving field while preserving identity and spatial anchors across its edge.",
          "evidence_ids": [
            "obs-06",
            "obs-09",
            "beat-03",
            "beat-04"
          ],
          "ablation_failure": "If the change leaks beyond the field or registration drifts, the effect stops reading as a controllable local window."
        },
        {
          "id": "inv-04",
          "rule": "Show at least three materially different field sizes or corner configurations that obey the same coupling and containment rule.",
          "evidence_ids": [
            "obs-05",
            "obs-11",
            "beat-02",
            "beat-03",
            "beat-05"
          ],
          "ablation_failure": "One static rectangle is merely an overlay; progressive rule-consistent states prove reusable control."
        },
        {
          "id": "inv-05",
          "rule": "Reserve the largest and most information-dense graphic state for a late apex after the containment rule is already legible.",
          "evidence_ids": [
            "obs-10",
            "obs-14",
            "obs-18",
            "beat-04"
          ],
          "ablation_failure": "If maximum spectacle arrives before the rule, the mechanism becomes noisy and the escalation has nowhere to go."
        },
        {
          "id": "inv-06",
          "rule": "Visibly contract or dismiss the field and end with the same controller and environment restored in the baseline medium.",
          "evidence_ids": [
            "obs-08",
            "obs-09",
            "obs-13",
            "beat-05",
            "beat-06"
          ],
          "ablation_failure": "Without a controlled return, reversibility and completion are not demonstrated."
        }
      ],
      "slots": [
        {
          "name": "adult_controller",
          "description": "One clearly adult original controller with three stable appearance anchors and readable hands."
        },
        {
          "name": "registered_environment",
          "description": "A stable original space with lines and objects that make field registration easy to verify."
        },
        {
          "name": "corner_system",
          "description": "Four original markers or material corners visibly attached to the controlling hands."
        },
        {
          "name": "bounded_state",
          "description": "A local visual or informational state that can intensify without leaking beyond the declared field."
        },
        {
          "name": "proof_sizes",
          "description": "At least three distinct field sizes or configurations, each obeying the same causal rule."
        },
        {
          "name": "apex_content",
          "description": "The largest late-stage coverage with a more information-dense but still bounded proof state."
        },
        {
          "name": "return_confirmation",
          "description": "A clean collapse followed by one stable baseline confirmation."
        },
        {
          "name": "sound_family",
          "description": "Original activation, stretch, lock, apex and release cues; source audio semantics are not reused."
        }
      ],
      "anti_copy_exclusions": [
        "Do not reproduce the source performer, face, hair, wardrobe or body proportions.",
        "Do not reuse the source bedroom, posters, furniture or framing choreography.",
        "Do not copy the cyan/magenta corner design, arrows, radial strokes, floor splashes or exact gesture sequence.",
        "Do not claim a source prompt, creator identity, generating model or semantic soundtrack because none was supplied."
      ],
      "instantiations": [
        {
          "concept": "Archive relief-inspection window",
          "description": "A clearly adult museum conservator in a map archive draws four brass-phosphor corners; only the enclosed shelves and document table become animated clay topographic relief, expanding through three field sizes before collapsing and leaving one real paper label gently flipped.",
          "changed_slots": [
            "adult_controller",
            "registered_environment",
            "corner_system",
            "bounded_state",
            "proof_sizes",
            "apex_content",
            "return_confirmation",
            "sound_family"
          ]
        },
        {
          "concept": "Ceramic kiln thermal blueprint",
          "description": "A clearly adult ceramic engineer in a quiet kiln hall binds four ceramic light tabs; only the bounded kiln and vessel region becomes layered thermal blueprint glass, reaches a late heat-flow apex, then retracts to the untouched workshop as one real kiln gauge settles.",
          "changed_slots": [
            "adult_controller",
            "registered_environment",
            "corner_system",
            "bounded_state",
            "proof_sizes",
            "apex_content",
            "return_confirmation",
            "sound_family"
          ]
        }
      ],
      "failure_modes": [
        {
          "failure": "The effect activates before the hands define the field.",
          "repair": "Show the complete hand/corner relationship first, then let the bounded state appear."
        },
        {
          "failure": "The field floats away from its controllers.",
          "repair": "Bind every corner to a visible fingertip or hand-edge trajectory through all scale changes."
        },
        {
          "failure": "The transformed state leaks into the full scene.",
          "repair": "Keep hard containment at the moving boundary and preserve the exterior baseline."
        },
        {
          "failure": "Scale changes feel like unrelated overlays.",
          "repair": "Use the same corner physics and registered environment across at least three progressive sizes."
        },
        {
          "failure": "The apex cannot resolve.",
          "repair": "Delay maximum information density until late, then visibly contract before the baseline confirmation."
        }
      ],
      "transfer_tests": [
        {
          "concept": "Archive relief-inspection window",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05",
            "inv-06"
          ],
          "changed_slots": [
            "adult_controller",
            "registered_environment",
            "corner_system",
            "bounded_state",
            "proof_sizes",
            "apex_content",
            "return_confirmation",
            "sound_family"
          ],
          "finding": "The archive, brass-phosphor corners, clay relief, document proofs, label residue and original sound family change every surface while the hand-bound growth/apex/return mechanism remains legible."
        },
        {
          "concept": "Ceramic kiln thermal blueprint",
          "result": "pass",
          "preserved_invariant_ids": [
            "inv-01",
            "inv-02",
            "inv-03",
            "inv-04",
            "inv-05",
            "inv-06"
          ],
          "changed_slots": [
            "adult_controller",
            "registered_environment",
            "corner_system",
            "bounded_state",
            "proof_sizes",
            "apex_content",
            "return_confirmation",
            "sound_family"
          ],
          "finding": "The kiln, ceramic tabs, thermal glass, heat-flow proof, gauge payoff and sound family preserve the causal topology without retaining source identity, room, graphics or gestures."
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
  "case_id": "user-video-c317cd9648205026eef7ad47e61b5bc4",
  "slug": "hand-bounded-local-medium-window",
  "title": "四角框域｜手势扩场、箭头峰值与收束",
  "source_title": "四角框域｜手势扩场、箭头峰值与收束",
  "summary": "双手先定义四个受控角点，让注册框域从掌间逐级扩展到房间尺度；最大状态才加入方向图形与地面响应，随后由同一双手收束并恢复普通环境。",
  "status": "released",
  "source_duration_seconds": 15.083333,
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
  "skill_ref": "../../../skills/hand-bounded-local-medium-window",
  "preview_refs": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/user-video-c317cd9648205026eef7ad47e61b5bc4/preview.mp4"
  },
  "preview_paths": {
    "gif": "preview.gif",
    "poster": "poster.webp",
    "mp4": "media/user-video-c317cd9648205026eef7ad47e61b5bc4/preview.mp4"
  },
  "preview_status": {
    "gif": "available",
    "poster": "available",
    "mp4": "available_in_electron_media_pack"
  },
  "template_id": "t8-case-hand-bounded-local-medium-window-v1",
  "template_action": "evidence_variant",
  "duplicate_of": "user-video-715b76cd11b1098f170d41a9b71208ba",
  "input_format": "明确成年原创控制者 + 稳定注册环境 + 四个手势角点 + 至少三种框域尺寸 + 晚段有界信息峰值 + 主动收束与基线回归",
  "recommended_input": "成年博物馆修复师在胡桃木地图桌前用四枚黄铜磷光角点拉出框域；只有框内纸张变成象牙色黏土等高线浮雕，框域从地图扩到档案柜，后段路线向量达到峰值，再收回掌心并让真实标本标签翻动一次。",
  "required_anchors": [
    "激活前先建立一名明确成年原创控制者、稳定注册环境和未激活的双手。",
    "手部几何必须先于活动角点形成，每个角或边始终绑定清楚可见的指尖或手部轨迹。",
    "变化严格限制在注册框域内，人物身份、空间锚点和边界两侧位置不得漂移。",
    "至少用三种框域尺寸证明同一规则；最大信息密度留到后段，再主动收束并完整回到基线。"
  ],
  "tags": [
    "hand-bound",
    "four-corner",
    "registered-field",
    "graphic-apex",
    "controlled-return"
  ],
  "quality": {
    "weighted_score": 4.853,
    "scale": 5,
    "anti_copy_passed": true,
    "prompt_validation": {
      "minimax_h3": true,
      "seedance_2_0": true
    },
    "release_passed": true
  },
  "created_at": "2026-08-25T04:31:16+08:00",
  "updated_at": "2026-08-25T04:54:15+08:00"
}
````

### prompts/minimax-h3.md

````text
# MiniMax H3 — user-video-c317cd9648205026eef7ad47e61b5bc4

Validation: PASS

```text
integrated_multimodal_description: [Shot 1] Premium photoreal conservation workshop with warm paper, dark walnut drawers, indigo cloth and restrained brass-phosphor light; the bounded alternate state uses tactile ivory clay relief and precise contour shadows, never an unrelated full-frame style takeover. In one frontal medium-wide continuous shot, establish a clearly adult original museum conservator with a silver-streaked dark crop, round tortoiseshell glasses, an indigo apron and one brass compass pin at a walnut map table. Archive drawers, rolled maps, one cream specimen label and both empty hands are visible. The conservator raises both hands into four separated corner positions; no field or relief exists before the geometry is complete. [Shot 2] At 00:02.600, Four tiny brass-phosphor tabs ignite exactly at the controlling fingertips. The hands separate into a compact horizontal rectangle over one folded map. Only the enclosed paper becomes shallow ivory clay topography with registered roads and folds; the exterior map, table and hands stay photoreal. Preserve the same face, glasses, pin, apron and archive geometry. [Shot 3] At 00:05.400, Let the camera ease backward as the conservator widens the hand-bound field first across the map table and then into a tall shelf-scale rectangle. Every corner follows a visible fingertip. New enclosed drawers and rolled documents become tactile relief while every exterior surface remains normal; keep edge registration exact through all three sizes. [Shot 4] At 00:08.900, At the late largest state, hold the conservator centered inside an archive-scale field. Raised contour ridges grow only inside it; fine brass route vectors and small elevation markers flow from the table toward the shelves, and ivory relief dust gathers along the lower inside edge. The exterior room remains photoreal and the adult identity does not change. [Shot 5] At 00:12.200, The conservator draws both hands inward. The archive-scale field contracts through a desk-sized rectangle and one palm-sized frame; contour ridges flatten into real paper immediately behind the moving edge, route vectors disappear, and the camera eases closer without changing frontal registration. [Shot 6] At 00:14.100, The four brass tabs meet and extinguish between the hands. Hold the same fully photoreal conservator and unchanged archive as the original cream specimen label beside the map flips once from a natural draft. No text, logo, identity change, source bedroom, neon corner palette, arrows, paint splashes or extra transformation.

overall_soundscape: Quiet archive room tone, dry paper movement and distant wooden drawer resonance; four small ceramic-brass ticks activate the corners, a low tactile scrape expands with the clay relief, delicate pin clicks mark each completed size, then the sound contracts into one close paper flutter. No dialogue.

non_diegetic_music: Minimal original felt-piano and brushed-frame pulse at approximately 78 BPM, adding one muted note per successful field size, widening into a restrained harmonic at the relief apex, then ending before the final paper-label flip.
```

## Trace

```json
[
  {
    "shot": 1,
    "start": 0.0,
    "source_beat_ids": [
      "beat-01"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-02"
    ]
  },
  {
    "shot": 2,
    "start": 2.6,
    "source_beat_ids": [
      "beat-02"
    ],
    "invariant_ids": [
      "inv-02",
      "inv-03"
    ]
  },
  {
    "shot": 3,
    "start": 5.4,
    "source_beat_ids": [
      "beat-03"
    ],
    "invariant_ids": [
      "inv-03",
      "inv-04"
    ]
  },
  {
    "shot": 4,
    "start": 8.9,
    "source_beat_ids": [
      "beat-04"
    ],
    "invariant_ids": [
      "inv-03",
      "inv-05"
    ]
  },
  {
    "shot": 5,
    "start": 12.2,
    "source_beat_ids": [
      "beat-05"
    ],
    "invariant_ids": [
      "inv-02",
      "inv-04",
      "inv-06"
    ]
  },
  {
    "shot": 6,
    "start": 14.1,
    "source_beat_ids": [
      "beat-06"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-06"
    ]
  }
]
```
````

### prompts/seedance-2.0.md

````text
# Doubao Seedance 2.0 — user-video-c317cd9648205026eef7ad47e61b5bc4

Validation: PASS

```text
任务：文本生成一支原创15秒连续镜头视觉机制短片：明确成年博物馆修复师用双手控制四个黄铜磷光角点，只让框域内部变成象牙色黏土等高线浮雕，三种尺寸证明规则，后段形成档案室尺度峰值，再收回框域并以真实纸标签翻动确认回归。
总时长约15秒，仅控制整体信息密度，不分配逐镜头秒数。
主体定义：修复师：一名明确成年的原创博物馆修复师，深色短发带一缕银发、圆形玳瑁眼镜、靛蓝围裙、黄铜罗盘胸针；全片保持同一张脸、年龄、眼镜、胸针、服装与身体比例；档案室：胡桃木地图桌、抽屉柜、卷轴地图、一张奶油色标本标签、暖纸色环境光；机位、桌面线条、柜体透视与光向全片稳定。
镜头1：固定正面中广景，不切镜；成年修复师、档案室和空闲双手先建立，完整四角手势形成后黄铜磷光角点才绑定指尖；脸、眼镜、胸针、围裙、地图桌、抽屉柜和标签全部清楚；暖纸色、胡桃木、靛蓝与少量黄铜磷光；<档案室底噪><四枚角点轻响>。
镜头2：保持正面轴线，开始缓慢后移；小横框只把折叠地图转为象牙色黏土等高线浮雕，再扩大到整张地图桌；每个角绑定指尖，框内外道路、折痕与桌线精确注册；写实暖纸色对比象牙浮雕与黄铜边缘；<低沉刮擦><两次尺寸锁定>。
镜头3：继续缓慢后移并保持正面透视；框域扩大成覆盖抽屉柜的竖向状态，只有框内抽屉与卷轴成为连续浮雕；人物身份、柜体透视和边界两侧位置不漂移；象牙浮雕仅在活动框域内出现；<第三次细小针扣声>。
镜头4：保持档案室尺度构图；晚段最大框域内等高线隆起，黄铜路线向量流向柜体，浮雕粉尘只聚集在内部下沿；同一成年修复师居中，所有框外物体保持写实；黄铜路线与象牙浮雕达到克制峰值；<浮雕层叠><受控低频展开>。
镜头5：沿原轴缓慢靠近；双手收拢，框域经桌面尺寸缩为掌心尺寸，浮雕随边缘压回真实纸张；恢复紧跟边界，角点持续绑定指尖；象牙与黄铜逐步退去；<边缘收缩><纸张恢复>。
镜头6：稳定停留在恢复后的正面中景；四角合拢熄灭，同一修复师与档案室纯写实，一张真实标本标签只翻动一次；全部原始人物与环境锚点恢复；只剩真实暖纸色与胡桃木；<近距纸标签轻响>。
整体风格与画质：原创高端写实博物馆修复影像，暖纸色、胡桃木、靛蓝围裙、克制黄铜磷光与象牙色黏土等高线浮雕；真实纸张与木材物理，不做无关全场换风格；同一成年身份与档案室注册稳定；角点先由双手定义；框内严格换媒；至少三种尺寸；最大信息密度留到后段；结尾完整回到写实基线。
约束：浮雕与路线信息只能出现在双手边界内部，框外永远保持原始写实状态；不得改变修复师身份、五官、眼镜、胸针、围裙比例、档案室透视或光向；不得加入来源人物、卧室、海报、青洋红角点、箭头、放射线、地面泼彩、精确手势、字幕、标志或随机文字。
```

## Trace

```json
[
  {
    "shot": 1,
    "source_beat_ids": [
      "beat-01",
      "beat-02"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-02"
    ],
    "primary_camera": "固定正面中广景，不切镜"
  },
  {
    "shot": 2,
    "source_beat_ids": [
      "beat-02",
      "beat-03"
    ],
    "invariant_ids": [
      "inv-02",
      "inv-03",
      "inv-04"
    ],
    "primary_camera": "保持正面轴线，开始缓慢后移"
  },
  {
    "shot": 3,
    "source_beat_ids": [
      "beat-03"
    ],
    "invariant_ids": [
      "inv-03",
      "inv-04"
    ],
    "primary_camera": "继续缓慢后移并保持正面透视"
  },
  {
    "shot": 4,
    "source_beat_ids": [
      "beat-04"
    ],
    "invariant_ids": [
      "inv-03",
      "inv-05"
    ],
    "primary_camera": "保持档案室尺度构图"
  },
  {
    "shot": 5,
    "source_beat_ids": [
      "beat-05"
    ],
    "invariant_ids": [
      "inv-02",
      "inv-04",
      "inv-06"
    ],
    "primary_camera": "沿原轴缓慢靠近"
  },
  {
    "shot": 6,
    "source_beat_ids": [
      "beat-06"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-06"
    ],
    "primary_camera": "稳定停留在恢复后的正面中景"
  }
]
```
````

### source.json

````text
{
  "schema_version": "public-source/v1",
  "case_id": "user-video-c317cd9648205026eef7ad47e61b5bc4",
  "source_type": "User-owned original creator contribution",
  "source_title": "四角框域｜手势扩场、箭头峰值与收束",
  "source_post_id": null,
  "canonical_url": "https://local.t8/user-supplied/c317cd9648205026eef7ad47e61b5bc4",
  "published_at": null,
  "model_attribution": {
    "model": "unknown",
    "status": "unknown",
    "basis": "No original post, prompt, or trustworthy generation metadata was supplied; visual appearance is not attribution evidence."
  },
  "prompt_evidence": {
    "binding": "video_only",
    "status": "absent",
    "note": "Compiled prompts are independent outputs and are not original-post evidence."
  },
  "video_reference": {
    "platform": "user-supplied",
    "author": "T8 original creator contribution",
    "post_url": "https://local.t8/user-supplied/c317cd9648205026eef7ad47e61b5bc4",
    "playback_mode": "source_post",
    "preview_gif": "./preview.gif",
    "preview_mp4": "media/user-video-c317cd9648205026eef7ad47e61b5bc4/preview.mp4",
    "poster": "./poster.webp",
    "preview_status": {
      "gif": "available",
      "poster": "available",
      "mp4": "available_in_electron_media_pack"
    },
    "fallback_mode": "open_original_post"
  },
  "rights": {
    "redistribution_allowed": true,
    "model_reference_allowed": false,
    "basis": "user_owned standing declaration bound to the exact case media hash"
  }
}
````

