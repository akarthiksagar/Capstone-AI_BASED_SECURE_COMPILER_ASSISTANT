# tests/test_llm_translation_pipeline.py
from scripts.generate_securelang_llm_dataset import normalize_cwe, stratified_select, build_prompt
from scripts.train_securelang_translator import is_codebert_model


def test_normalize_cwe_formats_variants():
    assert normalize_cwe("CWE-78") == "CWE78"
    assert normalize_cwe("CWE_89") == "CWE89"
    assert normalize_cwe("94") == "CWE94"


def test_stratified_select_limits_per_cwe():
    rows = [
        {"cwe": "CWE78", "id": 1},
        {"cwe": "CWE78", "id": 2},
        {"cwe": "CWE78", "id": 3},
        {"cwe": "CWE89", "id": 4},
        {"cwe": "CWE89", "id": 5},
    ]
    selected = stratified_select(rows, max_per_cwe=2, seed=7)
    cwe78 = [r for r in selected if normalize_cwe(r["cwe"]) == "CWE78"]
    cwe89 = [r for r in selected if normalize_cwe(r["cwe"]) == "CWE89"]
    assert len(cwe78) == 2
    assert len(cwe89) == 2


def test_build_prompt_contains_cwe_and_code():
    prompt = build_prompt("int main(){return 0;}", "CWE78")
    assert "CWE: CWE78" in prompt
    assert "int main(){return 0;}" in prompt


def test_codebert_detection_for_hf_training_mode():
    assert is_codebert_model("microsoft/codebert-base")
    assert not is_codebert_model("google/flan-t5-base")
