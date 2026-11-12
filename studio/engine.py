#!/usr/bin/env python3
"""Free FFmpeg-based scene-accurate video renderer; no paid API required."""
import argparse,json,pathlib,subprocess,tempfile,shutil
def run(cmd): subprocess.run(cmd,check=True)
def render(project,timeline,root,output):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):raise RuntimeError("ffmpeg/ffprobe missing")
    from check_project import check
    check(project,timeline)
    p=json.loads(pathlib.Path(project).read_text()); t=json.loads(pathlib.Path(timeline).read_text())
    root=pathlib.Path(root);output=pathlib.Path(output);output.mkdir(parents=True,exist_ok=True)
    source=root/p["source_uri"]
    if not source.is_file():raise FileNotFoundError(source)
    with tempfile.TemporaryDirectory() as tmp:
        for part in p["parts"]:
            clips=[]
            for idx,c in enumerate(x for x in t["cues"] if x["part_id"]==part["id"]):
                audio=root/c["audio_path"]
                if not audio.is_file():raise FileNotFoundError(audio)
                clip=pathlib.Path(tmp)/f"part{part['id']}_{idx}.mp4"
                duration=c["source_end"]-c["source_start"]
                # Audio from the provided dubbed cue only: avoids leaking original English dialogue.
                run(["ffmpeg","-y","-hide_banner","-loglevel","error","-ss",str(c["source_start"]),"-t",str(duration),"-i",str(source),"-i",str(audio),"-filter_complex",f"[0:v]fps=30,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2,setsar=1[v];[1:a]aresample=48000,apad,atrim=0:{duration},asetpts=PTS-STARTPTS[a]","-map","[v]","-map","[a]","-c:v","libx264","-preset","veryfast","-crf","22","-c:a","aac","-ar","48000","-t",str(duration),str(clip)])
                clips.append(clip)
            concat=pathlib.Path(tmp)/f"concat{part['id']}.txt"
            concat.write_text("".join("file '"+str(c).replace("'","'\\''")+"'\n" for c in clips))
            target=output/part["output"];target.parent.mkdir(parents=True,exist_ok=True)
            run(["ffmpeg","-y","-hide_banner","-loglevel","error","-f","concat","-safe","0","-i",str(concat),"-c","copy","-movflags","+faststart",str(target)])
            run(["ffprobe","-v","error","-show_entries","format=duration","-of","default=noprint_wrappers=1",str(target)])
            print("Rendered",target)
if __name__=="__main__":
    a=argparse.ArgumentParser();a.add_argument("--project",required=True);a.add_argument("--timeline",required=True);a.add_argument("--assets",required=True);a.add_argument("--output",required=True);x=a.parse_args()
    render(x.project,x.timeline,x.assets,x.output)
