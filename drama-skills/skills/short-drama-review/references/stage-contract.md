# 审查阶段契约

本阶段只拥有审查结论与修订要求，不改写 owner 来源。需要落盘时使用创作者可读 Markdown，引用当前
文件名、标题 ID、行号或短引文；不另建一套剧情事实或创作接受状态。

文本审查可以由独立 reviewer 或明确标注的自检完成。逐镜媒体必须另起未参与生产的全新 reviewer，
整片再换另一名全新 reviewer；reviewer 字段只作归属，独立性来自实际流程隔离而非名称或防伪权限。
媒体可读时必须实读（见 SKILL「媒体验收」）；不可读或无法核实的项写 `UNVERIFIED`，不得批准；
外部生产仍需要自己的显式确认。`审查/look/<项目相对路径>.look.json` 是媒体测量的技术证据与
复核历史，供 produce/edit 机械判断是否允许复用或剪辑；它不是剧情接受状态，剧情结论仍写在审查 Markdown 里。
`project_tool` 的 artifact accepted/rejected 记录创作者对文档的决定，与媒体验收各管一层，不互相替代。

## 本阶段规则

### `REV`

| ID | Class | Knowledge |
|---|---|---|
| REV-01 | structural_invariant | Run mechanical checks before spending creative review attention. |
| REV-02 | structural_invariant | A finding names a visible file and heading/shot/prompt ID, and includes evidence, impact, required fix, owner, severity and status. |
| REV-03 | reviewed_invariant | Semantic invention cites the source fact and conflicting downstream fact. |
| REV-04 | craft_default | Prefer a reviewer who did not author the current targets; disclose self-review, and keep reviewer findings separate from owner edits. |
| REV-05 | craft_default | Diagnose repeated structure or generic language with location and impact; do not label output merely "AI-ish". |
| REV-06 | taste_option | Alternatives remain notes unless they violate an accepted creator constraint. |
| REV-07 | structural_invariant | An end-to-end drafting request cannot impersonate creator acceptance; preview chains remain provisional and undeliverable. |
| REV-08 | craft_default | When authorized text notes report production defects, trace text/subtitle residue, music-boundary violations, wardrobe drift, axis breaks, or lip-sync mismatch to the exact prompt/spec text and keep unobserved outcomes unknown. |
| REV-09 | reviewed_invariant | After prompt revision or repackaging, recheck source coverage and every applicable accepted directive; correct asset bindings alone do not prove compliance. |
| REV-10 | reviewed_invariant | A project-calibration finding distinguishes input-reference from generated-result observation, binds the exact project, the prompt/spec records it observed, stable reference slots, production configuration, method and limits, and—when its disposition calls for a change (see REV-11)—proposes the smallest owner-routed one with a preserve set; it does not generalize across projects or infer quality from task state. |
| REV-11 | reviewed_invariant | A calibration finding carries `disposition` (keep, post_production, targeted_edit, resubmit, rewrite) and `disposition_rationale` before any revision text, justified by whether the defect is text-controllable and whether it has already recurred. Dispositions that call for no change leave `required_change` empty rather than inventing one. Resubmitting identical text and appending quality adjectives are not repairs; a recurring defect routes to a structural change instead. Findings outside project calibration use `not_applicable`. |
| REV-12 | craft_default | When the project's rhythm profile has status `accepted`, review checks the episode against it by arithmetic on the accepted values only and reports a deviation as a non-blocking finding citing field, accepted value, measured value, and location; the creator may keep the episode with a stated reason. A missing or proposed profile leaves the check inactive, and no finding compares against another project's or a suite-wide number. |
| REV-13 | craft_default | Beyond the whole-episode read, three local passes each read one part only: an opening-hook pass on the first segment, which also reads the first beat alone as the opening frame, an ending-suspense pass on the last segment, and a reversal-density pass on the middle. |
| REV-14 | craft_default | A revision request is a patch at a cited location with a preserve set, never a whole-episode rewrite; a strong hook, payoff line, or comic beat removed by polishing is logged with its prior location and quote so the owner can restore it. |
| REV-15 | structural_invariant | Generated media is accepted look-first: before technical, continuity, performance or dialogue judgments, it is measured by `look_check.py` against the project's registered look baseline and a reviewer records what the side-by-side sheet actually shows. A mechanical FAIL is never overridden; a PASS without a recorded visual review is still pending; prop counts, action order or ASR passing never compensate for a look regression. No registered baseline makes the media verdict PROVISIONAL. |
| REV-16 | structural_invariant | Only media approved for reuse may become the next generation's reference. A rejected, pending or look-failing output is never extracted for state frames, never bound as a reference, and never handed to edit; its downstream successors inherit its rejection and are re-reviewed when it is rejected later. |
| REV-17 | reviewed_invariant | A repair is routed in this order: rewrite the prompt text; rebind an original native asset or an already-approved output; simplify the shot through the storyboard or director owner. Hand-compositing, pasting, vector redraws or local pixel edits of a reference to force layout are not repairs. After every repair the look layer is re-run (regression), and two consecutive look-passing repairs of the same shot that still miss the same story fact stop the loop: the shot returns to storyboard/director to simplify or move the fact to edit/post, not to a third stronger constraint. |
| REV-18 | structural_invariant | Each shot is reviewed in a fresh context uninvolved in production, using the real media, references, script, storyboard and prompt, with PASS/FAIL/UNVERIFIED and evidence for look/technical, identity/costume, hands/limbs/contact, action/spatial continuity, exact dialogue/lip sync and audio/voice. A fresh, different reviewer repeats this for the final cut. Production measures but never approves; edit permission never implies reference permission, and reference requires story passage. ASR is locator-only and cannot prove exact dialogue, lip sync or voice. Reviewer labels are attribution, not proof of independence. |

规则分级由高到低：`structural_invariant`（结构缺陷，阻断）、
`reviewed_invariant`（需证据判断）、`craft_default`（常用做法，可覆盖）、
`taste_option`（创作者选择，不作缺陷）。创作者已接受的事实优先于本表。

## 验收报告的两份文件（`review_check.py` 的输入）

`review_check.py --findings <findings.jsonl> --verdict <verdict.jsonl>` 校验验收结论。
两份都是 **JSONL**（每行一个 JSON 对象），不是 JSON 数组——写成数组会报 `invalid JSON`。
每个字段都是必填，缺一个只报一条，所以要一次写全。

### `findings.jsonl`（一条发现一行）

| 字段 | 取值 |
|---|---|
| `finding_id` | 唯一，如 `F-001` |
| `diagnostic_code` | 命中的规则号或检查器项，如 `REV-15`、`video_check.brake` |
| `scope` | 这一条管什么，如 `SHOT-EP001-07` |
| `classification` | 分类，如 `look` / `technical` |
| `severity` | `fatal` / `error` / `warning` / `note` |
| `status` | `open` / `closed` |
| `enforcer` | 谁判的，如 `look_check.py` |
| `evidence` | 判据文本 |
| `evidence_refs` | 引用对象列表，每项 `{owner, artifact, field}`；**不是字符串列表** |
| `target_ref` | 这条针对的产物，同样是 `{owner, artifact, field}` |
| `impact` | 影响 |
| `disposition` | `keep` / `post_production` / `targeted_edit` / `resubmit` / `rewrite` / `not_applicable` |
| `disposition_rationale` | 为什么这样处置 |
| `owner_skill` | 归属技能 |
| `required_change` | 要改什么；`status: open` 且 `severity` 是 `fatal`/`error` 时不能为空 |

### `verdict.jsonl`（整份结论一行）

| 字段 | 取值 |
|---|---|
| `review_id` | 唯一 |
| `reviewer` | 谁验的（名字只是归属，不证明独立） |
| `review_method` | `uninvolved_reviewer` / `self_check` |
| `verdict` | `APPROVE` / `APPROVE_WITH_NOTES` / `REVISE` / `PROVISIONAL` |
| `scope` | 文本列表，如 `["SHOT-EP001-07"]` |
| `summary` | 一句话结论 |
| `findings` | finding_id 列表 |
| `findings_ref` | 指向 findings 文件，`{owner, artifact, field}` |
| `reviewed_artifacts` | 看过的产物，对象列表，**不是字符串列表** |
| `blocking_findings` | 必须等于 open 的 fatal/error findings |
| `open_blocker_count` | 必须等于 `blocking_findings` 的长度 |

引用对象统一是 `{owner, artifact, field}` 三段；`artifact` 是项目相对路径。写成裸字符串会报
`REF_IS_NOT_AN_OBJECT`，只写 owner+artifact 会报 `record_id or field is required`。

## 画风审批的三步（`look_check.py measure → review → approve`）

剪辑只认 `approve --use edit` 落下的批准记录；少一步都拦。顺序固定，参数互相依赖：

1. **`measure <project> --media <绝对路径>`** —— 相对路径按当前工作目录解析，写项目相对路径会报「文件不存在」。
   媒体要与已登记的画风基准比，而基准只从**二级标题 `## 画风基准`** 读（`startswith("## 画风基准")`）；
   写成 `### 画风基准` 会被判「没有可用画风基准」。每条基准写
   `- LOOK-…：<项目相对路径>《<中文名>》` 与 `- 认可依据：创作者 <日期> …`。
   首次测量要带 `--comparison comparable --comparison-note "<为什么可比>"`，否则 `review` 会拒
   「可比性尚未确认」。
2. **`review`** —— 六项逐项判定（`look_technical`、`identity_costume`、`hand_limb_contact`、
   `action_spatial_continuity`、`dialogue_lip_sync`、`audio_voice`），每项配一条
   `--evidence <检查名>=<观察记录>`，观察记录**至少 8 个字符**且必须是实际看到的，写「无」不行。
   还要给 `--script`/`--storyboard`/`--prompt`/`--reference` 的路径。
3. **`approve --use edit`** —— 六项必须**全部 PASS**（`FAIL` 与 `UNVERIFIED` 都不能批准）；
   外部生成的媒体还要加 `--creator-ack`，`--creator-ack` 是创作者本人实看后的批准，
   不是执行者可以代填的。

无对白的动态镜头有一个口径要认：`review` 禁止对动态媒体记 `N/A`（只允许静帧），
而 `approve` 又要求全 PASS，所以「这一项不适用」没有可写的值。实际做法是把该项记 `PASS`
（含义是「该维度未发现缺陷」），并在 evidence 里写清依据——例如全片转写只返回静音幻听句、
平均音量属环境底噪，因此无口型错位可言。把依据写透，不要把 PASS 当默认值。
