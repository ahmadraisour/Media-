import subprocess, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
# (image, start, end, motion)  motion: zin / zout / panup
CUTS=[('broll/b1.png',3.32,6.64,'zin'),
      ('broll/b2.png',7.64,10.30,'zout'),
      ('broll/b3.png',16.30,17.85,'zin'),
      ('broll/b4.png',32.95,36.74,'panup')]
MAZE=(38.40,40.80)
FPS=30
def kb(img,dur,motion,out):
    n=int(round(dur*FPS))+2
    if motion=='zin':  z=f"1+0.12*on/{n}"; x="iw/2-(iw/zoom/2)"; y="ih/2-(ih/zoom/2)"
    elif motion=='zout': z=f"1.14-0.12*on/{n}"; x="iw/2-(iw/zoom/2)"; y="ih/2-(ih/zoom/2)"
    else: z="1.12"; x="iw/2-(iw/zoom/2)"; y=f"(ih-ih/zoom)*(1-on/{n})"
    vf=(f"scale=2160:3840:force_original_aspect_ratio=increase,crop=2160:3840,"
        f"zoompan=z='{z}':x='{x}':y='{y}':d={n}:s=1080x1920:fps={FPS},"
        f"eq=contrast=1.04:saturation=1.05,format=yuv420p")
    subprocess.run(['ffmpeg','-y','-v','error','-loop','1','-i',img,'-vf',vf,'-frames:v',str(n),
                    '-c:v','libx264','-crf','16',out],check=True)
os.makedirs('kb',exist_ok=True)
ins=['-i','../vid1/reel-edit-v1.mp4']
for i,(img,s,e,m) in enumerate(CUTS):
    kb(img,e-s,m,f'kb/c{i}.mp4'); ins+=['-i',f'kb/c{i}.mp4']
ins+=['-i','maze_broll.mp4','-framerate',str(FPS),'-i','fr/%05d.png']
fc=[]; last='0:v'
allc=[(i+1,s,e) for i,(_,s,e,_) in enumerate(CUTS)]+[(5,MAZE[0],MAZE[1])]
for k,(idx,s,e) in enumerate(allc):
    # short 0.15s fade in/out on each cutaway
    d=e-s
    fc.append(f"[{idx}:v]setpts=PTS-STARTPTS+{s}/TB,format=yuva420p,"
              f"fade=in:st={s}:d=0.15:alpha=1,fade=out:st={e-0.15}:d=0.15:alpha=1[b{k}]")
    fc.append(f"[{last}][b{k}]overlay=enable='between(t,{s},{e})':eof_action=pass[v{k}]")
    last=f'v{k}'
fc.append(f"[{last}][6:v]overlay=0:0:format=auto[out]")
subprocess.run(['ffmpeg','-y','-v','error',*ins,'-filter_complex',';'.join(fc),
    '-map','[out]','-map','0:a','-c:v','libx264','-crf','17','-preset','medium','-pix_fmt','yuv420p',
    '-c:a','copy','-t','52.43','-movflags','+faststart','maze-motion-v2.mp4'],check=True)
subprocess.run(['ffmpeg','-y','-v','error','-i','maze-motion-v2.mp4','-c:v','libx264','-crf','24',
    '-preset','medium','-c:a','aac','-b:a','128k','-movflags','+faststart','maze-motion-v2-preview.mp4'],check=True)
print('ok')
