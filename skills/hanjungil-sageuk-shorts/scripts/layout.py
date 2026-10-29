import os
from PIL import Image,ImageDraw,ImageFont,ImageFilter
W,H=1080,1920;VY=540;VH=608
SANS="/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc";SERIF="/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc"
LANG={"kr":1,"cn":2,"jp":0}
FD=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","fonts")+"/";TITLE=FD+"Shilla_CultureB.ttf";SUBT=FD+"Paperlogy-5Medium.ttf";LINE=FD+"LXGWWenKaiKR-Light.ttf"
def FF(path,sz): return ImageFont.truetype(path,sz)
def F(sz,serif=False,lang="kr"): return ImageFont.truetype(SERIF if serif else SANS,sz,index=LANG[lang])
def ctext(d,y,t,f,fill,stroke=0,sc="black",w0=W):
    w=d.textlength(t,font=f);d.text(((w0-w)/2,y),t,font=f,fill=fill,stroke_width=stroke,stroke_fill=sc)
THEME={"kr":(245,245,240),"cn":(214,38,38),"jp":(40,96,200),None:(200,200,200)}
CUTS={
 "kr":dict(n=1,badge="조선  ·  한국",line="전하… 아니 되옵니다!",pron=None,tr="전하, 제발 그것만은 아니 되옵니다!",tag="#눈물의_읍소",sub=(0.5,4.4)),
 "cn":dict(n=2,badge="명나라  ·  중국",line="皇上，万万不可！",pron="[황상, 완완 부커!]",tr="폐하, 결코 그리하셔선 아니 되옵니다!",tag="#우렁찬_직언",sub=(0.0,4.4)),
 "jp":dict(n=3,badge="에도  ·  일본",line="殿…なりませぬ。",pron="[도노… 나리마세누]",tr="주군… 그리하셔서는 아니 되옵니다.",tag="#침묵의_압박",sub=(0.6,4.4)),
}
def base(theme=None):
    im=Image.new("RGB",(W,H),(0,0,0));d=ImageDraw.Draw(im)
    ctext(d,205,"“아니 되옵니다”",FF(TITLE,124),(255,255,255))
    ctext(d,385,"한·중·일 신하가 왕을 막는 법",FF(SUBT,48),(200,200,200))
    if theme:
        c=THEME[theme];d.rectangle([0,VY-6,W,VY-1],fill=c);d.rectangle([0,VY+VH+1,W,VY+VH+6],fill=c)
    return im,d
def dots(d,active):
    for i,k in enumerate(["kr","cn","jp"]):
        x=W/2+(i-1)*110;r=34;on=(i+1)==active;c=THEME[k]
        d.ellipse([x-r,1760-r,x+r,1760+r],fill=c if on else None,outline=c,width=3)
        f=F(36);t=str(i+1);w=d.textlength(t,font=f)
        d.text((x-w/2,1760-26),t,font=f,fill=((0,0,0) if k=="kr" else (255,255,255)) if on else c)
def cut(c,out):
    im,d=base(c);k=CUTS[c];col=THEME[c]
    f=FF(SUBT,46);t=f"{k['n']}  {k['badge']}";w=d.textlength(t,font=f)
    d.rounded_rectangle([(W-w)/2-34,1190,(W+w)/2+34,1266],radius=14,fill=col)
    ctext(d,1200,t,f,(0,0,0) if c=="kr" else (255,255,255))
    y=1320
    y+=95  # Korean line is animated by kinetic.py
    if k["pron"]: ctext(d,y,k["pron"],F(40),(150,150,150));y+=70
    ctext(d,1560,k["tag"],F(44),col if c!="kr" else (220,220,220))
    dots(d,k["n"]);im.save(out)
def glowsub(text,out):
    """movie-style subtitle: thin white text with a soft faint dark glow, no outline"""
    f=FF(LINE,48);y=VH-90
    g=Image.new("RGBA",(W,VH),(0,0,0,0));gd=ImageDraw.Draw(g);ctext(gd,y,text,f,(0,0,0,255),4,(0,0,0,255))
    g=g.filter(ImageFilter.GaussianBlur(9));a=g.split()[3].point(lambda v:int(v*0.55));g.putalpha(a)
    t=Image.new("RGBA",(W,VH),(0,0,0,0));ctext(ImageDraw.Draw(t),y,text,f,(255,255,255,255))
    Image.alpha_composite(g,t).save(out)
def onvideo(c,out):
    """transparent 1080x608 movie-style subtitle in original language"""
    glowsub(CUTS[c]["line"],out)
def intro(out):
    im,d=base(None)
    ctext(d,1250,"같은 대사,",F(76,True),(255,255,255))
    ctext(d,1355,"한중일 사극은 어떻게 다를까?",F(68,True),(255,255,255))
    dots(d,0);im.save(out)
def outro(out,thumbs):
    im,d=base(None)
    for i,(t,k) in enumerate(zip(thumbs,["kr","cn","jp"])):
        th=Image.open(t).convert("RGB");s=VH/th.height;th=th.resize((int(th.width*s),VH))
        x0=(th.width-356)//2;im.paste(th.crop((x0,0,x0+356,VH)),(i*362,VY))
        d.rectangle([i*362,VY+VH-8,i*362+356,VY+VH],fill=THEME[k])
        f=F(64);col=THEME[k]
        d.ellipse([i*362+178-44,VY+VH-124,i*362+178+44,VY+VH-36],fill=col)
        w=d.textlength(str(i+1),font=f);d.text((i*362+178-w/2,VY+VH-127),str(i+1),font=f,fill=(0,0,0) if k=="kr" else "white")
    ctext(d,1250,"당신의 원픽은?",F(96,True),(255,255,255))
    ctext(d,1390,"댓글로 1 · 2 · 3",F(64),(200,200,200))
    im.save(out)
if __name__=="__main__":
    for c in CUTS: cut(c,f"ov_{c}.png");onvideo(c,f"sub_{c}.png")
    intro("ov_intro.png");outro("ov_outro.png",["last_kr.png","last_cn.png","last_jp.png"])

KING=dict(badge="반전  ·  그 시각 조선의 왕",tag="#왕_퇴사_선언",
          subs=[("아우!",0.0,1.17),("왕 이거 진짜 드러워서 못 해먹겠네!",1.17,3.62),("니가 왕 하세요!",3.62,6.3)])
def king(out):
    im,d=base("kr")
    im.save(out)
    for i,(s,a,b) in enumerate(KING["subs"]): glowsub(s,f"sub_king{i}.png")
if __name__=="__main__": king("ov_king.png")
