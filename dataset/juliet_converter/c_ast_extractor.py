import os
import pycparser
from pycparser import parse_file,c_ast,c_parser
import re

def remove_comments(code):
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)
    code = re.sub(r'//.*', '', code)
    return code


def parse_c_file(filepath):

    try:
        with open(filepath, "r", errors="ignore") as f:
            code = f.read()

        code = remove_comments(code)

        cleaned_lines = []
        for line in code.splitlines():
            if line.strip().startswith("#"):
                continue
            cleaned_lines.append(line)

        cleaned_code = "\n".join(cleaned_lines)

        # 🔥 Inject fake typedefs
        fake_typedefs = """
typedef int DWORD;
typedef int size_t;
typedef int BOOL;
typedef int wchar_t;
typedef int HANDLE;
typedef int HCRYPTPROV;
typedef int HCRYPTKEY;
typedef int HCRYPTHASH;
"""

        cleaned_code = fake_typedefs + "\n" + cleaned_code

        # Neutralize tokens
        cleaned_code = cleaned_code.replace("__declspec", "")
        cleaned_code = cleaned_code.replace("__attribute__", "")
        cleaned_code = cleaned_code.replace("WINAPI", "")

        parser = c_parser.CParser()
        ast = parser.parse(cleaned_code)

        return ast

    except Exception as e:
        print("Parse failed:", filepath)
        print(e)
        return None

class FunctionExtractor(c_ast.NodeVisitor):

    def __init__(self):
        self.functions = []

    def visit_FuncDef(self, node):
        self.functions.append(node)