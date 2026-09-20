from textnode import TextNode, TextType
from re import findall

type ImageInfo = tuple[str, str]
type LinkInfo = tuple[str, str]


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_node: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_node.append(old_node)
            continue
        text = old_node.text
        splitted_text = text.split(delimiter)
        if len(splitted_text) == 1:
            new_node.append(old_node)
            continue
        if len(splitted_text) % 2 == 0:
            raise RuntimeError(
                "Invalid Markdown syntax. Check missing closing delimiters"
            )
        for i, split in enumerate(splitted_text):
            if split == "":
                continue
            if i % 2 == 0:
                new_node.append(TextNode(split, TextType.TEXT))
            else:
                new_node.append(TextNode(split, text_type))

    return new_node


def extract_markdown_images(text) -> list[ImageInfo]:
    return findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text) -> list[LinkInfo]:
    return findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
