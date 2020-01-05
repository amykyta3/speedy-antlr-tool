#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"

antlr4="java -Xmx500M -cp /usr/local/lib/antlr-4.7.2-complete.jar org.antlr.v4.Tool"

mkdir -p cpp
mkdir -p py

# Generate C++ target with visitor
$antlr4 -Dlanguage=Cpp -visitor -no-listener -o cpp MyGrammar.g4

# Generate Python target
$antlr4 -Dlanguage=Python3 -no-visitor -no-listener -o py MyGrammar.g4

# Run speedy-antlr-tool to generate parse accelerator
./generate_speedy_files.py