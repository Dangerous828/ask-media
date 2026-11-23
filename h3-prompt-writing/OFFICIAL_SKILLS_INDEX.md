# H3 提示词写作 · 本仓本地索引

本文件只索引本仓库 `h3-prompt-writing/` 内实际存在的资料。上游 [MiniMax-AI/MiniMax-H3](https://github.com/MiniMax-AI/MiniMax-H3) 官方 skill 索引为逐字节转载后已改写为本页；官方原文请以该仓库为准。

## 本仓资料

| 资料 | 用途 |
|---|---|
| [`SKILL.md`](SKILL.md) | H3 视频提示词正文写法（T2VA / I2VA / FL2VA / L2VA / Ref2VA），含中文说明与本项目已验收写法 |
| [`references/base-en.txt`](references/base-en.txt) | 官方基础文本/关键帧模式提示词指南（逐字节转载，222 行，SHA256 前 12 位 `2cfebc096a6e`） |
| [`references/ref-en.txt`](references/ref-en.txt) | 官方 Ref2VA 全参考模式提示词指南（逐字节转载，341 行，SHA256 前 12 位 `1e574f356716`） |
| [`references/case-notes.md`](references/case-notes.md) | 已验收案例与踩坑记录 |
| [`references/failure-modes.md`](references/failure-modes.md) | 症状 → 根因 → 替代写法 |
| [`references/market-reference-roles.md`](references/market-reference-roles.md) | 参考图角色定位 |
| [`references/ref-subject-picture.md`](references/ref-subject-picture.md) | 主体参考图约定 |
| [`corpus/README.md`](corpus/README.md) | 语料索引（含 creative-dna-t8 机制卡） |
| [`CHANGELOG.md`](CHANGELOG.md) | 本技能变更记录 |

## 说明

- 本仓只收录 H3 提示词写作与已吸收的语料；官方 8 个风格技能未随本仓发布，列表见[官方仓库 README](https://github.com/MiniMax-AI/MiniMax-H3)。
- 安装本仓版本：`npx skills add Dangerous828/ask-media`，或手动链接本目录；不要安装官方仓库版本，二者写法已分叉。
- 转载条款：MiniMax-H3 仓库无 LICENSE 文件、GitHub license 字段为空（2026-11-23 经 API 核实），未见覆盖仓库文档的明文条款；此处转载保留原文并署名来源，如上游后续发布文档许可条款，以之为准。
