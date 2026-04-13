lexer grammar PythonAssistantLexer;

/* =========================
 Keywords
 =========================
 */
DEF: 'def';
IF: 'if';
ELIF: 'elif';
ELSE: 'else';
WHILE: 'while';
FOR: 'for';
IN: 'in';
RETURN: 'return';
IMPORT: 'import';
TRUE: 'True';
FALSE: 'False';
NONE: 'None';
OR: 'or';
AND: 'and';
NOT: 'not';

/* =========================
 Operators
 =========================
 */
ASSIGN: '=';
PLUS: '+';
MINUS: '-';
STAR: '*';
SLASH: '/';
DOUBLE_STAR: '**';
IDIV: '//';

/* =========================
 Comparison Operators
 =========================
 */
EE: '==';
NE: '!=';
LT: '<';
GT: '>';

/* =========================
 Delimiters / Punctuation
 =========================
 */
LPAREN: '(';
RPAREN: ')';
COLON: ':';
COMMA: ',';
LBRACE: '{';
RBRACE: '}';
DOT: '.';

/* =========================
 Literals
 =========================
 */
NUMBER: [0-9]+ ('.' [0-9]+)?;

STRING: '"' (~["\r\n])* '"' | '\'' (~['\r\n])* '\'';

ID: [a-zA-Z_][a-zA-Z0-9_]*;

/* =========================
 Layout / Hidden Tokens
 =========================
 */
NEWLINE: '\r'? '\n';

WS: [ \t]+ -> skip;

COMMENT: '#' ~[\r\n]* -> skip;