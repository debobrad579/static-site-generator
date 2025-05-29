import unittest

from main import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_heading(self):
        md = """
# Heading

## Subheading
"""
        self.assertEqual(extract_title(md), "Heading")

    def test_no_heading(self):
        md = "## Subheading"
        with self.assertRaises(Exception):
            extract_title(md)

