import argparse
import re
from pathlib import Path


def parse_args():
    parser = argparse.ArgumentParser(
        description="Fix markdown issues (page links, word[suffixNumbers] pattern, etc.)"
    )
    parser.add_argument("in_file", type=Path, help="Input markdown file to process")
    parser.add_argument(
        "out_file", type=Path, nargs="?", help="Output file (default: in_file.fixed.md)"
    )
    return parser.parse_args()


args = parse_args()

if args.out_file is None:
    args.out_file = args.in_file.with_suffix(".fixed.md")

file_path = args.in_file
output_path = args.out_file

try:
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # 1. Remove page links (#page-X-Y)
    content = re.sub(r"\(#page-\d+-\d+\)", "", content)

    # 2. Fix word[suffixNumbers] pattern
    # Examples: rang[e8], filler[s15], enthalp[y26], graphen[e57], paraffin[58]
    # Regex: (\w+)\[([a-zA-Z]*)(\d+[0-9.,–\-\u2013\u2014]*)\]
    # We include standard and unicode hyphens/dashes in citation range
    content = re.sub(
        r"(\w+)\[([a-zA-Z]*)(\d+[0-9.,–\-\u2013\u2014]*)\]", r"\1\2 [\3]", content
    )

    # 3. Move trailing dot outside of brackets: [12.] -> [12].
    content = re.sub(r"\[([\d.,–\-\u2013\u2014]+)\.\]", r"[\1].", content)

    # 4. Replace special minus sign with hyphen
    content = content.replace("−", "-")

    # 5. Normalize newlines (ensure max 2 newlines)
    content = re.sub(r"\n{3,}", "\n\n", content)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"Fixed file written to: {output_path}")

except Exception as e:
    print(f"Error: {e}")
