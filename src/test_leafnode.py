import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        
    def test_props_to_html(self):
        props = {
                 "href": "https://www.google.com",
                  "target": "_blank",
            }


        node = LeafNode("p", "Hello, world!", props)
        #print(node.to_html())
        self.assertEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">Hello, world!</p>')

    def test_tag_and_prog_and_value(self):
        props = {
            "href": "https://liibalaaba.com",
            "image": "./boobies.jpg",
            }
        node = LeafNode("a", "blarhg", props)
        self.assertNotEqual(node.to_html(), '<p href="https://www.google.com" target="_blank">Hello, world!</p>')

if __name__ == "__main__":
    unittest.main()