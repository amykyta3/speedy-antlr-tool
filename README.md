[![Documentation Status](https://readthedocs.org/projects/speedy-antlr-tool/badge/?version=latest)](http://speedy-antlr-tool.readthedocs.io)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/speedy-antlr-tool.svg)](https://pypi.org/project/speedy-antlr-tool)

# Speedy Antlr Tool

Running an Antlr parser in Python is slow.

This tool generates a Python extension that runs your parser using Antlr's C++
target, and then translates the parsed tree back into Python.

See the [Speedy Antlr Tool Documentation](http://speedy-antlr-tool.readthedocs.io) for more details
