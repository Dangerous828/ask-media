# Assets And Asset-Image Prompt Rubric

## Occurrence and decision

- Does every extracted occurrence point to a source block?
- Is it production-relevant rather than every noun in the screenplay?
- Is the decision explicit: reuse, new identity, new variant, or unresolved?
- Were pronouns, aliases, groups, memories, portraits, and screen content handled
  without guessing?

## Identity versus variant

### Character / Look

Identity: stable face/body/hair anchors, distinguishing marks, voice/behavioral
identity. Look: wardrobe, makeup, hair arrangement, injury, dirt/wetness, disguise,
age/weathering state, validity range.

Fail when a costume change creates a new person or incompatible Looks mix in one
prompt without story reason.

Relationship labels may guide current blocking, gaze, and social presentation,
but they do not prove beauty, ugliness, body type, skin tone, or facial morality.
Fail when protagonist/antagonist status silently invents those identity traits;
creator-approved idealization or deliberate counter-casting remains a taste choice.

### Voice direction (optional, `AST-07`–`AST-12`)

Only reviewed when `视觉设定.md` records a voice direction. Timbre is carried by a
named reference recording, not by prose: identity is the reference plus the
creator's current pronunciation choices, and the text alongside it exists to
select or judge a voice, never to stand in for one.

Fail when:

- a project has no reference and a paragraph of adjectives is standing in for
  identity — the voice section must say `待选型` instead;
- a binding omits what it controls and what it must not, or lets the take's
  emotion, the recording space (reverb, mic distance) or background noise into
  identity (`AST-08`);
- a claim about what is audible in a reference has no creator description and no
  authorized listening observation, yet is written as established fact (`AST-09`);
- one proper noun appears with two accepted spellings anywhere in `视觉设定.md`
  (`AST-10`) — this one is structural and blocks;
- two characters designed together are bound to confusable references and no
  distinguishing trait names the nearest neighbour (`AST-11`);
- a selection criterion is an emotion word, carries no counter-example, or the
  list has grown past a handful (`AST-12`);
- reference audio bytes, a provider parameter, a model name, a task field or a
  URL appear in `视觉设定.md` or the delivery package.

### Location / View

Identity: architecture, layout, entrances, zones, anchors, materials, navigation.
View: camera-facing orientation/zone, time/weather/light state, visible anchors.

Fail when each camera angle becomes a new unrelated location or geography changes
silently between scene and plate.

Views of one Location sharing a time/weather state must also share key-light source,
warm/cool priority, contrast direction, and practical on/off state (`IMG-10`). Compare
the group side by side—each plate reading well alone is not evidence. Fail when an
unrecorded difference would read as two times or two rooms once the plates are
intercut; orientation-driven back/front lighting and occlusion shadows are expected
and need only a stated source.

### Prop / State

Identity: scale, shape, material, function, moving parts, marks, text policy.
State: owner/hand/location, open/closed, clean/damaged/wet/bloodied, contents,
validity.

Fail when a prop teleports, changes scale/material, or readable evidence is erased.

## Era

The era comes from source facts: devices, platforms, slang, stated years. Fail
when the era shown in `视觉设定.md`, `图片提示词.md` or `视频提示词.md` contradicts
them, or when a retro or aged descriptor (旧/老式/复古/褪色/斑驳, old, worn, dusty,
period, CRT) has neither a source basis nor an explicit creator choice (`AST-14`).
This is the visual layer of the source-fidelity check (`STY-07`): cite the source
fact and the conflicting line. A visual direction with
no era anchors, or entries that leave the era-specific form unstated, is a craft
note (`AST-15`).

## Prompt recipe review

All prompt types need purpose, exact binding, identifying facts, current variant,
composition, background, lighting, text policy, constraints, and exclusions. Then
apply type-specific criteria:

- Does each media reference declare one purpose, the facts it may copy,
  the facts it must not import, and a pixel/text admission decision?
- If a reference is composition-, scale-, or effect-only, did the prompt avoid
  borrowing its identity, wardrobe, content, text, count, or story state?

- **Character sheet:** one identity and coherent Look; useful reference views;
  neutral enough background/light to recognize anchors; no story action chain.
- **Location plate:** navigable geography, orientation, fixed anchors, material,
  palette, light direction, atmosphere; normally empty of cast.
- **Prop plate:** scale cue, shape, materials, wear, function/moving parts, current
  state, viewing angle, isolation, text policy.
- **Edit delta:** exact target and region, changes, preserve set, expected
  continuity impact; no unrelated regeneration.

## 纯文生图与外观复刻

区分写作者观察的来源图与生成器实际接收的图片。纯文生图时只读最终英文，核对必要的画法/成像、受光与明暗、空间投影、主体及接触关系能否独立读出，再回图找漏写或写反的部分；使用 `doc-still-prompt` 时读取它的 `../../../../doc-still-prompt/references/appearance-reconstruction.md`；未安装该协作技能时仍按本段核对实际来源与正文。类别词、品质词与完整表格不证明事实覆盖。

模式转换时重新对正文和实际输入清单；不能以删除refs完成垫图到文生图的转换。先判断输出的画风、光与构图是否符合本次目标，再核对局部元素；重要外观不符时明确需修订，不用道具齐全或人物漂亮补足。垫图结果不提供纯文生图通过证据；结构PASS、文字审读与实际出图分别报告。没有实际纯文生图或只测一次时，结论限制在对应证据，不推定模型能力上限。

## Prompt quality failures

- quality/style boilerplate appears before or instead of identity/geography/scale;
- prompt copies the whole 设定集 rather than the needed variant;
- character description mixes immutable anchors with accidental pose;
- location prose is rich but cannot orient entrances/zones;
- one character or prop is assigned to mutually exclusive positions, hands, or
  relationship lines in the same frozen instant;
- prop has no scale or text state;
- negative constraints contradict the required visible fact;
- edit request says “make better” without target/change/preserve;
- `图片提示词.md` contradicts the current identity, state or text policy in `视觉设定.md`;
- private URL, source ID, provider task field, or operator complaint leaks in.
- “use the whole reference” does not say what may or may not be copied.

Prompt prose elegance is secondary to recognition, reuse, continuity, and clear
control of the current operation.
