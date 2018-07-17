from abc import ABC as Abstract, abstractmethod

class StatementVisitor(Abstract):
    @abstractmethod
    def visitClassStatement(self, statement):
        pass

    @abstractmethod
    def visitFunctionStatement(self, statement):
        pass

    @abstractmethod
    def visitReturnStatement(self, statement):
        pass

    @abstractmethod
    def visitExpressionStatement(self, statement):
        pass

    @abstractmethod
    def visitVariableStatement(self, statement):
        pass

    @abstractmethod
    def visitIfStatement(self, statement):
        pass

    @abstractmethod
    def visitWhileStatement(self, statement):
        pass

    @abstractmethod
    def visitForStatement(self, statement):
        pass

    @abstractmethod
    def visitOutputStatement(self, statement):
        pass

class Statement(Abstract):
    @abstractmethod
    def accept(self, visitor):
        pass

class Class(Statement):
    def __init__(self, identifier, superClass, methods):
        self._identifier = identifier
        self._superClass = superClass
        self._methods = methods

    def getIdentifier(self):
        return self._identifier

    def getSuperClass(self):
        return self._superClass

    def getMethods(self):
        return self._methods

    def accept(self, visitor):
        return visitor.visitClassStatement(self)

    def __repr__(self):
        return "Class(Identifier: ({0}), SuperClass: ({1}), Methods: ({2}))".format(self._identifier, self._superClass, self._methods)

class Function(Statement):
    def __init__(self, identifier, parameters, body):
        self._identifier = identifier
        self._parameters = parameters
        self._body = body

    def getIdentifier(self):
        return self._identifier

    def getParameters(self):
        return self._parameters

    def getBody(self):
        return self._body

    def accept(self, visitor):
        return visitor.visitFunctionStatement(self)

    def __repr__(self):
        return "Function(Identifier: ({0}), Parameters: ({1}), Body: ({2}))".format(self._identifier, self._parameters, self._body)

class Return(Statement):
    def __init__(self, keyword, value):
        self._keyword = keyword
        self._value = value

    def getKeyword(self):
        return self._keyword

    def getValue(self):
        return self._value

    def accept(self, visitor):
        return visitor.visitReturnStatement(self)

    def __repr__(self):
        return "Return(Keyword: ({0}), Value: ({1}))".format(self._keyword, self._value)

class Expression(Statement):
    def __init__(self, expression):
        self._expression = expression

    def getExpression(self):
        return self._expression

    def accept(self, visitor):
        return visitor.visitExpressionStatement(self)

    def __repr__(self):
        return "Expression(Expression: ({0}))".format(self._expression)

class Variable(Statement):
    def __init__(self, identifier, initializer):
        self._identifier = identifier
        self._initializer = initializer

    def getIdentifier(self):
        return self._identifier

    def getInitializer(self):
        return self._initializer

    def accept(self, visitor):
        return visitor.visitVariableStatement(self)

    def __repr__(self):
        return "Variable(Identifier: ({0}), Initializer: ({1}))".format(self._identifier, self._initializer)

class If(Statement):
    def __init__(self, condition, thenBranch, elseBranch):
        self._condition = condition
        self._thenBranch = thenBranch
        self._elseBranch = elseBranch

    def getCondition(self):
        return self._condition

    def getThenBranch(self):
        return self._thenBranch

    def getElseBranch(self):
        return self._elseBranch

    def accept(self, visitor):
        return visitor.visitIfStatement(self)

    def __repr__(self):
        return "If(Condition: ({0}), ThenBranch: ({1}), ElseBranch: ({2}))".format(self._condition, self._thenBranch, self._elseBranch)

class While(Statement):
    def __init__(self, condition, body):
        self._condition = condition
        self._body = body

    def getCondition(self):
        return self._condition

    def getBody(self):
        return self._body

    def accept(self, visitor):
        return visitor.visitWhileStatement(self)

    def __repr__(self):
        return "While(Condition: ({0}), Body: ({1}))".format(self._condition, self._body)

class Output(Statement):
    def __init__(self, expression):
        self._expression = expression

    def getExpression(self):
        return self._expression

    def accept(self, visitor):
        return visitor.visitOutputStatement(self)

    def __repr__(self):
        return "Output(Expression: ({0}))".format(self._expression)

class For(Statement):
    def __init__(self, initializer, condition, body):
        self._initializer = initializer
        self._condition = condition
        self._body = body

    def getInitializer(self):
        return self._initializer

    def getCondition(self):
        return self._condition

    def getBody(self):
        return self._body

    def accept(self, visitor):
        return visitor.visitForStatement(self)

    def __repr__(self):
        return "For(Initializer: ({0}), Condition: ({1}), Body: ({2}))".format(self._initializer, self._condition, self._body)
