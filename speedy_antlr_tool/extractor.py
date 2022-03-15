import re
import os
import importlib.util
from typing import List

import antlr4
import inspect

from .objects import ContextData


def get_parser_class(parser_path:str) -> antlr4.Parser:
    """
    Given the path to the parser file, finds the antlr Parser class
    """
    # Import the parser module
    spec = importlib.util.spec_from_file_location("ParserModule", parser_path)
    ParserModule = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ParserModule)

    # Find the parser class
    for obj in ParserModule.__dict__.values():
        if isinstance(obj, type) and issubclass(obj, antlr4.Parser) and (obj.__module__ == ParserModule.__name__):
            return obj
    raise RuntimeError("Could not find parser class")


def iter_rule_context_classes(parser_cls:antlr4.Parser):
    """
    Given the main parser class, iterate through all the ParserRuleContext classes
    """
    for obj in parser_cls.__dict__.values():
        # Detect ParserRuleContext classes
        if not (isinstance(obj, type) and issubclass(obj, antlr4.ParserRuleContext)):
            continue

        yield obj


def get_rule_labels(context_cls:antlr4.ParserRuleContext) -> List[str]:
    """
    Given a ParserRuleContext class, return a list of token/context labels

    Returns a list of labels
    """

    # Parse the class's __init__ function
    init_func = context_cls.__init__

    # Detect any context/token labels from the init function's assignments
    # Conveniently, the type name is provided as a comment
    lines, _ = inspect.getsourcelines(init_func)
    labels = []
    for line in lines:
        m = re.match(r'self\.(\w+)\s*=\s*None', line.strip())
        if m and not m.group(1).startswith("_"):
            labels.append(m.group(1))

    return labels


def get_context_data(context_cls:antlr4.ParserRuleContext) -> ContextData:
    """
    Given a ParserRuleContext class, extract information about it and return a
    ContextData object
    """

    if antlr4.ParserRuleContext in context_cls.__bases__:
        # Is a pure rule context
        ctx_classname = context_cls.__name__
        label_ctx_classname = None
    else:
        # Is a labeled sub-context
        ctx_classname = context_cls.__bases__[0].__name__
        label_ctx_classname = context_cls.__name__

    labels = get_rule_labels(context_cls)

    is_label_parent = bool(context_cls.__subclasses__())

    return ContextData(ctx_classname, label_ctx_classname, is_label_parent, labels)


def extract(parser_path:str) -> List[ContextData]:
    parser_cls = get_parser_class(parser_path)

    parser_basename = os.path.splitext(os.path.basename(parser_cls.grammarFileName))[0]

    cds = []
    for context_cls in iter_rule_context_classes(parser_cls):
        cds.append(get_context_data(context_cls))

    return cds, parser_basename
