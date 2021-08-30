"""
THIS IS THE TOKENIZATION STAGE FOR CSS AS DESCRIBE HERE:
https://www.w3.org/TR/css-syntax-3/#tokenizer-algorithms
"""
from src.browser_engine.css_lib.structures.TOKENS import create_token

from src.browser_engine.helpers.preprocessor import preprocess_css
from src.browser_engine.helpers.stream import CharStream
from src.browser_engine.helpers.funcs import inside, is_name_code_point
from src.browser_engine.helpers.CONSTANTS import *


class CSSTokenizer:
    def __init__(self, source):
        # INITIALIZE STREAM
        preprocessed_stream = preprocess_css(source)
        self.stream = CharStream(preprocessed_stream)

        # BUFFERS
        self.current_token = None
        self.errors = 0

    def consume(self, step=1):
        return self.stream.consume(step)

    def parse_error(self):
        self.errors += 1

    def consume_a_token(self):
        # RETURNS A TOKEN OF ANY TYPE

        self.consume_comments()
        current_char, next_char = self.consume()

        if inside(WHITESPACE, current_char):
            while inside(WHITESPACE, current_char):
                current_char = self.consume()[0]

            self.current_token = create_token("whitespace-token")
            return self.current_token

        elif current_char == '"':
            self.current_token = self.consume_a_string_token()
            return self.current_token

        elif current_char == "#":
            second_next_char = self.stream.nth_next_char()
            if is_name_code_point(next_char) or self.is_valid_escape(next_char, second_next_char):
                self.current_token = create_token("hash-token")
                third_next_char = self.stream.nth_next_char(2)
                if self.three_code_points_start_an_identifier(next_char, second_next_char, third_next_char):
                    self.current_token.type = "id"

                self.current_token.value = self.consume_a_name()
                return self.current_token
            else:
                self.current_token = create_token("delim-token")
                self.current_token.value = current_char
                return self.current_token

        elif current_char == "'":
            self.current_token = self.consume_a_string_token()
            return self.current_token

        elif current_char == "(":
            self.current_token = create_token("(-token")
            return self.current_token

        elif current_char == ")":
            self.current_token = create_token(")-token")
            return self.current_token

        elif current_char == "+":
            if self.three_code_points_start_a_number():
                self.stream.reconsuming = True
                self.current_token = self.consume_a_numeric_token()
                return self.current_token
            else:
                self.current_token = create_token("delim-token")
                self.current_token.value = current_char
                return self.current_token

        elif current_char == ",":
            self.current_token = create_token("comma-token")
            return self.current_token

        elif current_char == "-":
            # NEGATIVE NUMBER
            if self.three_code_points_start_a_number():
                self.stream.reconsuming = True
                self.current_token = self.consume_a_numeric_token()
                return self.current_token

            # COMMENT DATA CLOSE (CDC) -->
            elif (next_char, self.stream.nth_next_char()) == ("-", ">"):
                self.consume(2)
                self.current_token = create_token("CDC-token")
                return self.current_token

            elif self.three_code_points_start_an_identifier():
                self.stream.reconsuming = True
                self.current_token = self.consume_ident_like_token()
                return self.current_token

            else:
                self.current_token = create_token("delim-token")
                self.current_token.value = current_char
                return self.current_token

        elif current_char == ".":
            if self.three_code_points_start_a_number():
                self.stream.reconsuming = True
                self.current_token = self.consume_a_numeric_token()
                return self.current_token

            else:
                self.current_token = create_token("delim-token")
                self.current_token.value = current_char
                return self.current_token

        elif current_char == ":":
            self.current_token = create_token("colon-token")
            return self.current_token

        elif current_char == ";":
            self.current_token = create_token("semicolon-token")
            return self.current_token

        elif current_char == "<":
            second_next_char = self.stream.nth_next_char()
            third_next_char = self.stream.nth_next_char(2)
            is_comment_start = (next_char, second_next_char, third_next_char) == ("!", "-", "-")
            if is_comment_start:
                self.consume(3)
                self.current_token = create_token("CDO-token")
                return self.current_token

            else:
                self.current_token = create_token("delim-token")
                self.current_token.value = current_char
                return self.current_token

        elif current_char == "@":
            second_next_char = self.stream.nth_next_char()
            third_next_char = self.stream.nth_next_char(2)
            if self.three_code_points_start_an_identifier(next_char, second_next_char, third_next_char):
                self.current_token = create_token("at-keyword-token")
                self.current_token.value = self.consume_a_name()
                return self.current_token

            else:
                self.current_token = create_token("delim-token")
                self.current_token.value = current_char
                return self.current_token

        elif current_char == "[":
            self.current_token = create_token("[-token")
            return self.current_token

        elif current_char == "\\":
            if self.two_code_points_are_valid_escape():
                self.stream.reconsuming = True
                self.current_token = self.consume_ident_like_token()
                return self.current_token

            else:
                self.parse_error()
                self.current_token = create_token("delim-token")
                self.current_token.value = current_char
                return self.current_token

        elif current_char == "]":
            self.current_token = create_token("]-token")
            return self.current_token

        elif current_char == "{":
            self.current_token = create_token("{-token")
            return self.current_token

        elif current_char == "}":
            self.current_token = create_token("}-token")
            return self.current_token

        elif inside(ASCII_DIGIT, current_char):
            self.stream.reconsuming = True
            self.current_token = self.consume_a_numeric_token()
            return self.current_token

        elif is_name_code_point(current_char):
            self.stream.reconsuming = True
            self.current_token = self.consume_ident_like_token()
            return self.current_token

        elif current_char == EOF:
            self.current_token = create_token("EOF-token")
            return self.current_token

        else:
            self.current_token = create_token("delim-token")
            self.current_token.value = current_char
            return self.current_token

    def consume_comments(self):
        next_char, next_next_char = self.stream.next_char, self.stream.nth_next_char()
        is_comment_start = (next_char, next_next_char) == ("/", "*")
        if is_comment_start:
            self.consume(2)
            while True:
                next_char, next_next_char = self.stream.next_char, self.stream.nth_next_char()
                is_comment_end = (next_char, next_next_char) == ("*", "/")
                eof_reached = self.stream.is_truly_out_of_index()
                if is_comment_end:
                    self.consume(2)
                    print("hola")
                    if not eof_reached:
                        self.consume_comments()
                    return
                elif eof_reached:
                    print("here")
                    self.parse_error()
                    self.consume(2)
                    return
                self.consume()

