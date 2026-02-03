#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <pdf_path> [test_out_dir]" >&2
  exit 2
fi

pdf_path="$1"
test_out_dir="${2:-./test_output}"

venv_dir="./.venv"
if [[ -x "${venv_dir}/bin/activate" ]]; then
  # shellcheck disable=SC1091
  . "${venv_dir}/bin/activate"
fi

mkdir -p "$test_out_dir"

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
if command -v marker_single &> /dev/null; then
  marker_bin=$(which marker_single)
fi

echo "=== Testing Marker WITHOUT custom processors ==="
echo "Input PDF: $pdf_path"
echo "Output directory: $test_out_dir"
echo ""

# Run marker_single WITHOUT the --processors flag
# This will use Marker's default processor pipeline
"$marker_bin" "$pdf_path" \
  --output_format markdown \
  --output_dir "$test_out_dir" \
  "${config_arg[@]}" \
  --use_llm --gemini_api_key "${GEMINI_API_KEY:-}"

echo ""
echo "=== Conversion complete ==="
echo "Output saved to: $test_out_dir"
echo ""
echo "Checking for tables in output..."

# Find the generated markdown file
md_file=$(find "$test_out_dir" -name "*.md" -type f | head -n 1)

if [[ -n "$md_file" ]]; then
  echo "Generated markdown: $md_file"
  echo ""
  
  # Check for table markers (pipe characters on consecutive lines)
  table_count=$(grep -c '|' "$md_file" || true)
  
  if [[ $table_count -gt 0 ]]; then
    echo "✓ Found $table_count lines with table markers (|)"
    echo ""
    echo "First few table lines:"
    grep '|' "$md_file" | head -n 10
  else
    echo "✗ No table markers found in the output"
  fi
else
  echo "✗ No markdown file generated"
fi
