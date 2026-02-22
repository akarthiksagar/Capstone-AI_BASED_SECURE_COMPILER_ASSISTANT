from dataclasses import dataclass, field
from typing import List, Optional, Any, Union
from abc import ABC, abstractmethod


@dataclass
class ASTNode(ABC):
    line: int = 0
    column: int = 0

    @abstractmethod
    def accept(self, visitor: 'ASTVisitor') -> Any:
        pass


@dataclass
class Expression(ASTNode):
    pass


@dataclass
class Statement(ASTNode):
    pass


@dataclass
class Identifier(Expression):
    name: str = ""

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_identifier(self)


@dataclass
class NumberLiteral(Expression):
    value: Union[int, float] = 0

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_number(self)


@dataclass
class StringLiteral(Expression):
    value: str = ""

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_string(self)


@dataclass
class BooleanLiteral(Expression):
    value: bool = False

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_boolean(self)


@dataclass
class NoneLiteral(Expression):
    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_none(self)


@dataclass
class ListLiteral(Expression):
    elements: List[Expression] = field(default_factory=list)

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_list(self)


@dataclass
class DictLiteral(Expression):
    entries: List[tuple] = field(default_factory=list)

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_dict(self)


@dataclass
class BinaryOp(Expression):
    left: Expression = None
    operator: str = ""
    right: Expression = None

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_binary_op(self)


@dataclass
class UnaryOp(Expression):
    operator: str = ""
    operand: Expression = None

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_unary_op(self)


@dataclass
class Call(Expression):
    function: Expression = None
    arguments: List[Expression] = field(default_factory=list)
    keyword_args: dict = field(default_factory=dict)

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_call(self)


@dataclass
class MemberAccess(Expression):
    object: Expression = None
    member: str = ""

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_member_access(self)


@dataclass
class Subscript(Expression):
    object: Expression = None
    index: Expression = None

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_subscript(self)


@dataclass
class Program(ASTNode):
    statements: List[Statement] = field(default_factory=list)

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_program(self)


@dataclass
class Assignment(Statement):
    target: Expression = None
    value: Expression = None

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_assignment(self)


@dataclass
class ExpressionStatement(Statement):
    expression: Expression = None

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_expression_statement(self)


@dataclass
class FunctionDef(Statement):
    name: str = ""
    parameters: List[str] = field(default_factory=list)
    body: List[Statement] = field(default_factory=list)

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_function_def(self)


@dataclass
class Return(Statement):
    value: Optional[Expression] = None

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_return(self)


@dataclass
class If(Statement):
    condition: Expression = None
    then_body: List[Statement] = field(default_factory=list)
    else_body: List[Statement] = field(default_factory=list)

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_if(self)


@dataclass
class While(Statement):
    condition: Expression = None
    body: List[Statement] = field(default_factory=list)

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_while(self)


@dataclass
class For(Statement):
    variable: str = ""
    iterable: Expression = None
    body: List[Statement] = field(default_factory=list)

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_for(self)


@dataclass
class Import(Statement):
    module: str = ""
    names: List[str] = field(default_factory=list)
    is_from: bool = False

    def accept(self, visitor: 'ASTVisitor') -> Any:
        return visitor.visit_import(self)


class ASTVisitor(ABC):

    def visit(self, node: ASTNode) -> Any:
        return node.accept(self)

    def visit_identifier(self, node: Identifier) -> Any:
        pass

    def visit_number(self, node: NumberLiteral) -> Any:
        pass

    def visit_string(self, node: StringLiteral) -> Any:
        pass

    def visit_boolean(self, node: BooleanLiteral) -> Any:
        pass

    def visit_none(self, node: NoneLiteral) -> Any:
        pass

    def visit_list(self, node: ListLiteral) -> Any:
        pass

    def visit_dict(self, node: DictLiteral) -> Any:
        pass

    def visit_binary_op(self, node: BinaryOp) -> Any:
        pass

    def visit_unary_op(self, node: UnaryOp) -> Any:
        pass

    def visit_call(self, node: Call) -> Any:
        pass

    def visit_member_access(self, node: MemberAccess) -> Any:
        pass

    def visit_subscript(self, node: Subscript) -> Any:
        pass

    def visit_program(self, node: Program) -> Any:
        for stmt in node.statements:
            self.visit(stmt)

    def visit_assignment(self, node: Assignment) -> Any:
        pass

    def visit_expression_statement(self, node: ExpressionStatement) -> Any:
        pass

    def visit_function_def(self, node: FunctionDef) -> Any:
        pass

    def visit_return(self, node: Return) -> Any:
        pass

    def visit_if(self, node: If) -> Any:
        pass

    def visit_while(self, node: While) -> Any:
        pass

    def visit_for(self, node: For) -> Any:
        pass

    def visit_import(self, node: Import) -> Any:
        pass


class ASTPrinter(ASTVisitor):

    def __init__(self):
        self.indent = 0

    def _print(self, text: str) -> None:
        print("  " * self.indent + text)

    def visit_program(self, node: Program) -> None:
        self._print("Program")
        self.indent += 1
        for stmt in node.statements:
            self.visit(stmt)
        self.indent -= 1

    def visit_function_def(self, node: FunctionDef) -> None:
        self._print(f"FunctionDef: {node.name}({', '.join(node.parameters)})")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1

    def visit_assignment(self, node: Assignment) -> None:
        self._print("Assignment")
        self.indent += 1
        self._print("Target:")
        self.indent += 1
        self.visit(node.target)
        self.indent -= 1
        self._print("Value:")
        self.indent += 1
        self.visit(node.value)
        self.indent -= 2

    def visit_call(self, node: Call) -> None:
        self._print("Call")
        self.indent += 1
        self._print("Function:")
        self.indent += 1
        self.visit(node.function)
        self.indent -= 1
        if node.arguments:
            self._print("Arguments:")
            self.indent += 1
            for arg in node.arguments:
                self.visit(arg)
            self.indent -= 1
        self.indent -= 1

    def visit_identifier(self, node: Identifier) -> None:
        self._print(f"Identifier: {node.name}")

    def visit_number(self, node: NumberLiteral) -> None:
        self._print(f"Number: {node.value}")

    def visit_string(self, node: StringLiteral) -> None:
        self._print(f"String: \"{node.value}\"")

    def visit_boolean(self, node: BooleanLiteral) -> None:
        self._print(f"Boolean: {node.value}")

    def visit_none(self, node: NoneLiteral) -> None:
        self._print("None")

    def visit_binary_op(self, node: BinaryOp) -> None:
        self._print(f"BinaryOp: {node.operator}")
        self.indent += 1
        self.visit(node.left)
        self.visit(node.right)
        self.indent -= 1

    def visit_unary_op(self, node: UnaryOp) -> None:
        self._print(f"UnaryOp: {node.operator}")
        self.indent += 1
        self.visit(node.operand)
        self.indent -= 1

    def visit_member_access(self, node: MemberAccess) -> None:
        self._print(f"MemberAccess: .{node.member}")
        self.indent += 1
        self.visit(node.object)
        self.indent -= 1

    def visit_if(self, node: If) -> None:
        self._print("If")
        self.indent += 1
        self._print("Condition:")
        self.indent += 1
        self.visit(node.condition)
        self.indent -= 1
        self._print("Then:")
        self.indent += 1
        for stmt in node.then_body:
            self.visit(stmt)
        self.indent -= 1
        if node.else_body:
            self._print("Else:")
            self.indent += 1
            for stmt in node.else_body:
                self.visit(stmt)
            self.indent -= 1
        self.indent -= 1

    def visit_while(self, node: While) -> None:
        self._print("While")
        self.indent += 1
        self._print("Condition:")
        self.indent += 1
        self.visit(node.condition)
        self.indent -= 1
        self._print("Body:")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1
        self.indent -= 1

    def visit_for(self, node: For) -> None:
        self._print(f"For: {node.variable}")
        self.indent += 1
        self._print("Iterable:")
        self.indent += 1
        self.visit(node.iterable)
        self.indent -= 1
        self._print("Body:")
        self.indent += 1
        for stmt in node.body:
            self.visit(stmt)
        self.indent -= 1
        self.indent -= 1

    def visit_return(self, node: Return) -> None:
        self._print("Return")
        if node.value:
            self.indent += 1
            self.visit(node.value)
            self.indent -= 1

    def visit_expression_statement(self, node: ExpressionStatement) -> None:
        self._print("ExpressionStatement")
        self.indent += 1
        self.visit(node.expression)
        self.indent -= 1

    def visit_import(self, node: Import) -> None:
        if node.is_from:
            self._print(f"FromImport: {node.module} -> {', '.join(node.names)}")
        else:
            self._print(f"Import: {node.module}")

    def visit_list(self, node: ListLiteral) -> None:
        self._print("List")
        self.indent += 1
        for elem in node.elements:
            self.visit(elem)
        self.indent -= 1

    def visit_dict(self, node: DictLiteral) -> None:
        self._print("Dict")
        self.indent += 1
        for key, value in node.entries:
            self._print("Entry:")
            self.indent += 1
            self.visit(key)
            self.visit(value)
            self.indent -= 1
        self.indent -= 1

    def visit_subscript(self, node: Subscript) -> None:
        self._print("Subscript")
        self.indent += 1
        self._print("Object:")
        self.indent += 1
        self.visit(node.object)
        self.indent -= 1
        self._print("Index:")
        self.indent += 1
        self.visit(node.index)
        self.indent -= 2
