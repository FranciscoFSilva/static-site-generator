# src/main.py

from htmlnode import HTMLNode
from textnode import TextNode, TextType
from md_parser import split_nodes_image


def main() -> None:
    text_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(text_node)
    html_node = HTMLNode("<p>", "This", None, None)
    print(html_node)


main()
