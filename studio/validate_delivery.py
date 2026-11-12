#!/usr/bin/env python3
"""Validate final video files and unique covers. This cannot validate narrative semantics."""
import argparse,json,pathlib,subprocess,sys
def probe(path):
    return json.loads(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration,size:stream=codec_type,width,height","-of","json",str(path)]))
def validate(project,output_dir):
    p=json.loads(pathlib.Path(project).read_text(encoding="utf-8")); root=pathlib.Path(output_dir)
    errors=[]
    for part in p.get("parts",[]):
        video=root/part.get("output","");cover=root/part.get("cover","")
        if not video.is_file() or video.stat().st_size<10000:errors.append(f"Part {part.get('id')}: video missing/empty");continue
        try:
            m=probe(video)
            if float(m["format"]["duration"])<=0:errors.append(f"Part {part['id']}: invalid duration")
            if not any(s["codec_type"]=="video" for s in m["streams"]):errors.append(f"Part {part['id']}: no video stream")
            if not any(s["codec_type"]=="audio" for s in m["streams"]):errors.append(f"Part {part['id']}: no audio stream")
        except Exception as e:errors.append(f"Part {part['id']}: ffprobe error {e}")
        if not cover.is_file() or cover.stat().st_size<1000:errors.append(f"Part {part['id']}: cover missing/empty")
    if errors:raise ValueError("; ".join(errors))
    print("Media checks passed; human audiovisual review and publication verification remain mandatory")
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("project");a.add_argument("output_dir");x=a.parse_args()
    try:validate(x.project,x.output_dir)
    except (ValueError,FileNotFoundError) as e:print("BLOCKED",e,file=sys.stderr);sys.exit(1)
