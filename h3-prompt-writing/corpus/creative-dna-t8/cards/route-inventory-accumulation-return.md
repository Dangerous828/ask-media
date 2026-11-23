# route-inventory-accumulation-return

- 类型：Creative DNA 机制卡（全量收录）
- 来源：T8mars/minimax-h3-prompt-skill-T8（案例库）· CC BY 4.0 内容许可（署名 T8mars；附仓库链接；本条目加入本地目录信息与检索元数据）。
- 验证状态：外部案例机制，**本地 h3q 未测**；不写成通过配方。
- 边界：英文骨架不是 H3 正文，禁止直接复制投产；机制不等于全局禁令。

## 原文（逐字收录，不改写）

### SKILL.md

````text
---
name: route-inventory-accumulation-return
description: "Create original short videos using the 晨间收获闭环｜人物巡园、连续采摘与动物回应 Creative DNA for MiniMax H3 or Seedance 2.0. Use when the user wants this causal, camera, motion, rhythm, or payoff structure with new subjects and surfaces."
---

# 晨间收获闭环｜人物巡园、连续采摘与动物回应

Create a new execution from the reusable mechanism, not a surface reskin of any reference video.

## Workflow

1. Read [references/summary.md](references/summary.md) for fit, input slots, and the concise starting example.
2. Read [references/template.md](references/template.md) completely before drafting.
3. Preserve the user's subject and objective, then fill every missing scene, trigger, event-chain, camera, sound, and payoff slot.
4. Treat these anchors as mandatory:

- One adult, route and container remain fixed.
- Every harvest action changes visible inventory.
- Animals remain secondary environmental witnesses.
- The final route return carries the completed harvest.

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
# 晨间收获闭环｜人物巡园、连续采摘与动物回应 — 摘要

## 用途

同一人物沿菜园路径完成巡看、采摘、装篮和离开，农作物变化形成进度证据；家禽只作为环境回应，不抢夺主任务，终局带着成果回到原路径。

## 推荐输入格式

`一名明确成年原创主体与一条可追踪往返路线 + 至少三次不同位置的可见收集接触 + 已收集对象持续保留并逐步累积 + 路线和方向连续可读 + 带着完整库存回到起点或交付点`

## 可直接改写的简短示例

> 成年屋顶园丁穿米色上衣，提空蓝筐沿路径行走，一只鸽子和一只小狗经过。；一次手部特写证明最后一个红椒从果梗脱离。；园丁提满筐沿开场路径返回，小狗在安全距离跟随。

## 必须保留的结构锚点

- One adult, route and container remain fixed.
- Every harvest action changes visible inventory.
- Animals remain secondary environmental witnesses.
- The final route return carries the completed harvest.

## 使用方法

1. 保留用户给出的主体与目标。
2. 按推荐输入格式补齐场景、事件链、镜头职责和结果。
3. 同时改变人物、环境、道具、风格、声音与结局表面，禁止只换名词。
4. 分别编译 MiniMax H3 与 Seedance 2.0，并逐项核对结构锚点。
````

### template.md

````text
# 晨间收获闭环｜人物巡园、连续采摘与动物回应 Template

## Mechanism

同一人物沿菜园路径完成巡看、采摘、装篮和离开，农作物变化形成进度证据；家禽只作为环境回应，不抢夺主任务，终局带着成果回到原路径。 The reusable mechanism preserves causal order, spatial anchors and the final proof while replacing every source-specific person, location, object, wording, choreography and design.

## Invariants

### inv-01

- Rule: One adult, route and container remain fixed.
- Purpose: Establishes the baseline identity, object or geography that every later state must preserve.
- Failure if removed: Without this exact baseline rule, later changes cannot be attributed to the same subject, object or place, so the sequence loses its reference state. Removed rule: "One adult, route and container remain fixed."

### inv-02

- Rule: Every harvest action changes visible inventory.
- Purpose: Makes the visible trigger precede and explain the first mechanism response.
- Failure if removed: Without this exact trigger rule, the response appears spontaneously and the central cause-and-effect claim is no longer demonstrated. Removed rule: "Every harvest action changes visible inventory."

### inv-03

- Rule: Close views prove physical detachment and placement.
- Purpose: Keeps the middle progression registered instead of allowing an unexplained reset.
- Failure if removed: Without this exact progression rule, the middle can jump to a replacement state and the accumulated result is no longer traceable. Removed rule: "Close views prove physical detachment and placement."

### inv-04

- Rule: Animals remain secondary environmental witnesses.
- Purpose: Reconnects the changed or partial state to the established subject and spatial anchor.
- Failure if removed: Without this exact reconnection rule, detail or transformed shots can belong to a different subject or geography and continuity cannot be verified. Removed rule: "Animals remain secondary environmental witnesses."

### inv-05

- Rule: The final route return carries the completed harvest.
- Purpose: Turns the terminal hold into observable proof that the mechanism completed.
- Failure if removed: Without this exact terminal-proof rule, the sequence stops on motion alone and never confirms the promised outcome or preserved aftermath. Removed rule: "The final route return carries the completed harvest."


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

- One adult, route and container remain fixed.
- Every harvest action changes visible inventory.
- Animals remain secondary environmental witnesses.
- The final route return carries the completed harvest.

## Anti-Copy Boundary

- all source faces, bodies, wardrobe, identities and creator-specific character designs
- the source location, set dressing, props, products and exact environmental geometry
- all source words, logos, watermarks, typefaces and brand identifiers
- the source choreography, exact camera path, shot durations and transition timing
- the source palette, signature effects, prompt wording, creator handle and narrative particulars

## Transfer Tests

1. A rooftop gardener fills one crate and returns with a companion dog.
   - Preserved: inv-01, inv-02, inv-03, inv-04, inv-05
   - Changed: lead_subject, setting, escalation_variable, performance_rule, camera_grammar, payoff, sound_family
2. An adult florist gathers cut stems into one bucket and returns through a greenhouse aisle.
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

