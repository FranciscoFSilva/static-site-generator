import unittest

from block_parser import BlockType, block_to_block_type


class TestBlockParser(unittest.TestCase):
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
