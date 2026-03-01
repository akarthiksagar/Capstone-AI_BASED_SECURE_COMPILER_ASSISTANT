# Generated from SecureLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SecureLangParser import SecureLangParser
else:
    from SecureLangParser import SecureLangParser

# This class defines a complete listener for a parse tree produced by SecureLangParser.
class SecureLangListener(ParseTreeListener):

    # Enter a parse tree produced by SecureLangParser#program.
    def enterProgram(self, ctx:SecureLangParser.ProgramContext):
        pass

    # Exit a parse tree produced by SecureLangParser#program.
    def exitProgram(self, ctx:SecureLangParser.ProgramContext):
        pass


    # Enter a parse tree produced by SecureLangParser#statementList.
    def enterStatementList(self, ctx:SecureLangParser.StatementListContext):
        pass

    # Exit a parse tree produced by SecureLangParser#statementList.
    def exitStatementList(self, ctx:SecureLangParser.StatementListContext):
        pass


    # Enter a parse tree produced by SecureLangParser#statement.
    def enterStatement(self, ctx:SecureLangParser.StatementContext):
        pass

    # Exit a parse tree produced by SecureLangParser#statement.
    def exitStatement(self, ctx:SecureLangParser.StatementContext):
        pass


    # Enter a parse tree produced by SecureLangParser#functionDef.
    def enterFunctionDef(self, ctx:SecureLangParser.FunctionDefContext):
        pass

    # Exit a parse tree produced by SecureLangParser#functionDef.
    def exitFunctionDef(self, ctx:SecureLangParser.FunctionDefContext):
        pass


    # Enter a parse tree produced by SecureLangParser#parameterList.
    def enterParameterList(self, ctx:SecureLangParser.ParameterListContext):
        pass

    # Exit a parse tree produced by SecureLangParser#parameterList.
    def exitParameterList(self, ctx:SecureLangParser.ParameterListContext):
        pass


    # Enter a parse tree produced by SecureLangParser#block.
    def enterBlock(self, ctx:SecureLangParser.BlockContext):
        pass

    # Exit a parse tree produced by SecureLangParser#block.
    def exitBlock(self, ctx:SecureLangParser.BlockContext):
        pass


    # Enter a parse tree produced by SecureLangParser#ifStatement.
    def enterIfStatement(self, ctx:SecureLangParser.IfStatementContext):
        pass

    # Exit a parse tree produced by SecureLangParser#ifStatement.
    def exitIfStatement(self, ctx:SecureLangParser.IfStatementContext):
        pass


    # Enter a parse tree produced by SecureLangParser#whileStatement.
    def enterWhileStatement(self, ctx:SecureLangParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by SecureLangParser#whileStatement.
    def exitWhileStatement(self, ctx:SecureLangParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by SecureLangParser#forStatement.
    def enterForStatement(self, ctx:SecureLangParser.ForStatementContext):
        pass

    # Exit a parse tree produced by SecureLangParser#forStatement.
    def exitForStatement(self, ctx:SecureLangParser.ForStatementContext):
        pass


    # Enter a parse tree produced by SecureLangParser#returnStatement.
    def enterReturnStatement(self, ctx:SecureLangParser.ReturnStatementContext):
        pass

    # Exit a parse tree produced by SecureLangParser#returnStatement.
    def exitReturnStatement(self, ctx:SecureLangParser.ReturnStatementContext):
        pass


    # Enter a parse tree produced by SecureLangParser#assignment.
    def enterAssignment(self, ctx:SecureLangParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SecureLangParser#assignment.
    def exitAssignment(self, ctx:SecureLangParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SecureLangParser#expressionStatement.
    def enterExpressionStatement(self, ctx:SecureLangParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by SecureLangParser#expressionStatement.
    def exitExpressionStatement(self, ctx:SecureLangParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by SecureLangParser#importStatement.
    def enterImportStatement(self, ctx:SecureLangParser.ImportStatementContext):
        pass

    # Exit a parse tree produced by SecureLangParser#importStatement.
    def exitImportStatement(self, ctx:SecureLangParser.ImportStatementContext):
        pass


    # Enter a parse tree produced by SecureLangParser#dottedName.
    def enterDottedName(self, ctx:SecureLangParser.DottedNameContext):
        pass

    # Exit a parse tree produced by SecureLangParser#dottedName.
    def exitDottedName(self, ctx:SecureLangParser.DottedNameContext):
        pass


    # Enter a parse tree produced by SecureLangParser#expression.
    def enterExpression(self, ctx:SecureLangParser.ExpressionContext):
        pass

    # Exit a parse tree produced by SecureLangParser#expression.
    def exitExpression(self, ctx:SecureLangParser.ExpressionContext):
        pass


    # Enter a parse tree produced by SecureLangParser#orExpr.
    def enterOrExpr(self, ctx:SecureLangParser.OrExprContext):
        pass

    # Exit a parse tree produced by SecureLangParser#orExpr.
    def exitOrExpr(self, ctx:SecureLangParser.OrExprContext):
        pass


    # Enter a parse tree produced by SecureLangParser#andExpr.
    def enterAndExpr(self, ctx:SecureLangParser.AndExprContext):
        pass

    # Exit a parse tree produced by SecureLangParser#andExpr.
    def exitAndExpr(self, ctx:SecureLangParser.AndExprContext):
        pass


    # Enter a parse tree produced by SecureLangParser#notExpr.
    def enterNotExpr(self, ctx:SecureLangParser.NotExprContext):
        pass

    # Exit a parse tree produced by SecureLangParser#notExpr.
    def exitNotExpr(self, ctx:SecureLangParser.NotExprContext):
        pass


    # Enter a parse tree produced by SecureLangParser#comparison.
    def enterComparison(self, ctx:SecureLangParser.ComparisonContext):
        pass

    # Exit a parse tree produced by SecureLangParser#comparison.
    def exitComparison(self, ctx:SecureLangParser.ComparisonContext):
        pass


    # Enter a parse tree produced by SecureLangParser#compOp.
    def enterCompOp(self, ctx:SecureLangParser.CompOpContext):
        pass

    # Exit a parse tree produced by SecureLangParser#compOp.
    def exitCompOp(self, ctx:SecureLangParser.CompOpContext):
        pass


    # Enter a parse tree produced by SecureLangParser#addExpr.
    def enterAddExpr(self, ctx:SecureLangParser.AddExprContext):
        pass

    # Exit a parse tree produced by SecureLangParser#addExpr.
    def exitAddExpr(self, ctx:SecureLangParser.AddExprContext):
        pass


    # Enter a parse tree produced by SecureLangParser#mulExpr.
    def enterMulExpr(self, ctx:SecureLangParser.MulExprContext):
        pass

    # Exit a parse tree produced by SecureLangParser#mulExpr.
    def exitMulExpr(self, ctx:SecureLangParser.MulExprContext):
        pass


    # Enter a parse tree produced by SecureLangParser#unaryExpr.
    def enterUnaryExpr(self, ctx:SecureLangParser.UnaryExprContext):
        pass

    # Exit a parse tree produced by SecureLangParser#unaryExpr.
    def exitUnaryExpr(self, ctx:SecureLangParser.UnaryExprContext):
        pass


    # Enter a parse tree produced by SecureLangParser#powerExpr.
    def enterPowerExpr(self, ctx:SecureLangParser.PowerExprContext):
        pass

    # Exit a parse tree produced by SecureLangParser#powerExpr.
    def exitPowerExpr(self, ctx:SecureLangParser.PowerExprContext):
        pass


    # Enter a parse tree produced by SecureLangParser#atomExpr.
    def enterAtomExpr(self, ctx:SecureLangParser.AtomExprContext):
        pass

    # Exit a parse tree produced by SecureLangParser#atomExpr.
    def exitAtomExpr(self, ctx:SecureLangParser.AtomExprContext):
        pass


    # Enter a parse tree produced by SecureLangParser#trailer.
    def enterTrailer(self, ctx:SecureLangParser.TrailerContext):
        pass

    # Exit a parse tree produced by SecureLangParser#trailer.
    def exitTrailer(self, ctx:SecureLangParser.TrailerContext):
        pass


    # Enter a parse tree produced by SecureLangParser#atom.
    def enterAtom(self, ctx:SecureLangParser.AtomContext):
        pass

    # Exit a parse tree produced by SecureLangParser#atom.
    def exitAtom(self, ctx:SecureLangParser.AtomContext):
        pass


    # Enter a parse tree produced by SecureLangParser#listLiteral.
    def enterListLiteral(self, ctx:SecureLangParser.ListLiteralContext):
        pass

    # Exit a parse tree produced by SecureLangParser#listLiteral.
    def exitListLiteral(self, ctx:SecureLangParser.ListLiteralContext):
        pass


    # Enter a parse tree produced by SecureLangParser#dictLiteral.
    def enterDictLiteral(self, ctx:SecureLangParser.DictLiteralContext):
        pass

    # Exit a parse tree produced by SecureLangParser#dictLiteral.
    def exitDictLiteral(self, ctx:SecureLangParser.DictLiteralContext):
        pass


    # Enter a parse tree produced by SecureLangParser#dictEntry.
    def enterDictEntry(self, ctx:SecureLangParser.DictEntryContext):
        pass

    # Exit a parse tree produced by SecureLangParser#dictEntry.
    def exitDictEntry(self, ctx:SecureLangParser.DictEntryContext):
        pass


    # Enter a parse tree produced by SecureLangParser#argumentList.
    def enterArgumentList(self, ctx:SecureLangParser.ArgumentListContext):
        pass

    # Exit a parse tree produced by SecureLangParser#argumentList.
    def exitArgumentList(self, ctx:SecureLangParser.ArgumentListContext):
        pass


    # Enter a parse tree produced by SecureLangParser#argument.
    def enterArgument(self, ctx:SecureLangParser.ArgumentContext):
        pass

    # Exit a parse tree produced by SecureLangParser#argument.
    def exitArgument(self, ctx:SecureLangParser.ArgumentContext):
        pass


    # Enter a parse tree produced by SecureLangParser#memberAccess.
    def enterMemberAccess(self, ctx:SecureLangParser.MemberAccessContext):
        pass

    # Exit a parse tree produced by SecureLangParser#memberAccess.
    def exitMemberAccess(self, ctx:SecureLangParser.MemberAccessContext):
        pass



del SecureLangParser