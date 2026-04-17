grammar SecureLang;

/* ======================================================
 PROGRAM STRUCTURE
 ======================================================
 */

program: NEWLINE* statementList EOF;

statementList: (statement NEWLINE*)*;

/* ======================================================
 STATEMENTS
 ======================================================
 */

statement:
	functionDef
	| ifStatement
	| whileStatement
	| forStatement
	| tryStatement
	| withStatement
	| assertStatement
	| returnStatement
	| assignment
	| expressionStatement
	| importStatement;

/* ------------------ FUNCTIONS ------------------ */

functionDef: DEF IDENTIFIER LPAREN parameterList? RPAREN block;

parameterList: IDENTIFIER (COMMA IDENTIFIER)*;

block: LBRACE NEWLINE* statementList RBRACE;

/* ------------------ CONTROL FLOW ------------------ */

ifStatement:
	IF expression block (
		NEWLINE* ELSE NEWLINE* (ifStatement | block)
	)?;

whileStatement: WHILE expression block;

forStatement: FOR IDENTIFIER IN expression block;

/* ------------------ EXCEPTION HANDLING ------------------ */

tryStatement: TRY block (exceptClause)* (finallyClause)?;

exceptClause: EXCEPT (expression (AS IDENTIFIER)?)? block;

finallyClause: FINALLY block;

/* ------------------ CONTEXT MANAGERS ------------------ */

withStatement: WITH expression (AS IDENTIFIER)? block;

/* ------------------ ASSERTIONS ------------------ */

assertStatement: ASSERT expression (COMMA expression)?;

/* ------------------ OTHER STATEMENTS ------------------ */

returnStatement: RETURN expression?;

assignment: (IDENTIFIER | memberAccess) ASSIGN expression;

expressionStatement: expression;

importStatement:
	IMPORT dottedName
	| FROM dottedName IMPORT IDENTIFIER (COMMA IDENTIFIER)*;

dottedName: IDENTIFIER (DOT IDENTIFIER)*;

/* ======================================================
 EXPRESSIONS (Precedence Hierarchy)
 ======================================================
 */

expression: orExpr;

orExpr: andExpr (OR andExpr)*;

andExpr: notExpr (AND notExpr)*;

notExpr: NOT notExpr | comparison;

comparison: addExpr (compOp addExpr)*;

compOp: LT | GT | EQ | GE | LE | NE | IN | NOT IN;

addExpr: mulExpr ((PLUS | MINUS) mulExpr)*;

mulExpr: unaryExpr ((STAR | SLASH | PERCENT) unaryExpr)*;

unaryExpr: (PLUS | MINUS) unaryExpr | powerExpr;

powerExpr: atomExpr (POWER atomExpr)?;

atomExpr: atom trailer*;

trailer:
	LPAREN argumentList? RPAREN
	| LBRACK expression RBRACK
	| DOT IDENTIFIER;

atom:
	IDENTIFIER
	| NUMBER
	| STRING
	| TRUE
	| FALSE
	| NONE
	| listLiteral
	| dictLiteral
	| LPAREN expression RPAREN;

listLiteral: LBRACK (expression (COMMA expression)*)? RBRACK;

dictLiteral: LBRACE (dictEntry (COMMA dictEntry)*)? RBRACE;

dictEntry: expression COLON expression;

argumentList: argument (COMMA argument)*;

argument: expression | IDENTIFIER ASSIGN expression;

memberAccess: IDENTIFIER (DOT IDENTIFIER)+;

/* ======================================================
 SECURITY-SPECIFIC BUILT-INS
 ======================================================
 */

// Security sinks (vulnerable operations)
EXEC: 'exec';
EVAL: 'eval';
SYSTEM: 'system';
SQL: 'sql';
FILE_OPEN: 'open';
NET_CONNECT: 'connect';
DESERIALIZE: 'deserialize';

// Security sources (untrusted input)
INPUT: 'input';
GETENV: 'getenv';
REQUEST: 'request';

// Additional security constructs
TRY: 'try';
EXCEPT: 'except';
FINALLY: 'finally';
AS: 'as';
WITH: 'with';
ASSERT: 'assert';

/* ======================================================
 OPERATORS & SYMBOLS
 ======================================================
 */

LPAREN: '(';
RPAREN: ')';
LBRACE: '{';
RBRACE: '}';
LBRACK: '[';
RBRACK: ']';
COMMA: ',';
COLON: ':';
DOT: '.';
ASSIGN: '=';
PLUS: '+';
MINUS: '-';
STAR: '*';
SLASH: '/';
PERCENT: '%';
POWER: '**';
LT: '<';
GT: '>';
EQ: '==';
GE: '>=';
LE: '<=';
NE: '!=';

/* ======================================================
 LITERALS
 ======================================================
 */

IDENTIFIER: [a-zA-Z_] [a-zA-Z0-9_]*;

NUMBER: [0-9]+ ('.' [0-9]+)?;

STRING:
	'"' (~["\r\n\\] | '\\' .)* '"'
	| '\'' (~['\r\n\\] | '\\' .)* '\'';

/* ======================================================
 COMMENTS & WHITESPACE
 ======================================================
 */

LINE_COMMENT: '//' ~[\r\n]* -> skip;

BLOCK_COMMENT: '/*' .*? '*/' -> skip;

NEWLINE: ('\r'? '\n' | '\r')+;

WS: [ \t]+ -> skip;