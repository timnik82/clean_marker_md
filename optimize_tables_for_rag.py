#!/usr/bin/env python3
"""
Optimize markdown tables for RAG (Retrieval-Augmented Generation) systems.

This script transforms markdown tables to improve embedding quality:
- Removes Table of Contents (ToC) tables
- Converts complex tables (with HTML tags) to structured text
- Cleans simple tables (removes HTML tags, empty columns)
- Provides statistics on transformations

Based on RAG best practices from vector database providers.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Literal, NamedTuple

# Regex patterns
HTML_TAG_RE = re.compile(r"</?(?:br|b|i|em|strong)(?:\s[^>]*)?>", re.IGNORECASE)
EMPTY_COLUMN_RE = re.compile(r"\|\s*\|")
TABLE_ROW_RE = re.compile(r"^\|.*\|.*\|")
TABLE_SEPARATOR_RE = re.compile(r"^\|[\s:-]+\|")


class TableInfo(NamedTuple):
    """Information about a detected table."""

    start_line: int
    end_line: int
    table_type: Literal["toc", "complex", "simple"]
    lines: list[str]


def remove_html_tags(text: str) -> str:
    """Remove HTML tags like <br>, <b>, <i> from text."""
    return HTML_TAG_RE.sub("", text)


def is_toc_table(lines: list[str]) -> bool:
    """
    Detect if a table is a Table of Contents.

    ToC tables typically have:
    - First column with section numbers (A.1, B.2, etc.)
    - Second column with dots for alignment
    - Last column with page numbers
    """
    if len(lines) < 3:  # Need header, separator, at least one row
        return False

    # Check for ToC patterns in rows
    toc_pattern_count = 0
    for line in lines[2:]:  # Skip header and separator
        # Look for patterns like "| A.1 |" or "| B.5 |" in first column
        if re.search(r"\|\s*[A-Z]\.\d+\s*\|", line):
            toc_pattern_count += 1
        # Look for dots used for alignment in content
        if "....." in line or "------" in line:
            toc_pattern_count += 1

    # If more than 30% of rows have ToC patterns, it's likely a ToC
    return toc_pattern_count > len(lines) * 0.3


def has_html_tags(lines: list[str]) -> bool:
    """Check if table contains HTML tags."""
    text = "\n".join(lines)
    return bool(HTML_TAG_RE.search(text))


def detect_empty_columns(lines: list[str]) -> set[int]:
    """
    Detect columns that are completely empty across all rows.
    Returns set of column indices to remove.
    """
    if len(lines) < 3:
        return set()

    # Parse table to get column values
    rows = []
    for line in lines[2:]:  # Skip header and separator
        cells = [
            cell.strip() for cell in line.split("|")[1:-1]
        ]  # Remove empty first/last
        rows.append(cells)

    if not rows:
        return set()

    # Find empty columns
    num_cols = len(rows[0])
    empty_cols = set()

    for col_idx in range(num_cols):
        is_empty = True
        for row in rows:
            if col_idx < len(row) and row[col_idx].strip():
                is_empty = False
                break
        if is_empty:
            empty_cols.add(col_idx)

    return empty_cols


def classify_table(lines: list[str]) -> Literal["toc", "complex", "simple"]:
    """Classify table type based on content."""
    if is_toc_table(lines):
        return "toc"
    elif has_html_tags(lines):
        return "complex"
    else:
        return "simple"


def convert_complex_table_to_text(lines: list[str], preceding_header: str = "") -> str:
    """
    Convert a complex table (with HTML tags) to structured text format.

    Args:
        lines: Table lines
        preceding_header: Header text that precedes the table

    Returns:
        Formatted text representation
    """
    if len(lines) < 3:
        return "\n".join(lines)

    # Parse header
    header_line = lines[0]
    headers = [remove_html_tags(cell.strip()) for cell in header_line.split("|")[1:-1]]

    # Remove empty headers at the end
    while headers and not headers[-1]:
        headers.pop()

    # Parse data rows
    rows = []
    for line in lines[2:]:
        cells = [remove_html_tags(cell.strip()) for cell in line.split("|")[1:-1]]
        # Trim to match header length
        cells = cells[: len(headers)]
        rows.append(cells)

    # Build structured text
    output = []

    # Add context header if available
    if preceding_header:
        output.append(f"\n**{preceding_header}**\n")

    # For comparison tables (detected by multiple data columns)
    if len(headers) >= 2 and rows:
        # Try to create grouped sections
        for col_idx in range(1, len(headers)):
            section_name = headers[col_idx]
            output.append(f"\n**{section_name}:**")

            for row in rows:
                if row and row[0]:  # First column is the attribute name
                    attr_name = row[0]
                    value = row[col_idx] if col_idx < len(row) else ""
                    if value:
                        output.append(f"- {attr_name}: {value}")
            output.append("")
    elif rows:
        # Fallback for non-comparison tables: list each row as a bullet point
        for row in rows:
            values = [cell for cell in row if cell]
            if values:
                output.append(f"- {' | '.join(values)}")

    return "\n".join(output)


def clean_simple_table(lines: list[str]) -> list[str]:
    """
    Clean a simple table by removing HTML tags and empty columns.
    """
    # Remove HTML tags from all lines
    cleaned_lines = [remove_html_tags(line) for line in lines]

    # Detect and remove empty columns
    empty_cols = detect_empty_columns(cleaned_lines)

    if not empty_cols:
        return cleaned_lines

    # Rebuild table without empty columns
    result = []
    for line in cleaned_lines:
        cells = line.split("|")
        # Keep first and last empty cells (table boundaries)
        filtered_cells = [cells[0]]
        for idx, cell in enumerate(cells[1:-1]):
            if idx not in empty_cols:
                filtered_cells.append(cell)
        filtered_cells.append(cells[-1])
        result.append("|".join(filtered_cells))

    return result


def detect_tables(content: str) -> list[TableInfo]:
    """
    Detect all tables in markdown content.

    Returns list of TableInfo objects.
    """
    lines = content.split("\n")
    tables = []
    in_table = False
    table_start = -1
    table_lines = []

    for idx, line in enumerate(lines):
        is_table_row = bool(TABLE_ROW_RE.match(line))

        if is_table_row:
            if not in_table:
                # Start of new table
                in_table = True
                table_start = idx
                table_lines = [line]
            else:
                # Continue existing table
                table_lines.append(line)
        else:
            if in_table:
                # End of table
                table_type = classify_table(table_lines)
                tables.append(
                    TableInfo(
                        start_line=table_start,
                        end_line=idx - 1,
                        table_type=table_type,
                        lines=table_lines.copy(),
                    )
                )
                in_table = False
                table_lines = []

    # Handle table at end of file
    if in_table:
        table_type = classify_table(table_lines)
        tables.append(
            TableInfo(
                start_line=table_start,
                end_line=len(lines) - 1,
                table_type=table_type,
                lines=table_lines.copy(),
            )
        )

    return tables


def process_markdown(content: str) -> tuple[str, dict]:
    """
    Process markdown content to optimize tables for RAG.

    Returns:
        Tuple of (processed_content, statistics)
    """
    lines = content.split("\n")
    tables = detect_tables(content)

    # Statistics
    stats = {
        "toc_removed": 0,
        "complex_converted": 0,
        "simple_cleaned": 0,
        "html_tags_removed": 0,
        "empty_cols_removed": 0,
    }

    # Process tables in reverse order to preserve line indices
    for table in reversed(tables):
        # Find preceding header for context
        preceding_header = ""
        lower_bound = max(0, table.start_line - 5)
        for i in range(table.start_line - 1, lower_bound - 1, -1):
            line = lines[i].strip()
            if line.startswith("###"):
                preceding_header = line.replace("###", "").strip()
                break
            elif line.startswith("##"):
                preceding_header = line.replace("##", "").strip()
                break

        if table.table_type == "toc":
            # Remove ToC table completely
            del lines[table.start_line : table.end_line + 1]
            stats["toc_removed"] += 1

        elif table.table_type == "complex":
            # Convert to structured text
            replacement = convert_complex_table_to_text(table.lines, preceding_header)
            lines[table.start_line : table.end_line + 1] = replacement.split("\n")
            stats["complex_converted"] += 1
            stats["html_tags_removed"] += len(
                HTML_TAG_RE.findall("\n".join(table.lines))
            )

        elif table.table_type == "simple":
            # Clean table
            original_html_count = len(HTML_TAG_RE.findall("\n".join(table.lines)))
            empty_cols = detect_empty_columns(table.lines)

            cleaned = clean_simple_table(table.lines)
            lines[table.start_line : table.end_line + 1] = cleaned

            stats["simple_cleaned"] += 1
            if original_html_count > 0:
                stats["html_tags_removed"] += original_html_count
            if empty_cols:
                stats["empty_cols_removed"] += len(empty_cols)

    # Join and clean up excessive blank lines
    output = "\n".join(lines)
    output = re.sub(r"\n{4,}", "\n\n\n", output)  # Max 3 newlines
    output = output.strip() + "\n"

    return output, stats


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Optimize markdown tables for RAG systems."
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--in-dir", type=Path, help="Directory containing .md files")
    group.add_argument("--in-file", type=Path, help="Single markdown file to process")

    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("out_rag_optimized"),
        help="Output directory (default: out_rag_optimized)",
    )
    parser.add_argument(
        "--stats", action="store_true", help="Print statistics about transformations"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing files",
    )
    parser.add_argument(
        "--force", action="store_true", help="Overwrite existing output files"
    )

    return parser.parse_args()


def main() -> int:
    """Main function."""
    args = parse_args()

    if args.in_file:
        # Process single file
        in_file = args.in_file
        if not in_file.exists():
            print(f"Input file not found: {in_file}", file=sys.stderr)
            return 2

        out_file = args.out_dir / in_file.name

        content = in_file.read_text(encoding="utf-8", errors="ignore")
        processed, stats = process_markdown(content)

        if args.dry_run:
            print(f"Would write: {out_file}")
            if args.stats:
                print(f"  ToC tables removed: {stats['toc_removed']}")
                print(f"  Complex tables converted: {stats['complex_converted']}")
                print(f"  Simple tables cleaned: {stats['simple_cleaned']}")
                print(f"  HTML tags removed: {stats['html_tags_removed']}")
                print(f"  Empty columns removed: {stats['empty_cols_removed']}")
            return 0

        if out_file.exists() and not args.force:
            print(f"Output file exists (use --force to overwrite): {out_file}")
            return 1

        out_file.parent.mkdir(parents=True, exist_ok=True)
        out_file.write_text(processed, encoding="utf-8")
        print(f"Processed: {in_file.name} -> {out_file}")

        if args.stats:
            print(f"  ToC tables removed: {stats['toc_removed']}")
            print(f"  Complex tables converted: {stats['complex_converted']}")
            print(f"  Simple tables cleaned: {stats['simple_cleaned']}")
            print(f"  HTML tags removed: {stats['html_tags_removed']}")
            print(f"  Empty columns removed: {stats['empty_cols_removed']}")

        return 0

    else:
        # Process directory
        in_dir = args.in_dir
        if not in_dir.exists():
            print(f"Input directory not found: {in_dir}", file=sys.stderr)
            return 2

        out_dir = args.out_dir

        total_stats = {
            "toc_removed": 0,
            "complex_converted": 0,
            "simple_cleaned": 0,
            "html_tags_removed": 0,
            "empty_cols_removed": 0,
            "files_processed": 0,
        }

        for md_file in sorted(in_dir.rglob("*.md")):
            rel_path = md_file.relative_to(in_dir)
            out_file = out_dir / rel_path

            content = md_file.read_text(encoding="utf-8", errors="ignore")
            processed, stats = process_markdown(content)

            if args.dry_run:
                print(f"Would write: {out_file}")
            else:
                if out_file.exists() and not args.force:
                    print(f"Skipping existing: {out_file}")
                    continue

                out_file.parent.mkdir(parents=True, exist_ok=True)
                out_file.write_text(processed, encoding="utf-8")
                print(f"Processed: {md_file.name} -> {out_file}")

            # Accumulate stats
            for key in stats:
                total_stats[key] += stats[key]
            total_stats["files_processed"] += 1

            if args.stats and not args.dry_run:
                print(
                    f"  Tables: {stats['toc_removed']} ToC, {stats['complex_converted']} complex, {stats['simple_cleaned']} simple"
                )

        if args.stats:
            print("\nTotal Summary:")
            print(f"  Files processed: {total_stats['files_processed']}")
            print(f"  ToC tables removed: {total_stats['toc_removed']}")
            print(f"  Complex tables converted: {total_stats['complex_converted']}")
            print(f"  Simple tables cleaned: {total_stats['simple_cleaned']}")
            print(f"  HTML tags removed: {total_stats['html_tags_removed']}")
            print(f"  Empty columns removed: {total_stats['empty_cols_removed']}")

        return 0


if __name__ == "__main__":
    sys.exit(main())
