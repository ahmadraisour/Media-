import subprocess, numpy as np, os
FPS=30; DUR=47.8; N=int(FPS*DUR)
SC=[(3.32,6.62),(7.42,10.10),(15.90,17.40),(19.00,20.72),(24.39,27.36),(28.78,31.77),(31.77,33.51),(34.72,37.32)]
m=np.zeros(N)
for a,b in SC:
    for k in range(N):
        t=k/FPS
        v=0
        if a-0.28<=t<a: v=(t-(a-0.28))/0.28
        if b<=t<b+0.4: v=max(v,1-(t-b)/0.4)
        m[k]=max(m[k],v)
os.makedirs('mask',exist_ok=True)
raw=np.repeat((m*255).astype(np.uint8),16*16).reshape(N,16,16)
raw.tofile('mask/m.gray')
subprocess.run(['ffmpeg','-v','error','-y','-f','rawvideo','-pix_fmt','gray','-s','16x16','-r',str(FPS),'-i','mask/m.gray','-vf','scale=1080:1920','-c:v','libx264','-crf','10','-pix_fmt','yuv420p','mask/mask.mp4'],check=True)
fc=("[0:v]split[b0][b1];[b1]gblur=sigma=28[bl];[1:v]format=gray[mk];[bl][mk]alphamerge[ba];[b0][ba]overlay=format=auto[v1];"
    "[2:v]setpts=PTS-STARTPTS+34.72/TB,format=yuva420p,fade=in:st=34.72:d=0.2:alpha=1,fade=out:st=37.12:d=0.2:alpha=1[mz];"
    "[v1][mz]overlay=enable='between(t,34.72,37.32)':eof_action=pass[v2];[v2][3:v]overlay=0:0:format=auto[out]")
subprocess.run(['ffmpeg','-y','-v','error','-i','base3.mp4','-i','mask/mask.mp4','-i','maze_broll.mp4','-framerate',str(FPS),'-i','fr/%05d.png',
  '-filter_complex',fc,'-map','[out]','-map','0:a','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p','-c:a','aac','-b:a','192k',
  '-t',str(DUR),'-movflags','+faststart','maze-motion-v11.mp4'],check=True)
print('ok')
