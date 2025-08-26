from htmlnode import *
from textnode import *
from blocktype import BlockType
import re
import os

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
                if not split_text[i] == "":
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
        #print(node.text_type)
        if node.text_type!=TextType.TEXT:
            new_nodes.append(node)
            continue
        current_text = node.text
        matches = extract_markdown_links(node.text)
        if not matches:
            new_nodes.append(TextNode(node.text, node.text_type))
            continue
        for i in range(0, len(matches)):
            
            link_text = matches[i][0]
            url_text = matches[i][1]
            textpart = current_text.split(f"[{link_text}]({url_text})", 1)
            
            if not textpart[0] == "":
                new_nodes.append(TextNode(textpart[0], TextType.TEXT))
                
            new_nodes.append(TextNode(link_text, TextType.LINK, url_text))
            current_text = textpart[1]
        if not current_text == "":
            new_nodes.append(TextNode(current_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    
    node = TextNode(text, TextType.TEXT)
    modified = split_nodes_delimiter([node], "**", TextType.BOLD)
    modified = split_nodes_delimiter(modified, "_", TextType.ITALIC)
    modified = split_nodes_delimiter(modified, "`", TextType.CODE)
    modified = split_nodes_image(modified)
    modified = split_nodes_link(modified)    
    return modified

def markdown_to_blocks(markdown):
    new_list = []
    blocks = re.split(r'\n\s*\n', markdown)
    for block in blocks:
        block = block.strip("\n").lstrip().rstrip()
        if not block == "":
            new_list.append(block)
    return new_list

def block_to_block_type(markdown):
    if markdown.startswith("#"):
        return BlockType.HEADING
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif markdown.startswith(">"):
        for mark in markdown.split("\n"):
            if not mark.startswith(">"):
                return BlockType.PARAGRAPH
            else:
                return BlockType.QUOTE
    elif markdown.startswith("-"):
        for mark in markdown.split("\n"):
            if not mark.startswith("-"):
                return BlockType.PARAGRAPH
            else:
                return BlockType.UNORDERED_LIST
            
    elif markdown.startswith("1."):
        i=1
        for mark in markdown.split("\n"):
            
            if not mark.startswith(f"{i}."):
                return BlockType.PARAGRAPH
            else:
                ol_bool = True
            i+=1
        if ol_bool == True:
            return BlockType.ORDERED_LIST
    else:    
        return BlockType.PARAGRAPH
    
def markdown_to_html_node(markdown):
    newblock_list = []
    blocks = markdown_to_blocks(markdown)
    
    for block in blocks:
        
        current_type = block_to_block_type(block)
        #create children because match case
        if not current_type == BlockType.CODE:
            children = text_to_children(block)
        
        match current_type:
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                paragraph_text = " ".join(lines)
                children = text_to_children(paragraph_text)
                NewBlock = ParentNode("p", children)
            case BlockType.HEADING:
                heading = heading_to_html(block)
                children = text_to_children(block[heading + 1:])
                NewBlock = ParentNode(f"h{heading}", children)
            case BlockType.CODE:
                child = TextNode(block.lstrip("```\n").rstrip("```"), TextType.CODE)
                children = text_node_to_html_node(child)
                NewBlock = ParentNode("pre", [children])
            case BlockType.QUOTE:
                lines = block.split("\n")
                temp = []
                for line in lines:
                    temp.append(line.lstrip("> "))     
                paragraph_text = " ".join(temp)
                children = text_to_children(paragraph_text)
                NewBlock = ParentNode("blockquote", children)
            case BlockType.UNORDERED_LIST:
                lines = block.split("\n")
                temp = []
                for line in lines:
                    text = line[2:]
                    children = text_to_children(text)
                    temp.append(ParentNode("li", children))
                NewBlock = ParentNode("ul", temp)
            case BlockType.ORDERED_LIST:
                lines = block.split("\n")
                temp = []
                for line in lines:
                    text = line[3:]
                    children = text_to_children(text)
                    temp.append(ParentNode("li", children))
                NewBlock = ParentNode("ol", temp)
        newblock_list.append(NewBlock)
    ReturnBlock = ParentNode("div",newblock_list)
    return ReturnBlock
                
def text_to_children(text):
    children = []
    md_blocks = markdown_to_blocks(text)
    for block in md_blocks:
        textnode = text_to_textnodes(block)
        for node in textnode:
            html_node = text_node_to_html_node(node)
            children.append(html_node)
    return children

def heading_to_html(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"Invalid heading: no text content")
    return level

def extract_title(markdown):

    capture_string = f"(?<=# ).*"
    header = re.search(capture_string, markdown)
    return(header[0])


