from pyPseudo.callable.PseudoCallable import PseudoCallable
from pyPseudo.callable.PseudoInstance import PseudoInstance

class PseudoClass(PseudoCallable):

    def __init__(self, identifier, superClass, methods):
        self._identifier = identifier
        self._superClass = superClass
        self._methods = methods

    def getIdentifier(self):
        return self._identifier

    def findMethod(self, instance, identifier):
        if identifier in self._methods:
            return self._methods[identifier].bind(instance)

        if self._superClass != None:
            return self._superClass.findMethod(instance, identifier)

        return None

    def arity(self):
        constructor = self._methods.get(self._identifier, None)
        if constructor == None:
            return 0
        return constructor.arity()

    def call(self, interpreter, arguments, parentheses):
        instance = PseudoInstance(self)
        constructor = self._methods.get(self._identifier, None)
        if constructor != None:
            constructor.bind(instance).call(interpreter, arguments, parentheses)
        return instance

    def __str__(self):
        return "<CLASS {0}>".format(self._identifier)
