import unittest

from reflow_reading_order import reflow_text


class ReflowReadingOrderTests(unittest.TestCase):
    def test_stitches_across_metadata_block(self) -> None:
        text = (
            "In the last decades, nanomaterials have become very important "
            "because of their useful properties, such as a large surface area "
            "to volume ratio and enhanced electrical and optical\n\n"
            "Published in the topical collection Young Investigators.\n\n"
            "- <sup>1</sup> Institute A\n"
            "- <sup>2</sup> Institute B\n\n"
            "responses, mainly related to the quantum size effect."
        )
        out, stats = reflow_text(text, passes=2)
        self.assertIn("enhanced electrical and optical responses, mainly", out)
        self.assertGreaterEqual(stats.stitched_pairs, 1)

        paragraphs = [p.strip() for p in out.split("\n\n") if p.strip()]
        self.assertTrue(paragraphs[0].startswith("In the last decades"))
        self.assertIn("Published in the topical collection", paragraphs[1])

    def test_does_not_stitch_when_following_paragraph_is_new_sentence(self) -> None:
        text = (
            "This paragraph is already complete.\n\n"
            "Published in the topical collection Young Investigators.\n\n"
            "This Next sentence starts a different thought."
        )
        out, stats = reflow_text(text, passes=2)
        self.assertEqual(stats.stitched_pairs, 0)
        self.assertIn("This paragraph is already complete.", out)
        self.assertIn("This Next sentence starts a different thought.", out)

    def test_stitches_across_figure_caption_block(self) -> None:
        text = (
            "The plasmon modes increase the scattering intensity associated "
            "to an oscillating dipole\n\n"
            "Figure 2. Simulation of radiative enhancement.\n\n"
            "which depends on dipole orientation relative to the metal surface."
        )
        out, stats = reflow_text(text, passes=2)
        self.assertGreaterEqual(stats.stitched_pairs, 1)
        self.assertIn(
            "oscillating dipole which depends on dipole orientation",
            out,
        )
        self.assertIn("Figure 2. Simulation of radiative enhancement.", out)

    def test_does_not_treat_equation_paragraph_as_interruption(self) -> None:
        text = (
            "The Raman scattering intensity can be expressed as:\n\n"
            "(1) I_Raman = (w0 ± wvib) <sup>4</sup> N |E0| <sup>2</sup>\n\n"
            "where w0 ± wvib is the frequency of scattered radiation."
        )
        out, stats = reflow_text(text, passes=2)
        self.assertEqual(stats.stitched_pairs, 0)
        self.assertIn("(1) I_Raman", out)
        self.assertIn("where w0 ± wvib", out)


if __name__ == "__main__":
    unittest.main()
