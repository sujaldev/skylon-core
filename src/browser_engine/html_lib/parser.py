"""
THIS IS THE TREE CONSTRUCTION STAGE AS SPECIFIED IN THE SPECIFICATION HERE:
https://html.spec.whatwg.org/multipage/parsing.html#tree-construction
"""
from src.browser_engine.html_lib.tokenizer import streams
from src.browser_engine.html_lib.DOM.algorithms import *
from src.browser_engine.html_lib.DOM.structures import *
from src.browser_engine.html_lib.constants import *


def create_html_element(element_name, node_document, attributes=None):
    element = type(element_name, (HTMLElement,), {})
    element.__init__(node_document, attributes)
    return element


class HTMLParser:
    def __init__(self, token_list):
        self.token_stream = streams.TokenStream(token_list)

        # STATE VARIABLES
        self.insertion_mode = self.initial_mode
        self.original_insertion_mode = None
        self.stack_of_open_elems = []

        # STATE FLAGS
        self.foster_parenting = False

        # OUTPUT
        self.document = Document()
        self.errors = 0

        self.current_token = None

    # DOM ALGORITHMS
    def generate_parse_error(self):
        self.errors += 1

    def reprocess_token_using(self, special_insertion_mode):
        self.token_stream.reprocessing = True
        special_insertion_mode()

    def current_node(self):
        try:
            return self.stack_of_open_elems[-1]
        except IndexError:
            return None

    def appropriate_place_for_inserting_node(self, override_target=None):
        if override_target is None:
            target = self.current_node()
        else:
            target = override_target

        if self.foster_parenting and type(target) in ["table", "tbody", "tfoot", "thead", "tr"]:
            raise NotImplementedError

        else:
            last_index_in_targets_children_list = len(target.children)
            adjusted_insertion_location = (target, last_index_in_targets_children_list)

        


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
                self.generate_parse_error()

            if not self.document.parser_cannot_change_mode:
                self.document.mode = "quirks"

            self.insertion_mode = self.before_html_mode
            self.token_stream.reprocessing = True

    def before_html_mode(self):
        token = self.token_stream.next()

        if token.type == "DOCTYPE":
            self.generate_parse_error()
            return  # ignore

        elif token.type == "comment":
            raise NotImplementedError

        elif token.type == "character" and token.data in WHITESPACE:
            return  # ignore

        elif token.type == "start tag" and token.tag_name == "html":
            element = create_element_for_token(token, HTML_NAMESPACE, self.document)
            element.type = "html"
            self.document.add_child(element)
            self.insertion_mode = self.before_head_mode

        elif token.type == "end tag" and token.tag_name not in ["head", "body", "html", "br"]:
            self.generate_parse_error()
            return  # ignore

        else:
            element = create_html_element("html", self.document)
            self.document.add_child(element)
            self.stack_of_open_elems.append(element)

            self.insertion_mode = self.before_head_mode
            self.token_stream.reprocessing = True

    def before_head_mode(self):
        token = self.token_stream.next()

        if token.type == "character" and token.data in WHITESPACE:
            return  # ignore

        elif token.type == "comment":
            raise NotImplementedError

        elif token.type == "DOCTYPE":
            self.generate_parse_error()
            return  # ignore

        elif token.type == "start tag" and token.tag_name == "html":
            self.reprocess_token_using(self.in_body_mode)

        elif token.type == "start tag" and token.tag_name == "head":

    def process_tokens(self):
        while not self.token_stream.is_truly_out_of_index():
            self.current_token = self.token_stream.next()

            # TREE CONSTRUCTION DISPATCHER CONDITIONS (AS DESCRIBED IN THE SPECS)
            stack_of_open_elems_is_empty = len(self.stack_of_open_elems) == 0
            eof_token_reached = self.token_stream.current_token

            if stack_of_open_elems_is_empty or eof_token_reached:
                self.insertion_mode()
            else:
                raise NotImplementedError
