#!/usr/bin/env python3
"""Verify a product landing page in headless Chromium (file:// or http(s)).

Usage:  verify.py <url> [--chat]
  <url>    file:///... or https://...
  --chat   also open the advisor and send a probe question (http mode only meaningful)

Checks: pageerrors, HTTP>=400 responses, broken <img>, FAB tab switch, chat panel open.
Screenshots: vfy_top.png vfy_fab.png vfy_gallery.png vfy_footer.png (cwd).
Requires playwright (workspace venv: ./venv/bin/python).
"""
import asyncio, sys
from playwright.async_api import async_playwright

async def main(url, do_chat):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1440, "height": 900})
        errors, bad = [], []
        page.on("pageerror", lambda e: errors.append(str(e)))
        page.on("response", lambda r: bad.append((r.status, r.url[:90])) if r.status >= 400 else None)
        await page.goto(url)
        await page.wait_for_timeout(2500)
        print("puter-dialog blocking:", await page.evaluate("!!document.querySelector('puter-dialog')"))
        await page.screenshot(path="vfy_top.png")
        tabs = page.locator(".system-tab")
        if await tabs.count() > 2:
            await tabs.nth(2).click()
            await page.wait_for_timeout(300)
            print("tab3 name:", (await page.text_content("#system-name") or "").strip())
        await page.screenshot(path="vfy_fab.png")
        if do_chat:
            await page.click("#chat-fab")
            await page.wait_for_timeout(300)
            print("chat visible:", await page.is_visible("#chat-panel"))
            msgs = await page.eval_on_selector_all(".chat-msg", "els => els.map(e => e.textContent.slice(0,90))")
            print("chat intro:", msgs[:1])
            await page.click("#chat-close")
        for sec, name in [("gallery", "gallery")]:
            if await page.locator(f"#{sec}").count():
                await page.evaluate(f"document.getElementById('{sec}').scrollIntoView()")
                await page.wait_for_timeout(500)
                await page.screenshot(path=f"vfy_{name}.png")
        broken = await page.eval_on_selector_all("img[src]", "els => els.filter(i => i.complete && i.naturalWidth===0).map(i => i.src)")
        await page.evaluate("document.querySelector('footer').scrollIntoView()")
        await page.wait_for_timeout(400)
        await page.screenshot(path="vfy_footer.png")
        print("broken images:", broken if broken else "none")
        print("http>=400:", bad if bad else "none")
        print("pageerrors:", errors[:5] if errors else "none")
        await browser.close()

if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]
    url = args[0]
    asyncio.run(main(url, "--chat" in args))
