from textnode import TextNode, TextType
from file_system_func import *
from functions import *
# hello world

def main():
    copy_src_to_dst("static", "public")
    generate_pages_recursively("content", "template.html", "public")
main()

