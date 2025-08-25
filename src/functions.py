from htmlnode import *
from textnode import *
import re

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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        matches = extract_markdown_images(node.text)
        if not matches:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        for i in range(0, len(matches)):
            
            alt_text = matches[i][0]
            url_text = matches[i][1]
            textpart = current_text.split(f"![{alt_text}]({url_text})", 1)
            if not textpart[0] == "":
                new_nodes.append(TextNode(textpart[0], TextType.TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url_text))
            current_text = textpart[1]
        if not current_text == "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        current_text = node.text
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        for i in range(0, len(matches)):
            
            alt_text = matches[i][0]
            url_text = matches[i][1]
            textpart = current_text.split(f"[{alt_text}]({url_text})", 1)

            if not textpart[0] == "":
                new_nodes.append(TextNode(textpart[0], TextType.TEXT))
                
            new_nodes.append(TextNode(alt_text, TextType.LINK, url_text))
            current_text = textpart[1]
        if not current_text == "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes