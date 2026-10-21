import sys, numpy as np, onnxruntime as ort
from PIL import Image
src, model, out = sys.argv[1], sys.argv[2], sys.argv[3]
im = Image.open(src).convert('RGB'); W,H = im.size
x = np.asarray(im.resize((1024,1024) if 'isnet' in model else (320,320), Image.LANCZOS)).astype(np.float32)/255.
if 'isnet' in model: x = (x-0.5)/1.0
else: x = (x-np.array([0.485,0.456,0.406]))/np.array([0.229,0.224,0.225])
x = x.transpose(2,0,1)[None].astype(np.float32)
s = ort.InferenceSession(model, providers=['CPUExecutionProvider'])
m = s.run(None, {s.get_inputs()[0].name: x})[0][0][0]
m = (m-m.min())/(m.max()-m.min()+1e-8)
mask = Image.fromarray((m*255).astype(np.uint8)).resize((W,H), Image.LANCZOS)
rgba = im.copy(); rgba.putalpha(mask); rgba.save(out)
