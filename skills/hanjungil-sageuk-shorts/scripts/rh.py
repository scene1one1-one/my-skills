import json,os,sys,time,urllib.request,uuid
H=os.environ["RUNNINGHUB_HOST"];K=os.environ["RUNNINGHUB_API_KEY"]
def post(path,obj):
    r=urllib.request.Request(H+path,json.dumps(obj).encode(),{"Content-Type":"application/json"})
    for i in range(6):
        try: return json.load(urllib.request.urlopen(r,timeout=120))
        except OSError:
            if i==5: raise
            time.sleep(2**i)
def upload(fn):
    b=uuid.uuid4().hex;data=open(fn,"rb").read()
    body=(f"--{b}\r\nContent-Disposition: form-data; name=\"apiKey\"\r\n\r\n{K}\r\n--{b}\r\nContent-Disposition: form-data; name=\"fileType\"\r\n\r\ninput\r\n--{b}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{os.path.basename(fn)}\"\r\nContent-Type: application/octet-stream\r\n\r\n").encode()+data+f"\r\n--{b}--\r\n".encode()
    r=json.load(urllib.request.urlopen(urllib.request.Request(H+"/task/openapi/upload",body,{"Content-Type":"multipart/form-data; boundary="+b}),timeout=300))
    return r["data"]["fileName"]
def wf(W):
    return json.loads(post("/api/openapi/getJsonApiFormat",{"apiKey":K,"workflowId":W})["data"]["prompt"])
def run(W,p,out,timeout=1800):
    for _ in range(360):
        r=post("/task/openapi/create",{"apiKey":K,"workflowId":W,"workflow":json.dumps(p)})
        if r.get("code")!=421: break
        time.sleep(10)
    if r.get("code")!=0: raise SystemExit("create failed: %s"%r)
    t=r["data"]["taskId"];print("task",t,flush=True);t0=time.time()
    while time.time()-t0<timeout:
        time.sleep(10)
        s=post("/task/openapi/status",{"apiKey":K,"taskId":t}).get("data")
        if s in("SUCCESS","FAILED"):break
    o=post("/task/openapi/outputs",{"apiKey":K,"taskId":t})
    if s!="SUCCESS": raise SystemExit("task %s %s %s"%(t,s,json.dumps(o)[:1500]))
    files=o["data"];res=[]
    for i,f in enumerate(files):
        ext=f["fileType"];fn=out if len(files)==1 else f"{out}_{i}.{ext}"
        for i in range(6):
            try: urllib.request.urlretrieve(f["fileUrl"],fn);break
            except OSError:
                if i==5: raise
                time.sleep(2**i)
        res.append(fn)
    print("done",res,"cost",[f.get("consumeCoins") for f in files],int(time.time()-t0),"s",flush=True);return res
