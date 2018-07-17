from pyPseudo.error.ParseError import ParseError

from pyPseudo.lexer.Lexer import Lexer
from pyPseudo.lexer.Token import Token
from pyPseudo.lexer.TokenType import TokenType

from pyPseudo.Utilities import readFile

import pyPseudo.parser.Expression as Expression
import pyPseudo.parser.Statement as Statement

class Parser:
    def __init__(self, tokens):
        self._current = 0
        self._tokens = tokens
        self._errors = []

    def parse(self):
        statements = []
        while not self._isAtEnd():
            statements.append(self._declaration())
        return statements

    def getErrors(self):
        return self._errors

    def _declaration(self):
        try:
            if self._match([TokenType.IMPORT]):
                self._importModule()

            if self._match([TokenType.CLASS]):
                return self._classDeclaration()

            if self._match([TokenType.FUNCTION]):
                return self._functionDeclaration()

            if self._match([TokenType.VAR]):
                return self._variableDeclaration()

            return self._statement()
        except ParseError as e:
            self._synchronise()
            return None

    def _importModule(self):
        path = self._consume(TokenType.STRING, "Expect file path for module.").getLiteral()
        #self._consume(TokenType.SEMICOLON, "Expect ';' after file path for module.")

        lexer = Lexer(readFile(path), path)
        moduleTokens = lexer.scanTokens()
        del moduleTokens[-1]
        self._tokens = self._tokens[ : self._current] + moduleTokens + self._tokens[self._current : ]

    def _classDeclaration(self):
        identifier = self._consume(TokenType.IDENTIFIER, "Expect class identifier.")
        superClass = None

        if self._match([TokenType.INHERITS]):
            self._consume(TokenType.IDENTIFIER, "Expect superclass identifier.")
            superClass = Expression.Variable(self._previous())

        methods = []
        while not self._check(TokenType.ENDCLASS) and not self._isAtEnd():
            if self._match([TokenType.FUNCTION]):
                methods.append(self._functionDeclaration())

        self._consume(TokenType.ENDCLASS, "Expect 'ENDCLASS' after class body.")
        return Statement.Class(identifier, superClass, methods)


    def _functionDeclaration(self):
        identifier = self._consume(TokenType.IDENTIFIER, "Expect function identifier.")
        self._consume(TokenType.LEFT_PAREN, "Expect '(' after function identifier.")
        parameters = []

        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                if len(parameters) >= 8:
                    self._error(self._peek(), "Cannot have more than 8 parameters.")
                parameters.append(self._consume(TokenType.IDENTIFIER, "Expect parameter identifier."))
                if not self._match([TokenType.COMMA]):
                    break
        self._consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters.")

        body = self._bodyDeclaration(TokenType.ENDFUNCTION)
        self._consume(TokenType.ENDFUNCTION, "Expect 'ENDFUNCTION' at the end of the function.")

        return Statement.Function(identifier, parameters, body)

    def _bodyDeclaration(self, terminator):
        body = []
        while not self._check(terminator) and not self._isAtEnd():
            body.append(self._declaration())
        return body

    def _variableDeclaration(self):
        identifier = self._consume(TokenType.IDENTIFIER, "Expect variable identifier.")

        initializer = None
        if self._match([TokenType.LEFT_ARROW]):
            initializer = self._expression()

        #self._consume(TokenType.SEMICOLON, "Expect ';' after variable declaration.")
        return Statement.Variable(identifier, initializer)

    def _statement(self):
        if self._match([TokenType.FOR]):
            return self._forStatement()

        if self._match([TokenType.IF]):
            return self._ifStatement()

        if self._match([TokenType.OUTPUT]):
            return self._outputStatement()

        if self._match([TokenType.RETURN]):
            return self._returnStatement()

        if self._match([TokenType.WHILE]):
            return self._whileStatement()

        return self._expressionStatement()

    def _forStatement(self):
        if self._match([TokenType.VAR]):
            identifier = self._consume(TokenType.IDENTIFIER, "Expect variable identifier.")
            self._consume(TokenType.LEFT_ARROW, "Expect '<-' after variable identifier.")
            expression = self._expression()

            initializer = Statement.Variable(identifier, expression)
        else:
            raise self._error(self._peek(), "Expect a variable declaration after 'FOR'.")

        self._consume(TokenType.TO, "Expect 'TO' after varable declaration.")
        right = self._oneDimensionalArithmetic()

        condition = Expression.Binary(
            Expression.Variable(identifier),
            Token(TokenType.LESS_EQUAL, "<=", None, "NULL", -1),
            right
        )

        increment = Expression.Assign(identifier, Expression.Binary(
            Expression.Variable(identifier),
            Token(TokenType.PLUS, "+", None, "NULL", -1),
            Expression.Literal(1.0)
        ))

        self._consume(TokenType.DO, "Expect 'DO' at end of for loop initialization.")

        body = self._bodyDeclaration(TokenType.ENDFOR)
        self._consume(TokenType.ENDFOR, "Expect 'ENDFOR' at end of the for loop.")
        body.append(Statement.Expression(increment))

        return Statement.For(initializer, condition, body)

    def _ifStatement(self):
        condition = self._or()
        self._consume(TokenType.THEN, "Expect 'THEN' after if statement condition.")

        thenBranch = []
        elseBranch = None

        while not(self._check(TokenType.ENDIF) or self._check(TokenType.ELSE)) and not self._isAtEnd():
            thenBranch.append(self._declaration())

        if self._match([TokenType.ELSE]):
            elseBranch = self._bodyDeclaration(TokenType.ENDIF)
        self._consume(TokenType.ENDIF, "Expect 'ENDIF' at end of the if statement.")

        return Statement.If(condition, thenBranch, elseBranch)

    def _outputStatement(self):
        value = self._expression()
        #self._consume(TokenType.SEMICOLON, "Expect ';' after output value.")
        return Statement.Output(value);

    def _returnStatement(self):
        keyword = self._previous()
        value = None
        if not self._check(TokenType.SEMICOLON):
            value = self._expression()

        #self._consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Statement.Return(keyword, value)

    def _whileStatement(self):
        condition = self._expression()
        self._consume(TokenType.DO, "Expect 'DO' after condition")

        body = self._bodyDeclaration(TokenType.ENDWHILE)
        self._consume(TokenType.ENDWHILE, "Expect 'ENDWHILE' at then end of the while statement.")

        return Statement.While(condition, body)

    def _expressionStatement(self):
        expression = self._expression()
        #self._consume(TokenType.SEMICOLON, "Expect ';' after expression.")
        return Statement.Expression(expression)

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        expression = self._or()

        if self._match([TokenType.LEFT_ARROW]):
            leftArrow = self._previous()
            value = self._assignment()
            if isinstance(expression, Expression.Variable):
                identifier = expression.getIdentifier()
                return Expression.Assign(identifier, value)
            elif isinstance(expression, Expression.Get):
                return Expression.Set(expression.getObject(), expression.getIdentifier(), value)
            elif isinstance(expression, Expression.GetIndex):
                return Expression.SetIndex(expression.getObject(), expression.getIndices(), expression.getBrackets(), value)

            self._error(leftArrow, "Invalid assignment target.")
        return expression

    def _or(self):
        expression = self._and()
        while self._match([TokenType.OR]):
            operator = self._previous()
            right = self._and() #check this line!
            expression = Expression.Logical(expression, operator, right)

        return expression

    def _and(self):
        expression = self._equality()

        while self._match([TokenType.AND]):
            operator = self._previous()
            right = self._equality()
            expression = Expression.Logical(expression, operator, right)

        return expression

    def _equality(self):
        expression = self._comparison()

        while self._match([TokenType.NOT_EQUAL, TokenType.EQUAL]):
            operator = self._previous()
            right = self._comparison()
            expression = Expression.Binary(expression, operator, right)

        return expression

    def _comparison(self):
        expression = self._oneDimensionalArithmetic()

        while self._match([TokenType.LESS, TokenType.GREATER, TokenType.LESS_EQUAL, TokenType.GREATER_EQUAL]):
            operator = self._previous()
            right = self._oneDimensionalArithmetic()
            expression = Expression.Binary(expression, operator, right)

        return expression

    def _oneDimensionalArithmetic(self):
        expression = self._twoDimensionalArithmetic()

        while self._match([TokenType.PLUS, TokenType.MINUS]):
            operator = self._previous()
            right = self._twoDimensionalArithmetic()
            expression = Expression.Binary(expression, operator, right)

        return expression

    def _twoDimensionalArithmetic(self):
        expression = self._unary()

        while self._match([TokenType.SLASH, TokenType.STAR]):
            operator = self._previous()
            right = self._unary()
            expression = Expression.Binary(expression, operator, right)

        return expression

    def _unary(self):
        if self._match([TokenType.NOT, TokenType.MINUS]):
            operator = self._previous()
            right = self._unary()
            return Expression.Unary(operator, right)

        return self._index()



    def _functionCall(self):
        expression = self._primary()

        while True:
            if self._match([TokenType.LEFT_PAREN]):
                expression = self._finishFunctionCall(expression)
            elif self._match([TokenType.DOT]):
                identifier = self._consume(TokenType.IDENTIFIER, "Expect property identifier after '.'.")
                expression = Expression.Get(expression, identifier)
            else:
                break

        return expression

    def _finishFunctionCall(self, caller):
        arguments = []
        if not self._check(TokenType.RIGHT_PAREN):
            while True:
                if len(arguments) >= 8:
                    self._error(self._peek(), "Cannot have more than 8 arguments.")
                arguments.append(self._expression())
                if not self._match([TokenType.COMMA]):
                    break
        parantheses = self._consume(TokenType.RIGHT_PAREN, "Expect ')' after arguments.")
        return Expression.Call(caller, parantheses, arguments)

    def _index(self):
        expression = self._functionCall()

        if self._match([TokenType.LEFT_SQUARE]):
            indices = []
            while True:
                if not self._peek().getType() in [TokenType.IDENTIFIER, TokenType.NUMBER]:
                    self._error(self._peek(), "Expect identifier or number for index value.")

                indices.append(self._expression())
                if not self._match([TokenType.COMMA]):
                    break


            brackets = self._consume(TokenType.RIGHT_SQUARE, "Expect ']' after index value.")
            return Expression.GetIndex(expression, indices, brackets)

        return expression

    def _primary(self):
        if self._match([TokenType.FALSE]):
            return Expression.Literal(False)

        if self._match([TokenType.TRUE]):
            return Expression.Literal(True)

        if self._match([TokenType.NULL]):
            return Expression.Literal(None)

        if self._match([TokenType.NUMBER, TokenType.STRING]):
            return Expression.Literal(self._previous().getLiteral())

        if self._match([TokenType.SUPER]):
            keyword = self._previous()
            self._consume(TokenType.DOT, "Expect '.' after 'SUPER'.")
            method = self._consume(TokenType.IDENTIFIER, "Expect super class method name.")
            return Expression.Super(keyword, method)

        if self._match([TokenType.THIS]):
            return Expression.This(self._previous())

        if self._match([TokenType.LEFT_BRACE]):
            values = []
            while True:
                values.append(self._expression())
                if not self._match([TokenType.COMMA]):
                    break
            self._consume(TokenType.RIGHT_BRACE, "Expect '}' after values.")
            return Expression.List(values)

        if self._match([TokenType.IDENTIFIER]):
            return Expression.Variable(self._previous())

        if self._match([TokenType.LEFT_PAREN]):
            expression = self._expression()
            self._consume(TokenType.RIGHT_PAREN, "Expect ')' after expression.")
            return Expression.Grouping(expression)

        raise self._error(self._peek(), "Expect expression.")

    def _consume(self, token, message):
        if self._check(token):
            return self._move()
        raise self._error(self._peek(), message)

    def _error(self, token, message):
        self._errors.append(ParseError(token, message))
        return self._errors[-1]

    def _match(self, tokens):
        for token in tokens:
            if self._check(token):
                self._move()
                return True
        return False

    def _check(self, tokenType):
        if self._isAtEnd():
            return False

        return self._peek().getType() == tokenType

    def _move(self):
        if not self._isAtEnd():
            self._current += 1
        return self._previous()

    def _previous(self):
        return self._tokens[self._current - 1]

    def _peek(self):
        return self._tokens[self._current]

    def _isAtEnd(self):
        return self._peek().getType() == TokenType.EOF

    def _synchronise(self):
        self._move()

        while not self._isAtEnd():
            if self._previous().getType() == TokenType.SEMICOLON:
                return

            if self._peek().getType() in [
                TokenType.CLASS,
                TokenType.FUNCTION,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.OUTPUT,
                TokenType.RETURN
            ]:
                return

            self._move()
