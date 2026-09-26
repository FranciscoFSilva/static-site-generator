from enum import StrEnum, auto
from re import search


class BlockType(StrEnum):
    PARAGRAPH = auto()
    HEADING = auto()
    CODE = auto()
    QUOTE = auto()
    UNORDERED_LIST = auto()
    ORDERED_LIST = auto()


def block_to_block_type(block: str) -> BlockType:
    if search(r"^#{1,6} ", block):
        return BlockType.HEADING
    if block.startswith("```\n") and block.endswith("\n```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in block.split("\n"):
            if not search(r"^> ?", line):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in block.split("\n"):
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        no = 1
        for line in block.split("\n"):
            if not search(rf"^{no}+. ", line):
                return BlockType.PARAGRAPH
            no += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
