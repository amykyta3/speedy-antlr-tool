
Tutorial
========

This section describes how to set up a fully-functional project using Speedy
Antlr. You can find `the completed example here. <https://github.com/amykyta3/speedy-antlr-example>`_

In this example, a we will put together a fictional Python module called
``spam`` that implements an Antlr parser for a grammar called ``MyGrammar``.


antlr4-cpp-runtime
------------------

`src/spam/parser/cpp_src/antlr4-cpp-runtime <https://github.com/amykyta3/speedy-antlr-example/tree/master/src/spam/parser/cpp_src/antlr4-cpp-runtime>`_

This directory contains a copy of Antlr's C++ runtime source. This is required
for our extension to be built against.

Future releases of the runtime can be downloaded from `Antlr's download page <https://www.antlr.org/download.html>`_


generate_parsers.sh
-------------------

`src/spam/parser/generate_parsers.sh <https://github.com/amykyta3/speedy-antlr-example/blob/master/src/spam/parser/generate_parsers.sh>`_

This script is what the developer uses to re-generate Antlr targets, as well as
the Speedy Antlr accelerator files.

As usual, generate targets from your grammar file using Antlr. We want to
generate both Python and C++ targets since both will be used together.

.. literalinclude:: speedy-antlr-example/src/spam/parser/generate_parsers.sh
    :language: bash
    :lines: 4-10

After the targets are generated, invoke ``speedy-antlr-tool`` via Python to
generate the accelerator files.

.. literalinclude:: speedy-antlr-example/src/spam/parser/generate_parsers.sh
    :language: bash
    :lines: 12-21

.. note::

    The optional ``entry_rule_names`` option allows you to provide a reduced list of
    parse tree entry points. This is a list of context names the parser will support
    when calling the ``parse()`` function from Python. Providing a reduced list
    can simplify the output and remove unnecessary code from the parse accelerator.

    If this option is omitted, support for all entry rules is generated.

You'll notice this last step generates the following files:

* sa_mygrammar.py
* cpp_src/sa_mygrammar_cpp_parser.cpp
* cpp_src/sa_mygrammar_translator.cpp/.h
* cpp_src/speedy_antlr.cpp/.h

.. note::
    If your language grammar is split into separate Lexer and Parser files, see
    the alternate `src/spam/parser/generate_parsers_split.sh <https://github.com/amykyta3/speedy-antlr-example/blob/master/src/spam/parser/generate_parsers_split.sh>`_
    example script.

sa_mygrammar.py
---------------

`src/spam/parser/sa_mygrammar.py <https://github.com/amykyta3/speedy-antlr-example/blob/master/src/spam/parser/sa_mygrammar.py>`_

This module provides the entry-point for the C++ based parser, as well as a
pure Python fall-back implementation. When calling the ``parse()`` function,
the fall-back implementation is automatically used if the C++ version failed to
install.


print_tree.py
-------------

`src/spam/print_tree.py <https://github.com/amykyta3/speedy-antlr-example/blob/master/src/spam/print_tree.py>`_

Now let's use the resulting parser.

You can use the following boolean flag to detect whether the C++ accelerator
extension will be used. Using this flag is not necessary, but it can be
overridden to ``False`` if you want to force it to use the fall-back Python
parser.

.. literalinclude:: speedy-antlr-example/src/spam/print_tree.py
    :language: python
    :lines: 20-23

In some applications it is useful to intercept lex/parse syntax errors. The
Antlr runtime provides a mechanism to do so via the ``ErrorListener`` class.
Unfortunately since it is not practical to translate all Antlr C++ objects back
to Python, the usual error listener can not be used. Instead, an equivalent
``SA_ErrorListener`` is provided that provides a very similar interface.

Using the error listener is totally optional. If it is omitted, Antlr's default
ConsoleErrorListener is used.

For this example, let's define a pretty verbose listener:

.. literalinclude:: speedy-antlr-example/src/spam/print_tree.py
    :language: python
    :lines: 6-16

And finally put everything together:

.. literalinclude:: speedy-antlr-example/src/spam/print_tree.py
    :language: python
    :lines: 25-32


setup.py
--------

`setup.py <https://github.com/amykyta3/speedy-antlr-example/blob/master/setup.py>`_

This example setup script shows how to gracefully omit the C++ accelerator if
it fails to build. Recall from earlier, if the extension is not available, the
``parse()`` wrapper function will automatically choose the Python equivalent.


LICENSE-3RD-PARTY
-----------------

`LICENSE-3RD-PARTY <https://github.com/amykyta3/speedy-antlr-example/blob/master/LICENSE-3RD-PARTY>`_

Since you'll be bundling the Antlr C++ runtime in your package's distribution
(source and binary), be a good steward of open-source software and include a
copy of Antlr's BSD license.

.github/workflows/build.yml
---------------------------

`.github/workflows/build.yml <https://github.com/amykyta3/speedy-antlr-example/blob/master/.github/workflows/build.yml>`_

If you've attempted to install this example by now, you've probably noticed that
it takes a *looong* time. This is because all the C++ files (antlr has many)
are getting compiled.

If you plan to publish your package to PyPi, it is good practice to also publish
binary distributions. This eliminates the need for the end-user to install a
compiler and build everything from source.

Since you probably don't have access to every variant of Windows/Linux/macOS,
this is typically done using a continuous integration service like Github
Actions. This YAML file tells Github Actions how to run your project's tests,
and how to deploy to PyPi. I'm also using
`cibuildwheel <https://github.com/joerick/cibuildwheel>`_ to automate building
all the different distribution variants.
