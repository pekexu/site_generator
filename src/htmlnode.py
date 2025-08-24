class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag              #html tag; <p>, <h1> etc.
        self.value = value          #text inside
        self.children = children    #HTMLNode objects
        self.props = props          #dictionary representing attributes of a html tag

    def to_html(self):
        raise NotImplementedError("to_html method not implemented")
    
    def props_to_html(self):
        prop_str = []
        if self.props:
            for prop in self.props:
                prop_str.append(f" {prop}=\"{self.props[prop]}\"")
        return "".join(prop_str)
    
    def __repr__(self):
        return f"HTMLNode: tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"
    
class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == None:
            raise ValueError
        if self.tag == None:
            return self.value
        #convert tag to html tag:
        
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode: tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
    
    def to_html(self):
        
        if not self.tag:
            raise ValueError("Invalid HTML: no tag")
        if not self.children:
            raise ValueError("Invalid HTML: no children")
        return_string = ""
        for child in self.children:
            return_string = return_string + child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{return_string}</{self.tag}>"
    
    def __repr__(self):
        return f"ParentNode: tag: {self.tag}, value: {self.value}, children: {self.children}, props: {self.props}"
