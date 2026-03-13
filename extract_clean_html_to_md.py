#!/usr/bin/env python3
"""
Extract clean article text from HTML into markdown.

Designed for scientific article HTML where headings and body text are present
in semantic tags, while figures/captions/references and navigation boilerplate
should be dropped.
"""

from __future__ import annotations

import argparse
import logging
import re
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

from clean_extraction_artifacts import clean_text

logger = logging.getLogger(__name__)


ENDMATTER_HEADING_RE = re.compile(
    r"^(references?|acknowledg(e)?ments?|conflicts? of interest|"
    r"author contributions?|author information|supporting information|"
    r"terms? (and|&) conditions|data availability)\b",
    flags=re.IGNORECASE,
)

SECTION_H2_ID_PATTERNS = (
    re.compile(r"^sect\d+$"),
    re.compile(r"^_i\d+$"),
)

HEADING_LEVEL_MAP = {"h2": "##", "h3": "###", "h4": "####"}
DEDUP_HEADING_PREFIXES = ("## ", "### ", "#### ")


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def _attr_text(value: object) -> str:
    """Normalize BeautifulSoup attribute values to plain text."""
    if isinstance(value, str):
        return value
    if isinstance(value, (list, tuple)):
        return " ".join(str(item) for item in value)
    return ""


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
        href = _attr_text(a_tag.get("href")).strip()
        title = _attr_text(a_tag.get("title")).lower()

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


def _is_descendant_or_self(node: Tag, container: Tag | None) -> bool:
    if container is None:
        return False
    return node is container or container in node.parents


def _first_h2_outside_container(
    soup: BeautifulSoup,
    container: Tag | None,
    id_pattern: re.Pattern[str] | None = None,
) -> Tag | None:
    headings: list[Tag] = soup.find_all("h2")
    for heading in headings:
        if id_pattern is not None and not id_pattern.match(_attr_text(heading.get("id"))):
            continue
        if not _is_descendant_or_self(heading, container):
            return heading
    return None


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

    abstract = soup.select_one("div.abstract") or soup.select_one("div.hlFld-Abstract")
    if abstract:
        abstract_paras: list[str] = []
        seen_abstract_paras: set[str] = set()
        for node in abstract.find_all(["p", "div"]):
            if node.name == "div":
                if "NLM_p" not in (node.get("class") or []):
                    continue
                # Skip NLM container divs when they wrap structured children to avoid
                # duplicates. But first emit any lead-in text (e.g. intro sentence
                # before a list or paragraph child), including text in inline tags.
                if node.find(["p", "ul", "li", "span"]):
                    block_tags = frozenset(("p", "ul", "ol", "li", "table", "blockquote", "div"))
                    abs_parts: list[str] = []
                    for _child in node.children:
                        if isinstance(_child, Tag) and _child.name in block_tags:
                            break
                        if isinstance(_child, NavigableString):
                            t = str(_child).strip()
                        elif isinstance(_child, Tag):
                            t = _child.get_text(" ", strip=True)
                        else:
                            continue
                        if t:
                            abs_parts.append(t)
                    direct_text = normalize(" ".join(abs_parts))
                    if direct_text and len(direct_text) >= 40 and direct_text not in seen_abstract_paras:
                        seen_abstract_paras.add(direct_text)
                        abstract_paras.append(direct_text)
                    continue
            text = normalize(node.get_text(" ", strip=True))
            if len(text) >= 40 and text not in seen_abstract_paras:
                seen_abstract_paras.add(text)
                abstract_paras.append(text)
        if abstract_paras:
            lines.append("## Abstract")
            lines.extend(abstract_paras)

    start = None
    for pattern in (*SECTION_H2_ID_PATTERNS, None):
        start = _first_h2_outside_container(soup, abstract, id_pattern=pattern)
        if start:
            break

    current = start
    while current:
        if abstract and _is_descendant_or_self(current, abstract):
            current = current.find_next()
            continue

        tag_name = current.name

        if tag_name in ("h2", "h3", "h4"):
            heading = normalize(current.get_text(" ", strip=True))
            if not heading:
                current = current.find_next()
                continue
            if not keep_endmatter and ENDMATTER_HEADING_RE.match(heading):
                break
            prefix = HEADING_LEVEL_MAP.get(tag_name, "###")
            lines.append(f"{prefix} {heading}")

        elif tag_name in ("p", "span", "li") or (
            tag_name == "div" and "NLM_p" in (current.get("class") or [])
        ):
            if (
                tag_name == "div"
                and "NLM_p" in (current.get("class") or [])
                and current.find(["p", "span", "li"])
            ):
                # Emit lead-in text before the first structural child (e.g. an intro
                # sentence before a <ul>). Collect text from NavigableString nodes
                # AND inline tags (strong, em, a, sup, …); stop at block-level tags.
                block_tags = frozenset(("p", "ul", "ol", "li", "table", "blockquote", "div"))
                parts: list[str] = []
                for _child in current.children:
                    if isinstance(_child, Tag) and _child.name in block_tags:
                        break
                    if isinstance(_child, NavigableString):
                        t = str(_child).strip()
                    elif isinstance(_child, Tag):
                        t = _child.get_text(" ", strip=True)
                    else:
                        continue
                    if t:
                        parts.append(t)
                direct_text = normalize(" ".join(parts))
                if direct_text:
                    lines.append(direct_text)
                # Prefer structured descendants over wrapper-level flattened text.
                current = current.find_next()
                continue
            # Skip tags whose text is already captured by a containing block element:
            # - anything inside a heading (handled separately as '## heading')
            # - p/li inside another p/li (outer block's get_text() already includes it)
            # - spans inside a p or li (prevents duplicating inline text)
            if current.find_parent(("h1", "h2", "h3", "h4", "h5", "h6", "p", "li")):
                current = current.find_next()
                continue
            # Skip spans that are children of a div.NLM_p — their text was already
            # emitted as lead-in text when the div was processed above.
            if tag_name == "span" and current.find_parent(
                lambda tag: isinstance(tag, Tag)
                and "NLM_p" in (tag.get("class") or [])
            ):
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

            text = normalize(text)
            if text:
                lines.append(text)

        current = current.find_next()

    deduped: list[str] = []
    for line in lines:
        if deduped and deduped[-1] == line:
            continue
        if deduped and deduped[-1].startswith(DEDUP_HEADING_PREFIXES):
            previous_heading_text = deduped[-1].split(" ", 1)[1]
            if line == previous_heading_text:
                continue
        deduped.append(line)

    markdown = "\n\n".join(deduped)
    return clean_text(markdown, drop_citations=True)


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
        help=(
            "Keep end-matter sections such as references, acknowledgements, "
            "author information, supporting information, and terms & conditions"
        ),
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite output files if they exist",
    )
    return parser.parse_args()


def main() -> int:
    logging.basicConfig(format="%(levelname)s: %(message)s", level=logging.INFO)
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
        logger.info("%s -> %s", args.in_file, out_file)
        return 0

    if args.in_dir:
        html_files = sorted(args.in_dir.rglob(args.glob))
        if not html_files:
            logger.info("no files matched '%s' in %s", args.glob, args.in_dir)
            return 0

        written = 0
        errors = 0
        for in_file in html_files:
            out_file = output_path_for_file(in_file, args.out_dir, base_dir=args.in_dir)
            try:
                process_one_file(
                    in_file=in_file,
                    out_file=out_file,
                    keep_endmatter=args.keep_endmatter,
                    force=args.force,
                )
                written += 1
            except Exception as exc:  # noqa: BLE001
                logger.error("%s: %s", in_file, exc)
                errors += 1
        logger.info("wrote %d file(s) to %s; errors %d", written, args.out_dir, errors)
        return 1 if errors else 0

    raise SystemExit("Provide either --in-file or --in-dir")


if __name__ == "__main__":
    raise SystemExit(main())
