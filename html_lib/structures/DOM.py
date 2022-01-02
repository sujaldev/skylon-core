class Node:
    def __init__(self, tag, parent=None):
        self.tag = tag
        self.parent = parent
        self.children = []

    def show_tree(self, tab=0):
        prompt = "├──" + "┼──" * tab + " "
        print(prompt + str(self))
        for child in self.children:
            child.show_tree(tab=tab + 1)

    def __repr__(self):
        return self.tag.__repr__()


class Document(Node):
    pass


class Element(Node):
    pass


class TextNode(Node):
    def __repr__(self):
        if not self.tag.data.isspace():
            return '"' + self.tag.data + '"'
        else:
            return '""'
