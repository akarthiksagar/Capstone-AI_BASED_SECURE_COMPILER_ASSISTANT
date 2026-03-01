from antlr4.error.ErrorListener import ErrorListener
from frontend.errors.syntax_errors import SyntaxErrorDetail


class SecureLangErrorListener(ErrorListener):

    def __init__(self):
        super().__init__()
        self.errors = []

    def syntaxError(self, recognizer, offendingSymbol, line, column, msg, e):
        error = SyntaxErrorDetail(line, column, msg)
        self.errors.append(error)

    def has_errors(self):
        return len(self.errors) > 0

    def get_errors(self):
        return self.errors