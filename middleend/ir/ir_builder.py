from frontend.ast.ast_visitor import ASTVisitor
from frontend.ast.ast_nodes import (
    Identifier,
    Literal,
    BinaryOp,
    UnaryOp,
    Assignment,
    FunctionCall,
    IfStatement,
    WhileStatement,
    ReturnStatement,
    Block,
    ExpressionStatement
)

from middleend.ir.ir_instructions import (
    IRAssign,
    IRBinaryOp,
    IRCall,
    IRReturn,
    IRBranch,
    IRJump
)

from middleend.cfg.cfg_builder import ControlFlowGraph


class IRBuilder(ASTVisitor):

    def __init__(self):
        self.cfg = ControlFlowGraph()
        self.current_block = self.cfg.new_block("entry")
        self.temp_counter = 0

    # =====================================================
    # Utility
    # =====================================================

    def new_temp(self):
        self.temp_counter += 1
        return f"t{self.temp_counter}"

    # =====================================================
    # Program
    # =====================================================

    def visit_Program(self, node):

        self.cfg = ControlFlowGraph()

        entry_block = self.cfg.new_block("entry")
        self.cfg.entry = entry_block
        self.current_block = entry_block

        for stmt in node.statements:
            stmt.accept(self)

        # Create explicit exit block
        exit_block = self.cfg.new_block("exit")
        self.cfg.exit = exit_block

        # Connect last block to exit
        if self.current_block != exit_block:
            self.current_block.add_successor(exit_block)

        return self.cfg

    # =====================================================
    # Block
    # =====================================================

    def visit_Block(self, node):
        for stmt in node.statements:
            stmt.accept(self)

    # =====================================================
    # Expression Statement
    # =====================================================

    def visit_ExpressionStatement(self, node):
        node.expression.accept(self)

    # =====================================================
    # Literal
    # =====================================================

    def visit_Literal(self, node):
        temp = self.new_temp()

        instr = IRAssign(temp, node.value)
        instr.security_label = node.security_label

        self.current_block.add_instruction(instr)

        return temp

    # =====================================================
    # Identifier
    # =====================================================

    def visit_Identifier(self, node):
        return node.name

    # =====================================================
    # Assignment
    # =====================================================

    def visit_Assignment(self, node):
        value = node.value.accept(self)

        instr = IRAssign(node.target.name, value)
        instr.security_label = node.security_label

        self.current_block.add_instruction(instr)

        return node.target.name

    # =====================================================
    # Unary Operation
    # =====================================================

    def visit_UnaryOp(self, node):
        operand = node.operand.accept(self)
        temp = self.new_temp()

        instr = IRBinaryOp(temp, "0", node.operator, operand)
        instr.security_label = node.security_label

        self.current_block.add_instruction(instr)

        return temp

    # =====================================================
    # Binary Operation
    # =====================================================

    def visit_BinaryOp(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)

        temp = self.new_temp()

        instr = IRBinaryOp(temp, left, node.operator, right)
        instr.security_label = node.security_label

        self.current_block.add_instruction(instr)

        return temp

    # =====================================================
    # Function Call
    # =====================================================

    def visit_FunctionCall(self, node):
        args = [arg.accept(self) for arg in node.args]

        temp = self.new_temp()

        instr = IRCall(temp, node.function.name, args)
        instr.security_label = node.security_label

        self.current_block.add_instruction(instr)

        return temp

    # =====================================================
    # Return
    # =====================================================

    def visit_ReturnStatement(self, node):
        if node.expression:
            value = node.expression.accept(self)
        else:
            value = None

        instr = IRReturn(value)
        instr.security_label = node.security_label

        self.current_block.add_instruction(instr)

    # =====================================================
    # If Statement
    # =====================================================

    def visit_IfStatement(self, node):
        cond = node.condition.accept(self)

        true_block = self.cfg.new_block("if_true")
        false_block = self.cfg.new_block("if_false")
        merge_block = self.cfg.new_block("if_merge")

        branch = IRBranch(cond, true_block, false_block)
        branch.security_label = node.condition.security_label

        self.current_block.add_instruction(branch)

        self.current_block.add_successor(true_block)
        self.current_block.add_successor(false_block)

        # True branch
        self.current_block = true_block
        node.then_block.accept(self)

        self.current_block.add_instruction(IRJump(merge_block))
        self.current_block.add_successor(merge_block)

        # False branch
        self.current_block = false_block
        if node.else_block:
            node.else_block.accept(self)

        self.current_block.add_instruction(IRJump(merge_block))
        self.current_block.add_successor(merge_block)

        # Continue at merge
        self.current_block = merge_block

    # =====================================================
    # While Loop
    # =====================================================

    def visit_WhileStatement(self, node):

        condition_block = self.cfg.new_block("while_condition")
        body_block = self.cfg.new_block("while_body")
        exit_block = self.cfg.new_block("while_exit")

        # Jump to condition
        self.current_block.add_instruction(IRJump(condition_block))
        self.current_block.add_successor(condition_block)

        # Condition block
        self.current_block = condition_block
        cond = node.condition.accept(self)

        branch = IRBranch(cond, body_block, exit_block)
        branch.security_label = node.condition.security_label

        self.current_block.add_instruction(branch)

        self.current_block.add_successor(body_block)
        self.current_block.add_successor(exit_block)

        # Body block
        self.current_block = body_block
        node.body.accept(self)

        self.current_block.add_instruction(IRJump(condition_block))
        self.current_block.add_successor(condition_block)

        # Continue after loop
        self.current_block = exit_block