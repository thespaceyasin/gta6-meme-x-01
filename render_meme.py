#!/usr/bin/env python3
"""Render the gta6-meme-x-01 meme, v3: Vice City Impound Lot release form.

Yasin: the court verdict version was still ugly, redo everything to match
ranks 1-3. What ranks 1-3 actually do (analysis of their images):

- Rank 1 (90.80%, eviction notice), rank 2 (90.38%, rental return
  receipt), rank 3 (90.38%, funeral obituary): all are ONE fake official
  document filling the whole square, cream paper, huge bold title,
  itemized charges with dotted leaders and exact numbers (4,811 days,
  Fall 2025 and May 2026 as line items, $79.99, 214 GB, Jason and Lucia),
  a big red stamp (PAID / 13 YEARS LATE), and the make.fun ghost worked
  in LARGE (rank 2: ghost ~40% of the image height, bottom left, holding
  its pink coin, overlapping the receipt edge; rank 3: ghost as a
  character stamping PAID). Bottom magenta banner inside the image:
  "PAID BY MY AI AGENT with real money it won in make.fun bounties."
  plus the white make.fun pill. The pitch IS the punchline.
- The court version failed that formula: centered text, big empty cream
  areas, a small ghost tucked in a corner, a stamp floating in empty
  space, a pasted-on gavel. This version copies the winners' density:
  black header band, huge two-line title, fields grid, six itemized
  charges, total, big red RELEASED stamp, a LARGE ghost bottom left
  overlapping the banner like rank 2, magenta banner with the winners'
  exact pitch wording.

Fresh document type (none of the top 20 uses it): a vehicle release
form from the Vice City impound lot. The car waited 13 years too.
No em dashes anywhere. Programmatic PIL render, 1024x1024, readable
at 480x480, every word spelled right.
"""
import math
from PIL import Image, ImageDraw, ImageFont

REPO = "/home/hatch/workspace/makefun/entries/gta6-meme-x-01"
MARK = "/home/hatch/workspace/makefun/scratch/gta6-meme-x-01/mark-1024.png"
OUT = REPO + "/meme.png"

W = H = 1024
PAPER = (247, 241, 220)
NAVY = (31, 42, 68)
INK = (20, 20, 28)
RED = (200, 16, 46)
MAGENTA = (196, 28, 131)
GOLD = (212, 175, 55)

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
    white star, inside the coin's own black outline. The crop is the
    union of the body bbox and the coin circle, so the pink coin is never
    clipped. The extracted ghost is COMPLETE: rounded bottom with its
    two lobes, both sparkle eyes, little hand, full pink coin.
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

    # Black header band, rank 2 style.
    d.rectangle([31, 31, 993, 148], fill=INK)
    d.text((58, 46), "CITY OF VICE CITY", font=font(SANS_B, 26),
           fill=(255, 255, 255))
    d.text((58, 82), "DEPT. OF PARKING AND TOWING", font=font(SANS, 20),
           fill=(200, 200, 210))
    d.text((58, 108), "IMPOUND LOT 13  •  FORM 13-VI", font=font(SANS_B, 22),
           fill=GOLD)
    # Magenta LOT 13 box, right side of the band, text centered in it.
    d.rounded_rectangle([820, 52, 966, 126], radius=10, fill=MAGENTA)
    lot_f = font(SANS_B, 32)
    lot = "LOT 13"
    lw = d.textlength(lot, font=lot_f)
    d.text((820 + (146 - lw) / 2, 68), lot, font=lot_f,
           fill=(255, 255, 255))

    # Huge two-line title, rank 1 style.
    center(d, 162, "IMPOUNDED 4,811 DAYS.", font(SANS_B, 46), NAVY)
    center(d, 214, "RELEASED TODAY.", font(SANS_B, 46), RED)

    # Fields grid: three rows, two columns.
    fields = [
        ("VEHICLE:  WHITE INFERNUS", "PLATE:  LUCIA-6"),
        ("OWNER:  JASON AND LUCIA", "IMPOUNDED:  17 SEP 2013"),
        ("RELEASED:  19 NOV 2026", "KEYS:  JASON AND LUCIA"),
    ]
    fy = 272
    for left, right in fields:
        d.text((70, fy), left, font=font(SANS_B, 21), fill=NAVY)
        d.text((560, fy), right, font=font(SANS_B, 21), fill=NAVY)
        fy += 32
    d.line([70, 368, 954, 368], fill=NAVY, width=2)

    # Itemized charges with dotted leaders, rank 1 and 2 style.
    # 250 + 4811 + 130 + 26 + 250 + 137 = 5604.
    rows = [
        ("Towing, 17 Sep 2013", "$250.00"),
        ("Storage, $1.00 a day, 4,811 days", "$4,811.00"),
        ('"Coming soon" fee, Fall 2025', "$130.00"),
        ("Reschedule fee, May 2026", "$26.00"),
        ("Alligator in the back seat", "$250.00"),
        ("Dust removal, 13 years", "$137.00"),
    ]
    label_f = font(SANS, 24)
    amount_f = font(SANS_B, 24)
    y = 384
    for label, amount in rows:
        aw = d.textlength(amount, font=amount_f)
        ax = 954 - aw
        d.text((70, y), label, font=label_f, fill=NAVY)
        lw = d.textlength(label, font=label_f)
        dot_y = y + 19
        x = 70 + lw + 12
        while x < ax - 10:
            d.ellipse([x, dot_y, x + 4, dot_y + 4], fill=(120, 110, 90))
            x += 12
        d.text((ax, y), amount, font=amount_f, fill=NAVY)
        y += 34
    # Total.
    d.line([70, 592, 954, 592], fill=NAVY, width=2)
    d.text((70, 604), "TOTAL DUE", font=font(SANS_B, 32), fill=NAVY)
    tot = "$5,604.00"
    tw = d.textlength(tot, font=font(SANS_B, 34))
    d.text((954 - tw, 602), tot, font=font(SANS_B, 34), fill=RED)
    d.text((70, 646), "($1.00 for every day you waited.)",
           font=font(SERIF, 20), fill=NAVY)

    # Big red RELEASED stamp, right side, clear of the ghost and the total.
    stamp = Image.new("RGBA", (300, 120), (0, 0, 0, 0))
    sd = ImageDraw.Draw(stamp)
    sd.rectangle([5, 5, 295, 115], outline=RED + (235,), width=6)
    sd.rectangle([12, 12, 288, 108], outline=RED + (235,), width=2)
    sf = font(SANS_B, 44)
    tw = sd.textlength("RELEASED", font=sf)
    sd.text(((300 - tw) / 2, 32), "RELEASED", font=sf, fill=RED + (235,))
    stamp = stamp.rotate(-12, expand=True, resample=Image.BICUBIC)
    img.paste(stamp, (620, 690), stamp)

    # Bottom magenta banner, winners' pitch wording. The ghost overlaps
    # its left part, rank 2 style. The make.fun pill sits at the right, so
    # both text lines are auto-fit to the window between the ghost and the
    # pill (x 420 to 800): measure and shrink the font until each line fits,
    # never let the pill cover any letter.
    d.rectangle([31, 892, 993, 993], fill=MAGENTA)
    bx, bw = 420, 380
    head = "PAID BY MY AI AGENT"
    hs = 30
    while d.textlength(head, font=font(SANS_B, hs)) > bw and hs > 18:
        hs -= 1
    d.text((bx, 906), head, font=font(SANS_B, hs), fill=(255, 255, 255))
    sub = "with real money it won on make.fun"
    ss = 23
    while d.textlength(sub, font=font(SANS, ss)) > bw and ss > 16:
        ss -= 1
    d.text((bx, 946), sub, font=font(SANS, ss), fill=(255, 255, 255))
    # make.fun white pill logo.
    pill = Image.new("RGBA", (170, 56), (0, 0, 0, 0))
    pd = ImageDraw.Draw(pill)
    pd.rounded_rectangle([0, 0, 169, 55], radius=28, fill=(255, 255, 255))
    pf = font(SANS_B, 26)
    tw = pd.textlength("make.fun", font=pf)
    pd.text(((170 - tw) / 2, 12), "make.fun", font=pf, fill=MAGENTA)
    img.paste(pill, (815, 918), pill)

    # LARGE ghost, bottom left, rank 2 style: ~27% of the image height,
    # holding its pink coin, pasted LAST so it sits on top of the banner
    # edge and nothing covers any part of it. Whole body, rounded bottom,
    # both sparkle eyes, little hand, full pink coin. Its top clears the
    # total note below the charges, so it covers no text at all.
    ghost = extract_ghost()
    gw, gh = ghost.size
    GH = 280
    GW = int(GH * gw / gh)
    gx = 50
    gy = 675
    img.paste(ghost.resize((GW, GH), Image.LANCZOS), (gx, gy),
              ghost.resize((GW, GH), Image.LANCZOS))

    img.save(OUT, "PNG")
    print("saved", OUT, img.size)


if __name__ == "__main__":
    main()
