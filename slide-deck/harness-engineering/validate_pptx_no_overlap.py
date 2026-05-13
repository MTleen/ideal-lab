#!/usr/bin/env python3
from __future__ import annotations

import json
import math
import re
import shutil
import subprocess
import sys
import zipfile
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from xml.etree import ElementTree as ET

import numpy as np
from bs4 import BeautifulSoup
from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageStat

BASE_DIR = Path("/Users/mathrippermacmini/Documents/Sync/Work/电信/理想/产品/0-最佳实践/slide-deck/harness-engineering")
PPTX_PATH = BASE_DIR / "harness-engineering.pptx"
SCREENSHOTS_DIR = BASE_DIR / "screenshots"
HTML_DIR = BASE_DIR / "html_output"
DEBUG_DIR = BASE_DIR / "pptx_debug"

SLIDE_W_EMU = 12_192_000
SLIDE_H_EMU = 6_858_000
CANVAS = (1280, 720)
EXPECTED_SLIDES = 5

NS = {
    "p": "http://schemas.openxmlformats.org/presentationml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}


@dataclass
class TextBox:
    slide: int
    text: str
    box_emu: tuple[int, int, int, int]
    box_px: tuple[int, int, int, int]


@dataclass
class SlideEvidence:
    slide: int
    background_path: str
    screenshot_path: str | None
    ocr_text: str
    textlike_boxes: int
    max_components: int
    avg_components: float
    bg_html_similarity: float | None
    suspiciously_identical_to_html: bool
    textbox_count: int
    textbox_html_matches: int
    html_fragment_count: int
    html_pptx_matches: int
    missing_html_fragments: list[str]
    status: str
    reason: str


def parse_xml(data: bytes) -> ET.Element:
    return ET.fromstring(data)


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", "", value or "").strip()


def resolve_target(slide_index: int, target: str) -> str:
    base = PurePosixPath(f"ppt/slides/slide{slide_index}.xml").parent
    path = PurePosixPath(target)
    if not path.is_absolute():
        path = base / path
    parts: list[str] = []
    for part in path.parts:
        if part in ("", "."):
            continue
        if part == "..":
            if parts:
                parts.pop()
        else:
            parts.append(part)
    return "/".join(parts)


def rel_targets(zf: zipfile.ZipFile, slide_index: int) -> dict[str, str]:
    rel_name = f"ppt/slides/_rels/slide{slide_index}.xml.rels"
    if rel_name not in zf.namelist():
        return {}
    root = parse_xml(zf.read(rel_name))
    result: dict[str, str] = {}
    for rel in root.findall("rel:Relationship", NS):
        if "image" not in rel.attrib.get("Type", ""):
            continue
        rid = rel.attrib.get("Id")
        target = rel.attrib.get("Target")
        if rid and target:
            result[rid] = resolve_target(slide_index, target)
    return result


def xfrm_of(node: ET.Element) -> tuple[int, int, int, int] | None:
    xfrm = node.find(".//a:xfrm", NS)
    if xfrm is None:
        return None
    off = xfrm.find("a:off", NS)
    ext = xfrm.find("a:ext", NS)
    if off is None or ext is None:
        return None
    return (
        int(off.attrib.get("x", "0")),
        int(off.attrib.get("y", "0")),
        int(ext.attrib.get("cx", "0")),
        int(ext.attrib.get("cy", "0")),
    )


def box_emu_to_px(box: tuple[int, int, int, int], size: tuple[int, int] = CANVAS) -> tuple[int, int, int, int]:
    x, y, w, h = box
    sx = size[0] / SLIDE_W_EMU
    sy = size[1] / SLIDE_H_EMU
    return (
        max(0, int(round(x * sx))),
        max(0, int(round(y * sy))),
        min(size[0], int(round((x + w) * sx))),
        min(size[1], int(round((y + h) * sy))),
    )


def shape_text(node: ET.Element) -> str:
    return "".join(t.text or "" for t in node.findall(".//a:t", NS)).strip()


def slide_textboxes(root: ET.Element, slide_index: int) -> list[TextBox]:
    boxes: list[TextBox] = []
    for shape in root.findall(".//p:sp", NS):
        if shape.find("p:txBody", NS) is None:
            continue
        text = re.sub(r"\s+", " ", shape_text(shape))
        box = xfrm_of(shape)
        if not text or box is None:
            continue
        boxes.append(TextBox(slide_index, text, box, box_emu_to_px(box)))
    return boxes


def extract_background(zf: zipfile.ZipFile, slide_index: int, root: ET.Element, out_dir: Path) -> Path:
    rels = rel_targets(zf, slide_index)
    candidates: list[tuple[float, str]] = []

    bg = root.find("p:cSld/p:bg", NS)
    if bg is not None:
        blip = bg.find(".//a:blip", NS)
        rid = blip.attrib.get(f"{{{NS['r']}}}embed") if blip is not None else None
        if rid and rid in rels:
            candidates.append((999.0, rels[rid]))

    for pic in root.findall(".//p:pic", NS):
        blip = pic.find(".//a:blip", NS)
        rid = blip.attrib.get(f"{{{NS['r']}}}embed") if blip is not None else None
        if not rid or rid not in rels:
            continue
        box = xfrm_of(pic)
        if box is None:
            area = 0.0
        else:
            _, _, w, h = box
            area = (w * h) / (SLIDE_W_EMU * SLIDE_H_EMU)
        candidates.append((area, rels[rid]))

    if not candidates:
        raise RuntimeError(f"slide {slide_index}: no related image found")

    _, image_name = sorted(candidates, reverse=True)[0]
    if image_name not in zf.namelist():
        raise RuntimeError(f"slide {slide_index}: image target missing: {image_name}")

    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"slide_{slide_index:02d}_background.png"
    Image.open(zf.open(image_name)).convert("RGB").save(out_path)
    return out_path


def try_ocr_setup(debug_dir: Path) -> tuple[bool, str]:
    log_path = debug_dir / "ocr_install_attempt.log"
    tesseract = shutil.which("tesseract")
    try:
        import pytesseract  # noqa: F401

        wrapper_ok = True
    except Exception:
        wrapper_ok = False

    if wrapper_ok and tesseract:
        return True, "pytesseract + tesseract available"

    proc = subprocess.run(
        [sys.executable, "-m", "pip", "install", "--user", "pytesseract"],
        cwd=str(BASE_DIR),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=60,
        check=False,
    )
    log_path.write_text(proc.stdout, encoding="utf-8")

    try:
        import pytesseract  # noqa: F401

        wrapper_ok = True
    except Exception:
        wrapper_ok = False
    tesseract = shutil.which("tesseract")
    if wrapper_ok and tesseract:
        return True, "pytesseract installed and tesseract available"
    return False, f"OCR unavailable; install attempt exit={proc.returncode}, tesseract={tesseract or 'missing'}"


def ocr_image(path: Path, available: bool) -> str:
    if not available:
        return ""
    try:
        import pytesseract

        return pytesseract.image_to_string(Image.open(path))
    except Exception:
        return ""


def connected_components(mask: np.ndarray) -> list[tuple[int, int, int, float]]:
    h, w = mask.shape
    seen = np.zeros(mask.shape, dtype=bool)
    out: list[tuple[int, int, int, float]] = []
    ys, xs = np.where(mask)
    for sy, sx in zip(ys.tolist(), xs.tolist()):
        if seen[sy, sx]:
            continue
        stack = [(sy, sx)]
        seen[sy, sx] = True
        min_x = max_x = sx
        min_y = max_y = sy
        count = 0
        while stack:
            y, x = stack.pop()
            count += 1
            min_x = min(min_x, x)
            max_x = max(max_x, x)
            min_y = min(min_y, y)
            max_y = max(max_y, y)
            for ny in (y - 1, y, y + 1):
                for nx in (x - 1, x, x + 1):
                    if ny == y and nx == x:
                        continue
                    if 0 <= ny < h and 0 <= nx < w and mask[ny, nx] and not seen[ny, nx]:
                        seen[ny, nx] = True
                        stack.append((ny, nx))
        bw = max_x - min_x + 1
        bh = max_y - min_y + 1
        out.append((bw, bh, count, count / max(1, bw * bh)))
    return out


def textlike_component_count(crop: Image.Image) -> int:
    gray = crop.convert("L")
    arr = np.array(gray, dtype=np.int16)
    blur = np.array(gray.filter(ImageFilter.GaussianBlur(radius=1.4)), dtype=np.int16)
    residual = np.abs(arr - blur)
    mask = residual > 12
    if mask.size > 130_000:
        mask = mask[::2, ::2]
    comps = connected_components(mask)
    textlike = [
        c
        for c in comps
        if 2 <= c[0] <= 90
        and 3 <= c[1] <= 55
        and 3 <= c[2] <= 2500
        and 0.04 <= c[3] <= 0.85
    ]
    return len(textlike)


def analyze_background_text(background_path: Path, boxes: list[TextBox], evidence_path: Path) -> tuple[int, int, float]:
    image = Image.open(background_path).convert("RGB").resize(CANVAS, Image.Resampling.LANCZOS)
    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    counts: list[int] = []
    for tb in boxes:
        x0, y0, x1, y1 = tb.box_px
        if x1 <= x0 or y1 <= y0:
            continue
        pad = max(1, int(min(x1 - x0, y1 - y0) * 0.06))
        crop_box = (x0 + pad, y0 + pad, x1 - pad, y1 - pad)
        if crop_box[2] <= crop_box[0] or crop_box[3] <= crop_box[1]:
            crop_box = (x0, y0, x1, y1)
        count = textlike_component_count(image.crop(crop_box))
        counts.append(count)
        if count >= 2:
            draw.rectangle((x0, y0, x1, y1), outline=(255, 0, 0), width=2)
            draw.text((x0 + 3, y0 + 3), str(count), fill=(255, 0, 0))
    overlay.save(evidence_path)
    return sum(c >= 2 for c in counts), max(counts or [0]), float(sum(counts) / len(counts)) if counts else 0.0


def image_similarity(a_path: Path, b_path: Path, diff_path: Path) -> float:
    a = Image.open(a_path).convert("RGB").resize(CANVAS, Image.Resampling.LANCZOS)
    b = Image.open(b_path).convert("RGB").resize(CANVAS, Image.Resampling.LANCZOS)
    diff = ImageChops.difference(a, b)
    diff.save(diff_path)
    stat = ImageStat.Stat(diff)
    mae = sum(stat.mean) / (3 * 255)
    return max(0.0, 1.0 - mae)


def html_fragments_for_slide(slide_index: int) -> list[str]:
    files = sorted(HTML_DIR.glob(f"{slide_index:02d}-*.html"))
    if not files:
        return []
    soup = BeautifulSoup(files[0].read_text(encoding="utf-8"), "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    body = soup.body or soup
    fragments: list[str] = []
    seen: set[str] = set()
    for text in body.stripped_strings:
        normalized = normalize_text(text)
        if len(normalized) < 2 or normalized in seen:
            continue
        fragments.append(text.strip())
        seen.add(normalized)
    return fragments


def html_text_for_slide(slide_index: int) -> str:
    return normalize_text(" ".join(html_fragments_for_slide(slide_index)))


def screenshot_for_slide(slide_index: int) -> Path | None:
    files = sorted(SCREENSHOTS_DIR.glob(f"{slide_index:02d}-*.png"))
    return files[0] if files else None


def render_pptx(debug_dir: Path) -> tuple[bool, str]:
    render_dir = debug_dir / "rendered_pptx"
    render_dir.mkdir(parents=True, exist_ok=True)
    soffice = shutil.which("soffice")
    if not soffice:
        return False, "soffice missing"
    proc = subprocess.run(
        [
            soffice,
            "--headless",
            "-env:UserInstallation=file:///tmp/pptx-no-overlap-lo",
            "--convert-to",
            "pdf",
            "--outdir",
            str(render_dir),
            str(PPTX_PATH),
        ],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=90,
        check=False,
    )
    (render_dir / "soffice.log").write_text(proc.stdout, encoding="utf-8")
    pdf_path = render_dir / f"{PPTX_PATH.stem}.pdf"
    if proc.returncode != 0 or not pdf_path.exists():
        return False, f"soffice pdf export failed, exit={proc.returncode}"
    try:
        import fitz

        doc = fitz.open(pdf_path)
        for idx, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=fitz.Matrix(1280 / page.rect.width, 720 / page.rect.height), alpha=False)
            pix.save(render_dir / f"slide_{idx:02d}_render.png")
        return True, f"rendered {len(doc)} slides to {render_dir}"
    except Exception as exc:
        return False, f"pdf rasterization failed: {exc}"


def validate() -> tuple[str, bool]:
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    bg_dir = DEBUG_DIR / "extracted_backgrounds"
    evidence_dir = DEBUG_DIR / "text_leak_evidence"
    diff_dir = DEBUG_DIR / "html_background_diffs"
    for directory in (bg_dir, evidence_dir, diff_dir):
        directory.mkdir(parents=True, exist_ok=True)

    inventory = {
        "pptx_exists": PPTX_PATH.exists(),
        "pptx_size": PPTX_PATH.stat().st_size if PPTX_PATH.exists() else 0,
        "screenshots": [str(p) for p in sorted(SCREENSHOTS_DIR.glob("*.png"))],
        "html": [str(p) for p in sorted(HTML_DIR.glob("*.html"))],
        "debug_dir": str(DEBUG_DIR),
    }
    (DEBUG_DIR / "inventory.json").write_text(json.dumps(inventory, ensure_ascii=False, indent=2), encoding="utf-8")

    preflight_failures = []
    if not PPTX_PATH.exists():
        preflight_failures.append(f"PPTX missing: {PPTX_PATH}")
    if not SCREENSHOTS_DIR.exists():
        preflight_failures.append(f"screenshots dir missing: {SCREENSHOTS_DIR}")
    if not HTML_DIR.exists():
        preflight_failures.append(f"html_output dir missing: {HTML_DIR}")
    if preflight_failures:
        report = "## 验收报告 (ppt-v5-no-overlap)\n\n### C1: 背景图不含文字\n- FAIL: " + "; ".join(preflight_failures)
        return report, False

    ocr_available, ocr_note = try_ocr_setup(DEBUG_DIR)
    render_ok, render_note = render_pptx(DEBUG_DIR)

    evidences: list[SlideEvidence] = []
    all_textboxes: dict[int, list[TextBox]] = {}
    with zipfile.ZipFile(PPTX_PATH) as zf:
        slide_names = sorted(
            [n for n in zf.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", n)],
            key=lambda n: int(re.search(r"slide(\d+)", n).group(1)),
        )
        for slide_name in slide_names:
            slide_index = int(re.search(r"slide(\d+)", slide_name).group(1))
            root = parse_xml(zf.read(slide_name))
            boxes = slide_textboxes(root, slide_index)
            all_textboxes[slide_index] = boxes
            bg_path = extract_background(zf, slide_index, root, bg_dir)
            evidence_path = evidence_dir / f"slide_{slide_index:02d}_textlike_boxes.png"
            textlike_boxes, max_components, avg_components = analyze_background_text(bg_path, boxes, evidence_path)
            shot = screenshot_for_slide(slide_index)
            similarity = None
            identical = False
            if shot:
                similarity = image_similarity(bg_path, shot, diff_dir / f"slide_{slide_index:02d}_bg_vs_html_diff.png")
                identical = similarity >= 0.992
            html_fragments = html_fragments_for_slide(slide_index)
            html_text = normalize_text(" ".join(html_fragments))
            pptx_text = normalize_text(" ".join(tb.text for tb in boxes))
            matches = sum(1 for tb in boxes if normalize_text(tb.text) and normalize_text(tb.text) in html_text)
            html_matches = sum(1 for fragment in html_fragments if normalize_text(fragment) in pptx_text)
            missing_html = [fragment for fragment in html_fragments if normalize_text(fragment) not in pptx_text]
            ocr_text = normalize_text(ocr_image(bg_path, ocr_available))

            fail_reasons = []
            if ocr_text:
                fail_reasons.append(f"OCR detected text: {ocr_text[:80]}")
            if textlike_boxes >= 3 or max_components >= 6:
                fail_reasons.append(f"{textlike_boxes}/{len(boxes)} TextBox regions contain text-like strokes")
            if identical:
                fail_reasons.append(f"background is nearly identical to text-containing HTML screenshot ({similarity:.4f})")

            evidences.append(
                SlideEvidence(
                    slide=slide_index,
                    background_path=str(bg_path),
                    screenshot_path=str(shot) if shot else None,
                    ocr_text=ocr_text,
                    textlike_boxes=textlike_boxes,
                    max_components=max_components,
                    avg_components=avg_components,
                    bg_html_similarity=similarity,
                    suspiciously_identical_to_html=identical,
                    textbox_count=len(boxes),
                    textbox_html_matches=matches,
                    html_fragment_count=len(html_fragments),
                    html_pptx_matches=html_matches,
                    missing_html_fragments=missing_html[:12],
                    status="FAIL" if fail_reasons else "PASS",
                    reason="; ".join(fail_reasons) if fail_reasons else "no OCR text and no text-like leakage in TextBox regions",
                )
            )

    (DEBUG_DIR / "ppt_v5_no_overlap_evidence.json").write_text(
        json.dumps([asdict(e) for e in evidences], ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    c1_pass = all(e.status == "PASS" for e in evidences) and len(evidences) == EXPECTED_SLIDES
    c2_pass = c1_pass
    textbox_to_html_ok = all(e.textbox_count > 0 and e.textbox_html_matches >= max(1, math.floor(e.textbox_count * 0.75)) for e in evidences)
    html_to_pptx_ok = all(
        e.html_fragment_count > 0 and e.html_pptx_matches >= max(1, math.floor(e.html_fragment_count * 0.90))
        for e in evidences
    )
    bg_layout_ok = all(e.bg_html_similarity is not None and 0.94 <= e.bg_html_similarity < 0.992 for e in evidences)
    c3_pass = textbox_to_html_ok and html_to_pptx_ok and bg_layout_ok and c1_pass

    lines = [
        "## 验收报告 (ppt-v5-no-overlap)",
        "",
        "### C1: 背景图不含文字",
        f"- OCR: {ocr_note}",
    ]
    for e in evidences:
        sim = "N/A" if e.bg_html_similarity is None else f"{e.bg_html_similarity:.4f}"
        lines.append(
            f"- Slide {e.slide}: {e.status} - {e.reason}; "
            f"textlike_boxes={e.textlike_boxes}/{e.textbox_count}, max_components={e.max_components}, "
            f"bg_html_similarity={sim}"
        )

    lines.extend(["", "### C2: 无文字重叠"])
    c2_status = "PASS" if c2_pass else "FAIL"
    leak_slides = [str(e.slide) for e in evidences if e.status == "FAIL"]
    if c2_pass:
        lines.append("- PASS - 背景图未检测到残留文字，TextBox 不会与背景文字重叠。")
    else:
        lines.append(f"- {c2_status} - 背景图在 slide {', '.join(leak_slides)} 的 TextBox 区域存在文字笔画，说明会与 PPTX TextBox 叠加。")
        lines.append(f"- 证据: {evidence_dir}")

    lines.extend(["", "### C3: 整体视觉效果一致"])
    c3_status = "PASS" if c3_pass else "FAIL"
    render_prefix = "rendered" if render_ok else "render unavailable; used structural fallback"
    lines.append(f"- {c3_status} - PPTX render: {render_note} ({render_prefix})")
    for e in evidences:
        pptx_ratio = e.textbox_html_matches / e.textbox_count if e.textbox_count else 0.0
        html_ratio = e.html_pptx_matches / e.html_fragment_count if e.html_fragment_count else 0.0
        sim = "N/A" if e.bg_html_similarity is None else f"{e.bg_html_similarity:.4f}"
        missing = ""
        if e.missing_html_fragments:
            missing = f"; missing HTML text: {' | '.join(e.missing_html_fragments[:6])}"
        lines.append(
            f"- Slide {e.slide}: TextBox->HTML {e.textbox_html_matches}/{e.textbox_count} ({pptx_ratio:.0%}); "
            f"HTML->TextBox {e.html_pptx_matches}/{e.html_fragment_count} ({html_ratio:.0%}); "
            f"background-vs-HTML similarity {sim}{missing}"
        )
    if not c1_pass:
        lines.append("- 视觉一致性不能通过：当前背景图本身已经包含 HTML 文字，叠加 TextBox 后存在重影风险。")

    all_pass = c1_pass and c2_pass and c3_pass
    lines.extend(["", f"### 总结: {'ALL PASS' if all_pass else '需要修复'}"])
    lines.append(f"- 中间产物: {DEBUG_DIR}")

    report = "\n".join(lines)
    (DEBUG_DIR / "ppt_v5_no_overlap_report.md").write_text(report, encoding="utf-8")
    return report, all_pass


def main() -> int:
    report, passed = validate()
    print(report)
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
