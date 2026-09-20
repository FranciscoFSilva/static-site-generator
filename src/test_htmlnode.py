import unittest
from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_node_creation(self):
        node = HTMLNode("p", "this is a paragraph", None, None)
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "this is a paragraph")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_none_node(self):
        node = HTMLNode()
        self.assertEqual(node.tag, None)
        self.assertEqual(node.value, None)
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_node_props_setting(self):
        node = HTMLNode("a", "boot", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.value, "boot")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"href": "https://www.boot.dev"})

    def test_node_children(self):
        node_a = HTMLNode("a", "boot", None, {"href": "https://www.boot.dev"})
        node_b = HTMLNode("a", "dev", None, {"href": "https://www.boot.dev"})
        node_div = HTMLNode("<div>", None, [node_a, node_b], None)
        self.assertEqual(node_div.children, [node_a, node_b])

    def test_get_one_prop_to_text(self):
        node_a = HTMLNode("a", "boot", None, {"href": "https://www.boot.dev"})
        prop_str = node_a.props_to_html()
        self.assertEqual(prop_str, ' href="https://www.boot.dev"')

    def test_get_multiple_prop_to_text(self):
        props = {
            "href": "https://www.boot.dev",
            "target": "_blank",
            "prop": "this",
        }
        node_a = HTMLNode("a", "boot", None, props)
        prop_str = node_a.props_to_html()
        self.assertEqual(
            prop_str, ' href="https://www.boot.dev" target="_blank" prop="this"'
        )

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


if __name__ == "__main__":
    unittest.main()
