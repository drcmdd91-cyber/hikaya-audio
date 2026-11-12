#!/usr/bin/env python3
"""Reusable 1080x1920 branded layout for story-specific covers and subtitles.
Requirements: ffmpeg, ffprobe, Pillow (PIL), Arabic shaping optional: arabic_reshaper, python-bidi.
Inputs: story cover image, video, subtitles .ass (optional).
The only constant brand element is 'دفتر الحكايات'; no fixed story imagery.
"""
import argparse,pathlib,subprocess,shutil,json
def call(cmd): subprocess.run(cmd,check=True)
def render(video,cover,output,subtitles=None):
    for p in [video,cover]:
        if not pathlib.Path(p).is_file():raise FileNotFoundError(p)
    if not shutil.which("ffmpeg"):raise RuntimeError("FFmpeg required")
    pathlib.Path(output).parent.mkdir(parents=True,exist_ok=True)
    # Upper cover 480px; middle video 1100px; lower graphic/subtitle zone 340px.
    # Story-specific cover is mandatory; no generic reused artwork.
    filter_graph=(
        "[0:v]scale=1080:1100:force_original_aspect_ratio=decrease,"
        "pad=1080:1100:(ow-iw)/2:(oh-ih)/2:color=0x080f1b,setsar=1[mid];"
        "[1:v]scale=1080:480:force_original_aspect_ratio=increase,crop=1080:480[top];"
        "color=c=0x081321:s=1080x340:r=30[bottom];"
        "[top][mid][bottom]vstack=inputs=3[stack]"
    )
    if subtitles:
        if not pathlib.Path(subtitles).is_file():raise FileNotFoundError(subtitles)
        # ASS events should use a bottom-aligned style and safe margins.
        escaped=str(pathlib.Path(subtitles).resolve()).replace("\\","/").replace(":","\\:").replace("'","\\'")
        filter_graph+=f";[stack]ass=filename='{escaped}'[v]"
    else:filter_graph+=";[stack]null[v]"
    cmd=["ffmpeg","-y","-hide_banner","-loglevel","error","-i",str(video),"-loop","1","-i",str(cover),"-filter_complex",filter_graph,"-map","[v]","-map","0:a?","-c:v","libx264","-pix_fmt","yuv420p","-preset","veryfast","-crf","21","-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",str(output)]
    call(cmd)
    print("Rendered:",output)
if __name__=="__main__":
    p=argparse.ArgumentParser();p.add_argument("--video",required=True);p.add_argument("--cover",required=True);p.add_argument("--output",required=True);p.add_argument("--subtitles");a=p.parse_args()
    render(a.video,a.cover,a.output,a.subtitles)
