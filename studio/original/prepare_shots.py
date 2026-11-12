#!/usr/bin/env python3
"""Build shot prompts/manifests for original scenes; does not generate images or video."""
import json, pathlib, sys
def prepare(src,out):
    p=json.loads(pathlib.Path(src).read_text(encoding="utf-8"))
    if not p.get("project_id") or not p.get("title_ar") or p.get("aspect_ratio") not in ("9:16","16:9","1:1"):
        raise ValueError("Invalid project header")
    shots=p.get("shots",[])
    if not shots:raise ValueError("No shots")
    seen=set(); manifest=[]
    for s in shots:
        sid=s.get("shot_id")
        if not sid or sid in seen:raise ValueError("Missing/duplicate shot ID")
        seen.add(sid)
        for field in ("location","time_of_day","subjects","action_ar","camera","style","continuity","sound_design"):
            if not s.get(field):raise ValueError(f"{sid}: missing {field}")
        duration=s.get("duration_seconds")
        if not isinstance(duration,(int,float)) or duration<=0 or duration>60:
            raise ValueError(f"{sid}: invalid duration")
        if not s.get("visual_review_required"):raise ValueError(f"{sid}: review gate disabled")
        prompt=f"{s['style']}. {s['location']}, {s['time_of_day']}. Action: {s['action_ar']}. Camera: {s['camera']}. Subjects: {', '.join(s['subjects'])}. Maintain continuity: {'; '.join(s['continuity'])}. Aspect: {p['aspect_ratio']}."
        manifest.append({"shot_id":sid,"duration_seconds":duration,"prompt":prompt,"narration_ar":s.get("narration_ar",""),"dialogue":s.get("dialogue",[]),"sound_design":s["sound_design"],"reference_assets":s.get("reference_assets",[]),"render_status":"NOT_RENDERED","qa_status":"PENDING"})
    pathlib.Path(out).parent.mkdir(parents=True,exist_ok=True)
    pathlib.Path(out).write_text(json.dumps({"project_id":p["project_id"],"shots":manifest},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Prepared {len(manifest)} shot manifests; no video generated")
if __name__=="__main__":
    if len(sys.argv)!=3:raise SystemExit("Usage: prepare_shots.py spec.json output.json")
    prepare(*sys.argv[1:])
