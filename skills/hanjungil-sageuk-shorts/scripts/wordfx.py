"""Ports of HyperFrames caption-highlight (Word-Sweep Highlight) and caption-clip-wipe to PIL frame sequences."""
import os
from PIL import Image,ImageDraw,ImageFilter
import layout as L
FR=24
def p2out(x): x=min(max(x,0),1); return 1-(1-x)**2          # power2.out
def p2in(x):  x=min(max(x,0),1); return x*x                 # power2.in
# word timings (s, e) inside each 5s cut, aligned to the spoken line
SWEEP={
 "kr":[("전하,",0.72,1.18),("제발",1.2,1.7),("그것만은",1.7,2.35),("아니",2.38,2.85),("되옵니다!",2.85,3.5)],
 "cn":[("폐하,",0.0,0.76),("결코",1.64,2.2),("그리하셔선",2.2,2.9),("아니",2.9,3.4),("되옵니다!",3.4,4.0)],
 "jp":[("주군…",0.77,1.4),("그리하셔서는",1.5,2.6),("아니",2.69,3.05),("되옵니다.",3.05,3.6)],
}
BOXY=1300;BOXH=170;GAP=18;PADX=14;PADY=8
def sweep(c,outdir,dur=5.0):
    os.makedirs(outdir,exist_ok=True);f=L.FF(L.TITLE,58);col=L.THEME[c]
    words=SWEEP[c];d0=ImageDraw.Draw(Image.new("RGB",(4,4)))
    ws=[d0.textlength(w,font=f) for w,_,_ in words];total=sum(ws)+GAP*(len(ws)-1);x=(L.W-total)/2;xs=[]
    for w in ws: xs.append(x);x+=w+GAP
    asc,desc=f.getmetrics();ty=20;th=asc+desc
    on_text=(0,0,0) if c=="kr" else (255,255,255)
    g0=words[0][1];last=len(words)-1
    for fi in range(int(dur*FR)+1):
        t=fi/FR;im=Image.new("RGBA",(L.W,BOXH),(0,0,0,0))
        ga=0 if t<g0 else p2out((t-g0)/0.12)
        if ga>0:
            bg=Image.new("RGBA",(L.W,BOXH),(0,0,0,0));bd=ImageDraw.Draw(bg)
            tx=Image.new("RGBA",(L.W,BOXH),(0,0,0,0));td=ImageDraw.Draw(tx)
            for i,(w,s,e) in enumerate(words):
                e2=e+0.6 if i==last else e
                if t<s: sx=0;so=0
                elif t<e2: k=p2out((t-s)/0.15);sx=k;so=k
                else: k=p2in((t-e2)/0.1);sx=1+0.02*k;so=1-k
                active=so>0.5
                if so>0 and sx>0:
                    x0=xs[i]-PADX;x1=x0+(ws[i]+2*PADX)*sx
                    bd.rounded_rectangle([x0,ty-PADY+4,x1,ty+th+PADY-6],radius=10,fill=col+(int(255*so),))
                td.text((xs[i],ty),w,font=f,fill=(on_text if active else (255,255,255))+(255,))
            sh=Image.new("RGBA",(L.W,BOXH),(0,0,0,0));sh.putalpha(tx.split()[3].point(lambda v:int(v*0.45)))
            sh=sh.filter(ImageFilter.GaussianBlur(9));sh=sh.transform(sh.size,Image.AFFINE,(1,0,0,0,1,-6))
            im=Image.alpha_composite(Image.alpha_composite(sh,bg),tx)
            if ga<1: im.putalpha(im.split()[3].point(lambda v:int(v*ga)))
        im.save(f"{outdir}/f{fi:04d}.png")
# intro clip wipe, two lines, keywords yellow
INTRO=[[("목숨",0.0,0.4,True),("걸고",0.4,0.64,True),("말리는",0.64,1.0,False),("신하",1.0,1.47,False)],
       [("한중일은",1.98,2.7,"kcj"),("어떻게",2.83,3.3,False),("다를까?",3.3,3.8,False)]]
def clipwipe(outdir,dur=3.9,top=1230,sizes=(76,68),lh=105):
    os.makedirs(outdir,exist_ok=True);d0=ImageDraw.Draw(Image.new("RGB",(4,4)));H=260
    lines=[]
    for li,ln in enumerate(INTRO):
        f=L.FF(L.SUBT,sizes[li]);gap=22;ws=[d0.textlength(w[0],font=f) for w in ln];tot=sum(ws)+gap*(len(ws)-1);x=(L.W-tot)/2;xs=[]
        for w in ws: xs.append(x);x+=w+gap
        lines.append((f,ln,xs,ws,li*lh))
    for fi in range(int(dur*FR)+1):
        t=fi/FR;im=Image.new("RGBA",(L.W,H),(0,0,0,0))
        for f,ln,xs,ws,y in lines:
            for i,(w,s,e,kw) in enumerate(ln):
                if t<s: continue
                p=p2out((t-s)/0.3)
                g=Image.new("RGBA",(L.W,H),(0,0,0,0));gd=ImageDraw.Draw(g)
                if kw=="kcj":  # 한=white 중=red 일=blue (country theme colours)
                    cx=xs[i]
                    for ch,k in zip(w,["kr","cn","jp"]+[None]*len(w)):
                        col=L.THEME[k] if (k and t>=s+0.1) else (255,255,255)
                        gd.text((cx,y),ch,font=f,fill=col+(255,));cx+=gd.textlength(ch,font=f)
                else:
                    color=(255,215,0) if (kw and t>=s+0.1) else (255,255,255)
                    gd.text((xs[i],y),w,font=f,fill=color+(255,))
                cut=int(xs[i]-4+(ws[i]+12)*p)
                g=g.crop((0,0,max(cut,0),H)) if cut>0 else None
                if g: im.alpha_composite(g,(0,0))
        im.save(f"{outdir}/f{fi:04d}.png")

def linewipe(c,outdir,dur=5.0):
    """caption-clip-wipe on the Korean dialogue line: each word wipes in L->R (0.3s power2.out) on its spoken cue"""
    os.makedirs(outdir,exist_ok=True);f=L.FF(L.TITLE,58);words=SWEEP[c]
    d0=ImageDraw.Draw(Image.new("RGB",(4,4)));ws=[d0.textlength(w,font=f) for w,_,_ in words]
    total=sum(ws)+GAP*(len(ws)-1);x=(L.W-total)/2;xs=[]
    for w in ws: xs.append(x);x+=w+GAP
    full=Image.new("RGBA",(L.W,BOXH),(0,0,0,0));fd=ImageDraw.Draw(full)
    for i,(w,_,_) in enumerate(words): fd.text((xs[i],20),w,font=f,fill=(255,255,255,255))
    for fi in range(int(dur*FR)+1):
        t=fi/FR;mask=Image.new("L",(L.W,BOXH),0);md=ImageDraw.Draw(mask)
        for i,(w,s,e) in enumerate(words):
            if t<s: continue
            p=p2out((t-s)/0.3);md.rectangle([xs[i]-6,0,xs[i]-6+(ws[i]+14)*p,BOXH],fill=255)
        im=Image.new("RGBA",(L.W,BOXH),(0,0,0,0));im.paste(full,(0,0),mask);im.save(f"{outdir}/f{fi:04d}.png")


# king reversal: romanized / Chinese / Japanese lines below the video, HyperFrames line-swap (bottom-up through a mask)
KING_ML=[  # (start, romanization, Chinese, Japanese) aligned with layout.KING subs
 (0.0, "Au!", "哎哟！", "あーもう！"),
 (1.17,"Wang igeo jinjja deureowoseo mot haemeokgenne!","这皇帝我真是干不下去了！","王なんて、もうやってられるか！"),
 (3.62,"Niga wang haseyo!","你来当皇帝吧！","お前が王をやれ！"),
]
def p4out(x): x=min(max(x,0),1); return 1-(1-x)**4
def kingswap(outdir,dur):
    os.makedirs(outdir,exist_ok=True);H=260;ROWH=70;ROWY=[20,84,148]
    cols=[L.THEME["kr"],L.THEME["cn"],(90,140,235)]
    d0=ImageDraw.Draw(Image.new("RGB",(4,4)))
    def fit(t,base):
        sz=base
        while sz>28 and d0.textlength(t,font=L.FF(L.LINE,sz))>1000: sz-=2
        return L.FF(L.LINE,sz)
    rows=[]  # per row: list of rendered strip images per beat
    for r in range(3):
        strips=[]
        for b in KING_ML:
            txt=b[1+r];f=fit(txt,46 if r==0 else 50);s=Image.new("RGBA",(L.W,ROWH),(0,0,0,0))
            dd=ImageDraw.Draw(s);w=dd.textlength(txt,font=f);asc,desc=f.getmetrics()
            dd.text(((L.W-w)/2,(ROWH-asc-desc)/2),txt,font=f,fill=cols[r]+(255,));strips.append(s)
        rows.append(strips)
    IN_A,EXIT,LAG,IN_B=0.5,0.35,0.22,0.5
    for fi in range(int(dur*FR)+1):
        t=fi/FR;im=Image.new("RGBA",(L.W,H),(0,0,0,0))
        for r in range(3):
            st=r*0.06  # slight row stagger
            band=Image.new("RGBA",(L.W,ROWH*3),(0,0,0,0))  # mask = middle third
            for bi,b in enumerate(KING_ML):
                beat=b[0]+st;nxt=KING_ML[bi+1][0]+st if bi+1<len(KING_ML) else None
                if bi==0: yin=1.15*(1-p4out((t-beat)/IN_A)) if t>=beat else None
                else: yin=1.15*(1-p4out((t-beat-LAG)/IN_B)) if t>=beat+LAG else None
                if yin is None: continue
                y=yin
                if nxt is not None and t>=nxt: y=-1.15*p2in((t-nxt)/EXIT)
                off=int(round(y*ROWH))
                if abs(off)>=ROWH: continue
                band.alpha_composite(rows[r][bi],(0,ROWH+off))
            im.alpha_composite(band.crop((0,ROWH,L.W,2*ROWH)),(0,ROWY[r]))
        im.save(f"{outdir}/f{fi:04d}.png")

if __name__=="__main__":
    for c in SWEEP: linewipe(c,f"kin_{c}")
    clipwipe("kin_intro")
    import subprocess
    kd=float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0","cut_king_fast.mp4"],capture_output=True,text=True).stdout)
    kingswap("kin_king",kd)
