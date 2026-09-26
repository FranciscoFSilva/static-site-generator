from re import findall, search

from textnode import TextNode, TextType

from enum import StrEnum, auto

type ImageInfo = tuple[str, str]
type LinkInfo = tuple[str, str]


class BlockType(StrEnum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def extract_markdown_images(text) -> list[ImageInfo]:
    return findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text) -> list[LinkInfo]:
    return findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_node: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_node.append(old_node)
            continue
        text = old_node.text
        matches = extract_markdown_images(text)
        if matches:
            for image_alt, image_link in matches:
                split_text = text.split(f"![{image_alt}]({image_link})", 1)
                if split_text[0]:
                    new_node.append(TextNode(split_text[0], TextType.TEXT))
                new_node.append(TextNode(image_alt, TextType.IMAGE, image_link))
                text = split_text[1]
        if text:
            new_node.append(TextNode(text, TextType.TEXT))
    return new_node


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    new_node: list[TextNode] = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_node.append(old_node)
            continue
        text = old_node.text
        matches = extract_markdown_links(text)
        if matches:
            for link_name, link_url in matches:
                split_text = text.split(f"[{link_name}]({link_url})", 1)
                if split_text[0]:
                    new_node.append(TextNode(split_text[0], TextType.TEXT))
                new_node.append(TextNode(link_name, TextType.LINK, link_url))
                text = split_text[1]
        if text:
            new_node.append(TextNode(text, TextType.TEXT))
    return new_node


def text_to_textnodes(input: str) -> list[TextNode]:
    src_node = TextNode(input, TextType.TEXT)
    nodes = split_nodes_delimiter([src_node], "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes


def markdown_to_blocks(markdown: str) -> list[str]:
    return list(filter(None, [block.strip() for block in markdown.split("\n\n")]))


def block_to_block_type(block: str) -> BlockType:
    if search(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in block.split("\n"):
            if not search(r"^> ?", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in block.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        no = 1
        for line in block.split("\n"):
            if not search(rf"^{no}+. ", line):
                return BlockType.PARAGRAPH
            no += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
