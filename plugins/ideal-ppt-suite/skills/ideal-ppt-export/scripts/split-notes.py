#!/usr/bin/env python3
"""
split-notes.py - 将 notes/total.md 分割为每页独立的备注文件

用法：
    python3 split-notes.py <slide-deck-dir>

输入：
    <slide-deck-dir>/notes/total.md

输出：
    <slide-deck-dir>/notes/01_cover.md
    <slide-deck-dir>/notes/02_xxx.md
    ...
"""

import os
import re
import sys
from pathlib import Path


def split_notes(total_md_path: Path):
    """Split total.md into per-page note files."""
    if not total_md_path.exists():
        print(f"Error: {total_md_path} not found")
        sys.exit(1)

    content = total_md_path.read_text(encoding="utf-8")
    notes_dir = total_md_path.parent

    # Split by lines starting with # (heading)
    # Pattern: # 01_封面 or # 01_cover or # Slide 01
    sections = re.split(r'^(?=#[^#])', content, flags=re.MULTILINE)

    count = 0
    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Extract heading
        heading_match = re.match(r'^#\s+(.+)$', section, re.MULTILINE)
        if not heading_match:
            continue

        heading = heading_match.group(1).strip()

        # Generate filename from heading
        # Try to extract slide number and name
        # Formats: "01_封面", "01_cover", "Slide 01: Cover"
        num_match = re.match(r'(?:(?:Slide\s+)?(\d+)[_:]?\s*)(.*)', heading)
        if num_match:
            num = num_match.group(1)
            name = num_match.group(2).strip() if num_match.group(2) else ""
            if name:
                # Convert to safe filename
                safe_name = re.sub(r'[^\w\u4e00-\u9fff-]', '_', name)[:30]
                filename = f"{num}_{safe_name}.md"
            else:
                filename = f"{num}.md"
        else:
            # Fallback: use heading as filename
            safe_name = re.sub(r'[^\w\u4e00-\u9fff-]', '_', heading)[:30]
            count += 1
            filename = f"{count:02d}_{safe_name}.md"

        # Remove heading line from content (individual files don't need # heading)
        body = re.sub(r'^#\s+.+\n?', '', section, count=1).strip()

        output_path = notes_dir / filename
        output_path.write_text(body + "\n", encoding="utf-8")
        print(f"  Created: notes/{filename}")

    print(f"\nSplit complete: {count or len(sections)-1} note files created")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 split-notes.py <slide-deck-dir>")
        sys.exit(1)

    deck_dir = Path(sys.argv[1])
    total_md = deck_dir / "notes" / "total.md"

    if not total_md.exists():
        print(f"Error: {total_md} not found")
        print("Make sure notes/total.md exists in the slide deck directory.")
        sys.exit(1)

    print(f"Splitting: {total_md}")
    split_notes(total_md)


if __name__ == "__main__":
    main()
