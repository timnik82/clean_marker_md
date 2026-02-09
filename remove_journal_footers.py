#!/usr/bin/env python3
"""
Remove journal page footers from academic paper Markdown files.

Removes patterns like:
- "*Biosensors* **2023**, *13*, 328 2 of 37"
- "*Nature* **2024**, *15*, 1234 5 of 20"
- "*Science* **2023**, *42*, 999 X of Y"

These footers typically appear as lines or text fragments embedded in the document
and break the reading flow.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# Pattern to detect journal footer lines with optional <sup> tags
# Matches: *journal name* **year**, *volume*, issue/article number X of Y
# Handles variants like: *Biosensors* **<sup>2023</sup>**, *<sup>13</sup>*, 328 16 of 37
JOURNAL_FOOTER_PATTERN = re.compile(
    r"\*[A-Za-z\s&\-]+\*\s+\*\*<sup>?\d{4}</sup>?\*\*,?\s+\*<sup>?\d+</sup>?\*,\s*\d+\s+\d+\s+of\s+\d+",
    re.IGNORECASE,
)

# More lenient pattern for incomplete or variant footers
FOOTER_PATTERN_LENIENT = re.compile(
    r"\*[A-Za-z\s&\-]+\*\s+\*\*<sup>?\d{4}</sup>?\*\*.*?\d+\s+of\s+\d+", re.IGNORECASE
)

# Pattern for embedded footers (where footer appears mid-line)
EMBEDDED_FOOTER_PATTERN = re.compile(
    r"\s+\*[A-Za-z\s&\-]+\*\s+\*\*<sup>?\d{4}</sup>?\*\*.*?\d+\s+of\s+\d+(?:\s|$)",
    re.IGNORECASE,
)

# Pattern for standalone page numbers: "X of Y" or "<sup>X</sup> of <sup>Y</sup>"
PAGE_NUMBER_PATTERN = re.compile(
    r"<sup>?\d+</sup>?\s+of\s+<sup>?\d+</sup>?", re.IGNORECASE
)

# Pattern for "FOR PEER REVIEW" text
PEER_REVIEW_PATTERN = re.compile(r"x?\s+FOR\s+PEER\s+REVIEW", re.IGNORECASE)


def remove_journal_footers(text: str, lenient: bool = False) -> str:
    """
    Remove journal page footers from text.

    Args:
        text: The markdown text to clean
        lenient: If True, use more lenient pattern matching

    Returns:
        Text with journal footers removed
    """
    lines = text.split("\n")
    cleaned_lines = []

    for line in lines:
        # Check if line is entirely a footer
        stripped = line.strip()
        if JOURNAL_FOOTER_PATTERN.match(stripped):
            # Skip entirely footer lines
            continue
        if lenient and FOOTER_PATTERN_LENIENT.match(stripped):
            continue

        # Remove embedded footers from lines
        # (footer appears in the middle of text)
        cleaned_line = EMBEDDED_FOOTER_PATTERN.sub(" ", line)

        # Remove "FOR PEER REVIEW" text
        cleaned_line = PEER_REVIEW_PATTERN.sub("", cleaned_line)

        # Remove standalone page numbers (X of Y) that are not part of proper content
        # Be conservative: only remove if it's on a line by itself or appears isolated
        # We'll remove the entire line if it's just a page number
        if PAGE_NUMBER_PATTERN.fullmatch(cleaned_line.strip()):
            continue

        # Clean up multiple spaces that might result from footer removal
        cleaned_line = re.sub(r"\s{2,}", " ", cleaned_line).strip()

        if cleaned_line or not stripped:
            # Keep non-empty lines or preserve blank lines for structure
            cleaned_lines.append(cleaned_line if cleaned_line else "")

    return "\n".join(cleaned_lines)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Remove journal page footers from academic paper Markdown files."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--in-file", type=Path, help="Single markdown file to clean")
    group.add_argument("--in-dir", type=Path, help="Directory containing .md files")

    parser.add_argument("--out-file", type=Path, help="Output file (for --in-file)")
    parser.add_argument("--out-dir", type=Path, help="Output directory (for --in-dir)")
    parser.add_argument(
        "--ext", default=".md", help="File extension to process (default: .md)"
    )
    parser.add_argument(
        "--lenient",
        action="store_true",
        help="Use lenient pattern matching for footers",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show actions without writing files"
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing output files"
    )
    parser.add_argument(
        "--keep-tree",
        action="store_true",
        help="Preserve input subfolders for --in-dir (default: flatten)",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.in_file:
        if not args.out_file:
            print("Error: --out-file is required with --in-file", file=sys.stderr)
            return 2
        if not args.in_file.exists():
            print(f"Error: Input file not found: {args.in_file}", file=sys.stderr)
            return 2

        content = args.in_file.read_text(encoding="utf-8", errors="ignore")
        cleaned = remove_journal_footers(content, lenient=args.lenient)

        if args.dry_run:
            print(f"Would write: {args.out_file}")
        else:
            if args.out_file.exists() and not args.force:
                print(f"Skipping existing output: {args.out_file}")
                return 0
            args.out_file.parent.mkdir(parents=True, exist_ok=True)
            args.out_file.write_text(cleaned, encoding="utf-8")
            print(f"Cleaned: {args.in_file} -> {args.out_file}")

        return 0

    if args.in_dir:
        if not args.out_dir:
            print("Error: --out-dir is required with --in-dir", file=sys.stderr)
            return 2
        if not args.in_dir.exists():
            print(f"Error: Input directory not found: {args.in_dir}", file=sys.stderr)
            return 2

        if not args.dry_run:
            args.out_dir.mkdir(parents=True, exist_ok=True)

        processed = 0
        for path in sorted(args.in_dir.rglob(f"*{args.ext}")):
            if args.keep_tree:
                rel = path.relative_to(args.in_dir)
                out_path = args.out_dir / rel
            else:
                out_path = args.out_dir / path.name

            if not args.dry_run:
                out_path.parent.mkdir(parents=True, exist_ok=True)

            content = path.read_text(encoding="utf-8", errors="ignore")
            cleaned = remove_journal_footers(content, lenient=args.lenient)

            if args.dry_run:
                print(f"Would clean: {path} -> {out_path}")
            else:
                if out_path.exists() and not args.force:
                    print(f"Skipping existing: {out_path}")
                    continue
                out_path.write_text(cleaned, encoding="utf-8")
                print(f"Cleaned: {path.name}")

            processed += 1

        print(f"\nProcessed {processed} file(s)")
        return 0

    print("Error: specify either --in-file or --in-dir", file=sys.stderr)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
