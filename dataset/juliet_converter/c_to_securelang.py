from pycparser import c_ast


class CToSecureLangConverter(c_ast.NodeVisitor):

    def __init__(self):
        self.lines = []

    # =====================================================
    # Entry Point
    # =====================================================

    def convert(self, func_node):
        self.lines = []   # 🔥 reset state
        if func_node.body:
            self.visit(func_node.body)
        return "\n".join(self.lines)

    # =====================================================
    # Utility
    # =====================================================

    def emit(self, line):
        self.lines.append(line)

    # =====================================================
    # Compound Block
    # =====================================================

    def visit_Compound(self, node):
        for stmt in node.block_items or []:
            self.visit(stmt)

    # =====================================================
    # Declarations
    # =====================================================

    def visit_Decl(self, node):
        if node.init:
            var = node.name
            value = self._expr(node.init)
            self.emit(f"{var} = {value}")

    # =====================================================
    # Assignments
    # =====================================================

    def visit_Assignment(self, node):
        left = self._expr(node.lvalue)
        right = self._expr(node.rvalue)
        self.emit(f"{left} = {right}")

    # =====================================================
    # Function Calls
    # =====================================================

    def visit_FuncCall(self, node):
        name = self._expr(node.name)

        args = []
        if node.args and hasattr(node.args, "exprs"):
            for arg in node.args.exprs:
                args.append(self._expr(arg))

        arg_str = ", ".join(args)

        self.emit(f"{name}({arg_str})")

    # =====================================================
    # If Statement
    # =====================================================

    def visit_If(self, node):
        cond = self._expr(node.cond)

        self.emit(f"if {cond} {{")
        self.visit(node.iftrue)
        self.emit("}")

        if node.iffalse:
            self.emit("else {")
            self.visit(node.iffalse)
            self.emit("}")

    # =====================================================
    # Return
    # =====================================================

    def visit_Return(self, node):
        if node.expr:
            val = self._expr(node.expr)
            self.emit(f"return {val}")
        else:
            self.emit("return")

    # =====================================================
    # Expression Statement
    # =====================================================

    def visit_ExprList(self, node):
        for expr in node.exprs:
            self.visit(expr)

    # =====================================================
    # Expression Handling
    # =====================================================

    def _expr(self, node):

        if node is None:
            return ""

        # Identifier
        if isinstance(node, c_ast.ID):
            return node.name

        # Constant
        if isinstance(node, c_ast.Constant):
            return node.value

        # Binary Operation
        if isinstance(node, c_ast.BinaryOp):
            left = self._expr(node.left)
            right = self._expr(node.right)
            return f"{left} {node.op} {right}"

        # Unary Operation
        if isinstance(node, c_ast.UnaryOp):
            operand = self._expr(node.expr)
            return f"{node.op}{operand}"

        # Function Call (used inside expressions)
        if isinstance(node, c_ast.FuncCall):
            name = self._expr(node.name)

            args = []
            if node.args and hasattr(node.args, "exprs"):
                for arg in node.args.exprs:
                    args.append(self._expr(arg))

            arg_str = ", ".join(args)
            return f"{name}({arg_str})"

        # Array reference
        if isinstance(node, c_ast.ArrayRef):
            name = self._expr(node.name)
            index = self._expr(node.subscript)
            return f"{name}[{index}]"

        # Fallback
        return "0"