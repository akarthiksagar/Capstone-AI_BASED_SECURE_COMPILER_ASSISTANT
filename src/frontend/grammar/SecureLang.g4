grammar SecureLang;

program
    : NEWLINE* (statement NEWLINE*)* EOF
    ;

statement
    : functionDef
    | ifStatement
    | whileStatement
    | forStatement
    | returnStatement
    | assignment
    | expressionStatement
    | importStatement
    ;

functionDef
    : 'def' IDENTIFIER '(' parameterList? ')' block
    ;

parameterList
    : IDENTIFIER (',' IDENTIFIER)*
    ;

block
    : '{' NEWLINE* (statement NEWLINE*)* '}'
    ;

ifStatement
    : 'if' expression block ('else' (ifStatement | block))?
    ;

whileStatement
    : 'while' expression block
    ;

forStatement
    : 'for' IDENTIFIER 'in' expression block
    ;

returnStatement
    : 'return' expression?
    ;

assignment
    : (IDENTIFIER | memberAccess) '=' expression
    ;

expressionStatement
    : expression
    ;

importStatement
    : 'import' dottedName
    | 'from' dottedName 'import' IDENTIFIER (',' IDENTIFIER)*
    ;

dottedName
    : IDENTIFIER ('.' IDENTIFIER)*
    ;

expression
    : orExpr
    ;

orExpr
    : andExpr ('or' andExpr)*
    ;

andExpr
    : notExpr ('and' notExpr)*
    ;

notExpr
    : 'not' notExpr
    | comparison
    ;

comparison
    : addExpr (compOp addExpr)*
    ;

compOp
    : '<' | '>' | '==' | '>=' | '<=' | '!=' | 'in' | 'not' 'in'
    ;

addExpr
    : mulExpr (('+' | '-') mulExpr)*
    ;

mulExpr
    : unaryExpr (('*' | '/' | '//' | '%') unaryExpr)*
    ;

unaryExpr
    : ('-' | '+') unaryExpr
    | powerExpr
    ;

powerExpr
    : atomExpr ('**' atomExpr)?
    ;

atomExpr
    : atom trailer*
    ;

trailer
    : '(' argumentList? ')'
    | '[' expression ']'
    | '.' IDENTIFIER
    ;

atom
    : IDENTIFIER
    | NUMBER
    | STRING
    | 'True'
    | 'False'
    | 'None'
    | listLiteral
    | dictLiteral
    | '(' expression ')'
    ;

listLiteral
    : '[' (expression (',' expression)*)? ']'
    ;

dictLiteral
    : '{' (dictEntry (',' dictEntry)*)? '}'
    ;

dictEntry
    : expression ':' expression
    ;

argumentList
    : argument (',' argument)*
    ;

argument
    : expression
    | IDENTIFIER '=' expression
    ;

memberAccess
    : IDENTIFIER ('.' IDENTIFIER)+
    ;

DEF     : 'def';
IF      : 'if';
ELSE    : 'else';
WHILE   : 'while';
FOR     : 'for';
IN      : 'in';
RETURN  : 'return';
IMPORT  : 'import';
FROM    : 'from';
AND     : 'and';
OR      : 'or';
NOT     : 'not';
TRUE    : 'True';
FALSE   : 'False';
NONE    : 'None';

IDENTIFIER
    : [a-zA-Z_] [a-zA-Z0-9_]*
    ;

NUMBER
    : INT
    | FLOAT
    ;

fragment INT
    : [0-9]+
    ;

fragment FLOAT
    : [0-9]+ '.' [0-9]*
    | '.' [0-9]+
    ;

STRING
    : '"' (~["\r\n\\] | '\\' .)* '"'
    | '\'' (~['\r\n\\] | '\\' .)* '\''
    ;

COMMENT
    : '//' ~[\r\n]* -> skip
    ;

BLOCK_COMMENT
    : '/*' .*? '*/' -> skip
    ;

NEWLINE
    : ('\r'? '\n' | '\r')+
    ;

WS
    : [ \t]+ -> skip
    ;

LPAREN  : '(';
RPAREN  : ')';
LBRACE  : '{';
RBRACE  : '}';
LBRACK  : '[';
RBRACK  : ']';
COMMA   : ',';
COLON   : ':';
DOT     : '.';
ASSIGN  : '=';
PLUS    : '+';
MINUS   : '-';
STAR    : '*';
SLASH   : '/';
DSLASH  : '//';
PERCENT : '%';
POWER   : '**';
LT      : '<';
GT      : '>';
EQ      : '==';
GE      : '>=';
LE      : '<=';
NE      : '!=';