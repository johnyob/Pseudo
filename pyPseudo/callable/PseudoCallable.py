from abc import ABC as Abstract, abstractmethod

class PseudoCallable(Abstract):
    @abstractmethod
    def arity(self):
        pass

    @abstractmethod
    def call(self, interpreter, arguments, parentheses):
        pass
