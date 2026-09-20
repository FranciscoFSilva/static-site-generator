import unittest
from textnode import TextNode, TextType
from md_parser import split_nodes_delimiter


class TestMDParser(unittest.TestCase):
    def test_empty_text_node(self):
        text_node = TextNode("",TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(node_list[0].text, "")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)

    def test_not_text_node(self):
        text_node = TextNode("Bold",TextType.BOLD)
        node_list = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        self.assertEqual(node_list[0].text, "Bold")
        self.assertEqual(node_list[0].text_type, TextType.BOLD)

    def test_text_node_with_bold(self):
        text_node = TextNode("This is **Bold**",TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "Bold")
        self.assertEqual(node_list[1].text_type, TextType.BOLD)

    def test_text_node_with_italic(self):
        text_node = TextNode("This is _italic_",TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "_", TextType.ITALIC)
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "italic")
        self.assertEqual(node_list[1].text_type, TextType.ITALIC)

    def test_text_node_with_code(self):
        text_node = TextNode("This is `code`",TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "`", TextType.CODE)
        self.assertEqual(len(node_list), 2)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "code")
        self.assertEqual(node_list[1].text_type, TextType.CODE)

    def test_text_node_with_two_bolds(self):
        text_node = TextNode("This is **Bold** and **Bolder** boy",TextType.TEXT)
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
        text_node = TextNode("This is **Bold** and _Bolder_ boy",TextType.TEXT)
        node_list = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        self.assertEqual(len(node_list), 3)
        self.assertEqual(node_list[0].text, "This is ")
        self.assertEqual(node_list[0].text_type, TextType.TEXT)
        self.assertEqual(node_list[1].text, "Bold")
        self.assertEqual(node_list[1].text_type, TextType.BOLD)
        self.assertEqual(node_list[2].text, " and _Bolder_ boy")
        self.assertEqual(node_list[2].text_type, TextType.TEXT)

