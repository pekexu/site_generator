import unittest

from htmlnode import *

class TestTextNode(unittest.TestCase):
    def test_to_html_with_children(self):
    
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        
        self.assertEqual(
                parent_node.to_html(),
                "<div><span><b>grandchild</b></span></div>",
        )
    def test_with_nesting_and_props(self):
        props = {
            "color": "green",
            "bgcolor": "blue",
            "cols": 7,
        }
        props2 = {
            "magic": "Yes",
            "colorful": "no",
        }


        grandchild = LeafNode("div", "grandchild", props2)
        child1 = ParentNode("span", [grandchild], props2)
        child2 = ParentNode("cspan", [grandchild])
        father = ParentNode("h1", [child1, child2], props2)

        
        self.assertEqual(
            
            father.to_html(), '<h1 magic="Yes" colorful="no"><span magic="Yes" colorful="no"><div magic="Yes" colorful="no">grandchild</div></span><cspan><div magic="Yes" colorful="no">grandchild</div></cspan></h1>'
        )







if __name__ == "__main__":
    unittest.main()