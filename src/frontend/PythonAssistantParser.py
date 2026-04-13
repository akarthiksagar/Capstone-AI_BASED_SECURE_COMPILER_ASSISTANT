# Generated from src/frontend/PythonAssistantParser.g4 by ANTLR 4.13.2
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,39,222,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,2,21,7,21,2,22,7,22,2,23,7,23,2,24,7,24,1,0,1,0,5,0,53,8,0,
        10,0,12,0,56,9,0,1,0,1,0,1,1,1,1,3,1,62,8,1,1,2,1,2,1,2,3,2,67,8,
        2,1,3,1,3,1,3,3,3,72,8,3,1,4,1,4,1,4,1,4,1,4,1,4,1,5,1,5,1,5,1,5,
        5,5,84,8,5,10,5,12,5,87,9,5,3,5,89,8,5,1,5,1,5,1,6,1,6,1,7,1,7,1,
        7,5,7,98,8,7,10,7,12,7,101,9,7,1,7,1,7,1,8,1,8,1,8,1,8,1,8,1,8,1,
        8,1,8,1,8,5,8,114,8,8,10,8,12,8,117,9,8,1,8,1,8,1,8,3,8,122,8,8,
        1,9,1,9,1,9,1,9,1,9,1,10,1,10,1,10,1,10,1,11,1,11,3,11,135,8,11,
        1,12,1,12,1,13,1,13,1,14,1,14,1,14,5,14,144,8,14,10,14,12,14,147,
        9,14,1,15,1,15,1,15,5,15,152,8,15,10,15,12,15,155,9,15,1,16,1,16,
        1,16,3,16,160,8,16,1,17,1,17,1,17,1,17,5,17,166,8,17,10,17,12,17,
        169,9,17,1,18,1,18,1,19,1,19,1,19,5,19,176,8,19,10,19,12,19,179,
        9,19,1,20,1,20,1,20,5,20,184,8,20,10,20,12,20,187,9,20,1,21,1,21,
        5,21,191,8,21,10,21,12,21,194,9,21,1,22,1,22,1,22,1,22,1,22,1,22,
        1,22,3,22,203,8,22,1,23,1,23,3,23,207,8,23,1,23,1,23,1,23,3,23,212,
        8,23,1,24,1,24,1,24,5,24,217,8,24,10,24,12,24,220,9,24,1,24,0,0,
        25,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34,36,38,40,42,
        44,46,48,0,3,1,0,23,26,1,0,17,18,2,0,19,20,22,22,223,0,54,1,0,0,
        0,2,61,1,0,0,0,4,66,1,0,0,0,6,71,1,0,0,0,8,73,1,0,0,0,10,79,1,0,
        0,0,12,92,1,0,0,0,14,94,1,0,0,0,16,104,1,0,0,0,18,123,1,0,0,0,20,
        128,1,0,0,0,22,132,1,0,0,0,24,136,1,0,0,0,26,138,1,0,0,0,28,140,
        1,0,0,0,30,148,1,0,0,0,32,159,1,0,0,0,34,161,1,0,0,0,36,170,1,0,
        0,0,38,172,1,0,0,0,40,180,1,0,0,0,42,188,1,0,0,0,44,202,1,0,0,0,
        46,211,1,0,0,0,48,213,1,0,0,0,50,53,3,2,1,0,51,53,5,37,0,0,52,50,
        1,0,0,0,52,51,1,0,0,0,53,56,1,0,0,0,54,52,1,0,0,0,54,55,1,0,0,0,
        55,57,1,0,0,0,56,54,1,0,0,0,57,58,5,0,0,1,58,1,1,0,0,0,59,62,3,4,
        2,0,60,62,3,6,3,0,61,59,1,0,0,0,61,60,1,0,0,0,62,3,1,0,0,0,63,67,
        3,20,10,0,64,67,3,22,11,0,65,67,3,24,12,0,66,63,1,0,0,0,66,64,1,
        0,0,0,66,65,1,0,0,0,67,5,1,0,0,0,68,72,3,8,4,0,69,72,3,16,8,0,70,
        72,3,18,9,0,71,68,1,0,0,0,71,69,1,0,0,0,71,70,1,0,0,0,72,7,1,0,0,
        0,73,74,5,1,0,0,74,75,5,36,0,0,75,76,3,10,5,0,76,77,5,29,0,0,77,
        78,3,14,7,0,78,9,1,0,0,0,79,88,5,27,0,0,80,85,3,12,6,0,81,82,5,30,
        0,0,82,84,3,12,6,0,83,81,1,0,0,0,84,87,1,0,0,0,85,83,1,0,0,0,85,
        86,1,0,0,0,86,89,1,0,0,0,87,85,1,0,0,0,88,80,1,0,0,0,88,89,1,0,0,
        0,89,90,1,0,0,0,90,91,5,28,0,0,91,11,1,0,0,0,92,93,5,36,0,0,93,13,
        1,0,0,0,94,99,5,31,0,0,95,98,3,2,1,0,96,98,5,37,0,0,97,95,1,0,0,
        0,97,96,1,0,0,0,98,101,1,0,0,0,99,97,1,0,0,0,99,100,1,0,0,0,100,
        102,1,0,0,0,101,99,1,0,0,0,102,103,5,32,0,0,103,15,1,0,0,0,104,105,
        5,2,0,0,105,106,3,26,13,0,106,107,5,29,0,0,107,115,3,14,7,0,108,
        109,5,3,0,0,109,110,3,26,13,0,110,111,5,29,0,0,111,112,3,14,7,0,
        112,114,1,0,0,0,113,108,1,0,0,0,114,117,1,0,0,0,115,113,1,0,0,0,
        115,116,1,0,0,0,116,121,1,0,0,0,117,115,1,0,0,0,118,119,5,4,0,0,
        119,120,5,29,0,0,120,122,3,14,7,0,121,118,1,0,0,0,121,122,1,0,0,
        0,122,17,1,0,0,0,123,124,5,5,0,0,124,125,3,26,13,0,125,126,5,29,
        0,0,126,127,3,14,7,0,127,19,1,0,0,0,128,129,5,36,0,0,129,130,5,16,
        0,0,130,131,3,26,13,0,131,21,1,0,0,0,132,134,5,8,0,0,133,135,3,26,
        13,0,134,133,1,0,0,0,134,135,1,0,0,0,135,23,1,0,0,0,136,137,3,26,
        13,0,137,25,1,0,0,0,138,139,3,28,14,0,139,27,1,0,0,0,140,145,3,30,
        15,0,141,142,5,13,0,0,142,144,3,30,15,0,143,141,1,0,0,0,144,147,
        1,0,0,0,145,143,1,0,0,0,145,146,1,0,0,0,146,29,1,0,0,0,147,145,1,
        0,0,0,148,153,3,32,16,0,149,150,5,14,0,0,150,152,3,32,16,0,151,149,
        1,0,0,0,152,155,1,0,0,0,153,151,1,0,0,0,153,154,1,0,0,0,154,31,1,
        0,0,0,155,153,1,0,0,0,156,157,5,15,0,0,157,160,3,32,16,0,158,160,
        3,34,17,0,159,156,1,0,0,0,159,158,1,0,0,0,160,33,1,0,0,0,161,167,
        3,38,19,0,162,163,3,36,18,0,163,164,3,38,19,0,164,166,1,0,0,0,165,
        162,1,0,0,0,166,169,1,0,0,0,167,165,1,0,0,0,167,168,1,0,0,0,168,
        35,1,0,0,0,169,167,1,0,0,0,170,171,7,0,0,0,171,37,1,0,0,0,172,177,
        3,40,20,0,173,174,7,1,0,0,174,176,3,40,20,0,175,173,1,0,0,0,176,
        179,1,0,0,0,177,175,1,0,0,0,177,178,1,0,0,0,178,39,1,0,0,0,179,177,
        1,0,0,0,180,185,3,42,21,0,181,182,7,2,0,0,182,184,3,42,21,0,183,
        181,1,0,0,0,184,187,1,0,0,0,185,183,1,0,0,0,185,186,1,0,0,0,186,
        41,1,0,0,0,187,185,1,0,0,0,188,192,3,44,22,0,189,191,3,46,23,0,190,
        189,1,0,0,0,191,194,1,0,0,0,192,190,1,0,0,0,192,193,1,0,0,0,193,
        43,1,0,0,0,194,192,1,0,0,0,195,203,5,36,0,0,196,203,5,34,0,0,197,
        203,5,35,0,0,198,199,5,27,0,0,199,200,3,26,13,0,200,201,5,28,0,0,
        201,203,1,0,0,0,202,195,1,0,0,0,202,196,1,0,0,0,202,197,1,0,0,0,
        202,198,1,0,0,0,203,45,1,0,0,0,204,206,5,27,0,0,205,207,3,48,24,
        0,206,205,1,0,0,0,206,207,1,0,0,0,207,208,1,0,0,0,208,212,5,28,0,
        0,209,210,5,33,0,0,210,212,5,36,0,0,211,204,1,0,0,0,211,209,1,0,
        0,0,212,47,1,0,0,0,213,218,3,26,13,0,214,215,5,30,0,0,215,217,3,
        26,13,0,216,214,1,0,0,0,217,220,1,0,0,0,218,216,1,0,0,0,218,219,
        1,0,0,0,219,49,1,0,0,0,220,218,1,0,0,0,23,52,54,61,66,71,85,88,97,
        99,115,121,134,145,153,159,167,177,185,192,202,206,211,218
    ]

class PythonAssistantParser ( Parser ):

    grammarFileName = "PythonAssistantParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'def'", "'if'", "'elif'", "'else'", "'while'", 
                     "'for'", "'in'", "'return'", "'import'", "'True'", 
                     "'False'", "'None'", "'or'", "'and'", "'not'", "'='", 
                     "'+'", "'-'", "'*'", "'/'", "'**'", "'//'", "'=='", 
                     "'!='", "'<'", "'>'", "'('", "')'", "':'", "','", "'{'", 
                     "'}'", "'.'" ]

    symbolicNames = [ "<INVALID>", "DEF", "IF", "ELIF", "ELSE", "WHILE", 
                      "FOR", "IN", "RETURN", "IMPORT", "TRUE", "FALSE", 
                      "NONE", "OR", "AND", "NOT", "ASSIGN", "PLUS", "MINUS", 
                      "STAR", "SLASH", "DOUBLE_STAR", "IDIV", "EE", "NE", 
                      "LT", "GT", "LPAREN", "RPAREN", "COLON", "COMMA", 
                      "LBRACE", "RBRACE", "DOT", "NUMBER", "STRING", "ID", 
                      "NEWLINE", "WS", "COMMENT" ]

    RULE_file_input = 0
    RULE_stmt = 1
    RULE_simple_stmt = 2
    RULE_compound_stmt = 3
    RULE_funcdef = 4
    RULE_parameters = 5
    RULE_param = 6
    RULE_block = 7
    RULE_if_stmt = 8
    RULE_while_stmt = 9
    RULE_assignment = 10
    RULE_return_stmt = 11
    RULE_expr_stmt = 12
    RULE_test = 13
    RULE_or_test = 14
    RULE_and_test = 15
    RULE_not_test = 16
    RULE_comparison = 17
    RULE_comp_op = 18
    RULE_expr = 19
    RULE_term = 20
    RULE_factor = 21
    RULE_atom = 22
    RULE_trailer = 23
    RULE_arglist = 24

    ruleNames =  [ "file_input", "stmt", "simple_stmt", "compound_stmt", 
                   "funcdef", "parameters", "param", "block", "if_stmt", 
                   "while_stmt", "assignment", "return_stmt", "expr_stmt", 
                   "test", "or_test", "and_test", "not_test", "comparison", 
                   "comp_op", "expr", "term", "factor", "atom", "trailer", 
                   "arglist" ]

    EOF = Token.EOF
    DEF=1
    IF=2
    ELIF=3
    ELSE=4
    WHILE=5
    FOR=6
    IN=7
    RETURN=8
    IMPORT=9
    TRUE=10
    FALSE=11
    NONE=12
    OR=13
    AND=14
    NOT=15
    ASSIGN=16
    PLUS=17
    MINUS=18
    STAR=19
    SLASH=20
    DOUBLE_STAR=21
    IDIV=22
    EE=23
    NE=24
    LT=25
    GT=26
    LPAREN=27
    RPAREN=28
    COLON=29
    COMMA=30
    LBRACE=31
    RBRACE=32
    DOT=33
    NUMBER=34
    STRING=35
    ID=36
    NEWLINE=37
    WS=38
    COMMENT=39

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.2")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class File_inputContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(PythonAssistantParser.EOF, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.StmtContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.StmtContext,i)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.NEWLINE)
            else:
                return self.getToken(PythonAssistantParser.NEWLINE, i)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_file_input

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFile_input" ):
                listener.enterFile_input(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFile_input" ):
                listener.exitFile_input(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFile_input" ):
                return visitor.visitFile_input(self)
            else:
                return visitor.visitChildren(self)




    def file_input(self):

        localctx = PythonAssistantParser.File_inputContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_file_input)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 54
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 257832288550) != 0):
                self.state = 52
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1, 2, 5, 8, 15, 27, 34, 35, 36]:
                    self.state = 50
                    self.stmt()
                    pass
                elif token in [37]:
                    self.state = 51
                    self.match(PythonAssistantParser.NEWLINE)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 56
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 57
            self.match(PythonAssistantParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class StmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def simple_stmt(self):
            return self.getTypedRuleContext(PythonAssistantParser.Simple_stmtContext,0)


        def compound_stmt(self):
            return self.getTypedRuleContext(PythonAssistantParser.Compound_stmtContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterStmt" ):
                listener.enterStmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitStmt" ):
                listener.exitStmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitStmt" ):
                return visitor.visitStmt(self)
            else:
                return visitor.visitChildren(self)




    def stmt(self):

        localctx = PythonAssistantParser.StmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_stmt)
        try:
            self.state = 61
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8, 15, 27, 34, 35, 36]:
                self.enterOuterAlt(localctx, 1)
                self.state = 59
                self.simple_stmt()
                pass
            elif token in [1, 2, 5]:
                self.enterOuterAlt(localctx, 2)
                self.state = 60
                self.compound_stmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Simple_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def assignment(self):
            return self.getTypedRuleContext(PythonAssistantParser.AssignmentContext,0)


        def return_stmt(self):
            return self.getTypedRuleContext(PythonAssistantParser.Return_stmtContext,0)


        def expr_stmt(self):
            return self.getTypedRuleContext(PythonAssistantParser.Expr_stmtContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_simple_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSimple_stmt" ):
                listener.enterSimple_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSimple_stmt" ):
                listener.exitSimple_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitSimple_stmt" ):
                return visitor.visitSimple_stmt(self)
            else:
                return visitor.visitChildren(self)




    def simple_stmt(self):

        localctx = PythonAssistantParser.Simple_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_simple_stmt)
        try:
            self.state = 66
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,3,self._ctx)
            if la_ == 1:
                self.enterOuterAlt(localctx, 1)
                self.state = 63
                self.assignment()
                pass

            elif la_ == 2:
                self.enterOuterAlt(localctx, 2)
                self.state = 64
                self.return_stmt()
                pass

            elif la_ == 3:
                self.enterOuterAlt(localctx, 3)
                self.state = 65
                self.expr_stmt()
                pass


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Compound_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def funcdef(self):
            return self.getTypedRuleContext(PythonAssistantParser.FuncdefContext,0)


        def if_stmt(self):
            return self.getTypedRuleContext(PythonAssistantParser.If_stmtContext,0)


        def while_stmt(self):
            return self.getTypedRuleContext(PythonAssistantParser.While_stmtContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_compound_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterCompound_stmt" ):
                listener.enterCompound_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitCompound_stmt" ):
                listener.exitCompound_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitCompound_stmt" ):
                return visitor.visitCompound_stmt(self)
            else:
                return visitor.visitChildren(self)




    def compound_stmt(self):

        localctx = PythonAssistantParser.Compound_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_compound_stmt)
        try:
            self.state = 71
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 68
                self.funcdef()
                pass
            elif token in [2]:
                self.enterOuterAlt(localctx, 2)
                self.state = 69
                self.if_stmt()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 70
                self.while_stmt()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncdefContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DEF(self):
            return self.getToken(PythonAssistantParser.DEF, 0)

        def ID(self):
            return self.getToken(PythonAssistantParser.ID, 0)

        def parameters(self):
            return self.getTypedRuleContext(PythonAssistantParser.ParametersContext,0)


        def COLON(self):
            return self.getToken(PythonAssistantParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PythonAssistantParser.BlockContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_funcdef

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncdef" ):
                listener.enterFuncdef(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncdef" ):
                listener.exitFuncdef(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFuncdef" ):
                return visitor.visitFuncdef(self)
            else:
                return visitor.visitChildren(self)




    def funcdef(self):

        localctx = PythonAssistantParser.FuncdefContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_funcdef)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 73
            self.match(PythonAssistantParser.DEF)
            self.state = 74
            self.match(PythonAssistantParser.ID)
            self.state = 75
            self.parameters()
            self.state = 76
            self.match(PythonAssistantParser.COLON)
            self.state = 77
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParametersContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(PythonAssistantParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PythonAssistantParser.RPAREN, 0)

        def param(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.ParamContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.ParamContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.COMMA)
            else:
                return self.getToken(PythonAssistantParser.COMMA, i)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_parameters

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParameters" ):
                listener.enterParameters(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParameters" ):
                listener.exitParameters(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParameters" ):
                return visitor.visitParameters(self)
            else:
                return visitor.visitChildren(self)




    def parameters(self):

        localctx = PythonAssistantParser.ParametersContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_parameters)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 79
            self.match(PythonAssistantParser.LPAREN)
            self.state = 88
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==36:
                self.state = 80
                self.param()
                self.state = 85
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                while _la==30:
                    self.state = 81
                    self.match(PythonAssistantParser.COMMA)
                    self.state = 82
                    self.param()
                    self.state = 87
                    self._errHandler.sync(self)
                    _la = self._input.LA(1)



            self.state = 90
            self.match(PythonAssistantParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ParamContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PythonAssistantParser.ID, 0)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_param

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterParam" ):
                listener.enterParam(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitParam" ):
                listener.exitParam(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitParam" ):
                return visitor.visitParam(self)
            else:
                return visitor.visitChildren(self)




    def param(self):

        localctx = PythonAssistantParser.ParamContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_param)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 92
            self.match(PythonAssistantParser.ID)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class BlockContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LBRACE(self):
            return self.getToken(PythonAssistantParser.LBRACE, 0)

        def RBRACE(self):
            return self.getToken(PythonAssistantParser.RBRACE, 0)

        def stmt(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.StmtContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.StmtContext,i)


        def NEWLINE(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.NEWLINE)
            else:
                return self.getToken(PythonAssistantParser.NEWLINE, i)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_block

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterBlock" ):
                listener.enterBlock(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitBlock" ):
                listener.exitBlock(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitBlock" ):
                return visitor.visitBlock(self)
            else:
                return visitor.visitChildren(self)




    def block(self):

        localctx = PythonAssistantParser.BlockContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_block)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 94
            self.match(PythonAssistantParser.LBRACE)
            self.state = 99
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 257832288550) != 0):
                self.state = 97
                self._errHandler.sync(self)
                token = self._input.LA(1)
                if token in [1, 2, 5, 8, 15, 27, 34, 35, 36]:
                    self.state = 95
                    self.stmt()
                    pass
                elif token in [37]:
                    self.state = 96
                    self.match(PythonAssistantParser.NEWLINE)
                    pass
                else:
                    raise NoViableAltException(self)

                self.state = 101
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 102
            self.match(PythonAssistantParser.RBRACE)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class If_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def IF(self):
            return self.getToken(PythonAssistantParser.IF, 0)

        def test(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.TestContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.TestContext,i)


        def COLON(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.COLON)
            else:
                return self.getToken(PythonAssistantParser.COLON, i)

        def block(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.BlockContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.BlockContext,i)


        def ELIF(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.ELIF)
            else:
                return self.getToken(PythonAssistantParser.ELIF, i)

        def ELSE(self):
            return self.getToken(PythonAssistantParser.ELSE, 0)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_if_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterIf_stmt" ):
                listener.enterIf_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitIf_stmt" ):
                listener.exitIf_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitIf_stmt" ):
                return visitor.visitIf_stmt(self)
            else:
                return visitor.visitChildren(self)




    def if_stmt(self):

        localctx = PythonAssistantParser.If_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_if_stmt)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 104
            self.match(PythonAssistantParser.IF)
            self.state = 105
            self.test()
            self.state = 106
            self.match(PythonAssistantParser.COLON)
            self.state = 107
            self.block()
            self.state = 115
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==3:
                self.state = 108
                self.match(PythonAssistantParser.ELIF)
                self.state = 109
                self.test()
                self.state = 110
                self.match(PythonAssistantParser.COLON)
                self.state = 111
                self.block()
                self.state = 117
                self._errHandler.sync(self)
                _la = self._input.LA(1)

            self.state = 121
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==4:
                self.state = 118
                self.match(PythonAssistantParser.ELSE)
                self.state = 119
                self.match(PythonAssistantParser.COLON)
                self.state = 120
                self.block()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class While_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def WHILE(self):
            return self.getToken(PythonAssistantParser.WHILE, 0)

        def test(self):
            return self.getTypedRuleContext(PythonAssistantParser.TestContext,0)


        def COLON(self):
            return self.getToken(PythonAssistantParser.COLON, 0)

        def block(self):
            return self.getTypedRuleContext(PythonAssistantParser.BlockContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_while_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterWhile_stmt" ):
                listener.enterWhile_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitWhile_stmt" ):
                listener.exitWhile_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitWhile_stmt" ):
                return visitor.visitWhile_stmt(self)
            else:
                return visitor.visitChildren(self)




    def while_stmt(self):

        localctx = PythonAssistantParser.While_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_while_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 123
            self.match(PythonAssistantParser.WHILE)
            self.state = 124
            self.test()
            self.state = 125
            self.match(PythonAssistantParser.COLON)
            self.state = 126
            self.block()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AssignmentContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PythonAssistantParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(PythonAssistantParser.ASSIGN, 0)

        def test(self):
            return self.getTypedRuleContext(PythonAssistantParser.TestContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_assignment

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAssignment" ):
                listener.enterAssignment(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAssignment" ):
                listener.exitAssignment(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAssignment" ):
                return visitor.visitAssignment(self)
            else:
                return visitor.visitChildren(self)




    def assignment(self):

        localctx = PythonAssistantParser.AssignmentContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_assignment)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 128
            self.match(PythonAssistantParser.ID)
            self.state = 129
            self.match(PythonAssistantParser.ASSIGN)
            self.state = 130
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Return_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def RETURN(self):
            return self.getToken(PythonAssistantParser.RETURN, 0)

        def test(self):
            return self.getTypedRuleContext(PythonAssistantParser.TestContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_return_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterReturn_stmt" ):
                listener.enterReturn_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitReturn_stmt" ):
                listener.exitReturn_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitReturn_stmt" ):
                return visitor.visitReturn_stmt(self)
            else:
                return visitor.visitChildren(self)




    def return_stmt(self):

        localctx = PythonAssistantParser.Return_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_return_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 132
            self.match(PythonAssistantParser.RETURN)
            self.state = 134
            self._errHandler.sync(self)
            la_ = self._interp.adaptivePredict(self._input,11,self._ctx)
            if la_ == 1:
                self.state = 133
                self.test()


        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Expr_stmtContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def test(self):
            return self.getTypedRuleContext(PythonAssistantParser.TestContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_expr_stmt

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr_stmt" ):
                listener.enterExpr_stmt(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr_stmt" ):
                listener.exitExpr_stmt(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr_stmt" ):
                return visitor.visitExpr_stmt(self)
            else:
                return visitor.visitChildren(self)




    def expr_stmt(self):

        localctx = PythonAssistantParser.Expr_stmtContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_expr_stmt)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 136
            self.test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TestContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def or_test(self):
            return self.getTypedRuleContext(PythonAssistantParser.Or_testContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_test

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTest" ):
                listener.enterTest(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTest" ):
                listener.exitTest(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTest" ):
                return visitor.visitTest(self)
            else:
                return visitor.visitChildren(self)




    def test(self):

        localctx = PythonAssistantParser.TestContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_test)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 138
            self.or_test()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Or_testContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def and_test(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.And_testContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.And_testContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.OR)
            else:
                return self.getToken(PythonAssistantParser.OR, i)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_or_test

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOr_test" ):
                listener.enterOr_test(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOr_test" ):
                listener.exitOr_test(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitOr_test" ):
                return visitor.visitOr_test(self)
            else:
                return visitor.visitChildren(self)




    def or_test(self):

        localctx = PythonAssistantParser.Or_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_or_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 140
            self.and_test()
            self.state = 145
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==13:
                self.state = 141
                self.match(PythonAssistantParser.OR)
                self.state = 142
                self.and_test()
                self.state = 147
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class And_testContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def not_test(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.Not_testContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.Not_testContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.AND)
            else:
                return self.getToken(PythonAssistantParser.AND, i)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_and_test

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAnd_test" ):
                listener.enterAnd_test(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAnd_test" ):
                listener.exitAnd_test(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAnd_test" ):
                return visitor.visitAnd_test(self)
            else:
                return visitor.visitChildren(self)




    def and_test(self):

        localctx = PythonAssistantParser.And_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_and_test)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 148
            self.not_test()
            self.state = 153
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==14:
                self.state = 149
                self.match(PythonAssistantParser.AND)
                self.state = 150
                self.not_test()
                self.state = 155
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Not_testContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(PythonAssistantParser.NOT, 0)

        def not_test(self):
            return self.getTypedRuleContext(PythonAssistantParser.Not_testContext,0)


        def comparison(self):
            return self.getTypedRuleContext(PythonAssistantParser.ComparisonContext,0)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_not_test

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterNot_test" ):
                listener.enterNot_test(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitNot_test" ):
                listener.exitNot_test(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitNot_test" ):
                return visitor.visitNot_test(self)
            else:
                return visitor.visitChildren(self)




    def not_test(self):

        localctx = PythonAssistantParser.Not_testContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_not_test)
        try:
            self.state = 159
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [15]:
                self.enterOuterAlt(localctx, 1)
                self.state = 156
                self.match(PythonAssistantParser.NOT)
                self.state = 157
                self.not_test()
                pass
            elif token in [27, 34, 35, 36]:
                self.enterOuterAlt(localctx, 2)
                self.state = 158
                self.comparison()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparisonContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expr(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.ExprContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.ExprContext,i)


        def comp_op(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.Comp_opContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.Comp_opContext,i)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_comparison

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparison" ):
                listener.enterComparison(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparison" ):
                listener.exitComparison(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComparison" ):
                return visitor.visitComparison(self)
            else:
                return visitor.visitChildren(self)




    def comparison(self):

        localctx = PythonAssistantParser.ComparisonContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_comparison)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 161
            self.expr()
            self.state = 167
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 125829120) != 0):
                self.state = 162
                self.comp_op()
                self.state = 163
                self.expr()
                self.state = 169
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class Comp_opContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EE(self):
            return self.getToken(PythonAssistantParser.EE, 0)

        def NE(self):
            return self.getToken(PythonAssistantParser.NE, 0)

        def LT(self):
            return self.getToken(PythonAssistantParser.LT, 0)

        def GT(self):
            return self.getToken(PythonAssistantParser.GT, 0)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_comp_op

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComp_op" ):
                listener.enterComp_op(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComp_op" ):
                listener.exitComp_op(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitComp_op" ):
                return visitor.visitComp_op(self)
            else:
                return visitor.visitChildren(self)




    def comp_op(self):

        localctx = PythonAssistantParser.Comp_opContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_comp_op)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 170
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 125829120) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExprContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def term(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.TermContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.TermContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.PLUS)
            else:
                return self.getToken(PythonAssistantParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.MINUS)
            else:
                return self.getToken(PythonAssistantParser.MINUS, i)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_expr

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpr" ):
                listener.enterExpr(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpr" ):
                listener.exitExpr(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitExpr" ):
                return visitor.visitExpr(self)
            else:
                return visitor.visitChildren(self)




    def expr(self):

        localctx = PythonAssistantParser.ExprContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_expr)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 172
            self.term()
            self.state = 177
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==17 or _la==18:
                self.state = 173
                _la = self._input.LA(1)
                if not(_la==17 or _la==18):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 174
                self.term()
                self.state = 179
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TermContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.FactorContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.FactorContext,i)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.STAR)
            else:
                return self.getToken(PythonAssistantParser.STAR, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.SLASH)
            else:
                return self.getToken(PythonAssistantParser.SLASH, i)

        def IDIV(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.IDIV)
            else:
                return self.getToken(PythonAssistantParser.IDIV, i)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_term

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTerm" ):
                listener.enterTerm(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTerm" ):
                listener.exitTerm(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTerm" ):
                return visitor.visitTerm(self)
            else:
                return visitor.visitChildren(self)




    def term(self):

        localctx = PythonAssistantParser.TermContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_term)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 180
            self.factor()
            self.state = 185
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while (((_la) & ~0x3f) == 0 and ((1 << _la) & 5767168) != 0):
                self.state = 181
                _la = self._input.LA(1)
                if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 5767168) != 0)):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 182
                self.factor()
                self.state = 187
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def atom(self):
            return self.getTypedRuleContext(PythonAssistantParser.AtomContext,0)


        def trailer(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.TrailerContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.TrailerContext,i)


        def getRuleIndex(self):
            return PythonAssistantParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactor" ):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactor" ):
                listener.exitFactor(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitFactor" ):
                return visitor.visitFactor(self)
            else:
                return visitor.visitChildren(self)




    def factor(self):

        localctx = PythonAssistantParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 42, self.RULE_factor)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 188
            self.atom()
            self.state = 192
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,18,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 189
                    self.trailer() 
                self.state = 194
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,18,self._ctx)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AtomContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(PythonAssistantParser.ID, 0)

        def NUMBER(self):
            return self.getToken(PythonAssistantParser.NUMBER, 0)

        def STRING(self):
            return self.getToken(PythonAssistantParser.STRING, 0)

        def LPAREN(self):
            return self.getToken(PythonAssistantParser.LPAREN, 0)

        def test(self):
            return self.getTypedRuleContext(PythonAssistantParser.TestContext,0)


        def RPAREN(self):
            return self.getToken(PythonAssistantParser.RPAREN, 0)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_atom

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAtom" ):
                listener.enterAtom(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAtom" ):
                listener.exitAtom(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitAtom" ):
                return visitor.visitAtom(self)
            else:
                return visitor.visitChildren(self)




    def atom(self):

        localctx = PythonAssistantParser.AtomContext(self, self._ctx, self.state)
        self.enterRule(localctx, 44, self.RULE_atom)
        try:
            self.state = 202
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [36]:
                self.enterOuterAlt(localctx, 1)
                self.state = 195
                self.match(PythonAssistantParser.ID)
                pass
            elif token in [34]:
                self.enterOuterAlt(localctx, 2)
                self.state = 196
                self.match(PythonAssistantParser.NUMBER)
                pass
            elif token in [35]:
                self.enterOuterAlt(localctx, 3)
                self.state = 197
                self.match(PythonAssistantParser.STRING)
                pass
            elif token in [27]:
                self.enterOuterAlt(localctx, 4)
                self.state = 198
                self.match(PythonAssistantParser.LPAREN)
                self.state = 199
                self.test()
                self.state = 200
                self.match(PythonAssistantParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TrailerContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(PythonAssistantParser.LPAREN, 0)

        def RPAREN(self):
            return self.getToken(PythonAssistantParser.RPAREN, 0)

        def arglist(self):
            return self.getTypedRuleContext(PythonAssistantParser.ArglistContext,0)


        def DOT(self):
            return self.getToken(PythonAssistantParser.DOT, 0)

        def ID(self):
            return self.getToken(PythonAssistantParser.ID, 0)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_trailer

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTrailer" ):
                listener.enterTrailer(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTrailer" ):
                listener.exitTrailer(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitTrailer" ):
                return visitor.visitTrailer(self)
            else:
                return visitor.visitChildren(self)




    def trailer(self):

        localctx = PythonAssistantParser.TrailerContext(self, self._ctx, self.state)
        self.enterRule(localctx, 46, self.RULE_trailer)
        self._la = 0 # Token type
        try:
            self.state = 211
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [27]:
                self.enterOuterAlt(localctx, 1)
                self.state = 204
                self.match(PythonAssistantParser.LPAREN)
                self.state = 206
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if (((_la) & ~0x3f) == 0 and ((1 << _la) & 120393334784) != 0):
                    self.state = 205
                    self.arglist()


                self.state = 208
                self.match(PythonAssistantParser.RPAREN)
                pass
            elif token in [33]:
                self.enterOuterAlt(localctx, 2)
                self.state = 209
                self.match(PythonAssistantParser.DOT)
                self.state = 210
                self.match(PythonAssistantParser.ID)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ArglistContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def test(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(PythonAssistantParser.TestContext)
            else:
                return self.getTypedRuleContext(PythonAssistantParser.TestContext,i)


        def COMMA(self, i:int=None):
            if i is None:
                return self.getTokens(PythonAssistantParser.COMMA)
            else:
                return self.getToken(PythonAssistantParser.COMMA, i)

        def getRuleIndex(self):
            return PythonAssistantParser.RULE_arglist

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterArglist" ):
                listener.enterArglist(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitArglist" ):
                listener.exitArglist(self)

        def accept(self, visitor:ParseTreeVisitor):
            if hasattr( visitor, "visitArglist" ):
                return visitor.visitArglist(self)
            else:
                return visitor.visitChildren(self)




    def arglist(self):

        localctx = PythonAssistantParser.ArglistContext(self, self._ctx, self.state)
        self.enterRule(localctx, 48, self.RULE_arglist)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 213
            self.test()
            self.state = 218
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==30:
                self.state = 214
                self.match(PythonAssistantParser.COMMA)
                self.state = 215
                self.test()
                self.state = 220
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





