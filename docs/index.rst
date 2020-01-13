.. toctree::
   :hidden:

   self
   example

Speedy Antlr Tool
=================

Running an Antlr parser in Python is slow.

This tool generates a Python extension that runs your parser using Antlr's C++
target, and then translates the parsed tree back into Python.

Performance is highly dependant on the complexity of the grammar. Depending on
the test input used, parse speed can be improved by 5x to 25x.

Installing
----------

Install from `PyPi`_ using pip

.. code-block:: bash

   python3 -m pip install speedy-antlr-tool

.. _PyPi: https://pypi.org/project/speedy-antlr-tool
