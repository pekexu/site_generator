import unittest

from htmlnode import HTMLNode

class TestTextNode(unittest.TestCase):


    def test_eq(self):
        props = {
            "href": "https://www.google.com",
            "target": "_blank",
        }
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), " href=\"https://www.google.com\" target=\"_blank\"")
        
    def test_eq2(self):
        props = {
            "bgcolor": "white",
            "rows": 3,
            "columns": 5,
            "size": 6,
            "title": "Masters of the universe"
        }
        node = HTMLNode(None, None, None, props)
        self.assertEqual(node.props_to_html(), " bgcolor=\"white\" rows=\"3\" columns=\"5\" size=\"6\" title=\"Masters of the universe\"")

    def test_eq3(self):
        props = {
            None: None
        }
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()