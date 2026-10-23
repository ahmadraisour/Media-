import asyncio, os
from playwright.async_api import async_playwright
async def main():
    os.makedirs('f',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+os.getcwd()+'/demo.html'); await pg.evaluate('document.fonts.ready')
        await pg.evaluate('Promise.all([].slice.call(document.images).map(i=>i.decode()))')
        for k in range(99):
            await pg.evaluate(f'frame({k/30})'); await pg.screenshot(path=f'f/{k:03d}.jpg',type='jpeg',quality=92)
        await b.close()
asyncio.run(main())
