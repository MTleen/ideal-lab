#!/usr/bin/env python3
"""Create same-canvas overlays for source-vs-rendered SVG verification.

The source image is scaled to the rendered PNG size. Output contains:
- left: source at full opacity
- middle: rendered at full opacity
- right: source under rendered at configurable opacity

The script only prepares visual evidence. It does not score fidelity.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


LABEL_H = 44
GAP = 16
LABEL_BG = (28, 32, 48)
LABEL_FG = (255, 255, 255)


def _font(size: int) -> ImageFont.ImageFont:
    candidates = [
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        "/Library/Fonts/Arial Unicode.ttf",
    ]
    for p in candidates:
        if Path(p).exists():
            try:
                return ImageFont.truetype(p, size)
            except OSError:
                pass
    return ImageFont.load_default()


def _label(draw: ImageDraw.ImageDraw, x: int, w: int, text: str, font: ImageFont.ImageFont) -> None:
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text((x + (w - tw) / 2, 11), text, fill=LABEL_FG, font=font)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True, type=Path)
    ap.add_argument("--rendered", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--rendered-alpha", type=float, default=0.55)
    args = ap.parse_args()

    if not args.source.exists():
        print(f"[error] source not found: {args.source}", file=sys.stderr)
        return 2
    if not args.rendered.exists():
        print(f"[error] rendered not found: {args.rendered}", file=sys.stderr)
        return 2

    rendered = Image.open(args.rendered).convert("RGBA")
    source = Image.open(args.source).convert("RGBA").resize(rendered.size, Image.LANCZOS)

    overlay_rendered = rendered.copy()
    alpha = max(0.0, min(1.0, args.rendered_alpha))
    a = overlay_rendered.getchannel("A").point(lambda v: int(v * alpha))
    overlay_rendered.putalpha(a)
    overlay = Image.alpha_composite(source, overlay_rendered)

    w, h = rendered.size
    total_w = w * 3 + GAP * 2
    total_h = h + LABEL_H
    canvas = Image.new("RGBA", (total_w, total_h), (255, 255, 255, 255))
    label = Image.new("RGBA", (total_w, LABEL_H), LABEL_BG)
    d = ImageDraw.Draw(label)
    f = _font(20)
    _label(d, 0, w, "SOURCE SCALED", f)
    _label(d, w + GAP, w, "RENDERED", f)
    _label(d, (w + GAP) * 2, w, "OVERLAY", f)
    canvas.paste(label, (0, 0))
    canvas.paste(source, (0, LABEL_H), source)
    canvas.paste(rendered, (w + GAP, LABEL_H), rendered)
    canvas.paste(overlay, ((w + GAP) * 2, LABEL_H), overlay)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    canvas.convert("RGB").save(args.out, "PNG", optimize=True)
    print(f"[ok] overlay -> {args.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
