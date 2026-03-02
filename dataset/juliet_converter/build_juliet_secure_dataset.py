import json
import os
from juliet_loader import collect_c_files, is_vulnerable_file
from c_ast_extractor import parse_c_file, FunctionExtractor
from c_to_securelang import CToSecureLangConverter
from juliet_text_extractor import collect_c_files, clean_code, extract_functions

def is_vulnerable_function(name):
    return "bad" in name

def collect_c_files(root):
    c_files=[]

    for root_dir, _, files in os.walk(root):
        for file in files[:5]:
            if file.endswith(".c"):
                c_files.append(os.path.join(root_dir, file))

    return c_files

def build_dataset(juliet_root, output_file):

    c_files = collect_c_files(juliet_root)

    print("Total C files found:", len(c_files))

    dataset = []

    for file in c_files:

            ast = parse_c_file(file)
            if ast is None:
                continue

            collector = FunctionExtractor()
            collector.visit(ast)

            for func in collector.functions:

                func_name = func.decl.name
                label = 1 if is_vulnerable_function(func_name) else 0

                converter = CToSecureLangConverter()
                secure_code = converter.convert(func)

                if secure_code.strip() == "":
                    continue

                dataset.append({
                    "code": secure_code,
                    "label": label
                })

    with open(output_file, "w") as f:
        json.dump(dataset, f, indent=2)

    print("Generated samples:", len(dataset))

# ===============================================
# ENTRY POINT (THIS IS THE PATH YOU ASKED ABOUT)
# ===============================================

if __name__ == "__main__":

    # 🔥 CHANGE THIS TO YOUR JULIET ROOT DIRECTORY
    juliet_root_path = "/home/karthik/Documents/compiler_design/Capstone-AI_BASED_SECURE_COMPILER_ASSISTANT/dataset/juliet_raw/C/testcases"

    output_path = "/home/karthik/Documents/compiler_design/Capstone-AI_BASED_SECURE_COMPILER_ASSISTANT/dataset/juliet_securelang.json"

    build_dataset(juliet_root_path, output_path)

