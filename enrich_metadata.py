#!/usr/bin/env python3
"""Enrich abstracts with journal + citation metadata (OpenAlex + manual JCR IF).

Usage:
  python enrich_metadata.py \
    --papers-dir out_clean/papers \
    --input out_clean/abstracts_papers.md \
    --output out_clean/abstracts_papers_enriched.md \
    --cache-dir cache \
    --jcr-map jcr_manual_map.csv \
    --mailto you@example.com
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import time
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import datetime, timezone
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, cast
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError

OPENALEX_BASE = "https://api.openalex.org"

DOI_REGEX = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.IGNORECASE)
YEAR_REGEX = re.compile(r"\b(19|20)\d{2}\b")


@dataclass
class JcrMatch:
    if_value: str
    jcr_year: str
    journal_canonical: str
    match_method: str


@dataclass
class OpenAlexMetrics:
    journal_name: str | None
    cited_by_count: int | None
    h_index: float | None
    mean_citedness_2yr: float | None
    source_id: str | None


@dataclass
class PaperMetadata:
    paper_id: str
    doi: str | None
    openalex: OpenAlexMetrics | None
    jcr_match: JcrMatch | None
    journal_guess: str | None
    crossref_journal: str | None
    crossref_citations: int | None


def normalize_text(text: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", " ", text.lower())
    return re.sub(r"\s+", " ", cleaned).strip()


def normalize_issn(issn: str) -> str:
    return re.sub(r"[^0-9xX]", "", issn).upper()


def split_issn_field(value: str) -> list[str]:
    if not value:
        return []
    return [normalize_issn(v) for v in re.split(r"[;|,\s]+", value) if v.strip()]


def clean_doi(raw: str) -> str:
    cleaned = raw.strip()
    # Remove common trailing punctuation that may be attached to DOI
    cleaned = re.sub(r"[).,\];:>}\"']*$", "", cleaned)
    # Remove common leading punctuation
    cleaned = re.sub(r"^[({\[<\"']*", "", cleaned)
    return cleaned


def extract_doi(text: str) -> str | None:
    matches = [clean_doi(m) for m in DOI_REGEX.findall(text)]
    if not matches:
        return None
    preferred = [
        m
        for m in matches
        if "suppl_file" not in m.lower() and not m.lower().endswith(".pdf")
    ]
    return preferred[0] if preferred else matches[0]


def parse_filename_hint(stem: str) -> tuple[str | None, int | None]:
    year_match = YEAR_REGEX.search(stem)
    year = int(year_match.group(0)) if year_match else None
    parts = [p.strip() for p in stem.split(" - ")]
    title = None
    if year is not None:
        try:
            year_idx = parts.index(str(year))
            title = (
                " - ".join(parts[year_idx + 1 :]).strip()
                if year_idx + 1 < len(parts)
                else None
            )
        except ValueError:
            title = parts[-1] if len(parts) > 1 else None
    else:
        title = parts[-1] if len(parts) > 1 else stem
    return (title or None, year)


def extract_journal_and_title(text: str) -> tuple[str | None, str | None]:
    lines = text.splitlines()
    h1s: list[tuple[int, str]] = []
    for idx, line in enumerate(lines[:160]):
        if not line.startswith("# "):
            continue
        label = line[2:].strip()
        label_lower = label.lower()
        if label_lower in {"abstract"}:
            continue
        if "contents lists available at" in label_lower:
            continue
        h1s.append((idx, label))

    if len(h1s) >= 2:
        return (h1s[0][1], h1s[1][1])

    for _idx, line in enumerate(lines[:160]):
        if line.strip().lower().startswith("journal homepage") and h1s:
            return (h1s[0][1], None)

    return (None, None)


def fetch_json(url: str, retries: int = 3, backoff: float = 1.5) -> Any | None:
    for attempt in range(retries):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": "metadata-enricher/1.0",
                    "Accept": "application/json",
                },
            )
            with urlopen(req, timeout=30) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except (URLError, HTTPError, json.JSONDecodeError, ValueError) as exc:
            status = getattr(exc, "code", None)
            retry_after = (
                getattr(exc, "headers", {}).get("Retry-After")
                if hasattr(exc, "headers")
                else None
            )
            should_retry = status in {429, 500, 502, 503, 504} or status is None
            if not should_retry or attempt == retries - 1:
                return None
            sleep_for = (
                float(retry_after)
                if retry_after and str(retry_after).isdigit()
                else backoff * (2**attempt)
            )
            time.sleep(min(sleep_for, 30))
    return None


def get_crossref_work_by_doi(doi: str) -> dict | None:
    url = f"https://api.crossref.org/works/{quote(doi)}"
    data = fetch_json(url)
    if not data:
        return None
    return data.get("message") if isinstance(data, dict) else None


def search_crossref_work(query: str) -> list[dict[str, Any]]:
    url = (
        f"https://api.crossref.org/works?{urlencode({'query.title': query, 'rows': 5})}"
    )
    data = fetch_json(url)
    if not data:
        return []
    message = data.get("message") if isinstance(data, dict) else None
    if not message:
        return []
    return cast(list[dict[str, Any]], message.get("items", []))


def choose_best_crossref(
    candidates: list[dict], title: str | None, year: int | None
) -> dict | None:
    if not candidates:
        return None
    if not title:
        return candidates[0]

    normalized_title = normalize_text(title)
    best_score = 0.0
    best = None
    for cand in candidates:
        cand_title = " ".join(cand.get("title", [])).strip()
        cand_year = None
        issued = cand.get("issued") or {}
        date_parts = issued.get("date-parts") or []
        if date_parts and isinstance(date_parts, list) and date_parts[0]:
            cand_year = date_parts[0][0]
        ratio = SequenceMatcher(
            a=normalized_title, b=normalize_text(cand_title)
        ).ratio()
        if year and cand_year:
            if abs(int(cand_year) - int(year)) == 0:
                ratio += 0.1
            elif abs(int(cand_year) - int(year)) == 1:
                ratio += 0.05
        if ratio > best_score:
            best_score = ratio
            best = cand
    if best_score < 0.55:
        return None
    return best


def build_openalex_url(path: str, params: dict[str, str] | None = None) -> str:
    if params:
        return f"{OPENALEX_BASE}{path}?{urlencode(params)}"
    return f"{OPENALEX_BASE}{path}"


def get_openalex_work_by_doi(doi: str, mailto: str | None) -> dict | None:
    doi_url = f"https://doi.org/{doi}"
    path = f"/works/{quote(doi_url, safe='')}"
    params = {"mailto": mailto} if mailto else None
    url = build_openalex_url(path, params)
    return fetch_json(url)


def normalize_openalex_id(value: str | None) -> str | None:
    if not value:
        return None
    if value.startswith("https://openalex.org/"):
        return value.rsplit("/", 1)[-1]
    return value


def search_openalex_work(query: str, mailto: str | None) -> list[dict[str, Any]]:
    params = {"search": query, "per-page": "5"}
    if mailto:
        params["mailto"] = mailto
    url = build_openalex_url("/works", params)
    data = fetch_json(url)
    if data is None:
        return []
    return data.get("results", []) if isinstance(data, dict) else []


def choose_best_work(
    candidates: list[dict], title: str | None, year: int | None
) -> dict | None:
    if not candidates:
        return None
    if not title:
        return candidates[0]

    normalized_title = normalize_text(title)
    best_score = 0.0
    best = None
    for cand in candidates:
        cand_title = cand.get("title") or ""
        cand_year = cand.get("publication_year")
        ratio = SequenceMatcher(
            a=normalized_title, b=normalize_text(cand_title)
        ).ratio()
        if year and cand_year:
            if abs(int(cand_year) - int(year)) == 0:
                ratio += 0.1
            elif abs(int(cand_year) - int(year)) == 1:
                ratio += 0.05
        if ratio > best_score:
            best_score = ratio
            best = cand
    if best_score < 0.55:
        return None
    return best


def extract_openalex_metrics(work: dict, source: dict | None) -> OpenAlexMetrics:
    cited_by_count = work.get("cited_by_count") if isinstance(work, dict) else None
    journal_name = None
    source_id = None
    h_index = None
    mean_citedness_2yr = None

    if work:
        primary = work.get("primary_location") or {}
        host = work.get("host_venue") or {}
        source_obj = (
            primary.get("source") or host.get("source") or work.get("source") or {}
        )
        journal_name = source_obj.get("display_name") or host.get("display_name")
        source_id = normalize_openalex_id(
            source_obj.get("id") or work.get("host_venue_id")
        )

    if source and isinstance(source, dict):
        metrics = source.get("metrics") or {}
        h_index = metrics.get("h_index")
        mean_citedness_2yr = metrics.get("2yr_mean_citedness")

    return OpenAlexMetrics(
        journal_name=journal_name,
        cited_by_count=cited_by_count,
        h_index=h_index,
        mean_citedness_2yr=mean_citedness_2yr,
        source_id=source_id,
    )


def parse_abstracts(content: str) -> tuple[list[tuple[str, str]], str]:
    lines = content.splitlines()
    entries: list[tuple[str, str]] = []
    failure_block: list[str] = []

    current_title: str | None = None
    current_lines: list[str] = []
    in_failures = False

    for line in lines:
        if line.startswith("# Failures"):
            in_failures = True
            if current_title is not None:
                entries.append((current_title, "\n".join(current_lines).strip()))
            failure_block.append(line)
            continue

        if in_failures:
            failure_block.append(line)
            continue

        if line.startswith("## "):
            if current_title is not None:
                entries.append((current_title, "\n".join(current_lines).strip()))
            current_title = line[3:].strip()
            current_lines = []
            continue

        if current_title is not None:
            current_lines.append(line)

    if current_title is not None and not in_failures:
        entries.append((current_title, "\n".join(current_lines).strip()))

    return entries, "\n".join(failure_block).rstrip()


def load_cache(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))
    except (json.JSONDecodeError, OSError):
        return {}


def save_cache(path: Path, data: dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def load_jcr_map(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        return [row for row in reader if row.get("active", "1") != "0"]


def match_jcr(
    journal_title: str | None, issns: Iterable[str], rows: list[dict[str, str]]
) -> JcrMatch | None:
    if not rows:
        return None

    issn_set = {normalize_issn(i) for i in issns if i}
    issn_matches: list[dict[str, str]] = []
    for row in rows:
        candidates = set(
            split_issn_field(row.get("issn_print", ""))
            + split_issn_field(row.get("issn_electronic", ""))
            + split_issn_field(row.get("issn_other", ""))
        )
        if issn_set.intersection(candidates):
            issn_matches.append(row)

    if len(issn_matches) == 1:
        row = issn_matches[0]
        return JcrMatch(
            if_value=row.get("if_value", ""),
            jcr_year=row.get("jcr_year", ""),
            journal_canonical=row.get("journal_canonical", ""),
            match_method="ISSN",
        )
    if len(issn_matches) > 1:
        return None

    if not journal_title:
        return None

    normalized_title = normalize_text(journal_title)
    title_matches: list[dict[str, str]] = []
    for row in rows:
        canonical = normalize_text(row.get("journal_canonical", ""))
        variants = [
            normalize_text(v)
            for v in re.split(r"[;|]", row.get("title_variants", ""))
            if v.strip()
        ]
        if normalized_title == canonical or normalized_title in variants:
            title_matches.append(row)

    if len(title_matches) == 1:
        row = title_matches[0]
        return JcrMatch(
            if_value=row.get("if_value", ""),
            jcr_year=row.get("jcr_year", ""),
            journal_canonical=row.get("journal_canonical", ""),
            match_method="TITLE",
        )
    return None


def build_metadata_line(meta: PaperMetadata, fetched_date: str) -> str:
    journal = None
    if meta.openalex and meta.openalex.journal_name:
        journal = meta.openalex.journal_name
    elif meta.crossref_journal:
        journal = meta.crossref_journal
    else:
        journal = meta.journal_guess

    cited_by = meta.openalex.cited_by_count if meta.openalex else None
    citation_source = "OpenAlex"
    if cited_by is None and meta.crossref_citations is not None:
        cited_by = meta.crossref_citations
        citation_source = "Crossref"
    h_index = meta.openalex.h_index if meta.openalex else None
    mean_2yr = meta.openalex.mean_citedness_2yr if meta.openalex else None

    parts = ["**Metadata:**"]
    parts.append(f"Journal: **{journal or 'Unknown'}**")
    parts.append(
        f"Citations ({citation_source}): **{cited_by if cited_by is not None else 'n/a'}**"
    )

    metrics: list[str] = []
    if mean_2yr is not None:
        metrics.append(f"2yr_mean_citedness={mean_2yr}")
    if h_index is not None:
        metrics.append(f"h_index={h_index}")
    parts.append(f"Metrics (OpenAlex): **{', '.join(metrics) if metrics else 'n/a'}**")

    if meta.jcr_match and meta.jcr_match.if_value:
        parts.append(
            "JCR IF (manual, {year}, {method}): {value}".format(
                year=meta.jcr_match.jcr_year or "n/a",
                method=meta.jcr_match.match_method,
                value=meta.jcr_match.if_value,
            )
        )

    parts.append(f"Fetched: {fetched_date}")
    return " | ".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Enrich abstracts with metadata.")
    parser.add_argument(
        "--papers-dir",
        default="out_clean/papers",
        help="Directory with cleaned paper markdowns",
    )
    parser.add_argument(
        "--input",
        default="out_clean/abstracts_papers.md",
        help="Input abstracts markdown",
    )
    parser.add_argument(
        "--output",
        default="out_clean/abstracts_papers_enriched.md",
        help="Output enriched abstracts markdown",
    )
    parser.add_argument(
        "--cache-dir", default="cache", help="Cache directory for API responses"
    )
    parser.add_argument(
        "--jcr-map", default="jcr_manual_map.csv", help="Manual JCR mapping CSV"
    )
    parser.add_argument(
        "--mailto", default=None, help="Email for OpenAlex polite requests"
    )
    parser.add_argument(
        "--sleep", type=float, default=0.5, help="Sleep between API requests in seconds"
    )
    parser.add_argument(
        "--force-refresh",
        action="store_true",
        help="Ignore cached nulls and re-fetch metadata",
    )
    args = parser.parse_args()

    papers_dir = Path(args.papers_dir)
    input_path = Path(args.input)
    output_path = Path(args.output)
    cache_dir = Path(args.cache_dir)
    jcr_map_path = Path(args.jcr_map)

    if not papers_dir.exists():
        raise SystemExit(f"Papers directory not found: {papers_dir}")
    if not input_path.exists():
        raise SystemExit(f"Input abstracts not found: {input_path}")

    works_cache_path = cache_dir / "openalex_works.json"
    sources_cache_path = cache_dir / "openalex_sources.json"
    crossref_cache_path = cache_dir / "crossref_works.json"
    works_cache = load_cache(works_cache_path)
    sources_cache = load_cache(sources_cache_path)
    crossref_cache = load_cache(crossref_cache_path)

    jcr_rows = load_jcr_map(jcr_map_path)

    abstracts_text = input_path.read_text(encoding="utf-8")
    entries, failures_block = parse_abstracts(abstracts_text)

    fetched_date = datetime.now(timezone.utc).date().isoformat()

    enriched_entries: list[str] = ["# Abstracts", ""]

    for paper_id, abstract in entries:
        paper_path = papers_dir / f"{paper_id}.md"
        if not paper_path.exists():
            paper_text = ""
        else:
            paper_text = paper_path.read_text(encoding="utf-8", errors="ignore")

        journal_guess, title_from_text = extract_journal_and_title(paper_text)
        doi = extract_doi(paper_text)
        title_hint, year_hint = parse_filename_hint(paper_id)

        work_key = doi or normalize_text(paper_id)
        cached_entry = works_cache.get(work_key)
        work_data = cached_entry.get("data") if cached_entry else None
        skip_work_api = False
        if args.force_refresh:
            work_data = None
        elif (
            work_data is None
            and cached_entry
            and cached_entry.get("fetched_at") == fetched_date
        ):
            # Already tried and failed today, skip API call
            skip_work_api = True

        if work_data is None and not skip_work_api:
            if doi:
                work_data = get_openalex_work_by_doi(doi, args.mailto)
            else:
                search_query = title_from_text or title_hint or paper_id
                candidates = search_openalex_work(search_query, args.mailto)
                work_data = choose_best_work(
                    candidates, title_from_text or title_hint, year_hint
                )

            works_cache[work_key] = {"data": work_data, "fetched_at": fetched_date}
            time.sleep(args.sleep)

        source_data = None
        source_id = None
        if work_data:
            primary = work_data.get("primary_location") or {}
            host = work_data.get("host_venue") or {}
            source_obj = primary.get("source") or host.get("source") or {}
            source_id = normalize_openalex_id(
                source_obj.get("id") or work_data.get("host_venue_id")
            )

        if source_id:
            source_cache_entry = sources_cache.get(source_id)
            source_data = source_cache_entry.get("data") if source_cache_entry else None
            skip_source_api = False
            if args.force_refresh:
                source_data = None
            elif (
                source_data is None
                and source_cache_entry
                and source_cache_entry.get("fetched_at") == fetched_date
            ):
                # Already tried and failed today, skip API call
                skip_source_api = True
            if source_data is None and not skip_source_api:
                url = build_openalex_url(
                    f"/sources/{quote(str(source_id), safe='')}",
                    {"mailto": args.mailto} if args.mailto else None,
                )
                source_data = fetch_json(url)
                sources_cache[source_id] = {
                    "data": source_data,
                    "fetched_at": fetched_date,
                }
                time.sleep(args.sleep)

        metrics = extract_openalex_metrics(work_data or {}, source_data)

        crossref_work = None
        crossref_key = doi or normalize_text(paper_id)
        cached_crossref = crossref_cache.get(crossref_key)
        crossref_work = cached_crossref.get("data") if cached_crossref else None
        skip_crossref_api = False
        if args.force_refresh:
            crossref_work = None
        elif (
            crossref_work is None
            and cached_crossref
            and cached_crossref.get("fetched_at") == fetched_date
        ):
            # Already tried and failed today, skip API call
            skip_crossref_api = True
        if crossref_work is None and not skip_crossref_api:
            if doi:
                crossref_work = get_crossref_work_by_doi(doi)
            else:
                search_query = title_from_text or title_hint or paper_id
                candidates = search_crossref_work(search_query)
                crossref_work = choose_best_crossref(
                    candidates, title_from_text or title_hint, year_hint
                )
            crossref_cache[crossref_key] = {
                "data": crossref_work,
                "fetched_at": fetched_date,
            }
            time.sleep(args.sleep)

        crossref_journal = None
        crossref_citations = None
        crossref_issns: list[str] = []
        if crossref_work:
            titles = crossref_work.get("container-title") or []
            crossref_journal = titles[0] if titles else None
            crossref_citations = crossref_work.get("is-referenced-by-count")
            crossref_issns = crossref_work.get("ISSN") or []

        issns: list[str] = []
        if source_data and isinstance(source_data, dict):
            issns = source_data.get("issn") or []
            issn_l = source_data.get("issn_l")
            if issn_l:
                issns.append(issn_l)
        if crossref_issns:
            issns.extend(crossref_issns)

        jcr_match = match_jcr(metrics.journal_name, issns, jcr_rows)

        metadata = PaperMetadata(
            paper_id=paper_id,
            doi=doi,
            openalex=metrics if work_data else None,
            jcr_match=jcr_match,
            journal_guess=journal_guess,
            crossref_journal=crossref_journal,
            crossref_citations=crossref_citations,
        )

        enriched_entries.append(f"## {paper_id}")
        enriched_entries.append(build_metadata_line(metadata, fetched_date))
        if abstract:
            enriched_entries.append(abstract.strip())
        enriched_entries.append("")

    if failures_block:
        enriched_entries.append(failures_block)
        enriched_entries.append("")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        "\n".join(enriched_entries).rstrip() + "\n", encoding="utf-8"
    )

    save_cache(works_cache_path, works_cache)
    save_cache(sources_cache_path, sources_cache)
    save_cache(crossref_cache_path, crossref_cache)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
