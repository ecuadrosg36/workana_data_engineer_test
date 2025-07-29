import gzip
import json
import logging
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import polars as pl


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("etl.large_log_etl_polars")


def parse_timestamp(ts: str) -> Optional[str]:
    try:
        if ts.endswith("Z"):
            ts = ts.replace("Z", "+00:00")
        dt = datetime.fromisoformat(ts)
        return dt.replace(minute=0, second=0, microsecond=0).isoformat()
    except Exception:
        return None


def process_gz_to_polars(
    input_gz_path: str, output_parquet_path: str, status_threshold: int = 500
):
    logger.info("🚀 Iniciando procesamiento con polars: %s", input_gz_path)
    start = time.time()

    records = []
    with gzip.open(input_gz_path, mode="rt", encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                rec = json.loads(line)
                ts = rec.get("timestamp") or rec.get("ts")
                endpoint = rec.get("endpoint")
                status = rec.get("status_code") or rec.get("status")

                if not ts or not endpoint or status is None:
                    continue

                status = int(status)
                rounded_ts = parse_timestamp(ts)
                if not rounded_ts:
                    continue

                records.append(
                    {"hour": rounded_ts, "endpoint": endpoint, "status_code": status}
                )
            except json.JSONDecodeError:
                continue

    df = pl.DataFrame(records)
    logger.info("🔍 Registros procesados: %d", df.shape[0])

    grouped = (
        df.group_by(["hour", "endpoint"])
        .agg([
            pl.len().alias("total_requests"),
            (pl.col("status_code") >= status_threshold)
            .cast(pl.Int64)
            .sum()
            .alias("error_requests"),
        ])
        .with_columns([
            (
                (pl.col("error_requests") / pl.col("total_requests") * 100)
                .round(2)
                .alias("error_pct")
            ),
        ])
    )

    Path(output_parquet_path).parent.mkdir(parents=True, exist_ok=True)
    grouped.write_parquet(output_parquet_path, compression="snappy")

    logger.info("✅ Parquet exportado: %s", output_parquet_path)
    logger.info("⏱️ Tiempo total: %.2f s", time.time() - start)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="Ruta al archivo .gz")
    parser.add_argument("--output", required=True, help="Ruta al parquet de salida")
    parser.add_argument("--status-threshold", type=int, default=500)
    args = parser.parse_args()

    process_gz_to_polars(args.input, args.output, args.status_threshold)
