#!/usr/bin/env python3
"""
Optionally reflow reading order artifacts in Marker-cleaned Markdown.

This script is intentionally conservative. It only stitches paragraphs when:
- a short interruption block (metadata/caption-like text) appears between them
- the previous paragraph looks unfinished
- the next paragraph looks like a continuation

The interruption block is preserved and moved after the stitched paragraph.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

PARA_SPLIT_RE = re.compile(r"\n\s*\n")
TRAILING_SPACE_RE = re.compile(r"[ \t]+$")
MULTI_SPACE_RE = re.compile(r"[ \t]{2,}")

METADATA_HINT_RE = re.compile(
    r"("
    r"received:\s|revised:\s|accepted:\s|published:\s|"
    r"published in the topical collection|"
    r"\bcorresponding author\b|"
    r"\bemail:\b|\borcid\b|"
    r"@\w+\.\w+"
    r")",
    re.IGNORECASE,
)
CAPTION_HINT_RE = re.compile(
    r"^(?:\*\*)?(?:fig(?:ure)?|table)\.?\s*\d+[a-z]?(?:\s|[:.\-])",
    re.IGNORECASE,
)
STRUCTURED_LINE_RE = re.compile(r"^\s*(#{1,6}\s|[-*+]\s|\d+\.\s|>\s|```|\|)")
AFFILIATION_LINE_RE = re.compile(
    r"^\s*[-*+]\s*(?:\\?\*\s*)?(?:<sup>\d+</sup>|\w.*@\w+\.\w+)",
    re.IGNORECASE,
)
CONTINUATION_START_RE = re.compile(
    r"^(?:[a-z]|\(|\[|"
    r"and\b|or\b|to\b|from\b|for\b|with\b|where\b|which\b|that\b|"
    r"this\b|these\b|those\b|of\b|in\b|on\b|by\b|as\b|while\b|"
    r"but\b|also\b|however\b|moreover\b|additionally\b|therefore\b)",
    re.IGNORECASE,
)


@dataclass
class ReflowStats:
    stitched_pairs: int = 0
    shifted_blocks: int = 0


def split_paragraphs(text: str) -> list[str]:
    parts = PARA_SPLIT_RE.split(text.replace("\r\n", "\n").replace("\r", "\n"))
    return [p.strip() for p in parts if p.strip()]


def is_structured_paragraph(paragraph: str) -> bool:
    return any(STRUCTURED_LINE_RE.match(line) for line in paragraph.splitlines())


def is_interruption_block(paragraph: str) -> bool:
    lines = paragraph.splitlines()
    if len(lines) > 12 or len(paragraph) > 1800:
        return False
    if METADATA_HINT_RE.search(paragraph):
        return True
    if CAPTION_HINT_RE.match(paragraph.strip()):
        return True
    if sum(1 for line in lines if AFFILIATION_LINE_RE.match(line)) >= 2:
        return True
    return False


def paragraph_looks_incomplete(paragraph: str) -> bool:
    if is_structured_paragraph(paragraph):
        return False
    stripped = paragraph.strip()
    if len(stripped) < 40:
        return False
    if stripped.endswith((".", "!", "?")):
        return False
    return True


def paragraph_looks_like_continuation(paragraph: str) -> bool:
    if is_structured_paragraph(paragraph):
        return False
    stripped = paragraph.strip()
    if not stripped:
        return False
    return bool(CONTINUATION_START_RE.match(stripped))


def can_stitch(previous: str, following: str) -> bool:
    return paragraph_looks_incomplete(previous) and paragraph_looks_like_continuation(
        following
    )


def stitch_paragraphs(previous: str, following: str) -> str:
    stitched = f"{previous.rstrip()} {following.lstrip()}"
    stitched = MULTI_SPACE_RE.sub(" ", stitched)
    return stitched.strip()


def reflow_paragraphs(paragraphs: list[str]) -> tuple[list[str], ReflowStats]:
    output: list[str] = []
    stats = ReflowStats()
    i = 0

    while i < len(paragraphs):
        current = paragraphs[i]
        if output and is_interruption_block(current):
            j = i
            while j < len(paragraphs) and is_interruption_block(paragraphs[j]):
                j += 1
            if j < len(paragraphs) and can_stitch(output[-1], paragraphs[j]):
                output[-1] = stitch_paragraphs(output[-1], paragraphs[j])
                output.extend(paragraphs[i:j])
                stats.stitched_pairs += 1
                stats.shifted_blocks += j - i
                i = j + 1
                continue
        output.append(current)
        i += 1

    return output, stats


def reflow_text(text: str, passes: int = 2) -> tuple[str, ReflowStats]:
    paragraphs = split_paragraphs(text)
    total = ReflowStats()

    for _ in range(max(1, passes)):
        paragraphs, stats = reflow_paragraphs(paragraphs)
        total.stitched_pairs += stats.stitched_pairs
        total.shifted_blocks += stats.shifted_blocks
        if stats.stitched_pairs == 0:
            break

    output = "\n\n".join(paragraphs)
    output = TRAILING_SPACE_RE.sub("", output)
    output = re.sub(r"\n{3,}", "\n\n", output)
    return output.strip() + "\n", total


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Optionally reflow interrupted reading order artifacts "
            "(useful for some two-column PDFs)."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--in-dir", type=Path, help="Directory containing .md files")
    group.add_argument("--in-file", type=Path, help="Single markdown file to process")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("out_reflow"),
        help="Output directory (default: out_reflow)",
    )
    parser.add_argument(
        "--out-file",
        type=Path,
        help="Output file (for --in-file). If not specified, uses out_reflow/<filename>",
    )
    parser.add_argument(
        "--passes",
        type=int,
        default=2,
        help="Maximum reflow passes (default: 2)",
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
        help="Show per-file reflow statistics",
    )
    return parser.parse_args()


def process_file(
    in_path: Path,
    out_path: Path,
    passes: int,
    dry_run: bool,
    force: bool,
    stats: bool,
) -> ReflowStats:
    content = in_path.read_text(encoding="utf-8", errors="ignore")
    reflowed, file_stats = reflow_text(content, passes=passes)

    if dry_run:
        print(f"Would write: {out_path}")
    else:
        if out_path.exists() and not force:
            print(f"Skipping existing output: {out_path}")
            return ReflowStats()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(reflowed, encoding="utf-8")

    if stats:
        print(
            f"{in_path.name}: stitched={file_stats.stitched_pairs}, "
            f"shifted_blocks={file_stats.shifted_blocks}"
        )
    return file_stats


def main() -> int:
    args = parse_args()

    if args.in_dir:
        in_dir = args.in_dir
        if not in_dir.exists():
            print(f"Input directory not found: {in_dir}", file=sys.stderr)
            return 2
        if not args.dry_run:
            args.out_dir.mkdir(parents=True, exist_ok=True)

        total = ReflowStats()
        used_names: dict[str, int] = {}

        def unique_name(filename: str) -> str:
            if filename not in used_names:
                used_names[filename] = 0
                return filename
            used_names[filename] += 1
            stem = Path(filename).stem
            suffix = Path(filename).suffix
            return f"{stem}_{used_names[filename]}{suffix}"

        for in_path in sorted(in_dir.rglob(f"*{args.ext}")):
            if args.keep_tree:
                rel = in_path.relative_to(in_dir)
                out_path = args.out_dir / rel
            else:
                out_path = args.out_dir / unique_name(in_path.name)
            file_stats = process_file(
                in_path=in_path,
                out_path=out_path,
                passes=args.passes,
                dry_run=args.dry_run,
                force=args.force,
                stats=args.stats,
            )
            total.stitched_pairs += file_stats.stitched_pairs
            total.shifted_blocks += file_stats.shifted_blocks

        if args.stats:
            print(
                f"\nTotal: stitched={total.stitched_pairs}, "
                f"shifted_blocks={total.shifted_blocks}"
            )
        return 0

    in_file = args.in_file
    if not in_file.exists():
        print(f"Input file not found: {in_file}", file=sys.stderr)
        return 2

    out_file = args.out_file if args.out_file else args.out_dir / in_file.name
    process_file(
        in_path=in_file,
        out_path=out_file,
        passes=args.passes,
        dry_run=args.dry_run,
        force=args.force,
        stats=args.stats,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
