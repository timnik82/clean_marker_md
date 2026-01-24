#!/usr/bin/env python3
"""
Clean Marker-generated Markdown:
- drops tables, images, captions, math, and end-matter sections
- flattens output into a single folder by default
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


ENDMATTER_KEYWORDS = [
    "references",
    "bibliography",
    "acknowledgements",
    "acknowledgments",
    "acknowledgment",
    "acknowledgement",
    "credit authorship",
    "conflict of interest",
    "declaration of competing interest",
    "declaration of competing interests",
    "competing interest",
    "competing interests",
    "declaration of interests",
    "declarations",
    "funding",
    "author contributions",
    "data availability",
    "code availability",
    "ethics",
    "ethics statement",
    "supplementary",
    "supplementary material",
    "supplementary materials",
    "appendix",
    "appendices",
    "disclosure",
    "disclosures",
]

HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")

TABLE_SEPARATOR_RE = re.compile(
    r"^\s*\|?\s*:?-{3,}(:?\s*\|\s*:?-{3,})+\s*\|?\s*$"
)

IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
IMAGE_REF_RE = re.compile(r"!\[[^\]]*\]\[[^\]]+\]")
HTML_IMG_RE = re.compile(r"<img\s", re.IGNORECASE)
SPAN_ONLY_RE = re.compile(r"^\s*(<span\b[^>]*>\s*</span>\s*)+$", re.IGNORECASE)
EMPTY_SPAN_RE = re.compile(r"<span\b[^>]*>\s*</span>", re.IGNORECASE)

CAPTION_RE = re.compile(
    r"^\s*(figure|fig\.|table)\s*\d+\s*[:.\-]\s+.+",
    re.IGNORECASE,
)
CAPTION_TEXT_RE = re.compile(
    r"^\s*(figure|fig\.|table)\s*\d+\b(?:\s*\([^)]+\))?\s+.+",
    re.IGNORECASE,
)
CAPTION_ONLY_RE = re.compile(r"^\s*(figure|fig\.|table)\s*\d+\s*$", re.IGNORECASE)
CAPTION_CONTINUED_RE = re.compile(
    r"^\s*(figure|fig\.|table)\s*\d+\s*\([^)]+\)\s*$",
    re.IGNORECASE,
)
LEADING_HTML_TAG_RE = re.compile(r"^(?:\s*<[^>]+>\s*)+")

INLINE_MATH_RE = re.compile(
    r"(?<!\\)\$(?!\$).+?(?<!\\)\$|\\\(.+?\\\)",
    re.DOTALL,
)

MATH_BLOCK_PATTERNS = [
    re.compile(r"\$\$.*?\$\$", re.DOTALL),
    re.compile(
        r"\\begin\{(equation\*?|align\*?|gather\*?|multline\*?)\}.*?"
        r"\\end\{\1\}",
        re.DOTALL,
    ),
]

DISPLAY_MATH_BRACKET_RE = re.compile(r"\\\[(.*?)\\\]")
DISPLAY_MATH_CITATION_RE = re.compile(r"^\s*[\d,\-–\s]+\s*$")
DISPLAY_MATH_MAX_LEN = 200


def normalize_heading(text: str) -> str:
    cleaned = re.sub(r"[*_`]+", "", text)
    cleaned = re.sub(r"[:#*]+$", "", cleaned).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.lower()


def is_headingish(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if HEADING_RE.match(stripped):
        return True
    if re.search(r"[.!?]", stripped):
        return False
    if len(stripped) > 80:
        return False
    if re.match(r"^[-*+]\s", stripped):
        return False
    return True


def is_endmatter_heading(line: str) -> bool:
    match = HEADING_RE.match(line)
    if match:
        heading = normalize_heading(match.group(1))
        return any(heading.startswith(k) for k in ENDMATTER_KEYWORDS)
    if not is_headingish(line):
        return False
    heading = normalize_heading(line)
    return any(heading == k or heading.startswith(k) for k in ENDMATTER_KEYWORDS)


def is_table_row(line: str) -> bool:
    if TABLE_SEPARATOR_RE.match(line):
        return False
    return line.count("|") >= 2


def remove_math_blocks(text: str) -> str:
    for pattern in MATH_BLOCK_PATTERNS:
        text = pattern.sub("\n\n", text)

    def replace_in_line(line: str) -> str:
        def replace_display(match: re.Match[str]) -> str:
            inner = match.group(1)
            tail = line[match.end() :]
            if tail.startswith("]("):
                return match.group(0)
            if DISPLAY_MATH_CITATION_RE.match(inner):
                return match.group(0)
            if len(inner) > DISPLAY_MATH_MAX_LEN:
                return match.group(0)
            return " "

        return DISPLAY_MATH_BRACKET_RE.sub(replace_display, line)

    lines = text.split("\n")
    cleaned_lines = [replace_in_line(line) for line in lines]
    return "\n".join(cleaned_lines)


def contains_inline_math(text: str) -> bool:
    return bool(INLINE_MATH_RE.search(text))


def is_structured_line(line: str) -> bool:
    if re.match(r"^\s*#{1,6}\s+", line):
        return True
    if re.match(r"^\s*[-*+]\s+", line):
        return True
    if re.match(r"^\s*\d+\.\s+", line):
        return True
    if re.match(r"^\s*>\s+", line):
        return True
    if re.match(r"^\s*```", line):
        return True
    return False


def is_structured_block(lines: list[str]) -> bool:
    return any(is_structured_line(line) for line in lines)


def strip_inline_emphasis(line: str) -> str:
    return re.sub(r"[*_]{1,3}", "", line)


def caption_candidate(line: str) -> str:
    stripped = LEADING_HTML_TAG_RE.sub("", line)
    return strip_inline_emphasis(stripped).strip()


def clean_paragraph(paragraph: str, drop_math: bool) -> str:
    if not drop_math:
        return paragraph.strip()
    lines = paragraph.splitlines()
    if is_structured_block(lines):
        kept = [ln for ln in lines if not contains_inline_math(ln)]
        return "\n".join(kept).strip()
    collapsed = re.sub(r"\s*\n\s*", " ", paragraph).strip()
    if not collapsed:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", collapsed)
    kept = [s.strip() for s in sentences if s.strip() and not contains_inline_math(s)]
    return " ".join(kept).strip()


def cleanup_text(
    text: str,
    drop_endmatter: bool = True,
    drop_tables: bool = True,
    drop_images: bool = True,
    drop_captions: bool = True,
    drop_math: bool = True,
) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = remove_math_blocks(text)

    lines = text.split("\n")
    filtered: list[str] = []
    in_table = False
    skip_next_blank = False
    i = 0

    while i < len(lines):
        raw_line = lines[i]
        line = EMPTY_SPAN_RE.sub("", raw_line)

        if skip_next_blank and line.strip() == "":
            i += 1
            continue
        if skip_next_blank and line.strip():
            skip_next_blank = False

        if drop_endmatter and is_endmatter_heading(line):
            break

        if drop_tables and in_table:
            if line.strip() == "":
                in_table = False
                filtered.append("")
                i += 1
                continue
            if is_table_row(line) or TABLE_SEPARATOR_RE.match(line):
                i += 1
                continue
            in_table = False

        if drop_tables and i + 1 < len(lines) and is_table_row(line):
            if TABLE_SEPARATOR_RE.match(lines[i + 1]):
                in_table = True
                i += 2
                continue

        if drop_tables and TABLE_SEPARATOR_RE.match(line):
            in_table = True
            i += 1
            continue

        if drop_images and (
            IMAGE_MD_RE.search(line) or IMAGE_REF_RE.search(line) or HTML_IMG_RE.search(line)
        ):
            i += 1
            continue

        if SPAN_ONLY_RE.match(raw_line):
            i += 1
            continue

        if drop_captions:
            candidate = caption_candidate(line)
            prev_line_blank = not filtered or filtered[-1].strip() == ""
            next_line_blank = i + 1 < len(lines) and lines[i + 1].strip() == ""
            if (
                (prev_line_blank or next_line_blank)
                and (
                    CAPTION_RE.match(candidate)
                    or CAPTION_TEXT_RE.match(candidate)
                    or CAPTION_ONLY_RE.match(candidate)
                    or CAPTION_CONTINUED_RE.match(candidate)
                )
            ):
                prev_nonempty = ""
                for prior in reversed(filtered):
                    if prior.strip():
                        prev_nonempty = prior
                        break
                next_nonempty = ""
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        next_nonempty = lines[j]
                        break
                if (
                    prev_nonempty
                    and next_nonempty
                    and not is_structured_line(prev_nonempty)
                    and not is_structured_line(next_nonempty)
                ):
                    while filtered and filtered[-1].strip() == "":
                        filtered.pop()
                    skip_next_blank = True
                i += 1
                continue

        filtered.append(line)
        i += 1

    text = "\n".join(filtered)
    paragraphs = re.split(r"\n\s*\n", text)
    cleaned_paragraphs = []
    for para in paragraphs:
        cleaned = clean_paragraph(para, drop_math=drop_math)
        if cleaned:
            cleaned_paragraphs.append(cleaned)

    output = "\n\n".join(cleaned_paragraphs)
    output = re.sub(r"[ \t]+$", "", output, flags=re.MULTILINE)
    output = re.sub(r"\n{3,}", "\n\n", output).strip() + "\n"
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Clean Marker Markdown output (drop tables, images, math, end-matter)."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--in-dir", type=Path, help="Directory containing .md files")
    group.add_argument("--in-file", type=Path, help="Single markdown file to clean")
    parser.add_argument("--out-dir", type=Path, help="Output directory (for --in-dir)")
    parser.add_argument("--out-file", type=Path, help="Output file (for --in-file)")
    parser.add_argument("--ext", default=".md", help="File extension to process (default: .md)")
    parser.add_argument("--dry-run", action="store_true", help="Show actions without writing files")
    parser.add_argument(
        "--keep-tree",
        action="store_true",
        help="Preserve input subfolders instead of flattening into out-dir",
    )
    parser.add_argument("--keep-endmatter", action="store_true", help="Do not truncate end-matter")
    parser.add_argument("--keep-tables", action="store_true", help="Do not drop tables")
    parser.add_argument("--keep-images", action="store_true", help="Do not drop images")
    parser.add_argument("--keep-captions", action="store_true", help="Do not drop captions")
    parser.add_argument("--keep-math", action="store_true", help="Do not drop math sentences")
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    drop_endmatter = not args.keep_endmatter
    drop_tables = not args.keep_tables
    drop_images = not args.keep_images
    drop_captions = not args.keep_captions
    drop_math = not args.keep_math

    if args.in_dir:
        if not args.out_dir:
            print("--out-dir is required with --in-dir", file=sys.stderr)
            return 2
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

        for path in sorted(in_dir.rglob(f"*{args.ext}")):
            if args.keep_tree:
                rel = path.relative_to(in_dir)
                out_path = out_dir / rel
                if not args.dry_run:
                    out_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                out_path = out_dir / unique_name(path.name)
            content = path.read_text(encoding="utf-8", errors="ignore")
            cleaned = cleanup_text(
                content,
                drop_endmatter=drop_endmatter,
                drop_tables=drop_tables,
                drop_images=drop_images,
                drop_captions=drop_captions,
                drop_math=drop_math,
            )
            if args.dry_run:
                print(f"Would write: {out_path}")
            else:
                out_path.write_text(cleaned, encoding="utf-8")
        return 0

    in_file = args.in_file
    if not args.out_file:
        print("--out-file is required with --in-file", file=sys.stderr)
        return 2
    if not in_file.exists():
        print(f"Input file not found: {in_file}", file=sys.stderr)
        return 2
    content = in_file.read_text(encoding="utf-8", errors="ignore")
    cleaned = cleanup_text(
        content,
        drop_endmatter=drop_endmatter,
        drop_tables=drop_tables,
        drop_images=drop_images,
        drop_captions=drop_captions,
        drop_math=drop_math,
    )
    if args.dry_run:
        print(f"Would write: {args.out_file}")
        return 0
    args.out_file.parent.mkdir(parents=True, exist_ok=True)
    args.out_file.write_text(cleaned, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
