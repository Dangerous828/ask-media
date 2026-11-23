# material-use-product-return

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

> **原文块内的相对链接**（`references/…`、`./prompts/…`、`creative-dna.json`、`locales/…`、`preview.gif`）指向**上游仓结构**，本仓只收文本、没有这些文件；查机制与检索入口见 [INDEX.md](../INDEX.md)。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: material-use-product-return
description: "Create original short videos using the 材质到使用｜产品关联与实证回归 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 材质到使用｜产品关联与实证回归

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- 产品身份连续
- 材质与使用有可见关系
- 不把暗示写成未经验证的功效

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
# 材质到使用｜产品关联与实证回归 — 摘要

## 用途

同一产品在材料、实际使用和回归镜头之间建立可检查的联系。

## 推荐输入格式

`原创产品＋两种材料线索＋使用动作＋结果回归`

## 可直接改写的简短示例

> 同一无品牌不锈钢冷饮瓶，浅绿色硅胶密封圈，一名明确成年的徒步者、深色帆布包和一条短林径；不得改动瓶身形状或角色身份。

## 必须保留的结构锚点

- 产品身份连续
- 材质与使用有可见关系
- 不把暗示写成未经验证的功效

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 材质到使用｜产品关联与实证回归 Template

## Mechanism

The source maintains one product identity while associating it with water, cream-like textures and a brief skin-touch use image, returns the product, then ends on an isolated droplet. This is an associative material-to-use-to-product sequence, not observed proof of efficacy. A reusable transfer can strengthen the structure by replacing implication with a practical visible test and bounded outcome.

## Invariants

### inv-01

- Rule: Establish one stable product shape before close material inserts.
- Purpose: Lets each texture and usage shot refer to the same object.
- Failure if removed: If shape or owner changes, the montage cannot be attributed to one product.

### inv-02

- Rule: Keep material associations and a brief use context attributable to the same established product; do not mistake source spectacle for observed efficacy.
- Purpose: Links attractive material cues to the product without inventing a measured skin result.
- Failure if removed: If material and use imagery lose their product anchor, the montage becomes generic decoration.

### inv-03

- Rule: Return to a readable product view after material and use imagery; an abstract coda may follow.
- Purpose: Closes the product-identity chain before any final decorative image.
- Failure if removed: Ending on abstraction alone without a prior product return weakens the identity payoff.


## Variable Slots

| Slot | Constraint |
|---|---|
| product | One original unbranded, stable object with consistent geometry. |
| material_test | Source-level material association or, in an original transfer, one visible practical property test; never claim invisible health efficacy. |
| environment | A coherent setting that materially participates in the test. |
| user | Optional clearly adult user, same identity if present. |
| camera | Product establishing view, material/contact view, use/result view, end product proof. |
| medium_palette | Original medium and colors; avoid source's blue-white water/flower/cream package. |
| sound | Original synchronized contact sounds, not source audio attribution. |

## Required Human-Facing Anchors

- 产品身份连续
- 材质与使用有可见关系
- 不把暗示写成未经验证的功效

## Anti-Copy Boundary

- No AQUA LUXE brand, exact label, jar, flower arrangement, splash composition or skin model.
- Do not infer measured hydration, medical results or before/after proof from the original clip.
- Do not copy the creator's source prompt wording or the exact shot order/cut timing.

## Transfer Tests

1. An unbranded reusable cold-drink bottle demonstrates its cap seal, condensation and leak-free short carry before a legible product return.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: product, material_test, environment, user, camera, medium_palette, sound
2. An original insulated lunch box shows a safe carry, then releases visible steam only after its lid opens to reveal the warm meal.
   - Preserved: inv-01, inv-02, inv-03
   - Changed: product, material_test, environment, user, camera, medium_palette, sound

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

