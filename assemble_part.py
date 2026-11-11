#!/usr/bin/env python3
"""Build one TikTok segment and standalone cover from approved source + separated ambient stem."""
import argparse, subprocess
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageFilter

def cmd(*args):
    subprocess.run(list(map(str,args)),check=True)

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--source",required=True)
    p.add_argument("--narration",required=True)
    p.add_argument("--out",default="deliverables")
    p.add_argument("--start",type=float,default=0)
    p.add_argument("--duration",type=float,default=90)
    p.add_argument("--part",type=int,default=1)
    a=p.parse_args()
    out=Path(a.out)
    out.mkdir(parents=True,exist_ok=True)
    video=out/f"part_{a.part}.mp4"
    # Full original action is centered in frame; blurred bars are the original footage, not invented scenes.
    filtergraph=(
        "[0:v]split=2[fg][back];"
        "[back]scale=1080:1080:force_original_aspect_ratio=increase,"
        "crop=1080:1080,boxblur=20:2[blur];"
        "[fg]scale=1080:1080:force_original_aspect_ratio=decrease[main];"
        "[blur][main]overlay=(W-w)/2:(H-h)/2:shortest=1[v];"
        "[0:a]volume=0.55[bg];"
        "[1:a]volume=1.15,adelay=3000|3000[voice];"
        "[bg][voice]amix=inputs=2:duration=first:dropout_transition=1[a]"
    )
    cmd("ffmpeg","-y","-hide_banner","-loglevel","error","-ss",a.start,
        "-t",a.duration,"-i",a.source,"-i",a.narration,
        "-filter_complex",filtergraph,"-map","[v]","-map","[a]",
        "-c:v","libx264","-preset","veryfast","-crf","21","-pix_fmt","yuv420p",
        "-c:a","aac","-b:a","192k","-movflags","+faststart","-t",a.duration,video)
    frame=out/"source_frame.jpg"
    cmd("ffmpeg","-y","-hide_banner","-loglevel","error",
        "-ss",str(a.start+min(12,a.duration/2)),"-i",a.source,
        "-frames:v","1","-vf","scale=1080:1080:force_original_aspect_ratio=decrease,"
        "pad=1080:1080:(ow-iw)/2:(oh-ih)/2:black",frame)
    image=Image.open(frame).convert("RGB")
    overlay=Image.new("RGBA",image.size,(0,0,0,0))
    d=ImageDraw.Draw(overlay)
    d.rectangle((0,650,1080,1080),fill=(0,0,0,194))
    font_path="/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    title=ImageFont.truetype(font_path,73)
    small=ImageFont.truetype(font_path,58)
    d.text((540,742),"معركة كوريا الجوية",font=title,anchor="mm",direction="rtl",fill="white",stroke_width=2,stroke_fill="#111111")
    d.text((540,849),"كورساير ضد ميغ ١٥",font=small,anchor="mm",direction="rtl",fill="#F5D593")
    d.text((540,958),"الجزء "+str(a.part),font=title,anchor="mm",direction="rtl",fill="white")
    final=Image.alpha_composite(image.convert("RGBA"),overlay).convert("RGB")
    final.save(out/f"cover_part_{a.part}.jpg",quality=94)
    print(video)
    print(out/f"cover_part_{a.part}.jpg")

if __name__=="__main__":
    main()
