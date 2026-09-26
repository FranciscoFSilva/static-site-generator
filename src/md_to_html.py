from textnode import TextType
from htmlnode import HTMLNode, ParentNode, LeafNode
from md_parser import (
    markdown_to_blocks,
    block_to_block_type,
    text_to_textnodes,
    BlockType,
)
from re import sub


def markdown_to_html_node(markdown: str) -> ParentNode:
    def text_to_children(text: str) -> list[HTMLNode]:
        child_nodes = []
        text_nodes = text_to_textnodes(text)
        for text_node in text_nodes:
            match text_node.text_type:
                case TextType.TEXT:
                    child_nodes.append(LeafNode(None, text_node.text))
                case TextType.BOLD:
                    child_nodes.append(LeafNode("b", text_node.text))
                case TextType.ITALIC:
                    child_nodes.append(LeafNode("i", text_node.text))
                case TextType.CODE:
                    child_nodes.append(LeafNode("code", text_node.text))
                case TextType.IMAGE:
                    child_nodes.append(
                        LeafNode(
                            "img", "", {"src": text_node.url, "alt": text_node.text}
                        )
                    )
                case TextType.LINK:
                    child_nodes.append(
                        LeafNode("a", text_node.text, {"href": text_node.url})
                    )
        return child_nodes

    def paragraph_to_html_node(text: str) -> HTMLNode:
        formatted_text = block.replace("\n", " ")
        child_nodes = text_to_children(formatted_text)
        return ParentNode("p", child_nodes)

    def heading_to_html_node(text: str) -> HTMLNode:
        formatted_text = text.replace("\n", " ")
        heading, heading_text = formatted_text.split(" ", 1)
        child_nodes = text_to_children(heading_text)
        return ParentNode(f"h{len(heading)}", child_nodes)

    def quote_to_html_node(text: str) -> HTMLNode:
        lines = []
        parent_nodes = []
        for line in text.split("\n"):
            formatted_line = sub(r"^> ?", "", line)
            if formatted_line:
                lines.append(formatted_line)
            else:
                child_nodes = text_to_children(" ".join(lines))
                parent_nodes.append(ParentNode("p", child_nodes))
                lines = []

        child_nodes = text_to_children(" ".join(lines))
        if child_nodes:
            parent_nodes.append(ParentNode("p", child_nodes))
        return ParentNode("blockquote", parent_nodes)

    def unordered_list_to_html_node(text: str) -> HTMLNode:
        parent_nodes = []
        for line in text.split("\n"):
            formatted_line = sub(r"^- ", "", line)
            child_nodes = text_to_children(formatted_line)
            parent_nodes.append(ParentNode("li", child_nodes))
        return ParentNode("ul", parent_nodes)

    def ordered_list_to_html_node(text: str) -> HTMLNode:
        parent_nodes = []
        for line in text.split("\n"):
            formatted_line = sub(r"^\d+. ", "", line)
            child_nodes = text_to_children(formatted_line)
            parent_nodes.append(ParentNode("li", child_nodes))
        return ParentNode("ol", parent_nodes)

    def code_to_html_node(text: str) -> HTMLNode:
        formatted_text = sub(r"```$", "", sub(r"^```\n", "", text))
        child_node = LeafNode("code", formatted_text)
        return ParentNode("pre", [child_node])

    child_nodes = []

    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                child_nodes.append(paragraph_to_html_node(block))
            case BlockType.HEADING:
                child_nodes.append(heading_to_html_node(block))
            case BlockType.CODE:
                child_nodes.append(code_to_html_node(block))
            case BlockType.QUOTE:
                child_nodes.append(quote_to_html_node(block))
            case BlockType.UNORDERED_LIST:
                child_nodes.append(unordered_list_to_html_node(block))
            case BlockType.ORDERED_LIST:
                child_nodes.append(ordered_list_to_html_node(block))

    return ParentNode("div", child_nodes)
