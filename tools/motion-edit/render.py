"""رسم الطبقة الشفافة فريم فريم.

python3 render.py projects/maze                 # كل الفريمات (بيكمّل من وين وقف)
python3 render.py projects/maze --at 9.2 9.4    # أوقات محددة للفحص
python3 render.py projects/maze --from 60 --to 90   # مقطع (ثواني)
خيارات: --workers N (افتراضي عدد المعالجات)، --force (يعيد الرسم حتى لو الفريم موجود)، --work DIR
الفريمات بتنحفظ بـ<work>/fr/%05d.png، و<work> افتراضياً /home/claude/work/<اسم المشروع>.
"""
import asyncio, os, json, sys, argparse, time
from multiprocessing import Process
from playwright.async_api import async_playwright

HERE = os.path.dirname(os.path.abspath(__file__))


def load(proj):
    cfg = json.load(open(os.path.join(proj, 'project.json'), encoding='utf-8'))
    subs = json.load(open(os.path.join(proj, cfg.get('subs', 'subs.json')), encoding='utf-8'))
    return cfg, subs


def workdir(proj, w=None):
    d = w or os.path.join('/home/claude/work', os.path.basename(os.path.abspath(proj)))
    os.makedirs(os.path.join(d, 'fr'), exist_ok=True)
    return d


async def run(cfg, subs, frames, fr):
    fps = cfg['fps']
    async with async_playwright() as p:
        b = await p.chromium.launch()
        pg = await b.new_page(viewport={'width': 1080, 'height': 1920})
        await pg.goto('file://' + os.path.join(HERE, 'engine.html'))
        await pg.evaluate('document.fonts.ready')
        await pg.evaluate(f'init({json.dumps(cfg, ensure_ascii=False)},{json.dumps(subs, ensure_ascii=False)})')
        await pg.evaluate('ready()')
        for k in frames:
            await pg.evaluate(f'frame({k / fps})')
            await pg.screenshot(path=os.path.join(fr, f'{k:05d}.png'), omit_background=True)
        await b.close()


def worker(cfg, subs, frames, fr):
    asyncio.run(run(cfg, subs, frames, fr))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('proj')
    ap.add_argument('--at', nargs='*', type=float)
    ap.add_argument('--from', dest='t0', type=float, default=0)
    ap.add_argument('--to', dest='t1', type=float)
    ap.add_argument('--workers', type=int, default=os.cpu_count() or 2)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--work')
    a = ap.parse_args()
    cfg, subs = load(a.proj)
    fr = os.path.join(workdir(a.proj, a.work), 'fr')
    fps = cfg['fps']; N = int(fps * cfg['dur'])
    if a.at:
        frames = [int(round(x * fps)) for x in a.at]
        a.force = True
    else:
        k1 = N if a.t1 is None else min(N, int(round(a.t1 * fps)))
        frames = list(range(int(round(a.t0 * fps)), k1))
    if not a.force:
        frames = [k for k in frames if not os.path.exists(os.path.join(fr, f'{k:05d}.png'))]
    if not frames:
        print('nothing to render'); return
    n = max(1, min(a.workers, len(frames)))
    # كل عامل بياخد قطعة متصلة (أسرع للمشاهد اللي فيها حالة)
    size = -(-len(frames) // n)
    parts = [frames[i:i + size] for i in range(0, len(frames), size)]
    t = time.time()
    ps = [Process(target=worker, args=(cfg, subs, part, fr)) for part in parts]
    [p.start() for p in ps]; [p.join() for p in ps]
    bad = [p.exitcode for p in ps if p.exitcode]
    if bad:
        sys.exit(f'worker failed: {bad}')
    print(f'{len(frames)} frames in {time.time() - t:.0f}s -> {fr}')


if __name__ == '__main__':
    main()
