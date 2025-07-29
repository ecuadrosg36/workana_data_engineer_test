-- Elimina transacciones del último mes 
DELETE FROM transactions
WHERE DATE(ts) >= DATE('now', 'start of month');
