import asyncio, os
from playwright.async_api import async_playwright
JOBS=[('نفس الطريق…<br>واحد بسنتين<em>وواحد بعشرين</em>','cover-tpl3-a'),
      ('ما بحب اشتغل<br>مع الأذكيا…<em>وهاد هو السبب</em>','cover-tpl3-b')]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+os.getcwd()+'/cover2.html'); await pg.evaluate('document.fonts.ready'); await pg.wait_for_timeout(500)
        for h,n in JOBS:
            await pg.evaluate(f'set({h!r})'); await pg.wait_for_timeout(300); await pg.screenshot(path=n+'.png')
        await b.close()
asyncio.run(main())
