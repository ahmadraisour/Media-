"""من ترجمة whisper (كلمة بكلمة) لـsubs.json تبع المحرك.

whisper-cli -m MODEL -f audio16k.wav -l ar -osrt -ml 1 -sow -of words
python3 subs_build.py words.srt projects/video1/subs.json [--fix fixes.json] [--gap 0.35] [--max 5]

- كلمات: [بداية، نهاية، نص]
- جمل الترجمة (chunks): بتنقسم على السكتة (> gap) أو علامة الترقيم أو حد الكلمات، مع تجنّب كلمة يتيمة بآخر الجملة.
- fixes.json: {"رقم_الكلمة": "التصحيح"} أو {"الكلمة الغلط": "الصح"}.
- بيطبع النص مع أرقام الكلمات، لاختيار beats المشاهد.
"""
import re, json, sys, argparse

JUNK = ['ترجمة نانسي قنقر', 'اشتركوا في القناة', 'شكرا للمشاهدة']
PUNCT = '.،,؟?!:؛'


def ts(s):
    h, m, r = s.replace(',', '.').split(':')
    return int(h) * 3600 + int(m) * 60 + float(r)


def read_srt(p):
    out = []
    for blk in re.split(r'\n\s*\n', open(p, encoding='utf-8').read().strip()):
        ln = blk.strip().splitlines()
        if len(ln) < 3 or '-->' not in ln[1]:
            continue
        a, b = [ts(x.strip()) for x in ln[1].split('-->')]
        w = ' '.join(ln[2:]).strip()
        if w:
            out.append([round(a, 3), round(b, 3), w])
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('srt'); ap.add_argument('out')
    ap.add_argument('--fix'); ap.add_argument('--gap', type=float, default=0.35)
    ap.add_argument('--max', type=int, default=5)
    a = ap.parse_args()
    W = read_srt(a.srt)
    txt = ' '.join(w[2] for w in W)
    for j in JUNK:
        if j in txt:
            print('dropping hallucinated line:', j)
            k = len(j.split())
            for i in range(len(W) - k + 1):
                if ' '.join(w[2] for w in W[i:i + k]) == j:
                    del W[i:i + k]; break
    # كلمات ملزوقة بعلامة ترقيم لحالها
    M = []
    for w in W:
        if all(c in PUNCT for c in w[2]) and M:
            M[-1][2] += w[2]; M[-1][1] = w[1]
        else:
            M.append(w)
    W = M
    if a.fix:
        fx = json.load(open(a.fix, encoding='utf-8'))
        for k, v in fx.items():
            if k.isdigit():
                W[int(k)][2] = v
            else:
                for w in W:
                    if w[2].strip(PUNCT) == k:
                        w[2] = w[2].replace(k, v)
    C, cur = [], []
    for i, w in enumerate(W):
        cur.append(i)
        nxt = W[i + 1] if i + 1 < len(W) else None
        brk = (nxt is None or nxt[0] - w[1] > a.gap or w[2][-1] in PUNCT or len(cur) >= a.max
               or len(' '.join(W[j][2] for j in cur)) > 30)
        # ما في كلمة يتيمة: إذا الجاي آخر كلمة قبل سكتة، خليه معنا
        if brk and nxt is not None and len(cur) >= a.max - 1 and nxt[0] - w[1] <= a.gap and w[2][-1] not in PUNCT:
            n2 = W[i + 2] if i + 2 < len(W) else None
            if n2 is None or n2[0] - nxt[1] > a.gap or nxt[2][-1] in PUNCT:
                if len(cur) < a.max + 1:
                    brk = False
        if brk:
            C.append(cur); cur = []
    if cur:
        C.append(cur)
    # الترجمة بتنعرض بلا علامات ترقيم
    words = [[w[0], w[1], w[2].strip(PUNCT) or w[2]] for w in W]
    json.dump({'words': words, 'chunks': C}, open(a.out, 'w', encoding='utf-8'), ensure_ascii=False)
    for c in C:
        print(f'{W[c[0]][0]:7.2f}  ' + '  '.join(f'{i}:{W[i][2]}' for i in c))
    print(len(W), 'words,', len(C), 'chunks ->', a.out)


if __name__ == '__main__':
    main()
