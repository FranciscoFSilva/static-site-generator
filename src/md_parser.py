from re import findall

from textnode import TextNode, TextType

type ImageInfo = tuple[str, str]
type LinkInfo = tuple[str, str]


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

if __name__ == "__main__":
    text_node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.TEXT,
    )

    print("yes")
