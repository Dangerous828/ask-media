# shortvideo-understand

> 让任何支持 Agent Skills 的客户端**看懂短视频链接**：B 站 / 抖音（及 yt-dlp 支持的其它平台）
> 链接 → 标题、作者、时长、带时间轴文字稿，可选**画面层**（抽帧 + 多模态识图，抄出屏幕上的数字、
> UI、商品参数、代码、地图名等"只在画面里"的信息）。"看懂并回答"由 Agent 自身完成，
> 脚本只负责把视频变成 Agent 可以直接阅读的证据。

## 何时用

- 用户发来 B站 BV 号 / b23.tv 短链 / 抖音 `v.douyin.com` 链接，问"看看这条视频讲了啥 / 总结一下 / 视频里那个数值是多少 / 这条爆款怎么做的"
- 需要把一条短视频转成可检索的文字稿笔记
- 需要判断某条视频的信息分布（纯口播？还是关键信息全在画面上？）

## 入口

```bash
python3 scripts/understand.py "<URL 或 BV 号>"           # 文字稿（默认字幕优先）
python3 scripts/understand.py "<URL>" --look             # 加画面层
python3 scripts/understand.py "<URL>" --look --timestamps 0,45,90
python3 scripts/understand.py "<URL>" -o note.md         # 落 Markdown
python3 scripts/look.py /local/video.mp4 --frames 8      # 只要画面层（本地文件）
```

## 依赖

必需：

```bash
brew install ffmpeg          # ffmpeg + ffprobe
uv tool install yt-dlp       # 或 pip install -U yt-dlp
```

音频转录后端（二选一，优先前者）：

```bash
pip3 install mlx-whisper               # Apple Silicon，无需 torch；默认模型 mlx-community/whisper-large-v3-turbo
# 或
pip3 install funasr modelscope torch torchaudio   # SenseVoice-Small（约 2GB）
```

画面层（可选）：需要一个 OpenAI 兼容多模态端点。默认指向本机 sensenova 网关。

```bash
export CHUBBY_VISION_BASE="http://127.0.0.1:8321/v1"
export CHUBBY_VISION_MODEL="sensenova-6.8-flash-lite"
export CHUBBY_VISION_API_KEY=""        # 本地网关可留空
```

## 目录结构

```
shortvideo-understand/
├── SKILL.md                    # 触发词、路由、边界（Agent 侧）
├── scripts/
│   ├── understand.py           # 主编排：平台判定 + 元信息 + 字幕优先 + ASR + 画面层
│   └── look.py                 # 画面层：视频 URL/本地 → 抽帧 → 多模态描述
└── lib/chubby_common/          # 就地修正后的公共工具（vendored）
    ├── cookies.py              # 零配置浏览器 cookie 探测（按域条数择优）
    ├── deps.py                 # 绝对路径解析（yt-dlp / ffmpeg 不在 PATH 也能找到）
    ├── ytdlp.py                # yt-dlp 封装（cookie / UA / Referer / 重试 / 友好错误）
    ├── vtt.py                  # 字幕解析：同时支持 .vtt 与 .srt + 时间轴抽取
    ├── asr.py                  # 可插拔 ASR：mlx-whisper 优先，funasr 兜底
    ├── funasr.py               # SenseVoice-Small 后端实现
    ├── douyin.py               # 抖音分享页取流（不能走 yt-dlp，稳定 403）
    └── config.py               # PlatformConfig：平台差异收敛为数据
```

## 关键实现说明（实测踩过的坑，勿改）

- **cookie 是零配置的**：`lib/chubby_common/cookies.py` 扫描本机浏览器（Brave/Chrome/Edge/Chromium/Firefox）的 cookie 库，按目标域下的条数择优，无需设任何环境变量。B 站 AI 字幕与抖音分享页都依赖这个——匿名状态下 B 站只有 danmaku 字幕、抖音返回蜘蛛壳。
- **字幕优先是硬成本规则**：`Whisper-large-v3-turbo (MLX)` 的模型冷加载实测约 155 秒，与音频时长无关（5 秒音频同样 155s，warm 后仅 2.8s）；B 站命中字幕则秒级完成。所以能拿字幕绝不转录。
- **B 站字幕即使指定 `--sub-format vtt` 也落盘为 `.srt`**：只扫 `.vtt` 会让字幕优先必然失效回退到 ASR，故同时扫描 `.vtt` 与 `.srt` 两种扩展名。
- **抖音不能走 yt-dlp**：对 `douyin.com` 稳定返回 `HTTP 403 / Fresh cookies needed`。唯一可靠路径是 `iesdouyin.com/share/video/<id>` + iPhone UA，再解析 `window._ROUTER_DATA` 取 CDN 直链（把 `playwm` 换成 `play` 去水印）。
- **cookie 不能交给 `curl -b <netscape 文件>`**：浏览器里存的是 `.douyin.com`，按域匹配**不覆盖** `iesdouyin.com`（两者可注册域不同），实测等于没带 cookie。必须显式拼成 `Cookie:` 头发送，用完即删临时文件，凭据不留盘。
- **画面层只下视频轨**：不下音频能省一个数量级时间（同片 1491s：纯 360p 视频轨 8.7s；视频+音频合并下载曾超时 293s）。`--download-sections` 分段下载对 B 站 CDN 不稳定，未采用。
- **抖音 `--look` 只下载一次**：抖音的 mp4 自带音轨，画面层与转录复用同一文件，不再二次拉 CDN。
- **本地图像网关强制思考**：`thinking:{"type":"disabled"}` 与 `reasoning_effort:"none"` 对 `127.0.0.1:8321` 实测均不生效（reasoning 固定吃 350~600 token）。`max_tokens` 低于 ~1200 时 `content` 会被截空只剩 reasoning 草稿。故按 `1600→2500→2500` 预算阶梯重试，末位仍空才输出显式标注的降级稿。
- **Agent shell 的 PATH 常常不含 `/opt/homebrew/bin` 与 `~/.local/bin`**：`deps.py` 显式尝试常见路径；`asr.py` 给 `mlx_whisper` 内部裸调 `ffmpeg` 补 PATH。

## 出处

B站/抖音转录链路基于 [chubbyguan/chubbyskills](https://github.com/chubbyguan/chubbyskills) v0.15.0（MIT，`LICENSE` 随包保留）的 `bilibili-transcribe` / `douyin-transcribe`。字幕双扩展名扫描、零配置 cookie 探测、可插拔 ASR 后端、抖音 Cookie 头拼装、可执行文件绝对路径解析，以及画面层 `look.py` 与编排层 `understand.py`，行为定义全部见上文「关键实现说明」。

回流上游 PR 时，可在任意位置 `git clone` 上游 v0.15.0 作对照；本机另存有派生仓 `~/projects/vendor/chubbyskills/`（含 `.patch-backup/` 改动前原文件），非运行依赖。

## 已知边界

- 不支持说话人分离；多人对话需借 `timed` + 画面层判断
- 无人声视频（口技/BGM/风景）ASR 会幻觉出重复字，必须走 `--look`
- B 站 4K / 1080P60 需要大会员（属平台限制，与本技能无关）
- 抖音短链 `v.douyin.com/xxx` 会过期，过期后需要新链接；风控严时先浏览器打开 douyin.com 再重试
- 画面层依赖多模态端点，本机网关未起时 `notes` 会记 `画面层失败`，主流程不中断

## 合规

仅供**个人学习与研究**使用。请遵守目标平台 ToS 与 robots 规则，控制请求频率，不批量抓取、不商用、不侵犯他人权益。下载内容的版权归原作者。
