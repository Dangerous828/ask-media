# Frozen Keyframe Craft

## Purpose and ownership

A keyframe describes one instant that can exist within the accepted shot. The storyboard owns the shot's purpose, boundaries, viewing plan and frame records. `doc-still-prompt` supplies the single-frame writing method; its result updates the same SHOT/KF text, not a parallel prompt document.

Read accepted Character/Look, Location/View, Prop/State and the shot's camera/continuity facts. Do not change identity, action, pose, prop ownership or camera position to satisfy a prompt formula.

## Choose the frame role before drafting

| role | State to project | Use |
|---|---|---|
| `composition` | The declared instant best explaining this shot's composition and content | Core reference, normally 用途：构图; not automatically a first frame. |
| `start` | Exact 0s state | Actual first_frame must match this state. |
| `pose_proof` | Declared interior instant and read | Evidence of a crucial visible pose/contact; normally not first-frame production. |
| `end` | Exact shot-end state | Optional end reference when the chosen workflow actually consumes it. |

Every frame declares its time/read and responsibility. Camera phase and role are different: a composition reference may show a mid-move view, and a locked camera may still contain an irreversible action. Do not force all core references to the start or copy a result into an actual start frame.

Structured legacy `boundary_role`/`boundary_ref` records represent start/end boundary projections. Keep that distinction when reading them; do not label a composition reference as a start just to satisfy a legacy schema. When an adapter/checker cannot express the declared frame role, report the gap rather than silently changing its meaning.

## Ordered recipe

This is a drafting order, not a fixed prompt skeleton. Omit inapplicable detail while preserving necessary facts.

1. **Responsibility:** what this frame must let the audience understand, its role/read and instant.
2. **Visible identity/state:** exact accepted variants and visible anchors; a hand close-up does not expand to show a face.
3. **View:** inherit camera facts and record the [seven camera-language fields](keyframe-camera-language.md) outside the copyable text.
4. **Spatial relationship:** locate participants, important objects and relevant foreground/background zones using common anchors. Two-dimensional or simple frames need not fill three depth layers.
5. **Instant projection:** describe body/head direction, gaze, hands, held props and support/contact appropriate to this instant. Distinguish the visible owner of each body part and object.
6. **Performance:** where this frame has a performance responsibility, use a visible channel the shot can read. Animation may use shape/attitude; live action may use restrained physical cues. A neutral identity sample does not need invented drama.
7. **Light/material:** inherit this scene's accepted light/state and medium; add only frame-relevant visible response. No mandatory rim, SSS, wear, fixed ratio or face-brightest rule.
8. **Text:** project the accepted readable/symbolic/blank/postproduction treatment and carrier; exact words come from the asset/script owner.
9. **Risk notes:** put exclusions, reference responsibilities and production notes outside model prose. A negative list cannot create missing geometry or erase input pixels.

Write the model prose as one coherent image in `prompt_language`; translate faithfully where required. The metadata answers why and how it will be used; the prose answers what can be seen now.

## Boundary and instant tests

- `SHT-05`: each frame projects the accepted shot and its declared instant, with the required visual basis.
- `SHT-06`: all described facts can coexist at that instant; an ordered action chain is not one frame.
- `SHT-10`: start uses only start facts, end uses only end facts, and composition/pose_proof use the state at their declared time. None borrow incompatible facts from another instant.
- `SHT-17`: role, time and responsibility are explicit; end is a projection of the shot's end, not a second authority over it.

For example, start “right hand empty, looking at the other person” and end “right hand holding the bell rope, looking at the doorway” permit an end frame with the rope. The same image cannot silently become a start. A composition image at an interior time may show the accepted handoff phase, with its role/time stated.

## Optional start/end delivery

Only prepare an actual start/end pair when the accepted workflow needs it and the current execution profile supports it. Confirm whether other references can coexist with that mode from the current profile; this craft file does not cache backend capabilities.

The pair constrains both endpoints but does not prove the path, timing, dialogue or decisive action between them. Preserve the motion specification and assess whether its required action can be shown; do not automatically delete an action, split the shot or change camera merely because interpolation is uncertain. Return a concrete risk and implementation choice to the appropriate owner.

## Static and visibility test

Ask whether all model-prose facts could be captured together. Move ordered events, changing expressions, camera travel, dialogue progression and future changes to the motion/production layer. A held pose or visible motion trace can imply action within the accepted medium; it must still belong to this instant.

Every visible subject/place/prop requiring identity, Look or geography consistency appears in `视觉依据`, resolving to a real visual-setting entry. `IMG-...` locates an image-prompt item; it does not prove a real picture exists. Keep `REF-...`, `PLAN-...` and unresolved reference gaps distinct.

## Economy and continuity

Repeat only facts this actual prompt needs to be self-contained: visible identity, current Look, important spatial/contact relationships, light and text state. Cross-shot “same as before” may be a human note, but it cannot replace current visible facts in a standalone model input. Reuse exact accepted anchors without restating an entire hidden setting book.

A missed shot detail is repaired in the source entry. Do not create another coverage report, second identity authority or separate four-part prompt just to prove the task was checked. An optional snapshot must export the same final text.

## Completion

A reader can reconstruct the chosen instant, view, subjects and key relationships from the copyable text. Metadata and text agree; exact evidence comes from the final text, and the translation adds no facts. Unavailable media remains unverified: a text review cannot claim rendered success.
