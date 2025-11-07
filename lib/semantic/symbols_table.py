from dataclasses import dataclass
from typing import Dict, List, Optional
from lib.parser.ast import declarations, types

@dataclass(slots=True)
class Symbol:
    name: str

@dataclass(slots=True)
class VariableSymbol(Symbol):
    type_spec: types.TypeSpecifier

@dataclass(slots=True)
class FunctionSymbol(Symbol):
    params: list[declarations.ParamDecl]
    return_type: types.TypeSpecifier

@dataclass(slots=True)
class StructSymbol(Symbol):
    fields: Dict[str, types.TypeSpecifier]

class SymbolTable:
    def __init__(self) -> None:
        self.scopes: List[Dict[str, Symbol]] = [{}]

    def begin_scope(self) -> None:
        self.scopes.append({})

    def end_scope(self) -> None:
        if len(self.scopes) > 1:
            self.scopes.pop()

    def define(self, symbol: Symbol) -> bool:
        scope = self.scopes[-1]
        if symbol.name in scope:
            return False
        scope[symbol.name] = symbol
        return True

    def lookup(self, name: str) -> Optional[Symbol]:
        for scope in reversed(self.scopes):
            if name in scope:
                return scope[name]
        return None

    def lookup_in_current(self, name: str) -> Optional[Symbol]:
        scope = self.scopes[-1]
        return scope.get(name)
