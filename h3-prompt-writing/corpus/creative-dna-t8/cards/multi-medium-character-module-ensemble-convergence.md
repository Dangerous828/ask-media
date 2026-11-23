# multi-medium-character-module-ensemble-convergence

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: multi-medium-character-module-ensemble-convergence
description: "Create original short videos using the 跨媒介角色集结｜五个独立风格模块最终共享同一舞台 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 跨媒介角色集结｜五个独立风格模块最终共享同一舞台

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Give every module one different original character and one medium-specific material rule.
- Include one short action that visibly demonstrates each medium's behavior.
- Keep each outgoing character readable until the next module's anchor arrives.
- Converge intact heterogeneous characters on one neutral stage without restyling them uniformly.

5. Change source-specific people, setting, props, palette, dialogue, shot boundaries, sound family, and payoff surfaces together.
6. Compile MiniMax H3 and Seedance 2.0 independently; do not leak one model's field syntax into the other.
7. Silently verify anchor coverage, continuity, timing, physical causality, and anti-copy distance before returning the final prompts.

## MiniMax H3

- Use the current official H3 task grammar and language profile.
- Separate integrated visual action, overall soundscape, and non-diegetic music or explicit silence.
- Use timestamps only to make event order executable; keep shots consecutive and duration-safe.

## Seedance 2.0

- Define stable subjects once and preserve event order, camera motivation, sound intent, and overall duration.
- Use a simple paragraph for simple concepts or an ordered multi-shot structure for complex concepts.
- State overall duration once; do not copy H3 field labels or per-shot timecode grammar.

## Output

Return one concept sentence, the filled slots, an anchor-coverage check, one MiniMax H3 prompt, one Seedance 2.0 prompt, and a short anti-copy validation note.

## Non-Negotiable

- A subject-only request is underspecified. Preserve that subject and complete the mechanism instead of returning a generic portrait or showcase.
- Do not omit, reorder, or weaken a required anchor.
- Do not reuse source people, brands, dialogue, exact storyboard, signature props, exact timings, or recognizable effect surfaces.
````

### summary.md

````text
# 跨媒介角色集结｜五个独立风格模块最终共享同一舞台 — 摘要

## 用途

每章用一个原创角色、一个明确媒介规则和一个短动作证明该风格，避免仅靠滤镜换色；固定构图位置、徽记或运动方向在章节间接力。所有角色最后必须以各自材质完整进入同一中性舞台，而不是被统一成同一种风格。

## 推荐输入格式

`至少四个独立风格模块 + 每模块一个原创角色、一条材料或线条行为规则和一个能证明媒介的短动作 + 重复构图位置、徽记或运动方向连接章节 + 出场角色在下一锚点到达前保持可读 + 终局所有角色以原材质进入同一中性舞台且不得统一重绘`

## 可直接改写的简短示例

> 原创陶瓷定格交通吉祥物站在编号底座上，迈一步并留下可见黏土压痕，先证明第一种媒介规则。；剪纸浮雕狐狸展开一层尾巴，随后原创线框光龟划出一条体积弧线；每种媒介都有完整可读模块和一个专属动作。；五个吉祥物以原材质共同进入中性站台：陶瓷压痕、石墨颗粒、纸层、光线框和刺绣都保持不同；原创标记 ROUTE FIVE 稳定收束，不使用来源角色或风格名称。

## 必须保留的结构锚点

- Give every module one different original character and one medium-specific material rule.
- Include one short action that visibly demonstrates each medium's behavior.
- Keep each outgoing character readable until the next module's anchor arrives.
- Converge intact heterogeneous characters on one neutral stage without restyling them uniformly.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 跨媒介角色集结｜五个独立风格模块最终共享同一舞台 Template

## Mechanism

Build at least four self-contained style modules. Each module must introduce one original character, one material or line-behavior rule, and one short action that could not be explained by color grading alone. Connect modules with one repeated composition slot, emblem position or motion direction. In the final beat, bring the intact characters into one neutral shared stage while preserving each character's original medium, edge behavior and surface response. The reusable mechanism is medium-specific proof, matched modular handoff and heterogeneous ensemble convergence—not the source characters, named styles, exact order, cards, text, creator identity or timing.

## Invariants

### inv-01

- Rule: Give every module one different original character and one medium-specific material rule.
- Purpose: Separates genuine style construction from palette swapping.
- Failure if removed: The same render with filters cannot prove cross-medium design.

### inv-02

- Rule: Include one short action that visibly demonstrates each medium's behavior.
- Purpose: Makes style observable through motion.
- Failure if removed: Static portraits provide weak transfer evidence.

### inv-03

- Rule: Repeat one composition slot, emblem position or motion direction across modules.
- Purpose: Creates continuity despite radical surface changes.
- Failure if removed: Unmatched cards read as unrelated samples.

### inv-04

- Rule: Keep each outgoing character readable until the next module's anchor arrives.
- Purpose: Makes transitions attributable rather than abrupt.
- Failure if removed: Hard replacement loses the connection.

### inv-05

- Rule: Converge intact heterogeneous characters on one neutral stage without restyling them uniformly.
- Purpose: Proves co-presence and completes the system.
- Failure if removed: A final common filter erases the central difference.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair with a readable role. |
| setting | A new setting with fixed spatial anchors and no source-specific surface. |
| escalation_variable | One causal variable that changes through visible stages. |
| performance_rule | A restrained acting or motion rule that keeps the mechanism legible. |
| camera_grammar | An information order that proves each state without copying source shot boundaries. |
| payoff | A clean final physical, informational or social consequence. |
| sound_family | An original hierarchy of diegetic cues; no unsupported source-audio claim. |

## Required Human-Facing Anchors

- Give every module one different original character and one medium-specific material rule.
- Include one short action that visibly demonstrates each medium's behavior.
- Keep each outgoing character readable until the next module's anchor arrives.
- Converge intact heterogeneous characters on one neutral stage without restyling them uniformly.

## Anti-Copy Boundary

- source warriors and representative character designs
- source clay, painted, ink, storybook and comic executions in their exact order
- source captions, style labels, logos and typography
- source module layouts, transitions and final ensemble staging
- source MiniMax H3 creator identity, prompt thread and timing

## Transfer Tests

1. Four original transit mascots appear as ceramic stop-motion, charcoal rubbings, cut-paper relief and wireframe light, then keep those materials while sharing one station platform.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. Five original research drones appear as woodblock, frosted glass, embroidered patch, mechanical pencil and neon tube modules, then assemble around one neutral lab table.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family

## Model Skeletons

### MiniMax H3

    integrated_multimodal_description: [new subject, environment, ordered actions, camera, light and final state preserving every anchor]
    overall_soundscape: [diegetic ambience, action cues and causal payoff]
    non_diegetic_music: [original music arc or N/A]

### Seedance 2.0

    任务：[原创实例意图]
    总时长约[4–15]秒。
    主体定义：[稳定人物、物体与空间关系]
    事件或镜头：[按因果顺序实现全部锚点]
    整体风格与画质：[原创媒介、光影、色彩与声音]
    约束：[连续性、物理逻辑、反复制与结尾状态]

Adapt shot count to the user's concept. Preserve the causal mechanism, not a fixed storyboard.
````

