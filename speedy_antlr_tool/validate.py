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
    assert len(py_ctx.children) == len(cpp_ctx.children)

    # Validate children
    for i in range(len(py_ctx.children)):
        if isinstance(py_ctx.children[i], TerminalNodeImpl):
            validate_tnode(py_ctx.children[i], cpp_ctx.children[i])
        elif isinstance(py_ctx.children[i], ParserRuleContext):
            validate_ctx(py_ctx.children[i], cpp_ctx.children[i])
        else:
            raise RuntimeError
        assert py_ctx.children[i].parentCtx is py_ctx
        assert cpp_ctx.children[i].parentCtx is cpp_ctx
    
    # Validate start/stop markers
    validate_common_token(py_ctx.start, cpp_ctx.start)
    validate_common_token(py_ctx.stop, cpp_ctx.stop)

    # Validate labels
    for label in get_rule_labels(py_ctx):
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
