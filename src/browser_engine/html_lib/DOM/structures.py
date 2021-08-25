class OrderedSet:
    # AN ORDERED SET IS A JUST A LIST BUT WITH NO REPEATING ELEMENTS.

    def __init__(self, *args):
        self.data = list(args)
        self._remove_duplicates(list)

    def _remove_duplicates(self, iterable):
        unique_data = []

        for item in iterable:
            item_is_unique = item not in unique_data
            if item_is_unique:
                unique_data.append(item)

        self.data = unique_data

    def append(self, item):
        item_is_unique = item not in self.data
        if item_is_unique:
            self.data.append(item)

    def prepend(self, item):
        item_is_unique = item not in self.data
        if item_is_unique:
            self.data.insert(0, item)

    def replace(self, item, replacement):
        for i in range(len(self.data)):
            current_item = self.data[i]
            if current_item == item:
                self.data[i] = replacement

    def __len__(self):
        return len(self.data)

    def __repr__(self):
        return "OrderedSET(" + str(self.data)[1:-1] + ")"


class Node:
    def __init__(self, node_document):
        self.node_document = node_document

        self.root = self
        self.parent = None
        self.children = OrderedSet()

    def set_parent(self, parent):
        self.parent = parent
        self.root = parent.root

    def add_child(self, child):
        self.children.append(child)

    def __len__(self):
        return len(self.children)


class Document(Node):
    def __init__(self):
        super().__init__(node_document=self)
        self.encoding = "utf8"
        self.content_type = "application/xml"
        self.url = "about:blank"
        self.origin = None
        self.type = "xml"
        self.mode = "no-quirks"

        self.parser_cannot_change_mode = False


class DocumentType(Node):
    def __init__(self, node_document, name):
        super().__init__(node_document)
        self.name = name
        self.public_id = ""
        self.system_id = ""

    def __len__(self):
        return 0


class Element(Node):
    def __init__(self, node_document, namespace, namespace_prefix, local_name, custom_element_state,
                 custom_element_definition, is_value, attributes=None):
        super().__init__(node_document)
        self.namespace = namespace
        self.namespace_prefix = namespace_prefix
        self.local_name = local_name
        self.custom_element_state = custom_element_state
        self.custom_element_definition = custom_element_definition
        self.is_value = is_value

        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes

    def append_attrs_from_token(self, token_attr_list):
        for attr_name, attr_value in token_attr_list:
            self.attributes[attr_name] = attr_value

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, key, value):
        self.attributes[key] = value


class HTMLElement(Node):
    def __init__(self, node_document, attributes=None):
        super().__init__(node_document)
        if attributes is None:
            self.attributes = {}
        else:
            self.attributes = attributes

    def append_attrs_from_token(self, token_attr_list):
        for attr_name, attr_value in token_attr_list:
            self.attributes[attr_name] = attr_value

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, key, value):
        self.attributes[key] = value

    def __len__(self):
        return len(self.children)


class Text(Node):
    def __init__(self, node_document, data=""):
        super().__init__(node_document)
        self.data = data

    def add_child(self, child):
        raise Exception("Text nodes are leaves, cannot contain children.")

    def __len__(self):
        return len(self.data)
