from antlr4 import *
from grammar.generated.SecureLangLexer import SecureLangLexer
from grammar.generated.SecureLangParser import SecureLangParser
from frontend.errors.error_listener import SecureLangErrorListener
from frontend.ast_builder import ASTBuilder

class ParseResult:
    def __init__(self, tree, errors):
        self.tree = tree
        self.errors = errors

    def is_success(self):
        return len(self.errors) == 0


class ParserDriver:

    def parse(self, source_code: str) -> ParseResult:
        input_stream = InputStream(source_code)

        lexer = SecureLangLexer(input_stream)
        token_stream = CommonTokenStream(lexer)

        parser = SecureLangParser(token_stream)

        # Remove default error listeners
        lexer.removeErrorListeners()
        parser.removeErrorListeners()

        # Attach custom listener
        error_listener = SecureLangErrorListener()
        parser.addErrorListener(error_listener)

        tree = parser.program()
        print(tree.toStringTree(recog=parser))
        return ParseResult(tree, error_listener.get_errors())
    

def parse_source(source_code: str):

    driver = ParserDriver()
    result = driver.parse(source_code)

    if not result.is_success():
        print("====== SYNTAX ERRORS ======")
        for err in result.errors:
            try:
                print(f"Line {err.line}:{err.column} → {err.message}")
            except:
                print(err)
        raise Exception("Parsing failed")

    builder = ASTBuilder()
    ast = builder.visit(result.tree)

    return ast