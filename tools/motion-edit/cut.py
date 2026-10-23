import sys, numpy as np, onnxruntime as ort
from PIL import Image, ImageFilter
import os
M=os.environ.get('U2NET','u2net_human_seg.onnx')  # model: github.com/danielgatis/rembg releases, tag v0.0.0
s=ort.InferenceSession(M,providers=['CPUExecutionProvider'])
for src,dst in zip(sys.argv[1::2],sys.argv[2::2]):
    im=Image.open(src).convert('RGB'); W,H=im.size
    x=np.asarray(im.resize((320,320),Image.LANCZOS)).astype(np.float32)/255.
    x=(x-[0.485,0.456,0.406])/[0.229,0.224,0.225]; x=x.transpose(2,0,1)[None].astype(np.float32)
    o=s.run(None,{s.get_inputs()[0].name:x})[0][0,0]; o=(o-o.min())/(o.max()-o.min()+1e-8)
    m=Image.fromarray((o*255).astype(np.uint8)).resize((W,H),Image.LANCZOS).filter(ImageFilter.GaussianBlur(1.2))
    im.putalpha(m); im.save(dst)
