from pyPseudo.error.RuntimeError import RuntimeError

class Environment:

    def __init__(self, enclosing=None):
        self._enclosing = enclosing
        self._values = {}

    def getValues(self):
        return self._values

    def getEnclosing(self):
        return self._enclosing

    def get(self, identifier):
        if identifier.getLexeme() in self._values:
            return self._values[identifier.getLexeme()]

        if self._enclosing != None:
            return self._enclosing.get(identifier)

        raise RuntimeError(identifier, "Undefined vairable '{0}'.".format(identifier.getLexeme()))

    def assign(self, identifier, value):
        if identifier.getLexeme() in self._values:
            self._values[identifier.getLexeme()] = value
            return

        if self._enclosing != None:
            self._enclosing.assign(identifier, value)
            return

        raise RuntimeError(identifier, "Undefined vairable '{0}'.".format(identifier.getLexeme()))

    def define(self, identifier, value):
        self._values[identifier] = value

    def getAt(self, distance, identifier):
        return self._ancestor(distance).getValues()[identifier]

    def _ancestor(self, distance):
        environment = self
        for i in range(0, distance):
            environment = environment.getEnclosing()

        return environment

    def assignAt(self, distance, identifier, value):
        self._ancestor(distance).getValues()[identifier.getLexeme()] = value
