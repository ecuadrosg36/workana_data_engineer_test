-- Tablas Dimensionales
CREATE TABLE IF NOT EXISTS dim_user (
  user_id INTEGER PRIMARY KEY,
  -- Agrega aquí campos relevantes si tienes
  scd_version INTEGER DEFAULT 1,
  scd_start_ts TEXT,
  scd_end_ts TEXT
);

CREATE TABLE IF NOT EXISTS dim_status (
  status TEXT PRIMARY KEY,
  description TEXT
);

CREATE TABLE IF NOT EXISTS dim_date (
  date_id TEXT PRIMARY KEY,
  year INTEGER,
  month INTEGER,
  day INTEGER
);

-- Tabla de hechos
CREATE TABLE IF NOT EXISTS fact_transactions (
  order_id INTEGER PRIMARY KEY,
  user_id INTEGER,
  amount REAL,
  ts TEXT,
  status TEXT,
  date_id TEXT,
  FOREIGN KEY(user_id) REFERENCES dim_user(user_id),
  FOREIGN KEY(status) REFERENCES dim_status(status),
  FOREIGN KEY(date_id) REFERENCES dim_date(date_id)
);
