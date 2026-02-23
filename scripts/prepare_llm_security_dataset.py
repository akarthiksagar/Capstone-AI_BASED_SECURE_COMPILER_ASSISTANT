# scripts/prepare_llm_security_dataset.py
import json
import os
import random
import re
from collections import defaultdict

INPUT_FILE = "datasets/juliet_dataset.json"
OUTPUT_FILE = "datasets/llm_security_subset.json"
SEED = 7
PER_CWE_LIMIT = 120
TARGET_CWES = {
    "CWE78",
    "CWE89",
    "CWE94",
    "CWE502",
}


def _extract_cwe(cwe_text: str) -> str:
    m = re.search(r"CWE[-_]?\d+", cwe_text or "")
    if not m:
        return "UNKNOWN"
    return m.group(0).replace("-", "").replace("_", "")


def _to_securelang_stub(code: str, cwe: str):
    lowered = code.lower()
    lines = ["data = input()"]

    if cwe == "CWE78" or "system(" in lowered or "popen(" in lowered:
        lines += ["import os", "os.system(data)"]
    elif cwe == "CWE89" or "execute(" in lowered or "sprintf(" in lowered:
        lines += ['query = "SELECT * FROM users WHERE id=" + data', "execute(query)"]
    elif cwe == "CWE94" or "eval(" in lowered or "exec(" in lowered:
        lines += ["eval(data)"]
    elif cwe == "CWE502" or "pickle" in lowered:
        lines += ["import pickle", "obj = pickle.loads(data)"]
    else:
        return None

    return "\n".join(lines)


def _frontend_obfuscation_variants(base_secure_code: str):
    variants = [base_secure_code]

    if "import os" in base_secure_code and "os.system" in base_secure_code:
        variants.append(base_secure_code.replace("import os", "import os as o").replace("os.system", "o.system"))

    if "import pickle" in base_secure_code and "pickle.loads" in base_secure_code:
        variants.append(base_secure_code.replace("import pickle", "import pickle as pk").replace("pickle.loads", "pk.loads"))

    return variants


def main():
    random.seed(SEED)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    per_cwe = defaultdict(list)
    for row in dataset:
        cwe = _extract_cwe(row.get("cwe", ""))
        if cwe in TARGET_CWES:
            per_cwe[cwe].append(row)

    selected = []
    for cwe, rows in per_cwe.items():
        random.shuffle(rows)
        selected.extend(rows[:PER_CWE_LIMIT])

    transformed = []
    for item in selected:
        cwe = _extract_cwe(item.get("cwe", ""))
        secure_code = _to_securelang_stub(item.get("code", ""), cwe)
        if not secure_code:
            continue

        for variant in _frontend_obfuscation_variants(secure_code):
            transformed.append(
                {
                    "source_file": item.get("file"),
                    "cwe": cwe,
                    "frontend_code": variant,
                    "expected_label": "vulnerable",
                    "training_target": {
                        "frontend": "detect",
                        "middle_end": "detect",
                    },
                }
            )

    os.makedirs("datasets", exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(transformed, f, indent=2)

    print(f"Saved {len(transformed)} curated samples to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
