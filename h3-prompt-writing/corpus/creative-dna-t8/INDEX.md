# Creative DNA 机制卡索引（T8 · 全量语料库）

**这不是死仓。** 这里收录 T8 案例库全部文本：284 张机制卡（273 个正式模板 + 9 个官方 Skill + 2 个社区 Skill）、613 条案例原文，共 624 个官方索引条目。验证状态统一为**外部案例机制，本地 h3q 未测**。

## 三条进来路径

1. **从阶段链进来**：文档准备／`ask-media` 第 ④ 导演就按需检索；⑤ 场记落实，⑥ 分镜和⑧ 视频词继承已选条款。按 `ask-media/references/route-table.md` → 本索引 → 症状表或检索；不是直到写词才首次用卡。
2. **从写词技能进来**：`h3-prompt-writing/SKILL.md` Workflow 第 5 步 → `corpus/README.md` → 本索引 → 症状表或检索。
3. **从验收进来**：独立验收按写作阶段留下的锚点逐条核，FAIL 写成带时间码的 Finding 交还 owner；返工换路线可再查卡，但卡的主入口是写作前，不是事后。完整链路实证见 [PRODUCTION-INTEGRATION.md](PRODUCTION-INTEGRATION.md)。

> **卡内 `references/summary.md`、`references/template.md` 是上游 T8mars 原文残留链接，本地未收录**：
> 卡片是原文逐字收录、自足的，命中后直接读卡内「原文」段与机制锚点，不要去找这两个文件；
> `cases/`、`cards-community/` 里的 `../creative-dna.json`、`./prompts/...` 同理。

## 全量检索（关键词）

```bash
python3 corpus/creative-dna-t8/search.py 关键词 [关键词...]
```

例：`python3 corpus/creative-dna-t8/search.py 身份 情绪 停顿`（在本技能目录下运行）。脚本按官方中文标题、机制、摘要、标签、适用面匹配，输出原文路径；一次只读命中的一张卡。全量清单见 [MASTER-INDEX.md](MASTER-INDEX.md)。

## 按镜头要解决的问题选卡（写作前定时用，一次只读一张）

| 症状 / 需求 | 卡 | 拿哪条不变量 |
|---|---|---|
| 双人同镜一问一答、捧哏短答、结尾无声反应 | [双轮停顿无声反应](stage-two-turn-pause-reaction.md) | 双人中景眼线；一次清楚停顿；结尾第一人无声反应 |
| 委屈→忍住→哭出来→被逗笑 | [情绪压力曲线](continuous-emotion-escalation-conceal-residue.md) | 锁基线；三个不重置信号；遮挡后再露脸留残余 |
| 跨场身份漂移、参考图没人逐项核 | [常驻参考板](persistent-reference-board-multi-character-product-continuity.md) | 每个主体≥3 锚点；换场后强制视觉比对 |
| 产品广告、功能演示、结果先行 | [功能证据递进](structure-product-proof-launch.md) | 结果→可见证据→收束；先算时长 |

更多卡用上面的 `search.py` 按关键词找，不要通读 MASTER-INDEX。

## 用卡三步

1. 选卡 → 读该卡的**完整原文**（SKILL.md + summary.md + template.md 逐字收录），不要只看中文摘要。
2. 导演核完整 template 的不变量、目的与缺失后果，记录采纳/改编理由及承载镜头；资产按需补状态，场记落实状态与接续条件，分镜再给证明时间窗，词继承为可见证据。统一按 [语料机制与剪辑准备](../../../drama-skills/skills/short-drama/references/mechanism-preparation.md)，未定条件不宣称就绪。
3. 写完仍按本地链路走：场记取值 → 六段/三段 H3 方言 → `h3-video-gate` → 出片实看。**卡的英文骨架不是 H3 正文，禁止直接复制投产。**

## 硬边界

- 全量库是**外部案例机制**，不是通过配方；本地 h3q 未测，标"在该案例条件下观察到"。
- 一次只读一张卡；检索是找卡，不是加载全库。
- 署名：内容 © T8mars，CC BY 4.0（[LICENSE-CONTENT](https://github.com/T8mars/minimax-h3-prompt-skill-T8/blob/main/LICENSE-CONTENT)）；每张卡头部已标注来源与本地补写边界。ComfyUI 插件为保留全部权利，未收录其代码。
- **只做文本机制参考，不调用 T8mars 云端 API**（中枢禁区）。
- 机制卡不替代阶段 owner：选卡不改导演/分镜/场记的决定，改动仍回上游。
