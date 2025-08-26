from textnode import TextNode, TextType
from file_system_func import *
from functions import *
# hello world

def main():
    copy_static_to_public("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")
main()

