import unittest

from block import BlockType, block_to_block_type, markdown_to_blocks, markdown_to_html_node


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_block_whitespace(self):
        md = """

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_inline_whitespace(self):
        md = """
            This is **bolded** paragraph

            This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

            - This is a list
- with items
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_heading1(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading2(self):
        block = "## Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading3(self):
        block = "### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading4(self):
        block = "#### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading5(self):
        block = "##### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading6(self):
        block = "###### Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_not_heading(self):
        block = "####### Not Heading"
        self.assertNotEqual(block_to_block_type(block), BlockType.HEADING)

    def test_code(self):
        block = """```
def add(a, b):
    return a + b
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_quote(self):
        block = """> This
> is
> a
> quote"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_not_quote(self):
        block = """> This
> is
not
> a
> quote"""
        self.assertNotEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = """- Item
- Item
- Item"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_not_unordered_list(self):
        block = """- Item
Not Item
- Item"""
        self.assertNotEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = """1. Item
2. Item
3. Item"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_not_ordered_list(self):
        block = """1. Item
3. Item
2. Item"""
        self.assertNotEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        block = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, 
quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. 
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. 
Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading **1**

## Heading _2_

### Heading `3`

#### Heading ![4](https://4url.com)

##### Heading [5](https://5url.com)

###### Heading 6
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            '<div><h1>Heading <b>1</b></h1><h2>Heading <i>2</i></h2><h3>Heading <code>3</code></h3><h4>Heading <img alt="4" src="https://4url.com"></img></h4><h5>Heading <a href="https://5url.com">5</a></h5><h6>Heading 6</h6></div>'
        )

    def test_quote(self):
        md = """
# Quote

> This
> is
> a
> quote
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h1>Quote</h1><blockquote>This\nis\na\nquote</blockquote></div>"
        )

    def test_unordered_list(self):
        md = """
# Unordered List

- Item
- Another item
- A final item
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h1>Unordered List</h1><ul><li>Item</li><li>Another item</li><li>A final item</li></ul></div>"
        )

    def test_ordered_list(self):
        md = """
# Ordered List

1. Item
2. A second item
3. A third item
"""
        self.assertEqual(
            markdown_to_html_node(md).to_html(),
            "<div><h1>Ordered List</h1><ol><li>Item</li><li>A second item</li><li>A third item</li></ol></div>"
        )
