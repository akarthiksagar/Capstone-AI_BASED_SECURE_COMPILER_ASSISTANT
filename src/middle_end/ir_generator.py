from typing import List, Optional, Dict, Any

from ..frontend.ast_nodes import (
    ASTVisitor, Program, FunctionDef, Assignment, ExpressionStatement,
    Return, If, While, For, Import, Call, MemberAccess, Subscript,
    BinaryOp, UnaryOp, Identifier, NumberLiteral, StringLiteral,
    BooleanLiteral, NoneLiteral, ListLiteral, DictLiteral, Expression
)
from .ir import (
    IRProgram, IRFunction, IRInstruction, IROpCode,
    IRTemp, IRConst, IRVar, IRLabel, IRBuilder, IRValue
)


class IRGenerator(ASTVisitor):

    def __init__(self):
        self.builder = IRBuilder()
        self.program = IRProgram()
        self.current_function: Optional[IRFunction] = None
        self.instructions: List[IRInstruction] = []
        self.break_labels: List[IRLabel] = []
        self.continue_labels: List[IRLabel] = []

    def generate(self, ast: Program) -> IRProgram:
        self.program = IRProgram()
        self.current_function = None
        self.instructions = []
        self.break_labels = []
        self.continue_labels = []

        self.visit(ast)

        self.program.global_instructions = self.instructions
        return self.program

    def _emit(self, instr: IRInstruction) -> None:
        instr.metadata.setdefault("source_line", instr.line)
        instr.metadata.setdefault("source_column", 0)
        self.instructions.append(instr)

    def _current_instructions(self) -> List[IRInstruction]:
        return self.instructions

    def visit_program(self, node: Program) -> None:
        for stmt in node.statements:
            self.visit(stmt)

    def visit_function_def(self, node: FunctionDef) -> IRFunction:
        old_instructions = self.instructions
        old_function = self.current_function

        func = IRFunction(
            name=node.name,
            parameters=node.parameters
        )
        self.current_function = func
        self.instructions = []

        self._emit(self.builder.func_begin(node.name, node.parameters, node.line))

        for stmt in node.body:
            self.visit(stmt)

        self._emit(self.builder.func_end(node.line))

        func.instructions = self.instructions
        self.program.functions.append(func)

        self.instructions = old_instructions
        self.current_function = old_function

        return func

    def visit_assignment(self, node: Assignment) -> None:
        value = self.visit_expression(node.value)

        if isinstance(node.target, Identifier):
            dest = self.builder.var(node.target.name)
            self._emit(self.builder.assign(dest, value, node.line))
        elif isinstance(node.target, MemberAccess):
            base = self.visit_expression(node.target.object)
            self._emit(IRInstruction(
                IROpCode.STORE,
                arg1=base,
                arg2=self.builder.var(node.target.member),
                dest=value,
                line=node.line
            ))

    def visit_expression_statement(self, node: ExpressionStatement) -> None:
        self.visit_expression(node.expression)

    def visit_expression(self, node: Expression) -> IRValue:
        if isinstance(node, Identifier):
            return self.visit_identifier(node)
        elif isinstance(node, NumberLiteral):
            return self.visit_number(node)
        elif isinstance(node, StringLiteral):
            return self.visit_string(node)
        elif isinstance(node, BooleanLiteral):
            return self.visit_boolean(node)
        elif isinstance(node, NoneLiteral):
            return self.visit_none(node)
        elif isinstance(node, BinaryOp):
            return self.visit_binary_op(node)
        elif isinstance(node, UnaryOp):
            return self.visit_unary_op(node)
        elif isinstance(node, Call):
            return self.visit_call(node)
        elif isinstance(node, MemberAccess):
            return self.visit_member_access(node)
        elif isinstance(node, Subscript):
            return self.visit_subscript(node)
        elif isinstance(node, ListLiteral):
            return self.visit_list(node)
        elif isinstance(node, DictLiteral):
            return self.visit_dict(node)
        else:
            return self.builder.const(None, "null")

    def visit_identifier(self, node: Identifier) -> IRValue:
        return self.builder.var(node.name)

    def visit_number(self, node: NumberLiteral) -> IRValue:
        return self.builder.const(node.value)

    def visit_string(self, node: StringLiteral) -> IRValue:
        return self.builder.const(node.value, "string")

    def visit_boolean(self, node: BooleanLiteral) -> IRValue:
        return self.builder.const(node.value, "bool")

    def visit_none(self, node: NoneLiteral) -> IRValue:
        return self.builder.const(None, "null")

    def visit_binary_op(self, node: BinaryOp) -> IRValue:
        left = self.visit_expression(node.left)
        right = self.visit_expression(node.right)

        temp = self.builder.new_temp()

        if node.operator == '+':
            if (isinstance(left, IRConst) and left.value_type == "string" and
                isinstance(right, IRConst) and right.value_type == "string"):
                result = self.builder.const(left.value + right.value, "string")
                self._emit(self.builder.assign(temp, result, node.line))
                return temp

        self._emit(self.builder.binary_op(node.operator, temp, left, right, node.line))
        return temp

    def visit_unary_op(self, node: UnaryOp) -> IRValue:
        operand = self.visit_expression(node.operand)
        temp = self.builder.new_temp()
        self._emit(self.builder.unary_op(node.operator, temp, operand, node.line))
        return temp

    def visit_call(self, node: Call) -> IRValue:
        args = [self.visit_expression(arg) for arg in node.arguments]

        if isinstance(node.function, Identifier):
            func = self.builder.var(node.function.name)
        elif isinstance(node.function, MemberAccess):
            func = self.visit_member_access(node.function)
        else:
            func = self.visit_expression(node.function)

        temp = self.builder.new_temp()
        self._emit(self.builder.call(temp, func, args, node.line))
        return temp

    def visit_member_access(self, node: MemberAccess) -> IRValue:
        base = self.visit_expression(node.object)
        temp = self.builder.new_temp()
        self._emit(self.builder.member(temp, base, node.member, node.line))
        return temp

    def visit_subscript(self, node: Subscript) -> IRValue:
        base = self.visit_expression(node.object)
        index = self.visit_expression(node.index)
        temp = self.builder.new_temp()
        self._emit(self.builder.index(temp, base, index, node.line))
        return temp

    def visit_if(self, node: If) -> None:
        else_label = self.builder.new_label("else")
        end_label = self.builder.new_label("endif")

        cond = self.visit_expression(node.condition)

        if node.else_body:
            self._emit(self.builder.jump_if_not(cond, else_label, node.line))
        else:
            self._emit(self.builder.jump_if_not(cond, end_label, node.line))

        for stmt in node.then_body:
            self.visit(stmt)

        if node.else_body:
            self._emit(self.builder.jump(end_label, node.line))
            self._emit(self.builder.label(else_label, node.line))
            for stmt in node.else_body:
                self.visit(stmt)

        self._emit(self.builder.label(end_label, node.line))

    def visit_while(self, node: While) -> None:
        start_label = self.builder.new_label("while_start")
        end_label = self.builder.new_label("while_end")

        self.break_labels.append(end_label)
        self.continue_labels.append(start_label)

        self._emit(self.builder.label(start_label, node.line))

        cond = self.visit_expression(node.condition)
        self._emit(self.builder.jump_if_not(cond, end_label, node.line))

        for stmt in node.body:
            self.visit(stmt)

        self._emit(self.builder.jump(start_label, node.line))
        self._emit(self.builder.label(end_label, node.line))

        self.break_labels.pop()
        self.continue_labels.pop()

    def visit_for(self, node: For) -> None:
        start_label = self.builder.new_label("for_start")
        end_label = self.builder.new_label("for_end")

        self.break_labels.append(end_label)
        self.continue_labels.append(start_label)

        iterable = self.visit_expression(node.iterable)
        iter_temp = self.builder.new_temp()
        index_temp = self.builder.new_temp()

        self._emit(self.builder.assign(index_temp, self.builder.const(0), node.line))
        self._emit(self.builder.label(start_label, node.line))

        loop_var = self.builder.var(node.variable)
        self._emit(self.builder.index(loop_var, iterable, index_temp, node.line))

        for stmt in node.body:
            self.visit(stmt)

        new_index = self.builder.new_temp()
        self._emit(self.builder.binary_op('+', new_index, index_temp, self.builder.const(1), node.line))
        self._emit(self.builder.assign(index_temp, new_index, node.line))

        self._emit(self.builder.jump(start_label, node.line))
        self._emit(self.builder.label(end_label, node.line))

        self.break_labels.pop()
        self.continue_labels.pop()

    def visit_return(self, node: Return) -> None:
        value = None
        if node.value:
            value = self.visit_expression(node.value)
        self._emit(self.builder.ret(value, node.line))

    def visit_import(self, node: Import) -> None:
        if node.is_from:
            for name in node.names:
                self.program.global_vars[name] = self.builder.var(name)
        else:
            module_name = node.module.split('.')[0]
            self.program.global_vars[module_name] = self.builder.var(module_name)

    def visit_list(self, node: ListLiteral) -> IRValue:
        temp = self.builder.new_temp()
        elements = [self.visit_expression(e) for e in node.elements]
        self._emit(IRInstruction(
            IROpCode.ALLOC,
            dest=temp,
            line=node.line,
            metadata={'type': 'list', 'elements': elements}
        ))
        return temp

    def visit_dict(self, node: DictLiteral) -> IRValue:
        temp = self.builder.new_temp()
        entries = [(self.visit_expression(k), self.visit_expression(v))
                   for k, v in node.entries]
        self._emit(IRInstruction(
            IROpCode.ALLOC,
            dest=temp,
            line=node.line,
            metadata={'type': 'dict', 'entries': entries}
        ))
        return temp
