import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_empty_props(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_one_prop(self):
        node = HTMLNode(props={"href": "https://www.advantageauto.ca"})
        self.assertEqual(node.props_to_html(), 'href="https://www.advantageauto.ca"')

    def test_multiple_props(self):
        node = HTMLNode(props={"class": "background-color: red;", "disabled": "true"})
        self.assertEqual(node.props_to_html(), 'class="background-color: red;" disabled="true"')

