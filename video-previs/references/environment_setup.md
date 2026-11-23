# 环境配置（LLM / Vision / Blender / 深度模型）

> **平台声明**：2D 渲染引擎（`dialogue_engine.py` / `previs_engine.py`）与 dashboard 启动脚本
> 按 **Windows 优先** 编写：引擎在初始化时加载 `C:\Windows\Fonts\msyh.ttc`（无跨平台回退），
> `launch.py` 用 `CREATE_NEW_CONSOLE`、`watch.py` 用 `pythonw.exe` + `DETACHED_PROCESS`。
> macOS / Linux 下初始化引擎会 OSError，跨平台尚未验证。
> 仅做拉片/台词提取/文档导出等离线步骤时不受字体限制。

Skill 核心拉片/白模是离线的（opencv/rapidocr/faster-whisper/本地引擎），无需密钥。
以下为可选的增强能力。

## 1. LLM + Vision（智谱 GLM，可选）
用于：自动补分镜描述、生成关键镜头讲解/潜台词、对接触印片做语义分析。
- 客户端：`../scripts/glm_client.py`（标准库实现，无第三方依赖）。
- 配置环境变量（二选一设 key）：
  - `ZHIPUAI_API_KEY` 或 `GLM_API_KEY`（智谱开放平台 key，必填）
  - `GLM_BASE`（默认 https://open.bigmodel.cn/api/paas/v4）
  - `GLM_TEXT_MODEL`（默认 glm-5.3-flash）
  - `GLM_VISION_MODEL`（默认 glm-4.5v）
- Windows 持久配置（PowerShell，用户级）：
  ```powershell
  [Environment]::SetEnvironmentVariable("GLM_API_KEY","你的key","User")
  ```
  配置后重开终端生效；`glm_client.is_configured()` 返回 True。
- 相关脚本：
  - `fill_descriptions.py`：为分镜/接触印片补描述（vision）。
  - `explain_storyboard.py`：生成关键镜头讲解（叙事/潜台词/镜头语言）。
  - `draft_storyboard.py` / `lapian_docs.py`：由接触印片+切点草拟分镜文档。
- 未配置 key 时这些脚本报“未配置 GLM_API_KEY”，不影响离线流程。

## 2. Blender 3D 白模（可选，需要 Blender）
- 脚本：`../scripts/blender_previs.py`。
- 输入 storyboard JSON，输出 `projects/<项目>/白模3D/gen_<slug>.py`（Blender Python 构建脚本）。
- 通过 Blender MCP 或在 Blender 内执行该脚本，生成 3D 场景/走位。
- 坐标约定：JSON (x横,y上,z深) → Blender (x, z, y)，与 `blender_previs.py` 的 `P()` 一致。
- Blender 可执行路径：dashboard 用环境变量 `BLENDER_EXE` 覆盖；未设置时按 Windows 常见安装路径查找。
- 适用：需要真三维走位/机位推演时；2D 对白白模（dialogue_engine）仍是首选、无需 Blender。

## 3. 离线依赖（必备，无需密钥）
- 基础 python 包：numpy / Pillow / opencv-python / openpyxl / rapidocr_onnxruntime / faster-whisper。
- 外部：ffmpeg（H.264 转码）、Blender（仅 3D 白模）。
- 字体：Windows `C:\Windows\Fonts\msyh.ttc`（白模渲染叠加文字，见顶部平台声明）。

### 3.1 深度动作捕捉的额外依赖（SKILL 流程第 5 步）
这两个脚本**不在基础依赖清单内**，按文档装基础包会在运行时 ImportError：
- `motion_depth.py`：需 `transformers`（底层 `torch`）。首次运行会联网下载 Hugging Face 模型
  `depth-anything/Depth-Anything-V2-Small-hf`（约百 MB 级），请确保网络可用或提前缓存模型。
- `motion_silhouette.py`：需 `rembg`（及其 onnxruntime 依赖）。首次运行会下载 `u2net_human_seg` 模型。
- 仅用拉片/2D 对白白模/台词提取时不需要这两项。

## 4. 云端 ASR（`extract_speech.py --engine cloud`，可选，配置不在本仓）
脚本支持云端引擎，但**配置源与豆包适配脚本均不在本仓库**，本仓只保留本地 faster-whisper 链路可开箱即用：
- 配置源：工作区的 workbench/providers.json（不在本仓；含 vendors 的 `base_url` / `api_key` / `enabled`，豆包另需 `extra.speech_api_key`）。
- 豆包适配：workbench/tools/doubao_plan_asr.py（不在本仓；Agent Plan SAUC WebSocket 实现，需 `base_url=https://ark.cn-beijing.volces.com/api/plan/v3`）。
- 通用 OpenAI 兼容链路走 `POST {base_url}/audio/transcriptions`，厂商需支持 `response_format=srt`。
- 没有上述文件与配置时请用默认 `--engine local`；报错“找不到 workbench/providers.json”即指此可选链路未配置，与本地 ASR 无关。
