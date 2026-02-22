import os
import json

JULIET_PATH = "datasets/raw/juliet/C/testcases"
OUTPUT_FILE = "datasets/juliet_dataset.json"

dataset = []

def detect_cwe(folder):
    parts = folder.split("_")
    return parts[0] if parts else "UNKNOWN"

for root, dirs, files in os.walk(JULIET_PATH):
    for file in files:

        if not file.endswith("_bad.c"):
            continue

        # Ignore support files
        if "io.c" in file.lower():
            continue

        full_path = os.path.join(root, file)

        try:
            with open(full_path, "r", errors="ignore") as f:
                code = f.read()

            folder_name = os.path.basename(root)
            cwe = detect_cwe(folder_name)

            
            dataset.append({
                "file": file,
                "cwe": cwe,
                "vulnerable": True,
                "code": code
            })

        except Exception as e:
            print("Skipped:", file, e)


os.makedirs("datasets", exist_ok=True)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(dataset, f, indent=2)

print("\nDONE")
print("Total vulnerable samples:", len(dataset))
print("Saved to:", OUTPUT_FILE)
