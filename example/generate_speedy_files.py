#!/usr/bin/env python3

import os
import sys

# Ignore this. Only needed for this example
this_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.join(this_dir, "../"))


import speedy_antlr_tool

speedy_antlr_tool.generate("py/MyGrammarParser.py", "cpp")
