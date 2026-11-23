#!/usr/bin/env python3
"""Render the GTA 6 meme: a skeleton who waited 13 years, and the make.fun ghost.

Original Pillow illustration, 1024x1024. Top text states the joke, the ghost
worked into the scene carries the make.fun pitch in the bottom banner.
"""
import math
import random

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
BOLD = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

random.seed(13)


def font(size):
    return ImageFont.truetype(BOLD, size)


def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def sky_color(y):
    """Vice City sunset gradient, y in 0..700."""
    if y < 260:
        return lerp((43, 16, 85), (160, 30, 120), y / 260)
    if y < 520:
        return lerp((160, 30, 120), (255, 46, 136), (y - 260) / 260)
    return lerp((255, 46, 136), (255, 154, 61), (y - 520) / 180)


img = Image.new("RGB", (W, H))
d = ImageDraw.Draw(img)

# --- sky gradient ---
for y in range(700):
    d.line([(0, y), (W, y)], fill=sky_color(y))

# --- retro sun with slits ---
SUN = (700, 430, 150)
d.ellipse([SUN[0] - SUN[2], SUN[1] - SUN[2], SUN[0] + SUN[2], SUN[1] + SUN[2]],
          fill=(255, 217, 77))
for i, yy in enumerate(range(SUN[1] + 10, SUN[1] + SUN[2], 16)):
    half = int(math.sqrt(max(0, SUN[2] ** 2 - (yy - SUN[1]) ** 2)))
    d.line([(SUN[0] - half, yy), (SUN[0] + half, yy)],
           fill=sky_color(yy), width=5 + i)

# --- skyline silhouette ---
SKYLINE = (36, 16, 64)
x = -10
while x < W:
    bw = random.randint(55, 120)
    bh = random.randint(90, 210)
    top = 700 - bh
    d.rectangle([x, top, x + bw, 700], fill=SKYLINE)
    for _ in range(bw * bh // 900):
        wx = random.randint(x + 6, x + bw - 10)
        wy = random.randint(top + 8, 690)
        d.rectangle([wx, wy, wx + 4, wy + 6], fill=(255, 217, 77))
    x += bw + random.randint(4, 18)

# --- palm silhouettes ---
PALM = (26, 11, 46)


def palm(cx, base, s, lean):
    # curved trunk, then fronds that arc out and droop down
    tx, ty = cx + lean, base - 210 * s
    n = 24
    for i in range(n):
        t0, t1 = i / n, (i + 1) / n
        x0 = cx + (tx - cx) * t0 + math.sin(t0 * 1.2) * 14 * s
        y0 = base - (base - ty) * t0
        x1 = cx + (tx - cx) * t1 + math.sin(t1 * 1.2) * 14 * s
        y1 = base - (base - ty) * t1
        d.line([(x0, y0), (x1, y1)], fill=PALM, width=int(13 * s))
    for k in range(7):
        ang = -170 + k * 26  # spread of fronds around the crown
        r = math.radians(ang)
        # frond: out along the angle, then drooping down
        px, py = tx, ty
        for j in range(1, 13):
            t = j / 12
            ex = tx + math.cos(r) * 105 * s * t
            ey = ty + math.sin(r) * 40 * s * t + 95 * s * t * t
            d.line([(px, py), (ex, ey)], fill=PALM, width=int(7 * s))
            px, py = ex, ey


palm(85, 705, 1.0, 30)
palm(940, 705, 0.9, -25)

# --- ground ---
for y in range(700, H):
    d.line([(0, y), (W, y)], fill=lerp((26, 11, 46), (14, 6, 26), (y - 700) / 324))

# --- couch ---
d.rounded_rectangle([70, 770, 640, 925], radius=28, fill=(122, 31, 61),
                    outline=(60, 12, 30), width=5)
d.rounded_rectangle([95, 745, 330, 830], radius=22, fill=(146, 40, 76),
                    outline=(60, 12, 30), width=4)
d.rounded_rectangle([360, 745, 615, 830], radius=22, fill=(146, 40, 76),
                    outline=(60, 12, 30), width=4)
d.rectangle([70, 880, 640, 925], fill=(100, 24, 50))

# --- skeleton, slumped on the couch ---
SK = (240, 238, 230)
SKO = (20, 18, 22)


def sk_line(p1, p2, w):
    d.line([p1, p2], fill=SKO, width=w + 6)
    d.line([p1, p2], fill=SK, width=w)


# legs stretched out
sk_line((300, 880), (180, 915), 16)
sk_line((380, 880), (520, 915), 16)
d.ellipse([150, 900, 195, 930], fill=SK, outline=SKO, width=4)  # shoe
d.ellipse([505, 900, 550, 930], fill=SK, outline=SKO, width=4)  # shoe
# spine + ribs
sk_line((335, 800), (335, 885), 14)
for i, ry in enumerate((815, 840, 865)):
    d.arc([300, ry, 372, ry + 34], start=0, end=180, fill=SK, width=10)
# arms to the controller
sk_line((320, 815), (255, 875), 12)
sk_line((352, 815), (415, 875), 12)
# controller
d.rounded_rectangle([235, 862, 440, 912], radius=16, fill=(40, 38, 48),
                    outline=(15, 14, 18), width=4)
d.ellipse([255, 872, 275, 892], fill=(120, 120, 130))
d.ellipse([395, 872, 415, 892], fill=(120, 120, 130))
d.ellipse([300, 880, 312, 892], fill=(255, 217, 77))
d.ellipse([330, 880, 342, 892], fill=(255, 80, 120))
# skull
d.ellipse([278, 700, 392, 800], fill=SK, outline=SKO, width=5)
d.rounded_rectangle([305, 778, 368, 812], radius=8, fill=SK, outline=SKO, width=4)
d.ellipse([298, 732, 330, 762], fill=(12, 10, 14))  # left eye
d.ellipse([344, 732, 376, 762], fill=(12, 10, 14))  # right eye
d.polygon([(336, 772), (328, 786), (344, 786)], fill=(12, 10, 14))  # nose
for tx in (318, 332, 346, 360):
    d.line([(tx, 790), (tx, 806)], fill=SKO, width=2)
# (no cobweb: the stray line read as a squiggle at small size)

# --- torn calendar page: 2013, crossed out ---
cal = Image.new("RGBA", (190, 220), (0, 0, 0, 0))
cd = ImageDraw.Draw(cal)
cd.rounded_rectangle([6, 6, 184, 214], radius=10, fill=(245, 244, 238, 255),
                     outline=(30, 28, 32, 255), width=4)
cd.rounded_rectangle([6, 6, 184, 52], radius=10, fill=(214, 48, 49, 255))
cd.rectangle([6, 40, 184, 52], fill=(214, 48, 49, 255))
cd.text((95, 120), "2013", font=font(64), fill=(40, 38, 44, 255), anchor="mm")
for gy in (150, 175, 200):
    cd.line([(30, gy), (160, gy)], fill=(180, 178, 170, 255), width=3)
cd.line([(25, 80), (165, 200)], fill=(214, 48, 49, 255), width=10)
cd.line([(165, 80), (25, 200)], fill=(214, 48, 49, 255), width=10)
cal = cal.rotate(-12, expand=True, resample=Image.BICUBIC)
img.paste(cal, (600, 210), cal)

# --- make.fun ghost, worked into the scene ---
ghost = Image.new("RGBA", (340, 380), (0, 0, 0, 0))
gd = ImageDraw.Draw(ghost)


def ghost_shape(draw, dx, dy, fill):
    # dome + body + wavy hem, drawn as one filled shape
    draw.pieslice([40 + dx, 10 + dy, 300 + dx, 270 + dy], start=180, end=360,
                  fill=fill)
    draw.rectangle([40 + dx, 140 + dy, 300 + dx, 320 + dy], fill=fill)
    for i, cx in enumerate((75, 135, 195, 255)):
        draw.ellipse([cx - 32 + dx, 300 + dy, cx + 32 + dy, 352 + dy], fill=fill)


# thick black outline: stamp the shape offset in all directions, then white
for ox, oy in [(x, y) for x in (-7, 0, 7) for y in (-7, 0, 7)]:
    ghost_shape(gd, ox, oy, (12, 10, 14, 255))
ghost_shape(gd, 0, 0, (255, 255, 255, 255))


def sparkle(draw, cx, cy, r, fill):
    pts = []
    for i in range(8):
        ang = math.pi / 2 + i * math.pi / 4
        rr = r if i % 2 == 0 else r * 0.28
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    draw.polygon(pts, fill=fill)


sparkle(gd, 130, 165, 34, (12, 10, 14, 255))
sparkle(gd, 212, 165, 34, (12, 10, 14, 255))
# little round hand
gd.ellipse([292, 235, 332, 275], fill=(255, 255, 255, 255),
           outline=(12, 10, 14, 255), width=5)
# magenta coin with white star, held in the hand
gd.ellipse([268, 268, 336, 336], fill=(230, 0, 126, 255),
           outline=(12, 10, 14, 255), width=5)


def star(draw, cx, cy, r, fill):
    pts = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.42
        pts.append((cx + math.cos(ang) * rr, cy + math.sin(ang) * rr))
    draw.polygon(pts, fill=fill)


star(gd, 302, 302, 22, (255, 255, 255, 255))
img.paste(ghost, (660, 480), ghost)

# --- top text ---
def outline_text(text, y, size):
    f = font(size)
    d.text((W // 2, y), text, font=f, fill=(255, 255, 255), anchor="ma",
           stroke_width=6, stroke_fill=(12, 10, 14))


outline_text("WAITED 13 YEARS", 28, 78)
outline_text("FOR GTA 6", 112, 78)

# --- bottom banner: the make.fun pitch, in the meme's own voice ---
d.rectangle([0, 930, W, H], fill=(230, 0, 126))
d.text((W // 2, 977), "MY AGENT EARNED MY COPY ON MAKE.FUN", font=font(40),
       fill=(255, 255, 255), anchor="mm")

img.save("/home/hatch/workspace/makefun/meme/meme.png")
small = img.resize((480, 480), Image.LANCZOS)
small.save("/home/hatch/workspace/makefun/meme/meme-480.png")
print("saved meme.png and meme-480.png")
