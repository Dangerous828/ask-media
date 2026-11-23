"""零配置 cookie 来源探测：自动选出「哪个浏览器登录过该平台」。

为什么需要：B 站的 AI 字幕与抖音分享页都要登录态 cookie 才可见。上游要求用户手工
export YTDLP_COOKIES_FROM_BROWSER=<浏览器名>，实际使用时没人会记得设，结果就是
「字幕永远抓不到、抖音永远被风控」。这里把选择交给探测：

  1. 显式环境变量优先（YTDLP_COOKIES_FROM_BROWSER / DOUYIN_COOKIES*），不覆盖用户选择；
  2. 否则扫描各浏览器的 cookie 数据库，看哪个域名下的 cookie 条数最多就用哪个；
  3. 全部拿不到就返回 None，调用方按无 cookie 处理（不报错、不中断）。

只读：把 DB 复制到临时目录再查（浏览器运行中会锁库），查完即删；不解密、不打印值。
"""

import glob
import os
import shutil
import sqlite3
import tempfile
import time

# 浏览器名 → cookie DB 路径模板（yt-dlp 认可的浏览器名作为 key）
_SPECS = {
    "brave": ["~/Library/Application Support/BraveSoftware/Brave-Browser/*/Cookies"],
    "chrome": ["~/Library/Application Support/Google/Chrome/*/Cookies"],
    "edge": ["~/Library/Application Support/Microsoft Edge/*/Cookies"],
    "chromium": ["~/Library/Application Support/Chromium/*/Cookies"],
    "firefox": ["~/Library/Application Support/Firefox/Profiles/*/cookies.sqlite"],
    "safari": ["~/Library/Cookies/Cookies.binarycookies"],
}

CACHE_TTL = 600  # 秒；探测结果（浏览器+条数）缓存 10 分钟，避免每次调用都复制库文件


def _cache_path(domain: str) -> str:
    base = os.path.expanduser("~/.cache/chubby-skills")
    os.makedirs(base, exist_ok=True)
    return os.path.join(base, "cookie-probe-" + "".join(c if c.isalnum() else "_" for c in domain))


def _read_cache(domain: str):
    p = _cache_path(domain)
    try:
        with open(p, encoding="utf-8") as f:
            ts, browser, count = f.read().split()
        if time.time() - float(ts) < CACHE_TTL:
            return browser or None, int(count)
    except (OSError, ValueError):
        pass
    return None, 0


def _write_cache(domain: str, browser: str, count: int) -> None:
    try:
        with open(_cache_path(domain), "w", encoding="utf-8") as f:
            f.write(f"{time.time():.0f} {browser} {count}\n")
    except OSError:
        pass


def _count_chromium(db: str, domain: str) -> int:
    """Chrome 系（Brave/Chrome/Edge）cookies 表。"""
    tmp = tempfile.mkdtemp(prefix="ck-")
    dst = os.path.join(tmp, "Cookies")
    try:
        shutil.copy2(db, dst)
        # 运行中的浏览器可能带 -wal/-shm，一起复制才能读到最新写入
        for ext in ("-wal", "-shm"):
            if os.path.isfile(db + ext):
                shutil.copy2(db + ext, dst + ext)
        con = sqlite3.connect("file:%s?mode=ro" % dst, uri=True)
        try:
            row = con.execute(
                "select count(*) from cookies where host_key like ?", (f"%{domain}%",)
            ).fetchone()
            return int(row[0]) if row else 0
        finally:
            con.close()
    except (OSError, sqlite3.Error):
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def _count_firefox(db: str, domain: str) -> int:
    """Firefox 用 moz_cookies 表，列名与 Chrome 系不同。"""
    tmp = tempfile.mkdtemp(prefix="ck-")
    dst = os.path.join(tmp, "cookies.sqlite")
    try:
        shutil.copy2(db, dst)
        con = sqlite3.connect("file:%s?mode=ro" % dst, uri=True)
        try:
            row = con.execute(
                "select count(*) from moz_cookies where host like ?", (f"%{domain}%",)
            ).fetchone()
            return int(row[0]) if row else 0
        finally:
            con.close()
    except (OSError, sqlite3.Error):
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def probe(domain: str, refresh: bool = False) -> list:
    """返回 [(浏览器名, cookie 条数), ...]，按条数降序。"""
    if not refresh:
        cached, count = _read_cache(domain)
        if cached:
            return [(cached, count)]

    found = []
    for browser, patterns in _SPECS.items():
        best = 0
        for pattern in patterns:
            for db in glob.glob(os.path.expanduser(pattern)):
                if browser == "safari":
                    # binarycookies 无法用 sqlite 读，仅看文件是否存在
                    n = 1 if os.path.getsize(db) > 0 else 0
                elif browser == "firefox":
                    n = _count_firefox(db, domain)
                else:
                    n = _count_chromium(db, domain)
                best = max(best, n)
        if best:
            found.append((browser, best))

    found.sort(key=lambda x: -x[1])
    if found:
        _write_cache(domain, found[0][0], found[0][1])
    return found


def resolve(domain: str, refresh: bool = False):
    """选出用于 --cookies-from-browser 的浏览器名；没探测到返回 None。

    环境变量 YTDLP_COOKIES_FROM_BROWSER 始终优先（用户显式指定不覆盖）。
    """
    forced = os.environ.get("YTDLP_COOKIES_FROM_BROWSER", "").strip()
    if forced:
        return forced
    found = probe(domain, refresh=refresh)
    return found[0][0] if found else None


def describe(domain: str) -> str:
    """给日志/排障用的一句话摘要。"""
    found = probe(domain)
    if not found:
        return f"未在本地浏览器找到 {domain} 的 cookie"
    return "，".join(f"{b}({n} 条)" for b, n in found[:3])
