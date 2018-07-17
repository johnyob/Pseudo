from copy import deepcopy as DeepCopy

from pyPseudo.interpreter.PseudoList import PseudoList
from pyPseudo.error.RuntimeError import RuntimeError
from pyPseudo.callable.PseudoCallable import PseudoCallable

class ROUND(PseudoCallable):
    def arity(self):
        return 1

    def call(self, interpreter, arguments, parentheses):
        if not isinstance(arguments[0], float):
            raise RuntimeError(parentheses, "Can only round numbers.")
        return round(float(arguments[0]), 0)

class STR(PseudoCallable):
    def arity(self):
        return 1

    def call(self, interpreter, arguments, parentheses):
        if arguments[0] == None:
            return "NULL"

        if isinstance(arguments[0], float):
            text = str(arguments[0])
            if text.endswith(".0"):
                text = text[ : -2]
            return text

        if isinstance(arguments[0], bool):
            if arguments[0] == True:
                return "TRUE"
            return "FALSE"

        return str(arguments[0])

class APPEND(PseudoCallable):
    def arity(self):
        return 2

    def call(self, interpreter, arguments, parentheses):
        if not isinstance(arguments[0], PseudoList):
            raise RuntimeError(parentheses, "Can only append to a list.")

        pseudoList = DeepCopy(arguments[0]) #Deep copy is inefficient
        pseudoList.getValues().append(arguments[1])

        return PseudoList(pseudoList.getValues())

class REMOVE(PseudoCallable):
    def arity(self):
        return 2

    def call(self, interpreter, arguments, parentheses):
        if not isinstance(arguments[0], PseudoList):
            raise RuntimeError(parentheses, "Can only remove elements from a list.")

        pseudoList = DeepCopy(arguments[0])
        pseudoList._checkIndex(parentheses, arguments[1]) #bad, using a private method but CBA
        del pseudoList.getValues()[int(arguments[1])]

        return PseudoList(pseudoList.getValues())


class LENGTH(PseudoCallable):
    def arity(self):
        return 1

    def call(self, interpreter, arguments, parentheses):
        if not isinstance(arguments[0], PseudoList) and not isinstance(arguments[0], str):
            raise RuntimeError(parentheses, "Can only get length of a list or string.")
        return float(len(arguments[0]))

class SLICE(PseudoCallable):
    def arity(self):
        return 3

    def call(self, interpreter, arguments, parentheses):
        if not isinstance(arguments[0], PseudoList):
            raise RuntimeError(parentheses, "Can only slice a list.")

        if not isinstance(arguments[1], float) and not isinstance(arguments[2], float):
            raise RuntimeError(parentheses, "Start and End indices must be numbers.")

        pseudoList = DeepCopy(arguments[0])

        pseudoList._checkIndex(parentheses, arguments[1])
        pseudoList._checkIndex(parentheses, arguments[2])

        return PseudoList(pseudoList.getValues()[int(arguments[1]) : int(arguments[2])])


class INPUT(PseudoCallable):
    def arity(self):
        return 1

    def call(self, interpreter, arguments, parentheses):
        if not isinstance(arguments[0], str):
            raise RuntimeError(parentheses, "Input prompt must be a string.")

        return input(arguments[0])

functions = {
    "ROUND": ROUND(),
    "STR": STR(),
    "APPEND": APPEND(),
    "REMOVE": REMOVE(),
    "LENGTH": LENGTH(),
    "SLICE": SLICE(),
    "INPUT": INPUT()
}
