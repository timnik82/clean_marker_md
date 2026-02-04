# Image Placeholder Removal Script

## Overview

`remove_image_placeholders.py` is a utility script that removes standalone image placeholders from Marker-generated markdown files while preserving all other content including tables, text, links, and formatting.

## What It Does

- ✅ **Removes**: Standalone image references like `![](_page_0_Picture_0.jpeg)`
- ✅ **Preserves**:
  - Tables
  - Text content
  - Links (both inline and reference-style)
  - Headings and formatting
  - Figure captions (text references to figures)
  - Code blocks
  - Lists

## Usage

### Single File Processing

```bash
python3 remove_image_placeholders.py \
  --in-file path/to/input.md \
  --out-file path/to/output.md \
  --stats
```

### Batch Processing (Directory)

```bash
python3 remove_image_placeholders.py \
  --in-dir path/to/input_dir \
  --out-dir path/to/output_dir \
  --stats
```

## Options

| Option | Description |
|--------|-------------|
| `--in-file` | Single markdown file to process |
| `--in-dir` | Directory containing .md files to process |
| `--out-file` | Output file (required with --in-file) |
| `--out-dir` | Output directory (required with --in-dir) |
| `--ext` | File extension to process (default: .md) |
| `--dry-run` | Show actions without writing files |
| `--keep-tree` | Preserve input subfolders instead of flattening |
| `--force` | Overwrite existing output files |
| `--stats` | Show statistics about removed placeholders |

## Examples

### Example 1: Clean a single file with statistics

```bash
python3 remove_image_placeholders.py \
  --in-file out_raw/document.md \
  --out-file out_clean/document.md \
  --stats
```

Output:

```
Found 13 image placeholders to remove
Processed: document.md -> document.md
Removed 13 image placeholders
```

### Example 2: Clean an entire directory

```bash
python3 remove_image_placeholders.py \
  --in-dir out_raw \
  --out-dir out_clean_no_images \
  --stats
```

### Example 3: Dry run to preview changes

```bash
python3 remove_image_placeholders.py \
  --in-dir out_raw \
  --out-dir out_clean \
  --dry-run \
  --stats
```

## Integration with Workflow

This script can be used alongside `clean_marker_md.py`:

1. **Convert PDF with Marker** (extracts images + markdown)
2. **Optional: Use `clean_marker_md.py`** to remove tables, captions, etc.
3. **Use `remove_image_placeholders.py`** to remove image placeholders

Or use them independently based on your needs.

## Use Cases

### Use Case 1: Text-only extraction for LLM processing

When you want clean text without image references for feeding to language models.

### Use Case 2: Markdown for documentation

When converting PDFs to documentation where images are not needed.

### Use Case 3: Content analysis

When analyzing text content without visual elements.

## Comparison with clean_marker_md.py

| Feature | clean_marker_md.py | remove_image_placeholders.py |
|---------|-------------------|---------------------------|
| Remove tables | ✅ | ❌ |
| Remove images | ✅ | ✅ |
| Remove captions | ✅ | ❌ |
| Remove math | ✅ | ❌ |
| Remove end-matter | ✅ | ❌ |
| **Keep tables** | Optional | ✅ Always |
| **Keep captions** | Optional | ✅ Always |
| **Simple & focused** | ❌ | ✅ |

## Technical Details

### Pattern Matching

The script uses regex to identify image placeholder lines:

```python
IMAGE_PLACEHOLDER_RE = re.compile(r"^!\[[^\]]*\]\([^)]+\)\s*$")
```

This matches lines that:

- Start with `![`
- Have optional alt text in brackets
- Have a file path in parentheses
- End with optional whitespace

### Edge Cases Handled

- Multiple consecutive blank lines are collapsed to maximum 2
- File always ends with a single newline
- Preserves blank lines around paragraphs
- Unicode and special characters handled via UTF-8 encoding

## Testing

Tested with the FAQs_Computation_Data_EN.md file:

- **Input**: 140 lines with 13 image placeholders
- **Output**: 114 lines (26 lines removed = 13 images + 13 blank lines)
- **Tables preserved**: ✅ Both tables intact
- **Text preserved**: ✅ All content intact
- **Links preserved**: ✅ All hyperlinks working
