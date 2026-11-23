# 真人摄影之外的分支-中文图鉴信息图-001

- 验证状态：**外部展示图为证**（来源作者生成，见 cover 图）；本地通道未测
- 来源：[ZeroLu/awesome-gpt-image](https://github.com/ZeroLu/awesome-gpt-image)（MIT，可直接吸收），无限画布提示词库同步条目
- 目标通道：GPT-Image（云端）——即本地 `magpie_generate_image` 的通道；对本地 Qwen 未测

## 原图观察（据来源展示图）

博物馆展板式中文拆解信息图：米白纸纹底，人物居中立姿，左侧结构拆解＋中文引线注释，右上材质纹理样块，右中配色/纹样释义，底部穿着顺序流程图。全图中文清晰可读。

## 完整原文（逐字保留）

```text
Please automatically generate a "museum catalog-style Chinese disassembly infographic" based on the [Subject].

The entire image is required to combine a realistic main visual, structural disassembly, Chinese annotations, material descriptions, pattern meanings, color meanings, and core feature summaries. You need to automatically determine the most appropriate main subject, clothing system, artifact structure, era style, key components, material craftsmanship, color scheme, and layout structure based on the [Subject], and the user does not need to provide any other information.

The overall style should be: national museum exhibition boards, historical clothing catalogs, and cultural/museum thematic infographics, rather than ordinary posters, ancient-style portraits, e-commerce detail pages, or anime illustrations. The background uses paper textures such as off-white, silk white, and light tea color, making the overall look premium, restrained, professional, and collectible.

The layout is fixed as:
- Top: Chinese main title + subtitle + introduction
- Left: Structural disassembly area, with Chinese lead lines annotating key components, accompanied by close-up details
- Upper right: Material / craftsmanship / texture area, displaying real texture samples with descriptions
- Middle right: Pattern / color / meaning area, displaying the main color palette, pattern samples, and cultural explanations
- Bottom: Dressing order / composition flowchart + core feature summary

If the subject is suitable for character display, use a full-body standing posture of a real person as the central subject; if it is more suitable for artifacts or single structures, change it to a central subject disassembly diagram, but the overall form remains a complete Chinese infographic. All text must be in Simplified Chinese, clear, neat, and readable, without garbled characters, typos, English, or pinyin. The focus is on highlighting real structures, material differences, cultural explanations, and a catalog atmosphere.

Avoid: poster feel, studio portrait feel, e-commerce feel, anime feel, cosplay feel, random annotations, incorrect structures, blurry text, fake materials, excessive decoration.
```

## 结构分析

**这套写法与我们的关系成文是两个流派，各有正确场景**：

| 段 | 手法 | 与我们方法的关系 |
|---|---|---|
| `[Subject]` 模板变量 | 一处占位，其余全由模型自动决定 | 与"事实先于正文"相反——适合**模板型产品**（批量出同版式不同主题），不适合保真复刻；复刻任务仍走四层契约 |
| 风格定义＋邻域排除 | "national museum exhibition boards … **rather than** ordinary posters, ancient-style portraits, e-commerce detail pages, or anime illustrations" | 用"点名邻近风格并排除"来防风格坍缩——与我们 2D 分支的"类别词不代替具体画法"互补；对有强中文理解的 GPT-Image 有效 |
| **固定版式规格** | Top/Left/Upper right/Middle right/Bottom 五区各写内容 | 信息图/图鉴类的正确工具——版面就是事实，逐区规格比关系成文更可控。叙事画面仍用 visual-prose，别混用 |
| 中文文字要求 | "All text must be in Simplified Chinese … without garbled characters" | GPT-Image 的中文图内文字是强项（`magpie_generate_image` 的选型理由）；本地 Qwen 未验证此能力 |
| 尾部 `Avoid:` 清单 | 10 项排除 | GPT-Image 无独立负向槽，排除清单在正文内——展示图为证这次成立了，但这是该案例条件下观察到，不升级为通用结论 |

## 边界

- 展示图是来源作者的生成结果；本地 `magpie_generate_image` 未实测此条。用于云端 gpt-image 出中文图鉴/信息图时优先参考。
- 中文正文是本条的**正确选择**（图内文字就是中文）；不是说所有通道都该用中文正文——本地 Qwen 静帧仍走英文正文＋四层契约。
- 固定版式规格不适用于叙事静帧；`[Subject]` 模板式不适用于保真复刻。

## 复用指引

写"中文图鉴 / 拆解信息图 / 知识卡片 / 版式固定批量出图"类任务（云端 gpt-image）时，取三件：五区版式规格骨架、邻域排除句式、中文文字硬要求。主题占位保持单变量；不要把叙事画面的关系成文塞进这里。
