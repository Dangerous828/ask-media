# 阶段 → 该读哪份参考

> 技能名和阶段表在 [`../SKILL.md`](../SKILL.md)，这里不重复。
> 本文件只回答一件事：**到了某一步，除 SKILL.md 之外还要读哪份二级文件。**
> 路径均为仓库内相对路径，直接可解析（运行 `../../scripts/check_references.py` 可校验）。

## 按阶段查

| 阶段 | 这一步要读的参考 |
|---|---|
| 文档准备／③ 资产／④ 导演 | 按需读 `../../creative-dna-cards/SKILL.md` 检索，正式采用完整读 SKILL＋summary＋template；准备与分工读 `../../drama-skills/skills/short-drama/references/mechanism-preparation.md`。资产按导演需求回补状态，导演明确因果、表演保护段、声画组织与实现责任 |
| ② 剧本 | 明确用 H3 或问它适不适合：`../../video-studio/references/craft/h3-script-fit.md` |
| ⑤ 场记 | `../../drama-skills/skills/short-drama/references/continuity-breakdown.md`（六账）及同目录 `mechanism-preparation.md`（采纳、分工与继承约定） |
| ⑥ 分镜 | **开工前必读** `../../video-studio/references/craft/sequence-planning.md`（连续段规划）；独立短片另核 `short-film-scene-continuity`。需要新机制时回导演，检索读 `../../creative-dna-cards/SKILL.md`，查 `../../h3-prompt-writing/corpus/creative-dna-t8/INDEX.md`；链上引入点见同目录 `PRODUCTION-INTEGRATION.md` |
| ⑦ 图片词／⑪ 剪辑 | 读取 `../../drama-skills/skills/short-drama/references/mechanism-preparation.md` 的相应 owner 行 |
| ⑧ 视频提示词 | Ref2VA 读 `../../h3-prompt-writing/references/ref-en.txt`；T2VA/I2VA/FL2VA/L2VA 读 `../../h3-prompt-writing/references/base-en.txt`。接缝手法读 `../../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md`（先读 §0.1 第 0 步判型，再查手法）。写完正文对号翻 `../../h3-prompt-writing/references/failure-modes.md`（症状→根因→替代写法，含画外角色入场一拍概括、哭笑同形、否定句带偏、end-state 参考图落位）；渲染回来出现已知崩坏也查它，不按写作顺序通读。先继承导演已选条件与分镜证明时间窗；确需补查双人问答／情绪峰值／身份漂移／功能演示时读 `../../creative-dna-cards/SKILL.md` 按症状查 `../../h3-prompt-writing/corpus/creative-dna-t8/INDEX.md` |
| ⑨ 生产（转场卡/接缝中间段） | 要在 A、B 两镜之间插一段（首尾帧插值）时读 `../../h3-queue/references/transcard.md`，用 `../../h3-queue/scripts/transcard.py` 一条命令跑完取帧→过闸→FL2VA→两端 MAD→拼 A+C+B；别手搓 `--workflow`（草稿档 `pdd_lu` 的渲染器没有首尾帧参数）。判据与分流见 ⑧ 指向的 seam-transition §0.4 |
| ⑨ 生产 | 通道参数与档位以 `../../h3-queue/SKILL.md` 为准；短剧生产记录与授权读 `short-drama-produce`。**角色要学参考视频的动作（含音轨）**：读 `../../h3-queue/references/video-motion-drive.md`（不经 h3q 的 ComfyUI 直投通道，含图模板、runner、门禁、耗时与验收） |
| ⑩ 验收 | 逐镜证据分级读 `../../drama-skills/skills/short-drama/references/observation-ledger.md`。接缝测量全绿、创作者仍反馈"有硬切"时，判型读 `../../drama-skills/skills/short-drama-video-prompts/references/seam-transition.md` §0.1 第 0 步（画面缝／镜内相位断／情绪缝），不用指标反驳实看 |

## 旁路 · 复刻

| 要做什么 | 读哪份 |
|---|---|
| 拆原片为可回填的材料 | `../../drama-skills/skills/short-drama/references/video-remake.md`（视频复刻模式） |
| 建九份 `RR-*` 准备文档 | `../../video-shot-reverse/references/reverse-documents.md`（清单）、`../../video-shot-reverse/references/reverse-format.md`（逐镜字段） |
| 把九份文档回填成六文档 | `../../drama-skills/skills/short-drama/references/document-contract.md`（六文档契约） |
| 查某份文档被谁消费 | `../../video-shot-reverse/references/consumers.md`（merge 索引） |

## 两条补充

- **media-studio 预设自带的 `media-image-creation` / `media-video-creation`**：只接非短剧的通用创作，短剧仍回 short-drama 套件。`media-finishing-qa` 管裁切缩放、格式适配、字幕配音与导出交付。
- **`ask-studio` 已停用**（2026-10-22）：参考资料只作历史保留在 `.archive/ask-studio/`；现用技能需要的判据已内联，不从归档读规则。
