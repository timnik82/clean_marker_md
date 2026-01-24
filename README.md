# Marker PDF -> Markdown (Text-Only) Workflow

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

```
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

## Notes

- The cleanup rules live in `clean_marker_md.py`.
- End-matter removal includes References, Bibliography, Acknowledgements,
  Competing/Conflict of Interest, Funding, etc.
- The cleaner strips empty `<span ...></span>` anchors and removes figure/table
  captions; if you need to preserve these, use `--keep-captions`.
