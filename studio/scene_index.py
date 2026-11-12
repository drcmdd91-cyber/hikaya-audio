#!/usr/bin/env python3
"""Build a source-time shot index with FFmpeg scene-change detection."""
import argparse,json,pathlib,subprocess,re
def index(source,output,threshold=0.28):
    cmd=["ffmpeg","-hide_banner","-i",str(source),"-vf",f"select='gt(scene,{threshold})',showinfo","-an","-f","null","-"]
    p=subprocess.run(cmd,capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr[-1200:])
    times=[]
    for line in p.stderr.splitlines():
        if "showinfo" not in line or "pts_time:" not in line:continue
        m=re.search(r"pts_time:\s*([0-9.]+)",line)
        if m:times.append(float(m.group(1)))
    duration=json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","json",str(source)]))["format"]["duration"]
    boundaries=[0.0]+sorted(set(t for t in times if 0<t<float(duration)))+[float(duration)]
    data={"source":str(source),"threshold":threshold,"duration":float(duration),"shots":[{"shot_id":f"S{i+1:04d}","start":round(a,3),"end":round(b,3),"visual_event":"REQUIRES_VISUAL_REVIEW","reviewed":False} for i,(a,b) in enumerate(zip(boundaries,boundaries[1:])) if b>a]}
    pathlib.Path(output).parent.mkdir(parents=True,exist_ok=True)
    pathlib.Path(output).write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding="utf-8")
    print("Indexed",len(data["shots"]),"shots; visual content NOT verified")
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("source");a.add_argument("output");a.add_argument("--threshold",type=float,default=.28);x=a.parse_args();index(x.source,x.output,x.threshold)
