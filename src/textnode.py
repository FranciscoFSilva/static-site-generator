from enum import auto, StrEnum
from dataclasses import dataclass
from typing import Optional


class TextType(StrEnum):
    PLAIN = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK_ANCHOR = auto()
    IMAGE_ALT = auto()


@dataclass
class TextNode:
    text: str
    text_type: TextType
    url: Optional[str] = None
