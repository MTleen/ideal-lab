import os
from playwright.sync_api import sync_playwright

SLIDE_DIR = "/Users/mathrippermacmini/Documents/Sync/Work/电信/理想/产品/0-最佳实践/slide-deck/ideal-lab-shi-ye-bu-jie-shao"

def html_to_png():
    html_files = sorted([f for f in os.listdir(SLIDE_DIR) if f.endswith('.html')])
    print(f"Found {len(html_files)} HTML files")

    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 1280, "height": 720})

        for i, html_file in enumerate(html_files):
            html_path = os.path.join(SLIDE_DIR, html_file)
            png_name = html_file.replace('.html', '.png')
            png_path = os.path.join(SLIDE_DIR, png_name)

            page.goto(f"file://{html_path}")
            page.wait_for_timeout(500)  # wait for CSS rendering
            page.screenshot(path=png_path, full_page=False)

            print(f"[{i+1}/{len(html_files)}] {html_file} → {png_name}")

        browser.close()
    print("Done! All HTML files converted to PNG.")

if __name__ == "__main__":
    html_to_png()
