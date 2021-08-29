from src.browser_engine.helpers.CONSTANTS import WHITESPACE


def is_whitespace(string):
    return all([char in WHITESPACE for char in string])


def inside(constant, char):
    """
    NORMALLY THE STATEMENT "" in "any_string" WILL RETURN TRUE, THIS FUNCTION AVOIDS THAT
    READ AS: "IF INSIDE CONSTANT IS CHAR"
    """

    if char != "":
        return char in constant
    else:
        return False
