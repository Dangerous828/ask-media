# 2.5 档位能力与队列执行能力

**提交前核对实际服务端 `build_argv` 与渲染器，不只看客户端帮助或档位表。** 2026-10-24 在渲染机核验：h3q视频分支支持first_frame、帧数、尺寸和步数；**2026-10-29 起 `h3qc submit` 另支持 `--workflow lu2|pdd_lu`、`--loras`、`--no-upscale`、`--out-width/--out-height`，短剧 adapter 已用 `parameters.tier` 暴露（见 §2.8），2026-11-01 起默认 draft**；仍没有任意graph参数；Mac adapter 已有 last_frame 成对校验与透传路径；该历史核验不能说明当前部署缺少首尾帧，实际服务端支持范围按本技能「输入能力与续接职责」核对。I2VA实际调用lib_workflow的Q4 Turbo图。下表hq/ref6属于构图工具能力，不等于该队列可以选择的生产档位。只有队列实际支持且输出workflow已核对，才报告使用相应档位。

`h3_quick.py`直连8199，不能替代h3q，**不得用于任何提交**（离线研究也必须在 GPU 空闲且经创作者同意时，由人工执行）。入口不支持优选档时明确记录实际回退与质量验证，不把增加步数当作切换底模或提高量化精度。下表只记录离线实测，**h3q 当前不可选这些档位**：

| 档位 | 底模 | LoRA | 步数 | 模式 | 用途 |
|---|---|---|---|---|---|
| `draft` | `fl2va_turbo_Q4_K_M.gguf` | 无（烘焙） | 8 | I2VA | 旧档，仅回退用 |
| `hq` | `fl2va_pruned_w6a8` | `fl2v_turbo_8step_v1.0_768p` | 8 | I2VA | 离线实测较优；h3q 不可选 |
| `ref8` | `ref2va_pruned_int8` | 无 | 20 | Ref2VA | 定稿 |
| `ref6` | `ref2va_pruned_w6a8` | `ref2v_turbo_8step_v1.1_768p` | 8 | Ref2VA | 未实跑；h3q 不可选 |

**换档的实测依据（2026-10-21，同首帧/同提示词/同 seed）**：

| 场景 | draft Q4 | hq w6a8 | 结论 |
|---|---|---|---|
| 横屏 1344×768×192f | 686.4 s / SSIM 0.808 | **546.3 s / SSIM 0.878** | 快 20%，更像官方 |
| 竖屏 768×1344×107f | 295.4 s | **222.6 s** | 快 25% |

> ⚠️ **关键不是清晰度，是构图稳定性。** 竖屏实测中 draft(Q4) 中段漂成脸部特写，
> hq(w6a8) 全程稳住中景。原因是 Q4 的 turbo 蒸馏自 **544p**，跑 768p 时先验错位。
> 官方 768p 专用 LoRA 才对齐。

`ref6` 文件与脚本已就绪但**未实跑验证**，首次用先跑小样。

**画布硬约束**：宽高必须都是 **32 的倍数**。720/1080 都不合法，报
`height=720 is not a multiple of 32`。用 1248×704、1312×736、1344×768、768×1344。

**PDD 竖屏支持（2026-11-20 新增，example-project 9:16）**：`pdd_render_ref.py` 用 `--width/--height` 覆盖首采（横屏 argv 不变），`h3q.py` pdd_lu 分支已透传；MCP `_pdd_argv` 仅 width<height 时传首采，MCP 改动需重连才生效（重连前可直连 `h3qg.py submit --workflow pdd_lu --width ... --height ... --no-upscale`）。
**推荐尺寸**：draft 首采 **576×992**、final 二采 **832×1440**（对 896×1536 基准的 aspect 差均 <2%）；896×1536 面积超 1536×864 上限会被拒。⚠️ **竖屏 draft 与 final 首采不是同一画布**（832×1440 → 544×960，宽高比差约 2%），**draft 只验表演/动作、不验构图**；要"草稿即成片构图"须让两条路径首采同尺寸（改 MCP `_pdd_argv`，需单独授权）或按 `../SKILL.md`「两条通道的档位语义」把 draft/final 当两次完整采样分别验收。尺寸推导与核验经过见 [incidents.md](incidents.md) §2026-11-15 档位对齐，结论见 [`pdd-offline-recipe.md`](pdd-offline-recipe.md)。

