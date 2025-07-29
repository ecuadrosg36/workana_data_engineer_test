import sqlite3
from datetime import datetime

def update_user_scd(user_id, new_data):
    con = sqlite3.connect('data/transactions.db')
    cur = con.cursor()
    now = datetime.now().isoformat()
    # Cierra versión anterior (pone fecha y is_current = 0)
    cur.execute("""
        UPDATE dim_user SET scd_end_ts = ?, is_current = 0
        WHERE user_id = ? AND is_current = 1
    """, (now, user_id))
    # Inserta nueva versión (is_current = 1)
    cur.execute("""
        INSERT INTO dim_user (user_id, scd_version, scd_start_ts, scd_end_ts, is_current)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, new_data['scd_version'], now, None, 1))
    con.commit()
    con.close()
# Ejemplo de uso:
update_user_scd(950, {'scd_version': 3})
