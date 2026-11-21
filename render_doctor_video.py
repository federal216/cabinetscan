import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\İBO\.gemini\antigravity\scratch\cabinetscan")
IMG_SRC = Path(r"C:\Users\İBO\.gemini\antigravity\brain\c8b3a174-68a7-4b61-9d8e-bf1a05ca8e5f\female_longevity_doctor_portrait_1795274627490.jpg")
AUDIO_SRC = ROOT / "dr_elena_voice.mp3"
POSTER_OUT = ROOT / "doctor_poster.jpg"
VIDEO_OUT = ROOT / "cabinetscan_doctor_briefing.mp4"

# 720x1280 (9:16)
W, H = 720, 1280
FPS = 25
TOTAL_DUR = 30.9

print("[*] Preparing background and poster image...")
img = Image.open(IMG_SRC).convert("RGB")
img_resized = img.resize((W, H), Image.Resampling.LANCZOS)
img_resized.save(POSTER_OUT, "JPEG", quality=92)

# Create Subtitle / Telemetry Overlays for 4 scenes
WORK_DIR = ROOT / "temp_video"
WORK_DIR.mkdir(exist_ok=True)

scenes = [
    {
        "start": 0.0,
        "dur": 6.8,
        "badge": "CRITICAL HEALTH ALERT",
        "title": "DON'T TAKE RANDOM SUPPLEMENTS",
        "sub": "Until you run this molecular clash audit."
    },
    {
        "start": 6.8,
        "dur": 8.0,
        "badge": "82% ABSORPTION SHUTDOWN",
        "title": "MAGNESIUM + CALCIUM CONFLICT",
        "sub": "Wasting $140+ monthly due to DMT1 saturation."
    },
    {
        "start": 14.8,
        "dur": 8.0,
        "badge": "AUTONOMOUS VISION AI",
        "title": "SCANS YOUR SHELF IN SECONDS",
        "sub": "Catches drug clashes & liver strain before it starts."
    },
    {
        "start": 22.8,
        "dur": 8.1,
        "badge": "1-CLICK CHRONO SYNC",
        "title": "SYNC TO IPHONE CALENDAR",
        "sub": "Unlock your lifetime Master Dossier for $99."
    }
]

rendered_clips = []

for idx, sc in enumerate(scenes):
    print(f"[*] Rendering Scene {idx+1}/{len(scenes)}...")
    # Create overlay frame
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    
    # Top Live Doctor Badge
    d.rounded_rectangle([30, 40, 340, 85], radius=22, fill=(0, 0, 0, 200), outline=(16, 185, 129, 180), width=2)
    d.ellipse([50, 58, 62, 70], fill=(52, 211, 153, 255))
    d.text((75, 50), "DR. ELENA VANCE • CLINICAL AI", fill=(255, 255, 255), font_size=13)
    
    # Bottom HUD Box
    box_y = H - 260
    d.rounded_rectangle([25, box_y, W - 25, H - 50], radius=24, fill=(8, 10, 15, 210), outline=(16, 185, 129, 120), width=2)
    
    # Badge
    d.rounded_rectangle([45, box_y + 20, 280, box_y + 55], radius=10, fill=(244, 63, 94, 230))
    d.text((58, box_y + 28), sc["badge"], fill=(255, 255, 255), font_size=12)
    
    # Title & Sub
    d.text((45, box_y + 70), sc["title"], fill=(255, 255, 255), font_size=24)
    d.text((45, box_y + 115), sc["sub"], fill=(209, 213, 219), font_size=16)
    
    ov_path = WORK_DIR / f"ov_{idx:02d}.png"
    ov.save(ov_path, "PNG")
    
    # Render scene segment with zoompan and overlay
    n_frames = int(sc["dur"] * FPS)
    dur = sc["dur"]
    clip_out = WORK_DIR / f"scene_{idx:02d}.mp4"
    
    zoom = f"z='min(1+0.07*on/{n_frames},1.07)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    fc = (
        f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
        f"zoompan={zoom}:d={n_frames}:s={W}x{H}:fps={FPS},setsar=1[bg];"
        f"[1:v]format=rgba,fade=t=in:st=0.2:d=0.3:alpha=1[ov];"
        f"[bg][ov]overlay=0:0:format=auto,fade=t=in:st=0:d=0.2,fade=t=out:st={dur-0.2}:d=0.2,format=yuv420p[v]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(POSTER_OUT),
        "-loop", "1", "-i", str(ov_path),
        "-t", str(dur),
        "-filter_complex", fc,
        "-map", "[v]",
        "-r", str(FPS),
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        str(clip_out)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    rendered_clips.append(clip_out)

print("[*] Concatenating scenes...")
concat_file = WORK_DIR / "concat_list.txt"
with open(concat_file, "w") as f:
    for c in rendered_clips:
        f.write(f"file '{c.as_posix()}'\n")

temp_video_silent = WORK_DIR / "video_silent.mp4"
subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0",
    "-i", str(concat_file),
    "-c", "copy",
    str(temp_video_silent)
], check=True, capture_output=True)

print("[*] Muxing speech audio track...")
subprocess.run([
    "ffmpeg", "-y",
    "-i", str(temp_video_silent),
    "-i", str(AUDIO_SRC),
    "-map", "0:v",
    "-map", "1:a",
    "-c:v", "copy",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    str(VIDEO_OUT)
], check=True, capture_output=True)

print(f"[+++] SUCCESS! Video generated at: {VIDEO_OUT}")
