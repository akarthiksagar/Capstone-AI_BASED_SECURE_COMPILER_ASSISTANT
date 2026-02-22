import sys
import os

grammar_path = os.path.join(os.path.dirname(__file__), 'grammar')
if grammar_path not in sys.path:
    sys.path.insert(0, grammar_path)

from typing import List, Optional, Any

from .ast_nodes import (
    Program, FunctionDef, Assignment, ExpressionStatement, Return,
    If, While, For, Import, Call, MemberAccess, Subscript,
    BinaryOp, UnaryOp, Identifier, NumberLiteral, StringLiteral,
    BooleanLiteral, NoneLiteral, ListLiteral, DictLiteral,
    Statement, Expression
)


class ASTBuilder:

    def __init__(self):
        self.source_lines: List[str] = []

    def build(self, tree, source: str = "") -> Program:
        self.source_lines = source.split('\n') if source else []
        return self.visit_program(tree)

    def visit_program(self, ctx) -> Program:
        statements = []
        for child in ctx.getChildren():
            stmt = self.visit_statement(child)
            if stmt:
                statements.append(stmt)
        return Program(statements=statements, line=1, column=0)

    def visit_statement(self, ctx) -> Optional[Statement]:
        rule_name = self._get_rule_name(ctx)

        if rule_name == 'functionDef':
            return self.visit_function_def(ctx)
        elif rule_name == 'ifStatement':
            return self.visit_if_statement(ctx)
        elif rule_name == 'whileStatement':
            return self.visit_while_statement(ctx)
        elif rule_name == 'forStatement':
            return self.visit_for_statement(ctx)
        elif rule_name == 'returnStatement':
            return self.visit_return_statement(ctx)
        elif rule_name == 'assignment':
            return self.visit_assignment(ctx)
        elif rule_name == 'expressionStatement':
            return self.visit_expression_statement(ctx)
        elif rule_name == 'importStatement':
            return self.visit_import_statement(ctx)
        elif rule_name == 'statement':
            for child in ctx.getChildren():
                result = self.visit_statement(child)
                if result:
                    return result
        return None

    def visit_function_def(self, ctx) -> FunctionDef:
        line, col = self._get_location(ctx)

        name = ctx.IDENTIFIER().getText()

        parameters = []
        param_list = ctx.parameterList()
        if param_list:
            for param in param_list.IDENTIFIER():
                parameters.append(param.getText())

        body = self.visit_block(ctx.block())

        return FunctionDef(
            name=name,
            parameters=parameters,
            body=body,
            line=line,
            column=col
        )

    def visit_block(self, ctx) -> List[Statement]:
        statements = []
        for child in ctx.getChildren():
            stmt = self.visit_statement(child)
            if stmt:
                statements.append(stmt)
        return statements

    def visit_if_statement(self, ctx) -> If:
        line, col = self._get_location(ctx)

        condition = self.visit_expression(ctx.expression())

        blocks = ctx.block()
        then_body = self.visit_block(blocks[0]) if blocks else []

        else_body = []
        if len(blocks) > 1:
            else_body = self.visit_block(blocks[1])
        elif ctx.ifStatement():
            else_body = [self.visit_if_statement(ctx.ifStatement())]

        return If(
            condition=condition,
            then_body=then_body,
            else_body=else_body,
            line=line,
            column=col
        )

    def visit_while_statement(self, ctx) -> While:
        line, col = self._get_location(ctx)

        condition = self.visit_expression(ctx.expression())
        body = self.visit_block(ctx.block())

        return While(
            condition=condition,
            body=body,
            line=line,
            column=col
        )

    def visit_for_statement(self, ctx) -> For:
        line, col = self._get_location(ctx)

        variable = ctx.IDENTIFIER().getText()
        iterable = self.visit_expression(ctx.expression())
        body = self.visit_block(ctx.block())

        return For(
            variable=variable,
            iterable=iterable,
            body=body,
            line=line,
            column=col
        )

    def visit_return_statement(self, ctx) -> Return:
        line, col = self._get_location(ctx)

        value = None
        if ctx.expression():
            value = self.visit_expression(ctx.expression())

        return Return(value=value, line=line, column=col)

    def visit_assignment(self, ctx) -> Assignment:
        line, col = self._get_location(ctx)

        if ctx.IDENTIFIER():
            target = Identifier(name=ctx.IDENTIFIER().getText(), line=line, column=col)
        else:
            target = self.visit_member_access(ctx.memberAccess())

        value = self.visit_expression(ctx.expression())

        return Assignment(target=target, value=value, line=line, column=col)

    def visit_expression_statement(self, ctx) -> ExpressionStatement:
        line, col = self._get_location(ctx)
        expr = self.visit_expression(ctx.expression())
        return ExpressionStatement(expression=expr, line=line, column=col)

    def visit_import_statement(self, ctx) -> Import:
        line, col = self._get_location(ctx)

        is_from = ctx.FROM() is not None

        dotted_name = ctx.dottedName()
        module = '.'.join([id.getText() for id in dotted_name.IDENTIFIER()])

        names = []
        if is_from:
            for id_node in ctx.IDENTIFIER():
                names.append(id_node.getText())

        return Import(
            module=module,
            names=names,
            is_from=is_from,
            line=line,
            column=col
        )

    def visit_expression(self, ctx) -> Expression:
        rule_name = self._get_rule_name(ctx)

        if rule_name == 'expression':
            return self.visit_expression(ctx.orExpr())
        elif rule_name == 'orExpr':
            return self.visit_or_expr(ctx)
        elif rule_name == 'andExpr':
            return self.visit_and_expr(ctx)
        elif rule_name == 'notExpr':
            return self.visit_not_expr(ctx)
        elif rule_name == 'comparison':
            return self.visit_comparison(ctx)
        elif rule_name == 'addExpr':
            return self.visit_add_expr(ctx)
        elif rule_name == 'mulExpr':
            return self.visit_mul_expr(ctx)
        elif rule_name == 'unaryExpr':
            return self.visit_unary_expr(ctx)
        elif rule_name == 'powerExpr':
            return self.visit_power_expr(ctx)
        elif rule_name == 'atomExpr':
            return self.visit_atom_expr(ctx)
        elif rule_name == 'atom':
            return self.visit_atom(ctx)

        for child in ctx.getChildren():
            result = self.visit_expression(child)
            if result:
                return result

        return None

    def visit_or_expr(self, ctx) -> Expression:
        exprs = ctx.andExpr()
        if len(exprs) == 1:
            return self.visit_and_expr(exprs[0])

        line, col = self._get_location(ctx)
        left = self.visit_and_expr(exprs[0])
        for i in range(1, len(exprs)):
            right = self.visit_and_expr(exprs[i])
            left = BinaryOp(left=left, operator='or', right=right, line=line, column=col)
        return left

    def visit_and_expr(self, ctx) -> Expression:
        exprs = ctx.notExpr()
        if len(exprs) == 1:
            return self.visit_not_expr(exprs[0])

        line, col = self._get_location(ctx)
        left = self.visit_not_expr(exprs[0])
        for i in range(1, len(exprs)):
            right = self.visit_not_expr(exprs[i])
            left = BinaryOp(left=left, operator='and', right=right, line=line, column=col)
        return left

    def visit_not_expr(self, ctx) -> Expression:
        if ctx.NOT():
            line, col = self._get_location(ctx)
            operand = self.visit_not_expr(ctx.notExpr())
            return UnaryOp(operator='not', operand=operand, line=line, column=col)
        return self.visit_comparison(ctx.comparison())

    def visit_comparison(self, ctx) -> Expression:
        exprs = ctx.addExpr()
        if len(exprs) == 1:
            return self.visit_add_expr(exprs[0])

        line, col = self._get_location(ctx)
        ops = ctx.compOp()

        left = self.visit_add_expr(exprs[0])
        for i, op in enumerate(ops):
            right = self.visit_add_expr(exprs[i + 1])
            op_text = self._get_comp_op_text(op)
            left = BinaryOp(left=left, operator=op_text, right=right, line=line, column=col)
        return left

    def _get_comp_op_text(self, ctx) -> str:
        text = ctx.getText()
        if text == 'notin':
            return 'not in'
        return text

    def visit_add_expr(self, ctx) -> Expression:
        exprs = ctx.mulExpr()
        if len(exprs) == 1:
            return self.visit_mul_expr(exprs[0])

        line, col = self._get_location(ctx)
        left = self.visit_mul_expr(exprs[0])

        ops = []
        for child in ctx.getChildren():
            text = child.getText()
            if text in ['+', '-']:
                ops.append(text)

        for i, op in enumerate(ops):
            right = self.visit_mul_expr(exprs[i + 1])
            left = BinaryOp(left=left, operator=op, right=right, line=line, column=col)
        return left

    def visit_mul_expr(self, ctx) -> Expression:
        exprs = ctx.unaryExpr()
        if len(exprs) == 1:
            return self.visit_unary_expr(exprs[0])

        line, col = self._get_location(ctx)
        left = self.visit_unary_expr(exprs[0])

        ops = []
        for child in ctx.getChildren():
            text = child.getText()
            if text in ['*', '/', '//', '%']:
                ops.append(text)

        for i, op in enumerate(ops):
            right = self.visit_unary_expr(exprs[i + 1])
            left = BinaryOp(left=left, operator=op, right=right, line=line, column=col)
        return left

    def visit_unary_expr(self, ctx) -> Expression:
        first_child = ctx.getChild(0)
        if first_child and first_child.getText() in ['-', '+']:
            line, col = self._get_location(ctx)
            operand = self.visit_unary_expr(ctx.unaryExpr())
            return UnaryOp(operator=first_child.getText(), operand=operand, line=line, column=col)

        return self.visit_power_expr(ctx.powerExpr())

    def visit_power_expr(self, ctx) -> Expression:
        exprs = ctx.atomExpr()
        if len(exprs) == 1:
            return self.visit_atom_expr(exprs[0])

        line, col = self._get_location(ctx)
        left = self.visit_atom_expr(exprs[0])
        right = self.visit_atom_expr(exprs[1])
        return BinaryOp(left=left, operator='**', right=right, line=line, column=col)

    def visit_atom_expr(self, ctx) -> Expression:
        line, col = self._get_location(ctx)

        base = self.visit_atom(ctx.atom())

        for trailer in ctx.trailer():
            base = self.visit_trailer(base, trailer)

        return base

    def visit_trailer(self, base: Expression, ctx) -> Expression:
        line, col = self._get_location(ctx)

        if ctx.argumentList() is not None or ctx.getText().startswith('('):
            args = []
            kwargs = {}
            if ctx.argumentList():
                for arg in ctx.argumentList().argument():
                    if arg.IDENTIFIER() and arg.expression():
                        name = arg.IDENTIFIER().getText()
                        value = self.visit_expression(arg.expression())
                        kwargs[name] = value
                    else:
                        args.append(self.visit_expression(arg.expression()))

            return Call(
                function=base,
                arguments=args,
                keyword_args=kwargs,
                line=line,
                column=col
            )

        if ctx.expression():
            index = self.visit_expression(ctx.expression())
            return Subscript(object=base, index=index, line=line, column=col)

        if ctx.IDENTIFIER():
            member = ctx.IDENTIFIER().getText()
            return MemberAccess(object=base, member=member, line=line, column=col)

        return base

    def visit_atom(self, ctx) -> Expression:
        line, col = self._get_location(ctx)

        if ctx.IDENTIFIER():
            return Identifier(name=ctx.IDENTIFIER().getText(), line=line, column=col)

        if ctx.NUMBER():
            text = ctx.NUMBER().getText()
            value = float(text) if '.' in text else int(text)
            return NumberLiteral(value=value, line=line, column=col)

        if ctx.STRING():
            text = ctx.STRING().getText()
            value = text[1:-1]
            value = value.replace('\\n', '\n').replace('\\t', '\t').replace('\\\\', '\\')
            return StringLiteral(value=value, line=line, column=col)

        if ctx.TRUE():
            return BooleanLiteral(value=True, line=line, column=col)
        if ctx.FALSE():
            return BooleanLiteral(value=False, line=line, column=col)

        if ctx.NONE():
            return NoneLiteral(line=line, column=col)

        if ctx.listLiteral():
            return self.visit_list_literal(ctx.listLiteral())

        if ctx.dictLiteral():
            return self.visit_dict_literal(ctx.dictLiteral())

        if ctx.expression():
            return self.visit_expression(ctx.expression())

        return None

    def visit_list_literal(self, ctx) -> ListLiteral:
        line, col = self._get_location(ctx)
        elements = []
        for expr in ctx.expression():
            elements.append(self.visit_expression(expr))
        return ListLiteral(elements=elements, line=line, column=col)

    def visit_dict_literal(self, ctx) -> DictLiteral:
        line, col = self._get_location(ctx)
        entries = []
        for entry in ctx.dictEntry():
            key = self.visit_expression(entry.expression(0))
            value = self.visit_expression(entry.expression(1))
            entries.append((key, value))
        return DictLiteral(entries=entries, line=line, column=col)

    def visit_member_access(self, ctx) -> MemberAccess:
        line, col = self._get_location(ctx)

        ids = list(ctx.IDENTIFIER())
        base = Identifier(name=ids[0].getText(), line=line, column=col)

        for i in range(1, len(ids)):
            base = MemberAccess(
                object=base,
                member=ids[i].getText(),
                line=line,
                column=col
            )

        return base

    def _get_rule_name(self, ctx) -> str:
        if hasattr(ctx, 'getRuleIndex'):
            class_name = ctx.__class__.__name__
            if class_name.endswith('Context'):
                name = class_name[:-7]
                return name[0].lower() + name[1:]
        return ""

    def _get_location(self, ctx) -> tuple:
        if hasattr(ctx, 'start') and ctx.start:
            return (ctx.start.line, ctx.start.column)
        return (0, 0)
