import os
import re

def collect_c_files(root_dir):
    c_files = []
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".c"):
                c_files.append(os.path.join(root, file))
    return c_files


def clean_code(code):
    # Remove includes
    code = re.sub(r'#include.*', '', code)

    # Remove defines
    code = re.sub(r'#define.*', '', code)

    # Remove comments
    code = re.sub(r'//.*', '', code)
    code = re.sub(r'/\*.*?\*/', '', code, flags=re.DOTALL)

    return code


def extract_functions(code):
    """
    Extract simple function bodies (naive but works for Juliet patterns)
    """
    functions = re.findall(
        r'(void\s+\w+\s*\([^)]*\)\s*\{.*?\})',
        code,
        flags=re.DOTALL
    )
    return functions