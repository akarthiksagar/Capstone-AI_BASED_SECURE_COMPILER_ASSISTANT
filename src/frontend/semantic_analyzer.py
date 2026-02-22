from typing import List, Optional, Set
from dataclasses import dataclass

from .ast_nodes import (
    ASTVisitor, Program, FunctionDef, Assignment, Call, MemberAccess,
    Identifier, If, While, For, Return, Import, BinaryOp, UnaryOp,
    ExpressionStatement, StringLiteral, NumberLiteral, BooleanLiteral,
    NoneLiteral, ListLiteral, DictLiteral, Subscript
)
from .symbol_table import SymbolTable, SymbolType
from ..utils.errors import CompilerError, ErrorType, CompilationResult


class SemanticAnalyzer(ASTVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors: List[CompilerError] = []
        self.current_function: Optional[str] = None
        self.in_loop: bool = False

    def analyze(self, ast: Program) -> CompilationResult:
        self.errors = []
        self.symbol_table = SymbolTable()
        self.current_function = None
        self.in_loop = False

        self._collect_functions(ast)
        self.visit(ast)

        result = CompilationResult(success=len(self.errors) == 0)
        result.errors = self.errors
        return result

    def _collect_functions(self, ast: Program) -> None:
        for stmt in ast.statements:
            if isinstance(stmt, FunctionDef):
                self.symbol_table.define_function(
                    stmt.name,
                    stmt.parameters,
                    stmt.line,
                    stmt.column
                )

    def _add_error(self, message: str, line: int, column: int = 0) -> None:
        error = CompilerError(
            error_type=ErrorType.SEMANTIC,
            message=message,
            line=line,
            column=column
        )
        self.errors.append(error)

    def visit_program(self, node: Program) -> None:
        for stmt in node.statements:
            self.visit(stmt)

    def visit_function_def(self, node: FunctionDef) -> None:
        self.current_function = node.name

        self.symbol_table.enter_scope(f"function:{node.name}")

        for param in node.parameters:
            self.symbol_table.define_parameter(param, node.line)

        for stmt in node.body:
            self.visit(stmt)

        self.symbol_table.exit_scope()
        self.current_function = None

    def visit_assignment(self, node: Assignment) -> None:
        self.visit(node.value)

        if isinstance(node.target, Identifier):
            existing = self.symbol_table.current_scope.lookup(node.target.name)
            if not existing:
                self.symbol_table.define_variable(
                    node.target.name,
                    node.line,
                    node.column
                )
        elif isinstance(node.target, MemberAccess):
            self.visit(node.target)

    def visit_expression_statement(self, node: ExpressionStatement) -> None:
        self.visit(node.expression)

    def visit_identifier(self, node: Identifier) -> None:
        if not self.symbol_table.is_defined(node.name):
            self._add_error(
                f"Undefined variable or function '{node.name}'",
                node.line,
                node.column
            )

    def visit_call(self, node: Call) -> None:
        if isinstance(node.function, Identifier):
            func_name = node.function.name
            if not self.symbol_table.is_defined(func_name):
                self._add_error(
                    f"Undefined function '{func_name}'",
                    node.line,
                    node.column
                )
            else:
                symbol = self.symbol_table.resolve(func_name)
                if symbol and symbol.symbol_type == SymbolType.FUNCTION:
                    expected = len(symbol.metadata.get('parameters', []))
                    actual = len(node.arguments)
                    if expected != actual:
                        self._add_error(
                            f"Function '{func_name}' expects {expected} arguments, got {actual}",
                            node.line,
                            node.column
                        )

        elif isinstance(node.function, MemberAccess):
            self.visit(node.function.object)

        for arg in node.arguments:
            self.visit(arg)

    def visit_if(self, node: If) -> None:
        self.visit(node.condition)

        self.symbol_table.enter_scope("if:then")
        for stmt in node.then_body:
            self.visit(stmt)
        self.symbol_table.exit_scope()

        if node.else_body:
            self.symbol_table.enter_scope("if:else")
            for stmt in node.else_body:
                self.visit(stmt)
            self.symbol_table.exit_scope()

    def visit_while(self, node: While) -> None:
        old_in_loop = self.in_loop
        self.in_loop = True

        self.visit(node.condition)

        self.symbol_table.enter_scope("while")
        for stmt in node.body:
            self.visit(stmt)
        self.symbol_table.exit_scope()

        self.in_loop = old_in_loop

    def visit_for(self, node: For) -> None:
        old_in_loop = self.in_loop
        self.in_loop = True

        self.visit(node.iterable)

        self.symbol_table.enter_scope("for")
        self.symbol_table.define_variable(node.variable, node.line)

        for stmt in node.body:
            self.visit(stmt)
        self.symbol_table.exit_scope()

        self.in_loop = old_in_loop

    def visit_return(self, node: Return) -> None:
        if self.current_function is None:
            self._add_error(
                "'return' outside of function",
                node.line,
                node.column
            )

        if node.value:
            self.visit(node.value)

    def visit_import(self, node: Import) -> None:
        if node.is_from:
            for name in node.names:
                self.symbol_table.define(
                    name, SymbolType.MODULE, node.line, node.column
                )
        else:
            module_name = node.module.split('.')[0]
            self.symbol_table.define(
                module_name, SymbolType.MODULE, node.line, node.column
            )

    def visit_binary_op(self, node: BinaryOp) -> None:
        self.visit(node.left)
        self.visit(node.right)

    def visit_unary_op(self, node: UnaryOp) -> None:
        self.visit(node.operand)

    def visit_member_access(self, node: MemberAccess) -> None:
        self.visit(node.object)

    def visit_subscript(self, node: Subscript) -> None:
        self.visit(node.object)
        self.visit(node.index)

    def visit_number(self, node: NumberLiteral) -> None:
        pass

    def visit_string(self, node: StringLiteral) -> None:
        pass

    def visit_boolean(self, node: BooleanLiteral) -> None:
        pass

    def visit_none(self, node: NoneLiteral) -> None:
        pass

    def visit_list(self, node: ListLiteral) -> None:
        for elem in node.elements:
            self.visit(elem)

    def visit_dict(self, node: DictLiteral) -> None:
        for key, value in node.entries:
            self.visit(key)
            self.visit(value)
