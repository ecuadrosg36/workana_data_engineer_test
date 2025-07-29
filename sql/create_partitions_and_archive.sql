-- Add the logical partition column (if not exists)
--ALTER TABLE fact_transactions ADD COLUMN period INTEGER;

-- Populate it for all rows
UPDATE fact_transactions
SET period = CAST(strftime('%Y', date_id) AS INTEGER) * 100 + CAST(strftime('%m', date_id) AS INTEGER);

-- Example: Archive data before May 2025
CREATE TABLE IF NOT EXISTS archive_transactions AS
SELECT * FROM fact_transactions WHERE period < 202505;

DELETE FROM fact_transactions WHERE period < 202505;


CREATE INDEX IF NOT EXISTS idx_fact_transactions_period ON fact_transactions(period);

CREATE INDEX IF NOT EXISTS idx_archive_transactions_period ON archive_transactions(period);

