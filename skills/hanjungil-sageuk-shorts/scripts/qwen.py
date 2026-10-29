# usage: qwen.py prompt.txt out.png aspect "ref1.png,ref2.png"
import sys,os,random;sys.path.insert(0,os.path.dirname(__file__));from rh import *
W=os.environ["RUNNINGHUB_EDIT_WORKFLOW_ID"];p=wf(W)
pr,out,ar=sys.argv[1:4];refs=[x for x in (sys.argv[4] if len(sys.argv)>4 else "").split(",") if x]
p["459:451"]["inputs"]["unet_name"]="qwen_image_2.1_int8_convrot.safetensors"
del p["470"];e=p["459:474"]["inputs"];e.pop("images.image_1",None)
for i,r in enumerate(refs,1):
    p[f"90{i}"]={"class_type":"LoadImage","inputs":{"image":upload(r)}};e[f"images.image_{i}"]=[f"90{i}",0]
e["prompt"]=open(pr).read()
p["459:468"]["inputs"]["switch"]=True
p["13"]["inputs"].update(aspect_ratio=ar,megapixels=2.0)
p["459:458"]["inputs"]["seed"]=random.randint(1,10**12)
p["461"]["inputs"]["filename_prefix"]="hjs/"+os.path.basename(out)
run(W,p,out)
