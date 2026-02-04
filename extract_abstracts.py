#!/usr/bin/env python3
"""Extract abstracts from cleaned markdown papers into one consolidated markdown file.

Usage:
  python extract_abstracts.py \
    --input-dir out_clean/papers \
    --output out_clean/abstracts.md
"""

from __future__ import annotations

import argparse
import re
from collections.abc import Iterable
from pathlib import Path

ABSTRACT_MIN_CHARS = 200
ABSTRACT_MAX_CHARS = 2200
ABSTRACT_MAX_SENTENCES = 12

BOILERPLATE_TOKENS = [
    "open access",
    "downloaded on",
    "downloaded from",
    "terms and conditions",
    "creative commons",
    "licensee",
    "all rights reserved",
    "©",
    "wileyonlinelibrary",
    "view article online",
    "published on",
    "doi:",
]

SECTION_STOP_HEADINGS = [
    "introduction",
    "materials and methods",
    "material and methods",
    "methods",
    "experimental",
    "experimental section",
    "results",
    "results and discussion",
    "discussion",
    "conclusion",
    "conclusions",
]

KEYWORDS_MARKER = re.compile(r"^\s*[*_]*\s*key\s*words\b", re.IGNORECASE)
HIGHLIGHTS_MARKER = re.compile(r"^\s*[*_]*\s*highlights\b", re.IGNORECASE)
METADATA_PREFIX_MARKER = re.compile(
    r"^\s*(?:<[^>]+>\s*)*[*_\s]*((received|accepted)\b\s*:|citation\b|academic editor\b|publisher's note\b|copyright\b|declaration of competing\b|conflict of interest\b)",
    re.IGNORECASE,
)
METADATA_INLINE_MARKER = re.compile(r"(corresponding author|e-?mail address(?:es)?|e-?mail)\b", re.IGNORECASE)


def is_metadata_line(line: str) -> bool:
    normalized = line.strip()
    if not normalized:
        return False
    if "@" in normalized and "http" not in normalized.lower():
        return True
    if METADATA_INLINE_MARKER.search(normalized):
        return True
    return METADATA_PREFIX_MARKER.match(normalized) is not None
INLINE_ABSTRACT = re.compile(
    r"^\s*(\*\*|__)?\s*abstract\s*(\*\*|__)?\s*[:\-–—]\s*(.+)$",
    re.IGNORECASE,
)


def normalize_label(text: str) -> str:
    cleaned = text.strip().strip("#").strip()
    cleaned = re.sub(r"[*_`]+", "", cleaned)
    cleaned = cleaned.strip().strip(".:;—–- ")
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned.lower()


def is_heading(line: str) -> str | None:
    match = re.match(r"^\s{0,3}#{1,6}\s+(.*?)\s*$", line)
    if not match:
        return None
    return match.group(1)


def is_section_boundary(line: str) -> bool:
    heading_text = is_heading(line)
    if heading_text is not None:
        label = normalize_label(heading_text)
        if label in SECTION_STOP_HEADINGS:
            return True
        # numbered headings like "1. Introduction" inside markdown heading
        if re.match(r"^\d+(\.\d+)*\s+", label):
            stripped = re.sub(r"^\d+(\.\d+)*\s+", "", label)
            if stripped in SECTION_STOP_HEADINGS:
                return True
        return False

    plain = normalize_label(line)
    if re.match(r"^\d+(\.\d+)*\s+", plain):
        stripped = re.sub(r"^\d+(\.\d+)*\s+", "", plain)
        return stripped in SECTION_STOP_HEADINGS

    if plain in SECTION_STOP_HEADINGS:
        return True

    return False


def is_graphical_abstract(label: str) -> bool:
    return "graphical abstract" in label


def contains_boilerplate(text: str) -> bool:
    lower = text.lower()
    return any(token in lower for token in BOILERPLATE_TOKENS if token != "©") or "©" in text


def truncate_at_boilerplate(text: str) -> str:
    lower = text.lower()
    cutoff: int | None = None
    for token in BOILERPLATE_TOKENS:
        idx = lower.find(token)
        if idx == -1:
            idx = text.find(token)
        if idx != -1:
            if cutoff is None or idx < cutoff:
                cutoff = idx
    if cutoff is None:
        return text
    return text[:cutoff].rstrip()


def sentence_count(text: str) -> int:
    return len([s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s])


def limit_sentences(text: str) -> str:
    sentences = [s for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s]
    limited: list[str] = []
    total_chars = 0
    for sentence in sentences:
        if len(limited) >= ABSTRACT_MAX_SENTENCES:
            break
        if total_chars + len(sentence) > ABSTRACT_MAX_CHARS:
            break
        limited.append(sentence)
        total_chars += len(sentence) + 1
    return " ".join(limited).strip()


def extract_explicit_abstract(lines: list[str]) -> str | None:
    in_abstract = False
    collected: list[str] = []

    for idx, line in enumerate(lines):
        heading_text = is_heading(line)
        if not in_abstract and heading_text is not None:
            label = normalize_label(heading_text)
            if is_graphical_abstract(label):
                continue
            if label == "abstract":
                in_abstract = True
                continue

        if not in_abstract:
            inline = INLINE_ABSTRACT.match(line)
            if inline:
                # Only check the label part for graphical abstract
                label = normalize_label(inline.group(0).split(':', 1)[0])
                if not is_graphical_abstract(label):
                    in_abstract = True
                    collected.append(inline.group(3).rstrip())
                continue

        if in_abstract:
            if is_heading(line):
                break
            if KEYWORDS_MARKER.match(line) or HIGHLIGHTS_MARKER.match(line):
                break
            if is_metadata_line(line):
                break
            if is_section_boundary(line):
                break
            collected.append(line.rstrip())

    if not collected:
        return None

    return "\n".join(collected).strip()


def paragraph_blocks(lines: Iterable[str]) -> list[str]:
    blocks: list[str] = []
    buffer: list[str] = []
    for line in lines:
        if is_metadata_line(line):
            if buffer:
                blocks.append(" ".join(buffer).strip())
                buffer = []
            continue
        if KEYWORDS_MARKER.match(line) or HIGHLIGHTS_MARKER.match(line):
            if buffer:
                blocks.append(" ".join(buffer).strip())
                buffer = []
            continue
        if line.strip() == "":
            if buffer:
                blocks.append(" ".join(buffer).strip())
                buffer = []
            continue
        buffer.append(line.strip())
    if buffer:
        blocks.append(" ".join(buffer).strip())
    return blocks


def extract_fallback_abstract(lines: list[str]) -> str | None:
    cutoff = len(lines)
    for idx, line in enumerate(lines):
        if is_metadata_line(line):
            cutoff = idx
            break
        if is_section_boundary(line):
            cutoff = idx
            break
        if is_heading(line):
            heading = normalize_label(is_heading(line) or "")
            if heading in SECTION_STOP_HEADINGS:
                cutoff = idx
                break

    blocks = paragraph_blocks(lines[:cutoff])
    for block in blocks:
        if len(block) < ABSTRACT_MIN_CHARS:
            continue
        if sentence_count(block) < 2:
            continue
        trimmed = truncate_at_boilerplate(block)
        if len(trimmed) < ABSTRACT_MIN_CHARS:
            continue
        trimmed = limit_sentences(trimmed)
        if len(trimmed) < ABSTRACT_MIN_CHARS:
            continue
        return trimmed

    return None


def extract_abstract(text: str) -> str | None:
    lines = text.splitlines()
    explicit = extract_explicit_abstract(lines)
    if explicit:
        explicit = truncate_at_boilerplate(explicit)
        if explicit:
            explicit = limit_sentences(explicit)
            if len(explicit) >= ABSTRACT_MIN_CHARS:
                return explicit
    return extract_fallback_abstract(lines)


def build_output(entries: list[tuple[str, str]], failures: list[str]) -> str:
    parts: list[str] = ["# Abstracts", ""]
    for filename, abstract in entries:
        parts.append(f"## {filename}")
        parts.append(abstract.strip())
        parts.append("")

    parts.append("# Failures")
    if failures:
        for name in failures:
            parts.append(f"- {name}")
    else:
        parts.append("- None")

    parts.append("")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Extract abstracts from markdown papers.")
    parser.add_argument("--input-dir", default="out_clean/papers", help="Directory with markdown papers")
    parser.add_argument("--output", default="out_clean/abstracts.md", help="Output markdown file")
    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_path = Path(args.output)

    if not input_dir.exists():
        raise SystemExit(f"Input directory not found: {input_dir}")

    entries: list[tuple[str, str]] = []
    failures: list[str] = []

    for path in sorted(input_dir.glob("*.md"), key=lambda p: p.name.lower()):
        text = path.read_text(encoding="utf-8", errors="ignore")
        abstract = extract_abstract(text)
        if abstract and abstract.strip():
            entries.append((path.stem, abstract.strip()))
        else:
            failures.append(path.stem)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(build_output(entries, failures), encoding="utf-8")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
