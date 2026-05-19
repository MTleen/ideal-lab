#!/usr/bin/env python3
"""Render an SVG file to a PNG at a specified resolution.

Uses Playwright headless Chromium because it handles modern SVG/font rendering
more faithfully than cairosvg or rsvg-convert (especially CJK fonts).

Usage:
    python3 render_svg.py --svg path/to/in.svg --out path/to/out.png \\
                          [--width 1920] [--height 1080]
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
import textwrap
from pathlib import Path


def render_with_playwright_lib(svg_path: Path, out_path: Path, w: int, h: int) -> bool:
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return False

    html = _wrap_svg_in_html(svg_path, w, h)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        html_path = Path(f.name)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            ctx = browser.new_context(viewport={"width": w, "height": h}, device_scale_factor=1)
            page = ctx.new_page()
            page.goto(html_path.as_uri())
            page.wait_for_timeout(500)
            page.screenshot(path=str(out_path), full_page=False, clip={"x": 0, "y": 0, "width": w, "height": h})
            browser.close()
        return True
    finally:
        html_path.unlink(missing_ok=True)


def render_with_playwright_cli(svg_path: Path, out_path: Path, w: int, h: int) -> bool:
    npx = shutil.which("npx")
    if not npx:
        return False

    html = _wrap_svg_in_html(svg_path, w, h)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        html_path = Path(f.name)

    try:
        cmd = [
            npx, "--yes", "playwright", "screenshot",
            html_path.as_uri(),
            str(out_path),
            f"--viewport-size={w},{h}",
            "--wait-for-timeout=500",
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            return False
        return True
    finally:
        html_path.unlink(missing_ok=True)


def render_with_chrome_cli(svg_path: Path, out_path: Path, w: int, h: int) -> bool:
    chrome = (
        shutil.which("google-chrome")
        or shutil.which("chromium")
        or shutil.which("chromium-browser")
    )
    if not chrome:
        mac_chrome = Path("/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
        if mac_chrome.exists():
            chrome = str(mac_chrome)
    if not chrome:
        return False

    html = _wrap_svg_in_html(svg_path, w, h)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as f:
        f.write(html)
        html_path = Path(f.name)

    try:
        cmd = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--hide-scrollbars",
            f"--window-size={w},{h}",
            f"--screenshot={out_path}",
            html_path.as_uri(),
        ]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            sys.stderr.write(r.stderr)
            return False
        return True
    finally:
        html_path.unlink(missing_ok=True)


def _wrap_svg_in_html(svg_path: Path, w: int, h: int) -> str:
    svg = svg_path.read_text(encoding="utf-8")
    base_href = svg_path.resolve().parent.as_uri() + "/"
    return textwrap.dedent(f"""\
        <!doctype html>
        <html><head><meta charset="utf-8">
        <base href="{base_href}">
        <style>
          html,body{{margin:0;padding:0;background:#fff;width:{w}px;height:{h}px;overflow:hidden;}}
          svg{{display:block;width:{w}px;height:{h}px;}}
        </style></head>
        <body>{svg}</body></html>
    """)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--svg", required=True, type=Path)
    ap.add_argument("--out", required=True, type=Path)
    ap.add_argument("--width", type=int, default=1920)
    ap.add_argument("--height", type=int, default=1080)
    args = ap.parse_args()

    if not args.svg.exists():
        print(f"[error] SVG not found: {args.svg}", file=sys.stderr)
        return 2

    args.out.parent.mkdir(parents=True, exist_ok=True)

    for fn in (render_with_playwright_lib, render_with_chrome_cli, render_with_playwright_cli):
        if fn(args.svg, args.out, args.width, args.height):
            print(f"[ok] rendered -> {args.out}")
            return 0

    print("[error] No working renderer (need playwright python lib or npx playwright)", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
