# DV手持vlog-首尔夏夜-001

- 验证状态：**外部复测通过**（MiniMax H3 Max 768p，2026-09-07，score 75.7，stability 76/100）；本地 h3q 未测
- 来源：作者 [@AIwithkhan](https://x.com/AIwithkhan/status/2092971211169100048)，原帖 2026-08-27；收录于 [awesome-seedance](https://github.com/LearnPrompt/awesome-seedance)（策展 CC BY 4.0，此条目署名引用）；复测视频见 [goodcase.ai retest](https://goodcase.ai/cases/vlog-c8171f712492)
- 目标通道：原帖为 Seedance 2.5；复测在 MiniMax H3 Max 云端

## 完整原文（逐字保留）

```text
Create a 30-second, 1080p ultra-realistic personal home-video showing an ordinary summer evening in the life of a young Korean woman. No reference image. MAIN SUBJECT Young Korean woman in her early 20s, naturally pretty, realistic skin texture, minimal makeup, relaxed and approachable personality. Long black hair loosely tied into a messy side ponytail with a few loose strands around her face. Wearing a fitted pastel-blue short top, loose cream pajama-style pants, black sneakers and a simple silver necklace. Maintain the same face, hairstyle, clothing, body proportions and overall appearance throughout the entire video. SETTING A quiet older Seoul residential neighborhood during a warm summer evening. Narrow concrete lanes, small houses, potted plants, bicycles, old walls, utility poles, overhead wires, a tiny neighborhood bakery, a public water tap and large leafy trees casting shadows across the street. Everything should feel lived-in, ordinary and peaceful. CAMERA / VISUAL AESTHETIC Raw personal footage casually recorded by a friend on an early-2000s consumer DV camcorder. Strong handheld shake, imperfect framing, autofocus hunting, exposure shifts, occasional motion blur, faded colors, soft digital detail, mild noise, accidental zooms and natural camera imperfections. — OUTSIDE THE HOUSE She steps outside carrying a small reusable shopping bag. She locks the door, adjusts her messy ponytail and looks toward the camera with a relaxed smile. — BAKERY STOP She reaches a tiny neighborhood bakery and buys a warm pastry. She steps outside, takes her first bite and immediately smiles because it tastes good. She notices her friend filming and holds the pastry toward the camera playfully before taking another bite. — WALKING HOME She continues down the narrow street while eating. A neighborhood cat follows her for a few steps. She notices it, crouches down and gently pets it. — SMALL ACCIDENT She walks beneath a large tree when a few leaves fall onto her hair. She stops, looks confused, then realizes what happened and laughs. — QUIET MOMENT She reaches a low concrete wall beside the street and sits down for a moment. — FINAL MOMENT She stands up and continues walking home.
```

## 结构分析

**起作用的段（有 H3 Max 复测证据支撑整个 prompt 存活）**：

| 段 | 作用 | 迁移到本地 H3 六段方言时放哪 |
|---|---|---|
| `MAIN SUBJECT` 段 | 身份锁：外貌＋服装＋`Maintain the same … throughout` | `subject_definitions` 的 `<Subject 1> is …`＋`retention_analysis` 的 `fully_preserved` |
| `SETTING` 段 | 地理锚：具体物件清单＋氛围词收尾（lived-in, ordinary） | `subject_definitions` 的场景/地点定义，或正文场景句 |
| `CAMERA / VISUAL AESTHETIC` 段 | **核心手法**：用"有名字的设备＋枚举缺陷"买真实感（DV 摄像机＋手抖＋对焦抽动＋曝光漂移＋偏色＋噪点） | `detailed_description` 开场风格句。注意：此手法与我们静帧语料 S02 的 `smartphone-like look`＋`fine low-light grain` 是同一族 |
| 事件段（`—` 分节） | 每拍一个小动作，带因果（叶子落→困惑→笑）；无台词 | `detailed_description` 的 `[Shot N]` 或时间码句。本条无分镜时间码，靠事件顺序；本地 H3 有 17k+5 帧网格，应给 `At` 时刻 |
| 无音频段 | 本条没写声景 | 本地 H3 音画同轨，须补 `overall_soundscape`（此条在 Seedance 上声画分离，**这是两通道真实差异**） |

**已记录的未决张力**：本条原文没有 ban-list 尾部（对比同库其他条目常见 `no music, no subtitles` 尾），是靠正向描述达成的；我们 `h3-prompt-writing` 的风格锁一节记录"官方 3D 动画 skill 自带六连不要"与 prompt-guide §8 的矛盾未决。本条目不改变那个结论，只作为"正向写法在 H3 Max 上存活"的一个外部数据点。

## 边界

- 复测在 **H3 Max 云端 768p**；本地 h3q 跑的是本地权重、draft/final 档位。75.7 是 goodcase 的评测口径，不是我们的 `video_check`。
- 原文无参考图（纯文生视频）；本地 h3q **没有纯文生视频**，只有 first_frame / reference_image 两种——引用此条写本地任务时，起止状态须绑参考或首帧，这是通道硬差异。
- 单案例。证明"该写法这次存活"，不证明"DV 风格写法必然稳定"。

## 复用指引

写"生活流 vlog / DV 质感 / 单人漫步"类 H3 任务时，取它的三件东西：身份锁段结构、设备缺陷枚举法、每拍一动作带因果的事件链。不照抄格式——本地提交必须重排成六段方言并补声景段。
