# Generated from src/frontend/PythonAssistantParser.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .PythonAssistantParser import PythonAssistantParser
else:
    from PythonAssistantParser import PythonAssistantParser

# This class defines a complete listener for a parse tree produced by PythonAssistantParser.
class PythonAssistantParserListener(ParseTreeListener):

    # Enter a parse tree produced by PythonAssistantParser#file_input.
    def enterFile_input(self, ctx:PythonAssistantParser.File_inputContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#file_input.
    def exitFile_input(self, ctx:PythonAssistantParser.File_inputContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#stmt.
    def enterStmt(self, ctx:PythonAssistantParser.StmtContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#stmt.
    def exitStmt(self, ctx:PythonAssistantParser.StmtContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#simple_stmt.
    def enterSimple_stmt(self, ctx:PythonAssistantParser.Simple_stmtContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#simple_stmt.
    def exitSimple_stmt(self, ctx:PythonAssistantParser.Simple_stmtContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#compound_stmt.
    def enterCompound_stmt(self, ctx:PythonAssistantParser.Compound_stmtContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#compound_stmt.
    def exitCompound_stmt(self, ctx:PythonAssistantParser.Compound_stmtContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#funcdef.
    def enterFuncdef(self, ctx:PythonAssistantParser.FuncdefContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#funcdef.
    def exitFuncdef(self, ctx:PythonAssistantParser.FuncdefContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#parameters.
    def enterParameters(self, ctx:PythonAssistantParser.ParametersContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#parameters.
    def exitParameters(self, ctx:PythonAssistantParser.ParametersContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#param.
    def enterParam(self, ctx:PythonAssistantParser.ParamContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#param.
    def exitParam(self, ctx:PythonAssistantParser.ParamContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#block.
    def enterBlock(self, ctx:PythonAssistantParser.BlockContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#block.
    def exitBlock(self, ctx:PythonAssistantParser.BlockContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#if_stmt.
    def enterIf_stmt(self, ctx:PythonAssistantParser.If_stmtContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#if_stmt.
    def exitIf_stmt(self, ctx:PythonAssistantParser.If_stmtContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#while_stmt.
    def enterWhile_stmt(self, ctx:PythonAssistantParser.While_stmtContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#while_stmt.
    def exitWhile_stmt(self, ctx:PythonAssistantParser.While_stmtContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#assignment.
    def enterAssignment(self, ctx:PythonAssistantParser.AssignmentContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#assignment.
    def exitAssignment(self, ctx:PythonAssistantParser.AssignmentContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#return_stmt.
    def enterReturn_stmt(self, ctx:PythonAssistantParser.Return_stmtContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#return_stmt.
    def exitReturn_stmt(self, ctx:PythonAssistantParser.Return_stmtContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#expr_stmt.
    def enterExpr_stmt(self, ctx:PythonAssistantParser.Expr_stmtContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#expr_stmt.
    def exitExpr_stmt(self, ctx:PythonAssistantParser.Expr_stmtContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#test.
    def enterTest(self, ctx:PythonAssistantParser.TestContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#test.
    def exitTest(self, ctx:PythonAssistantParser.TestContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#or_test.
    def enterOr_test(self, ctx:PythonAssistantParser.Or_testContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#or_test.
    def exitOr_test(self, ctx:PythonAssistantParser.Or_testContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#and_test.
    def enterAnd_test(self, ctx:PythonAssistantParser.And_testContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#and_test.
    def exitAnd_test(self, ctx:PythonAssistantParser.And_testContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#not_test.
    def enterNot_test(self, ctx:PythonAssistantParser.Not_testContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#not_test.
    def exitNot_test(self, ctx:PythonAssistantParser.Not_testContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#comparison.
    def enterComparison(self, ctx:PythonAssistantParser.ComparisonContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#comparison.
    def exitComparison(self, ctx:PythonAssistantParser.ComparisonContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#comp_op.
    def enterComp_op(self, ctx:PythonAssistantParser.Comp_opContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#comp_op.
    def exitComp_op(self, ctx:PythonAssistantParser.Comp_opContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#expr.
    def enterExpr(self, ctx:PythonAssistantParser.ExprContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#expr.
    def exitExpr(self, ctx:PythonAssistantParser.ExprContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#term.
    def enterTerm(self, ctx:PythonAssistantParser.TermContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#term.
    def exitTerm(self, ctx:PythonAssistantParser.TermContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#factor.
    def enterFactor(self, ctx:PythonAssistantParser.FactorContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#factor.
    def exitFactor(self, ctx:PythonAssistantParser.FactorContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#atom.
    def enterAtom(self, ctx:PythonAssistantParser.AtomContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#atom.
    def exitAtom(self, ctx:PythonAssistantParser.AtomContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#trailer.
    def enterTrailer(self, ctx:PythonAssistantParser.TrailerContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#trailer.
    def exitTrailer(self, ctx:PythonAssistantParser.TrailerContext):
        pass


    # Enter a parse tree produced by PythonAssistantParser#arglist.
    def enterArglist(self, ctx:PythonAssistantParser.ArglistContext):
        pass

    # Exit a parse tree produced by PythonAssistantParser#arglist.
    def exitArglist(self, ctx:PythonAssistantParser.ArglistContext):
        pass



del PythonAssistantParser