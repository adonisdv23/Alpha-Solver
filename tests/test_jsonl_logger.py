import gzip
import json
from pathlib import Path

from alpha.core.jsonl_logger import JSONLLogger


def test_jsonl_logger_rotation(tmp_path):
    log_path = tmp_path / "events.jsonl"
    logger = JSONLLogger(log_path, max_bytes=50)
    for i in range(20):
        logger.log({"i": i})
    logger.close()
    assert log_path.exists()
    rotated = log_path.with_suffix(log_path.suffix + ".1.gz")
    assert rotated.exists()
    with gzip.open(rotated, "rt", encoding="utf-8") as f:
        lines = [json.loads(line) for line in f]
    assert len(lines) > 0
