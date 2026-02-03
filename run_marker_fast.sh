#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <pdf_path> [raw_out_dir] [clean_out_dir]" >&2
  exit 2
fi

pdf_path="$1"
raw_out_dir="${2:-./out_raw}"
clean_out_dir="${3:-./out_clean}"

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
if [[ -x "${venv_dir}/bin/marker_single" ]]; then
  marker_bin="${venv_dir}/bin/marker_single"
fi

"$marker_bin" "$pdf_path" \
  --output_format markdown \
  --output_dir "$raw_out_dir" \
  --disable_ocr \
  "${config_arg[@]}" \
  --use_llm --gemini_api_key "${GEMINI_API_KEY:-}"

python_bin="python"
if [[ -x "${venv_dir}/bin/python" ]]; then
  python_bin="${venv_dir}/bin/python"
fi

echo "Cleaning markdown into: $clean_out_dir"
"$python_bin" clean_marker_md.py --in-dir "$raw_out_dir" --out-dir "$clean_out_dir" --keep-images
echo "Done. Cleaned files are in: $clean_out_dir"
