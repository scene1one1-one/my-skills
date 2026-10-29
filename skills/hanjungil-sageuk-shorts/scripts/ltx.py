# usage: ltx.py start.png prompt.txt out.mp4 seconds [seed]
import sys,os,json;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from rh import *
W="2087902142043815938";p=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"ltx25_i2v_facefix_api.json")))
img,pr,out,sec=sys.argv[1:5];seed=int(sys.argv[5]) if len(sys.argv)>5 else 20261029
neg="text, subtitles, watermark, logo, modern clothing, extra people, distorted face, deformed face, melting face, asymmetric eyes, blurry face, distorted hands, extra fingers, face morphing, identity change, flicker, flickering light, flashing, strobing, exposure changes, shimmering patterns, moire, blurry, low quality, cartoon, background music"
I=lambda k:p[k]["inputs"]
I("395")["image"]=upload(img);I("409")["value"]=open(pr).read();I("419")["text"]=neg
I("413")["value"]=int(sec);I("423")["noise_seed"]=seed
I("452")["filename_prefix"]="hjs/"+os.path.basename(out).split(".")[0]
run(W,p,out)
