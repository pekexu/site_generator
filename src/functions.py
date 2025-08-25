from htmlnode import *
from textnode import *


def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        split_text = node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise Exception("Error: Invalid number of delimiters")
        for i in range(0, len(split_text)):
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], TextType.TEXT))
            elif i % 2 == 1:
                new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

        