// Generated from d:/compiler-design/Capstone-AI_BASED_SECURE_COMPILER_ASSISTANT/grammar/SecureLang.g4 by ANTLR 4.13.1
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link SecureLangParser}.
 */
public interface SecureLangListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(SecureLangParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(SecureLangParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#statementList}.
	 * @param ctx the parse tree
	 */
	void enterStatementList(SecureLangParser.StatementListContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#statementList}.
	 * @param ctx the parse tree
	 */
	void exitStatementList(SecureLangParser.StatementListContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(SecureLangParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(SecureLangParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#functionDef}.
	 * @param ctx the parse tree
	 */
	void enterFunctionDef(SecureLangParser.FunctionDefContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#functionDef}.
	 * @param ctx the parse tree
	 */
	void exitFunctionDef(SecureLangParser.FunctionDefContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#parameterList}.
	 * @param ctx the parse tree
	 */
	void enterParameterList(SecureLangParser.ParameterListContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#parameterList}.
	 * @param ctx the parse tree
	 */
	void exitParameterList(SecureLangParser.ParameterListContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(SecureLangParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(SecureLangParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#ifStatement}.
	 * @param ctx the parse tree
	 */
	void enterIfStatement(SecureLangParser.IfStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#ifStatement}.
	 * @param ctx the parse tree
	 */
	void exitIfStatement(SecureLangParser.IfStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#whileStatement}.
	 * @param ctx the parse tree
	 */
	void enterWhileStatement(SecureLangParser.WhileStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#whileStatement}.
	 * @param ctx the parse tree
	 */
	void exitWhileStatement(SecureLangParser.WhileStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#forStatement}.
	 * @param ctx the parse tree
	 */
	void enterForStatement(SecureLangParser.ForStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#forStatement}.
	 * @param ctx the parse tree
	 */
	void exitForStatement(SecureLangParser.ForStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#returnStatement}.
	 * @param ctx the parse tree
	 */
	void enterReturnStatement(SecureLangParser.ReturnStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#returnStatement}.
	 * @param ctx the parse tree
	 */
	void exitReturnStatement(SecureLangParser.ReturnStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#assignment}.
	 * @param ctx the parse tree
	 */
	void enterAssignment(SecureLangParser.AssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#assignment}.
	 * @param ctx the parse tree
	 */
	void exitAssignment(SecureLangParser.AssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#expressionStatement}.
	 * @param ctx the parse tree
	 */
	void enterExpressionStatement(SecureLangParser.ExpressionStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#expressionStatement}.
	 * @param ctx the parse tree
	 */
	void exitExpressionStatement(SecureLangParser.ExpressionStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#importStatement}.
	 * @param ctx the parse tree
	 */
	void enterImportStatement(SecureLangParser.ImportStatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#importStatement}.
	 * @param ctx the parse tree
	 */
	void exitImportStatement(SecureLangParser.ImportStatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#dottedName}.
	 * @param ctx the parse tree
	 */
	void enterDottedName(SecureLangParser.DottedNameContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#dottedName}.
	 * @param ctx the parse tree
	 */
	void exitDottedName(SecureLangParser.DottedNameContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterExpression(SecureLangParser.ExpressionContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitExpression(SecureLangParser.ExpressionContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#orExpr}.
	 * @param ctx the parse tree
	 */
	void enterOrExpr(SecureLangParser.OrExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#orExpr}.
	 * @param ctx the parse tree
	 */
	void exitOrExpr(SecureLangParser.OrExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#andExpr}.
	 * @param ctx the parse tree
	 */
	void enterAndExpr(SecureLangParser.AndExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#andExpr}.
	 * @param ctx the parse tree
	 */
	void exitAndExpr(SecureLangParser.AndExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#notExpr}.
	 * @param ctx the parse tree
	 */
	void enterNotExpr(SecureLangParser.NotExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#notExpr}.
	 * @param ctx the parse tree
	 */
	void exitNotExpr(SecureLangParser.NotExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#comparison}.
	 * @param ctx the parse tree
	 */
	void enterComparison(SecureLangParser.ComparisonContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#comparison}.
	 * @param ctx the parse tree
	 */
	void exitComparison(SecureLangParser.ComparisonContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#compOp}.
	 * @param ctx the parse tree
	 */
	void enterCompOp(SecureLangParser.CompOpContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#compOp}.
	 * @param ctx the parse tree
	 */
	void exitCompOp(SecureLangParser.CompOpContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#addExpr}.
	 * @param ctx the parse tree
	 */
	void enterAddExpr(SecureLangParser.AddExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#addExpr}.
	 * @param ctx the parse tree
	 */
	void exitAddExpr(SecureLangParser.AddExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#mulExpr}.
	 * @param ctx the parse tree
	 */
	void enterMulExpr(SecureLangParser.MulExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#mulExpr}.
	 * @param ctx the parse tree
	 */
	void exitMulExpr(SecureLangParser.MulExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void enterUnaryExpr(SecureLangParser.UnaryExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#unaryExpr}.
	 * @param ctx the parse tree
	 */
	void exitUnaryExpr(SecureLangParser.UnaryExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#powerExpr}.
	 * @param ctx the parse tree
	 */
	void enterPowerExpr(SecureLangParser.PowerExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#powerExpr}.
	 * @param ctx the parse tree
	 */
	void exitPowerExpr(SecureLangParser.PowerExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#atomExpr}.
	 * @param ctx the parse tree
	 */
	void enterAtomExpr(SecureLangParser.AtomExprContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#atomExpr}.
	 * @param ctx the parse tree
	 */
	void exitAtomExpr(SecureLangParser.AtomExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#trailer}.
	 * @param ctx the parse tree
	 */
	void enterTrailer(SecureLangParser.TrailerContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#trailer}.
	 * @param ctx the parse tree
	 */
	void exitTrailer(SecureLangParser.TrailerContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#atom}.
	 * @param ctx the parse tree
	 */
	void enterAtom(SecureLangParser.AtomContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#atom}.
	 * @param ctx the parse tree
	 */
	void exitAtom(SecureLangParser.AtomContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#listLiteral}.
	 * @param ctx the parse tree
	 */
	void enterListLiteral(SecureLangParser.ListLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#listLiteral}.
	 * @param ctx the parse tree
	 */
	void exitListLiteral(SecureLangParser.ListLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#dictLiteral}.
	 * @param ctx the parse tree
	 */
	void enterDictLiteral(SecureLangParser.DictLiteralContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#dictLiteral}.
	 * @param ctx the parse tree
	 */
	void exitDictLiteral(SecureLangParser.DictLiteralContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#dictEntry}.
	 * @param ctx the parse tree
	 */
	void enterDictEntry(SecureLangParser.DictEntryContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#dictEntry}.
	 * @param ctx the parse tree
	 */
	void exitDictEntry(SecureLangParser.DictEntryContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#argumentList}.
	 * @param ctx the parse tree
	 */
	void enterArgumentList(SecureLangParser.ArgumentListContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#argumentList}.
	 * @param ctx the parse tree
	 */
	void exitArgumentList(SecureLangParser.ArgumentListContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#argument}.
	 * @param ctx the parse tree
	 */
	void enterArgument(SecureLangParser.ArgumentContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#argument}.
	 * @param ctx the parse tree
	 */
	void exitArgument(SecureLangParser.ArgumentContext ctx);
	/**
	 * Enter a parse tree produced by {@link SecureLangParser#memberAccess}.
	 * @param ctx the parse tree
	 */
	void enterMemberAccess(SecureLangParser.MemberAccessContext ctx);
	/**
	 * Exit a parse tree produced by {@link SecureLangParser#memberAccess}.
	 * @param ctx the parse tree
	 */
	void exitMemberAccess(SecureLangParser.MemberAccessContext ctx);
}