#!/usr/bin/env python3
"""
sanitize-svg.py — Strip SVG of PPT-incompatible elements and attributes.

Processes a single SVG file or all NN-slide-*.svg files in a directory.
Removes banned tags, attributes, and url() references that PowerPoint
cannot render correctly.

Usage:
    python3 sanitize-svg.py <input_path>           # single file
    python3 sanitize-svg.py <input_dir>             # all matching files
    python3 sanitize-svg.py <input_dir> -o <out_dir>  # output to directory
"""

import sys
import os
import re
import argparse
from pathlib import Path
from xml.etree import ElementTree as ET

# ---------------------------------------------------------------------------
# Banned SVG tags (removed entirely with all children)
# ---------------------------------------------------------------------------
BANNED_TAGS = {
    "filter", "feDropShadow", "feGaussianBlur", "feOffset", "feBlend",
    "feComposite", "feColorMatrix", "feFlood", "feMerge", "feMorphology",
    "feTurbulence", "feDisplacementMap", "feComponentTransfer",
    "feConvolveMatrix", "feDiffuseLighting", "feSpecularLighting",
    "feDistantLight", "fePointLight", "feSpotLight", "feImage",
    "feTile", "feFuncR", "feFuncG", "feFuncB", "feFuncA",
    "mask", "clipPath", "pattern", "foreignObject",
    "script", "marker", "animate", "animateTransform", "animateMotion",
    "set", "motionPath",
}

# ---------------------------------------------------------------------------
# Banned attributes (removed from any element)
# ---------------------------------------------------------------------------
BANNED_ATTRS = {
    "filter", "mask", "clip-path",
    "marker-start", "marker-mid", "marker-end",
}

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_banned_elements(root: ET.Element) -> int:
    """Remove all elements whose tag is in BANNED_TAGS. Returns count."""
    removed = 0
    for parent in root.iter():
        children_to_remove = [
            child for child in parent
            if _tag_name(child) in BANNED_TAGS
        ]
        for child in children_to_remove:
            parent.remove(child)
            removed += 1
    return removed


def strip_banned_attributes(root: ET.Element) -> int:
    """Remove banned attributes and url() references. Returns count."""
    removed = 0
    for elem in root.iter():
        attrs_to_remove = []
        for attr_name, attr_value in elem.attrib.items():
            # Direct banned attribute
            if attr_name in BANNED_ATTRS:
                attrs_to_remove.append(attr_name)
            # url() references to banned elements (not gradient)
            elif _is_banned_url(attr_name, attr_value):
                attrs_to_remove.append(attr_name)
        for attr_name in attrs_to_remove:
            del elem.attrib[attr_name]
            removed += 1
    return removed


def _tag_name(elem: ET.Element) -> str:
    """Extract local tag name (strip namespace)."""
    tag = elem.tag
    if "}" in tag:
        return tag.split("}", 1)[1]
    return tag


def _is_banned_url(attr_name: str, attr_value: str) -> bool:
    """Check if a url() reference should be removed.

    We keep url() for fill/stroke that reference gradients.
    Everything else (filter, mask, clip-path) is removed.
    """
    if "url(" not in attr_value:
        return False
    # Allow gradient references for fill and stroke
    if attr_name in ("fill", "stroke"):
        return False
    return True


def sanitize_file(input_path: str, output_path: str) -> dict:
    """Sanitize a single SVG file. Returns stats dict."""
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Register SVG namespace to preserve it in output
    ET.register_namespace("", "http://www.w3.org/2000/svg")

    tags_removed = strip_banned_elements(root)
    attrs_removed = strip_banned_attributes(root)

    # Write output
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    tree.write(output_path, encoding="unicode", xml_declaration=True)

    # Re-add proper SVG namespace if missing
    _fix_namespace(output_path)

    return {
        "file": os.path.basename(input_path),
        "tags_removed": tags_removed,
        "attrs_removed": attrs_removed,
    }


def _fix_namespace(filepath: str):
    """Ensure xmlns is present on root <svg> element."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Fix self-closing xml declaration + root
    content = content.replace(
        "<?xml version='1.0' encoding='utf-8'?>\n<svg ",
        '<?xml version="1.0" encoding="utf-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" ',
    )
    # Fix if namespace was preserved differently
    if 'xmlns="http://www.w3.org/2000/svg"' not in content:
        content = content.replace("<svg ", '<svg xmlns="http://www.w3.org/2000/svg" ', 1)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)


def find_slide_files(input_dir: str) -> list:
    """Find all NN-slide-*.svg files sorted naturally."""
    files = []
    for f in sorted(os.listdir(input_dir)):
        if re.match(r"^\d+-.*\.svg$", f):
            files.append(os.path.join(input_dir, f))
    return files


def main():
    parser = argparse.ArgumentParser(
        description="Sanitize SVG files for PPT compatibility"
    )
    parser.add_argument("input", help="Input SVG file or directory")
    parser.add_argument(
        "-o", "--output",
        help="Output directory (default: overwrite in place for file, "
             "or create svg_final/ sibling for directory)",
    )
    args = parser.parse_args()

    input_path = args.input

    if os.path.isfile(input_path):
        # Single file mode
        output_path = args.output or input_path
        stats = sanitize_file(input_path, output_path)
        print(f"[OK] {stats['file']}: "
              f"{stats['tags_removed']} tags, "
              f"{stats['attrs_removed']} attrs removed")

    elif os.path.isdir(input_path):
        # Directory mode
        slide_files = find_slide_files(input_path)
        if not slide_files:
            # Fallback: process all .svg files
            slide_files = sorted(
                os.path.join(input_path, f)
                for f in os.listdir(input_path)
                if f.endswith(".svg")
            )

        if not slide_files:
            print(f"No SVG files found in {input_path}", file=sys.stderr)
            sys.exit(1)

        output_dir = args.output or os.path.join(
            os.path.dirname(input_path.rstrip("/")), "svg_final"
        )
        os.makedirs(output_dir, exist_ok=True)

        total_tags = 0
        total_attrs = 0
        for filepath in slide_files:
            out_file = os.path.join(output_dir, os.path.basename(filepath))
            stats = sanitize_file(filepath, out_file)
            total_tags += stats["tags_removed"]
            total_attrs += stats["attrs_removed"]
            print(f"  [OK] {stats['file']}: "
                  f"{stats['tags_removed']} tags, "
                  f"{stats['attrs_removed']} attrs removed")

        print(f"\nDone: {len(slide_files)} files processed, "
              f"{total_tags} tags + {total_attrs} attrs removed")
        print(f"Output: {output_dir}")
    else:
        print(f"Error: {input_path} not found", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
