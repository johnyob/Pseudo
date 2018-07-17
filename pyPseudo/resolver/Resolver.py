from pyPseudo.error.ResolveError import ResolveError

from pyPseudo.callable.PseudoFunctions import functions

from pyPseudo.lexer.TokenType import TokenType
from pyPseudo.lexer.Token import Token

from pyPseudo.parser.Expression import ExpressionVisitor
from pyPseudo.parser.Statement import StatementVisitor

from pyPseudo.Utilities import Stack

from pyPseudo.resolver.FunctionType import FunctionType
from pyPseudo.resolver.ClassType import ClassType

class Resolver(ExpressionVisitor, StatementVisitor):

    def __init__(self, interpreter):
        self._interpreter = interpreter
        self._currentFunction = FunctionType.NONE
        self._currentClass = ClassType.NONE
        self._scopes = Stack()
        self._errors = []


    def resolveSource(self, statements):
        self._beginScope()

        for function in functions.keys():
            self._declare(Token(TokenType.IDENTIFIER, function, None, "BUILT-IN FUNCTIONS", -1))
            self._define(Token(TokenType.IDENTIFIER, function, None, "BUILT-IN FUNCTIONS", -1))

        for statement in statements:
            self._resolveStatement(statement)
        self._endScope()

    def getErrors(self):
        return self._errors

    def visitAssignExpression(self, expression):
        self._resolveExpression(expression.getValue())
        self._resolveLocal(expression, expression.getIdentifier())

    def visitVariableExpression(self, expression):
        if not self._scopes.isEmpty() and self._scopes.peek().get(expression.getIdentifier().getLexeme(), None) == False:
            self._error(expression.getIdentifier(), "Cannot read local variable in it's own initializer.")
        self._resolveLocal(expression, expression.getIdentifier())

    def visitGroupingExpression(self, expression):
        self._resolveExpression(expression.getExpression())

    def visitSetExpression(self, expression):
        self._resolveExpression(expression.getValue())
        self._resolveExpression(expression.getObject())

    def visitLiteralExpression(self, expression):
        pass

    def visitLogicalExpression(self, expression):
        self._resolveExpression(expression.getLeft())
        self._resolveExpression(expression.getRight())

    def visitBinaryExpression(self, expression):
        self._resolveExpression(expression.getLeft())
        self._resolveExpression(expression.getRight())

    def visitUnaryExpression(self, expression):
        self._resolveExpression(expression.getRight())

    def visitCallExpression(self, expression):
        self._resolveExpression(expression.getCaller())
        for argument in expression.getArguments():
            self._resolveExpression(argument)

    def visitGetExpression(self, expression):
        self._resolveExpression(expression.getObject())

    def visitThisExpression(self, expression):
        if self._currentClass == ClassType.NONE:
            self._error(expression.getKeyword, "Cannot use 'THIS' outside of a class")
            return

        self._resolveLocal(expression, expression.getKeyword())

    def visitSuperExpression(self, expression):
        if self._currentClass == ClassType.NONE:
            self._error(expression.getKeyword(), "Cannot use 'SUPER' outside of a class.")
        elif self._currentClass != ClassType.SUBCLASS:
            self._error(expression.getKeyword(), "Cannot use 'SUPER' in a class with no super class.")

        self._resolveLocal(expression, expression.getKeyword())

    def visitGetIndexExpression(self, expression):
        self._resolveExpression(expression.getObject())
        for index in expression.getIndices():
            self._resolveExpression(index)

    def visitListExpression(self, expression):
        for value in expression.getValues():
            self._resolveExpression(value)

    def visitSetIndexExpression(self, expression):
        self._resolveExpression(expression.getValue())
        self._resolveExpression(expression.getObject())
        for index in expression.getIndices():
            self._resolveExpression(index)

    def visitClassStatement(self, statement):
        self._declare(statement.getIdentifier())
        self._define(statement.getIdentifier())

        enclosingClass = self._currentClass
        self._currentClass = ClassType.CLASS

        if statement.getSuperClass() != None:
            self._currentClass = ClassType.SUBCLASS
            self._resolveExpression(statement.getSuperClass())
            self._beginScope()
            self._scopes.peek()["SUPER"] = True

        self._beginScope()
        self._scopes.peek()["THIS"] = True

        for method in statement.getMethods():
            declaration = FunctionType.METHOD
            if method.getIdentifier().getLexeme() == statement.getIdentifier():
                declaration = FunctionType.CONSTRUCTOR

            self._resolveFunction(method, declaration)
        self._endScope()

        if statement.getSuperClass() != None:
            self._endScope()

        self._currentClass = enclosingClass

    def visitFunctionStatement(self, statement):
        self._declare(statement.getIdentifier())
        self._define(statement.getIdentifier())

        self._resolveFunction(statement, FunctionType.FUNCTION)

    def visitReturnStatement(self, statement):
        if self._currentFunction == FunctionType.NONE:
            self._error(statement.getKeyword(), "Cannot return when return statement isn't enclosed in a function.")

        if statement.getValue() != None:
            if self._currentFunction == FunctionType.CONSTRUCTOR:
                self._error(statement.getKeyword(), "Cannot return a value from a constructor.")
            self._resolveExpression(statement.getValue())

    def visitExpressionStatement(self, statement):
        self._resolveExpression(statement.getExpression())

    def visitVariableStatement(self, statement):
        self._declare(statement.getIdentifier())
        if statement.getInitializer() != None:
            self._resolveExpression(statement.getInitializer())
        self._define(statement.getIdentifier())

    def visitIfStatement(self, statement):
        self._resolveExpression(statement.getCondition())
        self._resolveBody(statement.getThenBranch())
        if statement.getElseBranch() != None:
            self._resolveBody(statement.getElseBranch())

    def visitWhileStatement(self, statement):
        self._resolveExpression(statement.getCondition())
        self._resolveBody(statement.getBody())

    def visitForStatement(self, statement):
        self._resolveStatement(statement.getInitializer())
        self._resolveExpression(statement.getCondition())
        self._resolveBody(statement.getBody())

    def visitOutputStatement(self, statement):
        self._resolveExpression(statement.getExpression())

    def _resolveExpression(self, expression):
        expression.accept(self)

    def _resolveStatement(self, statement):
        statement.accept(self)

    def _resolveBody(self, statements):
        self._beginScope()
        for statement in statements:
            self._resolveStatement(statement)
        self._endScope()

    def _resolveLocal(self, expression, identifier):
        for i in range(len(self._scopes) - 1, -1, -1): #i <- len(scopes) - 1 TO 0
            if identifier.getLexeme() in self._scopes.get(i):
                self._interpreter.resolve(expression, len(self._scopes) - 1 - i)
                return

    def _resolveFunction(self, function, type):
        enclosingFunction = self._currentFunction
        self._currentFunction = type
        self._beginScope()

        for parameter in function.getParameters():
            self._declare(parameter)
            self._define(parameter)

        for statement in function.getBody():
            self._resolveStatement(statement)

        self._endScope()
        self._currentFunction = enclosingFunction

    def _declare(self, identifier):
        if self._scopes.isEmpty():
            return

        scope = self._scopes.peek()
        if identifier.getLexeme() in scope:
            pass
            self._error(identifier, "Variable with this name is already declared in this scope.")

        scope[identifier.getLexeme()] = False

    def _define(self, identifier):
        if self._scopes.isEmpty():
            return

        self._scopes.peek()[identifier.getLexeme()] = True

    def _beginScope(self):
        self._scopes.push({})

    def _endScope(self):
        self._scopes.pop()

    def _error(self, token, message):
        self._errors.append(ResolveError(token, message))
