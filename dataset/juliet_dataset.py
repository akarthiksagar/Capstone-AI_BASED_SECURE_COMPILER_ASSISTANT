import random
import json
import os

VARIABLES = ["a", "b", "c", "data", "user", "input_val", "cmd"]
SINKS = ["exec", "query"]
CONSTANTS = ["1", "5", "10", "100"]

def rand_var():
    return random.choice(VARIABLES)

def rand_const():
    return random.choice(CONSTANTS)

def generate_noise_block(var):
    """Generate irrelevant computation to make graph complex"""
    tmp = rand_var()
    return f"""
{tmp} = {rand_const()}
if {tmp} > 3 {{
    {tmp} = {tmp} + 1
}}
"""

def generate_vulnerable():

    src = rand_var()
    inter = rand_var()
    sink = random.choice(SINKS)

    noise = generate_noise_block(src)

    code = f"""
{src} = input()
{noise}
if {rand_const()} > 2 {{
    {inter} = {src}
}} else {{
    {inter} = sanitize({src})
}}
{sink}({inter})
"""

    return code.strip(), 1


def generate_safe():

    src = rand_var()
    inter = rand_var()
    sink = random.choice(SINKS)

    noise = generate_noise_block(src)

    code = f"""
{src} = input()
{noise}
if {rand_const()} > 2 {{
    {inter} = sanitize({src})
}} else {{
    {inter} = sanitize({src})
}}
{sink}({inter})
"""

    return code.strip(), 0


def generate_dataset(n_samples=5000):

    dataset = []

    for _ in range(n_samples // 2):
        code, label = generate_vulnerable()
        dataset.append({"code": code, "label": label})

    for _ in range(n_samples // 2):
        code, label = generate_safe()
        dataset.append({"code": code, "label": label})

    random.shuffle(dataset)

    return dataset


if __name__ == "__main__":

    os.makedirs("dataset", exist_ok=True)

    data = generate_dataset(5000)

    with open("dataset/securelang_juliet.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Generated 5000-sample dataset.")