#!/usr/bin/env python3
"""Process one approved pending video from the queue."""
import json
import subprocess
from pathlib import Path

p=Path("queue.json")
data=json.loads(p.read_text(encoding="utf-8"))
item=next((i for i in data.get("items",[])
           if i.get("rights_confirmed") is True and i.get("url")
           and i.get("status","pending")=="pending"),None)
if not item:
    print("No rights-cleared items pending.")
    raise SystemExit(0)
print("Processing",item.get("title","untitled"))
subprocess.run(["python","process_video.py","--source",item["url"],"--authorized"],check=True)
item["status"]="processed"
p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
