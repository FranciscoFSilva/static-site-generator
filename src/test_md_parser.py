import unittest

from md_parser import (
    BlockType,
    block_to_block_type,
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestMDParser(unittest.TestCase):
    def test_empty_text_node(self):
        text_node = TextNode("", TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(node_list[0].text, "")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)

    def test_not_text_node(self):
        text_node = TextNode("Bold", TextType.BOLD)
        node_list = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        self.assertEqual(node_list[0].text, "Bold")
        self.assertEqual(node_list[0].text_type, TextType.BOLD)

    def test_text_node_with_bold(self):
        text_node = TextNode("This is **Bold**", TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "Bold")
        self.assertEqual(node_list[1].text_type, TextType.BOLD)

    def test_text_node_with_italic(self):
        text_node = TextNode("This is _italic_", TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "italic")
        self.assertEqual(node_list[1].text_type, TextType.ITALIC)

    def test_text_node_with_code(self):
        text_node = TextNode("This is `code`", TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "code")
        self.assertEqual(node_list[1].text_type, TextType.CODE)

    def test_text_node_with_two_bolds(self):
        text_node = TextNode("This is **Bold** and **Bolder** boy", TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(node_list), 5)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "Bold")
        self.assertEqual(node_list[1].text_type, TextType.BOLD)
        self.assertEqual(node_list[2].text, " and ")
        self.assertEqual(node_list[2].text_type, TextType.TEXT)
        self.assertEqual(node_list[3].text, "Bolder")
        self.assertEqual(node_list[3].text_type, TextType.BOLD)
        self.assertEqual(node_list[4].text, " boy")
        self.assertEqual(node_list[4].text_type, TextType.TEXT)

    def test_text_node_with_bold_and_italic(self):
        text_node = TextNode("This is **Bold** and _Bolder_ boy", TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(node_list), 3)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "Bold")
        self.assertEqual(node_list[1].text_type, TextType.BOLD)
        self.assertEqual(node_list[2].text, " and _Bolder_ boy")
        self.assertEqual(node_list[2].text_type, TextType.TEXT)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_multiple_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ],
            matches,
        )

    def test_extract_markdown_images_empty_text(self):
        matches = extract_markdown_images(
            "This is text with an ![](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_empty_text(self):
        matches = extract_markdown_links(
            "This is text with an [](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links_more_brackets(self):
        matches = extract_markdown_links(
            "This is text with an [[]](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([], matches)

    def test_split_nodes_image_empty(self):
        text_node = TextNode("", TextType.TEXT)
        node_list = split_nodes_image([text_node])
        self.assertEqual(len(node_list), 0)

    def test_split_nodes_image(self):
        text_node = TextNode("![image](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node_list = split_nodes_image([text_node])
        self.assertEqual(len(node_list), 1)
        self.assertEqual(node_list[0].text, "image")
        self.assertEqual(node_list[0].text_type, TextType.IMAGE)
        self.assertEqual(node_list[0].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_nodes_image_with_text_before(self):
        text_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node_list = split_nodes_image([text_node])
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "This is text with an ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "image")
        self.assertEqual(node_list[1].text_type, TextType.IMAGE)
        self.assertEqual(node_list[1].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_nodes_image_with_text_after(self):
        text_node = TextNode(
            "![image](https://i.imgur.com/zjjcJKZ.png) with text after", TextType.TEXT
        )
        node_list = split_nodes_image([text_node])
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "image")
        self.assertEqual(node_list[0].text_type, TextType.IMAGE)
        self.assertEqual(node_list[0].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(node_list[1].text, " with text after")
        self.assertEqual(node_list[1].text_type, TextType.TEXT)

    def test_split_nodes_multiple_images(self):
        text_node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node_list = split_nodes_image([text_node])
        self.assertEqual(len(node_list), 4)
        self.assertEqual(node_list[0].text, "This is text with an ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "image")
        self.assertEqual(node_list[1].text_type, TextType.IMAGE)
        self.assertEqual(node_list[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(node_list[2].text, " and another ")
        self.assertEqual(node_list[2].text_type, TextType.TEXT)
        self.assertEqual(node_list[3].text, "image")
        self.assertEqual(node_list[3].text_type, TextType.IMAGE)
        self.assertEqual(node_list[1].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_nodes_link_empty(self):
        text_node = TextNode("", TextType.TEXT)
        node_list = split_nodes_link([text_node])
        self.assertEqual(len(node_list), 0)

    def test_split_nodes_link(self):
        text_node = TextNode("[link](https://i.imgur.com/zjjcJKZ.png)", TextType.TEXT)
        node_list = split_nodes_link([text_node])
        self.assertEqual(len(node_list), 1)
        self.assertEqual(node_list[0].text, "link")
        self.assertEqual(node_list[0].text_type, TextType.LINK)
        self.assertEqual(node_list[0].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_nodes_link_with_text_before(self):
        text_node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node_list = split_nodes_link([text_node])
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "This is text with an ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "link")
        self.assertEqual(node_list[1].text_type, TextType.LINK)
        self.assertEqual(node_list[1].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_split_nodes_link_with_text_after(self):
        text_node = TextNode(
            "[link](https://i.imgur.com/zjjcJKZ.png) with text after", TextType.TEXT
        )
        node_list = split_nodes_link([text_node])
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "link")
        self.assertEqual(node_list[0].text_type, TextType.LINK)
        self.assertEqual(node_list[0].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(node_list[1].text, " with text after")
        self.assertEqual(node_list[1].text_type, TextType.TEXT)

    def test_split_nodes_multiple_links(self):
        text_node = TextNode(
            "This is text with an [link](https://i.imgur.com/zjjcJKZ.png) and another [link](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        node_list = split_nodes_link([text_node])
        self.assertEqual(len(node_list), 4)
        self.assertEqual(node_list[0].text, "This is text with an ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "link")
        self.assertEqual(node_list[1].text_type, TextType.LINK)
        self.assertEqual(node_list[1].url, "https://i.imgur.com/zjjcJKZ.png")
        self.assertEqual(node_list[2].text, " and another ")
        self.assertEqual(node_list[2].text_type, TextType.TEXT)
        self.assertEqual(node_list[3].text, "link")
        self.assertEqual(node_list[3].text_type, TextType.LINK)
        self.assertEqual(node_list[1].url, "https://i.imgur.com/zjjcJKZ.png")

    def test_text_to_textnodes(self):
        input = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(input)
        self.assertEqual(nodes[0], TextNode("This is ", TextType.TEXT))
        self.assertEqual(nodes[1], TextNode("text", TextType.BOLD))
        self.assertEqual(nodes[2], TextNode(" with an ", TextType.TEXT))
        self.assertEqual(nodes[3], TextNode("italic", TextType.ITALIC))
        self.assertEqual(nodes[4], TextNode(" word and a ", TextType.TEXT))
        self.assertEqual(nodes[5], TextNode("code block", TextType.CODE))
        self.assertEqual(nodes[6], TextNode(" and an ", TextType.TEXT))
        self.assertEqual(
            nodes[7],
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        )
        self.assertEqual(nodes[8], TextNode(" and a ", TextType.TEXT))
        self.assertEqual(nodes[9], TextNode("link", TextType.LINK, "https://boot.dev"))

    def test_text_to_textnodes_empty(self):
        input = ""
        nodes = text_to_textnodes(input)
        self.assertEqual(isinstance(nodes, list), True)
        self.assertEqual(len(nodes), 0)

    def test_text_to_textnodes_no_text(self):
        input = "**bold****bold**"
        nodes = text_to_textnodes(input)
        self.assertEqual(nodes[0], TextNode("bold", TextType.BOLD))
        self.assertEqual(nodes[1], TextNode("bold", TextType.BOLD))

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_empty_block(self):
        block = ""
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_paragraph_block(self):
        block = ">this\nis the shit"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_Heading_block(self):
        block = "# this\n> is the shit\n>right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_Heading_block_fail_no_space(self):
        block = "#this\n> is the shit\n>right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_Heading_block_fail_H7(self):
        block = "####### this\n> is the shit\n>right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = ">this\n> is the shit\n>right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_quote_block_fail(self):
        block = ">this\n is the shit\n>right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```\nthis\n> is the shit\n>right?\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_code_block_fail(self):
        block = "```\nthis\n> is the shit\n>right?```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_unordered_list_block(self):
        block = "- this\n- is the shit\n- right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_unordered_list_block_fail(self):
        block = "- this\n* is the shit\n- right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_ordered_list_block(self):
        block = "1. this\n2. is the shit\n3. right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_ordered_list_block_fail(self):
        block = "1. this\n2. is the shit\n4. right?"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_extract_title(self):
        markdown = "# Hello\n\nThis is an amazing adventure!\n\n- list\n- this\n- shit\n\n## I know what I am doing\n # this"
        title = extract_title(markdown)
        self.assertEqual(title, "Hello")

    def test_extract_title_error(self):
        markdown = "Hello\n\nThis is an amazing adventure!\n\n- list\n- this\n- shit\n\n## I know what I am doing\n# this"
        with self.assertRaises(ValueError):
            extract_title(markdown)
