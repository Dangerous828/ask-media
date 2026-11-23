#!/usr/bin/env python3
"""grab — 公众号 / X 文章快速抓取，落盘为 Markdown。

用法:
  grab <url> [<url> ...]          抓取并保存到 ~/Articles
  grab -o DIR <url>               指定输出目录
  grab -p <url>                   只打印到终端，不存盘
  grab --stdout <url>             正文输出到 stdout（管道用）

支持:
  mp.weixin.qq.com  微信公众号（自动解短链、跟随跳转、图片改真链）
  x.com / twitter.com  单条推文或 X Article（走 fxtwitter 免登录接口）
  其它任意网页      通用正文提取（trafilatura）

仅用标准库 + 可选 bs4/trafilatura。
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime

# 微信只认"浏览器/微信内"的 UA。用 curl 默认 UA 会 302 到空壳，
# 所以这里必须给一个完整桌面 Chrome UA。
BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
)

DEFAULT_DIR = os.path.expanduser("~/Articles")


def http_get(url, timeout=25, retries=2):
    """带重试的 GET，返回 (HTML文本, 最终URL)。"""
    last = None
    for i in range(retries + 1):
        try:
            req = urllib.request.Request(
                url,
                headers={
                    "User-Agent": BROWSER_UA,
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
                    "Accept-Encoding": "identity",
                },
            )
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read()
                enc = r.headers.get_content_charset() or "utf-8"
                return raw.decode(enc, errors="ignore"), r.geturl()
        except Exception as e:  # noqa: BLE001
            last = e
            if i < retries:
                time.sleep(1.5 * (i + 1))
    raise RuntimeError(f"请求失败: {last}")


# ---------------------------------------------------------------- 微信
def fetch_wechat(url):
    html, final_url = http_get(url)

    if "wappoc_appmsgcaptcha" in final_url or (
        "环境异常" in html and "js_content" not in html
    ):
        raise RuntimeError(
            "被微信环境校验拦到验证页。多半是链接缺 chksm/poc_token 等分享参数——"
            "请在微信里用「···→复制链接」取完整链接再试；或等几分钟换网络重试。"
        )
    if "该内容已被发布者删除" in html or "此内容因违规无法查看" in html:
        raise RuntimeError("文章已删除或违规，无法获取。")

    try:
        from bs4 import BeautifulSoup
    except ImportError:
        raise RuntimeError("需要 beautifulsoup4：uv tool install --with beautifulsoup4 --with lxml grab")

    soup = BeautifulSoup(html, "lxml")
    node = soup.find(id="js_content")
    if node is None:
        raise RuntimeError("页面里没有正文节点（可能需在微信内打开的受限文章）。")

    title_el = soup.find(id="activity-name") or soup.find("h1")
    title = title_el.get_text(strip=True) if title_el else "未命名"
    author_el = soup.find(id="js_name")
    author = author_el.get_text(strip=True) if author_el else ""
    date_el = soup.find(id="publish_time")
    pub = date_el.get_text(strip=True) if date_el else ""

    # 图片懒加载：真实地址在 data-src
    for img in node.find_all("img"):
        src = img.get("data-src") or img.get("src") or ""
        if src.startswith("//"):
            src = "https:" + src
        img["src"] = src

    # 按块级元素分段：微信正文是一大坨 div/section，直接 get_text("\n")
    # 会把每个排版换行都拆成一段，读起来全是碎行。这里改成块级收集。
    BLOCK = {"p", "section", "h1", "h2", "h3", "h4", "h5", "h6",
             "li", "blockquote", "pre", "table", "figure", "figcaption"}

    def block_text(el):
        """把一个块元素渲染成单段文本，行内 <br> 转为软换行。"""
        for br in el.find_all("br"):
            br.replace_with("\n")
        for im in el.find_all("img"):
            src = im.get("src", "")
            if src:
                im.replace_with(f"\n![]({src})\n")
            else:
                im.decompose()
        t = el.get_text("", strip=False)
        t = t.replace("\u200b", "").replace("\xa0", " ")
        t = re.sub(r"[ \t\u3000]{2,}", " ", t)
        return "\n".join(ln.strip() for ln in t.split("\n")).strip()

    parts, seen = [], set()
    for el in node.find_all(BLOCK):
        # 只取叶子块，跳过包含其它块的容器，避免重复
        if el.find(BLOCK) is not None and el.name in {"section", "div", "li", "blockquote", "table"}:
            continue
        t = block_text(el)
        if t and t not in seen:
            parts.append(t)
            seen.add(t)

    if not parts:
        parts = [block_text(node)]

    text = "\n\n".join(parts)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()

    # 末尾的"点赞/在看/留言"导航噪声
    text = re.sub(r"\n*(轻点两下取消赞|轻点两下取消在看|预览时标签不可点|继续滑动看下一个)"
                  r"[\s\S]*$", "", text).strip()

    meta = {"source": "wechat", "author": author, "publish_time": pub, "url": url}
    return title, text, meta


# ---------------------------------------------------------------- X
def fetch_x(url):
    m = re.search(r"(?:x|twitter)\.com/([^/]+)/status/(\d+)", url)
    if not m:
        raise RuntimeError("无法识别的 X 链接（需要 .../status/<id>）")
    user, tid = m.group(1), m.group(2)

    data = json.loads(http_get(f"https://api.fxtwitter.com/{user}/status/{tid}")[0])
    if data.get("code") != 200 or not data.get("tweet"):
        raise RuntimeError(f"fxtwitter 取不到该推文: {data.get('message')}")

    t = data["tweet"]
    au = t.get("author") or {}
    handle = au.get("screen_name") or user
    name = au.get("name") or handle
    text = t.get("text") or ""

    # 长文（X Article）正文在 article 字段里
    art = t.get("article") or {}
    if art.get("title") or art.get("plain_text") or art.get("preview_text"):
        head = f"# {art.get('title','')}\n\n" if art.get("title") else ""
        text = head + (art.get("plain_text") or art.get("preview_text") or text)

    media = [mm.get("url") for mm in ((t.get("media") or {}).get("all") or []) if mm.get("url")]
    if media:
        text += "\n\n---\n\n**媒体**\n" + "\n".join(f"![]({u})" for u in media)

    quotes = t.get("quote")
    if quotes and quotes.get("text"):
        text += f"\n\n> 引用 @{(quotes.get('author') or {}).get('screen_name','')}:\n> " + \
                quotes["text"].replace("\n", "\n> ")

    # 文件名用推文正文开头更容易辨认，标题行保留作者
    snippet = re.sub(r"\s+", " ", text).strip()[:28]
    title = f"@{handle}_{snippet}" if snippet else f"@{handle}"
    meta = {
        "source": "x",
        "author": f"{name} @{handle}".strip(),
        "publish_time": t.get("created_at", ""),
        "url": url,
    }
    return title, text, meta


# ---------------------------------------------------------------- 通用
def fetch_generic(url):
    html, _ = http_get(url)
    text = ""
    title = ""

    try:
        import trafilatura
        text = trafilatura.extract(html, include_links=True, include_images=False,
                                   favor_recall=True) or ""
        md = trafilatura.extract_metadata(html)
        if md:
            title = md.title or ""
    except ImportError:
        pass

    if not text:
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "lxml")
            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()
            title = title or (soup.title.get_text(strip=True) if soup.title else "")
            container = soup.find("article") or soup.find("main") or soup.body
            text = container.get_text("\n") if container else ""
            text = re.sub(r"\n{3,}", "\n\n", text).strip()
        except ImportError:
            raise RuntimeError("需要 trafilatura 或 beautifulsoup4")

    if not text:
        raise RuntimeError("未能提取正文")

    return title or url, text, {"source": "web", "author": "", "publish_time": "", "url": url}


# ---------------------------------------------------------------- 落盘
def safe_name(s, n=60):
    s = re.sub(r'[\\/:*?"<>|\n\r\t]', "", s).strip()
    s = re.sub(r"\s+", " ", s)
    return (s[:n] or "untitled").strip()


def save(title, text, meta, outdir):
    os.makedirs(outdir, exist_ok=True)
    today = datetime.now().strftime("%Y-%m-%d")
    fname = f"{today}_{safe_name(title)}.md"
    path = os.path.join(outdir, fname)
    i = 2
    while os.path.exists(path):
        path = os.path.join(outdir, f"{today}_{safe_name(title)}_{i}.md")
        i += 1

    fm = [f"title: {title}", f"source: {meta.get('source')}"]
    if meta.get("author"):
        fm.append(f"author: {meta['author']}")
    if meta.get("publish_time"):
        fm.append(f"publish_time: {meta['publish_time']}")
    fm += [f"url: {meta['url']}", f"fetched_at: {datetime.now().isoformat(timespec='seconds')}",
           f"chars: {len(text)}"]

    with open(path, "w", encoding="utf-8") as f:
        f.write("---\n" + "\n".join(fm) + "\n---\n\n")
        f.write(f"# {title}\n\n{text}\n")
    return path


def route(url):
    u = url.strip()
    if "mp.weixin.qq.com" in u:
        return fetch_wechat
    if re.search(r"(?:^|//|www\.|mobile\.)(x|twitter)\.com/", u) and "/status/" in u:
        return fetch_x
    return fetch_generic


def main():
    ap = argparse.ArgumentParser(description="快速抓取公众号 / X / 网页文章为 Markdown")
    ap.add_argument("urls", nargs="+")
    ap.add_argument("-o", "--out", default=DEFAULT_DIR, help=f"输出目录（默认 {DEFAULT_DIR}）")
    ap.add_argument("-p", "--print", action="store_true", help="只打印不存盘")
    ap.add_argument("--stdout", action="store_true", help="正文输出到 stdout")
    ap.add_argument("--delay", type=float, default=2.0, help="多链接抓取间隔秒（默认 2）")
    args = ap.parse_args()

    ok = fail = 0
    for idx, url in enumerate(args.urls):
        if idx and args.delay:
            time.sleep(args.delay)
        try:
            title, text, meta = route(url)(url)
            if args.stdout or args.print:
                if args.stdout:
                    print(text)
                else:
                    print(f"\n{'='*70}\n# {title}\n{meta.get('author','')}  {meta.get('publish_time','')}"
                          f"\n{len(text)} 字\n{'='*70}\n{text}\n")
            if not (args.stdout or args.print):
                p = save(title, text, meta, args.out)
                print(f"✓ {len(text):>6} 字  {p}")
            ok += 1
        except Exception as e:  # noqa: BLE001
            print(f"✗ {url}\n  {e}", file=sys.stderr)
            fail += 1

    if len(args.urls) > 1:
        print(f"\n完成：成功 {ok} / 失败 {fail}", file=sys.stderr)
    return 0 if fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
