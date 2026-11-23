# connect-independent-roles-to-shared-result

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: connect-independent-roles-to-shared-result
description: "Create original short videos using the 双角色职责｜独立建立后共同完成 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 双角色职责｜独立建立后共同完成

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- Establish Character A through one stable tool, local operation and visible intermediate result.
- Keep Character A's identity and result legible while its local operation completes.
- Bring both roles to one shared interface where each contribution is visibly required.
- Hold a concrete joint result while preserving both identities, tools and complementary responsibilities.

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
# 双角色职责｜独立建立后共同完成 — 摘要

## 用途

先分别用工具、局部动作和中间结果建立两个角色的独立职责，随后让双方在一个共享接口产生不可替代的依赖，最终以缺少任一方都无法完成的可见成果收束。

## 推荐输入格式

`角色A工具/操作/中间结果 + 角色B不同工具/操作/中间结果 + 共享接口 + 双贡献成果`

## 可直接改写的简短示例

> 铜腿土壤采样自动机完成矿物路径，玻璃泵站自动机独立建立水压；两者在矩形混合阀会合，缺一不可地启动滴灌并让幼苗成排抬起。

## 必须保留的结构锚点

- Establish Character A through one stable tool, local operation and visible intermediate result.
- Keep Character A's identity and result legible while its local operation completes.
- Bring both roles to one shared interface where each contribution is visibly required.
- Hold a concrete joint result while preserving both identities, tools and complementary responsibilities.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 双角色职责｜独立建立后共同完成 Template

## Mechanism

Establish two distinct characters through separate, observable responsibilities before they interact. Give each one stable identity, tool, local action and intermediate result; only after both roles are independently legible may they meet at one shared interface where both contributions are required. End on a concrete joint result that could not exist if either role were removed, while preserving both identities.

## Invariants

### inv-01

- Rule: Establish Character A through one stable tool, local operation and visible intermediate result.
- Purpose: Creates the first readable responsibility.
- Failure if removed: A generic portrait provides no role for the second character to depend on.

### inv-02

- Rule: Keep Character A's identity and result legible while its local operation completes.
- Purpose: Connects identity to function before any team action.
- Failure if removed: A prop held without consequence is only costume.

### inv-03

- Rule: Establish Character B later through a different tool, operation and intermediate result rather than replaying Character A.
- Purpose: Creates meaningful role contrast.
- Failure if removed: An identical second introduction feels like duplicated character art.

### inv-04

- Rule: Bring both roles to one shared interface where each contribution is visibly required.
- Purpose: Turns adjacency into causal interdependence.
- Failure if removed: Placing characters side by side does not explain how they connect.

### inv-05

- Rule: Hold a concrete joint result while preserving both identities, tools and complementary responsibilities.
- Purpose: Closes the sequence as a dependency proof.
- Failure if removed: A generic team pose or merged emblem cannot prove that both operations mattered.


## Variable Slots

| Slot | Constraint |
|---|---|
| lead_subject | An original stable subject or pair whose role is readable without source identity. |
| setting | A materially new setting with fixed spatial anchors and no source-specific surface. |
| carrier_or_token | One visible material, prop or symbolic anchor that carries the causal mechanism. |
| state_change | A sequence of visible, causally ordered changes rather than decorative montage. |
| camera_grammar | An information order that proves each change without copying source shot boundaries. |
| payoff | A held final state that resolves or recontextualizes the setup. |
| sound_family | An original hierarchy of visible-action sounds; no unsupported source-audio claim. |

## Required Human-Facing Anchors

- Establish Character A through one stable tool, local operation and visible intermediate result.
- Keep Character A's identity and result legible while its local operation completes.
- Bring both roles to one shared interface where each contribution is visibly required.
- Hold a concrete joint result while preserving both identities, tools and complementary responsibilities.

## Anti-Copy Boundary

- source white-haired and older long-haired characters
- astrolabe, hourglass, masks and constellation-map vocabulary
- source city triptych, circular camera rotation and split poster panels
- the exact source red brush ring, character silhouettes and final game-PV diagram

## Transfer Tests

1. In one continuous tactile greenhouse aisle, a copper-legged soil sampler inserts a mineral cartridge after testing a bed, a glass-bodied pump keeper separately primes water pressure, and both meet at a rectangular mixing valve; only their combined inputs feed straight drip lines and lift a row of seedlings.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, carrier_or_token, state_change, camera_grammar, payoff, sound_family
2. In a dark practical-effects theatre, a shadow-puppet rigger tensions three overhead lines while a miniature lamp keeper independently aligns a moving slit light; both operations meet at one stage shutter and produce a readable flying-bird shadow that neither role can create alone.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, carrier_or_token, state_change, camera_grammar, payoff, sound_family

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

