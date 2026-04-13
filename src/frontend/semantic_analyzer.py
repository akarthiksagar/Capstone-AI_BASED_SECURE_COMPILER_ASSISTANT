from .PythonAssistantParserListener import PythonAssistantParserListener

class SymbolTable:
    def __init__(self):
        self.scopes = [{}]  # Stack of scopes (dictionaries)

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def declare(self, name, type_info="var", line=0):
        current_scope = self.scopes[-1]
        if name in current_scope:
            return False  # Already declared in this scope (redeclare? Python allows it)
        current_scope[name] = {"type": type_info, "line": line}
        return True

    def lookup(self, name):
        # Look from inner to outer scope
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

class SemanticAnalyzer(PythonAssistantParserListener):
    def __init__(self):
        self.symbol_table = SymbolTable()
        self.errors = []
        # Pre-populate global scope with built-ins if needed
        self._declare_builtins()

    def _declare_builtins(self):
        builtins = ["print", "range", "len", "str", "int", "float", "list", "dict", "set", "input", "os", "sys", "eval", "exec", "open"]
        for b in builtins:
            self.symbol_table.declare(b, "builtin")

    def enterFuncdef(self, ctx):
        func_name = ctx.ID().getText()
        self.symbol_table.declare(func_name, "function", ctx.start.line)
        self.symbol_table.enter_scope()

    def exitFuncdef(self, ctx):
        self.symbol_table.exit_scope()

    def enterParam(self, ctx):
        param_name = ctx.ID().getText()
        self.symbol_table.declare(param_name, "parameter", ctx.start.line)

    def enterAssignment(self, ctx):
        # assignment: ID ASSIGN test
        var_name = ctx.ID().getText()
        # Python declares variables on assignment if not exists
        self.symbol_table.declare(var_name, "variable", ctx.start.line)

    def enterAtom(self, ctx):
        # atom: ID | ...
        if ctx.ID():
            name = ctx.ID().getText()
            # Check if declared
            if not self.symbol_table.lookup(name):
                self.errors.append({
                    "line": ctx.start.line,
                    "message": f"Undefined variable or function '{name}'"
                })
