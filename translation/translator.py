# translation/translator.py

import sys
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

sys.path.append(".")

MODEL_NAME = "deepseek-ai/deepseek-coder-1.3b-instruct"

print("Loading tokenizer...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

print("Loading model...")
model = AutoModelForCausalLM.from_pretrained(
    MODEL_NAME,
    torch_dtype=torch.float16,
    device_map="auto"
)

print("Model loaded successfully.")

# -------------------------------------
# PROMPT BUILDER
# -------------------------------------

def build_prompt(c_code):

    return f"""
Rewrite the following C function into a simplified pseudo language.

Rules:
- Remove all type declarations.
- Remove includes.
- Remove pointer symbols.
- Keep only logical statements.
- Allowed statements:
  assignment: x = expression
  if condition {{ ... }} else {{ ... }}
  function call: func(arg)
  return expression
- Replace system() with exec()
- Replace scanf/fgets/gets with input()
- Do NOT use markdown.
- Do NOT use backticks.
- Output plain text only.

C function:
{c_code}

Output:
"""

# -------------------------------------
# TRANSLATE
# -------------------------------------

def translate(c_code, max_tokens=200):

    prompt = build_prompt(c_code)

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_tokens,
            temperature=0.0,      # deterministic
            do_sample=False,
            repetition_penalty=1.2
        )

    decoded = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # Remove prompt part
    decoded = decoded.replace(prompt, "")

    return decoded.strip()
# -------------------------------------
# VALIDATION
# -------------------------------------

def is_valid_securelang(code):

    try:
        from frontend.parser_driver import parse_source
        parse_source(code)
        return True
    except Exception:
        return False