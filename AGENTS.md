# Repo Guide (for next sessions)

## Purpose

This repo provides a workflow to convert scientific PDFs to Markdown using
Marker (marker-pdf), then clean the output to remove tables, figures, math,
and end-matter (references, acknowledgements, conflict of interest, etc.).

## Key Files

### Core Scripts

- `README.md`: full setup + usage instructions
- `clean_marker_md.py`: cleanup logic (drops tables/images/math/end-matter/captions/empty spans)
- `run_marker_fast.sh`: fast conversion + cleanup wrapper
- `run_python.sh`: wrapper script for running Python with venv activated

### Processing Scripts

- `remove_image_placeholders.py`: removes image placeholders and page anchors from markdown
- `extract_abstracts.py`: extracts abstracts from cleaned papers into consolidated file
- `optimize_tables_for_rag.py`: optimizes tables for RAG embedding (removes ToC, converts complex tables)
- `reflow_reading_order.py`: optional conservative reflow for local two-column reading-order interruptions
- `enrich_metadata.py`: enriches abstracts with journal metadata and citation counts via OpenAlex

### Configuration

- `gemini_config.json`: Gemini model override
- `.env`: API keys (GEMINI_API_KEY / GOOGLE_API_KEY)
- `jcr_manual_map.csv`: manual JCR Impact Factor mappings

## Default Workflow

### Basic PDF to Clean Markdown

1) Convert a PDF (fast mode, no tables/math processors):

```bash
./run_marker_fast.sh "Some Paper.pdf"
```

2) Results:

- Raw output: `./out_raw/`
- Cleaned output: `./out_clean/`

### Advanced Workflows

**Extract abstracts from papers:**

```bash
python extract_abstracts.py --input-dir out_clean/papers --output out_clean/abstracts.md
```

**Optimize tables for RAG:**

```bash
python optimize_tables_for_rag.py --in-dir ./out_clean --out-dir ./out_rag_optimized --stats
```

**Reflow reading order (manual, optional for problematic two-column files):**

```bash
python reflow_reading_order.py --in-file out_clean/paper.md --out-file out_clean/paper.md --force --stats
```

**Enrich abstracts with metadata:**

```bash
python enrich_metadata.py \
  --papers-dir out_clean/papers \
  --input out_clean/abstracts.md \
  --output out_clean/abstracts_enriched.md \
  --cache-dir cache \
  --jcr-map jcr_manual_map.csv \
  --mailto you@example.com
```

## Notes

### General

- Marker prefers `GOOGLE_API_KEY` if both keys are set.
- `clean_marker_md.py` flattens output into a single folder by default.
- If LLM calls are slow or error, try a different model in `gemini_config.json`
  or skip LLM for a quick run.

### Using Scripts

- Use `./run_python.sh` to run any Python scripts in this repo (automatically activates venv):
  ```bash
  ./run_python.sh remove_image_placeholders.py --in-file <input> --out-dir <output>
  ./run_python.sh extract_abstracts.py --input-dir <dir> --output <file>
  ```

### Key Options

**clean_marker_md.py:**

- `--keep-images`: Keep image references
- `--keep-tables`: Keep tables
- `--keep-math`: Keep math sentences
- `--keep-captions`: Keep figure/table captions
- `--keep-citations`: Keep numeric bracket citations (e.g., `[12]`)
- `--force`: Overwrite existing files
- `--dry-run`: Preview without writing

**remove_image_placeholders.py:**

- Removes only image placeholders and page anchors
- Preserves everything else (tables, text, links, etc.)

**extract_abstracts.py:**

- Filters abstracts by quality (length, sentence count)
- Removes boilerplate text
- Consolidates into single file

**optimize_tables_for_rag.py:**

- Removes ToC tables
- Converts complex tables to text
- Cleans HTML tags from tables

**reflow_reading_order.py:**

- Conservative paragraph stitching around metadata/caption interruption blocks
- Intended as manual post-step only for files with obvious reading-order artifacts
