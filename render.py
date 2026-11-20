#!/usr/bin/env python3
"""Render entry.png: a one-page newspaper front page summing up the world news
of Thursday 19 November 2026. Built with Pillow at build time; the graded
program (main.py) only copies the finished PNG. All facts were checked against
same-day reporting (UN News, BBC, Le Monde, AP/10things, Foreign Exchanges)
on 20 November 2026.
"""
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 229)
INK = (26, 26, 26)
RED = (163, 18, 18)
BLUE = (31, 58, 95)
PANEL = (255, 253, 246)
GREY = (90, 86, 76)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill=INK, leading=1.25):
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += int(fnt.size * leading)
    return y


def panel(draw, x, y, w, h, kicker=None):
    draw.rectangle([x, y, x + w, y + h], fill=PANEL, outline=INK, width=2)
    if kicker:
        draw.text((x + 14, y + 10), kicker, font=font(SANS_B, 17), fill=RED)
        return y + 36
    return y + 14


def draw_scales(draw, cx, cy, s, color=INK):
    # Scales of justice: post, beam, two pans.
    draw.line([(cx, cy - 70 * s), (cx, cy + 70 * s)], fill=color, width=int(6 * s))
    draw.line([(cx - 75 * s, cy - 45 * s), (cx + 75 * s, cy - 45 * s)],
              fill=color, width=int(6 * s))
    draw.ellipse([cx - 7 * s, cy - 78 * s, cx + 7 * s, cy - 64 * s], fill=color)
    for dx in (-75, 75):
        px = cx + dx * s
        draw.line([(px, cy - 45 * s), (px - 28 * s, cy + 5 * s)], fill=color, width=int(4 * s))
        draw.line([(px, cy - 45 * s), (px + 28 * s, cy + 5 * s)], fill=color, width=int(4 * s))
        draw.arc([px - 32 * s, cy - 12 * s, px + 32 * s, cy + 28 * s], 0, 180,
                 fill=color, width=int(4 * s))
        draw.line([(px - 32 * s, cy + 8 * s), (px + 32 * s, cy + 8 * s)],
                  fill=color, width=int(4 * s))
    draw.line([(cx - 45 * s, cy + 70 * s), (cx + 45 * s, cy + 70 * s)],
              fill=color, width=int(6 * s))


def draw_flag(draw, x, y, w, h, kind):
    if kind == "us":
        for i in range(7):
            draw.rectangle([x, y + i * h / 7, x + w, y + (i + 1) * h / 7],
                           fill=(178, 34, 52) if i % 2 == 0 else (255, 255, 255))
        draw.rectangle([x, y, x + w * 0.4, y + h * 4 / 7], fill=(30, 50, 110))
        for r in range(3):
            for c in range(4):
                draw.ellipse([x + 8 + c * 22, y + 8 + r * 16,
                              x + 14 + c * 22, y + 14 + r * 16], fill=(255, 255, 255))
    elif kind == "cn":
        draw.rectangle([x, y, x + w, y + h], fill=(222, 41, 16))
        draw.ellipse([x + 10, y + 8, x + 26, y + 24], fill=(255, 222, 0))
    elif kind == "ru":
        draw.rectangle([x, y, x + w, y + h / 3], fill=(255, 255, 255))
        draw.rectangle([x, y + h / 3, x + w, y + 2 * h / 3], fill=(0, 57, 166))
        draw.rectangle([x, y + 2 * h / 3, x + w, y + h], fill=(213, 0, 50))
    draw.rectangle([x, y, x + w, y + h], outline=INK, width=2)


def draw_globe(draw, cx, cy, r, color=BLUE):
    draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=color, width=4)
    draw.ellipse([cx - r * 0.55, cy - r, cx + r * 0.55, cy + r], outline=color, width=2)
    draw.line([(cx - r, cy), (cx + r, cy)], fill=color, width=2)
    draw.arc([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], 200, 340, fill=color, width=2)
    draw.arc([cx - r, cy - r * 0.5, cx + r, cy + r * 0.5], 20, 160, fill=color, width=2)


def draw_chart(draw, x, y, w, h, color=(34, 120, 60)):
    pts = [(x, y + h * 0.8), (x + w * 0.3, y + h * 0.65), (x + w * 0.55, y + h * 0.7),
           (x + w * 0.8, y + h * 0.3), (x + w, y + h * 0.12)]
    draw.line(pts, fill=color, width=5, joint="curve")
    ax, ay = pts[-1]
    draw.polygon([(ax, ay), (ax - 16, ay + 2), (ax - 2, ay + 16)], fill=color)
    draw.line([(x, y + h), (x + w, y + h)], fill=INK, width=2)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 36  # margin

    # ---- Masthead ----
    d.text((M, 22), "THE WORLD IN ONE IMAGE", font=font(SERIF_B, 56), fill=INK)
    d.text((M, 92), "THURSDAY  \u00b7  19 NOVEMBER 2026", font=font(SANS_B, 40), fill=RED)
    d.line([(M, 150), (W - M, 150)], fill=INK, width=4)
    d.line([(M, 158), (W - M, 158)], fill=INK, width=1)

    # ---- Lead story: ICJ / Myanmar ----
    ly, lh = 172, 272
    d.rectangle([M, ly, W - M, ly + lh], fill=PANEL, outline=INK, width=3)
    d.text((M + 16, ly + 12), "THE HAGUE  \u00b7  LEAD STORY", font=font(SANS_B, 18), fill=RED)
    tx = M + 16
    ty = text_block(d, tx, ly + 44,
                    wrap(d, "WORLD COURT: MYANMAR", font(SANS_B, 36), 620), font(SANS_B, 36), leading=1.05)
    ty = text_block(d, tx, ty + 2,
                    wrap(d, "COMMITTED GENOCIDE", font(SANS_B, 36), 620), font(SANS_B, 36), leading=1.05)
    ty = text_block(d, tx, ty + 10,
                    wrap(d, "The International Court of Justice finds the state "
                            "responsible for the 2017 crackdown on the Rohingya "
                            "\u2014 the first genocide ruling ever against a state. "
                            "Vote: 9\u20136.", font(SANS, 22), 620), font(SANS, 22))
    draw_scales(d, 830, ly + 150, 1.05)

    # ---- Row 2: two panels ----
    ry, rh, gap = 464, 226, 20
    pw = (W - 2 * M - gap) // 2
    # Panel A: Shenzhen summit
    y = panel(d, M, ry, pw, rh, "SHENZHEN  \u00b7  SUMMIT")
    y = text_block(d, M + 14, y,
                   wrap(d, "TRUMP, XI AND PUTIN MEET", font(SANS_B, 27), pw - 28),
                   font(SANS_B, 27), leading=1.05)
    y = text_block(d, M + 14, y + 6,
                   wrap(d, "First-ever trilateral summit ends with a four-point "
                           "\u201cDeclaration toward Peace\u201d; APEC adopts its "
                           "Shenzhen Outlook on trade, data and AI.",
                        font(SANS, 20), pw - 28), font(SANS, 20))
    fx, fy = M + 14, ry + rh - 52
    draw_flag(d, fx, fy, 92, 40, "us")
    draw_flag(d, fx + 104, fy, 92, 40, "cn")
    draw_flag(d, fx + 208, fy, 92, 40, "ru")
    # Panel B: Gulf
    x2 = M + pw + gap
    y = panel(d, x2, ry, pw, rh, "THE GULF  \u00b7  ON EDGE")
    y = text_block(d, x2 + 14, y,
                   wrap(d, "IRAN WIDENS ITS STRIKES", font(SANS_B, 27), pw - 28),
                   font(SANS_B, 27), leading=1.05)
    y = text_block(d, x2 + 14, y + 6,
                   wrap(d, "Tehran hits Kuwait and Bahrain as the US blockade "
                           "holds. The Senate rejects a war-powers curb, 51\u201348; "
                           "Trump: \u201csee what happens after January 1.\u201d",
                        font(SANS, 20), pw - 28), font(SANS, 20))
    draw_globe(d, x2 + pw - 62, ry + rh - 48, 30)

    # ---- Row 3: three panels ----
    ry3, rh3 = 710, 178
    pw3 = (W - 2 * M - 2 * gap) // 3
    # Ukraine
    y = panel(d, M, ry3, pw3, rh3, "UKRAINE")
    y = text_block(d, M + 12, y,
                   wrap(d, "EU PROPOSES \u20ac45BN LOAN", font(SANS_B, 22), pw3 - 24),
                   font(SANS_B, 22), leading=1.05)
    text_block(d, M + 12, y + 4,
               wrap(d, "UK and Norway fund two naval craft; Denmark backs the "
                       "Greenland defence pact, 109\u20130.",
                    font(SANS, 18), pw3 - 24), font(SANS, 18))
    # Gaza
    x3 = M + pw3 + gap
    y = panel(d, x3, ry3, pw3, rh3, "GAZA")
    y = text_block(d, x3 + 12, y,
                   wrap(d, "ISRAEL CROSSES CEASEFIRE LINE", font(SANS_B, 22), pw3 - 24),
                   font(SANS_B, 22), leading=1.05)
    text_block(d, x3 + 12, y + 4,
               wrap(d, "Nuseirat ground operation ends; aid groups score the "
                       "peace plan 4 out of 26.",
                    font(SANS, 18), pw3 - 24), font(SANS, 18))
    # Markets & space
    x4 = M + 2 * (pw3 + gap)
    y = panel(d, x4, ry3, pw3, rh3, "MARKETS & SPACE")
    y = text_block(d, x4 + 12, y,
                   wrap(d, "ANTHROPIC HITS ~$2 TRILLION", font(SANS_B, 22), pw3 - 24),
                   font(SANS_B, 22), leading=1.05)
    text_block(d, x4 + 12, y + 4,
               wrap(d, "Record Nasdaq debut. Voyager 1 reaches one light-day "
                       "from Earth.",
                    font(SANS, 18), pw3 - 24), font(SANS, 18))
    draw_chart(d, x4 + pw3 - 108, ry3 + rh3 - 46, 92, 34)

    # ---- Ticker ----
    ty2 = 906
    d.line([(M, ty2), (W - M, ty2)], fill=INK, width=2)
    text_block(d, M, ty2 + 12,
               wrap(d, "ALSO ON 19 NOVEMBER:  Cyclone Akvan nears India\u2019s "
                       "east coast  \u00b7  Mongolia\u2019s president resigns  \u00b7  "
                       "Ethiopia and Eritrea mass troops  \u00b7  Van Gogh sells "
                       "for a record $190.4m",
                    font(SANS, 19), W - 2 * M), font(SANS, 19))
    d.line([(M, 974), (W - M, 974)], fill=INK, width=1)
    ftr = "19 NOVEMBER 2026  \u00b7  THE DAY\u2019S WORLD NEWS IN ONE IMAGE"
    d.text(((W - d.textlength(ftr, font=font(SANS_B, 17))) / 2, 984),
           ftr, font=font(SANS_B, 17), fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png")


if __name__ == "__main__":
    main()
