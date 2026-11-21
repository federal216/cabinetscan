import math
from PIL import Image, ImageDraw, ImageFilter

# Create 1024x1024 canvas
size = 1024
img = Image.new("RGBA", (size, size), (8, 9, 13, 255))
draw = ImageDraw.Draw(img)

# Background subtle radial/linear glow
for r in range(400, 0, -5):
    alpha = int(35 * (1 - r / 400))
    draw.ellipse([512 - r, 512 - r, 512 + r, 512 + r], fill=(16, 185, 129, alpha))

for r in range(250, 0, -5):
    alpha = int(45 * (1 - r / 250))
    draw.ellipse([512 - r, 512 - r, 512 + r, 512 + r], fill=(6, 182, 212, alpha))

# App Icon Frame with rounded rectangle
icon_size = 800
pad = (size - icon_size) // 2
draw.rounded_rectangle([pad, pad, pad + icon_size, pad + icon_size], radius=180, fill=(13, 16, 24, 255), outline=(16, 185, 129, 90), width=4)

# Inner soft ambient glow
glow_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
glow_draw = ImageDraw.Draw(glow_layer)

# Draw Pill Capsule (Rotated 45 degrees or vertical)
# Let's draw centered capsule tilted 35 degrees
cx, cy = 512, 512
pill_w = 160
pill_h = 420

# Create pill mask on a separate layer
pill_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
p_draw = ImageDraw.Draw(pill_layer)

# Capsule coordinates (vertical then rotated)
x0, y0 = cx - pill_w // 2, cy - pill_h // 2
x1, y1 = cx + pill_w // 2, cy + pill_h // 2

# Top Half (Emerald green gradient)
p_draw.rounded_rectangle([x0, y0, x1, cy], radius=pill_w // 2, fill=(16, 185, 129, 240))
# Bottom Half (Cyan / Platinum)
p_draw.rounded_rectangle([x0, cy, x1, y1], radius=pill_w // 2, fill=(6, 182, 212, 240))

# Center separation ring
p_draw.line([x0 + 4, cy, x1 - 4, cy], fill=(255, 255, 255, 200), width=6)

# Specular shine on pill left side
p_draw.line([x0 + 25, y0 + 60, x0 + 25, cy - 20], fill=(255, 255, 255, 140), width=10)
p_draw.line([x0 + 25, cy + 20, x0 + 25, y1 - 60], fill=(255, 255, 255, 90), width=10)

# Rotate pill layer 40 degrees
rotated_pill = pill_layer.rotate(38, resample=Image.BICUBIC, center=(cx, cy))
img.paste(rotated_pill, (0, 0), rotated_pill)

# Horizontal Laser Scan Beam across the middle
beam_layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
b_draw = ImageDraw.Draw(beam_layer)

beam_y = cy - 20
# Outer glow of the beam
for w in range(40, 0, -4):
    a = int(60 * (1 - w / 40))
    b_draw.line([pad + 40, beam_y, pad + icon_size - 40, beam_y], fill=(52, 211, 153, a), width=w)

# Core sharp laser beam
b_draw.line([pad + 40, beam_y, pad + icon_size - 40, beam_y], fill=(255, 255, 255, 240), width=4)

# Laser crosshair target marks
t_len = 30
# Top-left target bracket
b_draw.line([cx - 220, cy - 220, cx - 220 + t_len, cy - 220], fill=(52, 211, 153, 180), width=3)
b_draw.line([cx - 220, cy - 220, cx - 220, cy - 220 + t_len], fill=(52, 211, 153, 180), width=3)
# Bottom-right target bracket
b_draw.line([cx + 220, cy + 220, cx + 220 - t_len, cy + 220], fill=(52, 211, 153, 180), width=3)
b_draw.line([cx + 220, cy + 220, cx + 220, cy + 220 - t_len], fill=(52, 211, 153, 180), width=3)

# Composite beam
img.paste(beam_layer, (0, 0), beam_layer)

# Save high-res PNG
output_path = r"C:\Users\İBO\.gemini\antigravity\scratch\cabinetscan\logo.png"
img.save(output_path, "PNG")
print(f"Logo generated successfully at: {output_path}")
