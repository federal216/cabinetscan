import os
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(r"C:\Users\İBO\.gemini\antigravity\scratch\cabinetscan")
AUDIO_SRC = ROOT / "dr_elena_voice.mp3"
VIDEO_OUT = ROOT / "cabinetscan_doctor_briefing.mp4"
POSTER_OUT = ROOT / "doctor_poster.jpg"

W, H = 720, 1280
FPS = 25

def build_scene_overlay(w, h, badge_text, title_text, sub_text, badge_color=(244, 63, 94, 230)):
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    
    # Top Live Doctor Badge
    d.rounded_rectangle([30, 40, 360, 85], radius=22, fill=(0, 0, 0, 210), outline=(16, 185, 129, 200), width=2)
    d.ellipse([50, 58, 62, 70], fill=(52, 211, 153, 255))
    d.text((75, 52), "DR. ELENA VANCE • CLINICAL AI", fill=(255, 255, 255), font_size=13)
    
    # Bottom HUD Box
    box_y = h - 250
    d.rounded_rectangle([25, box_y, w - 25, h - 45], radius=24, fill=(6, 8, 12, 225), outline=(16, 185, 129, 130), width=2)
    
    # Badge
    d.rounded_rectangle([45, box_y + 18, 45 + len(badge_text) * 11 + 30, box_y + 52], radius=10, fill=badge_color)
    d.text((58, box_y + 26), badge_text, fill=(255, 255, 255), font_size=12)
    
    # Title & Subtitle
    d.text((45, box_y + 68), title_text, fill=(255, 255, 255), font_size=23)
    d.text((45, box_y + 110), sub_text, fill=(209, 213, 219), font_size=15)
    
    return ov

def render_scene_clip(img_path, overlay_img, duration, out_path, zoom_direction="in"):
    n_frames = int(duration * FPS)
    
    # Prepare background resized to WxH
    im = Image.open(img_path).convert("RGB")
    im_resized = im.resize((W, H), Image.Resampling.LANCZOS)
    temp_bg = out_path.parent / f"bg_{out_path.stem}.jpg"
    im_resized.save(temp_bg, "JPEG", quality=90)
    
    temp_ov = out_path.parent / f"ov_{out_path.stem}.png"
    overlay_img.save(temp_ov, "PNG")
    
    if zoom_direction == "in":
        zoom = f"z='min(1+0.08*on/{n_frames},1.08)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
    else:
        zoom = f"z='max(1.08-0.08*on/{n_frames},1.0)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
        
    fc = (
        f"[0:v]scale={W*2}:{H*2}:force_original_aspect_ratio=increase,crop={W*2}:{H*2},"
        f"zoompan={zoom}:d={n_frames}:s={W}x{H}:fps={FPS},setsar=1[bg];"
        f"[1:v]format=rgba,fade=t=in:st=0.1:d=0.3:alpha=1[ov];"
        f"[bg][ov]overlay=0:0:format=auto,fade=t=in:st=0:d=0.2,fade=t=out:st={duration-0.2}:d=0.2,format=yuv420p[v]"
    )
    
    cmd = [
        "ffmpeg", "-y",
        "-loop", "1", "-i", str(temp_bg),
        "-loop", "1", "-i", str(temp_ov),
        "-t", str(duration),
        "-filter_complex", fc,
        "-map", "[v]",
        "-r", str(FPS),
        "-c:v", "libx264", "-preset", "fast", "-crf", "19",
        str(out_path)
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    return out_path
