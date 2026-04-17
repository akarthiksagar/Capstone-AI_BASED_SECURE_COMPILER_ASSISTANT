import ast
import re
import json
from typing import Dict, Any

class UniversalTranslator:
    def __init__(self):
        self.indent_level = 0

    def translate(self, code: str, language: str) -> str:
        """Translate code from any language to SecureLang"""
        if language.lower() == 'python':
            return self.translate_python(code)
        elif language.lower() in ['c', 'cpp']:
            return self.translate_c(code)
        elif language.lower() == 'javascript':
            return self.translate_javascript(code)
        else:
            return self.fallback_translate(code)

    def translate_python(self, code: str) -> str:
        """Translate Python to SecureLang"""
        try:
            tree = ast.parse(code)
            return self.python_ast_to_securelang(tree)
        except:
            return self.fallback_translate(code)

    def python_ast_to_securelang(self, node: ast.AST) -> str:
        """Convert Python AST to SecureLang"""
        if isinstance(node, ast.Module):
            return '\n'.join(self.python_ast_to_securelang(stmt) for stmt in node.body)

        elif isinstance(node, ast.FunctionDef):
            params = ', '.join(arg.arg for arg in node.args.args)
            body = '\n'.join('    ' + self.python_ast_to_securelang(stmt) for stmt in node.body)
            return f"def {node.name}({params}) {{\n{body}\n}}"

        elif isinstance(node, ast.If):
            cond = self.python_ast_to_securelang(node.test)
            body = '\n'.join('    ' + self.python_ast_to_securelang(stmt) for stmt in node.body)
            else_body = ''
            if node.orelse:
                else_body = '\nelse {\n' + '\n'.join('    ' + self.python_ast_to_securelang(stmt) for stmt in node.orelse) + '\n}'
            return f"if {cond} {{\n{body}\n}}{else_body}"

        elif isinstance(node, ast.While):
            cond = self.python_ast_to_securelang(node.test)
            body = '\n'.join('    ' + self.python_ast_to_securelang(stmt) for stmt in node.body)
            return f"while {cond} {{\n{body}\n}}"

        elif isinstance(node, ast.For):
            # Simple for loop translation
            target = self.python_ast_to_securelang(node.target)
            iter_expr = self.python_ast_to_securelang(node.iter)
            body = '\n'.join('    ' + self.python_ast_to_securelang(stmt) for stmt in node.body)
            return f"for {target} in {iter_expr} {{\n{body}\n}}"

        elif isinstance(node, ast.Assign):
            targets = ', '.join(self.python_ast_to_securelang(t) for t in node.targets)
            value = self.python_ast_to_securelang(node.value)
            return f"{targets} = {value}"

        elif isinstance(node, ast.Return):
            if node.value:
                return f"return {self.python_ast_to_securelang(node.value)}"
            return "return"

        elif isinstance(node, ast.Expr):
            return self.python_ast_to_securelang(node.value)

        elif isinstance(node, ast.Call):
            func = self.python_ast_to_securelang(node.func)
            args = ', '.join(self.python_ast_to_securelang(arg) for arg in node.args)
            return f"{func}({args})"

        elif isinstance(node, ast.Name):
            return node.id

        elif isinstance(node, ast.Str):
            return f'"{node.s}"'

        elif isinstance(node, ast.Num):
            return str(node.n)

        elif isinstance(node, ast.BinOp):
            left = self.python_ast_to_securelang(node.left)
            right = self.python_ast_to_securelang(node.right)
            op = self.get_op(node.op)
            return f"{left} {op} {right}"

        elif isinstance(node, ast.Compare):
            left = self.python_ast_to_securelang(node.left)
            comparators = [self.python_ast_to_securelang(c) for c in node.comparators]
            ops = [self.get_op(o) for o in node.ops]
            comparisons = [f"{left} {ops[0]} {comparators[0]}"]
            for i in range(1, len(ops)):
                comparisons.append(f"{comparators[i-1]} {ops[i]} {comparators[i]}")
            return ' and '.join(comparisons)

        else:
            return "// Unsupported construct"

    def get_op(self, op):
        ops = {
            ast.Add: '+', ast.Sub: '-', ast.Mult: '*', ast.Div: '/',
            ast.Eq: '==', ast.NotEq: '!=', ast.Lt: '<', ast.LtE: '<=',
            ast.Gt: '>', ast.GtE: '>=', ast.And: 'and', ast.Or: 'or'
        }
        return ops.get(type(op), '?')

    def translate_c(self, code: str) -> str:
        """Basic C to SecureLang translation"""
        # Remove includes and main function wrapper
        code = re.sub(r'#include.*\n', '', code)
        code = re.sub(r'int main\(.*?\) \{', 'def main() {', code, flags=re.DOTALL)
        code = re.sub(r'return 0;\s*\}', '}', code)

        # Basic replacements
        replacements = {
            'printf(': 'print(',
            'scanf(': 'input(',
            'strcpy(': 'strcpy(',  # Keep as is, assume SecureLang has it
            'strcmp(': 'strcmp(',
            'strlen(': 'len(',
            'int ': '',  # Remove type declarations
            'char ': '',
            'void ': '',
            ';': '',  # Remove semicolons
            '{': '{\n',
            '}': '\n}',
            'if(': 'if ',
            'while(': 'while ',
            'for(': 'for ',
        }

        for old, new in replacements.items():
            code = code.replace(old, new)

        # Fix braces and indentation
        lines = code.split('\n')
        result = []
        indent = 0
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if '}' in line:
                indent = max(0, indent - 1)
            result.append('    ' * indent + line)
            if '{' in line:
                indent += 1

        return '\n'.join(result)

    def translate_javascript(self, code: str) -> str:
        """Basic JavaScript to SecureLang translation"""
        # Basic replacements
        replacements = {
            'console.log(': 'print(',
            'function ': 'def ',
            'var ': '',
            'let ': '',
            'const ': '',
            'if(': 'if ',
            'while(': 'while ',
            'for(': 'for ',
            ';': '',
            '{': '{\n',
            '}': '\n}',
        }

        for old, new in replacements.items():
            code = code.replace(old, new)

        return code

    def fallback_translate(self, code: str) -> str:
        """Fallback: minimal cleaning"""
        # Remove common syntax
        code = re.sub(r'#include.*', '', code)
        code = re.sub(r'import.*', '', code)
        code = re.sub(r';', '', code)
        return f"// Fallback translation\n{code}"

def main():
    translator = UniversalTranslator()

    # Test examples
    test_cases = [
        ("python", "def hello(name):\n    print(f'Hello {name}')"),
        ("c", "#include <stdio.h>\nint main() {\n    printf(\"Hello\");\n    return 0;\n}"),
        ("javascript", "function hello(name) {\n    console.log('Hello ' + name);\n}")
    ]

    for lang, code in test_cases:
        translated = translator.translate(code, lang)
        print(f"=== {lang.upper()} ===")
        print(translated)
        print()

if __name__ == "__main__":
    main()