#!/usr/bin/env python3
import json, pathlib, tempfile
from check_project import check
def run():
    p={"project_id":"demo","title_ar":"تجربة","source_uri":"file.mp4","source_rights_verified":True,"script_complete":True,"parts":[{"id":1,"cover":"cover1.jpg","output":"part1.mp4"}]}
    t={"project_id":"demo","cues":[{"part_id":1,"source_start":1,"source_end":3,"arabic_text":"اختبار","speaker_id":"narrator","audio_path":"voice.wav","visual_event":"verified action","visual_evidence":"reviewer notes","verified_by_viewing":True}]}
    with tempfile.TemporaryDirectory() as d:
        a=pathlib.Path(d)/"p.json";b=pathlib.Path(d)/"t.json"
        def write():a.write_text(json.dumps(p));b.write_text(json.dumps(t))
        write();check(a,b)
        t["cues"][0]["verified_by_viewing"]=False;write()
        try:check(a,b)
        except ValueError:pass
        else:raise AssertionError("Unreviewed cue passed")
        t["cues"][0]["verified_by_viewing"]=True;p["script_complete"]=False;write()
        try:check(a,b)
        except ValueError:pass
        else:raise AssertionError("Incomplete script passed")
    print("All studio preflight tests passed")
if __name__=="__main__":run()
