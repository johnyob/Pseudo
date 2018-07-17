from abc import ABC as Abstract, abstractmethod

class ExpressionVisitor(Abstract):
    @abstractmethod
    def visitAssignExpression(self, expression):
        pass

    @abstractmethod
    def visitVariableExpression(self, expression):
        pass

    @abstractmethod
    def visitGroupingExpression(self, expression):
        pass

    @abstractmethod
    def visitSetExpression(self, expression):
        pass

    @abstractmethod
    def visitLiteralExpression(self, expression):
        pass

    @abstractmethod
    def visitLogicalExpression(self, expression):
        pass

    @abstractmethod
    def visitBinaryExpression(self, expression):
        pass

    @abstractmethod
    def visitUnaryExpression(self, expression):
        pass

    @abstractmethod
    def visitCallExpression(self, expression):
        pass

    @abstractmethod
    def visitGetExpression(self, expression):
        pass

    @abstractmethod
    def visitThisExpression(self, expression):
        pass

    @abstractmethod
    def visitSuperExpression(self, expression):
        pass

    @abstractmethod
    def visitGetIndexExpression(self, expression):
        pass

    @abstractmethod
    def visitListExpression(self, expression):
        pass

    @abstractmethod
    def visitSetIndexExpression(self, expression):
        pass

class Expression(Abstract):
    @abstractmethod
    def accept(self, visitor):
        pass

class Assign(Expression):
    def __init__(self, identifier, value):
        self._identifier = identifier
        self._value = value

    def getIdentifier(self):
        return self._identifier

    def getValue(self):
        return self._value

    def accept(self, visitor):
        return visitor.visitAssignExpression(self)

    def __repr__(self):
        return "Assign(Identifier: ({0}), Value: ({1}))".format(self._identifier, self._value)

class Variable(Expression):
    def __init__(self, identifier):
        self._identifier = identifier

    def getIdentifier(self):
        return self._identifier

    def accept(self, visitor):
        return visitor.visitVariableExpression(self)

    def __repr__(self):
        return "Variable(Identifier: ({0}))".format(self._identifier)

class Grouping(Expression):
    def __init__(self, expression):
        self._expression = expression

    def getExpression(self):
        return self._expression

    def accept(self, visitor):
        return visitor.visitGroupingExpression(self)

    def __repr__(self):
        return "Grouping(Expression: ({0}))".format(self._expression)

class Set(Expression):
    def __init__(self, object, identifier, value):
        self._object = object
        self._identifier = identifier
        self._value = value

    def getObject(self):
        return self._object

    def getIdentifier(self):
        return self._identifier

    def getValue(self):
        return self._value

    def accept(self, visitor):
        return visitor.visitSetExpression(self)

    def __repr__(self):
        return "Set(Object: ({0}), Identifier: ({1}), Value: ({2}))".format(self._object, self._identifier, self._value)
class Literal(Expression):
    def __init__(self, value):
        self._value = value

    def getValue(self):
        return self._value

    def accept(self, visitor):
        return visitor.visitLiteralExpression(self)

    def __repr__(self):
        return "Literal(Value: ({0}))".format(self._value)

class Logical(Expression):
    def __init__(self, left, operator, right):
        self._left = left
        self._operator = operator
        self._right = right

    def getLeft(self):
        return self._left

    def getOperator(self):
        return self._operator

    def getRight(self):
        return self._right

    def accept(self, visitor):
        return visitor.visitLogicalExpression(self)

    def __repr__(self):
        return "Logical(Left: ({0}), Operator: ({1}), Right: ({2}))".format(self._left, self._operator, self._right)

class Binary(Expression):
    def __init__(self, left, operator, right):
        self._left = left
        self._operator = operator
        self._right = right

    def getLeft(self):
        return self._left

    def getOperator(self):
        return self._operator

    def getRight(self):
        return self._right

    def accept(self, visitor):
        return visitor.visitBinaryExpression(self)

    def __repr__(self):
        return "Binary(Left: ({0}), Operator: ({1}), Right: ({2}))".format(self._left, self._operator, self._right)

class Unary(Expression):
    def __init__(self, operator, right):
        self._operator = operator
        self._right = right

    def getOperator(self):
        return self._operator

    def getRight(self):
        return self._right

    def accept(self, visitor):
        return visitor.visitUnaryExpression(self)

    def __repr__(self):
        return "Unary(Operator: ({0}), Right: ({1}))".format(self._operator, self._right)

class Call(Expression):
    def __init__(self, caller, parentheses, arguments):
        self._caller = caller
        self._parentheses = parentheses
        self._arguments = arguments

    def getCaller(self):
        return self._caller

    def getParentheses(self):
        return self._parentheses

    def getArguments(self):
        return self._arguments

    def accept(self, visitor):
        return visitor.visitCallExpression(self)

    def __repr__(self):
        return "Call(Caller: ({0}), Parentheses: ({1}), Arguments: ({2}))".format(self._caller, self._parentheses, self._arguments)

class Get(Expression):
    def __init__(self, object, identifier):
        self._object = object
        self._identifier = identifier

    def getObject(self):
        return self._object

    def getIdentifier(self):
        return self._identifier

    def accept(self, visitor):
        return visitor.visitGetExpression(self)

    def __repr__(self):
        return "Get(Object: ({0}), Identifier: ({1}))".format(self._object, self._identifier)

class This(Expression):
    def __init__(self, keyword):
        self._keyword = keyword

    def getKeyword(self):
        return self._keyword

    def accept(self, visitor):
        return visitor.visitThisExpression(self)

    def __repr__(self):
        return "This(Keyword: ({0}))".format(self._keyword)

class Super(Expression):
    def __init__(self, keyword, method):
        self._keyword = keyword
        self._method = method

    def getKeyword(self):
        return self._keyword

    def getMethod(self):
        return self._method

    def accept(self, visitor):
        return visitor.visitSuperExpression(self)

    def __repr__(self):
        return "Super(Keyword: ({0}), Method: ({1}))".format(self._keyword, self._method)

class GetIndex(Expression):
    def __init__(self, object, indices, brackets):
        self._object = object
        self._indices = indices
        self._brackets = brackets

    def getObject(self):
        return self._object

    def getIndices(self):
        return self._indices

    def getBrackets(self):
        return self._brackets

    def accept(self, visitor):
        return visitor.visitGetIndexExpression(self)

    def __repr__(self):
        return "GetIndex(Object: ({0}), Index: ({1}))".format(self._object, self._indices)

class List(Expression):
    def __init__(self, values):
        self._values = values

    def getValues(self):
        return self._values

    def accept(self, visitor):
        return visitor.visitListExpression(self)

    def __repr__(self):
        return "List(Values: ({0}))".format(self._values)

class SetIndex(Expression):
    def __init__(self, object, indices, brackets, value):
        self._object = object
        self._indices = indices
        self._brackets = brackets
        self._value = value

    def getObject(self):
        return self._object

    def getIndices(self):
        return self._indices

    def getBrackets(self):
        return self._brackets

    def getValue(self):
        return self._value

    def accept(self, visitor):
        return visitor.visitSetIndexExpression(self)

    def __repr__(self):
        return "SetIndex(Object: ({0}), Index: ({1}), Value: ({2}))".format(self._object, self._indices, self._value)