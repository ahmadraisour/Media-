import os, subprocess, asyncio, shutil
from playwright.async_api import async_playwright
B = os.path.dirname(os.path.abspath(__file__))
JOBS = [('car3','mentor-1c'),('car4','onepct-1c'),('car6','proverbs7-1c'),('car7','geo-1c')]
FPS, DUR = 30, 4.0
async def main():
    async with async_playwright() as p:
        b = await p.chromium.launch()
        for d, name in JOBS:
            D = f'{B}/{d}'
            pg = await b.new_page(viewport={'width':1080,'height':1350})
            await pg.goto('file://'+D+'/slide.html')
            await pg.evaluate('document.fonts.ready')
            await pg.evaluate('setup(0)')
            await pg.wait_for_timeout(400)
            await pg.evaluate('document.fonts.ready')
            # text visible from the very first frame; line animation untouched
            await pg.evaluate("document.querySelectorAll('.f').forEach(e=>e.dataset.t='-1')")
            fd = f'{D}/cover_frames'; shutil.rmtree(fd, ignore_errors=True); os.makedirs(fd)
            for k in range(int(FPS*DUR)):
                await pg.evaluate(f'frame({k/FPS})')
                await pg.screenshot(path=f'{fd}/{k:04d}.jpg', type='jpeg', quality=95)
            shutil.copy(f'{fd}/0000.jpg', f'{B}/check_{name}.jpg')
            subprocess.run(['ffmpeg','-y','-loglevel','error','-framerate',str(FPS),'-i',f'{fd}/%04d.jpg',
              '-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-movflags','+faststart',f'{D}/send/{name}.mp4'],check=True)
            await pg.close()
        await b.close()
asyncio.run(main())
