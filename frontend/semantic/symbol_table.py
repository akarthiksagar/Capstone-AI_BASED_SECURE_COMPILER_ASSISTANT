class Symbol:
    def __init__(self, name, symbol_type, security_label=None):
        self.name = name
        self.type = symbol_type
        self.security_label = security_label


class FunctionSymbol:
    def __init__(self, name, parameters):
        self.name = name
        self.parameters = parameters  # list of parameter names
        self.return_type = None
        self.return_security = None



class SymbolTable:

    def __init__(self):
        self.scopes = [{}]
        self.functions = {}

    def enter_scope(self):
        self.scopes.append({})

    def exit_scope(self):
        self.scopes.pop()

    def define(self, name, symbol):
        if name in self.scopes[-1]:
            raise Exception(f"Variable '{name}' already defined in this scope.")
        self.scopes[-1][name] = symbol

    def resolve(self, name):
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        raise Exception(f"Undefined variable '{name}'.")
    
    def define_function(self, func_symbol):
        self.functions[func_symbol.name] = func_symbol

    def resolve_function(self, name):
        if name in self.functions:
            return self.functions[name]
        raise Exception(f"Undefined function '{name}'")