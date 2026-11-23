# Storyboard, Keyframe, And Motion Rubric

## 目录

- [Coverage](#coverage-and-meaning)
- [Shot](#shot-purpose-and-geography)
- [Keyframe](#frozen-keyframe)
- [Motion](#motion)
- [Continuity](#cross-shot-continuity)
- [Rhythm profile](#rhythm-profile-shots)
- [Findings](#common-findings)
- [Production risks and authorized observations](#production-risk-and-authorized-observation-checklist-rev-08)

## Coverage and meaning

- Does every production-relevant block have a disposition?
- Are omissions/repeats explained?
- Does each shot preserve the source action, dialogue, information, and reaction?
- Has downstream work invented or deleted a story fact?

## Director plan and audience reads

- Does each filmed scene have a director entry with a concrete goal/opposition, visible action or information change,
  consequence receiver, audience-knowledge strategy, viewing plan and spatial/sound facts? A scene omitted for a reason
  must not silently acquire a shot.
- Does every formal SHOT resolve to the director's shot plan, or record its intentional split/merge and preserve source facts?
- Do reads explain what the audience understands, in what order and with what attention lead and landing time? They must not
  be a list of action verbs or a fixed three-second split. Cause and consequential reaction must not compete for the same read.
- Does the camera actually expose its claimed reaction? A reverse or over-shoulder frame cannot assert an unseen face is its endpoint.
- Check absolute inventions, changed contact/ownership, spatial state after movement, and contradictions inside a frame. Mechanical
  table validity cannot clear these; review the actual wording against the screenplay.
- Does the finished shot let an independent reviewer reconstruct the director's intent and the previous/next state without reading
  the design process? If not, repair the earliest missing decision rather than blaming model attention.

## Shot purpose and geography

- For a high-value scene with an accepted coverage audition: did the approaches
  genuinely differ — in knowledge timing, audience alignment, performance space,
  strongest image, landing, losses, or production fit?
- Does the formal plan bind the approach the creator selected, rather than the first draft?
- When a scene visual plan was used: do its start/end audience positions, spatial
  pressure, camera rhythm, reaction landing, and sound movement carry **one** dramatic turn?
- Does that plan stay clear of owning shot boundaries? (Ordinary scenes need no plan
  merely to satisfy a form.)
- What changes for audience or character by the shot end?
- Why is this a new shot?
- Do framing and camera behavior serve attention, alignment, pressure, reveal, or
  rhythm rather than decorate the prose?
- Does each shot's `运镜` line state a behavior and a reason chosen from the shot's
  purpose (`SHT-04`)? A stated lock-off with its reason passes. An episode locked on
  nearly every shot while its peak gets no movement is a finding; so is a missing line,
  which leaves the choice to the video-prompt stage; a bare 「运镜：固定」 with no reason
  is also a finding.
- Are Location/View, axis, screen direction, eyelines, entrances, positions,
  hands, and props coherent?
- Are exact asset variants bound?
- Does the shot expose every fact it must carry while protecting
  facts the source withholds until a later action or cut?
- Do crop, occlusion, focus, back view, and offscreen space serve that information
  permission rather than accidentally reveal or conceal it?

## Rhythm profile: shots

Under the `REV-12` conditions in the [story rubric](rubric-story-script.md#rhythm-profile-rev-12),
measure two storyboard fields: the average shot length per scene (scene duration divided
by its shot count) against `target_avg_shot_seconds`, and the share of close-range shots
across the episode, as the profile field defines them, against `close_shot_share_min`. The average is a
scene-level target; one long or short shot is not a finding. Also report durations folded
from screenplay word counts instead of the scene's sound timeline (`SHT-28`).

## Frozen keyframe

- Can all described facts exist in one still instant?
- Does the frame plan declare `start` / `pose_proof` / `end`, a matching read, exact time and proof responsibility?
  `start` is at 0, `end` at shot end, and `pose_proof` is inside the shot rather than a prettier first frame.
- Does a declared key pose have corresponding `### 关键姿势提示词` and `#### KF-...`, and is it excluded from default start-frame production?
- Does the frozen keyframe project only its declared boundary, without hidden future highlights, props, expressions or reflections?
- Are focal hierarchy, composition, camera/lens, geography, pose/gaze/hands/prop,
  expression, and light legible?
- Does the keyframe prose begin with the seven-slot camera-language anchor — shot size,
  horizontal angle and axis side (or “no axis”), camera height, lens intent, composition
  layers, focus plane, frame phase — without overriding the shot's accepted framing or
  axis? See `$short-drama-storyboard` → `../../short-drama-storyboard/references/keyframe-camera-language.md`.
- Does it avoid ordered actions, performance arcs, camera moves, or transforming
  environments?
- Read the finished keyframe text, not the shot's intent: is every visible character,
  place, and prop whose identity, Look, or geography must stay recognizable listed in
  this shot's `视觉依据` (`SHT-22`)? A second body that entered the composition while the
  frame was being written is the usual miss.
- Does each declared 控制 scope stay inside what this frame can carry, and is nothing
  bound merely because it was bound in the previous shot (`SHT-24`)?
- When real reference images are bound, does every `REF-...` slot declare a 用途, so the
  shot says which start frame and which identity/geography/prop pictures it sends
  (`SHT-25`, `VID-24`)?
- Is anything the frames need kept consistent across shots — a carried prop, a garment —
  absent from `视觉设定.md` entirely, so it can appear in no shot's basis at all? The
  mechanical check cannot see this: an entry that does not exist cannot be reported missing.

## Motion

- Does it start from the accepted frame/boundary?
- Are subject actions ordered and small enough to preserve intended performance?
- Does performance change express the story move rather than stack synonyms?
- **Clean handoff body (`SCR-24` at the video layer)**: does the prompt text the
  generation endpoint consumes contain zero working aids — numbering, timing
  estimates, beat tables, checkpoint/self-check lists, template labels,
  `[连续性]`-style annotations, asset internal IDs? Anything the video model
  would render as text or treat as instructions must be stripped before
  submission; a prompt that needs cleaning before use is itself the finding.
  (Basis: 110/120 blind-review rounds in the awesome-short-drama arena flagged
  exactly this class of metadata in delivered scripts.)
- In multi-character motion: do the actors who actually change have distinct,
  readable triggers, choices, leaks, or landings — as this shot needs, not one
  identical arc per actor?
- Is attention handed off only where it truly transfers, rather than for
  synchronized reaction?
- Does any text-readiness claim cite the current creator-visible inputs and a real blocking gap?
- Does it avoid any claim about generated media quality or create a second readiness truth?
- Is camera behavior coherent and motivated?
- Are environment motion, dialogue, SFX, and audio included only when relevant?
- Does the described end match the storyboard's written end state without rewriting the next shot?
- When a reference frame carries appearance/composition, does motion prose avoid
  dumping the full visual 设定集?
- Does every claim about text-bearing reference pixels cite a creator/reference-owner
  description or an authorized input-reference observation? Without that evidence,
  is admission still `unverified` instead of pretending a negative prompt solved it?
- For any selective transform, are the accepted trigger, exact target scope,
  end geometry/state, and preserve set explicit? Do non-target people, props,
  text surfaces, and spatial anchors keep their required position, count, and state?
- Does each media reference state its exact purpose, what may be copied, and what
  must not be copied, rather than treating all visible pixels as authority?

For a copyable body (`VID-22`, `VID-23`), check that actions and sound match the
source and that the timeline accounts for the intended ambience or silence.
A summary must not introduce a layer absent from the shot. H3's
`non_diegetic_music: N/A` is a valid empty music layer.

Report a concrete contradiction, omission or ambiguity. A negative clause is
not a defect by itself; do not impose a clause count or assume that negation
causes the model to generate the excluded content. Keep model-specific
observations scoped to their tested model and execution path.

For a pickup or alternate, ask these separately:

- Does the pickup/alternate name its master by visible `MOTION-...` heading?
- Is every source obligation assigned to the master, this version, another named version or a requested storyboard revision?
- Are the changed items and the items that must remain unchanged explicit?
- Is replacement only requested here? The review Markdown decides whether the master remains primary or the alternate replaces it.

For music, ask these separately (`VID-14`):

- Is intent written as a relative entry/exit/duck against neighbouring shots,
  rather than an independent cue per shot?
- Do adjacent annotations actually join?
- Does the text ask for a per-shot music bed against an accepted timeline-layer plan?
- Whether a rendered clip carries a baked-in track is **not decidable here**. Cite it
  only from an authorized text observation record; otherwise keep it `unverified`
  and never infer a mix result from prose.

Explicit timing that does not sum exactly to its shot's accepted duration—over or
under—is a structural error. Untimed overload is a
reviewed feasibility question: cite which action/performance/story beat would be
lost, not a universal verbs-per-second formula.

Container arithmetic is a separate structural check (`VID-13`). Count the accepted
shots a delivery container carries, then confirm its duration equals the sum of
their accepted durations. For a multi-shot container, confirm the members are
contiguous in source order, share one geography/asset binding chain, do not cross a
scene boundary, and each remains independently reviewable. A space or subject jump
belongs on a member boundary; the same jump inside a member's timed segment is a
hidden cut. Report an arithmetic mismatch and a hidden cut as two findings, not one.

- Is the axis recorded as two named anchors, a stated working side, and a per-character
  screen position — rather than a placeholder?
- In a shot-reverse-shot pair, are the two screen directions complementary?
- Bare left/right always means **screen** left/right. Where a subject's own side is
  meant, does the text name the subject?

## Cross-shot continuity

Trace Look, injury, dirt/wetness, emotion/knowledge, position/facing/gaze, hands,
held prop, prop owner/state, location/time/weather/light, axis, and screen
direction. Distinguish unexplained contradiction from declared montage,
ellipsis, dream, or deliberate disorientation.

## Common findings

- beautiful shot with no dramatic purpose;
- dialogue covered but consequential reaction absent;
- anonymous asset or wrong variant;
- cross-location/time action hidden in one ordinary shot;
- keyframe contains “first/then/finally”;
- keyframe has no seven-slot camera-language anchor, or only says “中景/特写” without angle, height, lens, composition, focus, or frame phase;
- locked camera also pans or pushes in the same interval;
- motion invents a grab, injury, transfer, relationship change, or line;
- a selective transform removes, copies, or reshapes a non-target person, prop,
  text surface, or spatial anchor because its preserve set was unspecified;
- end pose/prop state disagrees with next start;
- every emotional beat uses the same close-up/push template;
- provider batching is mistaken for editorial shot structure.
- a narrowed pickup silently replaces the master and drops dialogue, reaction,
  reveal, end-state, or creator-directive obligations.

## Production-risk and authorized-observation checklist (REV-08)

运行环境能读取媒体时，生成物按 SKILL「媒体验收」实读：先过画风层（REV-15），再看本表各项。
读不到媒体时，先把下列项目当作文字风险，引用准确的 prompt/spec 说明为什么会造成
执行歧义或违背已接受约束；只有创作者提供了授权的文字观察记录时，才能称为已观察缺陷，
并把该记录作为外部证据引用。没有观察记录时保持结果未知，不从任务成功、结果地址或提示词
存在推断成片质量。

需要项目校准时，先区分输入参考与生成结果。后一种观察只有在绑定准确的提示词/镜头标题、参考顺序、
制作形态/配置、观察方法和限制时才可引用；finding 同时给出最小修改项与保持项，并保持结论只在该项目
和版本条件下有效。

短剧生产中需要防范的文字风险或获授权观察包括：

- on-screen text or subtitle residue despite a declared no-text constraint;
- a text-bearing reference admitted under no-text or exact-readable policy
  without an allowed surface or a crop, clean, mask, or replace decision;
- background music implied where the audio boundary allows sound effects only;
- wardrobe or look drift against the bound reference (re-describing clothes the
  reference already fixes invites drift — flag redundant appearance prose);
- 180° axis violation or eyeline mismatch across consecutive shots without a
  declared transition;
- lip-sync mismatch: dialogue bound to the wrong character, inner monologue
  written as mouthed speech, or extra lines the source dialogue never contained;
- explicit segment timings that do not sum exactly to the shot duration, in either direction;
- emotion-intensity mismatch between stated level and described performance
  (a declared 9/10 rage performed as mild irritation, or the reverse).
