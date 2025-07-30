import gzip
import json
import logging
import time
from collections import defaultdict
from datetime import datetime
from multiprocessing import get_context
from pathlib import Path
from typing import Dict, Optional, Tuple

import pandas as pd

# --- Logging setup ---
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("etl.large_log_etl_multiproc")


# --- Helpers ---
def parse_timestamp(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)


def floor_hour(dt: datetime) -> str:
    return dt.replace(minute=0, second=0, microsecond=0).isoformat()


def safe_json_loads(line: str) -> Optional[dict]:
    try:
        return json.loads(line)
    except Exception:
        return None


def process_lines(lines, status_threshold=500):
    agg: defaultdict[Tuple[str, str], Dict[str, int]] = defaultdict(
        lambda: {"total": 0, "errors": 0}
    )
    for line in lines:
        rec = safe_json_loads(line)
        if not rec:
            continue
        ts = rec.get("timestamp") or rec.get("ts")
        endpoint = rec.get("endpoint")
        status = rec.get("status_code") or rec.get("status")
        if not ts or not endpoint or status is None:
            continue
        try:
            status = int(status)
            hour = floor_hour(parse_timestamp(ts))
        except Exception as e:
            logger.debug(f"Error parsing record (ts={ts}, endpoint={endpoint}, status={status}): {e}")
            continue
        key = (hour, endpoint)
        agg[key]["total"] += 1
        if status >= status_threshold:
            agg[key]["errors"] += 1
    return dict(agg)


# --- Main function ---
def process_file_parallel(input_path: str, output_path: str, chunk_size=20000):
    start = time.time()
    logger.info("🚀 Starting multiprocessing ETL on: %s", input_path)

    chunks = []
    with gzip.open(input_path, mode="rt", encoding="utf-8", errors="ignore") as f:
        chunk = []
        for i, line in enumerate(f):
            chunk.append(line)
            if len(chunk) >= chunk_size:
                chunks.append(chunk)
                chunk = []
        if chunk:
            chunks.append(chunk)

    logger.info("🔢 Total chunks to process: %d", len(chunks))

    # Use spawn context to avoid Windows forking issues
    with get_context("spawn").Pool(processes=4) as pool:
        results = pool.map(process_lines, chunks)

    agg: defaultdict[Tuple[str, str], Dict[str, int]] = defaultdict(
        lambda: {"total": 0, "errors": 0}
    )
    for result in results:
        for key, val in result.items():
            agg[key]["total"] += val["total"]
            agg[key]["errors"] += val["errors"]

    rows = []
    for (hour, endpoint), counts in agg.items():
        total = counts["total"]
        errors = counts["errors"]
        error_pct = (errors / total * 100.0) if total > 0 else 0.0
        rows.append(
            {
                "hour": hour,
                "endpoint": endpoint,
                "total_requests": total,
                "error_requests": errors,
                "error_pct": round(error_pct, 2),
            }
        )

    df = pd.DataFrame(rows)
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, compression="snappy", index=False)

    logger.info("✅ Parquet written: %s | Rows: %d", output_path, len(df))
    logger.info("⏱️ Total Time: %.2f seconds", time.time() - start)


# --- Entry point ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Input .gz file")
    parser.add_argument("--output", required=True, help="Output .parquet file")
    parser.add_argument("--chunk-size", type=int, default=20000)
    args = parser.parse_args()

    process_file_parallel(args.input, args.output, args.chunk_size)
