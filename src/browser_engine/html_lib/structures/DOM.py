from src.browser_engine.html_lib.CONSTANTS import HTML_NAMESPACE


class Node:
    def __init__(self, tag_name=None):
        self.type = tag_name  # <tag_name>
        self.data = None  # <tag_name>data</tag_name>
        self.attributes = {}  # <tag_name attr_key=attr_val>
        self.namespace = HTML_NAMESPACE  # elements not defining a namespace are by default in the html namespace

        self.parent = None
        self.children = []

    def root(self):
        """:returns tree root"""
        if self.parent is None:
            return self
        else:
            return self.parent.root()

    def append_child(self, child):
        child.parent = self
        self.children.append(child)

    def insert_child(self, child, position):
        child.parent = self
        self.children.insert(position, child)

    def find_child(self, child):
        return self.children.index(child)

    def __repr__(self):
        return f"<{self.__class__.__name__} type={self.type}>"


class Document(Node):
    def __init__(self):
        super().__init__("Document")
        self.encoding = "utf-8"
        self.content_type = "application/xml"
        self.url = "about:blank"
        self.origin = None
        self.type = "xml"
        self.mode = "no-quirks"


class Element(Node):
    def __init__(self, tag_name=None):
        super().__init__(tag_name)
        self.namespace_prefix = None
        self.local_name = None
        self.custom_element_state = None
        self.custom_element_definition = None
        self.is_value = None


class TextNode(Node):
    def __init__(self, data=""):
        super().__init__("text")
        self.data = data
