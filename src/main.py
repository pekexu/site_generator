from textnode import TextNode, TextType
from file_system_func import *
from functions import *
from sys import argv

def main():
    if not argv[1]:
        basepath = "/"
    else:
        basepath = argv[1]
    
    copy_src_to_dst("static", "public")
    generate_pages_recursively("content", "template.html", "docs", basepath)

main()

