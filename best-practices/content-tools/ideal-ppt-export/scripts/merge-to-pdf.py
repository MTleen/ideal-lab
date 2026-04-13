#!/usr/bin/env python3
"""
SVG to PDF converter - merges all SVG slides into one PDF.

Usage: python3 merge-to-pdf.py <slide-deck-dir>

Dependencies: rsvg-convert (brew install librsvg), PyPDF2 (pip install PyPDF2)
"""

import sys
import os
import re
import glob
import subprocess
import tempfile
import shutil
from pathlib import Path

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 merge-to-pdf.py <slide-deck-dir>"); sys.exit(1)

    project_dir = Path(sys.argv[1]).resolve()
    slug = project_dir.name

    # Find SVG source
    svg_dir = project_dir / 'svg_final' if (project_dir / 'svg_final').exists() else project_dir / 'svg_output'
    if not svg_dir.exists():
        print(f"Error: No SVG directory found"); sys.exit(1)

    svg_files = sorted(svg_dir.glob('*.svg'), key=lambda f: int(re.match(r'(\d+)', f.name).group(1)))
    if not svg_files:
        print(f"Error: No SVG files in {svg_dir}"); sys.exit(1)

    print(f"Converting {len(svg_files)} SVGs to PDF...")

    # Create temp dir for individual PDFs
    temp_dir = Path(tempfile.mkdtemp())
    try:
        pdf_pages = []
        for i, svg_path in enumerate(svg_files, 1):
            pdf_path = temp_dir / f'{svg_path.stem}.pdf'
            result = subprocess.run(
                ['rsvg-convert', '-w', '1920', '-h', '1080', '-o', str(pdf_path), str(svg_path)],
                capture_output=True, text=True
            )
            if result.returncode == 0 and pdf_path.exists():
                pdf_pages.append(pdf_path)
                print(f"  [{i}/{len(svg_files)}] {svg_path.name}")
            else:
                print(f"  [{i}/{len(svg_files)}] {svg_path.name} - FAILED: {result.stderr.strip()}")

        if not pdf_pages:
            print("Error: No PDFs generated"); sys.exit(1)

        # Merge PDFs
        try:
            from PyPDF2 import PdfMerger
        except ImportError:
            print("Error: pip install PyPDF2"); sys.exit(1)

        output_path = project_dir / f'{slug}.pdf'
        merger = PdfMerger()
        for p in pdf_pages:
            merger.append(str(p))
        merger.write(str(output_path))
        merger.close()

        print(f"\nExported: {output_path} ({len(pdf_pages)} pages)")

    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == '__main__':
    main()
