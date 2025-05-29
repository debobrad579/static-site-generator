from typing import Optional, Sequence

class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[Sequence['HTMLNode']] = None,
        props: Optional[dict[str, str]] = None
    ) -> None:
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if self.props is None: return ""
        return " ".join(map(lambda prop: f'{prop[0]}="{prop[1]}"', self.props.items()))

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

