import sys,os,json,random;sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)));from rh import *
W="2115288764628336641";p=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"wf_yue2.json")))
style,out=sys.argv[1:3]
g=p["8"]["inputs"];g["style"]=style;g["max_duration"]=30
g["lyrics"]="[instrumental]\n\n[Intro]\n[instrumental]\n\n[Verse 1]\n[instrumental]\n\n[Chorus]\n[instrumental]"
s=random.randint(1,2**31);g["seed"]=s;p["10"]["inputs"]["seed"]=s
p["15"]["inputs"]["filename_prefix"]="audio/hjs_"+os.path.basename(out).split(".")[0]
run(W,p,out)
