
Tutorial
========

This section describes how to set up a fully-functional project using Speedy
Antlr. You can find `the completed example here. <https://github.com/amykyta3/speedy-antlr-example>`_

In this example, a we will put together a fictional Python module called
``spam`` that implements an Antlr parser for a grammar called ``MyGrammar``.

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
    :lines: 12-20

You'll notice this last step generates the following files:

* sa_mygrammar.py
* cpp_src/sa_mygrammar_cpp_parser.cpp
* cpp_src/sa_mygrammar_translator.cpp/.h
* cpp_src/speedy_antlr.cpp/.h


sa_mygrammar.py
---------------

`src/spam/parser/sa_mygrammar.py <https://github.com/amykyta3/speedy-antlr-example/blob/master/src/spam/parser/sa_mygrammar.py>`_

TODO


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

TODO


LICENSE-3RD-PARTY
-----------------

`LICENSE-3RD-PARTY <https://github.com/amykyta3/speedy-antlr-example/blob/master/LICENSE-3RD-PARTY>`_

Since you'll be bundling the Antlr C++ runtime in your package's distribution
(source and binary), be a good steward of open-source software and include a
copy of Antlr's BSD license.
