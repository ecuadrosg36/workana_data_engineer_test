import io
import gzip
import json
from pathlib import Path

import pandas as pd

from etl.large_log_etl import process_log_streaming

def _make_gz(tmp_path: Path) -> Path:
    data = [
        {"timestamp": "2025-07-28T01:00:00Z", "endpoint": "/api/a", "status_code": 200},
        {"timestamp": "2025-07-28T01:15:00Z", "endpoint": "/api/a", "status_code": 503},
        {"timestamp": "2025-07-28T01:45:00Z", "endpoint": "/api/b", "status_code": 500},
        {"timestamp": "2025-07-28T02:05:00Z", "endpoint": "/api/a", "status_code": 404},
    ]
    gz_path = tmp_path / "sample.log.gz"
    with gzip.open(gz_path, "wt", encoding="utf-8") as f:
        for d in data:
            f.write(json.dumps(d) + "\n")
    return gz_path

def test_process_log_streaming(tmp_path):
    gz = _make_gz(tmp_path)
    df = process_log_streaming(gz, status_threshold=500, log_every=1_000_000)
    # esperamos 2 grupos por hora-endpoint
    # 2025-07-28T01:00:00 /api/a -> total 2, error 1
    # 2025-07-28T01:00:00 /api/b -> total 1, error 1
    # 2025-07-28T02:00:00 /api/a -> total 1, error 0 (404)
    assert isinstance(df, pd.DataFrame)
    assert set(df.columns) == {"hour", "endpoint", "total_requests", "error_requests", "error_pct"}
    assert df["error_requests"].sum() == 2
