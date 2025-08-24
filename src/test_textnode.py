import unittest

from textnode import TextNode, TextType


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

if __name__ == "__main__":
    unittest.main()