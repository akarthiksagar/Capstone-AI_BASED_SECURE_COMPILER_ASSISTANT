# scripts/build_juliet_dataset.py
import argparse
import json
import os
from pathlib import Path


def detect_cwe(folder: str) -> str:
    parts = folder.split("_")
    return parts[0] if parts else "UNKNOWN"


def collect_samples(juliet_path: Path, suffixes: tuple[str, ...]) -> list[dict]:
    dataset = []
    for root, _, files in os.walk(juliet_path):
        for file in files:
            if not file.endswith(suffixes):
                continue
            if "io.c" in file.lower():
                continue
            full_path = Path(root) / file
            try:
                code = full_path.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            folder_name = Path(root).name
            cwe = detect_cwe(folder_name)
            dataset.append(
                {
                    "file": file,
                    "cwe": cwe,
                    "vulnerable": True,
                    "code": code,
                }
            )
    return dataset


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--juliet-path", default="datasets/raw/juliet/C/testcases")
    parser.add_argument("--output", default="datasets/juliet_dataset.json")
    parser.add_argument("--suffixes", nargs="+", default=["_bad.c"])
    return parser.parse_args()


def run(args: argparse.Namespace) -> None:
    juliet_path = Path(args.juliet_path)
    output = Path(args.output)
    if not juliet_path.exists():
        raise FileNotFoundError(f"Juliet path not found: {juliet_path}")

    dataset = collect_samples(juliet_path, tuple(args.suffixes))

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(dataset, indent=2), encoding="utf-8")

    print("DONE")
    print(f"Juliet path: {juliet_path}")
    print(f"Suffixes: {', '.join(args.suffixes)}")
    print(f"Total vulnerable samples: {len(dataset)}")
    print(f"Saved to: {output}")


if __name__ == "__main__":
    run(parse_args())
