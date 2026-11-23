# 上游 PR #13 迁移预案

> [PR #13](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/13)（open，未合并）拟把 `SKILL.md`、`DETECT.md`、`references/`、`scripts/` 移进 `lieflat-less-ai-tone/` 子目录，让安装时只装 skill 本体、不带 README/RESEARCH/图片。**本地暂不跟进。**

## 为什么现在不动

中枢发布器 `publish_hub_skills.py` 的 `prepare()` 要求 `SKILL.md` 在技能目录根；13 个 Agent 端的软链也指向 `../SKILL.md`。提前重构会让打包校验直接失败，各端技能不可触发。等 PR 合并、确认上游定稿布局后再整体迁移。

## 合并后迁移清单

1. 从上游重新 clone 定稿版本，先与本地 2.1.0 的改动做 diff，确认哪些需要重放：
   - `detect.py`：`ACADEMIC_DEMOTE` / `ACADEMIC_PAPER_CHECKS` / `effective_levels()` / `--genre` / `fmt_report` 分档 / 5 脚本 UTF-8 补丁
   - `report.py`：`levels_of()` / `paper_check_section*` / 两处分级循环
   - `tests/test_academic_genre.py`：整目录带走
   - `academic-paper.md`、`research-pipeline.md`、`upstream-pr13.md`：整目录带走
   - `SKILL.md` frontmatter（version / description 里的两个指针）与「第一步」「第四步」命令
   - `CHANGELOG.md`、`../../AGENTS.md` 的文字创作表
2. 决定中枢里的目录形态：若上游子目录布局与 Hub 根目录要求冲突，保留平铺，在 metadata 里注明「上游已改子目录，本地为兼容 Hub 保持平铺」。
3. 重跑 `python3 tests/test_academic_genre.py`，13 项须全绿。
4. 跑 `publish_hub_skills.py --dry-run --only humanizer`，确认打包通过。
5. 跑 `sync-skills.sh`，确认 13 端软链与 Hub 入库都成功。
6. 版本号 bump 到 2.2.0，CHANGELOG 记迁移。

## 其他开放 PR

| PR | 内容 | 本地状态 |
|---|---|---|
| [#11](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/11) | 日文 README | 不需要 |
| [#12](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/12) | Windows GBK 输出修复 | **已本地先行**，见 CHANGELOG 2.1.0 |
| [#13](https://github.com/larashero3-dotcom/lieflat-less-ai-tone/pull/13) | 目录重构 | 本预案，等合并 |
