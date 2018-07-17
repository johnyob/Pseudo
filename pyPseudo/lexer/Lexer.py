from pyPseudo.error.ScanError import ScanError

from pyPseudo.lexer.Token import Token
from pyPseudo.lexer.TokenType import TokenType, keywords

class Lexer:
    def __init__(self, source, path):
        self._source = source
        self._path = path
        self._tokens = []
        self._errors = []

        self._start = 0
        self._current = 0
        self._line = 1

    def scanTokens(self):
        while not self._isAtEnd():
            self._start = self._current
            self._scanToken()

        self._tokens.append(Token(TokenType.EOF, "", None, self._path, self._line))
        return self._tokens

    def getErrors(self):
        return self._errors

    def _case(self, character, comparableCharacter):
        return character == comparableCharacter

    def _scanToken(self):
        character = self._move()
        if self._case(character, "("):
            self._addToken(TokenType.LEFT_PAREN)
        elif self._case(character, ")"):
            self._addToken(TokenType.RIGHT_PAREN)
        elif self._case(character, "["):
            self._addToken(TokenType.LEFT_SQUARE)
        elif self._case(character, "]"):
            self._addToken(TokenType.RIGHT_SQUARE)
        elif self._case(character, "{"):
            self._addToken(TokenType.LEFT_BRACE)
        elif self._case(character, "}"):
            self._addToken(TokenType.RIGHT_BRACE)
        elif self._case(character, ","):
            self._addToken(TokenType.COMMA)
        elif self._case(character, "."):
            self._addToken(TokenType.DOT)
        elif self._case(character, "-"):
            self._addToken(TokenType.MINUS)
        elif self._case(character, "+"):
            self._addToken(TokenType.PLUS)
        elif self._case(character, ";"):
            #self._addToken(TokenType.SEMICOLON)
            pass
        elif self._case(character, "*"):
            self._addToken(TokenType.STAR)
        elif self._case(character, "<"):
            self._addToken(
                TokenType.LEFT_ARROW if self._match("-") else TokenType.LESS_EQUAL \
                if self._match("=") else TokenType.NOT_EQUAL if self._match(">") else \
                TokenType.LESS
            )
        elif self._case(character, ">"):
            self._addToken(
                TokenType.GREATER_EQUAL if self._match("=") else TokenType.GREATER
            )
        elif self._case(character, "="):
            self._addToken(TokenType.EQUAL)
        elif self._case(character, "/"):
            if self._match("/"):
                while self._peek() != "\n" and not self._isAtEnd():
                    self._move()
            else:
                self._addToken(TokenType.SLASH)
        elif self._case(character, " "):
            pass
        elif self._case(character, "\r"):
            pass
        elif self._case(character, "\t"):
            pass
        elif self._case(character, "\n"):
            self._line += 1
        elif self._case(character, "\""):
            self._string()
        else:
            if self._isDigit(character):
                self._number()
            elif self._isAlpha(character):
                self._identifier()
            else:
                self._error(self._path, self._line, "Unexpected character")

    def _identifier(self):
        while not self._isAtEnd() and self._isAlphaNumeric(self._peek()):
            self._move()

        text = self._source[self._start : self._current]
        token = keywords.get(text, TokenType.IDENTIFIER)
        self._addToken(token)

    def _number(self):
        while not self._isAtEnd() and self._isDigit(self._peek()):
            self._move()

        if self._peek() == "." and self._isDigit(self._peekNext()):
            self._move()
            while self._isDigit(self._peek()):
                self._move()

        literal = float(self._source[self._start : self._current])
        self._addTokenLiteral(TokenType.NUMBER, literal)

    def _string(self):
        while self._peek() != "\"" and not self._isAtEnd():
            if self._peek() == "\n":
                self._line += 1
            self._move()

        if self._isAtEnd():
            self._error("Unterminated string")
            return

        self._move()
        literal = self._source[self._start + 1 : self._current - 1]
        self._addTokenLiteral(TokenType.STRING, literal)

    def _match(self, expected):
        if self._isAtEnd():
            return False

        if self._source[self._current] != expected:
            return False

        self._current += 1
        return True

    def _peekNext(self):
        if self._current + 1 >= len(self._source):
            return '\0'
        return self._source[self._current + 1]

    def _peek(self):
        if self._isAtEnd():
            return '\0'
        return self._source[self._current]

    def _move(self):
        self._current += 1
        return self._source[self._current - 1]

    def _addToken(self, type):
        self._addTokenLiteral(type, None)

    def _addTokenLiteral(self, type, literal):
        lexeme = self._source[self._start : self._current]
        self._tokens.append(Token(type, lexeme, literal, self._path, self._line))

    def _isDigit(self, character):
        return character.isdigit()

    def _isAlpha(self, character):
        return character.isalpha()

    def _isAlphaNumeric(self, character):
        return self._isDigit(character) or self._isAlpha(character)

    def _isAtEnd(self):
        return self._current >= len(self._source)

    def _error(self, message):
        self._errors.append(ScanError(self._path, self._line, message))
