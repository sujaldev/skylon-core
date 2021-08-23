from src.browser_engine.html_lib.tokens import EOFToken


class InfiniteString(str):
    """
    THIS IS A TYPE OF STRING THAT DOES NOT RAISE INDEX ERRORS,
    INSTEAD IT RETURNS EMPTY STRING WHEN OUT OUT OF INDEX.
    ALSO RETURNS EMTPY STRING WHEN A NEGATIVE INDEX IS ACCESSED.
    """

    def __init__(self, string):
        self.string = string

    def __getitem__(self, index):
        string_length = len(self.string)
        if index in range(string_length):
            return self.string[index]
        else:
            return ""


class InfiniteList:
    """
    THIS IS A TYPE OF LIST THAT DOES NOT RAISE INDEX ERRORS,
    INSTEAD IT RETURNS EOF TOKEN WHEN OUT OUT OF INDEX.
    ALSO RETURNS EOF TOKEN WHEN A NEGATIVE INDEX IS ACCESSED.
    """

    def __init__(self, data):
        self.data = data

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        if index in range(len(self.data)):
            return self.data[index]
        else:
            return EOFToken()


class Stream:
    def __init__(self, source):
        self.source = InfiniteString(source)

        self.index = 0

        # CHARACTERS ARE INITIALIZED AS MENTIONED IN THE SPECIFICATION
        self.current_char = ""  # The HTML Specification doesn't mention a specific initial value for the Current Char
        self.next_char = self.source[self.index]

        # A Flag is used instead of directly calling Stream.reconsume because,
        # A tokenizer state can just set the reconsumption flag and next state can normally call Stream.consume,
        # The Stream.consume will automatically call the reconsume method, so the tokenizer doesn't have to.
        self.reconsuming = False  # (MAKING THE TOKENIZER IMPLEMENTATION MUCH EASIER)

    def is_truly_out_of_index(self):
        # The index could be out of range but processing should continue until no reconsumption is required.
        is_out_of_index = self.index > len(self.source) or len(self.source) == 0
        return is_out_of_index and not self.reconsuming

    def consume(self, step=1):
        if self.reconsuming:
            return self.reconsume()

        self.current_char = self.next_char
        self.index += step
        self.next_char = self.source[self.index]

        return self.current_char, self.next_char

    def reconsume(self):
        self.reconsuming = False
        return self.current_char, self.next_char


class TokenStream:
    def __init__(self, token_list):
        self.token_list = token_list

        self.index = -1
        self.current_token = None

        self.reconsuming = False

    def next(self):
        if self.reconsuming:
            return self.reprocess()

        self.index += 1
        self.current_token = self.token_list[self.index]
        return self.current_token

    def reprocess(self):
        self.reconsuming = False
        return self.current_token

    def is_truly_out_of_index(self):
        is_out_of_index = self.index > len(self.token_list) or len(self.token_list) == 0
        return is_out_of_index and not self.reconsuming
