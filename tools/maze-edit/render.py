import asyncio, os, json, sys
from playwright.async_api import async_playwright
FPS=30; DUR=52.43; N=int(FPS*DUR)
async def main():
    d=json.load(open('subs.json',encoding='utf-8'))
    os.makedirs('fr',exist_ok=True)
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={'width':1080,'height':1920})
        await pg.goto('file://'+os.getcwd()+'/ov.html'); await pg.evaluate('document.fonts.ready')
        await pg.evaluate(f'init({json.dumps(d,ensure_ascii=False)})')
        only=[float(x) for x in sys.argv[1:]]
        frames=[int(x*FPS) for x in only] if only else range(N)
        for k in frames:
            await pg.evaluate(f'frame({k/FPS})')
            await pg.screenshot(path=f'fr/{k:05d}.png', omit_background=True)
        await b.close()
asyncio.run(main())
