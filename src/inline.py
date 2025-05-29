import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        sections = node.text.split(delimiter)

        for index, section in enumerate(sections):
            if section == "": continue
            if index % 2 == 0: new_nodes.append(TextNode(section, TextType.NORMAL))
            else: new_nodes.append(TextNode(section, text_type))

    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)

        remaining_text = node.text

        for image in images:
            sections = remaining_text.split(f"![{image[0]}]({image[1]})")
            if sections[0] != "": new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
            remaining_text = sections[1]

        if remaining_text != "": new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        remaining_text = node.text

        for link in links:
            sections = remaining_text.split(f"[{link[0]}]({link[1]})")
            if sections[0] != "": new_nodes.append(TextNode(sections[0], TextType.NORMAL))
            new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            remaining_text = sections[1]

        if remaining_text != "": new_nodes.append(TextNode(remaining_text, TextType.NORMAL))

    return new_nodes


def text_to_textnodes(text: str):
    return split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(split_nodes_link(split_nodes_image([TextNode(text, TextType.NORMAL)])), "**", TextType.BOLD), "_", TextType.ITALIC), "`", TextType.CODE)

