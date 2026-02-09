# Marker PDF -> Markdown (Text-Only) Workflow

[![Lint and Quality Check](https://github.com/timnik82/clean_marker_md/actions/workflows/lint.yml/badge.svg)](https://github.com/timnik82/clean_marker_md/actions/workflows/lint.yml)

This repo contains a small workflow for converting PDFs to Markdown with Marker
and then cleaning the output to remove tables, figures, math, and end-matter.

## Prereqs

- Python 3.10+
- Virtualenv already created at `./.venv`
- Marker + CPU PyTorch installed in the venv

Activate the venv:

```bash
source /home/timnik/coding/Reviews/.venv/bin/activate
```

## Environment

Put your key(s) in `.env`:

```bash
GEMINI_API_KEY=your_key_here
GOOGLE_API_KEY=your_key_here
```

Marker uses `GOOGLE_API_KEY` if both are set.

## Model Override (Gemini)

`gemini_config.json` sets the Gemini model name:

```json
{
  "gemini_model_name": "gemini-3-flash-preview"
}
```

## Convert a PDF (raw output)

This keeps OCR off (digital PDFs), disables image extraction, and uses LLM mode.

```bash
export JOBLIB_TEMP_FOLDER=/tmp

marker_single "Some Paper.pdf" \
  --output_format markdown \
  --output_dir ./out_raw \
  --disable_image_extraction \
  --disable_ocr \
  --config_json ./gemini_config.json \
  --use_llm --gemini_api_key "$GEMINI_API_KEY"
```

Marker writes into a subfolder under `./out_raw`.

### Faster run (skip table + math processors)

This avoids LLM table handling and math processing since the cleanup step
removes tables and equations anyway.

```bash
export JOBLIB_TEMP_FOLDER=/tmp

marker_single "Some Paper.pdf" \
  --output_format markdown \
  --output_dir ./out_raw \
  --disable_image_extraction \
  --disable_ocr \
  --config_json ./gemini_config.json \
  --use_llm --gemini_api_key "$GEMINI_API_KEY" \
  --processors \
marker.processors.order.OrderProcessor,\
marker.processors.block_relabel.BlockRelabelProcessor,\
marker.processors.line_merge.LineMergeProcessor,\
marker.processors.blockquote.BlockquoteProcessor,\
marker.processors.code.CodeProcessor,\
marker.processors.document_toc.DocumentTOCProcessor,\
marker.processors.footnote.FootnoteProcessor,\
marker.processors.ignoretext.IgnoreTextProcessor,\
marker.processors.line_numbers.LineNumbersProcessor,\
marker.processors.list.ListProcessor,\
marker.processors.page_header.PageHeaderProcessor,\
marker.processors.sectionheader.SectionHeaderProcessor,\
marker.processors.llm.llm_form.LLMFormProcessor,\
marker.processors.text.TextProcessor,\
marker.processors.llm.llm_complex.LLMComplexRegionProcessor,\
marker.processors.llm.llm_sectionheader.LLMSectionHeaderProcessor,\
marker.processors.llm.llm_page_correction.LLMPageCorrectionProcessor,\
marker.processors.reference.ReferenceProcessor,\
marker.processors.blank_page.BlankPageProcessor,\
marker.processors.debug.DebugProcessor
```

You can use the helper script instead:

```bash
./run_marker_fast.sh "Some Paper.pdf"
```

It writes raw output to `./out_raw` and cleaned output to `./out_clean`.
Any extra output-directory arguments are ignored by design for a stable workflow.
By default, cleaning drops images/tables/math/captions, numeric citations, and end-matter.
If you need to keep numeric citations, run the cleaner separately with
`--keep-citations` after conversion.

## Clean the output (text-only)

This strips tables, figures, figure/table captions, math, end-matter, and
empty span anchors, and flattens all cleaned files into a single folder by default.

```bash
python clean_marker_md.py --in-dir ./out_raw --out-dir ./out_clean
```

To preserve the original folder tree:

```bash
python clean_marker_md.py --in-dir ./out_raw --out-dir ./out_clean --keep-tree
```

Additional options:

- `--keep-images`: Keep image references (don't remove them)
- `--keep-tables`: Keep tables (don't remove them)
- `--keep-math`: Keep mathematical sentences (don't remove them)
- `--keep-captions`: Keep figure/table captions (don't remove them)
- `--keep-citations`: Keep numeric bracket citations like `[12]` and `[5,6]`
- `--keep-endmatter`: Don't truncate end-matter sections
- `--force`: Overwrite existing output files
- `--dry-run`: Show what would be done without writing files

## Remove image placeholders (optional)

If you want to remove image placeholders and page anchors while keeping everything else:

```bash
python remove_image_placeholders.py --in-dir ./out_raw --out-dir ./out_clean
```

Or for a single file:

```bash
python remove_image_placeholders.py --in-file paper.md --out-file paper_clean.md
```

Additional options:

- `--keep-tree`: Preserve folder structure
- `--force`: Overwrite existing files
- `--stats`: Show statistics about removed placeholders
- `--dry-run`: Preview changes without writing files

## Remove journal footers (optional)

Remove journal page footers from academic papers:

```bash
python remove_journal_footers.py --in-file paper.md --out-file paper_clean.md
```

Or batch process a directory:

```bash
python remove_journal_footers.py --in-dir ./out_clean --out-dir ./out_no_footers
```

This removes patterns like:
- `*Biosensors* **2023**, *13*, 328 2 of 37`
- `*Nature* **2024**, *15*, 1234 5 of 20`
- Standalone page numbers: "X of Y"
- "FOR PEER REVIEW" text

Additional options:

- `--lenient`: Use more lenient pattern matching for footers
- `--force`: Overwrite existing files
- `--dry-run`: Preview changes without writing files
- `--stats`: Show statistics about removed footers

## Clean extraction artifacts (optional)

Clean common text artifacts left after HTML/figure/citation stripping:

```bash
python clean_extraction_artifacts.py --in-file paper.md --out-file paper_clean.md
```

Or batch process:

```bash
python clean_extraction_artifacts.py --in-dir ./out_clean --out-dir ./out_final
```

This removes:
- Empty brackets: `()`, `[]`, `{}`
- Broken figure references: "as shown in ."
- Extra whitespace and punctuation debris
- Multiple consecutive blank lines

Additional options:

- `--force`: Overwrite existing files
- `--dry-run`: Preview changes without writing files
- `--stats`: Show statistics about cleaned artifacts

## Extract clean HTML to Markdown (optional)

Extract clean article text from scientific HTML files:

```bash
python extract_clean_html_to_md.py --in-file article.html --out-file article.md
```

Or batch process:

```bash
python extract_clean_html_to_md.py --in-dir ./html_files --out-dir ./markdown_files
```

This script:
- Extracts headings and body text from semantic HTML tags
- Drops figures, captions, references, and navigation boilerplate
- Cleans up extraction artifacts automatically
- Stops at end-matter sections (References, Acknowledgements, etc.)

Additional options:

- `--force`: Overwrite existing files
- `--dry-run`: Preview changes without writing files
- `--keep-tree`: Preserve folder structure

## Reflow reading order (optional, two-column fixes)

For some two-column PDFs, Marker output can contain local reading-order
interruptions (for example, metadata/caption blocks inserted between two halves
of one sentence). This optional script applies conservative paragraph stitching.

Run it manually only for files that still show ordering artifacts:

```bash
python reflow_reading_order.py --in-file out_clean/paper.md --out-file out_clean/paper.md --force --stats
```

Or batch process:

```bash
python reflow_reading_order.py --in-dir ./out_clean --out-dir ./out_reflow --stats
```

Additional options:

- `--passes`: Maximum reflow passes (default: 2)
- `--keep-tree`: Preserve folder structure
- `--force`: Overwrite existing files
- `--dry-run`: Preview changes without writing files

## Extract abstracts from papers (optional)

Extract abstracts from cleaned markdown papers into a consolidated file:

```bash
python extract_abstracts.py \
  --input-dir out_clean/papers \
  --output out_clean/abstracts.md
```

This script:

- Extracts abstract sections from papers
- Filters out boilerplate text
- Validates abstract quality (length, sentence count)
- Consolidates all abstracts into one file

## Optimize tables for RAG (optional)

Transform markdown tables to improve embedding quality for RAG systems:

```bash
python optimize_tables_for_rag.py --in-dir ./out_clean --out-dir ./out_rag_optimized
```

Additional options:

- `--stats`: Print statistics about transformations
- `--dry-run`: Preview changes without writing files
- `--force`: Overwrite existing files

This script:

- Removes Table of Contents (ToC) tables
- Converts complex tables to structured text
- Cleans simple tables (removes HTML tags, empty columns)

## Notes

- The cleanup rules live in `clean_marker_md.py`.
- End-matter removal includes References, Bibliography, Acknowledgements,
  Competing/Conflict of Interest, Funding, etc.
- The cleaner strips empty `<span ...></span>` anchors and removes figure/table
  captions; if you need to preserve these, use `--keep-captions`.
- The cleaner removes `(#page-X-Y)` links and numeric bracket citations by
  default; use `--keep-citations` to retain numeric citations.
- Reading-order reflow is intentionally separate (`reflow_reading_order.py`) and
  should be run manually for affected two-column papers.

## Enrich abstracts with metadata (optional)

Generate an enriched abstracts index with journal metadata, citation counts,
and optional manual JCR Impact Factor values.

```bash
python enrich_metadata.py \
  --papers-dir out_clean/papers \
  --input out_clean/abstracts_papers.md \
  --output out_clean/abstracts_papers_enriched.md \
  --cache-dir cache \
  --jcr-map jcr_manual_map.csv \
  --mailto you@example.com
```

Populate `jcr_manual_map.csv` if you want to display JCR Impact Factor values.

## Testing Marker with Tables

Test Marker's table extraction with default processors:

```bash
./test_marker_tables.sh "Some Paper.pdf" ./test_output
```

This script:
- Runs Marker with default processors (includes table extraction)
- Checks for table markers in the output
- Useful for verifying table extraction capabilities

## Development

### Linting & Formatting

This project uses `ruff` for Python linting/formatting, `mypy` for static type checking, and `shellcheck` for shell scripts.

To run checks locally:

```bash
pip install ruff mypy
ruff check .
ruff format .
mypy .
```
