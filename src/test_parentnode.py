import unittest

from htmlnode import LeafNode, ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_child(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", children=[child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", children=[child_node, child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span>child</span><span>child</span></div>"
        )

    def test_to_html_with_grandchild(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node, grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b><b>grandchild</b></span></div>",
        )

    def test_to_html_with_children_and_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        child_2_node = LeafNode("b", "child with no grandchildren")
        parent_node = ParentNode("div", [child_node, child_2_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span><b>child with no grandchildren</b></div>",
        )

    def test_parent_with_no_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", None)  # ty : ignore[invalid-argument-type]

    def test_parent_with_empty_children(self):
        with self.assertRaises(ValueError):
            ParentNode("div", [])


if __name__ == "__main__":
    unittest.main()
