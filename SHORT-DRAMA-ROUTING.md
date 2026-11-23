# 现用技能与短剧项目知识协作

现用技能继续完成其实际工作。short-drama套件提供项目事实、资产/镜头边界、连续性与制作阶段判据；知识关联不把当前写作、检查或队列执行转交出去。

不确定该用哪个技能或该从哪一步开始时，先读 [ask-media](ask-media/SKILL.md)；本文件用于已经确定要动短剧项目时，查套件外技能该读哪些套件内知识。

## 命中即读，读后继续本职

短剧/漫剧/动画叙事任务按下表读取相应阶段技能正文，不要求用户点名；已在本轮读取的内容直接复用。只有跨阶段、项目状态或初始化请求才读取 [short-drama总路由](drama-skills/skills/short-drama/SKILL.md)。看到名称不等于读过知识，也不需要为一个明确任务先通读整套。

本表只列**套件外**现用技能与套件知识的对接；短剧各阶段 owner（novel-analyze / develop / write / assets / direct / storyboard / image-prompts / video-prompts / produce / review / edit）的完整阶段表以 [ask-media 的阶段链](ask-media/SKILL.md) 为准。

| 当前实际使用技能 | 继续承担的工作 | 任务命中时必读的项目知识 |
|---|---|---|
| shortvideo-understand / video-previs | 复刻项目的原片文字稿、拉片、切点与代表帧；准备阶段从剧本新建白模 | 复刻读 [视频复刻模式](drama-skills/skills/short-drama/references/video-remake.md)，产出写进 `项目开发/原片拆解.md`，代表帧登记为画风基准；从剧本新建的白模用于写 `设定集/场记.md`，与场记账双向引用，**不作生成参考图** |
| video-shot-reverse | 只读逐镜反推、重建九份 `RR-*` 准备文档、观测转 caption 与 QC；不渲染白模、不改机位数值 | 复刻读 [视频复刻模式](drama-skills/skills/short-drama/references/video-remake.md)，九份文档落 `项目开发/原片还原/` 并按 [六文档契约](drama-skills/skills/short-drama/references/document-contract.md) 回填；清单见 [逆推准备文档体系](video-shot-reverse/references/reverse-documents.md)；导演／分镜／成片复审按 [逐镜证据台账](drama-skills/skills/short-drama/references/observation-ledger.md) 补依据分级与 QC，不改三个阶段的 owner 与验收六项；merge 索引见 [消费场景](video-shot-reverse/references/consumers.md) |
| short-drama-direct | 在正式分镜前写导演方案、观看与空间调度 | 读 [director](drama-skills/skills/short-drama-direct/SKILL.md) 的行动、知情、镜头计划和单场注意力工作包；定叙事必需的空间事实与关系，机位高度/焦段/景别数值留给场记账；交分镜 owner，不直接写提示词 |
| doc-still-prompt | 单帧成文方法、忠实译文与事实核对；当前写作者回填同一正式条目 | 资产条目由 [image-prompts](drama-skills/skills/short-drama-image-prompts/SKILL.md) 持有Look与制版；镜头条目由 [storyboard](drama-skills/skills/short-drama-storyboard/SKILL.md) 持有用途、瞬间与连续性。构图参考、起态、姿势证据与终态分别投影，不自动视为视频首帧 |
| anim3d-still-pitfalls | 定位3D翻车、提供修法，配合doc-still改词 | 身份/视角事实读 [assets](drama-skills/skills/short-drama-assets/SKILL.md)；制作可用性读 [review](drama-skills/skills/short-drama-review/SKILL.md) |
| storyboard-30s | 设计镜头、调度、节奏与分镜表 | 短剧分镜读 [storyboard](drama-skills/skills/short-drama-storyboard/SKILL.md)，沿用既有剧情和镜头边界 |
| h3-prompt-writing | 直接写完整H3正文、声音和参考标签 | 短剧动作/时长/交接读 [video-prompts](drama-skills/skills/short-drama-video-prompts/SKILL.md)，不要求先有另一份提示词稿 |
| creative-dna-cards | 文档准备即按需求查完整机制模板，给导演、场记及下游提供成立条件与失败条件 | 非阶段 owner；④ 导演采纳、③ 资产按需回补、⑤ 场记落实、⑥ 分镜证明、⑦⑧ 词继承、⑨⑩ 验收、⑪ 剪辑按 [准备约定](drama-skills/skills/short-drama/references/mechanism-preparation.md) 和 [PRODUCTION-INTEGRATION](h3-prompt-writing/corpus/creative-dna-t8/PRODUCTION-INTEGRATION.md) 交接；不擅改上游、不代替验收 |
| video-studio / shortvideo-pipeline | 工程检查、适配判断与测量（四件套、介质信号） | 生成物是否可用由 [review](drama-skills/skills/short-drama-review/SKILL.md) 的媒体验收裁决（先画风 `look_check.py`，后剧情）；本技能的测量作为证据，不单独放行 |
| h3-video-gate | 运行机械闸门、定位格式错误 | 需解释时序/动作时读 [video-prompts](drama-skills/skills/short-drama-video-prompts/SKILL.md)；机械PASS不等于语义与实图合格 |
| h3-queue | 核对真实输入，经h3q提交并追踪结果 | 短剧新生产读 [produce](drama-skills/skills/short-drama-produce/SKILL.md) 的本次授权、生成物再作参考规则与记录要求；实际支持的首帧/首尾帧/参考等模式查当前h3-queue与执行接口，路由表不缓存能力；档案使用所选H3方言 |

## 协作边界

- 用户明确请求本套件正式创作文档时，仍按套件原有阶段职责写作；当前技能需要的上游决定确实缺失或发生变化时，才回对应文档解决。明确的专项任务由当前技能完成，不循环派单。
- 同一正文回填现有条目，不叠加所有交付模板。doc-still需要单帧门禁快照时，从正式条目导出同一内容并核对，不另写平行版本。
- 新项目按六文档主链加入《导演.md》；旧项目只有补写导演层后才启用 director-v1，不批量伪造上游。创作者接受的阶段产物保持接受状态；新的实际冲突具体说明，技术观察不自动触发返工。
- 纯队列、显存、服务状态和下载既有产物不启动创作路由。读取知识不触发媒体生成、服务重启、渠道切换或额外审批；新生产仍以本次明确授权和真实可提交输入为前提。
- 本地图片/视频通常经 h3q 提交；用户授权的 AI-Canvas-tauri 工作流可直连 ComfyUI，例外及其限制见 `h3-queue/SKILL.md`。`ask-studio` 保持停用，不执行其旧路由和切镜流程。
- 复核结合本镜必要事实、实际发送英文、有序参考与真实产物，不只读作者自述；只检查当前请求范围。

中枢位于 `~/.skills/hub/`。通过软链接读取时先解析真实技能目录，再解析相对链接；也可直接读取 `~/.skills/hub/SHORT-DRAMA-ROUTING.md`。目标缺失时报告具体路径，不把名称当作已经加载。
