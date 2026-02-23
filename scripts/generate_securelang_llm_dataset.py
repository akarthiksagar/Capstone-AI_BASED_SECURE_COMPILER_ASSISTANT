# scripts/generate_securelang_llm_dataset.py
import argparse
import json
import os
import random
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional



def normalize_cwe(raw: str) -> str:
    if not raw:
        return "UNKNOWN"
    text = raw.replace("-", "").replace("_", "").strip()
    if text.startswith("CWE"):
        return text
    return f"CWE{text}"


def stratified_select(rows: List[dict], max_per_cwe: int, seed: int) -> List[dict]:
    random.seed(seed)
    by_cwe: Dict[str, List[dict]] = defaultdict(list)
    for row in rows:
        cwe = normalize_cwe(row.get("cwe", "UNKNOWN"))
        by_cwe[cwe].append(row)

    selected: List[dict] = []
    for cwe_rows in by_cwe.values():
        random.shuffle(cwe_rows)
        selected.extend(cwe_rows[:max_per_cwe])
    return selected


def build_prompt(c_code: str, cwe: str) -> str:
    return (
        "Translate the following vulnerable C code into SecureLang. "
        "Preserve vulnerability behavior for security analysis training. "
        "Use SecureLang syntax compatible with this compiler: function calls, import, assignments, if/while/for, return. "
        "Return only SecureLang code, no markdown. "
        f"CWE: {cwe}\n"
        "C code:\n"
        f"{c_code}\n"
    )


def call_openai(prompt: str, model: str) -> str:
    from openai import OpenAI

    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=prompt,
        max_output_tokens=700,
        temperature=0.1,
    )
    return response.output_text.strip()


def call_hf(prompt: str, model: str, max_new_tokens: int) -> str:
    from transformers import pipeline

    if "codebert" in model.lower():
        raise ValueError("CodeBERT is not supported for direct text2text dataset generation. Use a seq2seq model for generation and CodeBERT for training with scripts/train_securelang_translator.py")
    pipe = pipeline("text2text-generation", model=model)
    out = pipe(prompt, max_new_tokens=max_new_tokens, do_sample=False)
    return out[0]["generated_text"].strip()


def convert_with_backend(prompt: str, backend: str, model: str, max_new_tokens: int) -> str:
    if backend == "openai":
        return call_openai(prompt, model)
    return call_hf(prompt, model, max_new_tokens)


def validate_securelang(source: str) -> bool:
    from src.frontend.lexer_parser import Frontend
    frontend = Frontend()
    result = frontend.process(source)
    return not result.has_errors()


def run(args: argparse.Namespace) -> None:
    input_path = Path(args.input)
    out_dir = Path(args.output_dir)
    out_jsonl = Path(args.output_jsonl)

    rows = json.loads(input_path.read_text(encoding="utf-8"))
    selected = stratified_select(rows, args.max_per_cwe, args.seed)

    out_dir.mkdir(parents=True, exist_ok=True)
    accepted: List[dict] = []

    for idx, row in enumerate(selected):
        cwe = normalize_cwe(row.get("cwe", "UNKNOWN"))
        c_code = row.get("code", "")
        prompt = build_prompt(c_code, cwe)

        try:
            secure = convert_with_backend(
                prompt=prompt,
                backend=args.backend,
                model=args.model,
                max_new_tokens=args.max_new_tokens,
            )
        except Exception:
            continue

        if not secure:
            continue

        if not validate_securelang(secure):
            continue

        file_name = f"llm_sample_{idx}.secure"
        (out_dir / file_name).write_text(secure, encoding="utf-8")

        accepted.append(
            {
                "source_file": row.get("file", f"row_{idx}"),
                "cwe": cwe,
                "source_c": c_code,
                "target_securelang": secure,
                "output_file": file_name,
            }
        )

    with out_jsonl.open("w", encoding="utf-8") as f:
        for item in accepted:
            f.write(json.dumps(item) + "\n")

    print(f"Selected input samples: {len(selected)}")
    print(f"Accepted SecureLang samples: {len(accepted)}")
    print(f"Saved SecureLang files to: {out_dir}")
    print(f"Saved paired dataset to: {out_jsonl}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="datasets/juliet_dataset.json")
    parser.add_argument("--output-dir", default="datasets/secure_examples_llm")
    parser.add_argument("--output-jsonl", default="datasets/llm_translation_dataset.jsonl")
    parser.add_argument("--backend", choices=["openai", "hf"], default="hf")
    parser.add_argument("--model", default="google/flan-t5-base")
    parser.add_argument("--max-new-tokens", type=int, default=512)
    parser.add_argument("--max-per-cwe", type=int, default=200)
    parser.add_argument("--seed", type=int, default=7)
    return parser.parse_args()


if __name__ == "__main__":
    run(parse_args())
