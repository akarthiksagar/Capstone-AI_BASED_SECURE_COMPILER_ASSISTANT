# Generated from src/frontend/PythonAssistantParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PythonAssistantParser import PythonAssistantParser
else:
    from PythonAssistantParser import PythonAssistantParser

# This class defines a complete generic visitor for a parse tree produced by PythonAssistantParser.

class PythonAssistantParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by PythonAssistantParser#file_input.
    def visitFile_input(self, ctx:PythonAssistantParser.File_inputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#stmt.
    def visitStmt(self, ctx:PythonAssistantParser.StmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#simple_stmt.
    def visitSimple_stmt(self, ctx:PythonAssistantParser.Simple_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#compound_stmt.
    def visitCompound_stmt(self, ctx:PythonAssistantParser.Compound_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#funcdef.
    def visitFuncdef(self, ctx:PythonAssistantParser.FuncdefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#parameters.
    def visitParameters(self, ctx:PythonAssistantParser.ParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#param.
    def visitParam(self, ctx:PythonAssistantParser.ParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#block.
    def visitBlock(self, ctx:PythonAssistantParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#if_stmt.
    def visitIf_stmt(self, ctx:PythonAssistantParser.If_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#while_stmt.
    def visitWhile_stmt(self, ctx:PythonAssistantParser.While_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#assignment.
    def visitAssignment(self, ctx:PythonAssistantParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#return_stmt.
    def visitReturn_stmt(self, ctx:PythonAssistantParser.Return_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#expr_stmt.
    def visitExpr_stmt(self, ctx:PythonAssistantParser.Expr_stmtContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#test.
    def visitTest(self, ctx:PythonAssistantParser.TestContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#or_test.
    def visitOr_test(self, ctx:PythonAssistantParser.Or_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#and_test.
    def visitAnd_test(self, ctx:PythonAssistantParser.And_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#not_test.
    def visitNot_test(self, ctx:PythonAssistantParser.Not_testContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#comparison.
    def visitComparison(self, ctx:PythonAssistantParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#comp_op.
    def visitComp_op(self, ctx:PythonAssistantParser.Comp_opContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#expr.
    def visitExpr(self, ctx:PythonAssistantParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#term.
    def visitTerm(self, ctx:PythonAssistantParser.TermContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#factor.
    def visitFactor(self, ctx:PythonAssistantParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#atom.
    def visitAtom(self, ctx:PythonAssistantParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#trailer.
    def visitTrailer(self, ctx:PythonAssistantParser.TrailerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by PythonAssistantParser#arglist.
    def visitArglist(self, ctx:PythonAssistantParser.ArglistContext):
        return self.visitChildren(ctx)



del PythonAssistantParser