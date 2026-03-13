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
import logging
import re
from pathlib import Path

logger = logging.getLogger(__name__)


EMPTY_BRACKETS_RE = re.compile(r"\(\s*\)|\[\s*\]|\{\s*\}")
BROKEN_FIGURE_REF_RE = re.compile(
    r"\b(?:as\s+)?(?:is\s+)?shown\s+in\s*\.",
    flags=re.IGNORECASE,
)
PAREN_FIGURE_REF_RE = re.compile(
    r"\(\s*(?:fig(?:ure)?|tab(?:le)?|scheme|eq(?:uation)?)s?\.?\s*"
    r"\d+[a-z]?(?:\s*[-–−]\s*\d+[a-z]?)*"
    r"(?:\s*[a-z](?:\s*[,/]\s*[a-z])*)?\s*\)",
    flags=re.IGNORECASE,
)
BROKEN_PARENTHESES_SENTENCE_RE = re.compile(r"\(\s*\)\s*\.")
SPACE_BEFORE_PUNCT_RE = re.compile(r"\s+([,.;:!?])")
MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")
MULTI_BLANK_LINES_RE = re.compile(r"\n{3,}")
# Superscript exponents flattened by HTML serialisation: "cm –1" → "cm-1".
# Matches a letter (unit abbreviation) + space + any minus/dash char + 1–2 digits.
SUPERSCRIPT_MINUS_RE = re.compile(r"([A-Za-z])\s[–−-](\d{1,2})\b")
# Subscript digits flattened by HTML serialisation: "CH 2" → "CH2".
# Restricted to 1–2 uppercase letters and 1–2 digits; \b before the group
# prevents matching the tail of longer words (e.g. "PI 3" inside "API 3").
# Single-digit subscripts are always merged (CH 2, CO 2, N 2, etc.).
# Two-digit subscripts skip merging when followed by a lowercase word to
# avoid collapsing geopolitical codes like "EU 27 countries".
SUBSCRIPT_DIGIT_RE = re.compile(r"\b([A-Z]{1,2})\s(\d)\b")
SUBSCRIPT_DIGIT2_RE = re.compile(r"\b([A-Z]{1,2})\s(\d{2})\b(?!\s+[a-z])")

CITATION_BRACKET_RE = re.compile(
    r"\[\s*(?:\d{1,3}(?:\s*[-–−]\s*\d{1,3})?)"
    r"(?:\s*[,;]\s*\d{1,3}(?:\s*[-–−]\s*\d{1,3})?)*\s*\]"
)
PAREN_CITATION_RE = re.compile(
    r"\(\s*\d{1,3}"
    r"(?:\s*[-–−]\s*\d{1,3}|\s*[,;]\s*\d{1,3}(?:\s*[-–−]\s*\d{1,3})?)"
    r"(?:\s*[,;]\s*\d{1,3}(?:\s*[-–−]\s*\d{1,3})?)*"
    r"\s*\)"
)


def clean_text(text: str, drop_citations: bool = False) -> str:
    """Apply artifact cleanup rules to extracted markdown text."""
    text = SUPERSCRIPT_MINUS_RE.sub(r"\1-\2", text)
    text = SUBSCRIPT_DIGIT_RE.sub(r"\1\2", text)
    text = SUBSCRIPT_DIGIT2_RE.sub(r"\1\2", text)
    if drop_citations:
        text = CITATION_BRACKET_RE.sub("", text)
        text = PAREN_CITATION_RE.sub("", text)
    text = PAREN_FIGURE_REF_RE.sub("", text)
    text = EMPTY_BRACKETS_RE.sub("", text)
    text = BROKEN_FIGURE_REF_RE.sub("", text)
    text = BROKEN_PARENTHESES_SENTENCE_RE.sub(".", text)
    text = SPACE_BEFORE_PUNCT_RE.sub(r"\1", text)
    text = MULTI_SPACE_RE.sub(" ", text)
    text = MULTI_BLANK_LINES_RE.sub("\n\n", text)
    return text.strip() + "\n"


def process_file(
    in_file: Path,
    out_file: Path,
    force: bool = False,
    dry_run: bool = False,
    drop_citations: bool = False,
) -> bool:
    """Process one markdown file. Returns True if content changed."""
    if not in_file.exists():
        raise FileNotFoundError(f"Input file not found: {in_file}")
    if out_file.exists() and not force and in_file != out_file:
        raise FileExistsError(f"Output file exists (use --force): {out_file}")

    original = in_file.read_text(encoding="utf-8")
    cleaned = clean_text(original, drop_citations=drop_citations)
    changed = cleaned != original

    if not dry_run:
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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would change without writing any files",
    )
    parser.add_argument(
        "--drop-citations",
        action="store_true",
        help="Drop numeric bracket citations like [12] and [3,4]",
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
    args = parse_args()

    if args.in_file:
        if args.in_place:
            out_file = args.in_file
        elif args.out_file:
            out_file = args.out_file
        else:
            out_file = _default_output_path(args.in_file)
        changed = process_file(
            args.in_file,
            out_file,
            force=args.force,
            dry_run=args.dry_run,
            drop_citations=args.drop_citations,
        )
        tag = "dry-run" if args.dry_run else "ok"
        logger.info(
            "[%s] %s -> %s (%s)",
            tag,
            args.in_file,
            out_file,
            "changed" if changed else "no-op",
        )
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
            logger.info("no .md files in %s", args.in_dir)
            return 0
        changed_count = 0
        errors = 0
        for in_file in files:
            rel = in_file.relative_to(args.in_dir)
            out_file = out_dir / rel
            try:
                changed = process_file(
                    in_file,
                    out_file,
                    force=args.force,
                    dry_run=args.dry_run,
                    drop_citations=args.drop_citations,
                )
                if changed:
                    changed_count += 1
            except Exception as exc:  # noqa: BLE001
                logger.error("%s: %s", in_file, exc)
                errors += 1
        tag = "dry-run" if args.dry_run else "ok"
        logger.info(
            "[%s] processed %d files; changed %d; errors %d",
            tag,
            len(files),
            changed_count,
            errors,
        )
        return 1 if errors else 0

    raise SystemExit("Provide either --in-file or --in-dir")


if __name__ == "__main__":
    raise SystemExit(main())
