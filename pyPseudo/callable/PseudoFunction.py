from pyPseudo.error.Return import Return
from pyPseudo.interpreter.Environment import Environment
from pyPseudo.callable.PseudoCallable import PseudoCallable

class PseudoFunction(PseudoCallable):
    def __init__(self, declaration, closure, isConstructor):
        self._declaration = declaration
        self._closure = closure
        self._isConstructor = isConstructor

    def getClosure(self):
        return self._closure

    def arity(self):
        return len(self._declaration.getParameters())

    def call(self, interpreter, arguments, parentheses):
        environment = Environment(self._closure)
        for i in range(self.arity()):
            environment.define(self._declaration.getParameters()[i].getLexeme(), arguments[i])

        try:
            interpreter.executeBody(self._declaration.getBody(), environment)
        except Return as returnValue:
            return returnValue.getValue()

        if self._isConstructor:
            return self._closure.getAt(0, "THIS")

        return None

    def bind(self, instance):
        environment = Environment(self._closure)
        environment.define("THIS", instance)
        return PseudoFunction(self._declaration, environment, self._isConstructor)

    def __str__(self):
        return "<FUNCTION  {0}>".format(self._declaration.getIdentifier().getLexeme())
