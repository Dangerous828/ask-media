> 本页是渠道资料。短剧项目不直接执行这里的命令：TTS 一律经 `short-drama-produce` 的 `tts` 模态（预览→确认→运行记录），音色以 `short-drama-assets` 的声音方向为准，本页的音色表只作候选参考。

# TTS 渠道

## 1. 首选：Edge TTS（本机实测可用）

**优点**：免费、无需 key、中文自然、可调语速。**缺点**：微软接口会改 token 版本，需要较新的包。

### 安装与验证

```bash
pip3 install --upgrade edge-tts
python3 -m edge_tts --list-voices | grep zh-CN
```

**必须用 `python3 -m edge_tts`**，不要用 `~/.local/bin/edge-tts` 的旧入口（旧版会 403）。

### 中文音色

| 音色 | 性别 | 风格 | 适用 |
|---|---|---|---|
| `zh-CN-YunyangNeural` | 男 | News，专业可靠 | **冷静旁白、纪录片腔**（推荐） |
| `zh-CN-YunjianNeural` | 男 | Sports/Novel，激情 | 热血、体育解说 |
| `zh-CN-YunxiNeural` | 男 | Novel，活泼阳光 | 轻松、少年感 |
| `zh-CN-YunxiaNeural` | 男 | Cartoon，可爱 | 低龄向 |
| `zh-CN-XiaoxiaoNeural` | 女 | News/Novel，温暖 | 温柔旁白 |
| `zh-CN-XiaoyiNeural` | 女 | Cartoon/Novel，活泼 | 俏皮 |

### 生成命令

```bash
python3 -m edge_tts \
  --voice zh-CN-YunyangNeural \
  --rate=-8% \
  --text "小时候的我一直不明白，为什么这里是个选择。" \
  --write-media out.mp3
```

- `--rate`：语速，**建议 -8% ~ -12%** 做旁白（正常速偏快）
- `--volume`：音量，一般不用调
- 输出 mp3 24kHz 单声道，混音前建议转 48kHz 立体声

### 实测语速

`zh-CN-YunyangNeural` 在 `-8%` 下约 **4.4 字/秒**（含标点停顿），与 `writing-rules.md` §4 的核算表一致。

## 2. 备选：video-recap-skills 的多后端

外部技能 `video-recap-skills/video-voiceover` 支持三个后端，适合需要更高音质或声音克隆的场景：

| 后端 | 凭据 | 特点 |
|---|---|---|
| MiMo TTS（`mimo-v2.5-tts`） | `MIMO_API_KEY` | 支持情绪标签、可克隆音色；默认音色「冰糖」 |
| Fish Audio（`s2.1-pro-free`） | `FISH_API_KEY` | 免费模型无 SLA；数值语速控制 |
| 自托管 IndexTTS | `INDEX_TTS_ENDPOINT` | 完全本地，不外发文本 |

**注意外发**：MiMo 与 Fish 都会把旁白文本发到云端；`--voice-ref` 还会外发参考音频做克隆，需创作者授权。自托管 IndexTTS 不外发。

## 3. 本机不可用的路径

- **macOS `say`**：系统只装了英文语音，中文 `say -v Reed` 输出 0.016 秒空音频（语音包未下载）。要用得先在「系统设置 → 辅助功能 → 朗读内容」里下载中文语音。
- **`~/.local/bin/edge-tts` 旧入口**：403 拒绝。用 `python3 -m edge_tts`。

## 4. 混音注意

旁白音频混入成片时：

1. 转成与成片一致的采样率（48kHz）与声道数（立体声）
2. 旁白与台词**不重叠**；必须重叠时旁白压到 -12dB 以下
3. 混完后测整片 LUFS，并单独确认旁白区间可辨（`ffmpeg -ss <t> -t 0.5 -i out.mp4 -af volumedetect -f null -`）
4. 不要对已归一化的成片再做一次 loudnorm（会压到远低于目标）

## 5. 自检

- [ ] 已试听：音色是否贴合旁白身份（冷静/温情/活泼）
- [ ] 已核语速：实测字/秒 与时间窗核算表一致
- [ ] 已验时窗：每段音频时长 ≤ 目标窗口 - 0.45s
- [ ] 已确认外发：若用云端 TTS，创作者知道文本（与可能的音色参考）会外发
