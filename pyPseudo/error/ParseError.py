from pyPseudo.error.RuntimeError import RuntimeError

class ParseError(RuntimeError):
    def __init__(self, token, message):
        super().__init__(token, message)
