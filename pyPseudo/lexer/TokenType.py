from enum import Enum as Enumerate

class TokenType(Enumerate):
    IMPORT = 1
    LEFT_PAREN = 2
    RIGHT_PAREN = 3
    COMMA = 4
    DOT = 5

    MINUS = 6
    PLUS = 7
    SLASH = 8
    STAR = 9

    NOT_EQUAL = 10
    EQUAL = 11
    LEFT_ARROW = 12
    GREATER = 13
    GREATER_EQUAL = 14
    LESS = 15
    LESS_EQUAL = 16

    SEMICOLON = 17
    IDENTIFIER = 18
    STRING = 19
    NUMBER = 20

    AND = 21
    OR = 22
    NOT = 23

    CLASS = 24
    FUNCTION = 25
    SUPER = 26
    THIS = 27
    INHERITS = 28

    OUTPUT = 29
    RETURN = 30

    IF = 31
    THEN = 32
    ELSE = 33

    FALSE = 34
    TRUE = 35
    NULL = 36

    FOR = 37
    TO = 38
    WHILE = 39
    DO = 40

    VAR = 41

    ENDFUNCTION = 42
    ENDCLASS = 43
    ENDFOR = 44
    ENDWHILE = 45
    ENDIF = 46

    LEFT_SQUARE = 47
    RIGHT_SQUARE = 48

    LEFT_BRACE = 49
    RIGHT_BRACE = 50

    EOF = 51

keywords = {
    "IMPORT": TokenType.IMPORT,

    "AND": TokenType.AND,
    "OR": TokenType.OR,
    "NOT": TokenType.NOT,

    "CLASS": TokenType.CLASS,
    "FUNCTION": TokenType.FUNCTION,
    "SUPER": TokenType.SUPER,
    "THIS": TokenType.THIS,
    "INHERITS": TokenType.INHERITS,

    "OUTPUT": TokenType.OUTPUT,
    "RETURN": TokenType.RETURN,

    "IF": TokenType.IF,
    "THEN": TokenType.THEN,
    "ELSE": TokenType.ELSE,

    "TRUE": TokenType.TRUE,
    "FALSE": TokenType.FALSE,
    "NULL": TokenType.NULL,

    "VAR": TokenType.VAR,

    "FOR": TokenType.FOR,
    "TO": TokenType.TO,
    "WHILE": TokenType.WHILE,
    "DO": TokenType.DO,

    "ENDFUNCTION": TokenType.ENDFUNCTION,
    "ENDCLASS": TokenType.ENDCLASS,
    "ENDIF": TokenType.ENDIF,
    "ENDFOR": TokenType.ENDFOR,
    "ENDWHILE": TokenType.ENDWHILE
}
