from dataclasses import dataclass
from typing import Optional, Any


@dataclass
class HTMLNode:
    tag: Optional[str] = None
    value: Optional[str] = None
    children: Optional[list["HTMLNode"]] = None
    props: Optional[dict[str, Any]] = None

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self) -> str:
        if not self.props:
            return ""
        return "".join([f' {k}="{v}"' for k, v in self.props.items()])


@dataclass
class LeafNode(HTMLNode):
    tag: str | None
    value: str
    children: None = None
    props: Optional[dict[str, Any]] = None

    def __post_init__(self):
        if self.children is not None:
            raise ValueError("LeafNode cannot have children")
        if self.tag is None:
            raise ValueError("LeafNode needs to have a tag")

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"
