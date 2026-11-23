# H3 视频提示词语料库

收录**经过验证的完整视频提示词案例**：每条带原始出处、实际生成/复测证据、哪些结构起作用、哪些写法必须换成本地 H3 方言。写 H3 正文前按场景查同类条目。

## 条目格式

```markdown
# <场景>-<编号>
- 验证状态：本地 h3q 实测 / 外部复测（注明通道与分数）/ 未验证
- 来源：作者、原帖链接、收录仓库（外部条目遵守其许可证，CC BY 须署名）
- 完整原文：逐字保留，不改写——语料的价值在原文与证据的绑定
- 结构分析：哪段起什么作用（有生成证据）；哪些段要换成 H3 六段方言
- 边界：复测通道≠本地通道；分数是别人的评测口径，不是我们的 look/video_check
```

> 上述五段格式适用于本目录顶层精修条目。**T8 批量条目（`creative-dna-t8/`）用统一头部元数据 + 内嵌「原文」段**（外部案例机制，本地 h3q 未测），不另写「结构分析」节；仅少数本地精修卡带「结构分析（本地补写，非原文）」。

1. **案例保留为案例**。从案例提炼任何规则时，必须写成"在该案例条件下观察到"，不得升级为全局禁令——把个案蒸馏成教条会丢掉证据链，正是历史上错误吸收的形态。
2. 完整原文逐字保留；改写版另放，不覆盖原文。
3. 外部来源遵守其许可证（awesome-seedance 策展为 CC BY 4.0：署名作者＋原帖链接＋仓库链接）。T8mars 须分开看：仓库应用/公共校验代码为 MIT，但**原创摘要、机制说明与提示词模板为 CC BY 4.0**（许可声明内联于各卡正文，本公开版不附单独文件），需署名＋协议链接＋说明修改；ComfyUI 插件为保留全部权利，不收录代码。
4. 外部复测通过 ≠ 本地 h3q 通过。本地通道（MiniMax H3 本地权重、h3q 档位、我们的验收口径）未经实测就标未验证。

## 现有条目

| 条目 | 场景 | 状态 |
|---|---|---|
| [DV 手持vlog·首尔夏夜](seoul-night-dv-vlog.md) | DV 手持生活流 vlog | 外部复测通过（H3 Max 云端 75.7），本地未测 |
| [六宫格配置驱动分镜·示例项目](six-grid-storyboard-config.md) | 批量分镜＋整段氛围视频 | 来源项目实际产物，本地未测 |
| [官方技能写法·手绘实拍与品牌节拍](official-handdrawn-brand-beats.md) | 手绘融合、产品宣传片 | MiniMax 官方出品，本地未逐条实测 |
| [EP002·停车几何与参考职责](ep002-parking-contracts.md) | 窄位排演、参考改绑、逐镜验收与参数交接 | 本地事故观察，完整006/007原文留存；候选修法未实测 |

## Creative DNA 机制卡（全量 · 外部案例，本地未测）

从 [T8mars 案例库](https://github.com/T8mars/minimax-h3-prompt-skill-T8) 全量收录：**624 条可检索条目（613 案例原文 + 9 官方 Skill + 2 社区 Skill）**，与 `creative-dna-t8/catalog.json` / [MASTER-INDEX](creative-dna-t8/MASTER-INDEX.md) / `search.py` 同源可检索。**另有 273 张正式模板卡**仅见于上游 `catalog-index-source.json` 的 `recommendationEntities`，未入本地检索索引、`search.py` 搜不到；其原文落在 `cards/`（该目录共 284 文件 = 9 官方 + 2 社区 + 273 模板），需要时按上游来源补建索引。这类条目收录的是**镜头组织机制**（不变量／变量槽／反例），不是完整 H3 提示词；写作时按症状或关键词选一张，不整包加载。

入口：[Creative DNA 机制卡索引](creative-dna-t8/INDEX.md)（选卡表、检索命令、用卡三步、硬边界）· [正常生产链引入点](creative-dna-t8/PRODUCTION-INTEGRATION.md)（当前规则：准备检索 → 导演采纳／资产回补 → 场记落实 → 分镜与词继承 → 独立验收 → 剪辑；另保留 EP004 历史实证）· [MASTER-INDEX](creative-dna-t8/MASTER-INDEX.md)（624 条全量清单）· `python3 creative-dna-t8/search.py 关键词`（按中文标题／机制／摘要／标签检索）

| 卡 | 场景 | 状态 |
|---|---|---|
| [对话喜剧｜双轮停顿无声反应](creative-dna-t8/stage-two-turn-pause-reaction.md) | 双人问答、捧哏、停顿与无声反应 | 外部案例机制，本地 h3q 未测 |
| [情绪压力曲线｜压抑、峰值、遮挡与残余](creative-dna-t8/continuous-emotion-escalation-conceal-residue.md) | 委屈、忍住、哭出来、情绪落地 | 外部案例机制，本地 h3q 未测 |
| [多人商品一致性｜常驻参考板与角色接力实证](creative-dna-t8/persistent-reference-board-multi-character-product-continuity.md) | 跨场身份漂移、多角色一致性复核（只抽身份锚点两条） | 外部案例机制，本地 h3q 未测 |
| [产品广告｜功能证据递进](creative-dna-t8/structure-product-proof-launch.md) | 结果→证据→收束的产品演示（备用） | 外部案例机制，本地 h3q 未测 |

## 待挖源（登记未展开）

- **hypit**（[zhaihao118/hypit](https://github.com/zhaihao118/hypit)）：`skills/hypit/references/playbooks/craft/` 下 14 本写法手册（b-roll、字幕追踪、动图合成、声音混合、配音表演、画面指导等），服务"克隆病毒视频"工作流——对我们 video-shot-reverse 复刻线最有参考价值。逐本吸收时按条目格式入库。
- **MiniMax-H3 官方 skills/**：共 9 个技能（1 个 prompt-writing + 8 个风格技能，见 [OFFICIAL_SKILLS_INDEX.md](../OFFICIAL_SKILLS_INDEX.md)）。已吸收 3 个（prompt-writing 早已在主技能内、3d-animation 早已在主技能内、手绘+品牌已入库），余 5 个风格技能（co-op-game-intro、minimalist-product-ad、music-video-subtitle、paper-collage-explainer、papercraft-stop-motion）待按需挖。
- **Toonflow-app / T8-penguin-canvas / huobao-drama**：主分支无 prompt 资产（Toonflow 和 huobao 的内容在 release 包内；penguin-canvas 的提示词库在本地 SQLite 已登记）。需要时从 release 深挖。
