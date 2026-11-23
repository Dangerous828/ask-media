# Adapter Contract

## Job file

```json
{
  "schema_version": "1.0",
  "job_id": "EP001-MOTION001-video",
  "modality": "video",
  "adapter": "studio-video",
  "prompt": "the exact copyable prompt from MOTION-EP001-001",
  "source": "剧集/EP001/视频提示词.md",
  "source_entry": "MOTION-EP001-001",
  "reference_bindings": [
    {
      "slot_id": "REF-HERO",
      "order": 1,
      "path": "输入/approved-character-reference.png",
      "label": "女主定妆照",
      "role": "reference_image",
      "may_control": ["身份", "造型"],
      "must_not_control": ["构图", "动作"]
    }
  ],
  "references": ["输入/approved-character-reference.png"],
  "outputs": ["剧集/EP001/制作成果/video/SHOT-EP001-001.mp4"],
  "parameters": {"duration": 5, "ratio": "9:16", "prompt_language": "zh-CN"},
  "overwrite": false
}
```

- `modality`: `image`, `video`, `tts`, or `music`. `tts` is one bounded spoken
  utterance; `music` is a separately accepted timeline-level cue or song and
  must not be smuggled into every shot's video job.
- `source`: optional current project text/spec that owns the prompt.
- `source_entry`: for a creator-first job, the exact uppercase H2 ID inside a
  canonical `剧集|episodes/<EP>/` creator document, matched to that document:
  `图片提示词.md` takes `IMG-*` (image), `视频提示词.md` takes `MOTION-*` (video),
  and `分镜.md` takes the composite `SHOT-*#KF-*` (image). The KF ID must occur once
  in that shot's unique `### 画面证明计划`; rows in other tables do not register frames.
  Its role selects `冻结关键帧提示词` (composition), `起始帧提示词` (start), the
  matching `#### KF-*` body (pose_proof), or `收尾关键帧提示词` (end). Each of
  `composition`, `start`, and `end` may register at most one KF, so distinct frame
  IDs cannot silently share one body. A plain SHOT selector is rejected for new
  prepares, and a missing start body never falls back to composition. A new image/video job
  pointing to a canonical filename must provide the matching selector; an arbitrary
  Markdown file cannot impersonate a creator source. `prepare` requires `prompt`
  to exactly equal the selected copyable body after Markdown quote markers and
  the separate `Frame` / `镜头语言` metadata lines are removed.
- `reference_bindings`: zero to sixteen ordered semantic bindings. Every entry has
  exactly `slot_id`, contiguous `order`, project-relative `path`, Chinese `label`,
  non-empty `role`, and non-empty `may_control` / `must_not_control` lists. When
  `source_entry` is present, these fields must exactly match that entry's
  `参考` (IMG) or `输入参考图` (SHOT/MOTION) declaration (except `role`, which is
  production metadata). Allowed and prohibited scopes may not overlap.
  The creator declaration also carries a `用途` — what this picture decides in
  this shot, from the closed set in the storyboard skill. `role` is its
  production-side translation chosen per provider. For video, `用途：起始帧`
  requires `role:first_frame` and `用途：结束帧` requires `role:last_frame`;
  either endpoint role without the matching declared purpose also fails prepare.
  Other provider-specific roles remain explicit rather than inferred. This schema keeps
  `role` free-form because an external adapter names its own inputs, but the
  bundled video adapters read it as the provider's own role and accept only
  their published vocabulary: `first_frame`, `last_frame`, `reference_image`,
  `reference_video`, `reference_audio` for MiniMax, and the three `reference_*`
  values for Seedance. A video job carrying references without bindings fails
  closed there rather than having a role guessed for it.
  A `MOTION-*` entry's `参考音频` line binds after the pictures: its slots follow
  the `输入参考图` bindings in audio `顺序`, continuing the job's `order`, each with
  role `reference_audio` and `character` copied exactly from its `角色` field. Only those
  slots may use that role. Leaving a declared voice or its character out, or swapping
  characters, fails `prepare`. Adapters must preserve this character binding; bundled
  compilers derive the voice label from `character`, not the free-form asset `label`.
- `references`: zero to sixteen current project files actually sent to production.
  It may be omitted when `reference_bindings` is present, in which case the paths
  are derived in binding order. If both are present, they must match exactly.
- `outputs`: one to sixteen unique paths rooted at top-level `production/` or
  `剧集|episodes/<EP>/制作成果|production/`; extensions must match the modality.
  A nested directory merely named `production` does not grant write access to
  protected input or delivery trees.
- `parameters`: provider-neutral public settings only. Image/video jobs carry the resolved
  `prompt_language` so a bundled compiler writes its appended reference contract in the same
  language as the copyable prompt; this execution-only setting is not forwarded as a provider
  request field. Secret-like keys are rejected.
  Image jobs that produce a design asset must declare `asset_kind`:
  `character-card`, `scene-card`, `prop-card`, or `storyboard`. Those assets establish the
  look baseline and are not required to reference an existing one. A job that produces an
  `IMG-*` character/scene/prop/storyboard board without `asset_kind` is malformed; adding
  `no_look_baseline_ack` is not a substitute because it describes a Look development test,
  not a design asset. A missing baseline error must be repaired by declaring the asset kind
  or by registering the baseline, never by editing or bypassing `ref_gate`.
- `overwrite`: must be explicitly true to replace an existing result.

### Multi-shot (H3 multishot) parameters and bindings

`parameters.workflow: "multishot"` selects the multi-window container. It adds five
provider-neutral execution settings; every other field keeps its usual meaning:

| parameter | values | default | meaning |
|---|---|---|---|
| `workflow` | `ref2va` / `multishot` | `ref2va` | single-shot references vs. multi-window container |
| `frames_per_shot` | `17k+5` | `226` | per-window frames |
| `shot_count` | 1–8 | `2` | number of windows |
| `reference_image_size` | `match` / `max` | `match` | `match` scales references to the generation canvas; `max` keeps native pixels (≤2048) |
| `same_scene_continuous` | boolean | `false` | only meaningful when explicitly `true` and `workflow=multishot` |
| `scene_anchor_index` | 1-based integer | — | position in `reference_bindings` of the accepted scene/composition anchor; only with `same_scene_continuous=true` |

`reference_image_size` is multishot-only: declaring it on a `ref2va` job is rejected,
not silently ignored. `same_scene_continuous=true` is also rejected outside
`workflow=multishot`. Scene changes, hard cuts and jobs that say nothing keep the
previous behavior — the check is opt-in, never inferred.

A same-scene continuous job must carry an identity reference **and** a declared
geographic/composition anchor in the bindings, plus the explicit index:

```json
"parameters": {
  "workflow": "multishot",
  "frames_per_shot": 226,
  "shot_count": 2,
  "width": 768,
  "height": 448,
  "reference_image_size": "match",
  "same_scene_continuous": true,
  "scene_anchor_index": 2
},
"reference_bindings": [
  {
    "slot_id": "REF-HERO", "order": 1,
    "path": "剧集/EP001/输入/角色卡-女主.png", "label": "女主角色卡",
    "role": "reference_image",
    "may_control": ["身份", "造型"], "must_not_control": ["构图", "动作"]
  },
  {
    "slot_id": "REF-SCENE", "order": 2,
    "path": "剧集/EP001/输入/场景-餐厅卡座.png", "label": "餐厅卡座场景板",
    "role": "reference_image",
    "may_control": ["地理", "构图"], "must_not_control": ["身份"]
  }
]
```

The identity binding is any other `reference_image` whose `may_control` names
身份/人物/脸/造型 without denying it; the anchor binding at `scene_anchor_index`
must be a `reference_image` whose `may_control` names 场景/构图/地理 and whose
`must_not_control` does not deny it. Both pictures still pass the shared `ref_gate`
individually — this check adds the group-level requirement, it does not replace
per-picture acceptance.

`prepare` records internal digests of source/reference bytes and returns the exact confirmation phrase. Callers never
calculate those digests. A changed input requires prepare and confirmation again.
Jobs already prepared and stored before this contract remain readable under their
original fingerprint. New non-creator structured jobs remain valid without
`source_entry` and `reference_bindings`; they still receive the existing
path/digest/confirmation checks. A `music` job may continue to use the timeline
music section of canonical `视频提示词.md` without pretending that section is a
`MOTION-*` entry; other new image/video jobs using canonical creator paths must use
their matching selector.

## Quality revision (image/video retries)

When the same canonical `source` + `source_entry` + modality has a latest successful
run whose returned output carries a human `rejected` review bound to its exact bytes,
the next job for that entry must declare what actually changes:

```json
"parameters": {
  "duration": 5,
  "revision": {
    "previous_job_id": "EP001-MOTION001-video",
    "previous_run_id": "20261026T062006-b31551a3",
    "failure_key": "hand-ownership",
    "observation": "00:03握柄者错误，实际接触者与分镜不同。",
    "changes": {"prompt": "明确持物主体和其可见的发起动作。"},
    "preserve": ["原句、身份、时长及配置保持一致。"],
    "expected_result": "原定角色握柄，其他人的手不接触刀柄。",
    "strategy": "targeted"
  }
}
```

- `changes` keys must match the actual changed inputs (`prompt`, `references`,
  `parameters`) exactly; a no-op retry is rejected. Changing several inputs needs a
  `coupling_reason` of its own.
- `evidence_path` is filled by the tool with the exact current rejection report; the
  report and any redesign document join the input fingerprint and the private run
  snapshot, and `run` refuses before adapter start or confirmation spend if those
  bytes changed after `prepare`.
- A second consecutive failure under the same `failure_key` requires
  `"strategy": "redesign"` plus `"redesign_source": {"path", "section", "decision"}`
  pointing at a real section of 导演.md / 分镜.md / 视觉设定.md / 图片提示词.md.
- Technical failures (provider errors, timeouts) and `collect` retrievals are not
  quality retries and never require a revision. Renaming the job does not reset the
  source entry, and each run's executed job snapshot is kept under
  `.short-drama/production/executions/<job-key>/<run-id>.json` so a re-prepared job
  name cannot erase the predecessor evidence.
- The tool verifies structure and binding only; observing the defect, attributing it,
  and choosing a stable `failure_key` remain the reviewing human's job.

## Adapter config

Keep this file outside the project:

```json
{
  "adapters": {
    "studio-image": {
      "command": ["python3", "/opt/studio/image_adapter.py"],
      "timeout_seconds": 600
    }
  }
}
```

`command` is an argv array, never a shell string. Timeout is 1–3600 seconds. Do not put credentials in this file;
let the adapter read its environment or operating-system credential store.

A profile may add `"reference_roles": [...]`, the roles its configured model accepts. When present,
`run` refuses any binding whose role is not listed. A `reference_audio` binding always needs it:
a model without an audio input can drop the voice without an error. Either way `run` stops before
the confirmation is spent or the adapter starts. List `reference_audio` only for a model you know
accepts reference audio.

## Capability sources

Use the provider's current API reference for roles, limits and supported combinations.
A relay can expose a different subset, reject inputs itself or transform requests.
Record the tested execution path and distinguish its observations from the native API contract.

## Adapter stdin

The adapter receives one UTF-8 JSON document as raw stdin bytes. Read the
binary stream (for example `json.load(sys.stdin.buffer)`) rather than relying
on the machine locale. The document contains the confirmed job plus:

- `run_id`: unique attempt ID;
- `project_root`: local absolute path to a private, run-scoped snapshot containing
  the exact confirmed `source` and `references`. It is not the live creator
  project and is deleted after the attempt.
- `output_root`: empty private, run-scoped staging directory owned by the
  production tool. Every adapter output source must be a direct regular-file
  child of this directory. The whole directory is deleted after success or
  failure.
- `handle_path`: absolute path where the adapter records the provider's task id
  **as soon as it has one, before it starts polling** — write
  `{"provider_job_id": "<id>"}`, atomically. Unlike `output_root` this path
  survives the attempt.
- `collect_provider_job_id`: present only on a collect call. When it is set the
  adapter must **not submit anything**; it polls and downloads that existing
  task and returns its outputs as usual.

## Recovering a submitted task

Record the provider task ID before polling so an interrupted task can be collected without resubmission.
A local handle-write failure is non-fatal after submission. The tool copies the handle into the attempt
record on success or failure; `audit` reports unfinished tasks as `orphaned_provider_job` with
`action: collect_before_retry`.

`production_tool.py collect` retrieves the existing task without new submission or confirmation.

It may translate provider-neutral parameters into its chosen SDK/API. Optional
provider adapters under `scripts/` document and implement known translations;
the project job remains provider-neutral, and adapter selection, model access,
polling and credentials stay in the external runtime configuration.

The confirmed document includes `source_entry` and `reference_bindings`. Bundled
image/video compilers append an ordered reference contract to the provider prompt so the Chinese
label, role, allowed controls, and prohibited controls survive the handoff. Its prose follows
`parameters.prompt_language`; model-native compilers also use that model's actual reference tokens,
such as Seedance `@图片1` or H3 `<Picture 1>`, rather than adding a second generic numbering scheme.
External adapters must preserve equivalent semantics
or reject the job; silently reducing the input to an unlabelled file list is invalid.

## Adapter stdout

On success, write one bounded UTF-8 JSON object to stdout. Portable adapters
should ASCII-escape JSON strings so Windows locale settings cannot corrupt
project paths:

```json
{
  "outputs": [
    {
      "target": "剧集/EP001/制作成果/images/SHOT001.png",
      "source": "/temporary/adapter/result.png"
    }
  ],
  "provider_job_id": "optional-public-id"
}
```

Targets must appear in exactly the confirmed order. Sources must be direct
regular-file children of `output_root`, not symlinks. The tool opens each source
without following links, copies the pinned bytes into the project, records
size/media type/checksum, and removes staging. It never stores adapter
stdout/stderr or environment values.

On a provider failure, an adapter may write only this whitelisted evidence to stdout:

```json
{
  "error": {
    "provider": "studio-image",
    "category": "rate_limit",
    "code": "rate_limit_exceeded",
    "http_status": 429,
    "request_id": "request_safe_123",
    "retryable": true
  }
}
```

Never include provider messages, response bodies, prompts, paths or credentials.
The production run record keeps only validated fields; malformed failure output
is replaced with a generic adapter exit code.

A nonzero exit, timeout, malformed response or mismatched output marks the run failed. Because the adapter may have
submitted paid work before failing locally, confirmation is consumed as soon as execution starts; retry only after a
new creator confirmation. A job with an unresolved `running` attempt cannot be prepared, confirmed, or run again;
wait for its terminal record or investigate the interrupted attempt first.

## Operational reconciliation

`production_tool.py audit <project>` reads only local production metadata and the
current output bytes. It reports terminal failures, retryable failures, recovered
jobs, unresolved running attempts, repeated content fingerprints, and missing or
changed outputs. Terminal state, recovery, and repeated output claims are ordered
by validated completion time rather than start time. For paths written more than
once, the latest completed successful claim is authoritative for this operational
check. Only attempts bound to the current stored job fingerprint can claim its
current outputs; older fingerprints remain visible as `superseded` attempt history.
A successful record must declare exactly the current job's output set and media
types before any output claim is trusted. Jobs, confirmations, run records, and the
production lock use pinned no-follow directories where directory FDs are available,
and reparse/identity checks on the portable fallback. A linked parent chain fails
closed instead of redirecting state outside the project.

The audit deliberately returns `quality_verdict: not_assessed`. A provider success,
retry recovery, file presence, size, or checksum proves execution/custody only; it
does not prove identity, performance, continuity, lip-sync, mix, edit, or audience
quality. Those claims require an authorized observation and a separate review.
