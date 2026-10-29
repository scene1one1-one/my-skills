"""Hyper-motion kinetic typography for the Korean dialogue line below the video."""
import os,math,sys
from PIL import Image,ImageDraw
import layout as L
FR=24;DUR=5.0;BOXY=1300;BOXH=170;BASEY=1320-BOXY
STYLE={"kr":dict(stagger=0.045,dur=0.32,s0=1.9,shake=7),
       "cn":dict(stagger=0.03,dur=0.24,s0=2.3,shake=10),
       "jp":dict(stagger=0.08,dur=0.5,s0=1.25,shake=0)}
def back(t,s=2.2):t-=1;return t*t*((s+1)*t+s)+1
def render(c,outdir):
    os.makedirs(outdir,exist_ok=True);k=L.CUTS[c];st=STYLE[c];f=L.FF(L.TITLE,58)
    text=k["tr"];t0=k["sub"][0]
    d0=ImageDraw.Draw(Image.new("RGB",(4,4)));total=d0.textlength(text,font=f);x0=(L.W-total)/2
    xs=[x0+d0.textlength(text[:i],font=f) for i in range(len(text))]
    glyph={}
    for ch in set(text):
        w=int(d0.textlength(ch,font=f))+8;g=Image.new("RGBA",(max(w,8),90),(0,0,0,0))
        ImageDraw.Draw(g).text((4,0),ch,font=f,fill=(255,255,255,255));glyph[ch]=g
    n=len(text);end_in=t0+st["stagger"]*(n-1)+st["dur"]
    for fi in range(int(DUR*FR)+1):
        t=fi/FR;im=Image.new("RGBA",(L.W,BOXH),(0,0,0,0))
        sx=sy=0
        if st["shake"] and end_in<=t<end_in+0.22:
            a=st["shake"]*(1-(t-end_in)/0.22);sx=a*math.sin(t*95);sy=a*0.5*math.cos(t*77)
        for i,ch in enumerate(text):
            if ch==" ":continue
            p=(t-t0-i*st["stagger"])/st["dur"]
            if p<=0:continue
            p=min(p,1);sc=st["s0"]+(1-st["s0"])*back(p,1.7 if c!="jp" else 0.0);al=min(1,p*2.5)
            g=glyph[ch];w,h=g.size;gs=g.resize((max(1,int(w*sc)),max(1,int(h*sc))),Image.BICUBIC)
            if al<1: gs.putalpha(gs.split()[3].point(lambda v:int(v*al)))
            dy=(1-p)*(-18 if c!="jp" else 10)
            cx=xs[i]-4+w/2+sx;cy=BASEY+h/2+dy+sy
            im.alpha_composite(gs,(int(cx-gs.width/2),int(cy-gs.height/2)))
        im.save(f"{outdir}/f{fi:04d}.png")
if __name__=="__main__":
    for c in sys.argv[1:] or ["kr","cn","jp"]: render(c,f"kin_{c}")
