from pathlib import Path
import csv

from alpha.executors import csv_exec


def _write_csv(path: Path, rows):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def test_row_count(tmp_path):
    src = tmp_path / "input.csv"
    rows = [{"a": "1"}, {"a": "2"}]
    _write_csv(src, rows)
    res = csv_exec.row_count(str(src))
    assert res["ok"] and res["rows"] == 2


def test_filter_rows(tmp_path):
    src = tmp_path / "input.csv"
    rows = [{"a": "1"}, {"a": "2"}, {"a": "1"}]
    _write_csv(src, rows)
    res = csv_exec.filter_rows(str(src), "a", "1", "out.csv")
    out_path = Path(res["out"])
    assert res["ok"] and res["rows"] == 2
    assert out_path.exists()
    with open(out_path, newline="", encoding="utf-8") as fh:
        reader = list(csv.DictReader(fh))
        assert len(reader) == 2
        assert all(r["a"] == "1" for r in reader)
