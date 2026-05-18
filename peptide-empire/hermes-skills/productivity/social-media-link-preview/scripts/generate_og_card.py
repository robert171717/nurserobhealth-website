#!/usr/bin/env python3
"""Generate a Nurse Rob branded OG card (1200x630) with brightness verification.
Requires: Pillow (pip install Pillow)

Usage:
    python3 scripts/generate_og_card.py
    # Output: og-card-{timestamp}.jpg in current directory
"""

from PIL import Image, ImageDraw, ImageFont, ImageEnhance
import os, time

W, H = 1200, 630
# Slate-blue background — bright enough to register on X/Twitter preview
img = Image.new('RGB', (W, H), (25, 40, 65))
draw = ImageDraw.Draw(img)

# Find system fonts
def find_font(pattern, size):
    for d in ['/usr/share/fonts/truetype']:
        for root, dirs, files in os.walk(d):
            for f in files:
                fp = os.path.join(root, f)
                if pattern in f.lower():
                    try: return ImageFont.truetype(fp, size)
                    except: pass
    return ImageFont.load_default()

title_font = find_font('bold', 64)
sub_font = find_font('regular', 36)
small_font = ImageFont.load_default()

# Gold accent line
draw.rectangle([80, 80, 1120, 86], fill=(230, 190, 90))

# Centered title
title = "Nurse Rob, RN"
bbox = draw.textbbox((0, 0), title, font=title_font)
tw = bbox[2] - bbox[0]
draw.text(((W-tw)//2, 120), title, fill=(255, 255, 255), font=title_font)

# Subtitle in teal
sub = "Licensed Peptide Educator & Consultant"
bbox2 = draw.textbbox((0, 0), sub, font=sub_font)
sw = bbox2[2] - bbox2[0]
draw.text(((W-sw)//2, 210), sub, fill=(0, 210, 185), font=sub_font)

# Second line
sub2 = "Research-Backed. No Bro-Science. Real Clinical Knowledge."
bbox3 = draw.textbbox((0, 0), sub2, font=sub_font)
sw2 = bbox3[2] - bbox3[0]
draw.text(((W-sw2)//2, 265), sub2, fill=(200, 205, 220), font=sub_font)

# Teal divider
draw.rectangle([300, 370, 900, 373], fill=(0, 210, 185))

# Feature pills
features = ["Licensed RN", "100+ Protocols", "Research-Backed", "Safety First"]
x_start = 120
spacing = (W - 240) // len(features)
for i, feat in enumerate(features):
    x = x_start + i * spacing
    draw.rounded_rectangle([x, 400, x + 200, 460], radius=10, fill=(0, 160, 140))
    b = draw.textbbox((0, 0), feat, font=small_font)
    fw = b[2] - b[0]
    draw.text((x + 100 - fw//2, 415), feat, fill=(255, 255, 255), font=small_font)

# Bottom accent
draw.rectangle([80, 540, 1120, 544], fill=(230, 190, 90))
draw.text((100, 560), "nurserobhealth.com", fill=(160, 165, 185), font=small_font)

# CRITICAL: Brighten for social media visibility
# Dark navy backgrounds look like black voids on X/Twitter
enhancer = ImageEnhance.Brightness(img)
img = enhancer.enhance(1.4)
enhancer = ImageEnhance.Contrast(img)
img = enhancer.enhance(1.1)

# Save
ts = int(time.time())
outpath = f'og-card-{ts}.jpg'
img.save(outpath, 'JPEG', quality=93)

# Verify
img2 = Image.open(outpath)
pixels = list(img2.getdata())
unique = len(set(pixels))
brightness = [(r+g+b)//3 for (r,g,b) in pixels]
dark_pct = 100 * sum(1 for b in brightness if b < 50) / len(brightness)
avg_brightness = sum(brightness) / len(brightness)

print(f"FILE: {outpath}")
print(f"Size: {img2.size}")
print(f"Unique colors: {unique}")
print(f"Dark pixels (<50 brightness): {dark_pct:.1f}%")
print(f"Average brightness: {avg_brightness:.0f}/255")
print("PASS" if unique > 50 and dark_pct < 80 else "FAIL — image too dark, increase brightness multiplier")
