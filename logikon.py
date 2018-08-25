#!/usr/bin/python

from formal_checker import FormalChecker
from parser import Parser
from syntax_checker import SyntaxChecker

import os
import sys

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: " + sys.argv[0] + " <source>.lk")
        sys.exit(1)
    source_file = sys.argv[1]
    source = open(source_file, 'r').read()

    parser = Parser()
    tokens = parser.parse(source)
    print([t.toString() for t in tokens])

    syntax_checker = SyntaxChecker()
    ast = syntax_checker.check(tokens)
    print(ast.toString())

    formal_checker = FormalChecker()
    ast.accept(formal_checker)

    print(formal_checker.solver)
