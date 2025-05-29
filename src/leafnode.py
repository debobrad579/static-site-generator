from typing import Optional, Union
from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag: Union[str, None], value: str, props: Optional[dict[str, str]] = None) -> None:
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if self.value is None: raise ValueError("all leafnodes must have a value")
        if self.tag is None: return self.value
        return f"<{self.tag}{" " if self.props is not None else ""}{self.props_to_html()}>{self.value}</{self.tag}>"

