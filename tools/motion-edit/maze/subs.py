import json
d=json.load(open('../mg/subs.json',encoding='utf-8'))
W=d['words']; C=d['chunks']
def mp(t):
    if t<22.1: return t
    if 43.6<=t<43.72: return 43.72-4.6533
    if 25.86<=t<42.64: return t-3.5933
    if t>=43.72: return t-4.6533
    return None
FIX={(3.32,'وإنت'):'وقت',(13.21,'تحلها'):'حلّها',(36.24,'عراحها'):'عالرايحة',(36.74,'وجاي'):'والجاية'}
new=[];idx={}
for i,(a,b,w) in enumerate(W):
    m=mp(a)
    if m is None: continue
    w=FIX.get((a,w),w)
    idx[i]=len(new); new.append([round(m,3),round(mp(b) if mp(b) is not None else m+0.3,3),w])
ch=[]
for c in C:
    k=[idx[i] for i in c if i in idx]
    if k: ch.append(k)
json.dump({'words':new,'chunks':ch},open('subs3.json','w'),ensure_ascii=False)
print(len(W),len(new)); print(' '.join(w[2] for w in new))
