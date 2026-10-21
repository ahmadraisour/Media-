import asyncio
from playwright.async_api import async_playwright
JOBS=[('maze2.jpg','هاي مو متاهة…<br>هاي <em>حياتك إنت</em>','cover-maze-v2'),
      ('serious.jpg','نفس الطريق…<br>واحد بسنتين<br>و<em>واحد بعشرين سنة</em>','cover-r1-v2')]
async def main():
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        import os; await pg.goto('file://'+os.getcwd()+'/cover.html'); await pg.evaluate('document.fonts.ready')
        for img,h,n in JOBS:
            await pg.evaluate(f'set({img!r},{h!r})'); await pg.wait_for_timeout(400); await pg.evaluate('document.fonts.ready')
            await pg.screenshot(path=n+'.png')
        await b.close()
asyncio.run(main())
