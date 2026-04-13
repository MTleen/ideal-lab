#!/usr/bin/env python3
"""
generate-manifest.py

Scans the prompts/ directory for slide prompt files (NN-slide-*.md),
extracts headlines from each, and generates svg-generation-manifest.json.

Usage:
    python3 scripts/generate-manifest.py [prompts_dir] [output_path]

Defaults:
    prompts_dir   = ./prompts
    output_path   = ./prompts/svg-generation-manifest.json
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path


def extract_headline(filepath: str) -> str:
    """Extract headline from a prompt file.

    Search order:
    1. YAML frontmatter 'headline:' field
    2. First markdown heading (# ...)
    3. First non-empty, non-frontmatter line
    4. Fallback to filename-derived title
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Strategy 1: YAML frontmatter headline
    fm_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if fm_match:
        frontmatter = fm_match.group(1)
        headline_match = re.search(
            r"^headline:\s*[\"']?(.+?)[\"']?\s*$", frontmatter, re.MULTILINE
        )
        if headline_match:
            return headline_match.group(1).strip()

    # Strategy 2: First markdown heading
    heading_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    if heading_match:
        return heading_match.group(1).strip()

    # Strategy 3: First non-empty line after frontmatter
    body = content
    if fm_match:
        body = content[fm_match.end():]
    for line in body.strip().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line[:80]

    # Strategy 4: Filename-derived title
    stem = Path(filepath).stem
    title_part = re.sub(r"^\d{2}-slide-", "", stem)
    return title_part.replace("-", " ").title()


def extract_slide_number(filename: str) -> int:
    """Extract the slide number from filename (e.g., '03-slide-market.md' -> 3)."""
    match = re.match(r"^(\d{2})-", filename)
    if match:
        return int(match.group(1))
    return 999


def generate_session_id(prompts_dir: str) -> str:
    """Generate a unique session ID based on directory name and timestamp."""
    dir_name = Path(prompts_dir).resolve().parent.name
    # Sanitize dir_name for use in session ID
    safe_name = re.sub(r"[^a-zA-Z0-9_-]", "", dir_name)[:32]
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"slides-{safe_name}-{timestamp}"


def generate_manifest(prompts_dir: str, output_path: str) -> dict:
    """Scan prompts directory and generate manifest JSON."""
    prompts_path = Path(prompts_dir)

    if not prompts_path.exists():
        print(f"Error: prompts directory not found: {prompts_dir}", file=sys.stderr)
        sys.exit(1)

    # Find all NN-slide-*.md files
    prompt_files = sorted(
        prompts_path.glob("[0-9][0-9]-slide-*.md"),
        key=lambda p: extract_slide_number(p.name),
    )

    if not prompt_files:
        print(f"Warning: no prompt files found in {prompts_dir}", file=sys.stderr)
        sys.exit(1)

    slides = []
    for filepath in prompt_files:
        slide_num = extract_slide_number(filepath.name)
        # Derive target SVG filename from prompt filename
        svg_filename = filepath.stem + ".svg"
        headline = extract_headline(str(filepath))

        slides.append(
            {
                "slide_number": slide_num,
                "headline": headline,
                "prompt_file": filepath.name,
                "target_svg": svg_filename,
            }
        )

    manifest = {
        "session_id": generate_session_id(prompts_dir),
        "generated_at": datetime.now().isoformat(),
        "total_slides": len(slides),
        "slides": slides,
    }

    # Write manifest JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"Manifest generated: {output_path}")
    print(f"  Total slides: {len(slides)}")
    print(f"  Session ID:   {manifest['session_id']}")

    return manifest


def main():
    prompts_dir = sys.argv[1] if len(sys.argv) > 1 else "./prompts"
    output_path = (
        sys.argv[2]
        if len(sys.argv) > 2
        else os.path.join(prompts_dir, "svg-generation-manifest.json")
    )

    generate_manifest(prompts_dir, output_path)


if __name__ == "__main__":
    main()
