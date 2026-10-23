"""التركيب النهائي على دفعات: كل مقطع (افتراضي 30 ثانية) لحاله، وبعدين وصل وصوت.

python3 comp.py projects/maze            # بيقرا <work>/<base> و<work>/fr و<work>/<broll>
خيارات: --seg 30 (طول المقطع بالثواني)، --work DIR، --out NAME
الطبقات بالترتيب: الفيديو المقصوص ← ضباب وجه أحمد حوالين المشاهد ← B-roll فيديو (broll) ← الطبقة الشفافة (fr).
"""
import subprocess, numpy as np, os, json, argparse, shutil

SIGMA = 28      # ضباب الوجه
PRE, POST = 0.28, 0.4   # الضباب بيبلّش قبل المشهد بـ0.28 ث وبيروح بعده بـ0.4 ث


def run(cmd):
    subprocess.run(cmd, check=True)


def mask_values(cfg, N):
    fps = cfg['fps']
    spans = [(s['a'], s['b']) for s in cfg.get('scenes', [])]
    spans += [(r['a'], r['b']) for r in cfg.get('broll', []) if r.get('blurFace', True)]
    t = np.arange(N) / fps
    m = np.zeros(N)
    for a, b in spans:
        v = np.zeros(N)
        i = (t >= a - PRE) & (t < a); v[i] = (t[i] - (a - PRE)) / PRE
        j = (t >= b) & (t < b + POST); v[j] = np.maximum(v[j], 1 - (t[j] - b) / POST)
        m = np.maximum(m, v)
    return m


def segment(cfg, wd, k0, k1, m, out):
    fps = cfg['fps']; n = k1 - k0; s0 = k0 / fps; s1 = k1 / fps
    raw = os.path.join(wd, 'mask', f'm{k0:05d}.gray')
    np.repeat((m[k0:k1] * 255).astype(np.uint8), 16 * 16).reshape(n, 16, 16).tofile(raw)
    ins = ['-ss', f'{s0:.6f}', '-i', os.path.join(wd, cfg['base']),
           '-f', 'rawvideo', '-pix_fmt', 'gray', '-s', '16x16', '-r', str(fps), '-i', raw]
    fc = (f"[1:v]scale=1080:1920,format=gray[mk];[0:v]split[b0][b1];[b1]gblur=sigma={SIGMA}[bl];"
          "[bl][mk]alphamerge[ba];[b0][ba]overlay=format=auto,format=yuv420p[v0]")  # yuv420p ضروري، بدونه الضباب بيطلع أخف
    cur, ix = 'v0', 2
    for r in cfg.get('broll', []):
        a, b, f = r['a'], r['b'], r.get('fade', 0.2)
        if b <= s0 or a >= s1:
            continue
        # الـB-roll بيتعبّى بفريمات شفافة من أول المقطع (tpad) حتى يمشي مع الفيديو من الثانية 0.
        # بـv11 كان setpts لحاله، وffmpeg كان يرمي فريمات من أوله: المتاهة بلّشت 0.37 ث بكير وراحت قبل وقتها.
        pre = max(0, a - s0)
        ins += (['-ss', f'{s0 - a:.6f}'] if a < s0 else []) + ['-i', os.path.join(wd, r['file'])]
        fc += (f";[{ix}:v]fps={fps},setpts=PTS-STARTPTS,format=yuva420p,tpad=start_duration={pre:.6f}:color=black@0,"
               f"fade=in:st={a - s0:.6f}:d={f}:alpha=1,fade=out:st={b - f - s0:.6f}:d={f}:alpha=1[r{ix}];"
               f"[{cur}][r{ix}]overlay=enable='between(t,{a - s0:.6f},{b - s0:.6f})':eof_action=pass[v{ix}]")
        cur = f'v{ix}'; ix += 1
    ins += ['-framerate', str(fps), '-start_number', str(k0), '-i', os.path.join(wd, 'fr', '%05d.png')]
    fc += f";[{cur}][{ix}:v]overlay=0:0:format=auto[out]"
    run(['ffmpeg', '-y', '-v', 'error', *ins, '-filter_complex', fc, '-map', '[out]', '-frames:v', str(n),
         '-c:v', 'libx264', '-crf', '17', '-preset', 'medium', '-pix_fmt', 'yuv420p', '-r', str(fps), out])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('proj')
    ap.add_argument('--seg', type=float, default=30)
    ap.add_argument('--work')
    ap.add_argument('--out')
    a = ap.parse_args()
    cfg = json.load(open(os.path.join(a.proj, 'project.json'), encoding='utf-8'))
    wd = os.path.abspath(a.work) if a.work else os.path.join('/home/claude/work', os.path.basename(os.path.abspath(a.proj)))
    fps = cfg['fps']; N = int(fps * cfg['dur'])
    miss = [k for k in range(N) if not os.path.exists(os.path.join(wd, 'fr', f'{k:05d}.png'))]
    if miss:
        raise SystemExit(f'{len(miss)} frames missing (first {miss[0]}); run render.py first')
    shutil.rmtree(os.path.join(wd, 'mask'), ignore_errors=True); os.makedirs(os.path.join(wd, 'mask'))
    sd = os.path.join(wd, 'seg'); shutil.rmtree(sd, ignore_errors=True); os.makedirs(sd)
    m = mask_values(cfg, N)
    step = int(round(a.seg * fps)); parts = []
    for k0 in range(0, N, step):
        k1 = min(N, k0 + step); p = os.path.join(sd, f'{k0:05d}.mp4')
        segment(cfg, wd, k0, k1, m, p); parts.append(p)
        print(f'segment {k0 / fps:.1f}-{k1 / fps:.1f}s ok', flush=True)
    lst = os.path.join(sd, 'list.txt')
    open(lst, 'w').write(''.join(f"file '{p}'\n" for p in parts))
    out = os.path.join(wd, a.out or cfg.get('out', 'out.mp4'))
    run(['ffmpeg', '-y', '-v', 'error', '-f', 'concat', '-safe', '0', '-i', lst, '-i', os.path.join(wd, cfg['base']),
         '-map', '0:v', '-map', '1:a', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
         '-t', str(cfg['dur']), '-movflags', '+faststart', out])
    print('ok ->', out)


if __name__ == '__main__':
    main()
