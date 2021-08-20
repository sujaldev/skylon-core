class DOCTYPEToken:
    def __init__(self):
        self.type = "DOCTYPE"

        self.name = "missing"
        self.public_identifier = "missing"
        self.system_identifier = "missing"
        self.force_quirks_flag = False

    def emit(self, output_buffer, err_buffer):
        output_buffer.append(self)
        return self

    def __repr__(self):
        token_repr = f'<!DOCTYPE {self.name} PUBLIC "{self.public_identifier}" "{self.system_identifier}">'
        return token_repr


class StartTagToken:
    def __init__(self, tag_name=""):
        self.type = "start tag"

        self.tag_name = tag_name
        self.self_closing_flag = False
        self.attributes = {}

        self.current_attr = (None, None)

        self.errors = []

    def emit(self, output_buffer, err_buffer):
        output_buffer.append(self)
        for err in self.errors:
            err_buffer.append(err)
        return self

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, key, value):
        if key not in self.attributes.keys():
            self.attributes[key] = value
        else:
            self.errors.append("DUPLICATE ATTRIBUTE")
        self.current_attr = (key, value)

    def __repr__(self):
        attributes = ""
        for attr_name, attr_val in self.attributes.items():
            attributes += f' {attr_name}="{attr_val}"'

        self_ending = "/" if self.self_closing_flag else ""

        token_repr = "<" + self.tag_name + attributes + self_ending + ">"
        return token_repr


class EndTagToken:
    def __init__(self, tag_name=""):
        self.type = "end tag"

        self.tag_name = tag_name
        self.self_closing_flag = False
        self.attributes = {}

        self.current_attr = (None, None)

        self.errors = []

    def emit(self, output_buffer, err_buffer):
        has_attributes = len(self.attributes.keys()) != 0
        has_trailing_solidus = self.self_closing_flag

        if has_attributes:
            self.errors.append("END TAG WITH ATTRIBUTES")
        if has_trailing_solidus:
            self.errors.append("END TAG WITH TRAILING SOLIDUS")

        output_buffer.append(self)
        for err in self.errors:
            err_buffer.append(err)
        return self

    def __getitem__(self, item):
        return self.attributes[item]

    def __setitem__(self, key, value):
        if key not in self.attributes.keys():
            self.attributes[key] = value
        else:
            self.errors.append("DUPLICATE ATTRIBUTE")
        self.current_attr = (key, value)

    def __repr__(self):
        attributes = ""
        for attr_name, attr_val in self.attributes.items():
            attributes += f' {attr_name}="{attr_val}"'

        self_ending = "/" if self.self_closing_flag else ""

        token_repr = "</" + self.tag_name + attributes + self_ending + ">"
        return token_repr


class CommentToken:
    def __init__(self, data=""):
        self.type = "comment"

        self.data = data

    def emit(self, output_buffer, err_buffer):
        output_buffer.append(self)
        return self

    def __repr__(self):
        return f"<!--{self.data}-->"


class CharacterToken:
    def __init__(self, data=""):
        self.type = "character"

        self.data = data

    def emit(self, output_buffer, err_buffer):
        last_token = output_buffer[-1]
        if last_token.type == "character":
            output_buffer[-1].data += self.data
        else:
            output_buffer.append(self)
        return self

    def __repr__(self):
        return f"<!--{self.data}-->"


class EOFToken:
    def __init__(self):
        self.type = "EOF"

    def emit(self, output_buffer, err_buffer):
        output_buffer.append(self)
        return self

    def __repr__(self):
        return "<EOF>"
