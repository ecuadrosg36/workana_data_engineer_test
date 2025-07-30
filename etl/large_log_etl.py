import argparse
import gzip
import json
import logging
import sys
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

import pandas as pd


# ------------------------------------------------------
# Logging
# ------------------------------------------------------
def setup_logging(log_path: Optional[str] = None, level: int = logging.INFO) -> None:
    from logging import Handler, FileHandler, StreamHandler

    handlers: list[Handler] = [StreamHandler(sys.stdout)]
    if log_path:
        Path(log_path).parent.mkdir(parents=True, exist_ok=True)
        handlers.append(FileHandler(log_path, encoding="utf-8"))

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=handlers,
    )


logger = logging.getLogger("etl.large_log_etl")


# ------------------------------------------------------
# Utils
# ------------------------------------------------------
def parse_timestamp(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts.replace("Z", "+00:00")
    return datetime.fromisoformat(ts)


def floor_hour(dt: datetime) -> datetime:
    return dt.replace(minute=0, second=0, microsecond=0)


def safe_json_loads(line: str) -> Optional[dict]:
    try:
        return json.loads(line)
    except Exception as e:
        logger.debug("Línea inválida, no es JSON válido: %s", e)
        return None


# ------------------------------------------------------
# Core
# ------------------------------------------------------
def process_log_streaming(
    input_gz: Path,
    status_threshold: int = 500,
    log_every: int = 100_000,
) -> pd.DataFrame:
    logger.info("Iniciando procesamiento streaming: %s", input_gz)
    start = time.time()

    agg: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(lambda: {"total": 0, "errors": 0})

    total_lines = parsed_lines = error_lines = kept_lines = 0

    with gzip.open(input_gz, mode="rt", encoding="utf-8", errors="ignore") as f:
        for line in f:
            total_lines += 1
            rec = safe_json_loads(line)
            if rec is None:
                error_lines += 1
                continue

            parsed_lines += 1
            ts = rec.get("timestamp") or rec.get("ts")
            endpoint = rec.get("endpoint")
            status = rec.get("status_code") or rec.get("status")

            if ts is None or endpoint is None or status is None:
                error_lines += 1
                continue

            try:
                status = int(status)
                dt = parse_timestamp(ts)
                hour_dt = floor_hour(dt).isoformat()
            except Exception:
                error_lines += 1
                continue

            key = (hour_dt, endpoint)
            agg[key]["total"] += 1
            if status >= status_threshold:
                agg[key]["errors"] += 1
                kept_lines += 1

            if total_lines % log_every == 0:
                logger.info(
                    f"Progreso: {total_lines:,} líneas | parseadas: {parsed_lines:,} | "
                    f"inválidas: {error_lines:,} | errores >= {status_threshold}: {kept_lines:,}"
                )

    rows = []
    for (hour_dt, endpoint), counts in agg.items():
        total = counts["total"]
        errors = counts["errors"]
        error_pct = (errors / total * 100.0) if total > 0 else 0.0
        rows.append(
            {
                "hour": hour_dt,
                "endpoint": endpoint,
                "total_requests": total,
                "error_requests": errors,
                "error_pct": round(error_pct, 2),
            }
        )

    df = pd.DataFrame(rows)
    logger.info(
        f"Progreso: {total_lines:,} líneas | parseadas: {parsed_lines:,} | "
        f"inválidas: {error_lines:,} | errores >= {status_threshold}: {kept_lines:,}"
    )

    logger.info("Tiempo total: %.2f s", time.time() - start)
    return df


def write_parquet(df: pd.DataFrame, output_parquet: Path, compression: str = "snappy") -> None:
    output_parquet.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(str(output_parquet), compression=compression, index=False)  # <- cast Path to str
    logger.info(f"Parquet escrito en: {output_parquet} | filas: {len(df):,}")


# ------------------------------------------------------
# CLI
# ------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="ETL streaming para sample.log.gz (JSONL).")
    parser.add_argument("--input", required=True, help="Ruta al archivo .log.gz")
    parser.add_argument("--output", required=True, help="Ruta al parquet de salida")
    parser.add_argument(
        "--status-threshold",
        type=int,
        default=500,
        help="Status mínimo como error (default: 500)",
    )
    parser.add_argument("--log-file", default="logs/etl_run.log", help="Ruta del log")
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Nivel de logging: DEBUG, INFO, WARNING, ERROR",
    )
    args = parser.parse_args()

    setup_logging(args.log_file, getattr(logging, args.log_level.upper(), logging.INFO))

    input_gz = Path(args.input)
    if not input_gz.exists():
        logger.error("No existe el archivo: %s", input_gz)
        sys.exit(1)

    output_parquet = Path(args.output)

    df = process_log_streaming(
        input_gz=input_gz,
        status_threshold=args.status_threshold,
    )
    write_parquet(df, output_parquet)


if __name__ == "__main__":
    main()
