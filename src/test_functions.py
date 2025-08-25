import unittest

from textnode import TextNode, TextType
from functions import *

class TestTextNode(unittest.TestCase):

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.props, {"href": "https://"})
        self.assertEqual(html_node.value, "This is a link")

    def test_delimiter(self):
        node = TextNode("This is text with a **bold block** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes,[TextNode("This is text with a ", TextType.TEXT), TextNode("bold block", TextType.BOLD), TextNode(" word", TextType.TEXT)])

    def test_no_delimiter(self):
        node = TextNode("This has no bolding", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This has no bolding", TextType.TEXT)])

    def test_multiple_delimiters(self):
        node = TextNode("a **b** c **d** e", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            new_nodes,
            [
                TextNode("a ", TextType.TEXT),
                TextNode("b", TextType.BOLD),
                TextNode(" c ", TextType.TEXT),
                TextNode("d", TextType.BOLD),
                TextNode(" e", TextType.TEXT),
            ]
        )
        
    def test_odd_delimiters(self):
        node = TextNode("bad **markdown", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "A link [to the past](https://www.youtube.com) and [to the future](www.boot.dev)"
        )
        self.assertEqual([("to the past", "https://www.youtube.com"),("to the future", "www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )
    def test_one_image(self):
        node = TextNode("One image ![image](https://boot.dev/poop.jpg)", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("One image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://boot.dev/poop.jpg"),
            ],
            new_nodes,
        )


    def test_text_after_image(self):
        node = TextNode("One image ![image](https://boot.dev/poop.jpg) and some text", TextType.TEXT,)
        new_nodes = split_nodes_image([node])
        
        self.assertListEqual(
            [
                TextNode("One image ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://boot.dev/poop.jpg"),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_just_image(self):
        node = TextNode("![image](https://boot.dev/poop.jpg) and some text", TextType.TEXT,)
        new_nodes = split_nodes_image([node])     
        self.assertListEqual(
            [
                
                TextNode("image", TextType.IMAGE, "https://boot.dev/poop.jpg"),
                TextNode(" and some text", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_single_link_middle(self):
        node = TextNode(
            "This is text with a [link to Boot.dev](https://www.boot.dev).", TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link to Boot.dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(".", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_multiple_links(self):
        node = TextNode(
                    "Check out [Google](https://www.google.com) and also [DuckDuckGo](https://duckduckgo.com) for search.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Check out ", TextType.TEXT),
                TextNode("Google", TextType.LINK, "https://www.google.com"),
                TextNode(" and also ", TextType.TEXT),
                TextNode("DuckDuckGo", TextType.LINK, "https://duckduckgo.com"),
                TextNode(" for search.", TextType.TEXT),
            ],
            new_nodes,
        )    
    def test_no_links(self):
        node = TextNode(
                    "Plain text with no links.",
                TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Plain text with no links.", TextType.TEXT),
            ],
            new_nodes,
        )    

    def test_link_at_end_and_begin(self):
        node = TextNode(
                "[Start Link](https://start.com) text in middle [End Link](https://end.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Start Link", TextType.LINK, "https://start.com"),
                TextNode(" text in middle ", TextType.TEXT),
                TextNode("End Link", TextType.LINK, "https://end.com"),
                
            ],
            new_nodes,
        )    
    def test_text_to_nodes(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            TextType.TEXT,)
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            new_nodes,
            [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            
        )
    def test_no_markdown(self):
        nodes = text_to_textnodes("just plain text here!")
        assert len(nodes) == 1
        assert nodes[0].text == "just plain text here!"
        assert nodes[0].text_type == TextType.TEXT
        assert nodes[0].url is None

    def test_multi_bold_and_ita(self):
        node = TextNode("**this** **text** **is** _very_ _itaboldic_", TextType.TEXT)
        new_nodes = text_to_textnodes(node.text)
        self.assertListEqual(
            new_nodes,
            [
                    TextNode("this", TextType.BOLD),
                    TextNode(" ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" ", TextType.TEXT),
                    TextNode("is", TextType.BOLD),
                    TextNode(" ", TextType.TEXT),
                    TextNode("very", TextType.ITALIC),
                    TextNode(" ", TextType.TEXT),
                    TextNode("itaboldic", TextType.ITALIC),

            ],
            
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )
    def test_two_blocks(self):
        md = """
First block.

Second block.
"""
        expected = [
        "First block.",
        "Second block."
        ]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_leading_and_trailing_whitespace(self):
        md = """

        First block with leading whitespace.
    
        Second block after lots of space.  
    
"""
        expected = ["First block with leading whitespace.", "Second block after lots of space."]
        self.assertEqual(expected, markdown_to_blocks(md))

    def test_excessive_blank_lines(self):
        md = "Block one.\n\n\n\nBlock two."
        expected = ["Block one.", "Block two."]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_single_block(self):
        md = "Only one block"
        expected = ["Only one block"]
        self.assertEqual(markdown_to_blocks(md), expected)

    def test_empty_string(self):
        md = ""
        expected = []
        self.assertEqual(markdown_to_blocks(md), expected)



if __name__ == "__main__":
    unittest.main()