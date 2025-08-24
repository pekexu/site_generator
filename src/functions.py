from htmlnode import *
from textnode import *


def text_node_to_html_node(text_node):
    #if TextType.value not in Enum:
    #    raise Exception("TextType Error: Not a valid type")
    #print(text_node.text_type)
    match text_node.text_type.value:
        case "plain":
            return LeafNode(None, text_node.text)
        case "bold":
            return LeafNode("b", text_node.text)
        case "italic":
            return LeafNode("i", text_node.text)
        case "code":
            return LeafNode("code", text_node.text)
        case "link":
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case "image":
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError(f"invalid text type: {text_node.text_type}")
    
#def split_nodes_delimiter(old_nodes, )