#!/usr/bin/env python3
"""
Clean Marker-generated Markdown:
- drops tables, images, captions, math, numeric citations, and end-matter sections
- flattens output into a single folder by default
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ENDMATTER_TRUNCATE_KEYWORDS = [
    "references",
    "bibliography",
    "supplementary",
    "supplementary material",
    "supplementary materials",
    "appendix",
    "appendices",
]

ENDMATTER_SECTION_KEYWORDS = [
    "keywords",
    "key words",
    "author information",
    "corresponding authors",
    "authors",
    "author contributions",
    "notes",
    "biography",
    "biographies",
    "associated content",
    "supporting information",
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
    "data availability",
    "code availability",
    "ethics",
    "ethics statement",
    "disclosure",
    "disclosures",
]

HEADING_RE = re.compile(r"^\s{0,3}#{1,6}\s+(.+?)\s*$")

TABLE_SEPARATOR_RE = re.compile(r"^\s*\|?\s*:?-{3,}(:?\s*\|\s*:?-{3,})+\s*\|?\s*$")

IMAGE_MD_RE = re.compile(r"!\[[^\]]*\]\([^)]+\)")
IMAGE_REF_RE = re.compile(r"!\[[^\]]*\]\[[^\]]+\]")
HTML_IMG_RE = re.compile(r"<img\s", re.IGNORECASE)
IMAGE_DESC_RE = re.compile(r"^Image\s+/page/\d+/", re.IGNORECASE)
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
HEADING_BREAK_RE = re.compile(r"[,;:]")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
PAGE_LINK_RE = re.compile(r"\(#page-\d+-\d+\)")
SUP_TAG_RE = re.compile(r"<sup\b[^>]*>\s*(.*?)\s*</sup>", re.IGNORECASE | re.DOTALL)
DECORATIVE_HEADING_PREFIX_RE = re.compile(r"^(?:\s*[■•▪▫◦◆◇●○◉]+)+\s*")
WORD_SUFFIX_CITATION_RE = re.compile(
    r"(\w+)\[([a-zA-Z]*)(\d+[0-9.,–\-\u2013\u2014]*)\]"
)
NUMERIC_BRACKET_TRAILING_DOT_RE = re.compile(r"\[([\d.,–\-\u2013\u2014\s]+)\.\]")
# Conservative citation matcher: numeric/alphanumeric citation tokens
# (up to 3 digits with optional lowercase suffix per item).
# Examples matched: [151], [5,6], [61-65], [.13], [(10),], [47g]
CITATION_BRACKET_RE = re.compile(
    r"\[(?:\s*[.,]?\s*\\?\(?\s*\d{1,3}[a-z]?\s*\\?\)?\s*"
    r"(?:[-,–\u2013\u2014]\s*[.,]?\s*\\?\(?\s*\d{1,3}[a-z]?\s*\\?\)?\s*)*"
    r"[.,]?\s*)\]"
)
# Normalize escaped citation tokens such as "\[12\]" / "\[61e\]"
# or "[\[12\]]" / "[\[61e\]]".
ESCAPED_NUMERIC_CITATION_RE = re.compile(
    r"\\\[(\s*[0-9][0-9a-z.,,\-–\u2013\u2014\s]*)\\\]"
)
NESTED_ESCAPED_NUMERIC_CITATION_RE = re.compile(
    r"\[\s*\\\[(\s*[0-9][0-9a-z.,,\-–\u2013\u2014\s]*)\\\]\s*\]"
)
# Remove citation shell leftovers while preserving meaningful non-citation brackets.
# Examples: [], [\], [\, ], [60–], [–15\]
CITATION_FRAGMENT_BRACKET_RE = re.compile(
    r"\[\s*(?:(?=[^\]]*[\\,\-–\u2013\u2014])[0-9\\,\-–\u2013\u2014.\s]*"
    r"|[\\,\-–\u2013\u2014.\s]*)\s*\]"
)
NESTED_CITATION_FRAGMENT_BRACKET_RE = re.compile(
    r"\[\[\s*(?:(?=[^\]]*[\\,\-–\u2013\u2014])[0-9\\,\-–\u2013\u2014.\s]*"
    r"|[\\,\-–\u2013\u2014.\s]*)\s*\]\]"
)
NON_CITATION_LABEL_CONTEXT_RE = re.compile(
    r"(?:fig(?:ure)?|eq(?:uation)?|table|tab|scheme|sec(?:tion)?)\.?\s*$",
    re.IGNORECASE,
)

INLINE_MATH_RE = re.compile(
    r"(?<!\\)\$(?!\$).+?(?<!\\)\$|\\\(.+?\\\)",
    re.DOTALL,
)
UNIT_NEG_EXP_SPACING_RE = re.compile(r"([A-Za-zµμ°%])\s*([−-])\s+(\d)")
OPEN_PAREN_SPACE_RE = re.compile(r"\([ \t]+")
CLOSE_PAREN_SPACE_RE = re.compile(r"[ \t]+\)")
REPLACEMENT_TEMP_UNIT_RE = re.compile(r"�\s*([CFK])\b")
REPLACEMENT_PLUS_MINUS_RE = re.compile(r"(?<!\w)�\s*(\d)")
REPLACEMENT_NUMERIC_DEGREE_RE = re.compile(r"(?<=\d)\s*�(?=\s|[),.;:/]|$)")
FIG_LABEL = r"(?:fig(?:ure)?s?|tab(?:le)?s?|schemes?|eq(?:uation)?s?)"
FIG_LINK_RE = re.compile(
    rf"\[\s*\(?\s*{FIG_LABEL}\.?\s*[^\]]*?\]\([^)]+\)", re.IGNORECASE
)
# A single figure/table/eq reference with optional panel letter: "Fig. 5a", "Figs. 1-3(b)"
# Require either a dot (with optional space) or at least one space between label and
# number so compact tokens like "eq1" or "fig1" are not stripped.
_FIG_SINGLE_REF = (
    rf"{FIG_LABEL}(?:\.\s*|\s+)\d+[a-z]?(?:\s*[-–]\s*\d+[a-z]?)?(?:\s*\([a-z]\))?"
)
# A continuation ref after a comma may omit the label: "Figs. 1, 2" or "Fig. 1, Table 2"
_FIG_CONTINUATION = (
    rf"(?:{FIG_LABEL}\.?\s*)?\d+[a-z]?(?:\s*[-–]\s*\d+[a-z]?)?(?:\s*\([a-z]\))?"
)
FIG_PAREN_REF_RE = re.compile(
    rf"\(\s*{_FIG_SINGLE_REF}(?:\s*[,;]\s*{_FIG_CONTINUATION})*\s*\)",
    re.IGNORECASE,
)
# Require at least one space between label and number to avoid matching chemistry
# notation like "eq1" or compact abbreviations with no separator.
FIG_INLINE_REF_RE = re.compile(
    rf"\b{FIG_LABEL}\.?\s+\d+[a-z]?(?:\s*[-–]\s*\d+[a-z]?)?(?:\s*\([a-z]\))?",
    re.IGNORECASE,
)
ORPHANED_BRACKET_TOKEN_RE = re.compile(r"(?:(?<=\s)|^)[\[\]()]{1,3}(?=\s|$)")

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


def is_wiley_download_footer(line: str) -> bool:
    """Detect Wiley download/legal footer noise without matching normal prose."""
    normalized = re.sub(r"\s+", " ", line).strip().lower()
    if not normalized:
        return False
    # Conservative match: require multiple Wiley/legal markers on the same line.
    return (
        "downloaded from https://onlinelibrary.wiley.com/doi/" in normalized
        and "wiley online library" in normalized
        and (
            "terms-and-conditions" in normalized or "terms and conditions" in normalized
        )
        and "creative commons license" in normalized
    )


def normalize_heading(text: str) -> str:
    cleaned = LEADING_HTML_TAG_RE.sub("", text)
    cleaned = re.sub(r"[*_`]+", "", cleaned)
    # Drop decorative heading bullets used by some publishers (e.g., "■").
    cleaned = DECORATIVE_HEADING_PREFIX_RE.sub("", cleaned)
    # Drop common section numbering prefixes (e.g., "6.", "2.3", "IV)").
    cleaned = re.sub(
        r"^(?:\d+(?:\.\d+)*|[ivxlcdm]+)\s*[.)-]?\s+",
        "",
        cleaned,
        flags=re.IGNORECASE,
    )
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


def is_section_heading_candidate(line: str) -> bool:
    if HEADING_RE.match(line):
        return True
    if not is_headingish(line):
        return False
    if HEADING_BREAK_RE.search(line):
        return False
    if len(line.split()) > 8:
        return False
    return True


def classify_endmatter_heading(line: str) -> str | None:
    match = HEADING_RE.match(line)
    if match:
        heading = normalize_heading(match.group(1))
        if any(heading.startswith(k) for k in ENDMATTER_TRUNCATE_KEYWORDS):
            return "truncate"
        if any(heading.startswith(k) for k in ENDMATTER_SECTION_KEYWORDS):
            return "section"
        return None
    if not is_headingish(line):
        return None
    heading = normalize_heading(line)
    if any(heading == k or heading.startswith(k) for k in ENDMATTER_TRUNCATE_KEYWORDS):
        return "truncate"
    if any(heading == k or heading.startswith(k) for k in ENDMATTER_SECTION_KEYWORDS):
        return "section"
    return None


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


def strip_citation_math_escapes(text: str) -> str:
    def replace_link(match: re.Match[str]) -> str:
        label = match.group(1)
        url = match.group(2)
        label = label.replace("\\(", "(").replace("\\)", ")")
        return f"[{label}]({url})"

    return LINK_RE.sub(replace_link, text)


def normalize_citation_artifacts(text: str) -> str:
    """Normalize malformed citation-like tokens from OCR/layout extraction."""
    text = WORD_SUFFIX_CITATION_RE.sub(r"\1\2 [\3]", text)
    text = NUMERIC_BRACKET_TRAILING_DOT_RE.sub(r"[\1].", text)
    return text


def strip_numeric_citation_brackets(text: str) -> str:
    """
    Remove only numeric bracket citations while preserving non-numeric bracket text.
    """

    def strip_line_citations(line: str) -> str:
        def replace_citation(match: re.Match[str]) -> str:
            left_context = line[max(0, match.start() - 32) : match.start()]
            if NON_CITATION_LABEL_CONTEXT_RE.search(left_context):
                return match.group(0)
            return ""

        return CITATION_BRACKET_RE.sub(replace_citation, line)

    text = NESTED_ESCAPED_NUMERIC_CITATION_RE.sub(r"[\1]", text)
    text = ESCAPED_NUMERIC_CITATION_RE.sub(r"[\1]", text)
    for _ in range(4):
        prev = text
        lines = text.split("\n")
        text = "\n".join(strip_line_citations(line) for line in lines)
        text = NESTED_CITATION_FRAGMENT_BRACKET_RE.sub("", text)
        text = CITATION_FRAGMENT_BRACKET_RE.sub("", text)
        if text == prev:
            break
    # Cleanup punctuation artifacts caused by citation removal.
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r"\.\s*,", ".", text)
    text = re.sub(r"\.{2,}", ".", text)
    text = re.sub(r"\b(Fig|Eq|Ref)\.\s*\.", r"\1.", text, flags=re.IGNORECASE)
    text = re.sub(r",\s*,+", ", ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    text = re.sub(r"[ \t]+\n", "\n", text)
    return text


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


def normalize_spacing_artifacts(text: str) -> str:
    """Normalize extraction spacing artifacts useful for RAG token quality."""
    # Fix unit exponents like "m− 1" -> "m−1" and "K- 1" -> "K-1".
    text = UNIT_NEG_EXP_SPACING_RE.sub(r"\1\2\3", text)
    # Trim redundant spaces just inside parentheses.
    text = OPEN_PAREN_SPACE_RE.sub("(", text)
    text = CLOSE_PAREN_SPACE_RE.sub(")", text)
    return text


def normalize_replacement_char_artifacts(text: str) -> str:
    """Repair common decode artifacts represented by Unicode replacement char."""
    # Typical OCR/PDF decode artifacts in scientific texts.
    text = REPLACEMENT_PLUS_MINUS_RE.sub(r"±\1", text)
    text = REPLACEMENT_TEMP_UNIT_RE.sub(r"°\1", text)
    text = REPLACEMENT_NUMERIC_DEGREE_RE.sub("°", text)
    # Drop unresolved replacement glyphs (noise for RAG).
    text = text.replace("�", "")
    return text


def strip_figure_references(text: str) -> str:
    """Remove figure/table/scheme/equation references while keeping prose."""
    text = FIG_LINK_RE.sub("", text)
    text = FIG_PAREN_REF_RE.sub("", text)
    text = FIG_INLINE_REF_RE.sub("", text)
    # Remove standalone bracket tokens left by malformed figure links, e.g. ")".
    text = ORPHANED_BRACKET_TOKEN_RE.sub("", text)
    # Cleanup local punctuation/spacing artifacts caused by ref removal.
    text = re.sub(r"\[\s*\]", "", text)
    text = re.sub(r"\(\s*\)", "", text)
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    text = re.sub(r",\s*,+", ", ", text)
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text


def cleanup_text(
    text: str,
    drop_endmatter: bool = True,
    drop_tables: bool = True,
    drop_images: bool = True,
    drop_captions: bool = True,
    drop_math: bool = True,
    drop_image_descriptions: bool = True,
    drop_citations: bool = True,
    drop_superscripts: bool = True,
    drop_figure_refs: bool = True,
) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = strip_citation_math_escapes(text)
    text = normalize_citation_artifacts(text)
    # Remove dead internal page links emitted by Marker (e.g., "(#page-20-0)")
    # while preserving the visible link label text (e.g., "[123]").
    text = PAGE_LINK_RE.sub("", text)
    if drop_citations:
        text = strip_numeric_citation_brackets(text)
    if drop_superscripts:
        # Superscript tags are mostly extraction/layout artifacts in RAG corpora.
        text = SUP_TAG_RE.sub(r"\1", text)
    text = normalize_replacement_char_artifacts(text)
    if drop_figure_refs:
        text = strip_figure_references(text)
    text = remove_math_blocks(text)

    lines = text.split("\n")
    filtered: list[str] = []
    in_table = False
    skip_next_blank = False
    skip_endmatter_section = False
    i = 0

    while i < len(lines):
        raw_line = lines[i]
        line = EMPTY_SPAN_RE.sub("", raw_line)

        if skip_endmatter_section:
            if is_section_heading_candidate(line):
                skip_endmatter_section = False
                continue
            i += 1
            continue

        if skip_next_blank and line.strip() == "":
            i += 1
            continue
        if skip_next_blank and line.strip():
            skip_next_blank = False

        if drop_endmatter:
            endmatter_type = classify_endmatter_heading(line)
            if endmatter_type == "truncate":
                break
            if endmatter_type == "section":
                skip_endmatter_section = True
                i += 1
                continue

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
            IMAGE_MD_RE.search(line)
            or IMAGE_REF_RE.search(line)
            or HTML_IMG_RE.search(line)
        ):
            i += 1
            continue

        if drop_image_descriptions and IMAGE_DESC_RE.match(line):
            i += 1
            continue

        if SPAN_ONLY_RE.match(raw_line):
            i += 1
            continue

        if is_wiley_download_footer(line):
            i += 1
            continue

        if drop_captions:
            candidate = caption_candidate(line)
            prev_line_blank = not filtered or filtered[-1].strip() == ""
            next_line_blank = i + 1 < len(lines) and lines[i + 1].strip() == ""
            if (prev_line_blank or next_line_blank) and (
                CAPTION_RE.match(candidate)
                or CAPTION_TEXT_RE.match(candidate)
                or CAPTION_ONLY_RE.match(candidate)
                or CAPTION_CONTINUED_RE.match(candidate)
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
    output = normalize_spacing_artifacts(output)
    output = re.sub(r"[ \t]+$", "", output, flags=re.MULTILINE)
    output = re.sub(r"\n{3,}", "\n\n", output).strip() + "\n"
    return output


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Clean Marker Markdown output "
            "(drop tables, images, math, numeric citations, end-matter)."
        )
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--in-dir", type=Path, help="Directory containing .md files")
    group.add_argument("--in-file", type=Path, help="Single markdown file to clean")
    parser.add_argument("--out-dir", type=Path, help="Output directory (for --in-dir)")
    parser.add_argument("--out-file", type=Path, help="Output file (for --in-file)")
    parser.add_argument(
        "--ext", default=".md", help="File extension to process (default: .md)"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Show actions without writing files"
    )
    parser.add_argument(
        "--keep-tree",
        action="store_true",
        help="Preserve input subfolders instead of flattening into out-dir",
    )
    parser.add_argument(
        "--keep-endmatter", action="store_true", help="Do not truncate end-matter"
    )
    parser.add_argument("--keep-tables", action="store_true", help="Do not drop tables")
    parser.add_argument("--keep-images", action="store_true", help="Do not drop images")
    parser.add_argument(
        "--keep-captions", action="store_true", help="Do not drop captions"
    )
    parser.add_argument(
        "--keep-math", action="store_true", help="Do not drop math sentences"
    )
    parser.add_argument(
        "--keep-image-descriptions",
        action="store_true",
        help="Do not drop LLM image descriptions",
    )
    parser.add_argument(
        "--keep-citations",
        action="store_true",
        help="Do not drop numeric bracket citations like [12] or [5,6]",
    )
    parser.add_argument(
        "--keep-superscripts",
        action="store_true",
        help="Do not strip HTML superscript tags like <sup>...</sup>",
    )
    parser.add_argument(
        "--keep-figure-refs",
        action="store_true",
        help="Do not strip figure/table/scheme/equation references",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing output files (default: skip if output exists)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    drop_endmatter = not args.keep_endmatter
    drop_tables = not args.keep_tables
    drop_images = not args.keep_images
    drop_captions = not args.keep_captions
    drop_math = not args.keep_math
    drop_image_descriptions = not args.keep_image_descriptions
    drop_citations = not args.keep_citations
    drop_superscripts = not args.keep_superscripts
    drop_figure_refs = not args.keep_figure_refs

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
                drop_image_descriptions=drop_image_descriptions,
                drop_citations=drop_citations,
                drop_superscripts=drop_superscripts,
                drop_figure_refs=drop_figure_refs,
            )
            if args.dry_run:
                print(f"Would write: {out_path}")
            else:
                if out_path.exists() and not args.force:
                    print(f"Skipping existing output: {out_path}")
                    continue
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
        drop_image_descriptions=drop_image_descriptions,
        drop_citations=drop_citations,
        drop_superscripts=drop_superscripts,
        drop_figure_refs=drop_figure_refs,
    )
    if args.dry_run:
        print(f"Would write: {args.out_file}")
        return 0
    if args.out_file.exists() and not args.force:
        print(f"Skipping existing output: {args.out_file}")
        return 0
    args.out_file.parent.mkdir(parents=True, exist_ok=True)
    args.out_file.write_text(cleaned, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
