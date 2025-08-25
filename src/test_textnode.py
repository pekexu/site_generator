import unittest

from textnode import TextNode, TextType
from functions import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("url test", TextType.LINK, None)
        node2 = TextNode("url test", TextType.LINK)
        self.assertEqual(node, node2)
    
    def test_uneq_text(self):
        node = TextNode("foo", TextType.ITALIC)
        node2 = TextNode("bar", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_uneq_texttype(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a italic node")

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "https://piupau.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props, {'src': 'https://piupau.com', 'alt': 'This is an image'})
        self.assertNotEqual(html_node.value, "This is a text node")


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
            
if __name__ == "__main__":
    unittest.main()