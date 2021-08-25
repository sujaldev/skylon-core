from src.browser_engine.html_lib.constants import *
from src.browser_engine.html_lib.DOM.structures import Element


def look_up_custom_element_definition(document, namespace, local_name, is_value):
    if namespace != HTML_NAMESPACE:
        return None

    # TODO: IMPLEMENT ALL OTHER CASES FOR LOOKING UP CUSTOM ELEMENT DEFINITION

    return None


def is_valid_custom_element_name(name):
    # TODO: IMPLEMENT CUSTOM ELEMENT NAME VALIDATOR
    return False


# noinspection PyNoneFunctionAssignment
def create_element(document, local_name, namespace, prefix=None, is_value=None, synchronous_element_flag=None):
    result = None
    definition = look_up_custom_element_definition(document, namespace, local_name, is_value)

    if definition is not None and definition.name != local_name:
        raise NotImplementedError

    elif definition is not None:
        raise NotImplementedError

    else:
        result = Element(document, namespace, prefix, local_name, "uncustomized", None, is_value)
        if namespace == HTML_NAMESPACE and (is_valid_custom_element_name(local_name) or is_value is not None):
            result.custom_element_state = "undefined"

    return result


# noinspection PyNoneFunctionAssignment
def create_element_for_token(token, namespace, intended_parent, fragment_case=False):
    document = intended_parent.node_document
    local_name = token.tag_name
    try:
        is_value = token["is"]
    except KeyError:
        is_value = None
    definition = look_up_custom_element_definition(document, namespace, local_name, is_value)

    will_execute = definition is not None and not fragment_case

    if will_execute:
        raise NotImplementedError

    element = create_element(document, local_name, namespace, None, is_value, True if will_execute else None)
    element.append_attrs_from_token(token.attrib)

    # TODO: CREATE ELEMENT FOR TOKENS HAS SKIPPED STEPS HERE, COMPLETE THEM
    return element
