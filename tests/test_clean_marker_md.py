import unittest

from clean_marker_md import (
    CITATION_BRACKET_RE,
    classify_endmatter_heading,
    cleanup_text,
    normalize_heading,
)


class CitationPatternTests(unittest.TestCase):
    def test_numeric_citation_cases_match(self) -> None:
        should_match = [
            "[1]",
            "[12]",
            "[5,6]",
            "[1-3]",
            "[12, 45-67]",
        ]
        for text in should_match:
            with self.subTest(text=text):
                self.assertIsNotNone(CITATION_BRACKET_RE.fullmatch(text))

    def test_non_numeric_brackets_do_not_match(self) -> None:
        should_not_match = [
            "[TODO]",
            "[Fig. 1]",
            "[a1b]",
            "[version 2.0]",
            "[v2.1]",
            "[1.5.0]",
            "[1.2.3]",
        ]
        for text in should_not_match:
            with self.subTest(text=text):
                self.assertIsNone(CITATION_BRACKET_RE.fullmatch(text))


class HeadingNormalizationTests(unittest.TestCase):
    def test_decorative_heading_prefixes_normalize(self) -> None:
        self.assertEqual(normalize_heading("■ **REFERENCES**"), "references")
        self.assertEqual(normalize_heading("• ACKNOWLEDGMENTS"), "acknowledgments")

    def test_endmatter_classification_with_decorative_heading(self) -> None:
        self.assertEqual(classify_endmatter_heading("# ■ **REFERENCES**"), "truncate")
        self.assertEqual(
            classify_endmatter_heading("# ■ **ACKNOWLEDGMENTS**"), "section"
        )


class CleanupBehaviorTests(unittest.TestCase):
    def test_cleanup_strips_page_targets_and_numeric_citations(self) -> None:
        text = (
            "A [151](#page-20-0) B [5,6](#page-1-0) "
            "C [Figure](#page-3-0) D [Google](https://example.com)"
        )
        out = cleanup_text(
            text,
            drop_endmatter=False,
            drop_tables=False,
            drop_images=False,
            drop_captions=False,
            drop_math=False,
            drop_image_descriptions=False,
        )
        self.assertNotIn("(#page-", out)
        self.assertNotIn("[151]", out)
        self.assertNotIn("[5,6]", out)
        self.assertIn("[Figure]", out)
        self.assertIn("[Google](https://example.com)", out)

    def test_cleanup_can_keep_numeric_citations(self) -> None:
        text = "A [151](#page-20-0) and [5,6](#page-1-0)"
        out = cleanup_text(
            text,
            drop_endmatter=False,
            drop_tables=False,
            drop_images=False,
            drop_captions=False,
            drop_math=False,
            drop_image_descriptions=False,
            drop_citations=False,
        )
        self.assertNotIn("(#page-", out)
        self.assertIn("[151]", out)
        self.assertIn("[5,6]", out)

    def test_cleanup_removes_citation_shell_artifacts(self) -> None:
        text = (
            "responses [\\]. platforms []. range [[–15\\]]. mixed [\\, ]. "
            "see Fig. [1](#page-1-0)."
        )
        out = cleanup_text(
            text,
            drop_endmatter=False,
            drop_tables=False,
            drop_images=False,
            drop_captions=False,
            drop_math=False,
            drop_image_descriptions=False,
        )
        self.assertNotIn("[\\]", out)
        self.assertNotIn("[]", out)
        self.assertNotIn("[\\, ]", out)
        self.assertNotIn("[[–15\\]]", out)
        self.assertNotIn("Fig..", out)
        self.assertIn("Fig.", out)

    def test_cleanup_keeps_version_like_brackets(self) -> None:
        text = "Version [1.5.0] remains, citation [12](#page-1-0) is removed."
        out = cleanup_text(
            text,
            drop_endmatter=False,
            drop_tables=False,
            drop_images=False,
            drop_captions=False,
            drop_math=False,
            drop_image_descriptions=False,
        )
        self.assertIn("[1.5.0]", out)
        self.assertNotIn("[12]", out)


if __name__ == "__main__":
    unittest.main()
