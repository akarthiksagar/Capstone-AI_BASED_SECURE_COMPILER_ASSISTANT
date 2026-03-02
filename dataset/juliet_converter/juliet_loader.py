import os


def collect_c_files(root_dir):
    c_files = []

    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith(".c"):
                c_files.append(os.path.join(root, file))

    return c_files


def is_vulnerable_file(filepath):
    # Juliet naming convention
    # e.g. CWE121_Stack_Based_Buffer_Overflow__char_type_overrun_memcpy_01.c
    # Good functions contain "good", bad contain "bad"

    return "_bad" in filepath.lower()