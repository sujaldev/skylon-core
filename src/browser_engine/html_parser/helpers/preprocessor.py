"""
THIS MODULE REMOVES UNNECESSARY CHARACTERS FROM THE HTML STREAM

THE SPECIFICATION FOR PREPROCESSING HTML IS DEFINED HERE:
https://html.spec.whatwg.org/multipage/parsing.html#preprocessing-the-input-stream
"""
from src.browser_engine.html_parser.helpers.constants import *


# TODO: IMPLEMENT HTML PREPROCESSOR NON CHAR HANDLING
def handle_non_char():
    pass


# TODO: IMPLEMENT HTML PREPROCESSOR NON CONTROL CHAR HANDLING
def handle_control_chars():
    pass


def normalize_newlines(source):
    normalized = source.replace(CARRIAGE_RETURN + NEWLINE, NEWLINE).replace(CARRIAGE_RETURN, NEWLINE)
    return normalized


def preprocess(stream):
    handle_non_char()
    handle_control_chars()
    processed_stream = normalize_newlines(stream)
    return processed_stream
