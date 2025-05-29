from typing import Optional, Sequence
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: Sequence[HTMLNode], props: Optional[dict[str, str]] = None) -> None:
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None: raise ValueError("all parent nodes must have a tag")
        if self.children is None: raise ValueError("all parent nodes must have children")
        inner = ""
        for child in self.children:
            inner += child.to_html()
        return f"<{self.tag}{" " if self.props is not None else ""}{self.props_to_html()}>{inner}</{self.tag}>"

