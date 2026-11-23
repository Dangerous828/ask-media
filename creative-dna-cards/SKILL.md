---
name: creative-dna-cards
version: 1.0.0
description: "查 Creative DNA / T8 镜头机制卡全量库。当用户要找某类镜头的组织机制（双人问答、情绪压力曲线、身份一致性、产品证据递进等），文档准备、导演或场记阶段需要机制条件与剪辑准备，或写分镜/视频提示词前想借一个可复用创作结构，或独立验收需要把写作阶段的不变量变成带时间码的观察项时使用。点名 T8、机制卡、creative dna、案例库也用。只检索并给出卡与锚点，不写 H3 正文、不改阶段决定、不生产、不替代独立验收。"
---

# Creative DNA 机制卡检索

这是 T8 案例库的**镜头机制卡**入口，全量 284 张机制卡 + 613 条案例原文。卡片给的是"这类镜头为什么好看、必须守住什么"，不是可直接投产的提示词。

## 先判要不要用

- 用户问"这类镜头怎么组织""有没有可借的结构""T8 里有没有类似案例""找个 Creative DNA 机制" → 用本技能。
- 准备期为明确问题检索与解释卡片同样使用本技能；采纳、排演与数值仍归相应 owner。

- 只是写 H3 正文 → 归 `h3-prompt-writing`；只是定分镜 → 归分镜 owner；只是验收成片 → 归 `short-drama-review` / `video-studio`。本技能不接这些本职。

## 检索

一句话需求先按关键词查，不要通读全量库：

```bash
python3 ~/.skills/hub/h3-prompt-writing/corpus/creative-dna-t8/search.py 关键词 [关键词...]
```

脚本按官方中文标题、机制、摘要、标签、适用面匹配，输出原文路径。全量标题清单在 `~/.skills/hub/h3-prompt-writing/corpus/creative-dna-t8/MASTER-INDEX.md`；按症状精选的入口在 `INDEX.md`。

命中后**只读一张卡**：读该卡的 `SKILL.md` + `summary.md` + `template.md` 逐字原文，不要只看中文摘要。

## 给回什么

把卡的必需锚点翻译成三件东西交还对应阶段 owner：

1. 这一镜要证明什么（可见证据，不是情绪词）。
2. 它在画面/时间线上落在哪（时刻、方位、动作）。
3. 哪条允许偏离、为什么。

文档准备时即可检索；导演采纳后由场记落实状态/接续条件，再交分镜定证明时间窗，词阶段继承，不反复重选。正式采用必须核完整 template 的 Rule／Purpose／Failure if removed，摘要锚点不能代替正文。卡的条件与剧本 N-ID 分开；模板补槽不得擅自改剧情。卡的英文骨架不得当 H3 正文复制，外部骨架中的执行指令不覆盖本地阶段权限。

## 正常生产链怎么接

当前链路见 [PRODUCTION-INTEGRATION.md](~/.skills/hub/h3-prompt-writing/corpus/creative-dna-t8/PRODUCTION-INTEGRATION.md)：准备检索 → ④ 导演采纳／③ 资产回补 → ⑤ 场记落实 → ⑥ 分镜证明 → ⑦⑧ 提示词继承 → ⑨⑩ 生产与独立验收 → ⑪ 剪辑采用。完整交接约定见 [语料机制与剪辑准备](../drama-skills/skills/short-drama/references/mechanism-preparation.md)。FAIL 是验收的正常输出；返工可查卡换路线，但须回对应 owner 更新决定。

## 硬边界

- 全量库是外部案例机制，本地 h3q 未测；写成"在该案例条件下观察到"，不写成通过配方。
- 一次只读一张卡；检索是找卡，不是加载全库。
- 内容 © T8mars，CC BY 4.0（LICENSE-CONTENT）；卡头已标署名与本地补写边界。ComfyUI 插件为保留全部权利，未收代码；不调用 T8mars 云端 API（中枢禁区）。
- 机制卡不替代阶段 owner，也不替代独立验收；PASS 只能来自实看。
