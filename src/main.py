# src/main.py

from textnode import TextNode, TextType
from htmlnode import HTMLNode


def main() -> None:
    text_node = TextNode(
        "This is some anchor text", TextType.LINK, "https://www.boot.dev"
    )
    print(text_node)
    html_node = HTMLNode("<p>", "This", None, None)
    print(html_node)


main()
