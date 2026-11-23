"""shortvideo-understand 的内部工具层（vendored 自 chubbyguan/chubbyskills v0.15.0 并就地修正）。

模块职责：
  deps      可执行文件定位（yt-dlp/ffmpeg 不在 Agent 最小 PATH 里也能找到）+ 依赖体检
  config    PlatformConfig：把平台差异收敛成数据（UA / Referer / cookie 域）
  ytdlp     yt-dlp 统一封装（cookie 自动注入、UA、重试、友好错误）
  cookies   零配置浏览器 cookie 探测（B 站字幕与抖音分享页都依赖登录态）
  asr       可插拔音频转录后端（mlx-whisper 优先，funasr 兜底）
  funasr    SenseVoice-Small 后端实现
  vtt       字幕解析（vtt + srt 双格式）与时间轴抽取
  douyin    抖音分享页取流（yt-dlp 对 douyin.com 稳定 403，必须走 iesdouyin 直链）
"""
