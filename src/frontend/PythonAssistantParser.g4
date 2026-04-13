parser grammar PythonAssistantParser;

options {
	tokenVocab = PythonAssistantLexer;
}

/* =========================
 Entry Point
 =========================
 */
file_input: (stmt | NEWLINE)* EOF;

/* =========================
 Statements
 =========================
 */
stmt: simple_stmt | compound_stmt;

/* -------------------------
 Simple statements
 -------------------------
 */
simple_stmt: assignment | return_stmt | expr_stmt;

/* -------------------------
 Compound statements
 -------------------------
 */
compound_stmt: funcdef | if_stmt | while_stmt;

/* =========================
 Function Definition
 =========================
 */
funcdef: DEF ID parameters COLON block;

parameters: LPAREN (param (COMMA param)*)? RPAREN;

param: ID;

/* =========================
 Blocks (Simplified)
 =========================
 */
block: LBRACE (stmt | NEWLINE)* RBRACE;

/* =========================
 Control Flow
 =========================
 */
if_stmt:
	IF test COLON block (ELIF test COLON block)* (
		ELSE COLON block
	)?;

while_stmt: WHILE test COLON block;

/* =========================
 Assignments / Returns
 =========================
 */
assignment: ID ASSIGN test;

return_stmt: RETURN test?;

expr_stmt: test;

/* =========================
 Expressions (Precedence)
 =========================
 */
test: or_test;

or_test: and_test (OR and_test)*;

and_test: not_test (AND not_test)*;

not_test: NOT not_test | comparison;

comparison: expr (comp_op expr)*;

comp_op: EE | NE | LT | GT;

expr: term ((PLUS | MINUS) term)*;

term: factor ((STAR | SLASH | IDIV) factor)*;

factor: atom trailer*;

atom: ID | NUMBER | STRING | LPAREN test RPAREN;

trailer: LPAREN arglist? RPAREN | DOT ID;

arglist: test (COMMA test)*;