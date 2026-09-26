from dataclasses import dataclass
from typing import Any, Optional


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


@dataclass(init=False)
class LeafNode(HTMLNode):
    tag: str | None
    value: str
    children: None = None

    def __init__(
        self, tag: Optional[str], value: str, props: Optional[dict[str, Any]] = None
    ) -> None:
        if value is None:
            raise ValueError("All leaf nodes must have a value")
        super().__init__(props=props)
        self.tag = tag
        self.value = value

    def to_html(self):
        if not self.tag:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"


@dataclass(init=False)
class ParentNode(HTMLNode):
    tag: str
    children: list[HTMLNode] | None

    def __init__(
        self,
        tag: str,
        children: list[HTMLNode] | None,
        props: Optional[dict[str, Any]] = None,
    ) -> None:
        if not tag:
            raise ValueError("Parent Node must have a tag")
        if not children:
            print(self.children)
            raise ValueError("Parent Node must have children")
        super().__init__(props=props)
        self.tag = tag
        self.children = children

    def to_html(self):
        props = self.props_to_html()
        content = ""

        if not self.children:
            raise RuntimeError("Parent with no Children")

        for child in self.children:
            content += child.to_html()

        return f"<{self.tag}{props}>{content}</{self.tag}>"
