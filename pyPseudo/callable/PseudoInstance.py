class PseudoInstance:
    def __init__(self, pseudoClass):
        self._pseudoClass = pseudoClass
        self._properties = {}

    def getPseudoClass(self):
        return self._pseudoClass

    def get(self, identifier):
        if identifier.getLexeme() in self._properties:
            return self._properties[identifier.getLexeme()]

        method = self._pseudoClass.findMethod(self, identifier.getLexeme())
        if method != None:
            return method

        raise RuntimeError(identifier, "Undefined property '{0}'.".format(identifier.getLexeme()))

    def set(self, identifier, value):
        self._properties[identifier.getLexeme()] = value

    def __str__(self):
        return str(self._pseudoClass) + " instance."
