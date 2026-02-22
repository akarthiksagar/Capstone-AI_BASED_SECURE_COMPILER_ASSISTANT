import os
import re
import json

from src.frontend.lexer_parser import Frontend
from src.middle_end.ir_generator import IRGenerator
from src.middle_end.security_analyzer import MiddleEndSecurityAnalyzer


JULIET = "datasets/raw/juliet/C/testcases"
TEMP_SECURE = "datasets/generated_secure"
REPORT_FILE = "datasets/security_report.json"

os.makedirs(TEMP_SECURE, exist_ok=True)


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
    r'sprintf\s*\(': "sql"
}


def has_source(code):
    for p in SOURCE_PATTERNS:
        if re.search(p, code):
            return True
    return False


def detect_sink(code):
    for p, name in SINK_PATTERNS.items():
        if re.search(p, code):
            return name
    return None


def convert(code):

    src = has_source(code)
    sink = detect_sink(code)

    if not src and not sink:
        return None

    lines = []

    if src:
        lines.append("data = input()")

    if sink == "system":
        lines.append("system(data)")
    elif sink == "exec":
        lines.append("exec(data)")
    elif sink == "popen":
        lines.append("popen(data)")
    elif sink == "sql":
        lines.append('query = "SELECT..." + data')
        lines.append("execute(query)")

    return "\n".join(lines)


frontend = Frontend()
irgen = IRGenerator()
security = MiddleEndSecurityAnalyzer()

results = []
converted_count = 0

for root, _, files in os.walk(JULIET):

    for f in files:

        if not f.endswith(".c"):
            continue

        path = os.path.join(root, f)

        try:
            with open(path, "r", errors="ignore") as file:
                code = file.read()

            secure_code = convert(code)

            if not secure_code:
                continue

            res = frontend.process(secure_code)

            if res.has_errors():
                continue

            ast = frontend.get_ast()
            program = irgen.generate(ast)

            sec = security.analyze(program)

            is_vulnerable = len(sec.security_issues) > 0

            results.append({
                "file": f,
                "secure_code": secure_code,
                "issues": [str(i) for i in sec.security_issues],
                "label": "vulnerable" if is_vulnerable else "safe"
            })

            converted_count += 1

        except Exception:
            pass


with open(REPORT_FILE, "w", encoding="utf8") as out:
    json.dump(results, out, indent=2)

print("\nDONE")
print("Samples processed:", converted_count)
print("Report saved:", REPORT_FILE)
