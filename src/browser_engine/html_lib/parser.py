"""
THIS IS THE TREE CONSTRUCTION STAGE AS SPECIFIED IN THE SPECIFICATION HERE:
https://html.spec.whatwg.org/multipage/parsing.html#tree-construction
"""
from src.browser_engine.html_lib.tokenizer import streams
from src.browser_engine.html_lib.DOM import *
from src.browser_engine.html_lib.constants import *


def is_whitespace(string):
    return all([char in WHITESPACE for char in string])


# noinspection PyMethodMayBeStatic
class HTMLParser:
    def __init__(self, token_list):
        self.token_stream = streams.TokenStream(token_list)

        # STATE VARIABLES
        self.insertion_mode = self.initial_mode
        self.original_insertion_mode = None
        self.stack_of_open_elems = []

        # STATE FLAGS
        self.foster_parenting = False  # FOSTER PARENTING OCCURS DUE TO INCORRECT NESTING OF TAGS
        self.created_as_fragment_parser = False  # POSSIBLE BUG: POSSIBLY WRONG IMPLEMENTATION
        self.frameset_ok_flag = True  # True is "ok", False is "not ok" (idk why it's used, defined just for compliance)
        self.parser_cannot_change_mode = False

        # ELEMENT POINTERS
        self.head_pointer = None
        self.last_form_pointer = None  # the last form element that was opened, and has not yet reached it's end tag

        # OUTPUT
        self.document = Document()
        self.errors = 0

    # PROPERTIES
    def current_node(self):
        try:
            return self.stack_of_open_elems[-1]
        except IndexError:
            return None

    def adjusted_current_node(self):
        # TODO: PARTIALLY IMPLEMENTED METHOD
        if self.created_as_fragment_parser:
            context_element = None  # TODO: CONTEXT ELEMENT TO BE IMPLEMENTED WHEN FRAGMENT PARSER IS IMPLEMENTED
            return context_element
        else:
            return self.current_node()

    # ALGORITHMS
    def parse_error(self):
        self.errors += 1

    def appropriate_place_for_node_insertion(self, override_target=None):
        """
        # TODO: COMPLETE appropriate_place_Fore_node_insertion()
        RETURNS A DICT {AN ELEMENT, POSITION TO INSERT INTO ELEMENT'S CHILDREN LIST}

        EXAMPLE: TO INSERT AS THE LAST CHILD OF THE HTML ELEMENT:
        (
            # since first element in this stack is always the html element
            "insertion_node": self.stack_of_open_elems[0],
            "insertion_location": -1
        )
        """
        if override_target is not None:
            target = override_target
        else:
            target = self.current_node()

        if self.foster_parenting and target.type in ["table", "tbody", "tfoot", "thead", "tr"]:
            # STEP 1, 2
            last_template, last_table = None, None
            last_template_position, last_table_position = None, None

            reversed_range_for_open_element_stack = reversed(range(len(self.stack_of_open_elems)))
            for position in reversed_range_for_open_element_stack:
                element = self.stack_of_open_elems[position]

                last_template_found = element.type == "template" and last_template is None
                last_table_found = element.type == "table" and last_table is None

                if last_template_found:
                    last_template = element
                    last_template_position = position
                if last_table_found:
                    last_table = element
                    last_table_position = position

                both_elements_found = last_template is not None and last_table is not None
                if both_elements_found:
                    break

            # STEP 3
            last_template_exists, last_table_exists = last_template is not None, last_table is not None
            template_node_level_higher_than_table = last_template_position > last_table_position
            if last_template_exists and \
                    (not last_table_exists or last_table_exists and template_node_level_higher_than_table):
                raise NotImplementedError

            # STEP 4
            elif not last_table_exists:
                adjusted_insertion_location = {
                    "insertion_node": self.stack_of_open_elems[0],
                    "insertion_location": -1
                }
                return adjusted_insertion_location

            # STEP 5 (is possibly misinterpreted here)
            elif last_table.parent is not None:
                adjusted_insertion_location = {
                    "insertion_node": last_table.parent,
                    "insertion_position": last_table.parent.find_child(last_table) - 1
                }
                return adjusted_insertion_location

            # STEP 6
            else:
                previous_element = self.stack_of_open_elems[last_table_position - 1]
                adjusted_insertion_location = {
                    "insertion_node": previous_element,
                    "insertion_location": -1
                }
        else:
            adjusted_insertion_location = {
                "insertion_node": target,
                "insertion_position": -1
            }

        if adjusted_insertion_location["insertion_node"].type == "template":
            raise NotImplementedError

        return adjusted_insertion_location

    def create_element_for_token(self, token, namespace, intended_parent):
        document = intended_parent.root()
        local_name = token.tag_name
        try:
            is_value = token.attributes["is"]
        except KeyError:
            is_value = None

        definition = self.lookup_custom_element_definition(document, namespace, local_name, is_value)

        will_execute_script = False
        if definition is not None and not self.created_as_fragment_parser:
            will_execute_script = True

        if will_execute_script:
            raise NotImplementedError

        element = self.create_element(document, local_name, namespace, None, is_value, will_execute_script)
        element.attributes = token.attributes

        if will_execute_script:
            raise NotImplementedError

        # POSSIBLE BUG: SKIPPING SEEMINGLY UNNECESSARY STEPS

        return element

    def insert_a_foreign_element(self, token, namespace):
        adjusted_insertion_location = self.appropriate_place_for_node_insertion()
        insertion_node = adjusted_insertion_location["insertion_node"]
        insertion_location = adjusted_insertion_location["insertion_location"]
        element = self.create_element_for_token(token, namespace, insertion_node)

        # POSSIBLE BUG: NOT SURE IF THIS IS THE RIGHT CONDITION FOR THE CLAUSE
        possible_to_insert_at_insertion_location = not (
                insertion_node.type == "document" and len(insertion_node.children) >= 1
        )
        if possible_to_insert_at_insertion_location:
            if not self.created_as_fragment_parser:
                # TODO: IMPLEMENT ELEMENT QUES
                pass

            insertion_node.insert_child(element, insertion_location)

            if not self.created_as_fragment_parser:
                # TODO: IMPLEMENT ELEMENT QUES
                pass

        self.stack_of_open_elems.append(element)
        return element

    def insert_html_element(self, token):
        return self.insert_a_foreign_element(token, HTML_NAMESPACE)

    def adjust_foreign_attributes(self):
        # TODO: IMPLEMENT ADJUST FOREIGN ATTRIBUTES ALGORITHM
        return

    def insert_character(self, data=None):
        if data is None:
            data = self.token_stream.current_token

        adjusted_insertion_location = self.appropriate_place_for_node_insertion()

        insertion_node = adjusted_insertion_location["insertion_node"]
        insertion_location = adjusted_insertion_location["insertion_location"]
        if insertion_node.type == "document":
            return  # function doesn't return anything, just used to abort here

        preceding_element = self.stack_of_open_elems[insertion_location - 1]
        insertion_node_succeeds_text_element = preceding_element.type == "text"
        if insertion_node_succeeds_text_element:
            preceding_element.data += data

        else:
            new_text_node = TextNode(data=data)
            insertion_node.insert_child(new_text_node, insertion_location)  # insert_child(what, where)

    def parse_foreign_content(self):
        token = self.token_stream.next()

        if token.type == "character":
            if token.data == NULL:
                self.parse_error()
                self.insert_character(REPLACEMENT_CHARACTER)

            elif all([char in WHITESPACE for char in token.data]):
                self.insert_character(token.data)

            else:
                self.insert_character(token.data)
                self.frameset_ok_flag = False

        elif token.type == "comment":
            raise NotImplementedError

        elif token.type == "DOCTYPE":
            self.parse_error()
            return  # ignore

        elif token.type == "start tag":
            # POSSIBLE BUGS IN THE IF CLAUSE
            has_expected_font_attrs = all([attr in token.attributes.keys() for attr in ["color", "face", "size"]])
            if token.tag_name in UNACCEPTED_TAGS_IN_FOREIGN_CONTENT or \
                    (token.tag_name == "font" and has_expected_font_attrs):
                self.parse_error()
                current_elem = self.current_node()
                while current_elem not in MATH_ML_TEXT_INTEGRATION_POINTS \
                        or not is_html_integration_point(current_elem) or \
                        current_elem.namespace == HTML_NAMESPACE:
                    self.stack_of_open_elems.pop()

                self.token_stream.reprocessing = True
                return  # parse using the current insertion mode

            else:
                if self.adjusted_current_node().namespace in MATH_ML_NAMESPACE:
                    raise NotImplementedError

                if self.adjusted_current_node().namespace in SVG_NAMESPACE:
                    raise NotImplementedError

                self.adjust_foreign_attributes()

    def parse_generic_rcdata(self, token):
        element = self.insert_html_element(token)

    # EXTRA ALGORITHMS
    # noinspection PyUnusedLocal
    def lookup_custom_element_definition(self, document, namespace, local_name, is_value):
        # TODO: IMPLEMENT LOOKING UP CUSTOM ELEMENT DEFINITIONS
        return None

    def create_element(self, document, local_name, namespace, prefix=None, is_value=None,
                       synchronous_custom_elements_flag=False):
        result = None
        # noinspection PyNoneFunctionAssignment
        definition = self.lookup_custom_element_definition(document, namespace, local_name, is_value)
        # noinspection PyUnresolvedReferences
        definition_represents_custom_element = definition is not None and definition.name != local_name
        if definition_represents_custom_element:
            raise NotImplementedError

        elif definition is not None:
            raise NotImplementedError

        else:
            result = Element()
            result.namespace = namespace
            result.namespace_prefix = prefix
            result.local_name = local_name
            result.custom_element_state = "uncustomized"
            result.custom_element_definition = None
            result.is_value = is_value
        return result

    # MAIN LOOP
    def dispatcher(self):
        conditions_for_parsing_in_current_insertion_mode = [
            len(self.stack_of_open_elems) == 0,
            self.adjusted_current_node().namespace == HTML_NAMESPACE,
            # TODO: SKIPPING SEEMINGLY UNNECESSARY CONDITIONS IN DISPATCHER
            self.token_stream.current_token.type == "eof"
        ]

        if conditions_for_parsing_in_current_insertion_mode:
            self.insertion_mode()
        else:
            self.parse_foreign_content()

    # INSERTION MODES
    def initial_mode(self):
        token = self.token_stream.next()

        if token.type == "character" and token.data in WHITESPACE:
            return  # ignore

        elif token.type == "comment":
            raise NotImplementedError

        elif token.type == "DOCTYPE":
            raise NotImplementedError

        else:
            if self.document.type != "iframe srcdoc":
                self.parse_error()

            if self.parser_cannot_change_mode:
                self.document.mode = "quirks-mode"

            self.insertion_mode = self.before_html
            self.token_stream.reprocessing = True

    def before_html(self):
        token = self.token_stream.next()

        if token.type == "DOCTYPE":
            self.parse_error()
            return  # ignore

        elif token.type == "comment":
            raise NotImplementedError

        elif token.type == "character" and is_whitespace(token.data):
            return  # ignore

        elif token.type == "start tag" and token.tag_name == "html":
            html_element = self.create_element_for_token(token, HTML_NAMESPACE, self.document)
            self.document.append_child(html_element)
            self.stack_of_open_elems.append(html_element)
            self.insertion_mode = self.before_head

        elif token.type == "end tag" and token.tag_name not in ["head", "body", "br"]:
            self.parse_error()
            return  # ignore

        else:
            html_element = self.create_element(self.document, "html", HTML_NAMESPACE)
            html_element.type = "html"
            self.document.append_child(html_element)
            self.stack_of_open_elems.append(html_element)

            self.insertion_mode = self.before_head
            self.token_stream.reprocessing = True

    def before_head(self):
        token = self.token_stream.next()

        if token.type == "character" and is_whitespace(token.data):
            return  # ignore

        elif token.type == "comment":
            raise NotImplementedError

        elif token.type == "start tag" and token.tag_name == "html":
            self.token_stream.reprocessing = True
            self.in_body()

        elif token.type == "start tag" and token.tag_name == "head":
            head_element = self.insert_html_element(token)
            self.head_pointer = head_element

            self.insertion_mode = self.in_head

        elif token.type == "end tag" and token.tag_name not in ["head", "body", "html", "br"]:
            self.parse_error()
            return  # ignore

        else:
            head_element = self.insert_html_element(token)
            self.head_pointer = head_element

            self.insertion_mode = self.in_head
            self.token_stream.reprocessing = True

    def in_head(self):
        token = self.token_stream.next()
        tag_name = token.tag_name
        is_start_tag = token.type == "start tag"

        if token.type == "character" and is_whitespace(token.data):
            self.insert_character(token.data)

        elif token.type == "comment":
            raise NotImplementedError

        elif token.type == "DOCTYPE":
            self.parse_error()
            return  # ignore

        elif is_start_tag and tag_name == "html":
            self.token_stream.reprocessing = True
            self.in_body()

        elif is_start_tag and tag_name in ["base", "basefont", "bgsound", "link"]:
            self.insert_html_element(token)
            self.stack_of_open_elems.pop()

        elif is_start_tag and tag_name == "meta":
            self.insert_html_element(token)
            self.stack_of_open_elems.pop()
            # POSSIBLE BUG: SKIPPED ENCODING HANDLING HERE (SEEMED UNNECESSARY)

        elif is_start_tag and tag_name == "title":


