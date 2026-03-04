from antlr4 import *
from grammar.generated.SecureLangLexer import SecureLangLexer
from grammar.generated.SecureLangParser import SecureLangParser


def test_parser(filename):
    input_stream = FileStream(filename)
    lexer = SecureLangLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = SecureLangParser(stream)

    tree = parser.program()

    print("Parsing completed successfully.")
    print(tree.toStringTree(recog=parser))


if __name__ == "__main__":
    test_parser("test_pointer.sec")