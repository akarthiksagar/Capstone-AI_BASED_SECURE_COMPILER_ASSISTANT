# Generated from SecureLang.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .SecureLangParser import SecureLangParser
else:
    from SecureLangParser import SecureLangParser

# This class defines a complete generic visitor for a parse tree produced by SecureLangParser.

class SecureLangVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by SecureLangParser#program.
    def visitProgram(self, ctx:SecureLangParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#statementList.
    def visitStatementList(self, ctx:SecureLangParser.StatementListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#statement.
    def visitStatement(self, ctx:SecureLangParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#functionDef.
    def visitFunctionDef(self, ctx:SecureLangParser.FunctionDefContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#parameterList.
    def visitParameterList(self, ctx:SecureLangParser.ParameterListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#block.
    def visitBlock(self, ctx:SecureLangParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#ifStatement.
    def visitIfStatement(self, ctx:SecureLangParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#whileStatement.
    def visitWhileStatement(self, ctx:SecureLangParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#forStatement.
    def visitForStatement(self, ctx:SecureLangParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#returnStatement.
    def visitReturnStatement(self, ctx:SecureLangParser.ReturnStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#assignment.
    def visitAssignment(self, ctx:SecureLangParser.AssignmentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#expressionStatement.
    def visitExpressionStatement(self, ctx:SecureLangParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#importStatement.
    def visitImportStatement(self, ctx:SecureLangParser.ImportStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#dottedName.
    def visitDottedName(self, ctx:SecureLangParser.DottedNameContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#expression.
    def visitExpression(self, ctx:SecureLangParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#orExpr.
    def visitOrExpr(self, ctx:SecureLangParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#andExpr.
    def visitAndExpr(self, ctx:SecureLangParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#notExpr.
    def visitNotExpr(self, ctx:SecureLangParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#comparison.
    def visitComparison(self, ctx:SecureLangParser.ComparisonContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#compOp.
    def visitCompOp(self, ctx:SecureLangParser.CompOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#addExpr.
    def visitAddExpr(self, ctx:SecureLangParser.AddExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#mulExpr.
    def visitMulExpr(self, ctx:SecureLangParser.MulExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#unaryExpr.
    def visitUnaryExpr(self, ctx:SecureLangParser.UnaryExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#powerExpr.
    def visitPowerExpr(self, ctx:SecureLangParser.PowerExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#atomExpr.
    def visitAtomExpr(self, ctx:SecureLangParser.AtomExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#trailer.
    def visitTrailer(self, ctx:SecureLangParser.TrailerContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#atom.
    def visitAtom(self, ctx:SecureLangParser.AtomContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#listLiteral.
    def visitListLiteral(self, ctx:SecureLangParser.ListLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#dictLiteral.
    def visitDictLiteral(self, ctx:SecureLangParser.DictLiteralContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#dictEntry.
    def visitDictEntry(self, ctx:SecureLangParser.DictEntryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#argumentList.
    def visitArgumentList(self, ctx:SecureLangParser.ArgumentListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#argument.
    def visitArgument(self, ctx:SecureLangParser.ArgumentContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by SecureLangParser#memberAccess.
    def visitMemberAccess(self, ctx:SecureLangParser.MemberAccessContext):
        return self.visitChildren(ctx)



del SecureLangParser