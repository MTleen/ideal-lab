#!/usr/bin/env python3
"""Build a side-by-side comparison PNG for visual fidelity verification.

Output: [source | rendered] with a 10% grid overlay, captioned, ready for
human/AI inspection per Step 2.5 of image-to-svg.

Usage:
    python3 compare_images.py --source src.png --rendered out.png --out cmp.png
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


GRID_COLOR = (200, 60, 60, 140)
LABEL_BG = (28, 32, 48)
LABEL_FG = (255, 255, 255)
GAP_PX = 24
LABEL_H = 56


def _font(size: int) -> ImageFont.ImageFont:
    # Try a few common CJK-capable fonts; fall back to PIL default.
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()


def _draw_grid(img: Image.Image, color=GRID_COLOR) -> None:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    w, h = img.size
    for i in range(1, 10):
        x = int(w * i / 10)
        y = int(h * i / 10)
        d.line([(x, 0), (x, h)], fill=color, width=1)
        d.line([(0, y), (w, y)], fill=color, width=1)
    img.alpha_composite(overlay)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--rendered", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--no-grid", action="store_true", help="disable 10% grid overlay")
    args = ap.parse_args()

    if not args.source.exists():
        print(f"[error] source not found: {args.source}", file=sys.stderr)
        return 2
    if not args.rendered.exists():
        print(f"[error] rendered not found: {args.rendered}", file=sys.stderr)
        return 2

    src = Image.open(args.source).convert("RGBA")
    ren = Image.open(args.rendered).convert("RGBA")

    h = max(src.height, ren.height)
    src_w = int(src.width * h / src.height)
    ren_w = int(ren.width * h / ren.height)
    src = src.resize((src_w, h), Image.LANCZOS)
    ren = ren.resize((ren_w, h), Image.LANCZOS)

    if not args.no_grid:
        _draw_grid(src)
        _draw_grid(ren)

    total_w = src_w + GAP_PX + ren_w
    total_h = h + LABEL_H
    canvas = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 255))

    label_strip = Image.new("RGBA", (total_w, LABEL_H), LABEL_BG)
    d = ImageDraw.Draw(label_strip)
    f = _font(22)
    d.text((src_w / 2 - 80, 14), "SOURCE", fill=LABEL_FG, font=f)
    d.text((src_w + GAP_PX + ren_w / 2 - 100, 14), "RENDERED", fill=LABEL_FG, font=f)
    canvas.paste(label_strip, (0, 0))

    canvas.paste(src, (0, LABEL_H), src)
    canvas.paste(ren, (src_w + GAP_PX, LABEL_H), ren)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(args.out, "PNG", optimize=True)
    print(f"[ok] compare -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
