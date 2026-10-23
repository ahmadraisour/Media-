import cv2, numpy as np, sys
src,cut,out=sys.argv[1:4]
im=cv2.imread(src); a=cv2.imread(cut,cv2.IMREAD_UNCHANGED)[:,:,3]
m=cv2.dilate((a>40).astype(np.uint8)*255,np.ones((35,35),np.uint8))
s=0.35; ims=cv2.resize(im,None,fx=s,fy=s); ms=cv2.resize(m,(ims.shape[1],ims.shape[0]))
r=cv2.inpaint(ims,ms,15,cv2.INPAINT_TELEA); r=cv2.resize(r,(im.shape[1],im.shape[0]),interpolation=cv2.INTER_CUBIC)
mm=cv2.GaussianBlur(m,(41,41),0)[:,:,None]/255.
cv2.imwrite(out,(im*(1-mm)+r*mm).astype(np.uint8),[cv2.IMWRITE_JPEG_QUALITY,94])
