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
                TextType("link to Boot.dev", TextType.LINK, "https://www.boot.dev"),
            ]
        )



if __name__ == "__main__":
    unittest.main()