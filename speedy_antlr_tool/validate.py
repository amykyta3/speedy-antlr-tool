import re
import inspect

from antlr4 import ParserRuleContext
from antlr4.tree.Tree import TerminalNodeImpl
from antlr4.Token import Token, CommonToken

from .extractor import get_rule_labels

def validate_top_ctx(py_ctx:ParserRuleContext, cpp_ctx:ParserRuleContext):
    assert py_ctx.parentCtx is None
    assert cpp_ctx.parentCtx is None
    validate_ctx(py_ctx, cpp_ctx)

def validate_ctx(py_ctx:ParserRuleContext, cpp_ctx:ParserRuleContext):
    assert type(py_ctx) == type(cpp_ctx)
    pc = list(py_ctx.getChildren())
    cc = list(cpp_ctx.getChildren())
    assert len(pc) == len(cc)

    # Validate children
    for i in range(len(pc)):
        if isinstance(pc[i], TerminalNodeImpl):
            validate_tnode(pc[i], cc[i])
        elif isinstance(pc[i], ParserRuleContext):
            validate_ctx(pc[i], cc[i])
        else:
            raise RuntimeError
        assert pc[i].parentCtx is py_ctx
        assert cc[i].parentCtx is cpp_ctx
    
    # Validate start/stop markers
    validate_common_token(py_ctx.start, cpp_ctx.start)
    if cpp_ctx.start is not None:
        # When start is None, this ctx is empty, C++ may have
        # a different stop (None), but it doesn't matter
        validate_common_token(py_ctx.stop, cpp_ctx.stop)

    # Validate labels
    for label in get_rule_labels(py_ctx):
        if label.startswith("_"):
            continue
        py_label = getattr(py_ctx, label)
        cpp_label = getattr(cpp_ctx, label)
        assert type(py_label) == type(cpp_label)
        if isinstance(py_label, CommonToken):
            validate_common_token(py_label, cpp_label)
        elif isinstance(py_label, ParserRuleContext):
            validate_ctx(py_label, cpp_label)

    # Validate other ctx members
    assert py_ctx.invokingState == cpp_ctx.invokingState


def validate_tnode(py_tnode:TerminalNodeImpl, cpp_tnode:TerminalNodeImpl):
    assert type(py_tnode) == type(cpp_tnode)
    assert type(py_tnode.symbol) == type(cpp_tnode.symbol)

    validate_common_token(py_tnode.symbol, cpp_tnode.symbol)


def validate_common_token(py_tok:CommonToken, cpp_tok:CommonToken):
    if cpp_tok is None and py_tok is not None:
        # EOF in py_tok, cpp_tok can be None it is OK
        assert py_tok.start > py_tok.stop
        return
    assert type(py_tok) == type(cpp_tok)
    if py_tok is None:
        return
    assert py_tok.type == cpp_tok.type
    assert py_tok.channel == cpp_tok.channel
    assert py_tok.start == cpp_tok.start
    assert py_tok.stop == cpp_tok.stop
    assert py_tok.tokenIndex == cpp_tok.tokenIndex
    assert py_tok.line == cpp_tok.line
    assert py_tok.column == cpp_tok.column
    assert py_tok.text == cpp_tok.text
    assert py_tok.getInputStream() is cpp_tok.getInputStream()
