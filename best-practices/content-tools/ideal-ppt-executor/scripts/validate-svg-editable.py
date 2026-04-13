#!/usr/bin/env python3
"""
validate-svg-editable.py — Validate SVGs against the PPT-editable-safe subset.

Checks that all SVG files in a directory only use allowed elements and
attributes that are compatible with PowerPoint's SVG editor.

Exit codes:
    0  All files pass validation
    2  One or more files have errors (blocked elements found)

Usage:
    python3 validate-svg-editable.py <input_dir>
"""

import sys
import os
import re
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# Tag classification
# ---------------------------------------------------------------------------

# Fully supported — these are safe for PPT editing
SUPPORTED_TAGS = {
    "svg", "g", "defs", "linearGradient", "stop",
    "rect", "circle", "ellipse", "line", "polyline", "polygon",
    "text", "tspan",
}

# Warning — allowed but may cause issues (path-heavy slides are harder to edit)
WARNING_TAGS = {
    "path",
}

# Blocked — these will break PPT compatibility
BLOCKED_TAGS = {
    "filter", "feDropShadow", "feGaussianBlur", "feOffset", "feBlend",
    "feComposite", "feColorMatrix", "feFlood", "feMerge", "feMorphology",
    "feTurbulence", "feDisplacementMap", "feComponentTransfer",
    "feConvolveMatrix", "feDiffuseLighting", "feSpecularLighting",
    "feDistantLight", "fePointLight", "feSpotLight", "feImage",
    "feTile", "feFuncR", "feFuncG", "feFuncB", "feFuncA",
    "mask", "clipPath", "pattern", "foreignObject",
    "style", "script", "animate", "animateTransform", "animateMotion",
    "set", "marker", "symbol", "use", "textPath", "cursor", "view",
    "radialGradient", "image",
}

# Blocked attributes
BLOCKED_ATTRS = {
    "filter", "mask", "clip-path",
    "marker-start", "marker-mid", "marker-end",
    "class",
}

# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def _tag_name(elem: ET.Element) -> str:
    """Extract local tag name (strip namespace)."""
    tag = elem.tag
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def validate_file(filepath: str) -> dict:
    """Validate a single SVG file. Returns result dict."""
    result = {
        "file": os.path.basename(filepath),
        "errors": [],
        "warnings": [],
        "has_viewbox": False,
        "pass": True,
    }

    try:
        tree = ET.parse(filepath)
    except ET.ParseError as e:
        result["errors"].append(f"XML parse error: {e}")
        result["pass"] = False
        return result

    root = tree.getroot()

    # Check viewBox
    viewbox = root.attrib.get("viewBox", "")
    if viewbox:
        result["has_viewbox"] = True
    else:
        result["errors"].append("Missing viewBox attribute on <svg> root")
        result["pass"] = False

    # Check all elements
    for elem in root.iter():
        tag = _tag_name(elem)

        if tag in BLOCKED_TAGS:
            result["errors"].append(f"Blocked element: <{tag}>")
            result["pass"] = False
        elif tag in WARNING_TAGS:
            result["warnings"].append(
                f"Warning: <{tag}> found — may reduce editability"
            )
        elif tag not in SUPPORTED_TAGS:
            result["warnings"].append(
                f"Unknown element: <{tag}> — not in known allow-list"
            )

        # Check attributes
        for attr_name in elem.attrib:
            if attr_name in BLOCKED_ATTRS:
                result["errors"].append(
                    f"Blocked attribute '{attr_name}' on <{tag}>"
                )
                result["pass"] = False

    # Check for rgba() color values
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    rgba_matches = re.findall(r'rgba\s*\(', content)
    if rgba_matches:
        result["errors"].append(
            f"Found {len(rgba_matches)} rgba() color value(s) — "
            f"use fill-opacity/stroke-opacity instead"
        )
        result["pass"] = False

    # Check for group opacity
    group_opacity = re.findall(r'<g[^>]*\bopacity\s*=', content)
    if group_opacity:
        result["errors"].append(
            f"Found {len(group_opacity)} group opacity — "
            f"set opacity on each child element instead"
        )
        result["pass"] = False

    return result


def find_slide_files(input_dir: str) -> list:
    """Find all SVG files sorted naturally."""
    files = []
    for f in sorted(os.listdir(input_dir)):
        if f.endswith(".svg"):
            files.append(os.path.join(input_dir, f))
    return files


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 validate-svg-editable.py <input_dir>")
        sys.exit(1)

    input_dir = sys.argv[1]

    if not os.path.isdir(input_dir):
        print(f"Error: {input_dir} is not a directory", file=sys.stderr)
        sys.exit(2)

    slide_files = find_slide_files(input_dir)
    if not slide_files:
        print(f"No SVG files found in {input_dir}", file=sys.stderr)
        sys.exit(2)

    total_pass = 0
    total_fail = 0
    total_warn = 0

    for filepath in slide_files:
        result = validate_file(filepath)
        filename = result["file"]

        if result["pass"]:
            total_pass += 1
            status = "PASS"
        else:
            total_fail += 1
            status = "FAIL"

        # Print warnings
        for w in result["warnings"]:
            print(f"  [{filename}] {w}")
            total_warn += 1

        # Print errors
        for e in result["errors"]:
            print(f"  [{filename}] ERROR: {e}")

        # Print status line
        extra = ""
        if not result["has_viewbox"]:
            extra += " [no viewBox]"
        warn_count = len(result["warnings"])
        err_count = len(result["errors"])
        print(f"  [{status}] {filename}"
              f" — {err_count} error(s), {warn_count} warning(s){extra}")

    # Summary
    print(f"\n{'='*50}")
    print(f"Total: {len(slide_files)} files")
    print(f"  Pass: {total_pass}")
    print(f"  Fail: {total_fail}")
    print(f"  Warnings: {total_warn}")

    if total_fail > 0:
        print(f"\nValidation FAILED — {total_fail} file(s) have errors")
        sys.exit(2)
    else:
        print("\nAll files passed validation")
        sys.exit(0)


if __name__ == "__main__":
    main()
