from .ast_base import ASTNode


# ==========================
# PROGRAM ROOT
# ==========================

class Program(ASTNode):
    def __init__(self, statements):
        super().__init__(0, 0)
        self.statements = statements


# ==========================
# STATEMENTS
# ==========================

class FunctionDef(ASTNode):
    def __init__(self, name, params, body, line, column):
        super().__init__(line, column)
        self.name = name
        self.params = params  # list of strings
        self.body = body


class Block(ASTNode):
    def __init__(self, statements, line, column):
        super().__init__(line, column)
        self.statements = statements


class IfStatement(ASTNode):
    def __init__(self, condition, then_block, else_block, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.then_block = then_block
        self.else_block = else_block


class WhileStatement(ASTNode):
    def __init__(self, condition, body, line, column):
        super().__init__(line, column)
        self.condition = condition
        self.body = body


class ForStatement(ASTNode):
    def __init__(self, variable, iterable, body, line, column):
        super().__init__(line, column)
        self.variable = variable
        self.iterable = iterable
        self.body = body


class ReturnStatement(ASTNode):
    def __init__(self, expression, line, column):
        super().__init__(line, column)
        self.expression = expression


class Assignment(ASTNode):
    def __init__(self, target, value, line, column):
        super().__init__(line, column)
        self.target = target
        self.value = value


class ImportStatement(ASTNode):
    def __init__(self, module, names, line, column):
        super().__init__(line, column)
        self.module = module
        self.names = names  # None or list


class ExpressionStatement(ASTNode):
    def __init__(self, expression, line, column):
        super().__init__(line, column)
        self.expression = expression


# ==========================
# EXPRESSIONS
# ==========================

class BinaryOp(ASTNode):
    def __init__(self, left, operator, right, line, column):
        super().__init__(line, column)
        self.left = left
        self.operator = operator
        self.right = right


class UnaryOp(ASTNode):
    def __init__(self, operator, operand, line, column):
        super().__init__(line, column)
        self.operator = operator
        self.operand = operand


class Comparison(ASTNode):
    def __init__(self, left, operators, comparators, line, column):
        super().__init__(line, column)
        self.left = left
        self.operators = operators
        self.comparators = comparators


class FunctionCall(ASTNode):
    def __init__(self, function, args, keywords, line, column):
        super().__init__(line, column)
        self.function = function
        self.args = args
        self.keywords = keywords  # dict


class MemberAccess(ASTNode):
    def __init__(self, obj, attribute, line, column):
        super().__init__(line, column)
        self.obj = obj
        self.attribute = attribute


class IndexAccess(ASTNode):
    def __init__(self, collection, index, line, column):
        super().__init__(line, column)
        self.collection = collection
        self.index = index


class Identifier(ASTNode):
    def __init__(self, name, line, column):
        super().__init__(line, column)
        self.name = name


# ==========================
# LITERALS
# ==========================

class Literal(ASTNode):
    def __init__(self, value, line, column):
        super().__init__(line, column)
        self.value = value


class ListLiteral(ASTNode):
    def __init__(self, elements, line, column):
        super().__init__(line, column)
        self.elements = elements


class DictLiteral(ASTNode):
    def __init__(self, entries, line, column):
        super().__init__(line, column)
        self.entries = entries  # list of (key, value)