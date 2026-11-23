---
name: shortvideo-understand
version: 1.0.2
license: MIT
description: >
  让 AI 看懂短视频链接：B站/抖音（及 yt-dlp 支持的其它平台）链接 → 标题、作者、时长、
  带时间轴文字稿，可选画面层（抽帧 + 多模态识图抄出屏幕文字/数值）。
  当用户发来 B 站/BV 号/抖音/b23.tv/v.douyin.com 链接并说"看看这个视频""总结一下"
  "讲了啥""这条爆款怎么做的""视频里那个数据是多少"，要把视频转成文字稿/笔记，
  或复刻/翻拍时需保留链接原片并取得文字证据时使用。
  只做"把视频变成 AI 可读证据"，不负责剪辑（归 concat-video）、逐镜拆解、复刻项目编排、出图/出片或发布运营。
  skill 版本 1.0.2；转录链路引用上游 chubbyskills v0.15.0。
metadata:
  category: media
  triggers: 视频链接理解、看视频、总结视频、B站字幕、抖音转文字、视频转笔记
---

# shortvideo-understand — 短视频链接理解

把 B 站 / 抖音链接变成 Agent 能直接读的文字证据，然后**由你自己（Agent）完成"看懂"与回答**。

## 何时用 / 不用

**用**：用户发来视频链接（或 BV 号）并想了解内容；要把视频转成文字稿/笔记；要核对视频里出现过的数字、参数、标题、商品信息；要拆解一条短视频的叙事结构。
**不用**：剪辑成片 → `concat-video`；AI 出图/出视频 → `doc-still-prompt` / `h3-*`；发布与选题运营 → `write-tweet` / `write-article`。

## 核心判断：先拿字幕，再考虑转录

这是本技能唯一最重要的成本规则，实测得出：

| 路径 | 耗时 | 条件 |
|---|---|---|
| **B 站 AI/CC 字幕** | **秒级** | 本机浏览器登录过 B 站 |
| 音频转录（MLX Whisper large-v3-turbo） | **模型冷加载 ~155s** + 音频时长×约 1/3 | 无字幕时 |
| 音频转录（模型已热） | 约 5s 音频 / 2.8s | 同进程连续调用 |

- 冷加载 ≈155 秒与音频长短无关（5 秒音频同样要 155 秒）；warm 后 5 秒音频仅 2.8 秒。
- 所以：**能拿字幕绝不转录**。`--no-subtitle` 只在字幕明显错误或需要逐字稿时用。
- 长视频优先只处理前段：先跑，再按 `--max-minutes` 提示决定是否需要全量。

## 零配置（开箱即用，无必需环境变量）

cookie 由 `lib/chubby_common/cookies.py` 自动探测：扫描各浏览器 cookie 库的条数，选登录过该平台的那个（复制到临时目录再查，只读、不解密、不打印值）。

- **B 站**：匿名状态只有 `danmaku` 字幕；带登录 cookie 才会出现 `ai-zh` 字幕。这是"字幕优先"能否成立的关键。
- **抖音**：无 cookie 时分享页返回蜘蛛壳（无 `videoInfoRes`）。
- 用户可以强制指定：`YTDLP_COOKIES_FROM_BROWSER=brave`（优先级最高）。

## 用法

```bash
cd <本技能目录>

# 最基本：只要文字稿（JSON 到 stdout）
python3 scripts/understand.py "https://www.bilibili.com/video/BV1xxxxxxxxx/"
python3 scripts/understand.py "BV1xxxxxxxxx"
python3 scripts/understand.py "https://b23.tv/uMUrdgJ"  # 自动展开短链再提取 BV 号
python3 scripts/understand.py "https://v.douyin.com/xxxxxxx/"

# 复刻/翻拍：显式保留最高可用画质的完整原片（默认不下载）
python3 scripts/understand.py "<URL>" --keep-video <项目>/输入/原片

# 加画面层（短剧、带货、游戏账号、PPT 类视频必加）
python3 scripts/understand.py "<URL>" --look                  # 均匀 6 帧
python3 scripts/understand.py "<URL>" --look --frames 12
python3 scripts/understand.py "<URL>" --look --timestamps 0,45,90,135

# 落成 Markdown 笔记（含处理说明、文字稿、时间轴、画面层）
python3 scripts/understand.py "<URL>" --look -o note.md
python3 scripts/understand.py "<URL>" --markdown               # Markdown 到 stdout

# 只要画面层（已有本地视频时）
python3 scripts/look.py /path/to/video.mp4 --frames 8
```

参数：`--no-subtitle` 强制转录；`--max-minutes N` 超过 N 分钟时在 `notes` 里提示分段；`--frames`/`--timestamps` 控制画面层；`--height` 画面层下载视频轨最大高度（默认 480；小字、OCR 密集的画面提到 720）；`--keep-video DIR` 显式下载并保留最高可用画质的完整音视频，JSON/Markdown 的 `video_path` 给出实际路径；`-o` 落文件。

复刻/翻拍按 `short-drama` 的 `../drama-skills/skills/short-drama/references/video-remake.md` 衔接：把 `video_path` 交给 `video-previs` 的 `extract_shots.py --rep-frames ...` 生成切点与代表帧。`--look` 的压缩识图副本只用于读画面，不能登记为 `SRC-xx.jpg`；本技能只负责链接取证与原片保留，项目编排归 `short-drama`，媒体验收归 `short-drama-review`。

## 输出结构（JSON）

```json
{
  "platform": "bilibili|douyin|other",
  "source": "规范化后的链接",
  "title": "...", "author": "...", "duration": 1491.6,
  "transcriber": "字幕:sub.ai-zh.srt 或 Whisper-large-v3-turbo (MLX)",
  "text": "完整文字稿",
  "timed": [["00:00:00", "首句"], ["00:00:01", "..."], "..."],
  "video_path": "/absolute/path/source.mp4（仅 --keep-video 时出现）",
  "shots": [{"t": 8.0, "description": "【画面】...【文字】...【镜头】..."}],
  "notes": ["降级/风控/失败原因，可能是空数组"]
}
```

**失败时的输出契约**：stderr 打印两行（`❌ 处理失败：<原因>` + `   处置：<下一步>`），退出码 `2`。把「处置」原文转达给用户，不要自己编原因。

**先读 `notes`**：它记录降级原因（无字幕、蜘蛛壳、字幕过短、画面层失败）。`notes` 非空不代表失败，但要在回答里如实说明证据来源。

## 拿到输出后怎么"看懂"（这才是本技能的交付）

1. **先看 `transcriber`**：是 `字幕` 就用它的措辞；是 `Whisper` 就假定可能有同音错字（实测：`iPhone Duo` 被转成 `IPHONE度`），涉及专有名词/数字时要结合标题与画面层校对。
2. **判断要不要画面层**：以下类型**必须加 `--look`**，否则会漏掉核心信息——
   - 带货/测评：价格、参数、型号在画面上
   - 游戏、账号展示：ID、段位、数值只在 UI 里（实测：某抖音视频的关键信息 `编号1516586560`、`不朽星钻IV`、`王牌次数14` 全在画面）
   - 教程/代码/PPT：屏幕内容即正文
   - 剧情/短剧：要拆镜头、走位、字幕位置
   纯口播、访谈、播客类，音频稿通常够。
3. **交叉核对**：文字稿与画面层冲突时，以画面为准（OCR 抄的是原始字符），并在回答里指出差异。
4. **长视频**：先读 `timed` 定位，再回正文取细节，不要一次吞 1 万字。
5. **回答要带证据**：引用时间戳（`[12:34]`）；用户问"讲了啥"给结论+要点，问"某个数据"给逐字原文。
6. **画风观察与制作来源分开**：分别描述景别、脸部形面、发束、材质与光色，介质可写实拍观感、半写实CG、3D或2D动画；无法确认时标注不确定。逼真皮肤不证明是真人实拍，单帧也不证明使用了何种生成模型或渲染软件。仿作需匹配画风时，抽帧文字标签之外仍须目视核对代表帧。

## 已知边界与坑（都是实测踩过的）

| 现象 | 原因与处置 |
|---|---|
| B 站抓不到字幕 | 匿名只有 `danmaku`；需本机浏览器登录过 B 站。`notes` 会写出 cookie 探测结果 |
| B 站字幕文件是 `.srt` 而非 `.vtt` | 即使指定 `--sub-format vtt` 也落盘 `srt`。故本技能同时扫描 `.srt` 与 `.vtt` 两种扩展名 |
| 抖音 `HTTP 403 / Fresh cookies needed` | **yt-dlp 对 douyin.com 稳定 403，不要走 yt-dlp**。必须走 `iesdouyin.com/share/video/<id>` + iPhone UA |
| 抖音分享页"蜘蛛壳" | 无 `videoInfoRes`。处置：浏览器打开一次 douyin.com 再重试，或用 App 内「复制链接」的 `v.douyin.com` 短链 |
| 抖音 cookie 带了却仍被风控 | 不能用 `curl -b <netscape 文件>`：`.douyin.com` 按域匹配不覆盖 `iesdouyin.com`，等于没带。必须显式拼 `Cookie:` 头 |
| `FileNotFoundError: 'ffmpeg'` | Agent shell 的 PATH 常不含 `/opt/homebrew/bin`。本技能用绝对路径解析，并给 `mlx_whisper` 补 PATH |
| 缺少 `yt-dlp` | 装在 `~/.local/bin` 时 PATH 常不含。本技能会尝试该路径；仍找不到就装：`uv tool install yt-dlp` |
| 4K / 1080P60 下不了 | B 站大会员限制，与本技能无关 |
| 无人声视频转出满屏重复字 | 口技/BGM 类音频，ASR 会幻觉。此类必须走 `--look`，别信文字稿 |
| 画面层某帧返回 `（格式降级：仅思考草稿）` | 网关强制思考导致 `content` 被 `reasoning` 吃空；本技能已按 `1600→2500→2500` 阶梯重试，末位失败时才降级输出。远端 sensenova 直连加 `thinking:{"type":"disabled"}` 才真正关闭思考 |
| 画面层某帧返回 `（识别失败：…）` | 检查本机 `CHUBBY_VISION_BASE` 网关是否在跑（默认 `127.0.0.1:8321`）；`notes` 里也有摘要。文字稿仍可用 |
| 说话人分离 | 不支持。多人对话需借助 `timed` 与画面层人工判断 |

## 依赖

```bash
# 必需
brew install ffmpeg            # ffmpeg + ffprobe
uv tool install yt-dlp         # 或 pip install -U yt-dlp

# 转录后端（二选一；优先 MLX，无需 torch）
pip3 install mlx-whisper       # Apple Silicon，模型默认 mlx-community/whisper-large-v3-turbo
# 或
pip3 install funasr modelscope torch torchaudio   # SenseVoice-Small（约 2GB）

# 画面层（可选）
# 需要一个 OpenAI 兼容多模态端点，默认指向本机网关：
#   CHUBBY_VISION_BASE=http://127.0.0.1:8321/v1
#   CHUBBY_VISION_MODEL=sensenova-6.8-flash-lite
#   CHUBBY_VISION_API_KEY=<本地网关可留空>
```

## 合规

仅用于个人学习与研究：遵守目标平台 ToS 与 robots，控制请求频率，不批量爬取、不商用、不侵犯原作者权益。下载内容版权归原作者。
