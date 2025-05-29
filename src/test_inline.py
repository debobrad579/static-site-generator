import unittest

from inline import extract_markdown_images, extract_markdown_links, split_nodes_delimiter, split_nodes_image, split_nodes_link, text_to_textnodes
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("test `code` text", TextType.NORMAL)
        self.assertListEqual(split_nodes_delimiter([node], "`", TextType.CODE), [TextNode("test ", TextType.NORMAL), TextNode("code", TextType.CODE), TextNode(" text", TextType.NORMAL)])

    def test_italic(self):
        node = TextNode("test _italic_ text", TextType.NORMAL)
        self.assertListEqual(split_nodes_delimiter([node], "_", TextType.ITALIC), [TextNode("test ", TextType.NORMAL), TextNode("italic", TextType.ITALIC), TextNode(" text", TextType.NORMAL)])

    def test_bold(self):
        node = TextNode("test **bold** text", TextType.NORMAL)
        self.assertListEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("test ", TextType.NORMAL), TextNode("bold", TextType.BOLD), TextNode(" text", TextType.NORMAL)])

    def test_end(self):
        node = TextNode("test **end**", TextType.NORMAL)
        self.assertListEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("test ", TextType.NORMAL), TextNode("end", TextType.BOLD)])

    def test_start(self):
        node = TextNode("**start** test", TextType.NORMAL)
        self.assertListEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("start", TextType.BOLD), TextNode(" test", TextType.NORMAL)])

    def test_multiple(self):
        node = TextNode("**start** test **end**", TextType.NORMAL)
        self.assertListEqual(split_nodes_delimiter([node], "**", TextType.BOLD), [TextNode("start", TextType.BOLD), TextNode(" test ", TextType.NORMAL), TextNode("end", TextType.BOLD)])

    def test_multiple_nodes(self):
        node = TextNode("**start** test **end**", TextType.NORMAL)
        node2 = TextNode("test **end**", TextType.NORMAL)
        self.assertListEqual(split_nodes_delimiter([node, node2], "**", TextType.BOLD), [TextNode("start", TextType.BOLD), TextNode(" test ", TextType.NORMAL), TextNode("end", TextType.BOLD), TextNode("test ", TextType.NORMAL), TextNode("end", TextType.BOLD)])

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_image(self):
        matches = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual(matches, [("image", "https://i.imgur.com/zjjcJKZ.png")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        self.assertListEqual(matches, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_link(self):
        matches = extract_markdown_links("This is text with a [link](https://www.google.com)")
        self.assertListEqual(matches, [("link", "https://www.google.com")])

    def test_extract_markdown_links(self):
        matches = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual(matches, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) and more text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with an ", TextType.NORMAL),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
                TextNode(" and more text", TextType.NORMAL)
            ],
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [second link](https://www.boot.dev) and more text",
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.NORMAL),
                TextNode(
                    "second link", TextType.LINK, "https://www.boot.dev"
                ),
                TextNode(" and more text", TextType.NORMAL)
            ],
        )


class TestTextToTextnodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes("This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)")
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )
