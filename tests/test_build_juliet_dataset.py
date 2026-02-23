# tests/test_build_juliet_dataset.py
from pathlib import Path

from scripts.build_juliet_dataset import collect_samples, detect_cwe


def test_detect_cwe_from_folder_name():
    assert detect_cwe("CWE78_Command_Injection") == "CWE78"


def test_collect_samples_reads_bad_files(tmp_path: Path):
    folder = tmp_path / "CWE78_Command_Injection"
    folder.mkdir(parents=True)
    (folder / "sample_bad.c").write_text("int main(){return 0;}", encoding="utf-8")
    (folder / "sample_good.c").write_text("int main(){return 1;}", encoding="utf-8")
    rows = collect_samples(tmp_path, ("_bad.c",))
    assert len(rows) == 1
    assert rows[0]["file"] == "sample_bad.c"
    assert rows[0]["cwe"] == "CWE78"


def test_collect_samples_skips_io_support_files(tmp_path: Path):
    folder = tmp_path / "CWE89_SQL_Injection"
    folder.mkdir(parents=True)
    (folder / "helper_io.c").write_text("int x;", encoding="utf-8")
    rows = collect_samples(tmp_path, ("_io.c", ".c"))
    assert rows == []
