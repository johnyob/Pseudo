from pyPseudo.callable.PseudoCallable import PseudoCallable
from pyPseudo.callable.PseudoInstance import PseudoInstance
from pyPseudo.callable.PseudoClass import PseudoClass
from pyPseudo.callable.PseudoFunction import PseudoFunction
from pyPseudo.callable.PseudoFunctions import functions

from pyPseudo.error.RuntimeError import RuntimeError
from pyPseudo.error.Return import Return

from pyPseudo.lexer.TokenType import TokenType

from pyPseudo.parser.Expression import ExpressionVisitor
from pyPseudo.parser.Statement import StatementVisitor
import pyPseudo.parser.Expression as Expression

from pyPseudo.interpreter.Environment import Environment
from pyPseudo.interpreter.PseudoList import PseudoList

class Interpreter(ExpressionVisitor, StatementVisitor):
    def __init__(self):
        self.globals = Environment()
        self._environment = self.globals
        self._locals = {}
        self._errors = []

        for function in functions.keys():
            self.globals.define(function, functions[function])


    def interpret(self, statements):
        try:
            for statement in statements:
                self._executeStatement(statement)
        except (RuntimeError, Exception) as error:
            self._error(error)

    def getErrors(self):
        return self._errors

    def visitAssignExpression(self, expression):
        value = self._evaluateExpression(expression.getValue())
        distance = self._locals.get(expression, None)

        if distance != None:
            self._environment.assignAt(distance, expression.getIdentifier(), value)
        else:
            self.globals.assign(expression.getIdentifier(), value)

        return value

    def visitVariableExpression(self, expression):
        return self._lookUpVariable(expression, expression.getIdentifier())

    def visitGroupingExpression(self, expression):
        return self._evaluateExpression(expression.getExpression())

    def visitSetExpression(self, expression):
        object = self._evaluateExpression(expression.getObject())

        if not isinstance(object, PseudoInstance):
            raise RuntimeError(expression.getIdentifer(), "(Set) Only instances have properties.")

        value = self._evaluateExpression(expression.getValue())
        object.set(expression.getIdentifier(), value)
        return value

    def visitLiteralExpression(self, expression):
        return expression.getValue()

    def visitLogicalExpression(self, expression):
        left = self._evaluateExpression(expression.getLeft())

        if expression.getOperator().getType() == TokenType.OR:
            if self._isTruthy(left):
                return left
        else:
            if not self._isTruthy(left):
                return left

        return self._evaluateExpression(expression.getRight())

    def visitBinaryExpression(self, expression):
        left = self._evaluateExpression(expression.getLeft())
        right = self._evaluateExpression(expression.getRight())
        type = expression.getOperator().getType()

        if type == TokenType.GREATER:
            self._checkNumberOperands(expression.getOperator(), left, right)
            return float(left) > float(right)
        elif type == TokenType.GREATER_EQUAL:
            self._checkNumberOperands(expression.getOperator(), left, right)
            return float(left) >= float(right)
        elif type == TokenType.LESS:
            self._checkNumberOperands(expression.getOperator(), left, right)
            return float(left) < float(right)
        elif type == TokenType.LESS_EQUAL:
            self._checkNumberOperands(expression.getOperator(), left, right)
            return float(left) <= float(right)
        elif type == TokenType.NOT_EQUAL:
            return not self._isEqual(left, right)
        elif type == TokenType.EQUAL:
            return self._isEqual(left, right)
        elif type == TokenType.MINUS:
            self._checkNumberOperands(expression.getOperator(), left, right)
            return float(left) - float(right)
        elif type == TokenType.SLASH:
            self._checkNumberOperands(expression.getOperator(), left, right)
            return float(left) / float(right)
        elif type == TokenType.STAR:
            self._checkNumberOperands(expression.getOperator(), left, right)
            return float(left) * float(right)
        elif type == TokenType.PLUS:
            if isinstance(left, float) and isinstance(right, float):
                return float(left) + float(right)

            if isinstance(left, str) and isinstance(right, str):
                return str(left) + str(right)

            if isinstance(left, PseudoList) and isinstance(right, PseudoList):
                return PseudoList(left.getValues() + right.getValues())

            raise RuntimeError(expression.getOperator(), "Operands must be two numbers, two strings or two lists for addition.")

    def visitUnaryExpression(self, expression):
        right = self._evaluateExpression(expression.getRight())
        type = expression.getOperator().getType()

        if type == TokenType.MINUS:
            self._checkNumberOperand(expression.getOperator(), right)
            return - float(right)
        elif type == TokenType.NOT:
            return not self._isTruthy(right)

    def visitCallExpression(self, expression):
        caller = self._evaluateExpression(expression.getCaller())

        arguments = []
        for argument in expression.getArguments():
            arguments.append(self._evaluateExpression(argument))

        if not isinstance(caller, PseudoCallable):
            raise RuntimeError(expression.getParentheses(), "Can only call function and classes.")

        if len(arguments) != caller.arity():
            raise RuntimeError(expression.getParentheses(), "Expected {0} arguments, but got {1} arguments".format(caller.arity(), len(arguments)))

        return caller.call(self, arguments, expression.getParentheses())

    def visitGetExpression(self, expression):
        object = self._evaluateExpression(expression.getObject())
        if isinstance(object, PseudoInstance):
            return object.get(expression.getIdentifier())

        raise RuntimeError(expression.getIdentifier(), "(Get) Only instances have properties.")

    def visitThisExpression(self, expression):
        return self._lookUpVariable(expression, expression.getKeyword())

    def visitSuperExpression(self, expression):
        distance = self._locals.get(expression, None)
        superClass = self._environment.getAt(distance, "SUPER")
        object = self._environment.getAt(distance - 1, "THIS")

        method = superClass.findMethod(object, expression.getMethod().getLexeme())
        if method == None:
            raise RuntimeError(expression.getMethod(), "Undefined property '{0}'.".format(expression.getMethod().getLexeme()))

        return method

    def visitGetIndexExpression(self, expression):
        pseudoList = self._evaluateExpression(expression.getObject())
        if not isinstance(pseudoList, PseudoList):
            raise RuntimeError(expression.getBrackets(), "(Get) Only lists can be indexed.")

        indices = [self._evaluateExpression(index) for index in expression.getIndices()]
        return pseudoList.index(expression.getBrackets(), indices)


    def visitListExpression(self, expression):
        values = []
        for value in expression.getValues():
            values.append(self._evaluateExpression(value))

        return PseudoList(values)

    def visitSetIndexExpression(self, expression):
        pseudoList = self._evaluateExpression(expression.getObject())

        if not isinstance(pseudoList, PseudoList):
            raise RuntimeError(expression.getBrackets(), "(Set) Only lists can be indexed.")

        indices = [self._evaluateExpression(index) for index in expression.getIndices()]
        value = self._evaluateExpression(expression.getValue())
        pseudoList.set(expression.getBrackets(), indices, value)



    def visitClassStatement(self, statement):
        self._environment.define(statement.getIdentifier().getLexeme(), None)
        superClass = None
        if statement.getSuperClass() != None:
            superClass = self._evaluateExpression(statement.getSuperClass())
            if not isinstance(superClass, PseudoClass):
                raise RuntimeError(statement.getSuperClass().getIdentifier(), "Super class must be a class.")
            self._environment = Environment(self._environment)
            self._environment.define("SUPER", superClass)

        methods = {}
        for method in statement.getMethods():
            methods[method.getIdentifier().getLexeme()] = PseudoFunction(method, self._environment, method.getIdentifier().getLexeme() == statement.getIdentifier().getLexeme())

        pseudoClass = PseudoClass(statement.getIdentifier().getLexeme(), superClass, methods)

        if superClass != None:
            self._environment = self._environment.getEnclosing()

        self._environment.assign(statement.getIdentifier(), pseudoClass)

    def visitFunctionStatement(self, statement):
        function = PseudoFunction(statement, self._environment, False)
        self._environment.define(statement.getIdentifier().getLexeme(), function)

    def visitReturnStatement(self, statement):
        value = None
        if statement.getValue() != None:
            value = self._evaluateExpression(statement.getValue())

        raise Return(value)

    def visitExpressionStatement(self, statement):
        self._evaluateExpression(statement.getExpression())

    def visitVariableStatement(self, statement):
        value = None
        if statement.getInitializer() != None:
            value = self._evaluateExpression(statement.getInitializer())

        self._environment.define(statement.getIdentifier().getLexeme(), value)

    def visitIfStatement(self, statement):
        if not isinstance(statement.getCondition(), Expression.Logical):
            raise RuntimeError(statement.getCondition(), "Expect logical expression as operator")

        if self._isTruthy(self._evaluateExpression(statement.getCondition())):
            self.executeBody(statement.getThenBranch(), Environment(self._environment))
        elif statement.getElseBranch() != None:
            self.executeBody(statement.getElseBranch(), Environment(self._environment))

    def visitWhileStatement(self, statement):
        while self._isTruthy(self._evaluateExpression(statement.getCondition())):
            self.executeBody(statement.getBody(), Environment(self._environment))

    def visitForStatement(self, statement):
        self._executeStatement(statement.getInitializer()) #statement
        while self._isTruthy(self._evaluateExpression(statement.getCondition())):
            self.executeBody(statement.getBody(), Environment(self._environment))

    def visitOutputStatement(self, statement):
        value = self._evaluateExpression(statement.getExpression())
        print(self._stringify(value))

    def _evaluateExpression(self, expression):
        return expression.accept(self)

    def _executeStatement(self, statement):
        statement.accept(self)

    def _isTruthy(self, object):
        if object == None:
            return False

        if isinstance(object, bool):
            return bool(object)

        return True

    def _isEqual(self, left, right):
        return left == right

    def _checkNumberOperand(self, operator, operand):
        if isinstance(operand, float):
            return

        raise RuntimeError(operator, "Operand must be a number.")

    def _checkNumberOperands(self, operator, left, right):
        if isinstance(left, float) and isinstance(right, float):
            return

        raise RuntimeError(operator, "Operands must a number.")

    def executeBody(self, statements, environment):
        previous = self._environment
        try:
            self._environment = environment
            for statement in statements:
                self._executeStatement(statement)
        finally:
            self._environment = previous

    def _stringify(self, object):
        if object == None:
            return "NULL"

        if isinstance(object, float):
            text = str(object)
            if text.endswith(".0"):
                text = text[ : -2]
            return text

        if isinstance(object, bool):
            if object == True:
                return "TRUE"
            return "FALSE"

        return str(object)

    def resolve(self, expression, depth):
        self._locals[expression] = depth

    def _lookUpVariable(self, expression, identifier):
        distance = self._locals.get(expression, None)
        if distance != None:
            return self._environment.getAt(distance, identifier.getLexeme())
        else:
            return self.globals.get(identifier)

    def _error(self, error):
        self._errors.append(error)
