import os
import re

JULIET_PATH = "datasets/raw/juliet/C/testcases"
OUTPUT_DIR = "datasets/secure_examples"

os.makedirs(OUTPUT_DIR, exist_ok=True)


SOURCE_PATTERNS = [
    r'gets\s*\(',
    r'fgets\s*\(',
    r'scanf\s*\(',
    r'recv\s*\(',
    r'fread\s*\('
]


SINK_PATTERNS = {
    r'system\s*\(': "system",
    r'exec\w*\s*\(': "exec",
    r'popen\s*\(': "popen",
    r'sprintf\s*\(': "format"
}


def contains_pattern(code, patterns):
    for p in patterns:
        if re.search(p, code):
            return True
    return False


def detect_sink(code):
    for pattern, name in SINK_PATTERNS.items():
        if re.search(pattern, code):
            return name
    return None


def convert_to_securelang(code):

    has_input = contains_pattern(code, SOURCE_PATTERNS)
    sink = detect_sink(code)

    if not has_input and not sink:
        return None

    secure_code = []

    # simulate tainted input
    if has_input:
        secure_code.append("data = input()")

    # simulate dangerous sink
    if sink == "system":
        secure_code.append("system(data)")
    elif sink == "exec":
        secure_code.append("exec(data)")
    elif sink == "popen":
        secure_code.append("popen(data)")
    elif sink == "format":
        secure_code.append('query = "SELECT..." + data')
        secure_code.append("execute(query)")

    return "\n".join(secure_code)


count = 0

for root, _, files in os.walk(JULIET_PATH):

    for file in files:

        if not file.endswith(".c"):
            continue

        path = os.path.join(root, file)

        try:
            with open(path, "r", errors="ignore") as f:
                code = f.read()

            converted = convert_to_securelang(code)

            if converted:

                out_file = f"sample_{count}.secure"
                with open(os.path.join(OUTPUT_DIR, out_file), "w") as out:
                    out.write(converted)

                count += 1

        except Exception:
            pass

print("Converted samples:", count)
print("Saved to:", OUTPUT_DIR)
