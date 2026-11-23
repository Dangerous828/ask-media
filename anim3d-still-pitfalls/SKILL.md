---
name: anim3d-still-pitfalls
version: 1.2.0
description: 3D 动画 / Q 版（竖屏或横屏）的关键帧或角色设定图（依赖垫图出图）出现漏盖漏汤、道具失忆、爬桌悬空、水平腰斩、身份漂移、表情呆或僵时的排障清单，作为 doc-still-prompt 的补充使用。整帧写作与改词由doc-still-prompt完成，不用于真人写实，不用于视频提示词。 短剧任务按正文读取对应阶段知识，本技能继续完成当前工作。
---

# 3D 动画静帧翻车排障

## 短剧项目协作（命中即读，保留本职）

本技能继续定位 3D 静帧问题并给出有条件修法，由 doc-still-prompt 完成改词。短剧身份/造型问题先读 [short-drama-assets](../drama-skills/skills/short-drama-assets/SKILL.md) 的 Look 与视角规则，阶段验收先读 [short-drama-review](../drama-skills/skills/short-drama-review/SKILL.md)；读取后继续当前排障，不转交全部工作。规则见 [协作契约](../SHORT-DRAMA-ROUTING.md)。已读上下文复用；只有跨阶段、状态或初始化才读取 short-drama 主路由。

本技能是 `doc-still-prompt` 的**补丁层**：只在 3D 动画/Q 版静帧出现下列实际故障，或同一通路已复现相应风险时，读取对应一页。doc-still 负责完整事实推导与成文；这里不追加一套全量写作模板。

不适用：真人写实、2D 插画及任何 H3/视频提示词。真人表演、摄影质感与视频写法各回其主技能，不把本页病例外推过去。

## 现象 → 核对位置 → 去读

| 已见现象或已复现风险 | doc-still 核对位置 | 按需读 |
|---|---|---|
| 多身体、画中画越界、门户两侧角色混用 | 身份、实例与区域 | [多人场面](../doc-still-prompt/references/multi-character-scenes.md) |
| 桌上凭空空碗、汤与面分离、内容物悬空 | 关键空间与容器关系 | [容器栈](references/container-stack.md) |
| 写了“密封”仍画成敞口；跨镜状态不符上游 | 容器状态、连续物 | [容器栈](references/container-stack.md) |
| 静置道具被画成手持武器 | 持物与归属 | [容器栈](references/container-stack.md) |
| 本应坐椅却双脚踩桌，或站姿无故悬空 | 姿态、支撑、接触 | [接地与构图](references/grounding-framing.md) |
| 横向家具实际把人物切成“上天地下” | 构图边界 | [接地与构图](references/grounding-framing.md) |
| 远景反复被拉回中景 | 机位、可见范围与比例 | [接地与构图](references/grounding-framing.md) |
| 已选长杆、杠杆等交互出现结构崩坏 | 力、接触与归属 | [接地与构图](references/grounding-framing.md) |
| 表情呆板，或夸张表演破坏既定姿态 | 表演与可读部位 | [动画轨表演](references/performance-anim-track.md) |
| 身份被“通用 Q 版小孩”带跑、鞋/瞳色错 | 可见身份锚点 | [身份与参考](references/identity-tested.md) |
| 身份与构图距离互相回退 | 身份锚点 × 构图 | [身份与参考](references/identity-tested.md) |

## 使用原则

1. **先保护已定事实**：跳、飞、坐地、蹲、躺和复杂机械都可成立。只有实际结果违背本帧姿态或交互时，才修对应支撑、接触或结构；不自动改成端坐、站姿或静物摆放。
2. **一次只修命中项**：没有把容器、远景或表演故障时，对应页为 NA。占比、字长、态度句、形变、遮挡和参考数量均不设通用配额。
3. **参考按故障选用**：文字声明反复被同一通路推翻，或现有参考带有相反状态时，才调整/补充相应局部参考；不是所有关键状态都必须另做局部垫图。
4. **正向描述可见关系**：病例中的否定句可改写为位置、接触、数量与状态。改写是否有效仍以实际通路结果为准，不把词面命中当作修复证据。
5. **实测带条件**：标“实测”的结论只代表所注模型、参考与参数组合；换模型或输入需重测。项目例子见 [外卖短剧 / 角色D原型线](references/examples-gungun.md)，只借诊断结构。

## 回填与验收边界

- 短剧镜头静帧的事实与正文由**分镜**条目承载，资产板由**资产/图片提示词**条目承载；doc-still 在同一正式条目内完成方法写作与回填，不叠加另一份四段稿。只有独立静帧且没有既有格式时，才采用 doc-still 的完整四段布局与适用脚本。
- 本技能可以核对文字、来源和引用，不能把文字通过称为出图成功。尚未生成或没有实际图片时，媒体项记 `NA：未生成/无图可验`，不得要求写词者宣称看过出图。
- 已生成图片的画风、剧情、身份与连续性验收唯一 owner 是 `short-drama-review`；由其查看实际媒体并记录结论。本技能只提供对应故障的复查点，不代替验收，也不以文件存在、队列完成或脚本退出码代替实看。

## references

| 文件 | 何时读取 |
|---|---|
| [container-stack.md](references/container-stack.md) | 容器层序、盖子状态、内容物归属或道具放置实际出错 |
| [grounding-framing.md](references/grounding-framing.md) | 非预期悬空/踩桌、横向切割、远景回拉或复杂交互崩坏 |
| [performance-anim-track.md](references/performance-anim-track.md) | 3D 表演不可读，或表演词引起姿态/材质故障 |
| [identity-tested.md](references/identity-tested.md) | 可见身份漂移、参考职责冲突或身份与构图互相回退 |
| [examples-gungun.md](references/examples-gungun.md) | 需要查看上述诊断的项目原例；不是新项目填空模板 |

## 来源档案

以下真实相对指针指向保留的 Slate 原卡，仅供追溯病例；原卡保持不动：

- [container-stack.md](../../../.skills-backup-20261016/slate-workbench-skills/image-style/container-stack.md)
- [physical-grounding.md](../../../.skills-backup-20261016/slate-workbench-skills/image-style/physical-grounding.md)
- [performance-dual-track.md](../../../.skills-backup-20261016/slate-workbench-skills/image-style/performance-dual-track.md)
- [identity-anchor.md](../../../.skills-backup-20261016/slate-workbench-skills/image-style/identity-anchor.md)
- [doc-still-qban-doctrine.md](../../../.skills-backup-20261016/slate-workbench-skills/image-style/doc-still-qban-doctrine.md)
