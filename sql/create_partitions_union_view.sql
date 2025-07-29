DROP VIEW IF EXISTS all_transactions;

CREATE VIEW all_transactions AS
SELECT * FROM transactions_2025_01
UNION ALL
SELECT * FROM transactions_2025_02
UNION ALL
SELECT * FROM transactions_2025_03
UNION ALL
SELECT * FROM transactions_2025_04
UNION ALL
SELECT * FROM transactions_2025_05
UNION ALL
SELECT * FROM transactions_2025_06;
