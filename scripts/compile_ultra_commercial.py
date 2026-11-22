import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\İBO\.gemini\antigravity\scratch\cabinetscan")
BRAIN = Path(r"C:\Users\İBO\.gemini\antigravity\brain\c8b3a174-68a7-4b61-9d8e-bf1a05ca8e5f")
AUDIO_SRC = ROOT / "dr_elena_voice.mp3"
VIDEO_OUT = ROOT / "cabinetscan_doctor_briefing.mp4"
POSTER_OUT = ROOT / "doctor_poster.jpg"
AVATAR_VID = ROOT / "dr_elena_talking_avatar.mp4"

WORK = ROOT / "temp_render"
WORK.mkdir(exist_ok=True)

FFMPEG = r"C:\Python315\Lib\site-packages\imageio_ffmpeg\binaries\ffmpeg-win-x86_64-v7.1.exe"

W, H = 720, 1280
FPS = 25

SCENES = [
    {
        "type": "talking_video",
        "video": AVATAR_VID,
        "dur": 7.0,
        "badge": "CRITICAL HEALTH ALERT",
        "title": "DON'T TAKE RANDOM SUPPLEMENTS",
        "sub": "Until you run this molecular clash audit."
    },
    {
        "type": "image",
        "img": BRAIN / "supplement_desk_macro_1795275810979.jpg",
        "dur": 7.8,
        "zoom": "out",
        "badge": "82% ABSORPTION SHUTDOWN",
        "title": "MAGNESIUM + CALCIUM CONFLICT",
        "sub": "Wasting $140+ monthly due to DMT1 saturation."
    },
    {
        "type": "image",
        "img": BRAIN / "doctor_exam_room_pdf_1795275767039.jpg",
        "dur": 8.0,
        "zoom": "in",
        "badge": "MASTER PDF DOSSIER",
        "title": "EXAMINING CLINICAL DATA",
        "sub": "Detects liver transaminases & adaptogen burnout."
    },
    {
        "type": "image",
        "img": BRAIN / "doctor_walking_clinic_1795275788341.jpg",
        "dur": 8.1,
        "zoom": "out",
        "badge": "1-CLICK IPHONE SYNC",
        "title": "AUTONOMOUS CHRONO-TIMETABLE",
        "sub": "Claim your lifetime Master Dossier for $99."
    }
]

# Set poster to Scene 1 frame
im_poster = Image.open(BRAIN / "female_longevity_doctor_portrait_1795274627490.jpg").convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
im_poster.save(POSTER_OUT, "JPEG", quality=92)

rendered_clips = []

for idx, sc in enumerate(SCENES):
    print(f"[*] Compiling Scene {idx+1}/{len(SCENES)} ({sc['type']})...")
    
    # HUD overlay creation
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    
    # Top Live Doctor Badge
    d.rounded_rectangle([30, 40, 370, 85], radius=22, fill=(0, 0, 0, 210), outline=(16, 185, 129, 200), width=2)
    d.ellipse([50, 58, 62, 70], fill=(52, 211, 153, 255))
    d.text((75, 52), "DR. ELENA VANCE • CLINICAL AI", fill=(255, 255, 255), font_size=13)
    
    # Bottom HUD Box
    box_y = H - 245
    d.rounded_rectangle([25, box_y, W - 25, H - 45], radius=24, fill=(6, 8, 12, 230), outline=(16, 185, 129, 130), width=2)
    
    # Badge
    b_len = len(sc["badge"]) * 10 + 26
    d.rounded_rectangle([45, box_y + 16, 45 + b_len, box_y + 48], radius=9, fill=(244, 63, 94, 230))
    d.text((58, box_y + 24), sc["badge"], fill=(255, 255, 255), font_size=12)
    
    # Title & Sub
    d.text((45, box_y + 65), sc["title"], fill=(255, 255, 255), font_size=23)
    d.text((45, box_y + 106), sc["sub"], fill=(209, 213, 219), font_size=15)
    
    ov_path = WORK / f"ov_{idx:02d}.png"
    ov.save(ov_path, "PNG")
    
    dur = sc["dur"]
    clip_out = WORK / f"clip_{idx:02d}.mp4"
    
    if sc["type"] == "talking_video":
        # Video with moving mouth + overlay
        fc = (
            f"[0:v]scale=-1:{H},crop={W}:{H}:(in_w-{W})/2:0,setsar=1[vid];"
            f"[1:v]format=rgba,fade=t=in:st=0.1:d=0.25:alpha=1[ov];"
            f"[vid][ov]overlay=0:0:format=auto,fade=t=in:st=0:d=0.2,fade=t=out:st={dur-0.2}:d=0.2,format=yuv420p[v]"
        )
        cmd = [
            FFMPEG, "-y",
            "-i", str(sc["video"]),
            "-loop", "1", "-i", str(ov_path),
            "-t", str(dur),
            "-filter_complex", fc,
            "-map", "[v]",
            "-r", str(FPS),
            "-c:v", "libx264", "-preset", "fast", "-crf", "19",
            str(clip_out)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error in scene {idx}:", res.stderr)
            raise RuntimeError(res.stderr)
    else:
        # Image zoompan + overlay
        bg_raw = Image.open(sc["img"]).convert("RGB")
        bg_resized = bg_raw.resize((W, H), Image.Resampling.LANCZOS)
        bg_path = WORK / f"bg_{idx:02d}.jpg"
        bg_resized.save(bg_path, "JPEG", quality=90)
        
        n_frames = int(dur * FPS)
        if sc["zoom"] == "in":
            zoom = f"z='min(1+0.07*on/{n_frames},1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        else:
            zoom = f"z='max(1.07-0.07*on/{n_frames},1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            
        fc = (
            f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
            f"zoompan={zoom}:d={n_frames}:s={W}x{H}:fps={FPS},setsar=1[bg];"
            f"[1:v]format=rgba,fade=t=in:st=0.1:d=0.25:alpha=1[ov];"
            f"[bg][ov]overlay=0:0:format=auto,fade=t=in:st=0:d=0.2,fade=t=out:st={dur-0.2}:d=0.2,format=yuv420p[v]"
        )
        cmd = [
            FFMPEG, "-y",
            "-loop", "1", "-i", str(bg_path),
            "-loop", "1", "-i", str(ov_path),
            "-t", str(dur),
            "-filter_complex", fc,
            "-map", "[v]",
            "-r", str(FPS),
            "-c:v", "libx264", "-preset", "fast", "-crf", "19",
            str(clip_out)
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error in scene {idx}:", res.stderr)
            raise RuntimeError(res.stderr)
            
    rendered_clips.append(clip_out)

# Concatenate all scenes
print("[*] Concatenating all scenes...")
concat_list = WORK / "concat_list.txt"
with open(concat_list, "w") as f:
    for c in rendered_clips:
        f.write(f"file '{c.as_posix()}'\n")

temp_video = WORK / "video_merged.mp4"
subprocess.run([
    FFMPEG, "-y",
    "-f", "concat", "-safe", "0",
    "-i", str(concat_list),
    "-c", "copy",
    str(temp_video)
], check=True, capture_output=True)

# Mux audio
print("[*] Adding audio track...")
subprocess.run([
    FFMPEG, "-y",
    "-i", str(temp_video),
    "-i", str(AUDIO_SRC),
    "-map", "0:v",
    "-map", "1:a",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    str(VIDEO_OUT)
], check=True, capture_output=True)

print(f"[+++] TALKING HEAD CINEMATIC COMMERCIAL COMPLETE: {VIDEO_OUT} ({VIDEO_OUT.stat().st_size} bytes)")
