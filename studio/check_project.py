#!/usr/bin/env python3
"""Fail-closed preflight for a shot-accurate Arabic video project."""
import json, pathlib, sys
def fail(msg):
    raise ValueError(msg)
def check(project_path, timeline_path):
    p=json.loads(pathlib.Path(project_path).read_text(encoding="utf-8"))
    t=json.loads(pathlib.Path(timeline_path).read_text(encoding="utf-8"))
    for key in ("project_id","title_ar","source_uri"):
        if not p.get(key) or p[key]=="REPLACE_ME": fail("Missing project "+key)
    if not p.get("source_rights_verified"): fail("Source rights not verified")
    if not p.get("script_complete"): fail("Complete script required before editing")
    if t.get("project_id")!=p["project_id"]: fail("Project/timeline ID mismatch")
    parts=p.get("parts",[])
    if not parts or len({v["id"] for v in parts})!=len(parts): fail("Invalid/duplicate part IDs")
    ids={v["id"] for v in parts}
    for part in parts:
        if not part.get("cover") or not part.get("output"): fail("Missing unique cover/output")
    if len({v["cover"] for v in parts})!=len(parts): fail("Covers must be unique")
    cues=t.get("cues",[])
    if not cues: fail("No timed visual cues")
    seen=set()
    for i,c in enumerate(cues):
        if c.get("part_id") not in ids: fail(f"Cue {i}: unknown part")
        a,b=c.get("source_start"),c.get("source_end")
        if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or a<0 or b<=a:
            fail(f"Cue {i}: invalid source times")
        for field in ("arabic_text","speaker_id","audio_path","visual_event","visual_evidence"):
            if not c.get(field): fail(f"Cue {i}: missing {field}")
        if not c.get("verified_by_viewing"): fail(f"Cue {i}: visual review missing")
        key=(c["part_id"],a,b)
        if key in seen: fail(f"Cue {i}: duplicate range")
        seen.add(key)
    for part in parts:
        if not any(c["part_id"]==part["id"] for c in cues): fail("Part missing timed cues")
    print(f"Preflight passed: {len(parts)} parts, {len(cues)} cues. Manual final QA still required.")
if __name__=="__main__":
    if len(sys.argv)!=3:
        print("Usage: python studio/check_project.py project.json timeline.json",file=sys.stderr);sys.exit(2)
    try: check(*sys.argv[1:])
    except (ValueError,KeyError,TypeError,FileNotFoundError) as e:
        print("BLOCKED:",e,file=sys.stderr);sys.exit(1)
