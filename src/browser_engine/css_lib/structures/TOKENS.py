token_types = [
    "ident-token", "function-token", "at-keyword-token", "hash-token", "string-token", "url-token", "delim-token",
    "number-token", "percentage-token", "dimension-token", "bad-string-token", "bad-url-token", "whitespace-token",
    "CDO-token", "CDC-token", "colon-token", "semicolon-token", "comma-token", "[-token", "]-token", "(-token",
    ")-token", "{-token", "}-token"
]

tokens_with_value_attribute = token_types[:7]
tokens_with_numeric_value_attribute = token_types[7:10]


class Token:
    def __repr__(self):
        return f"<{self.__class__.__name__}>"


def create_token(token_type):
    # ABORT HERE IF TOKEN TYPE IS INVALID
    if token_type not in token_types:
        raise KeyError("Invalid Token Type!")

    # CREATE NEW TOKEN
    new_token_class = type(token_type, (Token,), {})  # DYNAMICALLY CREATES A NEW CLASS WITH Token AS BASE CLASS
    token = new_token_class()  # CREATE INSTANCE OF NEW CLASS

    # MODIFY CLASS INSTANCE VARIABLES ACCORDING TO TOKEN TYPE
    if token_type in tokens_with_value_attribute:
        token.value = ""

    elif token_type in tokens_with_numeric_value_attribute:
        token.value = None

    # ADDITIONAL ATTRIBUTES
    if token_type == "hash-token":
        token.type = "unrestricted"  # DEFAULT TYPE IS UNRESTRICTED AND OTHER IS ID

    if token_type in ["number-token", "dimension-token"]:
        token.type = "integer"  # DEFAULT TYPE IS INTEGER AND OTHER IS NUMBER

    if token_type == "dimension-token":
        token.unit = ""

    return token
