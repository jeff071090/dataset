from PIL import Image, ImageDraw, ImageFilter
import numpy as np, cv2, sys
im=Image.open(sys.argv[1]).convert('RGB')
a=np.array(im).astype(int)
r,g,b=a[...,0],a[...,1],a[...,2]
navy=(r<130)&(g<140)&(b<190)&(b-r>20)
reg=np.zeros_like(navy)
reg[330:365,185:280]=True
reg[367:427,78:380]=True
reg[426:500,50:402]=True
reg[:371,:142]=False
lb=(b>200)&(r<150)&(g>130)&(g<225)
sw=np.zeros_like(navy); sw[484:500,135:345]=True
mask=((navy&reg)|(lb&sw)).astype(np.uint8)*255
mask=cv2.dilate(mask,np.ones((5,5),np.uint8),iterations=1)
mask[:370,:142]=0
bgr=cv2.cvtColor(np.array(im),cv2.COLOR_RGB2BGR)
out=cv2.inpaint(bgr,mask,7,cv2.INPAINT_TELEA)
res=Image.fromarray(cv2.cvtColor(out,cv2.COLOR_BGR2RGB))
d=ImageDraw.Draw(res)
d.polygon([(91.2,52),(331,23.3),(363.8,275.3),(121.3,302.3)],fill=(214,222,235))
W=1080;H=round(644*W/451)
big=res.resize((W,H),Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2,percent=60,threshold=2))
big.save(sys.argv[2], quality=93) if sys.argv[2].endswith('.jpg') else big.save(sys.argv[2]); print(W,H)
