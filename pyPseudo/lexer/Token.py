class Token:
    def __init__(self, type, lexeme, literal, path, line):
        self._type = type
        self._lexeme = lexeme
        self._literal = literal
        self._path = path
        self._line = line

    def getType(self):
        return self._type

    def getLexeme(self):
        return self._lexeme

    def getLiteral(self):
        return self._literal

    def getPath(self):
        return self._path

    def getLine(self):
        return self._line

    def __str__(self):
        return "Type: {0}, Lexeme: {1}, Literal: {2}.".format(
            self._type, self._lexeme, self._literal
        )

    def __repr__(self):
        return "Type: {0}, Lexeme: {1}, Literal: {2}.".format(
            self._type, self._lexeme, self._literal
        )
