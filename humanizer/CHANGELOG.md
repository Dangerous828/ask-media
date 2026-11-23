# humanizer 变更记录

## v2.1.0 — 2026-11-15

本地升级，规则本体仍与上游 [lieflat-less-ai-tone](https://github.com/larashero3-dotcom/lieflat-less-ai-tone) `main@fe77df0`（2026-11-11）一致；上游无新版本。四件事：

**1. 论文语体档 `--genre academic`（本轮主项）**

- `detect.py` 新增 `ACADEMIC_DEMOTE` / `ACADEMIC_PAPER_CHECKS` / `effective_levels()` 与 `--genre {general,academic}`。
- academic 档把 6 条与学术语体冲突的规则降为 C 只报告：提示语冒号、顿号并列≥3、过长前置定语、前置话题壳、句首连接词、当…时从句。翻案腔与起手式**保留 A 级**（论文里同样是空话）。X 级已否决项两档都不变。
- 追加「论文核查」4 项清单（引用真实性 / 数据自洽 / 贡献可验证 / 可复现性），明确写出脚本查不到、报告不等于已通过核查。术语一致性归入改写纪律：术语表内的词一律不改，不为求自然给术语换叫法。
- `report.py` 的 md/html 报告按存档里的 `levels` 分组，追加同一核查清单；旧存档（无 `levels`）回落通用档。
- **证据边界**：降级是工程判读，上游 520 万字语料不含学位论文；参考值仍是新闻自媒体语料，在论文里没有统计意义。写在 `references/academic-paper.md` 与报告头部。
- **回归测试** `tests/test_academic_genre.py`（13 项，标准库）：general 档等级表逐项等于上游、academic 恰好降 6 条、X 级恒定、核查清单只在 academic 出现、两档报告都能出、候选抽取不受影响。

**2. 上游 [PR #12](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/12) 本地先行**

5 个脚本启动时把 stdout/stderr 设为 UTF-8，修 Windows 下重定向到管道时的 `UnicodeEncodeError`（GBK 编不了「☐」「≈」）。macOS / Linux 无影响。已用 `PYTHONIOENCODING=gbk` 验证输出仍是合法 UTF-8。

**3. 论文流水线契约**

新增 `references/research-pipeline.md`：检索 → 精读证据包 → 成稿 → 去 AI 味 → 投稿，四道手各定交接物与完成判据；上游没交出产物就报缺口。`AGENTS.md` 文字创作表新增「论文全流程」一行指向它。

**注意**：论文流水线的环节 1（库检索）与环节 2（精读证据包）不在本仓提供，由作者用自己的文献管理工具完成并交出同形状交接物。本档已写成不依赖特定工具，未擅自补入任何工具。

**4. 上游 [PR #13](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/13) 迁移预案**

上游拟把 SKILL.md / DETECT.md / references/ / scripts/ 移进 `lieflat-less-ai-tone/` 子目录，尚未合并。**本仓不跟进**：这里以 `humanizer/` 平铺发布，根级路由与仓内相对引用都指向 `humanizer/SKILL.md`，重构会断路径且无收益。若上游合并，只同步规则正文与脚本行为变化，不照搬布局，见 `references/upstream-pr13.md`。

**许可**：公开版 [CC BY-NC 4.0](./LICENSE)，学位论文 / 个人投稿属非商业使用，够用；商业交付与产品集成需另购 [lieflat.work](https://lieflat.work/skills/less-ai-tone/#pricing) 授权，本轮未购买。

## v2.0.1 — 2026-11-12

修正 `references/academic-paper.md` 两处与上游规则表冲突的判断（2.0.0 入库后自查发现）：

- **「显著/大幅/明显」是 X 级（已否决）**，即使同段有具体数值也不改。2.0.0 把它列为"可改的空洞强度副词"，属过度清理，已改为明确不改，并新增「上游已否决项」一节。
- **结论冒号引列表、序数词小标题、「这意味着」复述** 同为 X 级，2.0.0 却要求拆分。已翻转为不改，并说明论文的「结果表明：」与（1）（2）（3）编号是规范格式。
- 补 F 级分号在论文语境下的处置：功能用法，不做密度清理。
- 明确第三节各项**不在脚本正则表内**，由模型层或人审判读，避免读者以为 `detect.py` 已覆盖。

## v2.0.0 — 2026-11-12

**整体替换为 lieflat-less-ai-tone v2 公开版。** 旧版 v1.1.0 不再保留在本仓。

### 换掉了什么

v1.1.0 是自写的词表 + 规则清单，没有测量依据。v2 带两轮实测：

- 第一轮 629 篇对照语料，建立分级（A 机械改 / B 建议改 / C 只报告 / X 已否决 / F 指纹）。
- 第二轮 270 对同题同事实配对复测 + 43 万次语义判断，**推翻了 v1 的三条规则**，降级进「X 级清单·永不执行」。

因此 v2 不是"更多规则"，而是"哪些规则不该执行"有了证据。

### 能力变化

- 新增 `scripts/detect.py` 脚本层：正则与结构指标可复现，不再靠模型每次拍脑袋。
- 新增语义层四类判读（同义重命名 / 段间衔接接口 / 冒号句 / 三连同构），判据封闭在 `references/semantic-criteria.md`。
- 工作流改为**先出改前报告 → 等用户回复 → 再改写 → 复测对比**，不再直接改稿。
- 明确区分"研究语料中的统计显著"与"本篇单次命中"，禁止据单篇断言作者是 AI。

### 本仓改动（相对上游公开版）

1. 目录名保持 `humanizer`，frontmatter `name` 对齐为 `humanizer`——`AGENTS.md` 路由、`write-article`、`write-tweet` 的既有引用不断。
2. `SKILL.md` 顶部加来源说明与商业授权提示。
3. 新增 `references/academic-paper.md`（论文 / 学位论文语体档）。
4. `AGENTS.md`「文字创作与发布」表新增论文一行。

### 学术档的证据边界

`academic-paper.md` 是**工程判读，非配对实测**。上游两轮语料不含学位论文与期刊稿；该档只做规则映射（哪些失效、哪些保留、哪些另需人工查），对外不得表述为"研究证明论文这样写是 AI 味"。其中「引用真实性 / 数据自洽 / 贡献可验证 / 可复现性」四项脚本查不到，必须人工核对，优先级高于所有措辞问题。

### 待办

- [ ] 若要给学术档补实测，需要同题同事实的论文对照语料，上游没有。
- [ ] `detect.py` 未对论文语体做阈值标定，论文场景下 A/B 级判定偏多，按 `academic-paper.md` 第四节降级处理。
