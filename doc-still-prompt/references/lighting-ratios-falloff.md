# 光比、衰减与负补光

当本帧需要比较屏幕、脸、手、背景或诊断光向问题时读取。先说明哪两个可见区域需要怎样的关系，再决定是否写档差或光比；不要求每帧填写一套摄影数值。

## 档与比值

同一种测量量每多1档，数值翻倍：

| 档差 | 比值 |
|---|---|
| 0 | 1:1 |
| 1 | 2:1 |
| 2 | 4:1 |
| 3 | 8:1 |
| 4 | 16:1 |

这是比值换算，不直接规定情绪或风格。“key:fill”可能指两个光源单独的照度，也可能被用于描述亮侧与暗侧的总受光；两种定义不能混算。需要数字时说清比较对象。像素亮度还受材质反射率、曝光、色调映射与介质影响，不能从一个固定比值保证剪影或纪实感。

有明确设计依据时可写：

```text
The dashboard screen sits two stops below the light on his hand, leaving the fingers and the printed receipt easy to read together.
```

无此设计值时可用清楚的相对描述，例如屏幕较暗但数字仍可读，不编造“专业必须两档”。

## 背景与注意中心

背景压暗是一种办法；色彩、清晰层、边界、动作和画面位置也能引导注意。灯焰、太阳、窗和屏幕可以比脸更亮。先判断本镜需要读什么，再决定明暗层级；不要求主角皮肤是全画面最亮处。

```text
The bright window fills the upper background. Against it, her darker hand holds the folded note in a clear silhouette, with the writing side turned toward the room light.
```

亮背景与可读主体可以同时成立，是否足够仍以本镜画面与文字政策核对。

## 衰减：距离、角度与遮挡分别判断

- **小型光源的距离变化**：在可近似点源、传播条件适合时，照度随距离平方反比下降。例：靠近手的裸灯比房间深处的墙更强。具体档差取决于距离，不默认几厘米就掉两档。
- **窗、灯箱、天空等扩展源**：在近处通常不能用简单点源近似概括；还需考虑光源角尺寸、可见面积、遮挡与反射。窗边脸的亮暗不全是距离衰减。
- **太阳直射**：在普通场景尺度内，光源距离变化对强度可忽略。表面明暗主要受朝向、遮挡、表面材质及天光/环境光共同影响。若使用 `falloff`，说明看到的是表面转向还是影界，不把这个单词本身判为户外物理错误。
- **散射与气氛**：雾、烟、空气透视或风格化阴影另有成因；不把所有亮暗变化都塞进平方反比解释。

正文以可见结果为主：

```text
Light from the nearby lamp brightens the knuckles nearest its shade; the fingers turning beneath the cup fall into softer room light.
```

## 负补光

负补光是通过吸收或遮挡减少环境反射光，例如黑旗或暗墙降低一侧原本会收到的反射；它不是另一盏fill灯，也不是“主光对面”的同义词。

```text
A dark panel beside the chair reduces the reflected light reaching the far cheek, leaving that side darker than the forehead facing the window.
```

须有这个面板/环境条件的依据，不能为解释暗侧临时增设。暗侧发灰可能来自光向、反射、曝光、材质或色调映射，不凭发灰就认定缺负补光。暗部是否保留纹理服从本镜read与介质，剪影或图形化黑区同样可用。

## 人像明暗图案词汇

只在需要描述面部明暗时选用；物件、背影、平涂或均匀身份板可记NA。

| 名称 | 常见可见特征 | 可选描述 |
|---|---|---|
| Butterfly | 正前偏高光形成鼻下小影 | `a small shadow directly beneath the nose` |
| Loop | 鼻影向一侧延伸，尚未连上颊影 | `the nose casts a short shadow across the cheek` |
| Rembrandt | 暗侧眼下留一小块三角亮区 | `a triangular patch of light beneath the far eye` |
| Split | 两侧脸有较明显亮暗区分 | `one side of the face lit, the other in shade` |
| Short | 较少朝向镜头的那侧受主光 | `the far cheek catches the window light` |
| Broad | 较多朝向镜头的那侧受主光 | `the cheek nearest the camera is lit` |

图案依赖头角度、光源面积和位置，不能只报45°就保证伦勃朗三角。术语后接必要可见关系，比不加解释的标签更易核对，但不规定某个词是模型唯一有效写法。

## 光源、视线与反射各有归属

角色看窗时，视线和窗光可以同向；角色看包、对手或屏幕时，光可以来自另一侧。分别记录光源在哪里、照到什么、人物看什么。眼内高光回指可解释的光源/反射环境；它不要求光源进入取景，也不要求窗、瞳孔和目标排成一条线。

高光的形状和数量受光源、遮挡、角膜视角与景别影响。近景看得清时再写，远景或简化介质不补不可见碎点、泪膜与虹膜纤维。

## 条件回读

1. 本镜需要比较哪些亮区？各自承担什么read？脸不必最亮。
2. 相对亮度是否足够清楚？数字有观测或设计依据吗？没有需要可NA。
3. 描述的明暗是距离、表面转向、遮挡还是介质处理？解释没有超出依据吗？
4. 负补光是否实际存在？没有时不编黑旗/暗墙。
5. 光向、阴影、反射是否与本场一致？目光独立服从剧情目标。
6. 当前景别与介质能读到这些细节吗？细节不适用时留在NA，不进正文。
