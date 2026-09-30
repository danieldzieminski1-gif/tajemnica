"""Generuje grafiki do gry (Pillow). Odpal: python make_assets.py
Chcesz własne obrazki? Podmień PNG w assets/ (te same nazwy)."""
import os
import random

from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 800, 600
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
os.makedirs(OUT, exist_ok=True)
random.seed(7)


def gradient(top, bot):
    im = Image.new("RGB", (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * t) for i in range(3)))
    return im


def overlay(im, draw_fn, blur=0):
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_fn(ImageDraw.Draw(layer))
    if blur:
        layer = layer.filter(ImageFilter.GaussianBlur(blur))
    im.paste(layer, (0, 0), layer)


def glow(im, x, y, r, color):
    overlay(im, lambda d: d.ellipse([x - r, y - r, x + r, y + r], fill=color), r / 2)


def stars(im, n=110):
    d = ImageDraw.Draw(im)
    for _ in range(n):
        x, y, r = random.randint(0, W), random.randint(0, H // 2), random.choice([1, 1, 2, 3])
        d.ellipse([x, y, x + r, y + r], fill=(255, 255, 225))


def moon(im, x=660, y=110):
    glow(im, x, y, 100, (255, 240, 170, 110))
    d = ImageDraw.Draw(im)
    d.ellipse([x - 40, y - 40, x + 40, y + 40], fill=(250, 245, 215))
    for cx, cy, r in [(-15, -12, 9), (12, 10, 12), (-5, 18, 6)]:
        d.ellipse([x + cx - r, y + cy - r, x + cx + r, y + cy + r], fill=(226, 220, 190))


def smoke(im, y, a=70, n=14):
    def f(d):
        for _ in range(n):
            x, w = random.randint(-100, W), random.randint(200, 400)
            d.ellipse([x, y + random.randint(-20, 20), x + w, y + 60 + random.randint(0, 40)],
                      fill=(190, 200, 220, a))
    overlay(im, f, 28)


def house(im, lit=True, day=False):
    d = ImageDraw.Draw(im)
    x0, x1, top, base = 190, 610, 170, 500
    d.rectangle([x0, top, x1, base], fill=(78, 68, 62) if day else (16, 16, 24))
    d.polygon([(x0 - 20, top), (x1 + 20, top), (x1 - 30, top - 50), (x0 + 30, top - 50)],
              fill=(60, 44, 44) if day else (10, 10, 15))
    for r in range(3):
        for c in range(5):
            wx, wy = x0 + 30 + c * 78, top + 25 + r * 95
            on = lit and r == 0 and c == 2
            col = (255, 214, 90) if on else ((90, 110, 130) if day else (7, 7, 11))
            d.rectangle([wx, wy, wx + 42, wy + 62], fill=col)
            if on:
                glow(im, wx + 21, wy + 31, 75, (255, 200, 70, 120))
    d.rectangle([x0 + 165, base - 90, x0 + 255, base], fill=(8, 8, 12))


def ground(im, col=(10, 14, 12)):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 500, W, H], fill=col)
    d.line([0, 485, W, 485], fill=(6, 6, 8), width=5)
    for x in range(0, W, 40):
        d.rectangle([x, 465, x + 6, 520], fill=(6, 6, 8))


def person(d, x, y, col=(4, 4, 6), run=False):
    d.ellipse([x - 14, y - 92, x + 14, y - 64], fill=col)
    d.line([x, y - 64, x, y - 20], fill=col, width=16)
    legs = [(x - 40, y + 40), (x + 35, y + 30)] if run else [(x - 12, y + 45), (x + 12, y + 45)]
    arms = [(x - 42, y - 35), (x + 40, y - 78)] if run else [(x - 25, y - 20), (x + 25, y - 20)]
    for lx, ly in legs:
        d.line([x, y - 20, lx, ly], fill=col, width=12)
    for ax, ay in arms:
        d.line([x, y - 58, ax, ay], fill=col, width=10)


def font(size):
    try:
        return ImageFont.load_default(size)
    except Exception:
        return ImageFont.load_default()


def budynek():
    im = gradient((5, 8, 25), (32, 32, 62))
    stars(im); moon(im); house(im); smoke(im, 470); ground(im)
    ImageDraw.Draw(im).text((30, 25), "02:30", fill=(120, 255, 150), font=font(48))
    return im


def schody():
    im = gradient((2, 2, 6), (14, 14, 22))
    d = ImageDraw.Draw(im)
    for i in range(9):
        d.rectangle([i * 88, 520 - i * 42, W, H], fill=(24 + i * 4, 22 + i * 4, 30 + i * 4))
        d.line([i * 88, 520 - i * 42, W, 520 - i * 42], fill=(60, 55, 70), width=3)
    overlay(im, lambda d: d.polygon([(30, 580), (800, 90), (800, 430)], fill=(255, 240, 170, 95)), 16)
    glow(im, 60, 570, 50, (255, 250, 200, 200))
    d = ImageDraw.Draw(im)
    for _ in range(60):
        x, y = random.randint(150, 780), random.randint(150, 500)
        d.ellipse([x, y, x + 2, y + 2], fill=(255, 245, 200))
    d.rectangle([700, 90, 800, 96], fill=(255, 210, 90))  # uchylone drzwi
    return im


def kot():
    im = gradient((10, 14, 30), (22, 26, 46))
    overlay(im, lambda d: d.polygon([(500, 0), (700, 0), (560, 480), (300, 480)], fill=(150, 180, 255, 55)), 10)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 480, W, H], fill=(14, 12, 18))
    d.rectangle([110, 390, 700, 415], fill=(64, 42, 30))
    d.rectangle([140, 415, 160, 480], fill=(45, 30, 24)); d.rectangle([650, 415, 670, 480], fill=(45, 30, 24))
    d.ellipse([230, 545, 340, 575], fill=(90, 40, 40)); d.rectangle([250, 520, 300, 555], fill=(120, 125, 135))
    c = (4, 4, 6)
    d.arc([150, 300, 250, 400], 90, 270, fill=c, width=14)
    d.ellipse([210, 335, 330, 400], fill=c); d.ellipse([300, 300, 370, 365], fill=c)
    d.polygon([(305, 312), (312, 278), (332, 305)], fill=c); d.polygon([(340, 305), (360, 278), (368, 315)], fill=c)
    for ex in (322, 348):
        d.ellipse([ex - 5, 326, ex + 5, 340], fill=(120, 255, 120))
    glow(im, 540, 368, 70, (120, 180, 255, 70))
    d = ImageDraw.Draw(im)
    d.rectangle([480, 340, 600, 392], fill=(38, 38, 44)); d.rectangle([500, 328, 540, 340], fill=(38, 38, 44))
    d.ellipse([518, 346, 562, 390], fill=(12, 12, 18), outline=(150, 160, 185), width=3)
    d.ellipse([528, 354, 538, 364], fill=(255, 255, 255))
    return im


def maska():
    im = gradient((26, 6, 12), (6, 2, 6))
    glow(im, 400, 290, 240, (255, 30, 30, 90))
    d = ImageDraw.Draw(im)
    d.polygon([(130, 600), (250, 420), (550, 420), (670, 600)], fill=(4, 4, 6))
    d.ellipse([310, 170, 490, 410], fill=(4, 4, 6))
    d.ellipse([335, 195, 465, 375], fill=(232, 232, 226))
    d.polygon([(350, 250), (395, 268), (385, 302), (350, 286)], fill=(0, 0, 0))
    d.polygon([(450, 250), (405, 268), (415, 302), (450, 286)], fill=(0, 0, 0))
    d.arc([355, 285, 445, 360], 20, 160, fill=(0, 0, 0), width=7)
    for x in range(372, 430, 12):
        d.line([x, 330, x, 345], fill=(0, 0, 0), width=3)
    d.rectangle([600, 500, 720, 575], fill=(30, 30, 36)); d.ellipse([640, 515, 690, 565], fill=(10, 10, 12))
    for r in (40, 65, 90):
        d.arc([665 - r, 540 - r, 665 + r, 540 + r], 200, 250, fill=(255, 90, 90), width=3)
    smoke(im, 380, 120, 20); smoke(im, 500, 130, 12)
    return im


def bieg():
    im = gradient((4, 4, 10), (14, 14, 22))
    d = ImageDraw.Draw(im)
    d.rectangle([430, 110, 730, 490], fill=(110, 140, 195))
    glow(im, 580, 300, 160, (170, 200, 255, 90))
    d = ImageDraw.Draw(im)
    for pts in ([(430, 110), (520, 110), (470, 200)], [(730, 490), (640, 490), (700, 400)],
                [(730, 110), (690, 110), (730, 190)], [(430, 490), (500, 490), (440, 420)]):
        d.polygon(pts, fill=(12, 12, 20))
    for i in range(6):
        y = 300 + i * 22
        d.line([60 + i * 10, y, 190 + i * 6, y], fill=(90, 100, 130), width=3)
    person(d, 300, 420, run=True)
    return im


def pokrzywy():
    im = gradient((6, 8, 26), (30, 40, 60))
    stars(im, 70); moon(im, 130, 100); ground(im, (12, 20, 14))
    d = ImageDraw.Draw(im)
    person(d, 640, 470)
    d.rectangle([665, 405, 685, 435], fill=(220, 235, 255))
    glow(im, 675, 420, 45, (200, 225, 255, 130))
    d = ImageDraw.Draw(im)
    d.ellipse([700, 400, 710, 410], fill=(255, 40, 40)); d.text((715, 395), "REC", fill=(255, 60, 60), font=font(22))
    d.ellipse([190, 470, 330, 520], fill=(4, 4, 6)); d.ellipse([320, 455, 355, 490], fill=(4, 4, 6))
    for _ in range(320):
        x, y = random.randint(0, 520), random.randint(450, 600)
        g = random.randint(80, 170)
        d.line([x, y, x + random.randint(-14, 14), y - random.randint(40, 110)], fill=(20, g, 35), width=3)
    d.text((80, 520), "AUUUU!", fill=(255, 240, 120), font=font(44))
    return im


def kamera():
    im = gradient((255, 175, 115), (150, 205, 240))
    glow(im, 130, 130, 120, (255, 240, 170, 170))
    d = ImageDraw.Draw(im)
    d.ellipse([100, 100, 160, 160], fill=(255, 250, 210))
    house(im, lit=False, day=True); ground(im, (62, 112, 62))
    d = ImageDraw.Draw(im)
    for x, w, h in [(80, 150, 90), (250, 120, 70), (560, 170, 100)]:
        d.rectangle([x, 540 - h, x + w, 540], fill=(45, 48, 55), outline=(190, 195, 205), width=4)
        d.line([x, 540 - h + 20, x + w, 540 - h + 20], fill=(190, 195, 205), width=2)
    d.ellipse([275, 480, 305, 510], fill=(20, 20, 24)); d.ellipse([610, 470, 650, 510], fill=(20, 20, 24))
    d.line([420, 400, 400, 545], fill=(30, 30, 34), width=6); d.line([420, 400, 445, 545], fill=(30, 30, 34), width=6)
    d.rectangle([395, 375, 450, 410], fill=(25, 25, 30)); d.ellipse([440, 385, 462, 405], fill=(15, 15, 20))
    d.ellipse([28, 28, 50, 50], fill=(230, 30, 30)); d.text((58, 24), "REC", fill=(255, 255, 255), font=font(34))
    return im



def wide(im):
    """4:3 -> 16:9: skalowanie do 960x720 + rozciągnięte, uśrednione brzegi."""
    s = im.resize((960, 720))

    def edge(box):
        return s.crop(box).resize((1, 720), Image.BOX).resize((160, 720))
    out = Image.new("RGB", (1280, 720))
    out.paste(edge((0, 0, 12, 720)), (0, 0))
    out.paste(edge((948, 0, 960, 720)), (1120, 0))
    out.paste(s, (160, 0))
    return out


def ziomek(expr):
    S = Image.new("RGBA", (500, 800), (0, 0, 0, 0))
    d = ImageDraw.Draw(S)
    skin, hoodie, dark = (247, 208, 182), (72, 92, 148), (35, 25, 35)
    d.rounded_rectangle([70, 370, 140, 720], 32, fill=(62, 80, 130))
    d.rounded_rectangle([360, 370, 430, 720], 32, fill=(62, 80, 130))
    d.rounded_rectangle([105, 330, 395, 800], 46, fill=hoodie)
    d.rounded_rectangle([170, 600, 330, 690], 20, fill=(60, 78, 125))
    d.line([225, 380, 225, 520], fill=(230, 230, 240), width=4)
    d.line([275, 380, 275, 520], fill=(230, 230, 240), width=4)
    d.ellipse([72, 700, 138, 765], fill=skin); d.ellipse([362, 700, 428, 765], fill=skin)
    d.rectangle([222, 300, 278, 370], fill=skin)
    d.ellipse([150, 100, 350, 340], fill=skin)
    hair = (38, 28, 30)
    d.pieslice([138, 80, 362, 300], 180, 360, fill=hair)
    d.polygon([(150, 200), (215, 130), (245, 200)], fill=hair)
    d.polygon([(245, 200), (300, 125), (352, 200)], fill=hair)
    d.polygon([(140, 190), (120, 260), (165, 230)], fill=hair)
    d.polygon([(360, 190), (380, 260), (335, 230)], fill=hair)
    for ex in (212, 288):
        if expr == "smiech":
            d.arc([ex - 26, 215, ex + 26, 265], 200, 340, fill=dark, width=7)
        else:
            r = 30 if expr == "strach" else 26
            d.ellipse([ex - r, 232 - r, ex + r, 232 + r], fill=(255, 255, 255), outline=dark, width=4)
            if expr == "strach":
                d.ellipse([ex - 7, 225, ex + 7, 239], fill=dark)
            else:
                d.ellipse([ex - 16, 214, ex + 16, 254], fill=(70, 130, 210))
                d.ellipse([ex - 8, 224, ex + 8, 244], fill=dark)
                d.ellipse([ex - 12, 218, ex - 2, 228], fill=(255, 255, 255))
    by = 195 if expr == "strach" else 205
    d.line([182, by, 240, by - 10 if expr == "strach" else by], fill=dark, width=5)
    d.line([260, by - 10 if expr == "strach" else by, 318, by], fill=dark, width=5)
    if expr == "strach":
        d.ellipse([238, 290, 262, 320], fill=(90, 30, 40))
        d.ellipse([170, 130, 180, 150], fill=(150, 210, 255))
    elif expr == "smiech":
        d.pieslice([215, 270, 285, 320], 0, 180, fill=(120, 30, 50))
        d.ellipse([170, 262, 200, 280], fill=(255, 150, 160)); d.ellipse([300, 262, 330, 280], fill=(255, 150, 160))
    else:
        d.arc([225, 275, 275, 305], 20, 160, fill=dark, width=4)
    return S


def icon():
    return budynek().crop((100, 0, 700, 600)).resize((512, 512))


for name, fn in [("budynek", budynek), ("schody", schody), ("kot", kot), ("maska", maska),
                 ("bieg", bieg), ("pokrzywy", pokrzywy), ("kamera", kamera)]:
    wide(fn()).save(os.path.join(OUT, name + ".png"))
    print("ok", name)
icon().save(os.path.join(OUT, "icon.png"))
for e in ("ok", "strach", "smiech"):
    ziomek(e).save(os.path.join(OUT, f"ziomek_{e}.png"))
