# user-video-c60dc5cf8a4d200086e60498c10bbc49

- 类型：案例原文（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。


## 原文（逐字收录，不改写）

### SUMMARY.md

````text
# 时尚密度复位｜身份锁定、拼贴回顾与英雄主标

## 用途

锁定同一名明确成年角色，用前景载体轮转多个协调造型模块；密度升至峰值后切入白场减负，再把旧造型拼贴回顾并收束到简洁英雄主标。

## 推荐输入格式

`成年原创角色三项身份锚点 + 至少四个双通道造型模块 + 可见转场载体 + 一个密度峰值 + 一个低密度完整人物复位 + 至少三项旧状态回顾 + 简洁英雄主标`

## 可直接改写的简短示例

> 一名剃光头、右脸有细铜色标记的成年男性时尚表演者，依次经过矿物剪裁、交通图、档案纸和工业信号四个模块；黑铜红密度峰值后进入象牙白两步秀场，再穿过三张旧造型接触表，最终停在原创 AXIS NOIR 主标。

## 必须保留的结构锚点

- 第一轮切换前先锁定一名明确成年原创角色的至少三项身份锚点，并在全部模块中保持一致。
- 每个造型模块至少同时改变服装、版式、道具、色彩或镜头职责中的两个通道；纯换色不算新模块。
- 所有模块切换都由前景物、图形边、布料或角色手势完成可见交接，并在一个峰值后插入显著低密度的完整人物段落。
- 复位后必须回顾至少三个此前已经出现的状态，再清场到人物、原创名称和一句主张都清楚的英雄主标。

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐格式补齐身份锚点、模块、转场、密度复位、回顾与主标。
3. 同时改变来源人物、服装、配色、文案、道具、版式、声音与精确节奏。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并核对全部结构锚点。

## 来源

- 作者：T8 original creator contribution
- 原帖：https://github.com/T8mars/minimax-h3-prompt-skill-T8/tree/main/catalog/cases/user-video-c60dc5cf8a4d200086e60498c10bbc49
````

### creative-dna.json

````text
{
  "complexity": "complex",
  "mechanism": "A clearly adult identity remains locked while action-led foreground carriers rotate through multiple coordinated fashion-and-graphic worlds; visual density climbs to overload, abruptly resets to a sparse full-character interval, then prior states return as a compact collage recap before one simple hero wordmark closes the campaign.",
  "invariants": [
    {
      "id": "inv-01",
      "rule": "Lock one clearly adult original character with at least three stable identity anchors before the first style switch, and preserve those anchors through every wardrobe and layout module.",
      "evidence_ids": [
        "obs-01",
        "obs-09",
        "beat-01",
        "beat-03"
      ],
      "ablation_failure": "If face, age read, silhouette or signature anchors drift, the montage becomes unrelated models instead of one campaign identity proving range."
    },
    {
      "id": "inv-02",
      "rule": "Every style module must change at least two coordinated channels among wardrobe, palette, layout, prop system and camera duty; a palette swap alone does not count.",
      "evidence_ids": [
        "obs-03",
        "obs-04",
        "obs-07",
        "beat-02",
        "beat-04"
      ],
      "ablation_failure": "If only color changes, the progression feels like a filter reel and loses the sense of distinct fashion worlds."
    },
    {
      "id": "inv-03",
      "rule": "Use visible foreground objects, graphic edges or character gestures as motivated handoffs between modules so action, camera and graphic transition occur in the same beat.",
      "evidence_ids": [
        "obs-08",
        "obs-15",
        "beat-01",
        "beat-02"
      ],
      "ablation_failure": "If modules are connected by arbitrary cuts, the sequence keeps surface variety but loses causal flow and tactile momentum."
    },
    {
      "id": "inv-04",
      "rule": "Escalate visual and typographic density to one peak, then insert a substantially sparser full-character interval before the recap.",
      "evidence_ids": [
        "obs-05",
        "obs-06",
        "obs-11",
        "beat-04",
        "beat-06"
      ],
      "ablation_failure": "Without the sparse reset, constant maximal density flattens the rhythm and makes the final escalation feel no stronger than the middle."
    },
    {
      "id": "inv-05",
      "rule": "After the reset, visibly recap at least three earlier states as image fragments or registered panels before resolving to one simple hero lockup.",
      "evidence_ids": [
        "obs-10",
        "obs-13",
        "beat-07",
        "beat-08"
      ],
      "ablation_failure": "If the hero card arrives without a recap, the ending reads as a disconnected poster rather than a payoff that gathers the campaign's prior evidence."
    },
    {
      "id": "inv-06",
      "rule": "Limit each module to one short original copy unit and preserve a clear subject-copy hierarchy, especially in the held final frame.",
      "evidence_ids": [
        "obs-12",
        "obs-13",
        "beat-08"
      ],
      "ablation_failure": "Dense or malformed copy competes with the character, harms legibility and repeats the source prompt's own stated typography weakness."
    }
  ],
  "slots": [
    {
      "name": "adult_identity",
      "description": "One original clearly adult subject with at least three stable face, hair, silhouette or accessory anchors."
    },
    {
      "name": "style_modules",
      "description": "At least four worlds that each change two or more coordinated channels, not palette alone."
    },
    {
      "name": "transition_carriers",
      "description": "Foreground props, graphic edges, fabric, gestures or registered panels that motivate each handoff."
    },
    {
      "name": "density_peak",
      "description": "The highest-load module where movement, copy and graphic layers converge without hiding identity."
    },
    {
      "name": "sparse_reset",
      "description": "A full-character low-density interval with restrained camera and effects."
    },
    {
      "name": "recap_system",
      "description": "Contact sheets, specimen cards, panels or fragments that visibly quote at least three earlier states."
    },
    {
      "name": "copy_units",
      "description": "One original short word or phrase per module, plus one simple final name hierarchy."
    },
    {
      "name": "hero_lockup",
      "description": "A held final frame that resolves the stable subject, campaign name and one concise proposition."
    },
    {
      "name": "sound_arc",
      "description": "Original modular beat families, a restrained reset texture and a decisive return cue; complete silence is optional, not required."
    }
  ],
  "anti_copy_exclusions": [
    "Do not use SOLVÉRA, KAWAII IS POWER, any source Japanese/Chinese slogans, Ima Studio or confusingly similar wording.",
    "Do not reproduce the source heroine's face, hairstyle, body proportions, anime design or exact outfit sequence.",
    "Do not reuse the Harajuku kawaii accessory inventory, exact pink/cyan/lavender/black/white/hot-pink order or exact source typography layouts.",
    "Do not reproduce the exact source timing, triptych design, collage geometry, poses, camera path or soundtrack.",
    "Do not treat the user prompt's self-evaluation sentences as generation instructions or observed evidence."
  ],
  "instantiations": [
    {
      "concept": "AXIS NOIR mineral tailoring campaign",
      "description": "A clearly adult original male fashion performer moves through mineral, transit-map, archival-tailoring and industrial-signal modules, then a white runway reset, contact-sheet recap and original AXIS NOIR hero lockup."
    },
    {
      "concept": "LUMA FIELD athletic footwear launch",
      "description": "A clearly adult original nonbinary runner keeps face and silhouette anchors while footwear, terrain diagrams, reflective fabrics and motion graphics change as coordinated modules before a sparse testing lane and evidence-wall recap."
    },
    {
      "concept": "ORBITAL INK fragrance film",
      "description": "A clearly adult original female perfumer moves through glass, botanical ink, metallic vapor and monochrome laboratory modules, followed by a low-density white table walk, specimen-card recap and restrained final product-name hero frame."
    }
  ],
  "failure_modes": [
    {
      "failure": "Character identity drifts between style modules.",
      "repair": "Declare three identity anchors, restate them in every module and include one explicit multi-panel verification before the density peak."
    },
    {
      "failure": "Modules differ only by color.",
      "repair": "Require at least two coordinated changes among wardrobe, layout, prop system, medium and camera duty for each switch."
    },
    {
      "failure": "Random hard cuts break momentum.",
      "repair": "Assign a visible carrier to every handoff and make its movement cross the cut boundary."
    },
    {
      "failure": "Every moment stays equally dense.",
      "repair": "Reserve one full-character low-density interval with fewer effects and calmer camera before the recap."
    },
    {
      "failure": "Recap and hero frame feel unrelated.",
      "repair": "Populate recap panels from previously shown states, then let those panels physically clear toward the final name field."
    },
    {
      "failure": "Typography becomes unreadable or malformed.",
      "repair": "Use one declared short copy unit per module, large simple letterforms and a held final lockup with no extra text."
    }
  ],
  "transfer_tests": [
    {
      "concept": "LUMA FIELD athletic footwear launch",
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
        "adult_identity",
        "style_modules",
        "transition_carriers",
        "density_peak",
        "sparse_reset",
        "recap_system",
        "copy_units",
        "hero_lockup",
        "sound_arc"
      ],
      "finding": "A sports-product campaign preserves identity proof, coordinated modules, density reset and recap while changing character, action vocabulary, environments, props, copy and visual medium."
    },
    {
      "concept": "ORBITAL INK fragrance film",
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
        "adult_identity",
        "style_modules",
        "transition_carriers",
        "density_peak",
        "sparse_reset",
        "recap_system",
        "copy_units",
        "hero_lockup",
        "sound_arc"
      ],
      "finding": "A slower luxury fragrance context can retain the same causal architecture using glass, vapor and specimen cards instead of kawaii fashion surfaces."
    }
  ]
}
````

### locales/zh-CN.json

````text
{
  "schema_version": "public-display-locale/v1",
  "resource_kind": "case",
  "resource_id": "user-video-c60dc5cf8a4d200086e60498c10bbc49",
  "locale": "zh-CN",
  "source_bindings": {
    "manifest_sha256": "e34bf9c0c919601007420dfc3ecec3a15b2f7e564efba4a3ebe472319d345a61",
    "creative_dna_sha256": "b3367d0df444a3cc1ca4c66c49b80185da0d66b2c17d0e274bad21096f61ca18"
  },
  "content": {
    "title": "时尚密度复位｜身份锁定、拼贴回顾与英雄主标",
    "summary": "锁定同一名明确成年角色，用前景载体轮转多个协调造型模块；密度升至峰值后切入白场减负，再把旧造型拼贴回顾并收束到简洁英雄主标。",
    "quick_start": {
      "input_format": "成年原创角色三项身份锚点 + 至少四个双通道造型模块 + 可见转场载体 + 一个密度峰值 + 一个低密度完整人物复位 + 至少三项旧状态回顾 + 简洁英雄主标",
      "recommended_input": "一名剃光头、右脸有细铜色标记的成年男性时尚表演者，依次经过矿物剪裁、交通图、档案纸和工业信号四个模块；黑铜红密度峰值后进入象牙白两步秀场，再穿过三张旧造型接触表，最终停在原创 AXIS NOIR 主标。",
      "required_anchors": [
        "第一轮切换前先锁定一名明确成年原创角色的至少三项身份锚点，并在全部模块中保持一致。",
        "每个造型模块至少同时改变服装、版式、道具、色彩或镜头职责中的两个通道；纯换色不算新模块。",
        "所有模块切换都由前景物、图形边、布料或角色手势完成可见交接，并在一个峰值后插入显著低密度的完整人物段落。",
        "复位后必须回顾至少三个此前已经出现的状态，再清场到人物、原创名称和一句主张都清楚的英雄主标。"
      ],
      "usage_steps": [
        "把示例主体、品牌与表层元素替换为原创概念。",
        "让身份锚点、模块交接、密度复位、回顾来源与终局主标都可见。",
        "分别选择 MiniMax H3 或 Seedance 2.0 模板，只填写声明的变量槽位。",
        "生成前检查身份连续性、文字可读性、节奏对比、声音和反复制边界。"
      ],
      "applicable_scope": [
        "锁定同一名明确成年角色，用前景载体轮转多个协调造型模块；密度升至峰值后切入白场减负，再把旧造型拼贴回顾并收束到简洁英雄主标。",
        "能够在 4–15 秒内保留全部身份、密度与回顾锚点的原创广告。",
        "需要强烈节奏对比与终局主标的 MiniMax H3 或 Seedance 2.0 项目。"
      ],
      "not_suitable_for": [
        "要求复制来源人物、品牌、口号、服装、配色或精确分镜的任务。",
        "无法设置显著低密度复位段或无法让回顾引用此前状态的概念。",
        "不需要身份连续性与广告式结尾的松散多地点叙事。"
      ]
    },
    "creative_dna": {
      "complexity": "complex",
      "mechanism": "同一名明确成年角色的身份始终锁定；由动作驱动的前景载体轮转多个协调的时尚与图形世界，视觉密度逐步升至过载后突然复位到低密度完整人物段落，再以紧凑拼贴回顾此前状态，最终用一个简洁英雄主标收束广告。",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "第一次风格切换前，用至少三项稳定身份锚点锁定一名明确成年的原创角色，并在每个服装与版式模块中持续保留。",
          "evidence_ids": ["obs-01", "obs-09", "beat-01", "beat-03"],
          "ablation_failure": "如果脸、成年年龄感、轮廓或标志锚点漂移，蒙太奇就会变成互不相关的模特，而不是同一广告身份对风格跨度的证明。"
        },
        {
          "id": "inv-02",
          "rule": "每个风格模块必须在服装、配色、版式、道具系统和镜头职责中至少协调改变两个通道；只换配色不算新模块。",
          "evidence_ids": ["obs-03", "obs-04", "obs-07", "beat-02", "beat-04"],
          "ablation_failure": "如果只改变颜色，推进就会像滤镜轮播，失去不同完整时尚世界的区分度。"
        },
        {
          "id": "inv-03",
          "rule": "使用可见的前景物、图形边缘或角色手势作为模块间的动机交接，让动作、镜头和图形转场发生在同一节拍。",
          "evidence_ids": ["obs-08", "obs-15", "beat-01", "beat-02"],
          "ablation_failure": "如果模块只靠任意硬切连接，序列虽然保留表面变化，却会失去因果流动和可触感的动势。"
        },
        {
          "id": "inv-04",
          "rule": "把视觉与文字密度提升到一个峰值，再在回顾前插入一个显著更稀疏的完整人物段落。",
          "evidence_ids": ["obs-05", "obs-06", "obs-11", "beat-04", "beat-06"],
          "ablation_failure": "没有低密度复位，持续满负荷会压平节奏，让最终升能看起来并不比中段更强。"
        },
        {
          "id": "inv-05",
          "rule": "复位后，以图像碎片或对齐面板清楚回顾至少三个此前状态，再收束到一个简洁英雄主标。",
          "evidence_ids": ["obs-10", "obs-13", "beat-07", "beat-08"],
          "ablation_failure": "如果英雄卡没有回顾铺垫，结尾会像一张断开的海报，而不是汇总此前广告证据的兑现。"
        },
        {
          "id": "inv-06",
          "rule": "每个模块只使用一个原创短文案单位，并保持清楚的人物—文字层级，尤其是最终停留帧。",
          "evidence_ids": ["obs-12", "obs-13", "beat-08"],
          "ablation_failure": "过密或畸形的文字会与角色争夺注意力、损害可读性，并重复来源提示词自己指出的字体弱点。"
        }
      ],
      "slots": [
        {
          "name": "adult_identity",
          "description": "一名明确成年原创主体，具有至少三项稳定的脸部、发型、轮廓或配饰锚点。"
        },
        {
          "name": "style_modules",
          "description": "至少四个风格世界，每个世界都协调改变两个以上通道，而不只是换配色。"
        },
        {
          "name": "transition_carriers",
          "description": "用于驱动每次交接的前景道具、图形边缘、布料、手势或对齐面板。"
        },
        {
          "name": "density_peak",
          "description": "动作、文案和图形层汇聚但不遮住身份的最高负荷模块。"
        },
        {
          "name": "sparse_reset",
          "description": "一个镜头与特效都更克制的低密度完整人物段落。"
        },
        {
          "name": "recap_system",
          "description": "清楚引用至少三个此前状态的接触表、样本卡、面板或碎片。"
        },
        {
          "name": "copy_units",
          "description": "每个模块一个原创短词或短句，外加一个简洁的最终名称层级。"
        },
        {
          "name": "hero_lockup",
          "description": "一个稳定停留的终局帧，同时解决稳定主体、广告名称和一句简明主张。"
        },
        {
          "name": "sound_arc",
          "description": "原创模块化节拍族、克制的复位声场和明确的回归提示；完全静音可选而非必需。"
        }
      ],
      "anti_copy_exclusions": [
        "不得使用 SOLVÉRA、KAWAII IS POWER、任何来源日文/中文口号、Ima Studio 或容易混淆的相似文字。",
        "不得复制来源女主角的脸、发型、身体比例、动漫造型或精确服装顺序。",
        "不得复用来源的原宿可爱配饰清单、粉/青/薰衣草/黑/白/亮粉精确顺序或精确文字版式。",
        "不得复现来源的精确时序、三联画设计、拼贴几何、姿势、镜头路径或配乐。",
        "不得把用户提示词中的自评句当作生成指令或已观察证据。"
      ],
      "instantiations": [
        {
          "concept": "AXIS NOIR 矿物剪裁广告",
          "description": "一名明确成年的原创男性时尚表演者经过矿物、交通图、档案剪裁和工业信号模块，随后进入白色秀场复位、接触表回顾和原创 AXIS NOIR 英雄主标。"
        },
        {
          "concept": "LUMA FIELD 运动鞋发布",
          "description": "一名明确成年的原创非二元跑者保持脸部与轮廓锚点，同时让鞋履、地形图、反光面料和动态图形以协调模块变化，之后进入低密度测试跑道与证据墙回顾。"
        },
        {
          "concept": "ORBITAL INK 香氛短片",
          "description": "一名明确成年的原创女性调香师经过玻璃、植物墨水、金属蒸汽和单色实验室模块，随后进入低密度白色台面行走、样本卡回顾和克制的最终产品名英雄帧。"
        }
      ],
      "failure_modes": [
        {
          "failure": "角色身份在风格模块之间漂移。",
          "repair": "声明三项身份锚点，在每个模块重申，并在密度峰值前加入一次明确的多面板验真。"
        },
        {
          "failure": "模块之间只有颜色不同。",
          "repair": "每次切换都要求服装、版式、道具系统、媒介和镜头职责中至少两项协调变化。"
        },
        {
          "failure": "随机硬切打断动势。",
          "repair": "为每次交接指定一个可见载体，并让它的运动跨越剪辑边界。"
        },
        {
          "failure": "所有时刻都保持相同密度。",
          "repair": "在回顾前预留一个特效更少、镜头更平静的低密度完整人物段落。"
        },
        {
          "failure": "回顾与英雄帧彼此无关。",
          "repair": "用此前已经展示的状态填充回顾面板，再让这些面板通过物理运动清场到最终名称区域。"
        },
        {
          "failure": "文字变得难读或畸形。",
          "repair": "每个模块只使用一个已声明的短文案单位、简洁大字形，并让最终主标停留且不增加文字。"
        }
      ],
      "transfer_tests": [
        {
          "concept": "LUMA FIELD 运动鞋发布",
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
            "adult_identity",
            "style_modules",
            "transition_carriers",
            "density_peak",
            "sparse_reset",
            "recap_system",
            "copy_units",
            "hero_lockup",
            "sound_arc"
          ],
          "finding": "运动产品广告在更换角色、动作词汇、环境、道具、文案和视觉媒介的同时，保留身份证明、协调模块、密度复位与回顾。"
        },
        {
          "concept": "ORBITAL INK 香氛短片",
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
            "adult_identity",
            "style_modules",
            "transition_carriers",
            "density_peak",
            "sparse_reset",
            "recap_system",
            "copy_units",
            "hero_lockup",
            "sound_arc"
          ],
          "finding": "节奏更慢的奢侈香氛语境可以用玻璃、蒸汽和样本卡替代可爱时尚表面，同时保留同一因果架构。"
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
  "resource_id": "user-video-c60dc5cf8a4d200086e60498c10bbc49",
  "locale": "en",
  "source_bindings": {
    "manifest_sha256": "e34bf9c0c919601007420dfc3ecec3a15b2f7e564efba4a3ebe472319d345a61",
    "creative_dna_sha256": "b3367d0df444a3cc1ca4c66c49b80185da0d66b2c17d0e274bad21096f61ca18"
  },
  "content": {
    "title": "Fashion Density Reset | Identity Lock, Recap Collage, Hero Mark",
    "summary": "Lock one clearly adult identity across coordinated fashion modules, escalate to a density peak, reset in a sparse full-character field, recap earlier states as a collage, then resolve to one clean hero mark.",
    "quick_start": {
      "input_format": "Clearly adult original character with three identity anchors + at least four multi-channel style modules + visible transition carriers + one density peak + one sparse full-character reset + recap of at least three prior states + one clean hero lockup",
      "recommended_input": "A clearly adult male fashion performer with a shaved head and thin copper cheek stripe moves through mineral tailoring, transit-map, archival-paper, and industrial-signal modules. After a black-copper-red density peak, he enters a sparse ivory two-step runway, passes three prior-look contact sheets, and settles into an original AXIS NOIR hero mark.",
      "required_anchors": [
        "Before the first switch, establish at least three identity anchors for one clearly adult original character and preserve them in every module.",
        "Each style module must change at least two coordinated channels among wardrobe, layout, props, palette, and camera duty; a palette swap alone is not a new module.",
        "Every module handoff must be visibly carried by a foreground object, graphic edge, fabric, or gesture, and one density peak must be followed by a substantially sparser full-character interval.",
        "After the reset, recap at least three previously shown states, then clear to a hero frame where the character, original name, and one proposition are all readable."
      ],
      "usage_steps": [
        "Replace the example subject, brand, and surface details with an original concept.",
        "Keep identity anchors, module handoffs, the density reset, recap provenance, and final hero mark visibly causal.",
        "Choose the MiniMax H3 or Seedance 2.0 template and fill only the declared variable slots.",
        "Before generation, check identity continuity, copy legibility, rhythm contrast, sound, and anti-copy distance."
      ],
      "applicable_scope": [
        "Lock one clearly adult identity across coordinated fashion modules, escalate to a density peak, reset in a sparse full-character field, recap earlier states as a collage, then resolve to one clean hero mark.",
        "Original 4–15 second campaigns that can preserve every identity, density, recap, and hero-lockup anchor.",
        "MiniMax H3 or Seedance 2.0 projects that need strong rhythmic contrast and a resolved campaign ending."
      ],
      "not_suitable_for": [
        "Requests to copy the source identity, brand, slogans, wardrobe, palette, or exact storyboard.",
        "Concepts that cannot support a clearly sparse reset or cannot make the recap quote earlier states.",
        "Loose multi-location narratives that do not need identity continuity or an advertising lockup."
      ]
    },
    "creative_dna": {
      "complexity": "complex",
      "mechanism": "A clearly adult identity remains locked while action-led foreground carriers rotate through multiple coordinated fashion-and-graphic worlds; visual density climbs to overload, abruptly resets to a sparse full-character interval, then prior states return as a compact collage recap before one simple hero wordmark closes the campaign.",
      "invariants": [
        {
          "id": "inv-01",
          "rule": "Lock one clearly adult original character with at least three stable identity anchors before the first style switch, and preserve those anchors through every wardrobe and layout module.",
          "evidence_ids": ["obs-01", "obs-09", "beat-01", "beat-03"],
          "ablation_failure": "If face, age read, silhouette or signature anchors drift, the montage becomes unrelated models instead of one campaign identity proving range."
        },
        {
          "id": "inv-02",
          "rule": "Every style module must change at least two coordinated channels among wardrobe, palette, layout, prop system and camera duty; a palette swap alone does not count.",
          "evidence_ids": ["obs-03", "obs-04", "obs-07", "beat-02", "beat-04"],
          "ablation_failure": "If only color changes, the progression feels like a filter reel and loses the sense of distinct fashion worlds."
        },
        {
          "id": "inv-03",
          "rule": "Use visible foreground objects, graphic edges or character gestures as motivated handoffs between modules so action, camera and graphic transition occur in the same beat.",
          "evidence_ids": ["obs-08", "obs-15", "beat-01", "beat-02"],
          "ablation_failure": "If modules are connected by arbitrary cuts, the sequence keeps surface variety but loses causal flow and tactile momentum."
        },
        {
          "id": "inv-04",
          "rule": "Escalate visual and typographic density to one peak, then insert a substantially sparser full-character interval before the recap.",
          "evidence_ids": ["obs-05", "obs-06", "obs-11", "beat-04", "beat-06"],
          "ablation_failure": "Without the sparse reset, constant maximal density flattens the rhythm and makes the final escalation feel no stronger than the middle."
        },
        {
          "id": "inv-05",
          "rule": "After the reset, visibly recap at least three earlier states as image fragments or registered panels before resolving to one simple hero lockup.",
          "evidence_ids": ["obs-10", "obs-13", "beat-07", "beat-08"],
          "ablation_failure": "If the hero card arrives without a recap, the ending reads as a disconnected poster rather than a payoff that gathers the campaign's prior evidence."
        },
        {
          "id": "inv-06",
          "rule": "Limit each module to one short original copy unit and preserve a clear subject-copy hierarchy, especially in the held final frame.",
          "evidence_ids": ["obs-12", "obs-13", "beat-08"],
          "ablation_failure": "Dense or malformed copy competes with the character, harms legibility and repeats the source prompt's own stated typography weakness."
        }
      ],
      "slots": [
        {
          "name": "adult_identity",
          "description": "One original clearly adult subject with at least three stable face, hair, silhouette or accessory anchors."
        },
        {
          "name": "style_modules",
          "description": "At least four worlds that each change two or more coordinated channels, not palette alone."
        },
        {
          "name": "transition_carriers",
          "description": "Foreground props, graphic edges, fabric, gestures or registered panels that motivate each handoff."
        },
        {
          "name": "density_peak",
          "description": "The highest-load module where movement, copy and graphic layers converge without hiding identity."
        },
        {
          "name": "sparse_reset",
          "description": "A full-character low-density interval with restrained camera and effects."
        },
        {
          "name": "recap_system",
          "description": "Contact sheets, specimen cards, panels or fragments that visibly quote at least three earlier states."
        },
        {
          "name": "copy_units",
          "description": "One original short word or phrase per module, plus one simple final name hierarchy."
        },
        {
          "name": "hero_lockup",
          "description": "A held final frame that resolves the stable subject, campaign name and one concise proposition."
        },
        {
          "name": "sound_arc",
          "description": "Original modular beat families, a restrained reset texture and a decisive return cue; complete silence is optional, not required."
        }
      ],
      "anti_copy_exclusions": [
        "Do not use SOLVÉRA, KAWAII IS POWER, any source Japanese/Chinese slogans, Ima Studio or confusingly similar wording.",
        "Do not reproduce the source heroine's face, hairstyle, body proportions, anime design or exact outfit sequence.",
        "Do not reuse the Harajuku kawaii accessory inventory, exact pink/cyan/lavender/black/white/hot-pink order or exact source typography layouts.",
        "Do not reproduce the exact source timing, triptych design, collage geometry, poses, camera path or soundtrack.",
        "Do not treat the user prompt's self-evaluation sentences as generation instructions or observed evidence."
      ],
      "instantiations": [
        {
          "concept": "AXIS NOIR mineral tailoring campaign",
          "description": "A clearly adult original male fashion performer moves through mineral, transit-map, archival-tailoring and industrial-signal modules, then a white runway reset, contact-sheet recap and original AXIS NOIR hero lockup."
        },
        {
          "concept": "LUMA FIELD athletic footwear launch",
          "description": "A clearly adult original nonbinary runner keeps face and silhouette anchors while footwear, terrain diagrams, reflective fabrics and motion graphics change as coordinated modules before a sparse testing lane and evidence-wall recap."
        },
        {
          "concept": "ORBITAL INK fragrance film",
          "description": "A clearly adult original female perfumer moves through glass, botanical ink, metallic vapor and monochrome laboratory modules, followed by a low-density white table walk, specimen-card recap and restrained final product-name hero frame."
        }
      ],
      "failure_modes": [
        {
          "failure": "Character identity drifts between style modules.",
          "repair": "Declare three identity anchors, restate them in every module and include one explicit multi-panel verification before the density peak."
        },
        {
          "failure": "Modules differ only by color.",
          "repair": "Require at least two coordinated changes among wardrobe, layout, prop system, medium and camera duty for each switch."
        },
        {
          "failure": "Random hard cuts break momentum.",
          "repair": "Assign a visible carrier to every handoff and make its movement cross the cut boundary."
        },
        {
          "failure": "Every moment stays equally dense.",
          "repair": "Reserve one full-character low-density interval with fewer effects and calmer camera before the recap."
        },
        {
          "failure": "Recap and hero frame feel unrelated.",
          "repair": "Populate recap panels from previously shown states, then let those panels physically clear toward the final name field."
        },
        {
          "failure": "Typography becomes unreadable or malformed.",
          "repair": "Use one declared short copy unit per module, large simple letterforms and a held final lockup with no extra text."
        }
      ],
      "transfer_tests": [
        {
          "concept": "LUMA FIELD athletic footwear launch",
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
            "adult_identity",
            "style_modules",
            "transition_carriers",
            "density_peak",
            "sparse_reset",
            "recap_system",
            "copy_units",
            "hero_lockup",
            "sound_arc"
          ],
          "finding": "A sports-product campaign preserves identity proof, coordinated modules, density reset and recap while changing character, action vocabulary, environments, props, copy and visual medium."
        },
        {
          "concept": "ORBITAL INK fragrance film",
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
            "adult_identity",
            "style_modules",
            "transition_carriers",
            "density_peak",
            "sparse_reset",
            "recap_system",
            "copy_units",
            "hero_lockup",
            "sound_arc"
          ],
          "finding": "A slower luxury fragrance context can retain the same causal architecture using glass, vapor and specimen cards instead of kawaii fashion surfaces."
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
  "case_id": "user-video-c60dc5cf8a4d200086e60498c10bbc49",
  "slug": "identity-locked-density-reset-recap-hero",
  "title": "时尚密度复位｜身份锁定、拼贴回顾与英雄主标",
  "source_title": "可爱即力量｜角色锁定的风格爆切时尚广告",
  "summary": "锁定同一名明确成年角色，用前景载体轮转多个协调造型模块；密度升至峰值后切入白场减负，再把旧造型拼贴回顾并收束到简洁英雄主标。",
  "status": "released",
  "source_duration_seconds": 10.125,
  "target_duration_seconds": 15.0,
  "models": ["MiniMax H3", "Seedance 2.0"],
  "template_id": "t8-case-identity-locked-density-reset-recap-hero-v1",
  "template_action": "selector",
  "duplicate_of": null,
  "input_format": "成年原创角色三项身份锚点 + 至少四个双通道造型模块 + 可见转场载体 + 一个密度峰值 + 一个低密度完整人物复位 + 至少三项旧状态回顾 + 简洁英雄主标",
  "recommended_input": "一名剃光头、右脸有细铜色标记的成年男性时尚表演者，依次经过矿物剪裁、交通图、档案纸和工业信号四个模块；黑铜红密度峰值后进入象牙白两步秀场，再穿过三张旧造型接触表，最终停在原创 AXIS NOIR 主标。",
  "required_anchors": [
    "第一轮切换前先锁定一名明确成年原创角色的至少三项身份锚点，并在全部模块中保持一致。",
    "每个造型模块至少同时改变服装、版式、道具、色彩或镜头职责中的两个通道；纯换色不算新模块。",
    "所有模块切换都由前景物、图形边、布料或角色手势完成可见交接，并在一个峰值后插入显著低密度的完整人物段落。",
    "复位后必须回顾至少三个此前已经出现的状态，再清场到人物、原创名称和一句主张都清楚的英雄主标。"
  ],
  "tags": ["identity", "fashion", "density", "reset", "recap", "hero"],
  "quality": {
    "weighted_score": 4.773,
    "scale": 5,
    "anti_copy_passed": true,
    "prompt_validation": {
      "minimax_h3": true,
      "seedance_2_0": true
    },
    "release_passed": true
  },
  "created_at": "2026-08-25T00:21:03+08:00",
  "updated_at": "2026-08-25T01:52:00+08:00"
}
````

### prompts/minimax-h3.md

````text
# MiniMax H3 — user-video-c60dc5cf8a4d200086e60498c10bbc49

Validation: PASS

```text
integrated_multimodal_description: [Shot 1] Original premium photoreal editorial fashion campaign with restrained cel-shaded contour accents, charcoal, copper, cobalt, ivory and signal-red palette, tactile mineral surfaces, transit diagrams, archival paper and precision industrial typography; mature, elegant, kinetic and rebellious without kawaii, Harajuku or source-brand motifs. A rotating brushed-aluminum cuff crosses the foreground of an extreme close-up and reveals one clearly adult original male performer with a shaved head, thin copper cheek stripe and long charcoal coat. He lifts a smoked visor and looks directly into the camera as the exact large word "WAKE" snaps into a clean cobalt field; the cuff completes the wipe without obscuring his face. [Shot 2] At 00:01.800, Track backward at low waist height as the same performer walks through three coordinated modules. Mineral shards rise around copper tailoring under the exact word "FORM"; a curved transit-map ribbon wipes into an ivory technical coat under "ROUTE"; an archival pattern sheet rolls across the lens and reveals a cobalt pleated coat under "CUT". Every module changes wardrobe, layout and prop system together while the shaved head, cheek stripe, face and proportions remain identical. [Shot 3] At 00:05.800, Split the screen into three registered portrait panels that verify the same face, cheek stripe and silhouette. The performer steps out of the center panel toward the lens; the camera passes beneath his hand into a black, copper and signal-red industrial module where stamped strips, drafting marks and one exact phrase "BREAK FORM" converge. Orbit halfway around him as he turns and opens the coat once; keep the copy readable and the identity unobscured. [Shot 4] At 00:09.200, Push into a quiet face-scale hold for one beat, then cut to a vast ivory runway with almost no graphics. The same performer takes exactly two measured steps while the camera retreats smoothly; only one thin copper ring expands beneath the second footfall. Reduce layer count, camera speed and typography to create a clear visual reset, but keep a faint room tone and two dry footsteps rather than complete silence. [Shot 5] At 00:11.700, The copper ring expands into a curved corridor of registered contact sheets showing at least three earlier AXIS NOIR looks. Fly through the corridor while the same face and cheek stripe repeat consistently, then let the sheets fold outward and expose the final full-body performer against a charcoal field. [Shot 6] At 00:13.400, Hold the final hero frame: the performer shifts one shoulder and gives a restrained confident half-smile while the exact original hierarchy "AXIS NOIR" above "MOTION IS FORM" resolves in large ivory type. One small copper line flashes, all secondary fragments clear, and the complete subject and mark remain still for the final 0.3 seconds. No extra words, copied branding, source identity, kawaii accessories or malformed lettering.

overall_soundscape: Original fashion-film sound design: brushed metal sweep, mineral clicks, paper roll, transit-line pulses, industrial stamp impacts, two dry runway footsteps, contact-sheet folds and a restrained copper-line resolve; no copied source audio and no dialogue.

non_diegetic_music: Original 146 BPM percussive electro-fashion pulse that changes instrumentation with each module, narrows to a low sustained tone during the ivory runway, then returns with one decisive full-beat accent for the recap and final mark.
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
      "inv-03",
      "inv-06"
    ]
  },
  {
    "shot": 2,
    "start": 1.8,
    "source_beat_ids": [
      "beat-02",
      "beat-03"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-02",
      "inv-03",
      "inv-06"
    ]
  },
  {
    "shot": 3,
    "start": 5.8,
    "source_beat_ids": [
      "beat-03",
      "beat-04"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-02",
      "inv-04",
      "inv-06"
    ]
  },
  {
    "shot": 4,
    "start": 9.2,
    "source_beat_ids": [
      "beat-05",
      "beat-06"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-04"
    ]
  },
  {
    "shot": 5,
    "start": 11.7,
    "source_beat_ids": [
      "beat-07"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-05"
    ]
  },
  {
    "shot": 6,
    "start": 13.4,
    "source_beat_ids": [
      "beat-08"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-05",
      "inv-06"
    ]
  }
]
```
````

### prompts/seedance-2.0.md

````text
# Doubao Seedance 2.0 — user-video-c60dc5cf8a4d200086e60498c10bbc49

Validation: PASS

```text
任务：文本生成一支原创高端时尚动态图形广告：锁定同一名明确成年男性角色，经过四个协调风格模块、密度峰值、象牙白秀场复位、旧造型拼贴回顾，最后收束到 AXIS NOIR 英雄主标。
总时长约15秒，仅控制整体信息密度，不分配逐镜头秒数。
主体定义：主角：一名明确成年的原创男性时尚表演者，剃光头、右脸一条细铜色标记、修长但真实的成年比例、长炭灰大衣；所有镜头保持同一张脸、年龄、头型、标记位置与身体比例；品牌系统：原创名称 AXIS NOIR，炭灰、铜色、钴蓝、象牙白与信号红；不得出现源品牌、可爱原宿配饰或源人物外观。
镜头1：穿过旋转金属袖口快速推进到极近景；同一成年主角抬起烟色护目镜并直视镜头，只显示清楚大字【WAKE】；袖口只完成前景擦镜，不遮挡脸；光头、铜色脸部标记和成年比例清楚；钴蓝背景、铜色细节、炭灰服装；<拉丝金属掠过><短促身份钩子音>。
镜头2：低机位平稳后退跟拍，三次转场都由可见载体穿越镜头；矿物碎片、交通线路带和档案纸卷依次触发三次协调造型转换，对应【FORM】【ROUTE】【CUT】；每轮同时改变服装、版式与道具系统，同一张脸和身材比例始终连续；铜色矿物、象牙白技术图、钴蓝档案造型；<矿物轻击><线路脉冲><纸卷声>。
镜头3：三联注册画面验真后，穿过主角手部进入半环绕低机位；同一主角从中间画面走出，在工业图形峰值中只做一次转身开衣；【BREAK FORM】完整可读；冲压条和制图线围绕但不遮住脸；峰值层数最高；黑、铜、信号红高对比；<三次卡片落位><工业冲压><半环绕上升音>。
镜头4：面部短停后硬切象牙白大全景，镜头平稳后退；同一主角只走两步，第二步脚下扩散一圈细铜环；几乎没有其他图形，完整人物与大片负空间清楚；柔和象牙白与单一铜色强调；<微弱空间底噪><两声干净脚步>。
镜头5：铜环展开后沿弯曲接触表走廊向前穿行；至少三张此前已出现的 AXIS NOIR 造型卡片依次清楚回顾，同一脸部锚点重复稳定；卡片引用此前状态而非随机新造型，走廊最终让出中心；回顾原有铜、钴蓝、象牙白与信号红模块；<接触表翻折><完整节拍重新进入>。
镜头6：正面完整人物英雄构图，最终稳定停留；卡片向外清空，主角轻微侧肩并露出克制微笑，只显示【AXIS NOIR】与【MOTION IS FORM】；人物、品牌名和一句主张层级清楚，其他碎片全部退出；炭灰底、象牙白大字、一条铜色闪线；<铜线闪烁><两音主标收束>。
整体风格与画质：原创高端写实时尚广告，轻微赛璐璐轮廓强调，拉丝金属、矿物、档案纸和工业制图纹理，炭灰/铜/钴蓝/象牙白/信号红配色，成熟、克制、动感、叛逆；身份锚点跨模块稳定；每轮至少改变两个风格通道；所有转场有可见载体；密度峰值与象牙白复位差异明确；旧造型卡片来自此前已展示状态；最终主标大而清楚。
约束：不得出现任何源品牌名、源口号、源日文或中文文字、源平台名或相似字样；不得复刻源女主角脸、发型、身体比例、服装、原宿可爱配饰、精确颜色顺序或精确版式；每个模块只能出现声明的一组短文字，不得增加随机文字或乱码；不得在象牙白复位段继续堆叠大量贴纸、图形或快速摇镜。
```

## Trace

```json
[
  {
    "shot": 1,
    "source_beat_ids": [
      "beat-01"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-03",
      "inv-06"
    ],
    "primary_camera": "穿过旋转金属袖口快速推进到极近景"
  },
  {
    "shot": 2,
    "source_beat_ids": [
      "beat-02",
      "beat-03"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-02",
      "inv-03"
    ],
    "primary_camera": "低机位平稳后退跟拍，三次转场都由可见载体穿越镜头"
  },
  {
    "shot": 3,
    "source_beat_ids": [
      "beat-03",
      "beat-04"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-04",
      "inv-06"
    ],
    "primary_camera": "三联注册画面验真后，穿过主角手部进入半环绕低机位"
  },
  {
    "shot": 4,
    "source_beat_ids": [
      "beat-05",
      "beat-06"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-04"
    ],
    "primary_camera": "面部短停后硬切象牙白大全景，镜头平稳后退"
  },
  {
    "shot": 5,
    "source_beat_ids": [
      "beat-07"
    ],
    "invariant_ids": [
      "inv-05"
    ],
    "primary_camera": "铜环展开后沿弯曲接触表走廊向前穿行"
  },
  {
    "shot": 6,
    "source_beat_ids": [
      "beat-08"
    ],
    "invariant_ids": [
      "inv-01",
      "inv-05",
      "inv-06"
    ],
    "primary_camera": "正面完整人物英雄构图，最终稳定停留"
  }
]
```
````

### source.json

````text
{
  "schema_version": "public-source/v1",
  "case_id": "user-video-c60dc5cf8a4d200086e60498c10bbc49",
  "platform": "user-supplied",
  "author": "T8 original creator contribution",
  "source_title": "可爱即力量｜角色锁定的风格爆切时尚广告",
  "source_post_id": null,
  "canonical_url": "https://github.com/T8mars/minimax-h3-prompt-skill-T8/tree/main/catalog/cases/user-video-c60dc5cf8a4d200086e60498c10bbc49",
  "published_at": null,
  "model_attribution": {
    "model": "MiniMax H3",
    "status": "inferred",
    "basis": "The same-request original prompt explicitly names MiniMax H3, while the supplied video bytes do not independently verify the generating model."
  },
  "video_reference": {
    "platform": "user-supplied",
    "author": "T8 original creator contribution",
    "post_url": "https://github.com/T8mars/minimax-h3-prompt-skill-T8/tree/main/catalog/cases/user-video-c60dc5cf8a4d200086e60498c10bbc49",
    "playback_mode": "source_post",
    "fallback_mode": "open_original_post"
  }
}
````

