#!/usr/bin/env python3
"""Separate vocal stem from rights-cleared video; keep picture frames unchanged."""
import argparse
import subprocess
from pathlib import Path

def run(*args):
    subprocess.run([str(a) for a in args], check=True)

def duration(path):
    return float(subprocess.check_output([
        "ffprobe","-v","error","-show_entries","format=duration",
        "-of","default=noprint_wrappers=1:nokey=1",str(path)],text=True).strip())

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True,help="URL that you are authorized to download and process")
    p.add_argument("--authorized",action="store_true")
    p.add_argument("--out",default="output")
    a=p.parse_args()
    if not a.authorized:
        p.error("Explicit download and editing permission required (--authorized).")
    out=Path(a.out).resolve()
    out.mkdir(parents=True,exist_ok=True)
    run("yt-dlp","--no-playlist","--no-progress",
        "--merge-output-format","mp4","-f","bv*+ba/b",
        "-o",out/"original.%(ext)s",a.source)
    originals=[p for p in out.glob("original.*") if p.suffix.lower() in (".mp4",".mkv",".mov",".webm")]
    if not originals:
        raise RuntimeError("Download unavailable; request an authorized direct file URL.")
    source=originals[0]
    run("ffmpeg","-y","-hide_banner","-loglevel","error",
        "-i",source,"-vn","-ar","44100","-ac","2",out/"original.wav")
    run("python","-m","demucs","-n","htdemucs","--two-stems","vocals",
        "--mp3","--mp3-bitrate","192","--out",out/"stems",out/"original.wav")
    background=out/"stems"/"htdemucs"/"original"/"no_vocals.mp3"
    if not background.exists():
        raise RuntimeError("No instrumental/background stem generated.")
    run("ffmpeg","-y","-hide_banner","-loglevel","error","-i",source,
        "-i",background,"-map","0:v:0","-map","1:a:0","-c:v","copy",
        "-c:a","aac","-b:a","192k","-af","apad","-t",f"{duration(source):.6f}",
        "-movflags","+faststart",out/"video_no_english_narrator.mp4")
    print(f"Background stem: {background}")
    print(f"Video remux: {out/'video_no_english_narrator.mp4'}")
    print("Quality check required: Demucs music separation can damage sound effects and retain speech.")
if __name__=="__main__":
    main()
