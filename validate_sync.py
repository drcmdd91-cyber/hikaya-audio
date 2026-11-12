#!/usr/bin/env python3
"""Fail-closed validation of shot-to-voice cue sheets before rendering.
Usage: python validate_sync.py sync_cues.json --part 2
This checks metadata, not actual audiovisual correspondence; human review is mandatory.
"""
import argparse, json, pathlib, sys

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("cues")
    ap.add_argument("--part",type=int,required=True)
    a=ap.parse_args()
    data=json.loads(pathlib.Path(a.cues).read_text(encoding="utf-8"))
    if data.get("part_id") != a.part: raise ValueError("Part ID mismatch")
    if not data.get("source_video"): raise ValueError("Missing source_video")
    if data.get("visual_review_passed") is not True or data.get("audio_review_passed") is not True:
        raise ValueError("Actual visual and audio review not confirmed")
    cues=data.get("cues",[])
    if not cues: raise ValueError("No timed cues")
    prev=0.0
    for n,c in enumerate(cues,1):
        for field in ("scene_id","part_id","source_in","source_out","audio_in","audio_out","speaker_id","arabic_text","voice_file"):
            if field not in c: raise ValueError(f"Cue {n} missing {field}")
        if c["part_id"]!=a.part: raise ValueError(f"Cue {n}: wrong part")
        if not (0 <= c["audio_in"] < c["audio_out"] and c["source_in"] < c["source_out"]):
            raise ValueError(f"Cue {n}: invalid time range")
        if c["audio_in"] < prev: raise ValueError(f"Cue {n}: overlapping/out-of-order narration")
        if not pathlib.Path(c["voice_file"]).is_file(): raise ValueError(f"Cue {n}: voice file absent")
        prev=c["audio_out"]
    print(f"Metadata PASS for part {a.part}: {len(cues)} cues. Human A/V verification still required.")

if __name__=="__main__":
    try: main()
    except Exception as e:
        print("SYNC VALIDATION FAILED:",e,file=sys.stderr);sys.exit(1)
