import asyncio, os
from playwright.async_api import async_playwright
async def main():
    os.makedirs('mz',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+os.getcwd()+'/maze.html')
        for k in range(int(30*2.4)):
            await pg.evaluate(f'frame({k/30})'); await pg.screenshot(path=f'mz/{k:04d}.jpg',type='jpeg',quality=92)
        await b.close()
asyncio.run(main())
