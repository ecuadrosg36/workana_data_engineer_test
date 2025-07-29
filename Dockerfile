# Dockerfile
FROM python:3.12-slim

# Crear directorios
WORKDIR /app

# Copiar archivos necesarios
COPY requirements.txt ./
COPY etl ./etl
COPY data ./data
COPY output ./output
COPY logs ./logs

# Instalar dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Comando por defecto (puedes sobreescribirlo con CMD)
CMD ["python", "etl/large_log_etl.py", "--input", "data/sample.log.gz", "--output", "output/errors_summary.parquet"]
