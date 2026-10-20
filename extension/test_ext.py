"""Developer check (Jason does not need this; needs: pip install playwright). Start board.py first, then: python test_ext.py
Loads the extension in a headless Chromium with FAKE ESPN cookies and walks popup -> Send -> setup page -> Save, checks the URL is scrubbed and the board never echoes the cookies."""
import asyncio, hashlib, os, sys
from playwright.async_api import async_playwright

EXT = os.path.abspath(os.path.dirname(__file__))   # this folder
FAKE_SWID = "{ABCDEF12-3456-7890-ABCD-EF1234567890}"
FAKE_S2 = "AEB" + "x" * 300 + "%2Fabc%3D"   # long, url-encoded like the real one


def ext_id(path):  # Chrome derives an unpacked extension's id from its absolute path
    h = hashlib.sha256(path.encode("utf-8")).hexdigest()[:32]
    return "".join(chr(ord("a") + int(c, 16)) for c in h)


async def main():
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            "/tmp/pwprofile", headless=True, channel="chromium",
            args=[f"--disable-extensions-except={EXT}", f"--load-extension={EXT}"])
        await ctx.add_cookies([
            {"name": "SWID", "value": FAKE_SWID, "domain": ".espn.com", "path": "/", "secure": True},
            {"name": "espn_s2", "value": FAKE_S2, "domain": ".espn.com", "path": "/", "secure": True, "httpOnly": True},
        ])
        eid = ext_id(EXT)
        pop = await ctx.new_page()
        pop.on("console", lambda m: print("  popup console:", m.text))
        await pop.goto(f"chrome-extension://{eid}/popup.html")
        await pop.wait_for_selector("#s_ready:not([hidden])", timeout=5000)
        print("popup state: ready")
        print("  swid shown:", await pop.text_content("#v_swid"))
        print("  s2 shown:  ", await pop.text_content("#v_s2"))
        await pop.screenshot(path="popup.png")
        await pop.fill("#addr", "http://localhost:8765/setup")   # messy input on purpose
        async with ctx.expect_page() as newp:
            await pop.click("#b_send")
        page = await newp.value
        page.on("console", lambda m: print("  setup console:", m.text))
        await page.wait_for_load_state("domcontentloaded")
        await page.wait_for_timeout(800)
        print("setup url after receive:", page.url)
        assert page.url.endswith("/setup"), "fragment not scrubbed"
        vis = await page.is_visible("#extcard")
        print("receive card visible:", vis)
        print("  who:", await page.text_content("#ext_who"))
        await page.screenshot(path="setup_receive.png", full_page=False)
        # Save -> hits /api/accounts/espn with fake cookies; ESPN will reject the list, but the account must be stored
        await page.click("text=Save and list my leagues")
        await page.wait_for_timeout(6000)
        print("  ext_msg:", await page.text_content("#ext_msg"))
        # The response must not echo the cookies
        resp = await page.evaluate("""async () => { const r = await fetch('/api/config'); return await r.json(); }""")
        print("accounts stored:", resp["accounts"])
        assert all("espn_s2" not in a and "swid" not in a for a in resp["accounts"])
        # not-signed-in state
        await ctx.clear_cookies()
        pop2 = await ctx.new_page()
        await pop2.goto(f"chrome-extension://{eid}/popup.html")
        await pop2.wait_for_selector("#s_nologin:not([hidden])", timeout=5000)
        print("popup state with no cookies: not signed in (ok)")
        await pop2.screenshot(path="popup_nologin.png")
        await ctx.close()
        print("ALL OK")

asyncio.run(main())
