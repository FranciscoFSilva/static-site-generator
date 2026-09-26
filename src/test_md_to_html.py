import unittest
from md_to_html import markdown_to_html_node

class TestMDToHTML(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_headings(self):
        md = "# This is it. **bold** and _strong_.\n[link](www.google.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h1>This is it. <b>bold</b> and <i>strong</i>. <a href="www.google.com">link</a></h1></div>',
        )

    def test_unordered_lists(self):
        md = "- This is it.\n- **bold** and - this is special - _strong_.\n- [link](www.google.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ul><li>This is it.</li><li><b>bold</b> and - this is special - <i>strong</i>.</li><li><a href="www.google.com">link</a></li></ul></div>',
        )

    def test_ordered_lists(self):
        md = "1. This is it.\n2. **bold** and 4. _strong_.\n3. ![link](www.google.com)\n"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><ol><li>This is it.</li><li><b>bold</b> and 4. <i>strong</i>.</li><li><img src="www.google.com" alt="link"></img></li></ol></div>',
        )

    def test_quoteblock(self):
        md = "> This is it.\n> **bold** and > _strong_.\n>![link](www.google.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote><p>This is it. <b>bold</b> and > <i>strong</i>. <img src="www.google.com" alt="link"></img></p></blockquote></div>',
        )

    def test_quoteblock_two_paragraphs(self):
        md = "> This is it.\n> **bold** and\n>\n> _strong_.\n>![link](www.google.com)"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote><p>This is it. <b>bold</b> and</p><p><i>strong</i>. <img src="www.google.com" alt="link"></img></p></blockquote></div>',
        )

    def test_quoteblock_two_paragraphs(self):
        md = "> This is it.\n> **bold** and\n>\n> _strong_.\n>![link](www.google.com)\n> "
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><blockquote><p>This is it. <b>bold</b> and</p><p><i>strong</i>. <img src="www.google.com" alt="link"></img></p></blockquote></div>',
        )

    def test_codeblock(self):
        md = "```\nThis is text that _should_ remain\nthe **same** even with inline stuff\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
