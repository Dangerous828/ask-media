# 上游 PR #13 布局差异说明

> [PR #13](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/13)（上游仓库，未合并）拟把 `SKILL.md`、`DETECT.md`、`references/`、`scripts/` 移进 `lieflat-less-ai-tone/` 子目录，让安装时只装 skill 本体、不带 README/RESEARCH/图片。**本仓不跟进该目录重构。**

## 为什么本仓保持平铺

本仓是公开文档仓，技能以 `humanizer/` 目录平铺发布：`SKILL.md` 在目录根，引用 `./references/`、`./scripts/`、`./DETECT.md` 等相对路径。根级 [AGENTS.md](../../AGENTS.md) 的「文字创作与发布」路由表、`write-article` / `write-tweet` 的引用都指向 `humanizer/SKILL.md`。若把正文移进子目录，这些引用与仓库内相对路径都要改写，对读者与路由没有收益。

## 若上游合并后需要同步

只同步**规则正文与脚本的行为变化**，不照搬目录布局。按下列清单逐项 diff，确认哪些重放到本仓的平铺文件：

- `scripts/detect.py`：`ACADEMIC_DEMOTE` / `ACADEMIC_PAPER_CHECKS` / `effective_levels()` / `--genre` / `fmt_report` 分档 / UTF-8 输出补丁
- `scripts/report.py`：`levels_of()` / `paper_check_section*` / 两处分级循环
- `tests/test_academic_genre.py`：回归测试
- `references/academic-paper.md`、`references/research-pipeline.md`：本仓自有文档，以上游为参考，不整目录覆盖
- `SKILL.md` frontmatter（version / description 指针）与「第一步」「第四步」命令示例
- `CHANGELOG.md`、根级 `AGENTS.md` 的文字创作表

同步后重跑：

```bash
python3 tests/test_academic_genre.py   # 13 项须全绿
python3 scripts/check_references.py    # 从仓库根运行，断链应为 0
```

## 其他开放 PR

| PR | 内容 | 本仓状态 |
|---|---|---|
| [#11](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/11) | 日文 README | 不需要 |
| [#12](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/12) | Windows GBK 输出修复 | 已先行，见 CHANGELOG 2.1.0 |
| [#13](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/13) | 目录重构 | 不跟进，见上 |
