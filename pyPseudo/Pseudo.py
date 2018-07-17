import sys as System
import traceback as Traceback

from pyPseudo.lexer.Lexer import Lexer
from pyPseudo.parser.Parser import Parser
from pyPseudo.resolver.Resolver import Resolver
from pyPseudo.interpreter.Interpreter import Interpreter
from pyPseudo.Utilities import readFile

class Pseudo:

    def __init__(self, args):
        self._interpreter = Interpreter()

        if len(args) > 1:
            print("Usage: python pseudo.py file")
        elif len(args) == 1:
            self._runFile(args[0])
        else:
            self._runPrompt()

    def _runFile(self, path):
        errors, runtimeErrors = self._run(readFile(path), path)

        if errors:
            System.exit(65)

        if runtimeErrors:
            System.exit(70)

    def _runPrompt(self):
        while True:
            self._run(input("> "), "INTERPRETER")

    def _run(self, source, path):
        lexerErrors, parserErrors, resolverErrors, interpreterErrors = [], [], [], []

        lexer = Lexer(source, path)
        tokens = lexer.scanTokens()


        parser = Parser(tokens)
        statements = parser.parse()
        
        lexerErrors, parserErrors = lexer.getErrors(), parser.getErrors()
        self._printErrors(lexerErrors + parserErrors)

        if len(lexerErrors + parserErrors) > 0:
            return lexerErrors + parserErrors + resolverErrors, interpreterErrors


        resolver = Resolver(self._interpreter)
        resolver.resolveSource(statements)

        resolverErrors = resolver.getErrors()
        self._printErrors(resolverErrors)

        if len(resolverErrors) > 0:
            return lexerErrors + parserErrors + resolverErrors, interpreterErrors

        self._interpreter.interpret(statements)
        interpreterErrors = self._interpreter.getErrors()

        self._printErrors(interpreterErrors)

        return lexerErrors + parserErrors + resolverErrors, interpreterErrors

    def _printErrors(self, errors):
        for error in errors:
            if hasattr(error, "report"):
                print(error.report())
            else:
                print("Python Error: {0}".format(error))

def main(arguments):
    del arguments[0]
    Pseudo(arguments)

if __name__ == "__main__":
    main(System.argv)
