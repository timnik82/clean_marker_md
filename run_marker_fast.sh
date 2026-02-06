#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <pdf_path>" >&2
  exit 2
fi

pdf_path="$1"
raw_out_dir="./out_raw"
clean_out_dir="./out_clean"

if [[ $# -ge 2 ]]; then
  echo "Ignoring custom output directories. Using: $raw_out_dir and $clean_out_dir"
fi

venv_dir="./.venv"
if [[ -x "${venv_dir}/bin/activate" ]]; then
  # shellcheck disable=SC1091
  . "${venv_dir}/bin/activate"
fi

mkdir -p "$raw_out_dir" "$clean_out_dir"

if [[ -f .env ]]; then
  set -a
  # shellcheck disable=SC1091
  . ./.env
  set +a
fi

export JOBLIB_TEMP_FOLDER="${JOBLIB_TEMP_FOLDER:-/tmp}"

config_json="./gemini_config.json"
config_arg=()
if [[ -f "$config_json" ]]; then
  config_arg=(--config_json "$config_json")
fi

marker_bin="marker_single"
marker_args=()
if [[ -x "${venv_dir}/bin/marker_single" ]]; then
  marker_bin="${venv_dir}/bin/python3"
  marker_args=("${venv_dir}/bin/marker_single")
fi

fast_processors=(
  "marker.processors.order.OrderProcessor"
  "marker.processors.block_relabel.BlockRelabelProcessor"
  "marker.processors.line_merge.LineMergeProcessor"
  "marker.processors.blockquote.BlockquoteProcessor"
  "marker.processors.code.CodeProcessor"
  "marker.processors.document_toc.DocumentTOCProcessor"
  "marker.processors.footnote.FootnoteProcessor"
  "marker.processors.ignoretext.IgnoreTextProcessor"
  "marker.processors.line_numbers.LineNumbersProcessor"
  "marker.processors.list.ListProcessor"
  "marker.processors.page_header.PageHeaderProcessor"
  "marker.processors.sectionheader.SectionHeaderProcessor"
  "marker.processors.llm.llm_form.LLMFormProcessor"
  "marker.processors.text.TextProcessor"
  "marker.processors.llm.llm_complex.LLMComplexRegionProcessor"
  "marker.processors.llm.llm_sectionheader.LLMSectionHeaderProcessor"
  "marker.processors.llm.llm_page_correction.LLMPageCorrectionProcessor"
  "marker.processors.reference.ReferenceProcessor"
  "marker.processors.blank_page.BlankPageProcessor"
  "marker.processors.debug.DebugProcessor"
)
fast_processors_csv="$(IFS=,; echo "${fast_processors[*]}")"

"$marker_bin" "${marker_args[@]}" "$pdf_path" \
  --output_format markdown \
  --output_dir "$raw_out_dir" \
  --disable_ocr \
  --disable_image_extraction \
  "${config_arg[@]}" \
  --use_llm --gemini_api_key "${GEMINI_API_KEY:-}" \
  --processors "$fast_processors_csv"

python_bin="python"
if [[ -x "${venv_dir}/bin/python" ]]; then
  python_bin="${venv_dir}/bin/python"
fi

echo "Cleaning markdown into: $clean_out_dir"
"$python_bin" clean_marker_md.py --in-dir "$raw_out_dir" --out-dir "$clean_out_dir"
echo "Done. Cleaned files are in: $clean_out_dir"
