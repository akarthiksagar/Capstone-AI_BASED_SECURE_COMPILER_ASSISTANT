from frontend.ast.ast_visitor import ASTVisitor
from frontend.ast.ast_nodes import (
    FunctionDef,
    Identifier,
    ExpressionStatement
)

from frontend.semantic.symbol_table import (
    SymbolTable,
    Symbol,
    FunctionSymbol
)

from frontend.semantic.type_system import Type
from frontend.semantic.security_label import SecurityLabel, SecurityLevel
from frontend.semantic.builtin_registry import BuiltinRegistry
from frontend.semantic.semantic_errors import SemanticError, Severity

class SemanticAnalyzer(ASTVisitor):

    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        self.current_function = None

    # -------------------------------------------------
    # Error Handling
    # -------------------------------------------------

    def report_error(self, message, node,
                    error_code=None,
                    severity=Severity.ERROR,
                    security_related=False):

        self.errors.append(
            SemanticError(
                message=message,
                line=node.line,
                column=node.column,
                error_code=error_code,
                severity=severity,
                security_related=security_related
            )
        )
    # -------------------------------------------------
    # Program
    # -------------------------------------------------

    def visit_Program(self, node):

        # First pass: register function signatures
        for stmt in node.statements:
            if stmt is None:
                continue
            if isinstance(stmt, FunctionDef):
                self.symbol_table.define_function(
                    FunctionSymbol(stmt.name, stmt.params)
                )

        # Second pass: analyze
        for stmt in node.statements:
            if stmt is None:
                continue
            stmt.accept(self)

    # -------------------------------------------------
    # Function Definition
    # -------------------------------------------------

    def visit_FunctionDef(self, node):

        previous_function = self.current_function
        self.current_function = node.name

        func_symbol = self.symbol_table.resolve_function(node.name)

        self.symbol_table.enter_scope()

        for param in node.params:
            self.symbol_table.define(
                param,
                Symbol(
                    name=param,
                    symbol_type=Type.NONE,
                    security_label=SecurityLabel(SecurityLevel.TRUSTED)
                )
            )

        node.body.accept(self)

        self.symbol_table.exit_scope()

        self.current_function = previous_function

    # -------------------------------------------------
    # Block
    # -------------------------------------------------

    def visit_Block(self, node):
        for stmt in node.statements:
            if stmt is None:
                continue
            stmt.accept(self)

    # -------------------------------------------------
    # Expression Statement
    # -------------------------------------------------

    def visit_ExpressionStatement(self, node):
        node.expression.accept(self)

    # -------------------------------------------------
    # Identifier
    # -------------------------------------------------

    def visit_Identifier(self, node):
        try:
            symbol = self.symbol_table.resolve(node.name)
            node.type = symbol.type
            node.security_label = symbol.security_label
        except Exception:
            self.report_error(f"Undefined variable '{node.name}'", node)
            node.type = Type.NONE
            node.security_label = SecurityLabel(SecurityLevel.TAINTED)

    # -------------------------------------------------
    # Literal
    # -------------------------------------------------

    def visit_Literal(self, node):

        if isinstance(node.value, bool):
            node.type = Type.BOOL
        elif isinstance(node.value, int):
            node.type = Type.INT
        elif isinstance(node.value, float):
            node.type = Type.FLOAT
        elif node.value is None:
            node.type = Type.NONE
        else:
            node.type = Type.STRING

        node.security_label = SecurityLabel(SecurityLevel.TRUSTED)

    # -------------------------------------------------
    # Assignment
    # -------------------------------------------------

    def visit_Assignment(self, node):

        node.value.accept(self)

        value_type = node.value.type
        value_sec = node.value.security_label

        try:
            symbol = self.symbol_table.resolve(node.target.name)
            symbol.type = value_type
            symbol.security_label = value_sec
        except Exception:
            self.symbol_table.define(
                node.target.name,
                Symbol(node.target.name, value_type, value_sec)
            )

        node.type = value_type
        node.security_label = value_sec

    # -------------------------------------------------
    # Unary Operation
    # -------------------------------------------------

    def visit_UnaryOp(self, node):

        node.operand.accept(self)
        operand_type = node.operand.type

        if node.operator in ("+", "-"):
            if operand_type not in (Type.INT, Type.FLOAT):
                self.report_error(
                    f"Unary '{node.operator}' requires numeric type",
                    node
                )
            node.type = operand_type

        elif node.operator == "not":
            if operand_type != Type.BOOL:
                self.report_error(
                    "Logical 'not' requires boolean operand",
                    node
                )
            node.type = Type.BOOL

        else:
            self.report_error(
                f"Unsupported unary operator '{node.operator}'",
                node
            )
            node.type = Type.NONE

        node.security_label = node.operand.security_label

    # -------------------------------------------------
    # Binary Operation
    # -------------------------------------------------

    def visit_BinaryOp(self, node):

        node.left.accept(self)
        node.right.accept(self)

        left = node.left.type
        right = node.right.type
        op = node.operator

        if op in ("+", "-", "*", "/", "%"):

            if left in (Type.INT, Type.FLOAT) and right in (Type.INT, Type.FLOAT):
                node.type = Type.FLOAT if Type.FLOAT in (left, right) else Type.INT

            elif op == "+" and left == Type.STRING and right == Type.STRING:
                node.type = Type.STRING

            else:
                self.report_error(
                    f"Invalid arithmetic operation: {left} {op} {right}",
                    node
                )
                node.type = Type.NONE

        elif op in ("and", "or"):

            if left != Type.BOOL or right != Type.BOOL:
                self.report_error(
                    f"Logical '{op}' requires boolean operands",
                    node
                )

            node.type = Type.BOOL

        else:
            self.report_error(
                f"Unsupported operator '{op}'",
                node
            )
            node.type = Type.NONE

        node.security_label = node.left.security_label.join(
            node.right.security_label
        )

    # -------------------------------------------------
    # Comparison
    # -------------------------------------------------

    def visit_Comparison(self, node):

        node.left.accept(self)
        left_type = node.left.type
        current_security = node.left.security_label

        for comparator in node.comparators:
            comparator.accept(self)

            if comparator.type != left_type:
                self.report_error(
                    f"Comparison type mismatch: {left_type} vs {comparator.type}",
                    comparator
                )

            current_security = current_security.join(
                comparator.security_label
            )

        node.type = Type.BOOL
        node.security_label = current_security

    # -------------------------------------------------
    # Function Call
    # -------------------------------------------------

    def visit_FunctionCall(self, node):

        # Visit arguments first
        for arg in node.args:
            arg.accept(self)

        # Check builtin functions
        if isinstance(node.function, Identifier):

            name = node.function.name

            builtin_result = BuiltinRegistry.handle_builtin(name, node.args)

            if builtin_result:
                node.type, node.security_label = builtin_result

            # -------------------------
            # 🔥 Sink Detection
            # -------------------------
            
            if name == "exec" and node.args:

                arg = node.args[0]

                if arg.security_label.level == SecurityLevel.UNTRUSTED:
                    self.report_error(
                        "Untrusted data passed to exec()",
                        node,
                        security_related=True
                    )

            return

        # -------------------------
        # Normal function resolution
        # -------------------------

        node.function.accept(self)

        try:
            func_symbol = self.symbol_table.resolve_function(node.function.name)
        except:
            self.report_error(
                f"Undefined function '{node.function.name}'",
                node
            )
            node.type = Type.NONE
            node.security_label = SecurityLabel(SecurityLevel.TAINTED)
            return

        node.type = func_symbol.return_type or Type.NONE
        node.security_label = func_symbol.return_security or SecurityLabel(SecurityLevel.TRUSTED)
