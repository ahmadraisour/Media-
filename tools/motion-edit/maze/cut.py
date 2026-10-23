import subprocess
S='../vid1/reel-edit-v1.mp4'
KEEP=[(0,22.24),(25.86,42.64),(43.72,52.43)]
parts=[]
for i,(a,b) in enumerate(KEEP):
    d=b-a; o=f'k{i}.mp4'
    subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{a}','-i',S,'-t',f'{d:.3f}','-af',f'afade=t=in:d=0.02,afade=t=out:st={d-0.03:.3f}:d=0.03',
      '-c:v','libx264','-crf','14','-preset','fast','-pix_fmt','yuv420p','-r','30','-c:a','aac','-b:a','192k','-ar','48000',o],check=True)
    parts.append(f"file '{o}'")
open('l.txt','w').write('\n'.join(parts))
subprocess.run(['ffmpeg','-v','error','-y','-f','concat','-safe','0','-i','l.txt','-c','copy','base3.mp4'],check=True)
