# 2D插画-绘画性动漫双人缠斗-001

- 验证状态：**部分通过**（光线/构图/身份成立；品牌文字与画法颗粒未达）
- 通道：本地 h3q · Qwen Image 2.1，1536×1216，seed 42，cfg 4.5（r1 为 3.5），40 步标准档，无参考图
- 出图证据：`~/Code/kTool/research/t2i-contract-regression-20261106/output/compare-S01-r2.png`（r1 对照在同目录 `-r1`）
- 原图：`~/Code/kTool/recreate-20261106/refs/ref01-deepseek-vs-glm.png`

## 原图观察

- 画法：绘画性二次元插画——细碎断续轮廓、软硬边混合、灰蓝中间调厚涂、皮肤有粉紫过渡
- 机位：斜向俯视近景，可见两人头顶与肩胸上表面，前景拳与大腿被裁切
- 光：强白光从右后上方来，勾亮银发、肩缘与抬臂；脸部明显更暗；背景灰暗，墙面可辨
- 动作：黑发人物左臂高举抓银发头顶发束；银发人物右臂向左伸入黑发/躯干遮挡区**末端不可见**；两人各一拳伸向画面前方两侧
- 人物：黑发+蓝鲸发夹+黑裙"deepseek"印花；银发+GLM 发夹+白裙"GLM"印花；银发**一眼挤闭**另一眼睁开
- 下半幅：亮色角状薄片反光形态混在裙摆翻边、缎带与散发间，材质不明

## 实际英文（r2 提交原文，关键段）

```text
A painterly two-girl anime illustration, loose visible brush strokes building soft broken transitions around the eyes and jaw, muted grey-blue midtones… An oblique close view looks steeply down across the visible crowns of their heads and the upper surfaces of their shoulders, foreshortened fists and thighs filling the near foreground, cropped by the frame. The black-haired woman's face sits higher at the left and the silver-haired woman's face lower at the right, a clear lateral gap between them; neither face points at the viewer.

…Her left arm is raised high from the shoulder at the right edge of her torso, her fingers knotted in the silver-haired woman's white hair and pulling it upward…

…One eye is squeezed nearly shut while the visible violet eye turns up toward the black-haired woman…

Bright, thin, shard-like reflective shapes and flaring skirt edges break up the lower frame among loose hair and ribbons, catching hard white highlights.

Strong white light enters from high behind the pair and to their right, a bright rim tracing the silver hair and the raised arm; grey-pink and pale lavender facial midtones stay clearly darker than that rim…
```

## 出图结果（r2）

**成立**：陡俯角（r1 是平视）、右后逆光轮廓、脸部暗于亮缘、一眼挤闭另一眼睁开、黑发左臂抓发、双人分区。r1→r2 的改善证明是正文关系收拢的作用，不是抽 seed。

**未成立**：
1. **品牌文字**：正文两轮都写了逐字母 `d-e-e-p-s-e-e-k in clear lowercase sans-serif letters`，两轮出图都渲染为 `deepseok`。这是"已明确写出但通道未执行"的实证——品牌词/生造词在此通道不可靠。
2. **画法颗粒**：`loose visible brush strokes` 出图仍偏整洁赛璐璐，原图的碎笔涂抹感未恢复。形容词层面的画法指令（painterly/loose strokes）执行弱于几何关系指令。
3. **缠斗压缩感**：两人体态偏直立，原图的贴身错位压缩未完全恢复。

## 教训

- `neither face points at the viewer` + 各自 `face turned toward …` 是把"互看"从朝向冲突里解出来的有效写法（r1 两人都看镜头）。
- 光线收拢句式有效：`a bright rim tracing … ; facial midtones stay clearly darker than that rim`——用相对明暗关系而非光位术语，两轮都稳定执行。
- **几何/关系指令（俯角、左右、明暗、朝向）执行可靠；画法质感指令（painterly、loose strokes）执行不可靠；品牌文字不可靠。** 三类可靠性不同，验收和返修要分开对待，不要把画法残留当写词失败反复改词。
- 关键品牌文字在此通道建议直接规划后期贴字，不在正文里反复博弈。

## 复用指引

写"多人缠斗/逆光/俯视"类 2D 插画纯文生图时：朝向用 `neither face points at the viewer` 类否定+相对朝向；明暗用相对关系句；遮挡末端写 obscured 不猜接触。品牌文字预期失败，进审计提示通道限制。
