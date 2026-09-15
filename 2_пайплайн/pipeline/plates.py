#!/usr/bin/env python
"""Render transparent PNG overlays with Pillow: story lower-third plates and the
persistent "WEIRD NEWS USA" bug.

Run with: uv run --project ~/pet-projects/weirdnews-mpt/MoneyPrinterTurbo python 2_пайплайн/pipeline/plates.py \
    lower_third --number 1 --headline "Pentagon 9/11 gaffe" --out n1_lt.png
    bug --out bug.png
"""
import argparse
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from common import W, H, FONT  # noqa: E402

RED = (200, 30, 30, 255)
WHITE = (255, 255, 255, 255)
BLACK_BG = (10, 10, 10, 210)


def font(size):
    return ImageFont.truetype(FONT, size)


def lower_third(number, headline, out):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    plate_h = 140
    y0 = H - plate_h
    # dark translucent bar
    d.rectangle([0, y0, W, y0 + plate_h], fill=BLACK_BG)
    # red number block
    block_w = 150
    d.rectangle([0, y0, block_w, y0 + plate_h], fill=RED)
    numf = font(64)
    txt = f"#{number}"
    bbox = d.textbbox((0, 0), txt, font=numf)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    d.text((block_w / 2 - tw / 2, y0 + plate_h / 2 - th / 2 - bbox[1]), txt, font=numf, fill=WHITE)
    # headline
    headf = font(46)
    d.text((block_w + 30, y0 + plate_h / 2 - 46 / 2 - 6), headline, font=headf, fill=WHITE)

    img.save(out)
    return out


def bug(out, text="WEIRD NEWS USA"):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(28)
    pad = 12
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x1, y1 = W - 40, 40
    x0, y0 = x1 - tw - 2 * pad, y1
    d.rectangle([x0, y0, x1, y0 + th + 2 * pad], fill=BLACK_BG)
    d.text((x0 + pad, y0 + pad - bbox[1]), text, font=f, fill=WHITE)
    img.save(out)
    return out


def caption_box(text_lines, out, position="bottom", label=None):
    """SOT caption card: text lines + optional 'via <Outlet>' label. position: 'bottom'|'top'."""
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(48)
    line_h = 62
    n = len(text_lines)
    block_h = n * line_h + 40
    # bottom captions sit clear above the story-open lower third's zone (bottom 140px)
    y0 = (H - 160 - block_h) if position == "bottom" else 120
    d.rectangle([0, y0, W, y0 + block_h], fill=BLACK_BG)
    y = y0 + 20
    for line in text_lines:
        bbox = d.textbbox((0, 0), line, font=f)
        tw = bbox[2] - bbox[0]
        d.text((W / 2 - tw / 2, y), line, font=f, fill=WHITE)
        y += line_h
    if label:
        lf = font(30)
        d.rectangle([0, 0, 0, 0])  # no-op, label drawn separately by caller as top-left
    img.save(out)
    return out


def label_topleft(text, out):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    f = font(32)
    pad = 10
    bbox = d.textbbox((0, 0), text, font=f)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x0, y0 = 40, 40
    d.rectangle([x0, y0, x0 + tw + 2 * pad, y0 + th + 2 * pad], fill=RED)
    d.text((x0 + pad, y0 + pad - bbox[1]), text, font=f, fill=WHITE)
    img.save(out)
    return out


def title_card(out, title="TRUMP'S MONTH:", subtitle="THE GREATEST HITS"):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, H], fill=(5, 5, 5, 235))
    f1 = font(96)
    f2 = font(120)
    b1 = d.textbbox((0, 0), title, font=f1)
    b2 = d.textbbox((0, 0), subtitle, font=f2)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
    cy = H / 2
    d.text((W / 2 - w1 / 2, cy - h1 - h2 / 2 - 20), title, font=f1, fill=WHITE)
    d.text((W / 2 - w2 / 2, cy - h2 / 2 + 20), subtitle, font=f2, fill=RED)
    img.save(out)
    return out


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("lower_third")
    p.add_argument("--number", type=int, required=True)
    p.add_argument("--headline", required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("bug")
    p.add_argument("--out", required=True)
    p.add_argument("--text", default="WEIRD NEWS USA")

    p = sub.add_parser("label")
    p.add_argument("--text", required=True)
    p.add_argument("--out", required=True)

    p = sub.add_parser("title")
    p.add_argument("--out", required=True)
    p.add_argument("--title", default="TRUMP'S MONTH:")
    p.add_argument("--subtitle", default="THE GREATEST HITS")

    args = ap.parse_args()
    if args.cmd == "lower_third":
        lower_third(args.number, args.headline, args.out)
    elif args.cmd == "bug":
        bug(args.out, args.text)
    elif args.cmd == "label":
        label_topleft(args.text, args.out)
    elif args.cmd == "title":
        title_card(args.out, title=args.title, subtitle=args.subtitle)
    print(args.out)


if __name__ == "__main__":
    main()
