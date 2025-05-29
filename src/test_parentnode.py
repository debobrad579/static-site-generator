import unittest

from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_one_child(self):
        node = ParentNode("div", [LeafNode("div", "Hello, world!")])
        self.assertEqual(node.to_html(), "<div><div>Hello, world!</div></div>")

    def test_to_html_multiple_children(self):
        node = ParentNode("div", [LeafNode("div", "Hello, world!"), LeafNode("p", "Goodbye, world!"), ParentNode("div", [LeafNode("p", "Nested futher")])])
        self.assertEqual(node.to_html(), "<div><div>Hello, world!</div><p>Goodbye, world!</p><div><p>Nested futher</p></div></div>")

    def test_to_html_no_children(self):
        node = ParentNode("p", [])
        self.assertEqual(node.to_html(), "<p></p>")

