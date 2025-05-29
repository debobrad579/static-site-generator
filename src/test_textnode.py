import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_diff_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_diff_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_diff_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.brantchess.ca")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.2025ontarioopen.ca")
        self.assertNotEqual(node, node2)

    def test_normal_text_node_to_html_node(self):
        node = TextNode("Test", TextType.NORMAL)
        self.assertEqual(text_node_to_html_node(node).to_html(), "Test")

    def test_bold_text_node_to_html_node(self):
        node = TextNode("Test", TextType.BOLD)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<b>Test</b>")

    def test_italic_text_node_to_html_node(self):
        node = TextNode("Test", TextType.ITALIC)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<i>Test</i>")

    def test_code_text_node_to_html_node(self):
        node = TextNode("Test", TextType.CODE)
        self.assertEqual(text_node_to_html_node(node).to_html(), "<code>Test</code>")

    def test_link_text_node_to_html_node(self):
        node = TextNode("Test", TextType.LINK, "test")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<a href="test">Test</a>')

    def test_image_text_node_to_html_node(self):
        node = TextNode("Test", TextType.IMAGE, "test")
        self.assertEqual(text_node_to_html_node(node).to_html(), '<img alt="Test" src="test"></img>')



if __name__ == "__main__":
    unittest.main()
