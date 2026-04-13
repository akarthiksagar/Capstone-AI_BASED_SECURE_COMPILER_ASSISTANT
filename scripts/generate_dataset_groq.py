import os
import json
import time
import argparse
from tqdm import tqdm
try:
    from groq import Groq
except ImportError:
    print("Please install required packages: pip install groq python-dotenv")
    exit(1)

# Prompt to guide the LLM into generating SecureLang syntax
SYSTEM_PROMPT = """
You are an expert compiler engineer. Translate the following C/Python function into the custom "SecureLang" syntax.

SecureLang Rules:
1. It looks like Python but uses braces `{}` for blocks instead of indentation.
2. Uses `def func_name(args) { ... }` for functions.
3. No colons after if/while/def.
4. Uses standard operators (+, -, *, /) and assignments (x = 5).
5. Sinks like `exec(x)` or `eval(x)` or `system(x)` are built-in.
6. Sources like `input()` are built-in.
7. Return statements don't need parentheses.
8. Comments start with `//`.

IMPORTANT: Your response must ONLY contain the raw SecureLang code, without any markdown formatting, backticks, or explanations. If the snippet has a security vulnerability (e.g. arbitrary code execution, SQL injection), preserve that exact taint flow. If it is safe, ensure it remains safe.
"""

def generate_securelang_data(client, code_snippet, model="llama3-70b-8192"):
    """Translates a single snippet using Groq"""
    try:
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Translate this:\n\n{code_snippet}"}
            ],
            model=model,
            temperature=0.2,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq generation error: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Groq-Powered SecureLang Dataset Generator")
    parser.add_argument("--api-key", type=str, help="Groq API Key (or set GROQ_API_KEY env var)")
    parser.add_argument("--samples", type=int, default=100, help="Number of samples to generate")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("ERROR: Groq API Key required. Pass --api-key or set GROQ_API_KEY.")
        return

    client = Groq(api_key=api_key)

    try:
        from datasets import load_dataset
    except ImportError:
        print("ERROR: 'datasets' package not found.")
        print("Please install it: pip install datasets")
        return

    # ----------------------------------------------------
    # Load Real-World Vulnerability Dataset (CodeXGLUE Defect Detection)
    # This dataset contains real open source C/C++ functions labelled safe (0) or vulnerable (1)
    # ----------------------------------------------------
    print("Loading real-world dataset (code_x_glue_cc_defect_detection)...")
    dataset = load_dataset("code_x_glue_cc_defect_detection", split="train")

    # Shuffle to get a mix of vulnerabilities and select a subset
    dataset = dataset.shuffle(seed=42).select(range(args.samples))

    # Convert to standard format
    source_dataset = [
        {"code": item["func"], "label": item["target"]}
        for item in dataset
    ]

    results = []
    print(f"Starting LLM translation for {len(source_dataset)} real-world samples using Groq...")

    for i, item in enumerate(tqdm(source_dataset)):
        translated_code = generate_securelang_data(client, item["code"])
        
        if translated_code:
            # Basic cleanup of Markdown blocks if the LLM leaked them
            if translated_code.startswith("```"):
                translated_code = "\n".join(translated_code.split("\n")[1:-1])
                
            results.append({
                "id": str(i),
                "code": translated_code,
                "label": item["label"]
            })
            
        time.sleep(0.5) # Groq rate limit buffer

    # Write output
    os.makedirs("dataset", exist_ok=True)
    out_path = "dataset/secure_synthetic_groq.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSuccessfully generated {len(results)} SecureLang samples -> {out_path}")

if __name__ == "__main__":
    main()
