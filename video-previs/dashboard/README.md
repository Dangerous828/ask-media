# 视频拉片工作台

## 启动
默认端口 11872，服务只绑定 127.0.0.1 回环，**无鉴权设计**；不要转发到公网或局域网。
```
python launch.py 11872
```
（或 `python server.py 11872`）然后浏览器打开 http://127.0.0.1:11872

## 项目目录（首次使用先建）
仓库不含 `projects/`。后端从 dashboard 目录向上查找第一个含 `projects/` 的目录作为工作根；
找不到时页面项目列表为空。新建方法：在你要用的工作根下建 `projects/<项目名>/`，例如：

```
<工作根>/projects/示例项目/
├── 拉片素材/     # 原片；切点产物 frames_<名>/ 放这里
├── 素材/         # 导入的视频（导入即复制进项目，见下）
├── 分镜/         # storyboard JSON、Excel
├── 白模/         # 2D 预演 mp4
├── 白模3D/       # Blender .blend / 生成脚本
├── 成片/
└── 根目录/       # 散放的产物（可选）
```
子目录按需建，扫描器会自动跳过不存在的目录。

## 功能
- 左侧：projects/ 项目卡片（自动扫描，支持筛选）+ Downloads 源视频库（数量取决于本机 Downloads，点击直接播放，可一键导入当前项目）+ 当前项目影片
- 步骤页：总览状态 / ①拉片(切点) ②台词时间戳(OCR+ASR) ③分镜(JSON+Excel) ④白模成片(MP4) ⑤镜头语言讲解 / ⑥3D白模(Blender) / 全部产物
- 后端可调用 Skill 脚本（/api/run），任务后台执行 + 实时轮询日志（带计时）

## ⑥ 3D 白模（Blender）
- 自动扫描 `白模3D/`、`三维探索/` 及项目根目录的 `.blend / .mp4 / build_*.py`；render/ 帧序列自动折叠
- 卡片：.py 直接在网页看代码、.blend 弹窗可「在本机 Blender 打开」或「CLI 后台渲染」
- 动作按钮：🟢 打开 .blend（Windows 上 os.startfile）／ ▶ CLI 渲染（blender -b blend -a，任务超时 60min）／ ▶ 发送构建脚本到 Blender（MCP 127.0.0.1:9876 execute_code）
- Blender 可执行路径可用环境变量 `BLENDER_EXE` 覆盖，未设置时按 Windows 常见安装路径查找；CLI 渲染需要本机装有 Blender。

## 源视频
源片在 Downloads（Windows 默认 `C:\Users\<you>\Downloads`），工作台从该目录读取并**在导入时把文件复制进** `<工作根>/projects/<项目>/素材/`，不改动源文件；不导入则只读挂载播放。
媒体支持：mp4/mov/mkv（Range 拖动）、jpg/png、wav/m4a/mp3、md/txt/srt/json/py 文本预览、blend/xlsx 下载

## ⑦ 分镜 JSON → Blender 3D 一键生成
- 工具：`../scripts/blender_previs.py <storyboard.json>`（消费 dialogue 引擎契约：set/actors/shots 的 pos/look/fov），位于本 Skill 的 `scripts/`
- 产物：`projects/<项目>/白模3D/gen_<slug>.py` + `gen_<slug>.blend`（脚本发到 MCP 后自动存盘）
- 工作台 ⑥ 页签按钮：「✨ 从分镜JSON 一键生成 3D 场景」= 生成脚本 → 自动发送 Blender MCP(9876) 构建；之后可点「Blender CLI 后台渲染」出帧
- 支持：tatami 和室预设（榻榻米/障子/矮桌碟碗/坐姿）与 generic 通用房间预设；机位/fov/切点全部来自分镜 JSON
- 注意：previs_engine 自动机位模式（无显式 pos/look）暂不支持生成，需 dialogue 契约 JSON

## LLM 配置与 API Key
在设置页保存的 GLM API Key 会**明文**写入本目录 `llm_config.json`（已被根 `.gitignore` 排除，绝不入仓）。
- 推荐优先用环境变量 `ZHIPUAI_API_KEY` / `GLM_API_KEY`，页面保存只作为本机可选项。
- 页面保存时 key 留空只改模型、不动环境变量里已有的 key；点「清除 Key」才显式删除。
- 若曾在此目录保存过 key，勿把 `llm_config.json` 加入任何提交。
