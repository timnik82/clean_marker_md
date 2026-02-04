# Repo Guide (for next sessions)

## Purpose

This repo provides a workflow to convert scientific PDFs to Markdown using
Marker (marker-pdf), then clean the output to remove tables, figures, math,
and end-matter (references, acknowledgements, conflict of interest, etc.).

## Key Files

- `README.md`: full setup + usage instructions
- `clean_marker_md.py`: cleanup logic (drops tables/images/math/end-matter/captions/empty spans)
- `run_marker_fast.sh`: fast conversion + cleanup wrapper
- `gemini_config.json`: Gemini model override
- `.env`: API keys (GEMINI_API_KEY / GOOGLE_API_KEY)

## Default Workflow

1) Convert a PDF (fast mode, no tables/math processors):

```bash
./run_marker_fast.sh "Some Paper.pdf"
```

2) Results:

- Raw output: `./out_raw/`
- Cleaned output: `./out_clean/`

## Notes

- Marker prefers `GOOGLE_API_KEY` if both keys are set.
- `clean_marker_md.py` flattens output into a single folder by default.
- If LLM calls are slow or error, try a different model in `gemini_config.json`
  or skip LLM for a quick run.
