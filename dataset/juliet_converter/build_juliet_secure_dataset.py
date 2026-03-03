# dataset/juliet_converter/build_juliet_text_dataset.py

import os
import json
import re
from tqdm import tqdm

# -----------------------------------
# CONFIG
# -----------------------------------

JULIET_ROOT = "dataset/juliet_raw/C/testcases"
OUTPUT_FILE = "dataset/juliet_processed.json"

MAX_FUNCTION_LENGTH = 5000   # skip huge functions
MIN_FUNCTION_LENGTH = 50     # skip trivial ones

# -----------------------------------
# UTILITIES
# -----------------------------------

def collect_c_files(root):
    c_files = []
    for root_dir, _, files in os.walk(root):
        for f in files:
            if f.endswith(".c"):
                c_files.append(os.path.join(root_dir, f))
    return c_files


def remove_comments(code):
    # Remove /* ... */ comments
    code = re.sub(r"/\*.*?\*/", "", code, flags=re.DOTALL)
    # Remove // comments
    code = re.sub(r"//.*", "", code)
    return code


def remove_preprocessor(code):
    lines = code.splitlines()
    clean_lines = [line for line in lines if not line.strip().startswith("#")]
    return "\n".join(clean_lines)


def extract_functions(code):
    """
    Extract C functions using brace matching.
    This is simple but robust enough for Juliet.
    """
    functions = []
    pattern = re.compile(r"\b(?:void|int|char|float|double|long|short)\s+\w+\s*\([^)]*\)\s*\{", re.MULTILINE)

    for match in pattern.finditer(code):
        start = match.start()
        brace_count = 0
        i = start
        while i < len(code):
            if code[i] == "{":
                brace_count += 1
            elif code[i] == "}":
                brace_count -= 1
                if brace_count == 0:
                    functions.append(code[start:i+1])
                    break
            i += 1

    return functions


def label_function(func):
    """
    Juliet naming convention:
    bad() functions are vulnerable.
    good() functions are safe.
    """
    if re.search(r"\bbad\s*\(", func):
        return 1
    if re.search(r"\bgood", func):
        return 0
    return None


def is_supported(func):
    """
    Filter out very complex or irrelevant functions.
    """
    if len(func) < MIN_FUNCTION_LENGTH:
        return False
    if len(func) > MAX_FUNCTION_LENGTH:
        return False
    return True


# -----------------------------------
# MAIN BUILDER
# -----------------------------------

def build_dataset():
    dataset = []
    c_files = collect_c_files(JULIET_ROOT)

    print("Total C files found:", len(c_files))

    for path in tqdm(c_files):
        try:
            with open(path, "r", errors="ignore") as f:
                raw = f.read()

            code = remove_comments(raw)
            code = remove_preprocessor(code)

            functions = extract_functions(code)

            for func in functions:
                label = label_function(func)
                if label is None:
                    continue

                if not is_supported(func):
                    continue

                dataset.append({
                    "code": func.strip(),
                    "label": label
                })

        except Exception:
            continue

    print("Generated samples:", len(dataset))

    with open(OUTPUT_FILE, "w") as f:
        json.dump(dataset, f, indent=2)

    print("Saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    build_dataset()