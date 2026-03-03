import random
import json
import os

VARS = ["user", "data", "input_val", "cmd", "path", "query", "filename", "payload"]
SANITIZERS = ["sanitize", "validate", "escape"]
SINKS = ["exec", "open_file", "db_query"]
AUTH_FUNCS = ["is_admin", "check_auth"]
CONSTS = ["1", "5", "10", "100"]

def rand_var():
    return random.choice(VARS)

def rand_sanitizer():
    return random.choice(SANITIZERS)

def rand_sink():
    return random.choice(SINKS)

def rand_auth():
    return random.choice(AUTH_FUNCS)

def rand_const():
    return random.choice(CONSTS)

# ----------------------------------------------------
# Add small structural noise for graph diversity
# ----------------------------------------------------

def noise_block():
    v = rand_var()
    return f"""
{v} = {rand_const()}
if {v} > 0 {{
    {v} = {v} - 1
}}
"""

# ----------------------------------------------------
# COMMAND INJECTION
# ----------------------------------------------------

def command_injection_vuln():
    v = rand_var()
    return f"""
{v} = input()
{noise_block()}
exec({v})
""".strip(), 1, "command_injection"

def command_injection_safe():
    v = rand_var()
    s = rand_sanitizer()
    return f"""
{v} = input()
{v} = {s}({v})
exec({v})
""".strip(), 0, "command_injection"

# ----------------------------------------------------
# PATH TRAVERSAL
# ----------------------------------------------------

def path_traversal_vuln():
    v = rand_var()
    return f"""
{v} = input()
open_file({v})
""".strip(), 1, "path_traversal"

def path_traversal_safe():
    v = rand_var()
    s = rand_sanitizer()
    return f"""
{v} = input()
{v} = {s}({v})
open_file({v})
""".strip(), 0, "path_traversal"

# ----------------------------------------------------
# SQL INJECTION
# ----------------------------------------------------

def sql_injection_vuln():
    v = rand_var()
    return f"""
{v} = input()
db_query({v})
""".strip(), 1, "sql_injection"

def sql_injection_safe():
    v = rand_var()
    s = rand_sanitizer()
    return f"""
{v} = input()
{v} = {s}({v})
db_query({v})
""".strip(), 0, "sql_injection"

# ----------------------------------------------------
# UNCHECKED LOOP
# ----------------------------------------------------

def unchecked_loop_vuln():
    v = rand_var()
    return f"""
{v} = input()
while {v} > 0 {{
    exec({v})
    {v} = {v} - 1
}}
""".strip(), 1, "unchecked_loop"

def unchecked_loop_safe():
    v = rand_var()
    return f"""
{v} = input()
if {v} < 10 {{
    while {v} > 0 {{
        exec({v})
        {v} = {v} - 1
    }}
}}
""".strip(), 0, "unchecked_loop"

# ----------------------------------------------------
# MISSING AUTH
# ----------------------------------------------------

def missing_auth_vuln():
    v = rand_var()
    return f"""
{v} = input()
exec({v})
""".strip(), 1, "missing_auth"

def missing_auth_safe():
    v = rand_var()
    a = rand_auth()
    return f"""
{v} = input()
if {a}() {{
    exec({v})
}}
""".strip(), 0, "missing_auth"

# ----------------------------------------------------
# GENERATOR LIST
# ----------------------------------------------------

GENERATORS = [
    command_injection_vuln,
    command_injection_safe,
    path_traversal_vuln,
    path_traversal_safe,
    sql_injection_vuln,
    sql_injection_safe,
    unchecked_loop_vuln,
    unchecked_loop_safe,
    missing_auth_vuln,
    missing_auth_safe
]

# ----------------------------------------------------
# MAIN DATASET GENERATION
# ----------------------------------------------------

def generate_dataset(n_samples=10000):
    dataset = []

    for _ in range(n_samples):
        generator = random.choice(GENERATORS)
        code, label, vuln_type = generator()

        dataset.append({
            "code": code.strip(),
            "label": label,
            "vuln_type": vuln_type
        })

    return dataset


if __name__ == "__main__":
    os.makedirs("dataset", exist_ok=True)

    data = generate_dataset(10000)

    with open("dataset/secure_synthetic_10k.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Generated dataset:", len(data))