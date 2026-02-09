#!/usr/bin/env python3
"""
Clean common text artifacts left after HTML/figure/citation stripping.

Targets patterns such as:
- Empty brackets: (), [], {}
- Broken figure mentions: "as shown in ." / "shown in ."
- Spacing/punctuation debris after removals
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


EMPTY_BRACKETS_RE = re.compile(r"\(\s*\)|\[\s*\]|\{\s*\}")
BROKEN_FIGURE_REF_RE = re.compile(
    r"\b(?:as\s+)?(?:is\s+)?shown\s+in\s*\.",
    flags=re.IGNORECASE,
)
BROKEN_PARENTHESES_SENTENCE_RE = re.compile(r"\(\s*\)\s*\.")
SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,.;:!?])")
MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")
MULTI_BLANK_LINES_RE = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    """Apply artifact cleanup rules to extracted markdown text."""
    text = EMPTY_BRACKETS_RE.sub("", text)
    text = BROKEN_FIGURE_REF_RE.sub("", text)
    text = BROKEN_PARENTHESES_SENTENCE_RE.sub(".", text)
    text = SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)
    text = MULTI_SPACE_RE.sub(" ", text)
    text = MULTI_BLANK_LINES_RE.sub("\n\n", text)
    return text.strip() + "\n"


def process_file(in_file: Path, out_file: Path, force: bool = False) -> bool:
    """Process one markdown file. Returns True if content changed."""
    if not in_file.exists():
        raise FileNotFoundError(f"Input file not found: {in_file}")
    if out_file.exists() and not force and in_file != out_file:
        raise FileExistsError(f"Output file exists (use --force): {out_file}")

    original = in_file.read_text(encoding="utf-8")
    cleaned = clean_text(original)
    changed = cleaned != original

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(cleaned, encoding="utf-8")
    return changed


def _default_output_path(in_file: Path) -> Path:
    """Return a safe default output path that won't overwrite the input."""
    return in_file.with_stem(in_file.stem + "_cleaned")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean extraction artifacts in markdown files."
    )
    parser.add_argument("--in-file", type=Path, help="Input markdown file")
    parser.add_argument("--out-file", type=Path, help="Output markdown file")
    parser.add_argument("--in-dir", type=Path, help="Input directory with .md files")
    parser.add_argument(
        "--out-dir",
        type=Path,
        help="Output directory for cleaned .md files (default: <in-dir>_cleaned)",
    )
    parser.add_argument(
        "--in-place",
        action="store_true",
        help="Rewrite input file(s) in place",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output file(s) if they exist",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.in_file:
        if args.in_place:
            out_file = args.in_file
        elif args.out_file:
            out_file = args.out_file
        else:
            out_file = _default_output_path(args.in_file)
        changed = process_file(args.in_file, out_file, force=args.force)
        print(f"[ok] {args.in_file} -> {out_file} ({'changed' if changed else 'no-op'})")
        return 0

    if args.in_dir:
        if args.in_place:
            out_dir = args.in_dir
        elif args.out_dir:
            out_dir = args.out_dir
        else:
            out_dir = args.in_dir.parent / (args.in_dir.name + "_cleaned")
        files = sorted(args.in_dir.rglob("*.md"))
        if not files:
            print(f"[info] no .md files in {args.in_dir}")
            return 0
        changed_count = 0
        errors = 0
        for in_file in files:
            rel = in_file.relative_to(args.in_dir)
            out_file = out_dir / rel
            try:
                changed = process_file(in_file, out_file, force=args.force)
                if changed:
                    changed_count += 1
            except Exception as exc:  # noqa: BLE001
                print(f"[error] {in_file}: {exc}")
                errors += 1
        print(f"[ok] processed {len(files)} files; changed {changed_count}; errors {errors}")
        return 1 if errors else 0

    raise SystemExit("Provide either --in-file or --in-dir")


if __name__ == "__main__":
    raise SystemExit(main())
