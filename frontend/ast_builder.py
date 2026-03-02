from grammar.generated.SecureLangVisitor import SecureLangVisitor
from frontend.ast.ast_nodes import *


class ASTBuilder(SecureLangVisitor):

    # -------------------------
    # Program
    # -------------------------

    def visitProgram(self, ctx):
        statements = []
        for stmt in ctx.statementList().statement():
            node = self.visit(stmt)
            if node:
                statements.append(node)
        return Program(statements)

    # -------------------------
    # Function
    # -------------------------

    def visitFunctionDef(self, ctx):
        name = ctx.IDENTIFIER().getText()

        params = []
        if ctx.parameterList():
            for param in ctx.parameterList().IDENTIFIER():
                params.append(param.getText())

        body = self.visit(ctx.block())

        return FunctionDef(
            name,
            params,
            body,
            ctx.start.line,
            ctx.start.column
        )

    # -------------------------
    # Block
    # -------------------------

    def visitBlock(self, ctx):
        statements = []
        for stmt in ctx.statementList().statement():
            statements.append(self.visit(stmt))

        return Block(statements, ctx.start.line, ctx.start.column)

    # -------------------------
    # Assignment
    # -------------------------

    def visitAssignment(self, ctx):

        # Left side
        if ctx.IDENTIFIER():
            target = Identifier(
                ctx.IDENTIFIER().getText(),
                ctx.start.line,
                ctx.start.column
            )
        else:
            # memberAccess case
            target = self.visit(ctx.memberAccess())

        # Right side
        value = self.visit(ctx.expression())

        return Assignment(
            target,
            value,
            ctx.start.line,
            ctx.start.column
        )
    
    def visitExpression(self, ctx):
        return self.visit(ctx.orExpr())
    # -------------------------
    # Identifier
    # -------------------------

    def visitStatement(self, ctx):

        # Only one child will exist
        child = ctx.getChild(0)

        # Delegate to actual rule
        return self.visit(child)

    def visitAtom(self, ctx):
        if ctx.IDENTIFIER():
            return Identifier(
                ctx.IDENTIFIER().getText(),
                ctx.start.line,
                ctx.start.column
            )

        if ctx.NUMBER():
            return Literal(
                ctx.NUMBER().getText(),
                ctx.start.line,
                ctx.start.column
            )

        if ctx.STRING():
            return Literal(
                ctx.STRING().getText(),
                ctx.start.line,
                ctx.start.column
            )


    def visitOrExpr(self, ctx):
        node = self.visit(ctx.andExpr(0))

        for i in range(1, len(ctx.andExpr())):
            right = self.visit(ctx.andExpr(i))
            node = BinaryOp(
                node,
                "or",
                right,
                ctx.start.line,
                ctx.start.column
            )

        return node

    def visitAndExpr(self, ctx):
        node = self.visit(ctx.notExpr(0))

        for i in range(1, len(ctx.notExpr())):
            right = self.visit(ctx.notExpr(i))
            node = BinaryOp(
                node,
                "and",
                right,
                ctx.start.line,
                ctx.start.column
            )

        return node


    def visitNotExpr(self, ctx):
        if ctx.NOT():
            operand = self.visit(ctx.notExpr())
            return UnaryOp(
                "not",
                operand,
                ctx.start.line,
                ctx.start.column
            )

        return self.visit(ctx.comparison())


    def visitComparison(self, ctx):
        left = self.visit(ctx.addExpr(0))

        if len(ctx.addExpr()) == 1:
            return left

        operators = []
        comparators = []

        for i in range(1, len(ctx.addExpr())):
            operators.append(ctx.compOp(i - 1).getText())
            comparators.append(self.visit(ctx.addExpr(i)))

        return Comparison(
            left,
            operators,
            comparators,
            ctx.start.line,
            ctx.start.column
        )

    def visitAddExpr(self, ctx):
        node = self.visit(ctx.mulExpr(0))

        for i in range(1, len(ctx.mulExpr())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.mulExpr(i))
            node = BinaryOp(
                node,
                op,
                right,
                ctx.start.line,
                ctx.start.column
            )

        return node

    def visitMulExpr(self, ctx):
        node = self.visit(ctx.unaryExpr(0))

        for i in range(1, len(ctx.unaryExpr())):
            op = ctx.getChild(2 * i - 1).getText()
            right = self.visit(ctx.unaryExpr(i))
            node = BinaryOp(
                node,
                op,
                right,
                ctx.start.line,
                ctx.start.column
            )

        return node

    def visitUnaryExpr(self, ctx):
        if ctx.getChildCount() == 2:
            op = ctx.getChild(0).getText()
            operand = self.visit(ctx.unaryExpr())
            return UnaryOp(
                op,
                operand,
                ctx.start.line,
                ctx.start.column
            )

        return self.visit(ctx.powerExpr())

    def visitPowerExpr(self, ctx):
        base = self.visit(ctx.atomExpr(0))

        if len(ctx.atomExpr()) == 2:
            exponent = self.visit(ctx.atomExpr(1))
            return BinaryOp(
                base,
                "**",
                exponent,
                ctx.start.line,
                ctx.start.column
            )

        return base

    def visitAtomExpr(self, ctx):
        node = self.visit(ctx.atom())

        for trailer in ctx.trailer():
            node = self.handle_trailer(node, trailer)

        return node

    def handle_trailer(self, node, trailer_ctx):

        # Function call
        symbol = trailer_ctx.getChild(0).getText()
        if symbol == '(':
            args = []
            keywords = {}

            if trailer_ctx.argumentList():
                for arg in trailer_ctx.argumentList().argument():
                    if arg.ASSIGN():
                        key = arg.IDENTIFIER().getText()
                        value = self.visit(arg.expression())
                        keywords[key] = value
                    else:
                        args.append(self.visit(arg.expression()))

            return FunctionCall(
                node,
                args,
                keywords,
                trailer_ctx.start.line,
                trailer_ctx.start.column
            )

        # Index access
        elif symbol == '[':
            index = self.visit(trailer_ctx.expression())
            return IndexAccess(
                node,
                index,
                trailer_ctx.start.line,
                trailer_ctx.start.column
            )

        # Member access
        elif symbol == '.':
            attribute = trailer_ctx.IDENTIFIER().getText()
            return MemberAccess(
                node,
                attribute,
                trailer_ctx.start.line,
                trailer_ctx.start.column
            )
        
    def visitAtom(self, ctx):

        if ctx.IDENTIFIER():
            return Identifier(
                ctx.IDENTIFIER().getText(),
                ctx.start.line,
                ctx.start.column
            )

        if ctx.NUMBER():
            return Literal(
                ctx.NUMBER().getText(),
                ctx.start.line,
                ctx.start.column
            )

        if ctx.STRING():
            return Literal(
                ctx.STRING().getText(),
                ctx.start.line,
                ctx.start.column
            )

        if ctx.TRUE():
            return Literal(True, ctx.start.line, ctx.start.column)

        if ctx.FALSE():
            return Literal(False, ctx.start.line, ctx.start.column)

        if ctx.NONE():
            return Literal(None, ctx.start.line, ctx.start.column)

        if ctx.listLiteral():
            return self.visit(ctx.listLiteral())

        if ctx.dictLiteral():
            return self.visit(ctx.dictLiteral())

        if ctx.expression():
            return self.visit(ctx.expression())
        

    def visitListLiteral(self, ctx):
        elements = []

        if ctx.expression():
            for expr in ctx.expression():
                elements.append(self.visit(expr))

        return ListLiteral(
            elements,
            ctx.start.line,
            ctx.start.column
        )

    def visitDictLiteral(self, ctx):
        entries = []

        if ctx.dictEntry():
            for entry in ctx.dictEntry():
                key = self.visit(entry.expression(0))
                value = self.visit(entry.expression(1))
                entries.append((key, value))

        return DictLiteral(
            entries,
            ctx.start.line,
            ctx.start.column
        )

    def visitIfStatement(self, ctx):

        # Condition
        condition = self.visit(ctx.expression())

        # Then block (first block)
        then_block = self.visit(ctx.block(0))

        # Else block (optional)
        else_block = None

        # If grammar matched else
        if ctx.block(1):  # normal else { ... }
            else_block = self.visit(ctx.block(1))

        elif ctx.ifStatement():  # else if (...)
            else_block = self.visit(ctx.ifStatement())

        return IfStatement(
            condition,
            then_block,
            else_block,
            ctx.start.line,
            ctx.start.column
        )
    def generic_visit(self,node):
        return None