import unittest
from htmlnode import  LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_prop(self):
        props = {
            "href": "https://www.boot.dev",
        }
        node = LeafNode("a", "Hello, world!", props=props)
        self.assertEqual(
            node.to_html(), '<a href="https://www.boot.dev">Hello, world!</a>'
        )

    def test_leaf_to_html_a_with_mult_prop(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
            "prop": "this",
        }
        node = LeafNode("a", "Hello, world!", props=props)
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev" target="_blank" prop="this">Hello, world!</a>',
        )
