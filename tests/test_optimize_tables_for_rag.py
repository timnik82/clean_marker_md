import unittest

from optimize_tables_for_rag import process_markdown


class OptimizeTablesForRagTests(unittest.TestCase):
    def test_form_table_counts_removed_empty_columns(self) -> None:
        content = (
            "| Campo | Limite | |\n|---|---|---|\n| Nome | 10 | |\n| Email | 50 | |\n"
        )

        output, stats = process_markdown(content)

        self.assertEqual(stats["form_cleaned"], 1)
        self.assertEqual(stats["empty_cols_removed"], 1)
        self.assertIn("| Campo | Limite |", output)
        self.assertNotIn("| Campo | Limite | |", output)


if __name__ == "__main__":
    unittest.main()
