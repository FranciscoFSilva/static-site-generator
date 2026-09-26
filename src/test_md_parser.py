import unittest

from md_parser import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link
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
