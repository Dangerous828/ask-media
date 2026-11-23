---
name: grab-article
version: 1.0.2
kind: agent-skill
entrypoint: SKILL.md
summary: 抓取微信公众号 / X(推特) / 任意网页文章正文并转成 Markdown，免登录、免 cookie、免浏览器，也不依赖第三方 SaaS
description: 快速抓取微信公众号 / X(推特) / 任意网页文章正文为 Markdown，不需要登录、不需要 cookie、不需要浏览器，也不走第三方 SaaS。用户发来文章链接说"帮我抓一下/存下来/看这篇/总结这篇"时用它。
whenToUse: 用户给出 mp.weixin.qq.com、x.com/twitter.com 或任意文章 URL，要求抓正文、存 Markdown、喂给 AI 分析。不用于视频/音频（归 shortvideo-understand），不用于图片集。
license: MIT
---

# 抓取文章正文

## 目标

把一条文章链接变成干净、可读、可直接喂给模型的 Markdown。做完的状态：正文完整（公众号通常 2000–10000 字）、段落分明、图片是能打开的真实地址、开头有 title/author/url 等元信息。

不为抓一篇文章去装 Playwright / Selenium，也不找第三方采集服务——那些方案的维护成本远高于它解决的问题。

## 执行流程

1. **认链接**。`mp.weixin.qq.com` → 微信；含 `/status/` 的 `x.com`/`twitter.com` → X；其余走通用提取。
2. **抓**。`grab <url>` 直接存盘到 `~/Articles/`；要接管道或喂模型用 `grab --stdout <url>`；只看不留用 `-p`。
3. **验**。看输出字数。几百字就是被拦了，别当成"文章很短"。
4. **报**。告诉用户存到哪、多少字。被拦就照下面的坑排查，不要换工具硬试。

脚本随本 skill 一起分发，在 `scripts/grab.py`：标准库即可跑，微信正文解析另需 bs4+lxml。终端上若已有 `~/.local/bin/grab` 直接用它，没有就调仓库里的：

```bash
grab <url> [<url> ...]         # 存到 ~/Articles/<日期>_<标题>.md
grab -o ~/Documents/文章 <url>  # 换目录
grab --stdout <url>             # 正文打到 stdout
grab -p <url>                   # 只在终端看

python3 scripts/grab.py <url>
# 依赖不足时：
# uv tool install --with beautifulsoup4 --with lxml --with trafilatura \
#   --from scripts/grab.py grab
```

多链接默认间隔 2 秒（`--delay` 可调）。

## 各来源的实际行为（已实测）

| 来源 | 方式 | 说明 |
|---|---|---|
| 微信公众号 | 直取 HTML 抓 `#js_content` | 桌面 Chrome UA 即可，**不需要微信用 UA** |
| X / Twitter | `api.fxtwitter.com` 免登录接口 | 支持长推文、X Article、引用推、媒体图 |
| 其它网页 | trafilatura，失败退回 bs4 | 通用正文提取 |

## 微信的两个坑（这是关键）

1. **必须带完整分享参数。** 形如
   `https://mp.weixin.qq.com/s?__biz=...&mid=...&idx=1&sn=...`
   只有这四个参数会被踢到 `wappoc_appmsgcaptcha` 验证页；带上 `&chksm=...`
   就直接是正文。短链 `mp.weixin.qq.com/s/xxxxxxxx` 一直好使。
   → **正确取法：在微信里点「···」→「复制链接」，粘全，别手抄。**
2. **绝不能伪装成微信客户端。** UA 里带 `MicroMessenger` 反而会 302 到空壳页；
   用普通桌面 Chrome UA 才是通的。

正文在 `#js_content`，trafilatura/readability 这类通用提取器对微信页会返回空或验证页正文，必须按块级元素自己分段。频率上别猛：一篇间隔 2 秒够用。

## 调用契约

输入：一个或多个 URL（微信文章、X 推文、任意网页），来自用户粘贴。

输出：

- 默认：`~/Articles/<日期>_<标题>.md`，带 frontmatter（title / source / author / publish_time / url / fetched_at / chars）。
- `--stdout`：纯正文到 stdout，供管道或后续分析使用。
- `-p`：只打印不落盘。
- 多链接：每篇一行结果 + 末尾成功/失败计数；单篇失败不影响其余。

不做什么：不追公众号历史文章列表、不订阅、不定时归档、不做全文转载发布。

## 安全与权限边界

只访问用户给出的 URL，只写 `~/Articles/`（或 `-o` 指定目录），不碰其它路径。不带 cookie、不带登录态、不做 IP 轮换或代理池。爬取有版权与平台条款风险：只用于个人阅读、分析与存档，不整篇搬运再发布。

## 自检

- 字数对得上吗？公众号几百字 = 被拦，不是文章短。
- 有 frontmatter 且 url 是用户给的那条吗？
- 图片链接是 `mmbiz.qpic.cn` 这类真实地址，不是 `data-src` 占位吗？
- 报错信息是明确原因（验证页/已删除/无正文节点），不是"失败"两个字吗？

## 边界

- 付费/需要登录才能看的公众号文章抓不到，别硬试。
- 只抓正文做阅读、分析与临时存档；不接受长期定时归档类需求。
- 微信随时可能改策略。哪天全部被拦，先怀疑 UA 或新增参数，而不是脚本写错。

## 已被否掉的方案（别再提）

`wewe-rss`（2026-05-11 归档）、`wechat-article-exporter`（2026-07-30 停维护，上游接口被官方关闭）、各类"Selenium 模拟登录 + 打码"流程。抓单篇或几十篇，本脚本就够，不需要任何常驻服务。
