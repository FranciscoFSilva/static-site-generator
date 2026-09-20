from enum import auto, StrEnum

class TextType(StrEnum):
    PLAIN = auto()
    BOLD = auto()
    ITALIC = auto()
    CODE = auto()
    LINK_ANCHOR = auto()
    IMAGE_ALT = auto()


class TextNode():
    def __init__(self, text: str, text_type: TextType, url: str | None = None) -> None:
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TextNode):
            return False
        text_eq = self.text == other.text
        text_type_eq = self.text_type == other.text_type
        url_eq = self.url == other.url
        if text_eq & text_type_eq & url_eq:
            return True
        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

