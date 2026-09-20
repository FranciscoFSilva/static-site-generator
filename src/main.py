# src/main.py

from textnode import TextNode, TextType

def main() -> None:
    text_node = TextNode("This is some anchor text",TextType.LINK_ANCHOR, "https://www.boot.dev")
    print(text_node)

main()
