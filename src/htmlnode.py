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


@dataclass(init=False)
class LeafNode(HTMLNode):
    tag: str | None
    value: str
    children: None = None

    def __init__(self, tag: Optional[str], value: str, props: Optional[dict[str, Any]] = None) -> None:
        super().__init__(props=props)
        self.tag = tag
        self.value = value

    def to_html(self):
        if not self.value:
            raise ValueError("All leaf nodes must have a value")
        if not self.tag:
            return self.value
        props = self.props_to_html()
        return f"<{self.tag}{props}>{self.value}</{self.tag}>"

@dataclass(init=False)
class ParentNode(HTMLNode):
    tag: str
    children: list[HTMLNode]

    def __init__(self, tag: Optional[str], children: list[HTMLNode] , props: Optional[dict[str, Any]] = None) -> None:
        super().__init__(props=props)
        self.tag = tag
        self.children = children

    def to_html(self):
        if not self.tag:
            raise ValueError("Parent Node must have a tag")
        if not self.children:
            print(self.children)
            raise ValueError("Parent Node must have children")

        props = self.props_to_html()
        content = ""

        for child in self.children:
            content += child.to_html()
        
        return f"<{self.tag}{props}>{content}</{self.tag}>"

