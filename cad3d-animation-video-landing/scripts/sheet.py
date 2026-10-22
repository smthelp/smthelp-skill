import sys,glob
from PIL import Image
fs=sorted(glob.glob(f'prev/{sys.argv[1]}_*.jpg')); cols=int(sys.argv[2]); w=int(sys.argv[3])
ims=[Image.open(f) for f in fs]; h=int(ims[0].height*w/ims[0].width)
S=Image.new('RGB',(cols*w,((len(ims)+cols-1)//cols)*h))
for i,im in enumerate(ims): S.paste(im.resize((w,h)),((i%cols)*w,(i//cols)*h))
S.save(f'sheet_{sys.argv[1]}.jpg',quality=85)
