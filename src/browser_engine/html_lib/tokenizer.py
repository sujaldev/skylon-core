"""
THE TOKENIZER BREAKS DOWN A SOURCE STREAM OF CHARACTERS INTO TOKENS. A TOKEN CAN BE A GROUP OF CHARACTERS,
THAT TOGETHER HAVE A SPECIAL MEANING IN THAT LANGUAGE.
FOR EXAMPLE THE SENTENCE "A BROWN CAT" COULD BE TOKENIZED AS:
[<A, ARTICLE>, <BROWN, ADJECTIVE>, <CAT, NOUN>]

IF A LANGUAGE'S VOCABULARY CAN BE DEFINED WITH REGULAR EXPRESSIONS, IT IS A CONTEXT FREE GRAMMAR.
PARSING SUCH LANGUAGES IS EASIER. HTML IS NOT SUCH A LANGUAGE AND HAS TO PARSED BY WHAT'S CALLED
A STATE MACHINE. THE STATE MACHINE TO TOKENIZE HTML IS DESCRIBE HERE:
https://html.spec.whatwg.org/multipage/parsing.html#tokenization
"""
from src.browser_engine.html_lib.constants import *
from src.browser_engine.html_lib import preprocessor, tokenizer_stream


class HTMLTokenizer:
    def __init__(self, source):
        # INITIALIZE STREAM
        preprocessed_stream = preprocessor.preprocess(source)
        self.stream = tokenizer_stream.Stream(preprocessed_stream)

        # TOKENIZER STATE
        self.state = self.data_state  # DATA STATE IS THE DEFAULT STATE AS MENTIONED IN THE SPECIFICATION

        # TOKENIZER OUTPUT
        self.output = []  # STATES KEEP APPENDING PROCESSED TOKENS IN THIS LIST

    def data_state(self):
        pass

    def tokenize(self):
        while not self.stream.is_truly_out_of_index():
            self.state()
