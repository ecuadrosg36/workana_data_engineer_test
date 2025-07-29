DROP TABLE IF EXISTS fact_transactions;
DROP TABLE IF EXISTS dim_user;
DROP TABLE IF EXISTS dim_status;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_user (
    user_id INTEGER,
    scd_version INTEGER,
    scd_start_ts TEXT,
    scd_end_ts TEXT,
    PRIMARY KEY (user_id, scd_version)
);

CREATE TABLE dim_status (
    status TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE dim_date (
    date_id TEXT PRIMARY KEY,
    year INTEGER,
    month INTEGER,
    day INTEGER
);

CREATE TABLE fact_transactions (
    order_id INTEGER PRIMARY KEY,
    user_id INTEGER,
    amount REAL,
    ts TEXT,
    status TEXT,
    date_id TEXT,
    period INTEGER,
    FOREIGN KEY (user_id) REFERENCES dim_user(user_id),
    FOREIGN KEY (status) REFERENCES dim_status(status),
    FOREIGN KEY (date_id) REFERENCES dim_date(date_id)
);
