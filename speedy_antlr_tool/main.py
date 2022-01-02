from typing import List, Optional
import os

import jinja2 as jj

from .extractor import extract
from .__about__ import __version__

def write_cpp_files(grammar_name:str, parser_basename:str, context_data:str, entry_rule_names:List[str], output_dir:str):
    loader = jj.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))

    jj_env = jj.Environment(
        loader=loader,
        undefined=jj.StrictUndefined
    )

    context = {
        "grammar_name": grammar_name,
        "parser_basename": parser_basename,
        "context_data": context_data,
        "entry_rule_names": entry_rule_names,
        "__version__": __version__,
    }

    # Write out main module source
    template = jj_env.get_template("sa_X_cpp_parser.cpp")
    stream = template.stream(context)
    output_path = os.path.join(output_dir, "sa_%s_cpp_parser.cpp" % grammar_name.lower())
    stream.dump(output_path)

    # Write out translator visitor header
    template = jj_env.get_template("sa_X_translator.h")
    stream = template.stream(context)
    output_path = os.path.join(output_dir, "sa_%s_translator.h" % grammar_name.lower())
    stream.dump(output_path)

    # Write out translator visitor source
    template = jj_env.get_template("sa_X_translator.cpp")
    stream = template.stream(context)
    output_path = os.path.join(output_dir, "sa_%s_translator.cpp" % grammar_name.lower())
    stream.dump(output_path)

    # Write out support lib header
    template = jj_env.get_template("speedy_antlr.h")
    stream = template.stream(context)
    output_path = os.path.join(output_dir, "speedy_antlr.h")
    stream.dump(output_path)

    # Write out support lib source
    template = jj_env.get_template("speedy_antlr.cpp")
    stream = template.stream(context)
    output_path = os.path.join(output_dir, "speedy_antlr.cpp")
    stream.dump(output_path)


def write_py_files(grammar_name:str, parser_basename:str, context_data:str, output_dir:str):
    loader = jj.FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates"))

    jj_env = jj.Environment(
        loader=loader,
        undefined=jj.StrictUndefined
    )

    context = {
        "grammar_name": grammar_name,
        "parser_basename": parser_basename,
        "context_data": context_data,
        "__version__": __version__,
    }

    # Write out python file
    template = jj_env.get_template("sa_X.pyt")
    stream = template.stream(context)
    output_path = os.path.join(output_dir, "sa_%s.py" % grammar_name.lower())
    stream.dump(output_path)


def generate(py_parser_path:str, cpp_output_dir:str, entry_rule_names:Optional[List[str]]=None):
    if not os.path.exists(py_parser_path):
        raise ValueError("File does not exist: %s" % py_parser_path)
    parser_name = os.path.splitext(os.path.basename(py_parser_path))[0]
    if not parser_name.endswith('Parser'):
        raise ValueError("File does not look like a parser. Parser name shall end in 'Parser': %s" % py_parser_path)

    grammar_name = parser_name[:-6]

    py_output_dir = os.path.dirname(py_parser_path)

    # Parse the Parser.py file and extract context data
    context_data, parser_basename = extract(py_parser_path)

    if entry_rule_names:
        # Validate entry rule names
        for rule_name in entry_rule_names:
            for d in context_data:
                if not d.is_label_ctx:
                    if rule_name == d.rule_name:
                        break
            else:
                raise ValueError("Entry rule name '%s' does not exist in this grammar" % rule_name)
    else:
        # If no entry rule names were specified, load all of them
        entry_rule_names = []
        for d in context_data:
            if not d.is_label_ctx:
                entry_rule_names.append(d.rule_name)

    # Write out files
    write_py_files(grammar_name, parser_basename, context_data, py_output_dir)
    write_cpp_files(grammar_name, parser_basename, context_data, entry_rule_names, cpp_output_dir)
