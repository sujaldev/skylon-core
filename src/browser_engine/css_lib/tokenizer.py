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

    def consume(self, step=1):
        return self.stream.consume(step)

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
