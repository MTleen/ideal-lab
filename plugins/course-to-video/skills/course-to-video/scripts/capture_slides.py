#!/usr/bin/env python3
"""用 Playwright headless Chromium 截取 HTML 幻灯片的每一页为 PNG。"""
import argparse
import os
import sys
import subprocess


def find_chromium():
    """尝试查找可用的 Chromium 可执行文件。"""
    candidates = [
        # Puppeteer cache
        os.path.expanduser("~/.cache/puppeteer/chrome-headless-shell/mac_arm-131.0.6778.204/chrome-headless-shell-mac-arm64/chrome-headless-shell"),
        # Playwright cache
        os.path.expanduser("~/Library/Caches/ms-playwright/chromium-*/chrome-mac/Chromium.app/Contents/MacOS/Chromium"),
    ]
    for path in candidates:
        import glob
        matches = glob.glob(path)
        if matches and os.path.exists(matches[0]):
            return matches[0]

    # Try system chromium
    result = subprocess.run(["which", "chromium"], capture_output=True, text=True)
    if result.returncode == 0:
        return result.stdout.strip()

    return None


def main():
    parser = argparse.ArgumentParser(description="截取 HTML 幻灯片为 PNG 图片")
    parser.add_argument("--html", required=True, help="slides.html 文件路径")
    parser.add_argument("--count", type=int, required=True, help="幻灯片总数")
    parser.add_argument("--outdir", default="./screenshots", help="输出目录 (默认: ./screenshots)")
    parser.add_argument("--width", type=int, default=1280, help="视口宽度 (默认: 1280)")
    parser.add_argument("--height", type=int, default=720, help="视口高度 (默认: 720)")
    parser.add_argument("--delay", type=int, default=500, help="每页渲染等待时间 ms (默认: 500)")
    args = parser.parse_args()

    html_path = os.path.abspath(args.html)
    if not os.path.exists(html_path):
        print(f"Error: {html_path} not found")
        sys.exit(1)

    os.makedirs(args.outdir, exist_ok=True)

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: playwright not installed. Run: pip3 install playwright && playwright install chromium")
        sys.exit(1)

    chromium_path = find_chromium()

    with sync_playwright() as p:
        launch_opts = {"headless": True}
        if chromium_path:
            launch_opts["executable_path"] = chromium_path

        browser = p.chromium.launch(**launch_opts)
        page = browser.new_page(viewport={"width": args.width, "height": args.height})

        # Use file:// URL for local files
        file_url = f"file://{html_path}"
        page.goto(file_url, wait_until="domcontentloaded")
        page.wait_for_timeout(args.delay)

        for i in range(args.count):
            page.evaluate(f"showSlide({i})")
            page.wait_for_timeout(max(100, args.delay // 3))
            fname = os.path.join(args.outdir, f"slide_{i + 1:03d}.png")
            page.screenshot(path=fname, type="png")
            print(f"  [{i + 1}/{args.count}] {fname}")

        browser.close()

    # Verify
    files = sorted([f for f in os.listdir(args.outdir) if f.endswith(".png")])
    print(f"\nCaptured {len(files)} frames to {args.outdir}/")


if __name__ == "__main__":
    main()
