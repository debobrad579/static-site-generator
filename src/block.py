from enum import Enum
import re

from htmlnode import HTMLNode
from inline import text_to_textnodes
from leafnode import LeafNode
from parentnode import ParentNode
from textnode import text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str):
    return list(filter(lambda block: block != "", map(lambda block: block.strip(), markdown.split("\n\n"))))


def block_to_block_type(block: str):
    if re.match(r"^#{1,6} ", block): return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"): return BlockType.CODE
    lines = block.split("\n")
    if all(line.startswith(">") for line in lines): return BlockType.QUOTE
    if all(line.startswith("- ") for line in lines): return BlockType.UNORDERED_LIST
    if all(line.startswith(f"{index + 1}. ") for index, line in enumerate(lines)): return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str):
    children: list[HTMLNode] = []

    for block in markdown_to_blocks(markdown):
        match block_to_block_type(block):
            case BlockType.PARAGRAPH:
                children.append(ParentNode("p", text_to_children(block.replace("\n", " "))))
            case BlockType.HEADING:
                text = block.lstrip("#")
                children.append(ParentNode(f"h{len(block) - len(text)}", text_to_children(text[1:])))
            case BlockType.CODE:
                children.append(ParentNode("pre", [LeafNode("code", block.strip("```").strip())]))
            case BlockType.QUOTE:
                children.append(ParentNode("blockquote", text_to_children("\n".join(map(lambda line: line.lstrip(">").strip(), block.split("\n"))))))
            case BlockType.UNORDERED_LIST:
                children.append(ParentNode("ul", list(map(lambda item: ParentNode("li", text_to_children(item.lstrip("- "))), block.split("\n")))))
            case BlockType.ORDERED_LIST:
                children.append(ParentNode("ol", list(map(lambda item: ParentNode("li", text_to_children(item[1].lstrip(f"{item[0] + 1}. "))), enumerate(block.split("\n"))))))

    return ParentNode("div", children)


def text_to_children(text: str):
    return list(map(lambda text_node: text_node_to_html_node(text_node), text_to_textnodes(text)))
