#!/usr/bin/env python3
"""Fail closed on missing character voice identity and unreviewed Arabic pronunciation."""
import argparse,json,pathlib,sys
ALLOWED={"calm","suspense","urgency","fear","relief","excitement","whisper"}
def validate(cast,dialogue,require_review=True):
    c=json.loads(pathlib.Path(cast).read_text(encoding="utf-8"))
    d=json.loads(pathlib.Path(dialogue).read_text(encoding="utf-8"))
    ids=[v.get("id") for v in c.get("voices",[])]
    if not ids or len(ids)!=len(set(ids)):raise ValueError("Duplicate/missing cast identities")
    errors=[]
    for line in d.get("lines",[]):
        lid=line.get("id","?")
        if line.get("speaker") not in ids:errors.append(f"{lid}: unknown speaker")
        if not line.get("text") or not line.get("scene_id"):errors.append(f"{lid}: missing text/scene")
        if line.get("emotion") not in ALLOWED:errors.append(f"{lid}: unknown emotion")
        if not line.get("delivery"):errors.append(f"{lid}: no acting direction")
        if require_review and not line.get("reviewed_pronunciation"):errors.append(f"{lid}: pronunciation not reviewed")
    if not d.get("lines"):errors.append("No dialogue")
    if errors:raise ValueError("; ".join(errors))
    print("Cast structure passed. Audio listening and scene alignment must be checked separately.")
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--cast",required=True);a.add_argument("--dialogue",required=True);a.add_argument("--draft",action="store_true");x=a.parse_args()
    try:validate(x.cast,x.dialogue,not x.draft)
    except ValueError as e:print("BLOCKED:",e,file=sys.stderr);sys.exit(1)
