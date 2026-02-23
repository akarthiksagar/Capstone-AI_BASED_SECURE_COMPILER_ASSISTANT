import sys
import os
from typing import Optional, Tuple, List
from dataclasses import dataclass

grammar_path = os.path.join(os.path.dirname(__file__), 'grammar')
if grammar_path not in sys.path:
    sys.path.insert(0, grammar_path)

from antlr4 import CommonTokenStream, InputStream
from antlr4.error.ErrorListener import ErrorListener

from ..utils.errors import CompilerError, ErrorType, CompilationResult


class SecureLangErrorListener(ErrorListener):

    def __init__(self):
        super().__init__()
        self.errors: List[CompilerError] = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error = CompilerError(
            error_type=ErrorType.SYNTAX,
            message=msg,
            line=line,
            column=column
        )
        self.errors.append(error)

    def reportAmbiguity(self, recognizer, dfa, startIndex, stopIndex, exact, ambigAlts, configs):
        pass

    def reportAttemptingFullContext(self, recognizer, dfa, startIndex, stopIndex, conflictingAlts, configs):
        pass

    def reportContextSensitivity(self, recognizer, dfa, startIndex, stopIndex, prediction, configs):
        pass


class Lexer:

    def __init__(self):
        self.tokens = None
        self.errors: List[CompilerError] = []

    def tokenize(self, source: str) -> Tuple[Optional[CommonTokenStream], List[CompilerError]]:
        try:
            from SecureLangLexer import SecureLangLexer

            input_stream = InputStream(source)
            lexer = SecureLangLexer(input_stream)

            error_listener = SecureLangErrorListener()
            lexer.removeErrorListeners()
            lexer.addErrorListener(error_listener)

            tokens = CommonTokenStream(lexer)
            tokens.fill()

            self.tokens = tokens
            self.errors = error_listener.errors

            return tokens, self.errors

        except ImportError as e:
            error = CompilerError(
                error_type=ErrorType.INTERNAL,
                message=f"ANTLR lexer not generated. Run: antlr4 -Dlanguage=Python3 SecureLang.g4. Error: {e}",
                line=0
            )
            return None, [error]
        except Exception as e:
            error = CompilerError(
                error_type=ErrorType.LEXICAL,
                message=str(e),
                line=0
            )
            return None, [error]

    def get_tokens_list(self) -> List[dict]:
        if not self.tokens:
            return []

        result = []
        for token in self.tokens.tokens:
            result.append({
                'type': token.type,
                'text': token.text,
                'line': token.line,
                'column': token.column
            })
        return result


class Parser:

    def __init__(self):
        self.tree = None
        self.errors: List[CompilerError] = []

    def parse(self, tokens: CommonTokenStream) -> Tuple[Optional[object], List[CompilerError]]:
        try:
            from SecureLangParser import SecureLangParser

            parser = SecureLangParser(tokens)

            error_listener = SecureLangErrorListener()
            parser.removeErrorListeners()
            parser.addErrorListener(error_listener)

            tree = parser.program()

            self.tree = tree
            self.errors = error_listener.errors

            return tree, self.errors

        except ImportError as e:
            error = CompilerError(
                error_type=ErrorType.INTERNAL,
                message=f"ANTLR parser not generated. Run: antlr4 -Dlanguage=Python3 SecureLang.g4. Error: {e}",
                line=0
            )
            return None, [error]
        except Exception as e:
            error = CompilerError(
                error_type=ErrorType.SYNTAX,
                message=str(e),
                line=0
            )
            return None, [error]


class Frontend:

    def __init__(self):
        self.lexer = Lexer()
        self.parser = Parser()
        self.tokens = None
        self.parse_tree = None
        self.ast = None

    def process(self, source: str) -> CompilationResult:
        from .ast_builder import ASTBuilder
        from .semantic_analyzer import SemanticAnalyzer
        from .security_walker import SecurityWalker
        from .llm_security_checker import FrontendLLMSecurityChecker
        result = CompilationResult(success=True)

        tokens, lex_errors = self.lexer.tokenize(source)
        if lex_errors:
            for error in lex_errors:
                result.add_error(error)
            return result
        self.tokens = tokens

        parse_tree, parse_errors = self.parser.parse(tokens)
        if parse_errors:
            for error in parse_errors:
                result.add_error(error)
            return result
        self.parse_tree = parse_tree

        try:
            builder = ASTBuilder()
            self.ast = builder.build(parse_tree, source)
        except Exception as e:
            error = CompilerError(
                error_type=ErrorType.INTERNAL,
                message=f"AST construction failed: {e}",
                line=0
            )
            result.add_error(error)
            return result

        analyzer = SemanticAnalyzer()
        semantic_result = analyzer.analyze(self.ast)
        result.merge(semantic_result)

        walker = SecurityWalker()
        static_security_issues = walker.analyze(self.ast)
        for issue in static_security_issues:
            result.add_security_issue(issue)

        if not static_security_issues:
            llm_checker = FrontendLLMSecurityChecker()
            llm_security_issues = llm_checker.analyze(source)
            for issue in llm_security_issues:
                result.add_security_issue(issue)
                
        return result

    def get_ast(self):
        return self.ast

    def get_tokens(self) -> List[dict]:
        return self.lexer.get_tokens_list()
