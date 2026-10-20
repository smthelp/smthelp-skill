import os
PROJ=os.environ.get('PROJ', os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')))
# python encode.py l|p seg_index nsegs   -> segments; python encode.py l|p final  -> concat + audio
import sys,subprocess,json,os
P=PROJ+"/"
m=sys.argv[1]; F=P+f"frames_{m}/"; meta=json.load(open(F+'meta.json')); N=meta['N']; fps=meta['fps']
os.makedirs(P+'enc',exist_ok=True)
if sys.argv[2]!='final':
    i,n=int(sys.argv[2]),int(sys.argv[3]); a=N*i//n; b=N*(i+1)//n
    subprocess.run(['ffmpeg','-y','-v','error','-framerate',str(fps),'-start_number',str(a),'-i',F+'%05d.jpg','-frames:v',str(b-a),
      '-c:v','libx264','-preset','faster','-crf','17','-pix_fmt','yuv420p','-profile:v','high','-level','5.1','-g',str(fps*2),'-bf','2',
      P+f'enc/{m}_{i:02d}.mp4'],check=True)
    print('seg',i,a,b)
else:
    segs=sorted(f for f in os.listdir(P+'enc') if f.startswith(m+'_') and f.endswith('.mp4'))
    open(P+f'enc/{m}_list.txt','w').write(''.join(f"file '{P}enc/{s}'\n" for s in segs))
    name={'l':'CN-SM-2713_JUKI_Gripper_Nozzle_4K_16x9.mp4','p':'CN-SM-2713_JUKI_Gripper_Nozzle_4K_9x16_Shorts.mp4'}[m]
    subprocess.run(['ffmpeg','-y','-v','error','-f','concat','-safe','0','-i',P+f'enc/{m}_list.txt','-i',P+'build/audio/final_mix.wav',
      '-map','0:v','-map','1:a','-c:v','copy','-c:a','aac','-b:a','320k','-shortest','-movflags','+faststart','/tmp/'+name],check=True); import shutil; shutil.copy('/tmp/'+name,P+'deliverables/'+name)
    print(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration,size:stream=width,height,r_frame_rate','-of','compact',P+'deliverables/'+name]).decode())
