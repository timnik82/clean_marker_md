#!/usr/bin/env python3
"""
Remove image placeholders and page anchors from Marker-generated Markdown.

This script removes:
- Standalone image references (e.g., ![](_page_0_Picture_0.jpeg))
- HTML page anchor spans (e.g., <span id="page-X-Y"></span>)

While preserving all other content including:
- Tables
- Text content
- Links
- Captions
- All other markdown formatting
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Pattern to match image placeholders like ![](_page_0_Picture_0.jpeg)
IMAGE_PLACEHOLDER_RE = re.compile(r"^!\[[^\]]*\]\([^)]+\)\s*$")

# Pattern to match page anchor spans like <span id="page-4-0"></span>
PAGE_ANCHOR_RE = re.compile(r'<span id="page-\d+-\d+"></span>')


def remove_image_placeholders(text: str) -> str:
    """
    Remove lines containing only image placeholders and page anchor spans from markdown text.
    
    Args:
        text: Input markdown text
        
    Returns:
        Cleaned text with image placeholder lines and page anchors removed
    """
    lines = text.split("\n")
    filtered_lines = []
    
    for line in lines:
        # Skip lines that are only image placeholders
        if IMAGE_PLACEHOLDER_RE.match(line.strip()):
            continue
        
        # Remove page anchor spans from all lines
        line = PAGE_ANCHOR_RE.sub('', line)
        
        filtered_lines.append(line)
    
    # Join lines and clean up excessive blank lines
    output = "\n".join(filtered_lines)
    
    # Remove multiple consecutive blank lines (keep max 2 for paragraph spacing)
    output = re.sub(r"\n{3,}", "\n\n", output)
    
    # Ensure file ends with a single newline
    output = output.strip() + "\n"
    
    return output


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Remove image placeholders from Marker-generated markdown."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--in-dir", type=Path, help="Directory containing .md files")
    group.add_argument("--in-file", type=Path, help="Single markdown file to process")
    parser.add_argument(
        "--out-dir", 
        type=Path, 
        default=Path("out_clean"),
        help="Output directory (default: out_clean)"
    )
    parser.add_argument(
        "--out-file", 
        type=Path, 
        help="Output file (for --in-file). If not specified, uses out_clean/<filename>"
    )
    parser.add_argument(
        "--ext", default=".md", help="File extension to process (default: .md)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show actions without writing files",
    )
    parser.add_argument(
        "--keep-tree",
        action="store_true",
        help="Preserve input subfolders instead of flattening into out-dir",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output files (default: skip if output exists)",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show statistics about removed image placeholders",
    )
    return parser.parse_args()


def count_image_placeholders(text: str) -> int:
    """Count the number of image placeholder lines in the text."""
    lines = text.split("\n")
    count = 0
    for line in lines:
        if IMAGE_PLACEHOLDER_RE.match(line.strip()):
            count += 1
    return count


def count_page_anchors(text: str) -> int:
    """Count the number of page anchor spans in the text."""
    return len(PAGE_ANCHOR_RE.findall(text))


def main() -> int:
    """Main function."""
    args = parse_args()

    if args.in_dir:
        in_dir = args.in_dir
        out_dir = args.out_dir
        if not in_dir.exists():
            print(f"Input directory not found: {in_dir}", file=sys.stderr)
            return 2
        if not args.dry_run:
            out_dir.mkdir(parents=True, exist_ok=True)

        used_names: dict[str, int] = {}

        def unique_name(filename: str) -> str:
            if filename not in used_names:
                used_names[filename] = 0
                return filename
            used_names[filename] += 1
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            return f"{stem}_{used_names[filename]}{suffix}"

        total_removed = 0
        total_anchors_removed = 0
        total_files = 0

        for path in sorted(in_dir.rglob(f"*{args.ext}")):
            if args.keep_tree:
                rel = path.relative_to(in_dir)
                out_path = out_dir / rel
                if not args.dry_run:
                    out_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                out_path = out_dir / unique_name(path.name)

            content = path.read_text(encoding="utf-8", errors="ignore")
            
            if args.stats:
                removed_count = count_image_placeholders(content)
                anchors_count = count_page_anchors(content)
                total_removed += removed_count
                total_anchors_removed += anchors_count
                total_files += 1
                if removed_count > 0 or anchors_count > 0:
                    print(f"{path.name}: {removed_count} images, {anchors_count} page anchors")
            
            cleaned = remove_image_placeholders(content)

            if args.dry_run:
                print(f"Would write: {out_path}")
            else:
                if out_path.exists() and not args.force:
                    print(f"Skipping existing output: {out_path}")
                    continue
                out_path.write_text(cleaned, encoding="utf-8")
                if not args.stats:
                    print(f"Processed: {path.name} -> {out_path.name}")

        if args.stats:
            print(f"\nTotal: Removed {total_removed} image placeholders and {total_anchors_removed} page anchors from {total_files} files")
        return 0

    # Process single file
    in_file = args.in_file
    if not in_file.exists():
        print(f"Input file not found: {in_file}", file=sys.stderr)
        return 2
    
    # Auto-generate output file path if not specified
    if not args.out_file:
        out_file = args.out_dir / in_file.name
    else:
        out_file = args.out_file

    content = in_file.read_text(encoding="utf-8", errors="ignore")
    
    if args.stats:
        removed_count = count_image_placeholders(content)
        anchors_count = count_page_anchors(content)
        print(f"Found {removed_count} image placeholders and {anchors_count} page anchors to remove")
    
    cleaned = remove_image_placeholders(content)

    if args.dry_run:
        print(f"Would write: {out_file}")
        if args.stats:
            print(f"Would remove {removed_count} image placeholders and {anchors_count} page anchors")
        return 0

    if out_file.exists() and not args.force:
        print(f"Skipping existing output: {out_file}")
        return 0

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(cleaned, encoding="utf-8")
    print(f"Processed: {in_file.name} -> {out_file}")
    if args.stats:
        print(f"Removed {removed_count} image placeholders and {anchors_count} page anchors")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
