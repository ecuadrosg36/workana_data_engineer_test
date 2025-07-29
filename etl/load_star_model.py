import sqlite3
from datetime import datetime

import pandas as pd

# Carga CSV
df = pd.read_csv("data/sample_transactions.csv")

# Prepara dimensiones
df["date_id"] = df["ts"].apply(lambda x: x.split("T")[0])

dim_user = df[["user_id"]].drop_duplicates().copy()
dim_user["scd_version"] = 1
dim_user["scd_start_ts"] = datetime.now().isoformat()
dim_user["scd_end_ts"] = None

dim_status = pd.DataFrame(
    {"status": df["status"].unique(), "description": df["status"].unique()}
)

dim_date = df[["date_id"]].drop_duplicates().copy()
dim_date["year"] = dim_date["date_id"].apply(lambda x: int(x[:4]))
dim_date["month"] = dim_date["date_id"].apply(lambda x: int(x[5:7]))
dim_date["day"] = dim_date["date_id"].apply(lambda x: int(x[8:10]))

# Conecta DB y crea tablas
con = sqlite3.connect("data/transactions.db")
with open("sql/model_tables_star.sql") as f:
    con.executescript(f.read())

# Borra datos previos, NO la estructura
con.execute("DELETE FROM dim_user")
con.execute("DELETE FROM dim_status")
con.execute("DELETE FROM dim_date")
con.execute("DELETE FROM fact_transactions")
con.commit()

# Inserta los datos nuevos
dim_user.to_sql("dim_user", con, if_exists="append", index=False)
dim_status.to_sql("dim_status", con, if_exists="append", index=False)
dim_date.to_sql("dim_date", con, if_exists="append", index=False)

# Carga hechos
fact = df.copy()
fact["date_id"] = fact["ts"].apply(lambda x: x.split("T")[0])
fact = fact[["order_id", "user_id", "amount", "ts", "status", "date_id"]]
fact.to_sql("fact_transactions", con, if_exists="append", index=False)

con.close()
