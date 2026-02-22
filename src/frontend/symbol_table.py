from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class SymbolType(Enum):
    VARIABLE = "variable"
    FUNCTION = "function"
    PARAMETER = "parameter"
    BUILTIN = "builtin"
    MODULE = "module"


@dataclass
class Symbol:
    name: str
    symbol_type: SymbolType
    data_type: Optional[str] = None
    line: int = 0
    column: int = 0
    is_dangerous: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


class Scope:

    def __init__(self, name: str, parent: Optional['Scope'] = None):
        self.name = name
        self.parent = parent
        self.symbols: Dict[str, Symbol] = {}
        self.children: List['Scope'] = []

        if parent:
            parent.children.append(self)

    def define(self, symbol: Symbol) -> None:
        self.symbols[symbol.name] = symbol

    def lookup(self, name: str) -> Optional[Symbol]:
        return self.symbols.get(name)

    def resolve(self, name: str) -> Optional[Symbol]:
        symbol = self.lookup(name)
        if symbol:
            return symbol
        if self.parent:
            return self.parent.resolve(name)
        return None

    def __repr__(self) -> str:
        return f"Scope({self.name}, symbols={list(self.symbols.keys())})"


class SymbolTable:

    BUILTINS = {
        'print', 'len', 'range', 'str', 'int', 'float', 'bool', 'list', 'dict',
        'input', 'open', 'type', 'isinstance', 'hasattr', 'getattr', 'setattr',
        'min', 'max', 'sum', 'abs', 'round', 'sorted', 'reversed', 'enumerate',
        'zip', 'map', 'filter', 'any', 'all', 'chr', 'ord'
    }

    DANGEROUS_BUILTINS = {
        'eval': 'Code Injection: eval() executes arbitrary code',
        'exec': 'Code Injection: exec() executes arbitrary code',
        'compile': 'Code Injection: compile() can create executable code',
        '__import__': 'Dynamic Import: __import__ can load arbitrary modules',
    }

    def __init__(self):
        self.global_scope = Scope("global")
        self.current_scope = self.global_scope
        self.scope_stack: List[Scope] = [self.global_scope]
        self._init_builtins()

    def _init_builtins(self) -> None:
        for name in self.BUILTINS:
            symbol = Symbol(
                name=name,
                symbol_type=SymbolType.BUILTIN,
                is_dangerous=name in self.DANGEROUS_BUILTINS
            )
            self.global_scope.define(symbol)

        for name in self.DANGEROUS_BUILTINS:
            if name not in self.BUILTINS:
                symbol = Symbol(
                    name=name,
                    symbol_type=SymbolType.BUILTIN,
                    is_dangerous=True
                )
                self.global_scope.define(symbol)

    def enter_scope(self, name: str) -> Scope:
        new_scope = Scope(name, self.current_scope)
        self.current_scope = new_scope
        self.scope_stack.append(new_scope)
        return new_scope

    def exit_scope(self) -> Optional[Scope]:
        if len(self.scope_stack) > 1:
            old_scope = self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]
            return old_scope
        return None

    def define(self, name: str, symbol_type: SymbolType,
               line: int = 0, column: int = 0, **metadata) -> Symbol:
        symbol = Symbol(
            name=name,
            symbol_type=symbol_type,
            line=line,
            column=column,
            metadata=metadata
        )
        self.current_scope.define(symbol)
        return symbol

    def define_function(self, name: str, parameters: List[str],
                        line: int = 0, column: int = 0) -> Symbol:
        return self.define(
            name, SymbolType.FUNCTION, line, column,
            parameters=parameters
        )

    def define_variable(self, name: str, line: int = 0, column: int = 0) -> Symbol:
        return self.define(name, SymbolType.VARIABLE, line, column)

    def define_parameter(self, name: str, line: int = 0, column: int = 0) -> Symbol:
        return self.define(name, SymbolType.PARAMETER, line, column)

    def resolve(self, name: str) -> Optional[Symbol]:
        return self.current_scope.resolve(name)

    def is_defined(self, name: str) -> bool:
        return self.resolve(name) is not None

    def is_dangerous(self, name: str) -> bool:
        symbol = self.resolve(name)
        return symbol is not None and symbol.is_dangerous

    def get_danger_reason(self, name: str) -> Optional[str]:
        return self.DANGEROUS_BUILTINS.get(name)

    def get_all_symbols(self) -> Dict[str, Symbol]:
        all_symbols = {}

        def collect(scope: Scope):
            all_symbols.update(scope.symbols)
            for child in scope.children:
                collect(child)

        collect(self.global_scope)
        return all_symbols

    def print_table(self) -> None:
        print("=== Symbol Table ===")

        def print_scope(scope: Scope, indent: int = 0):
            prefix = "  " * indent
            print(f"{prefix}Scope: {scope.name}")
            for name, symbol in scope.symbols.items():
                danger = " [DANGEROUS]" if symbol.is_dangerous else ""
                print(f"{prefix}  {name}: {symbol.symbol_type.value}{danger}")
            for child in scope.children:
                print_scope(child, indent + 1)

        print_scope(self.global_scope)
