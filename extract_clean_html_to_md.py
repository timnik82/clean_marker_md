#!/usr/bin/env python3
"""
Extract clean article text from HTML into markdown.

Designed for scientific article HTML where headings and body text are present
in semantic tags, while figures/captions/references and navigation boilerplate
should be dropped.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from bs4 import BeautifulSoup

from clean_extraction_artifacts import clean_text


ENDMATTER_HEADING_RE = re.compile(
    r"^(references?|acknowledg(e)?ments?|conflicts? of interest|"
    r"author contributions?|data availability)\b",
    flags=re.IGNORECASE,
)


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _drop_global_noise(soup: BeautifulSoup) -> None:
    selectors = [
        "script",
        "style",
        "noscript",
        "svg",
        "iframe",
        "form",
        "header",
        "footer",
        "nav",
        "table",
        "figure",
        ".image_table",
        ".image_title",
        ".graphic_title",
        ".sup_ref",
        ".orcid",
        ".article_info",
    ]
    for selector in selectors:
        for node in soup.select(selector):
            node.decompose()


def _drop_navigation_links(soup: BeautifulSoup) -> None:
    for a_tag in soup.find_all("a"):
        href = (a_tag.get("href") or "").strip()
        title = (a_tag.get("title") or "").lower()

        if href.startswith("#") and any(
            href.startswith(prefix) for prefix in ("#cit", "#img", "#tbl", "#fn")
        ):
            a_tag.decompose()
            continue

        if any(
            token in title
            for token in (
                "navigate to reference",
                "navigate to references",
                "navigate to figure",
                "navigate to table",
                "navigate to footnote",
            )
        ):
            a_tag.decompose()


def extract_html_to_markdown(html: str, keep_endmatter: bool = False) -> str:
    soup = BeautifulSoup(html, "html.parser")

    _drop_global_noise(soup)
    _drop_navigation_links(soup)

    lines: list[str] = []

    title_tag = soup.select_one("h1 .title_heading") or soup.find("h1")
    if title_tag:
        title = normalize(title_tag.get_text(" ", strip=True))
        if title:
            lines.append(f"# {title}")

    abstract = soup.select_one("div.abstract")
    if abstract:
        abstract_paras = []
        for p_tag in abstract.find_all("p"):
            text = normalize(p_tag.get_text(" ", strip=True))
            if len(text) >= 40:
                abstract_paras.append(text)
        if abstract_paras:
            lines.append("## Abstract")
            lines.extend(abstract_paras)

    start = soup.find("h2", id=re.compile(r"^sect\d+$")) or soup.find("h2")
    current = start
    while current:
        tag_name = current.name

        if tag_name in ("h2", "h3", "h4"):
            heading = normalize(current.get_text(" ", strip=True))
            if not heading:
                current = current.find_next()
                continue
            if not keep_endmatter and ENDMATTER_HEADING_RE.match(heading):
                break
            prefix = "##" if tag_name == "h2" else "###"
            lines.append(f"{prefix} {heading}")

        elif tag_name in ("p", "span", "li"):
            if current.find_parent(("h1", "h2", "h3", "h4", "h5", "h6")):
                current = current.find_next()
                continue
            if abstract and current.find_parent("div", class_="abstract"):
                current = current.find_next()
                continue

            text = normalize(current.get_text(" ", strip=True))
            if len(text) < 45:
                current = current.find_next()
                continue
            if text.lower().startswith("open access article"):
                current = current.find_next()
                continue
            if text.lower().startswith("this open access article is licensed"):
                current = current.find_next()
                continue

            # Drop in-text numeric citation brackets.
            text = re.sub(
                r"\[(?:\d+|\d+\s*[–-]\s*\d+)(?:\s*,\s*(?:\d+|\d+\s*[–-]\s*\d+))*\]",
                "",
                text,
            )
            text = normalize(text)
            if text:
                lines.append(text)

        current = current.find_next()

    deduped: list[str] = []
    for line in lines:
        if deduped and deduped[-1] == line:
            continue
        if deduped and deduped[-1].startswith(("## ", "### ")):
            previous_heading_text = deduped[-1].split(" ", 1)[1]
            if line == previous_heading_text:
                continue
        deduped.append(line)

    markdown = "\n\n".join(deduped)
    return clean_text(markdown)


def output_path_for_file(
    in_file: Path, out_dir: Path, base_dir: Path | None = None
) -> Path:
    """Build output path, preserving relative directory structure when *base_dir* is given."""
    if base_dir is not None:
        rel = in_file.relative_to(base_dir)
        return out_dir / rel.with_suffix(".md")
    return out_dir / f"{in_file.stem}.md"


def process_one_file(
    in_file: Path,
    out_file: Path,
    keep_endmatter: bool = False,
    force: bool = False,
) -> bool:
    if not in_file.exists():
        raise FileNotFoundError(f"Input file not found: {in_file}")
    if out_file.exists() and not force:
        raise FileExistsError(f"Output file exists (use --force): {out_file}")

    html = in_file.read_text(encoding="utf-8", errors="ignore")
    cleaned_md = extract_html_to_markdown(html, keep_endmatter=keep_endmatter)

    out_file.parent.mkdir(parents=True, exist_ok=True)
    out_file.write_text(cleaned_md, encoding="utf-8")
    return True


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract clean markdown from scientific HTML files."
    )
    parser.add_argument("--in-file", type=Path, help="Input HTML file")
    parser.add_argument("--out-file", type=Path, help="Output markdown file")
    parser.add_argument("--in-dir", type=Path, help="Input directory with HTML files")
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=Path("out_clean"),
        help="Output directory for markdown (default: out_clean)",
    )
    parser.add_argument(
        "--glob",
        type=str,
        default="*.html",
        help="File glob for --in-dir mode (default: *.html)",
    )
    parser.add_argument(
        "--keep-endmatter",
        action="store_true",
        help="Keep references/acknowledgements/conflicts sections",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output files if they exist",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.in_file:
        out_file = args.out_file
        if out_file is None:
            out_file = output_path_for_file(args.in_file, args.out_dir)
        process_one_file(
            in_file=args.in_file,
            out_file=out_file,
            keep_endmatter=args.keep_endmatter,
            force=args.force,
        )
        print(f"[ok] {args.in_file} -> {out_file}")
        return 0

    if args.in_dir:
        html_files = sorted(args.in_dir.rglob(args.glob))
        if not html_files:
            print(f"[info] no files matched '{args.glob}' in {args.in_dir}")
            return 0

        written = 0
        for in_file in html_files:
            out_file = output_path_for_file(in_file, args.out_dir, base_dir=args.in_dir)
            process_one_file(
                in_file=in_file,
                out_file=out_file,
                keep_endmatter=args.keep_endmatter,
                force=args.force,
            )
            written += 1
        print(f"[ok] wrote {written} file(s) to {args.out_dir}")
        return 0

    raise SystemExit("Provide either --in-file or --in-dir")


if __name__ == "__main__":
    raise SystemExit(main())
