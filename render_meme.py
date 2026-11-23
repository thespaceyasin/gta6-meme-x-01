#!/usr/bin/env python3
"""Render the gta6-meme-x-01 meme: Vice City Superior Court verdict.
Programmatic PIL render (no image generator) so every word is spelled right.
Square 1024x1024, readable at 480x480.

TEXT VARIANTS DRAFTED IN-SESSION (no em dashes anywhere):

Variant A (task brief, plain):
  CHARGE: KEEPING US WAITING 4,811 DAYS SINCE 17 SEP 2013
  Delay No. 1, Fall 2025: GUILTY
  Delay No. 2, May 2026: GUILTY
  214 GB download: TIME SERVED
  Price $79.99: PAID
  SENTENCE: GRAND THEFT AUTO VI, SERVED IMMEDIATELY, 19 NOV 2026

Variant B (sharper, adds Jason and Lucia, hard drive joke):
  Count 1, Fall 2025 delay: GUILTY
  Count 2, May 2026 delay: GUILTY
  Count 3, 214 GB download: GUILTY, my hard drive pleads no contest
  Count 4, $79.99 price: PAID IN FULL
  SENTENCE: Jason and Lucia walk free in Vice City, 19 Nov 2026

Variant C (courtroom voice, fines punchline):
  The court finds the defendant guilty on all counts.
  Count 1: Promised Fall 2025, delivered May 2026. GUILTY.
  Count 2: 4,811 days of waiting. GUILTY.
  Count 3: A 214 GB download on launch day. GUILTY.
  FINE: $79.99. Paid in full by my AI agent.

CHOSEN: Variant A lines (cleanest itemized bill, matches the winning
formula) with Variant B's sentence (Jason and Lucia named) and
"PAID IN FULL" for the price. The fines-paid-by-agent punchline lives
in the bottom magenta banner, in the document's own voice.
"""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

REPO = "/home/hatch/workspace/makefun/entries/gta6-meme-x-01"
MARK = "/home/hatch/workspace/makefun/scratch/gta6-meme-x-01/mark-1024.png"
OUT = REPO + "/meme.png"

W = H = 1024
PAPER = (247, 241, 220)
NAVY = (31, 42, 68)
RED = (200, 16, 46)
MAGENTA = (196, 28, 131)
GOLD = (176, 141, 60)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def extract_ghost():
    """Cut the white ghost (and its magenta star coin) out of the mark disc.

    Mask: white body and dark outline only (magenta is left out: the disc
    magenta inside the coin circle bridged the coin outline to the outer
    ring and leaked the fill). Flood-fill from the ghost centre keeps
    only the ghost component, so the magenta disc and its black ring are
    dropped. The source PNG's alpha channel is honoured: its transparent
    corners read as black RGB, so they must not count as dark pixels.
    Pixels are capped to radius 410 of the disc centre (ghost outline
    ends near 397, the ring starts near 420), so the ring can never leak
    in. The star coin is then drawn back by hand: a magenta disc with a
    white star, inside the coin's own black outline.
    """
    im = Image.open(MARK).convert("RGBA")
    px = im.load()
    mask = Image.new("L", im.size, 0)
    mp = mask.load()
    for y in range(im.size[1]):
        for x in range(im.size[0]):
            r, g, b, a = px[x, y]
            if a < 128:
                continue
            if (x - 512) ** 2 + (y - 512) ** 2 >= 410 * 410:
                continue
            white = r > 200 and g > 200 and b > 200
            dark = r < 95 and g < 95 and b < 95
            if white or dark:
                mp[x, y] = 255
    ImageDraw.floodfill(mask, (512, 512), 128)
    alpha = mask.point(lambda v: 255 if v == 128 else 0)
    ghost = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ghost.paste(im, (0, 0), alpha)
    # Redraw the star coin inside its black outline.
    gd = ImageDraw.Draw(ghost)
    ccx, ccy, ccr = 790, 437, 126
    gd.ellipse([ccx - ccr, ccy - ccr, ccx + ccr, ccy + ccr],
               fill=(196, 28, 131, 255))
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 52 if i % 2 == 0 else 21
        star.append((ccx + rad * math.cos(ang), ccy + rad * math.sin(ang)))
    gd.polygon(star, fill=(255, 255, 255, 255))
    # Black ring around the coin, as in the mark.
    gd.ellipse([ccx - ccr - 6, ccy - ccr - 6, ccx + ccr + 6, ccy + ccr + 6],
               outline=(25, 20, 25, 255), width=10)
    bbox = alpha.getbbox()
    # FIX (user: the pink make.fun illustration was cut off): the redrawn
    # star coin reaches x=922, past the ghost body's own bbox (right edge
    # 901), so cropping to the body alone sliced 21 px off the pink coin's
    # right side. Widen the crop to the union of the body and the coin.
    bbox = (min(bbox[0], ccx - ccr - 6), min(bbox[1], ccy - ccr - 6),
            max(bbox[2], ccx + ccr + 6), max(bbox[3], ccy + ccr + 6))
    return ghost.crop(bbox)


def center(draw, y, text, fnt, fill):
    w = draw.textlength(text, font=fnt)
    draw.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    return w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # Document frame: navy double border.
    d.rectangle([12, 12, W - 13, H - 13], outline=NAVY, width=8)
    d.rectangle([30, 30, W - 31, H - 31], outline=NAVY, width=2)

    # Header.
    center(d, 46, "STATE OF LEONIDA", font(SERIF_B, 44), NAVY)
    center(d, 102, "VICE CITY SUPERIOR COURT", font(SERIF_B, 32), NAVY)
    d.line([70, 152, W - 70, 152], fill=NAVY, width=3)
    d.line([70, 158, W - 70, 158], fill=NAVY, width=1)

    center(d, 170, "VERDICT", font(SERIF_B, 66), NAVY)
    center(d, 244, "CASE NO. VI-13-1119", font(SANS, 24), NAVY)

    # Defendant and charge.
    center(d, 292, "THE PEOPLE OF LEONIDA v. ROCKSTAR GAMES",
           font(SANS_B, 25), NAVY)
    center(d, 330, "CHARGE: KEEPING US WAITING 4,811 DAYS", font(SANS, 23), NAVY)
    center(d, 360, "SINCE 17 SEP 2013", font(SANS, 23), NAVY)

    # Itemized counts with dotted leaders.
    rows = [
        ("Count 1. Fall 2025 delay", "GUILTY"),
        ("Count 2. May 2026 delay", "GUILTY"),
        ("Count 3. 214 GB download", "TIME SERVED"),
        ("Count 4. Price $79.99", "PAID IN FULL"),
    ]
    label_f = font(SANS, 26)
    verdict_f = font(SANS_B, 26)
    y = 402
    for label, verdict in rows:
        vw = d.textlength(verdict, font=verdict_f)
        vx = 655 - vw  # verdicts right-aligned at x=655
        d.text((70, y), label, font=label_f, fill=NAVY)
        lw = d.textlength(label, font=label_f)
        # dotted leader from label end to verdict start
        dot_y = y + 22
        x = 70 + lw + 12
        while x < vx - 10:
            d.ellipse([x, dot_y, x + 4, dot_y + 4], fill=(120, 110, 90))
            x += 12
        d.text((vx, y), verdict, font=verdict_f, fill=RED)
        y += 55

    # Ghost bailiff: NO robe. Yasin reviewed the meme twice and the black
    # judge robe read as the ghost being cut off at the waist (its top edge
    # sliced straight across the ghost's lower body), even though the ghost
    # itself was fully drawn. So the ghost stands complete on the bare
    # paper, nothing covering any part of it, and the court role comes from
    # a small wooden gavel resting on the paper below it instead.
    ghost = extract_ghost()
    gw, gh = ghost.size
    GH = 205
    GW = int(GH * gw / gh)
    gx = 800 - GW // 2
    gy = 388
    img.paste(ghost.resize((GW, GH), Image.LANCZOS), (gx, gy), ghost.resize((GW, GH), Image.LANCZOS))

    # Small wooden gavel resting on the paper below the ghost, clearly
    # separated from it (ghost bottom is gy+GH=593, gavel top is ~630).
    gavel = Image.new("RGBA", (170, 70), (0, 0, 0, 0))
    gd = ImageDraw.Draw(gavel)
    # handle
    gd.rounded_rectangle([8, 44, 150, 56], radius=6, fill=(122, 79, 42, 255))
    # head
    gd.rounded_rectangle([118, 8, 166, 52], radius=10, fill=(139, 90, 43, 255))
    gd.line([124, 18, 160, 18], fill=(90, 58, 26, 255), width=3)
    gd.line([124, 42, 160, 42], fill=(90, 58, 26, 255), width=3)
    gavel = gavel.rotate(18, expand=True, resample=Image.BICUBIC)
    img.paste(gavel, (710, 606), gavel)

    # Red GUILTY stamp, rotated, in the empty band below the counts and
    # above the sentence box. It overlaps nothing at all: not the ghost,
    # not the robe, not the sentence box. (Before, it sat on the ghost and
    # covered the ghost's lower body and robe, so the illustration looked
    # cut off.)
    stamp = Image.new("RGBA", (210, 86), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([5, 5, 205, 81], outline=RED + (235,), width=5)
    sd.rectangle([11, 11, 199, 75], outline=RED + (235,), width=2)
    sf = font(SANS_B, 36)
    tw = sd.textlength("GUILTY", font=sf)
    sd.text(((210 - tw) / 2, 22), "GUILTY", font=sf, fill=RED + (235,))
    stamp = stamp.rotate(-6, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (85, 596), stamp)

    # Sentence box (moved down 12 px to clear the stamp's band).
    d.rectangle([60, 708, 964, 812], outline=NAVY, width=3)
    center(d, 718, "SENTENCE", font(SANS_B, 18), NAVY)
    center(d, 740, "JASON AND LUCIA WALK FREE IN VICE CITY",
           font(SANS_B, 28), NAVY)
    center(d, 768, "19 NOV 2026", font(SANS_B, 34), RED)

    # Signature strip.
    d.line([70, 828, 420, 828], fill=NAVY, width=2)
    d.text((70, 836), "Signed, the Bailiff", font=font(SERIF, 22), fill=NAVY)
    d.text((640, 836), "BAILIFF OF THE COURT", font=font(SANS_B, 18), fill=NAVY)

    # Bottom magenta banner.
    d.rectangle([31, 892, 993, 993], fill=MAGENTA)
    d.text((60, 906), "FINES PAID BY MY AI AGENT", font=font(SANS_B, 30),
           fill=(255, 255, 255))
    d.text((60, 946), "with real money it won in make.fun bounties.",
           font=font(SANS, 23), fill=(255, 255, 255))
    # make.fun white pill logo.
    pill = Image.new("RGBA", (170, 56), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle([0, 0, 169, 55], radius=28, fill=(255, 255, 255))
    pf = font(SANS_B, 26)
    tw = pd.textlength("make.fun", font=pf)
    pd.text(((170 - tw) / 2, 12), "make.fun", font=pf, fill=MAGENTA)
    img.paste(pill, (800, 918), pill)

    img.save(OUT, "PNG")
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
