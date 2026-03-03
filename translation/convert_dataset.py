# translation/convert_dataset.py

import json
from tqdm import tqdm
from translator import translate, is_valid_securelang

INPUT_FILE = "dataset/juliet_balanced.json"
OUTPUT_FILE = "dataset/juliet_securelang.json"

MAX_SAMPLES = 10  # start small for testing

def main():

    print("Loading dataset...")
    with open(INPUT_FILE, "r") as f:
        data = json.load(f)

    subset = data[:MAX_SAMPLES]

    translated_samples = []

    print("Starting translation...")

    for sample in tqdm(subset):

        c_code = sample["code"]
        label = sample["label"]

        try:
            secure_code = translate(c_code)

            if (len(secure_code) > 10 and "```" not in secure_code and is_valid_securelang(secure_code)):
                translated_samples.append({
                    "code": secure_code,
                    "label": label
                })

        except Exception:
            continue

    print("Valid translations:", len(translated_samples))

    with open(OUTPUT_FILE, "w") as f:
        json.dump(translated_samples, f, indent=2)

    print("Saved to", OUTPUT_FILE)


if __name__ == "__main__":
    main()