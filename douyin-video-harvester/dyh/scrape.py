"""Stage 1 — scrape: open the profile in real Chromium with the user's douyin cookies and capture every
/aweme/v1/web/aweme/post/ JSON response while scrolling (Douyin signs these with a_bogus, so we let the page
sign them instead of calling the API directly)."""
import asyncio, os, re, shutil, urllib.parse
from . import log, io
from .cookies import load_douyin
from .errors import DyhError

API = "/aweme/v1/web/aweme/post/"
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/141.0.0.0 Safari/537.36")
SCROLL_JS = """()=>{const li=[...document.querySelectorAll('li')].filter(e=>e.querySelector('a[href*="/video/"]'));
if(li.length)li[li.length-1].scrollIntoView();
document.querySelectorAll('*').forEach(e=>{if(e.scrollHeight>e.clientHeight+50&&getComputedStyle(e).overflowY.match(/auto|scroll/))e.scrollTop=e.scrollHeight});
window.scrollTo(0,document.body.scrollHeight)}"""

def sec_uid_from(url_or_id):
    m = re.search(r"/user/([^/?#]+)", url_or_id)
    return m.group(1) if m else url_or_id.strip()

def _proxy():
    raw = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
    if not raw:
        return None
    u = urllib.parse.urlparse(raw)
    d = {"server": f"http://{u.hostname}:{u.port}"}
    if u.username:
        d.update(username=urllib.parse.unquote(u.username), password=urllib.parse.unquote(u.password or ""))
    return d

async def _run(cfg, sec_uid):
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        raise DyhError("E_DEP", "pip install playwright")
    if not shutil.which(cfg["chromium"]) and not os.path.exists(cfg["chromium"]):
        raise DyhError("E_DEP", f"chromium not found at {cfg['chromium']}")
    sc = cfg["scrape"]
    cookies = [dict(name=c["name"], value=c["value"], domain=c["domain"], path=c["path"], secure=c["secure"])
               for c in load_douyin(cfg["cookies"])]
    log.event("scrape", "cookies", count=len(cookies))
    items, state = {}, {"more": True, "pages": 0}
    async with async_playwright() as p:
        kw = dict(executable_path=cfg["chromium"], headless=True,
                  args=["--no-sandbox", "--disable-blink-features=AutomationControlled"])
        if cfg.get("proxy_from_env") and _proxy():
            kw["proxy"] = _proxy()
        b = await p.chromium.launch(**kw)
        ctx = await b.new_context(user_agent=UA, locale="zh-CN", viewport={"width": 1440, "height": 900})
        await ctx.add_cookies(cookies)
        pg = await ctx.new_page()

        async def on_resp(r):
            if API in r.url:
                try:
                    d = await r.json()
                except Exception as e:
                    log.event("scrape", "bad_response", status=r.status, err=str(e)[:100]); return
                for a in d.get("aweme_list") or []:
                    items[a["aweme_id"]] = a
                state["more"] = bool(d.get("has_more")); state["pages"] += 1
                log.event("scrape", "page", n=state["pages"], total=len(items), has_more=state["more"])
        pg.on("response", on_resp)
        await pg.goto(f"https://www.douyin.com/user/{sec_uid}?from_tab_name=main", timeout=60000)
        await pg.wait_for_timeout(sc["first_wait_ms"])
        stall, last = 0, 0
        for _ in range(sc["max_scrolls"]):
            await pg.evaluate(SCROLL_JS)
            await pg.mouse.move(800, 600); await pg.mouse.wheel(0, 3000)
            await pg.wait_for_timeout(sc["scroll_wait_ms"])
            stall = stall + 1 if len(items) == last else 0
            last = len(items)
            if (not state["more"] and state["pages"]) or stall > sc["stall_limit"]:
                break
        await pg.screenshot(path=os.path.join(cfg["run_dir"], "scrape_last.png"))
        await b.close()
    return list(items.values()), state

def run(cfg, profile):
    sec = sec_uid_from(profile)
    os.makedirs(cfg["run_dir"], exist_ok=True)
    items, state = asyncio.run(_run(cfg, sec))
    if not items:
        raise DyhError("E_SCRAPE_EMPTY", f"sec_uid={sec}; see {cfg['run_dir']}/scrape_last.png")
    try:  # merge with a previous partial scrape of the same run
        prev = io.read(cfg, "awemes")
        merged = io.by_id(prev); merged.update(io.by_id(items)); items = list(merged.values())
    except DyhError:
        pass
    io.write(cfg, "awemes", items)
    author = (items[0].get("author") or {}).get("nickname", "")
    log.event("scrape", "done", sec_uid=sec, author=author, total=len(items), complete=not state["more"])
    if state["more"]:
        log.get("scrape").warning("E_SCRAPE_PARTIAL: stalled with has_more=true; rerun to top up (results merge by aweme_id)")
    return items
