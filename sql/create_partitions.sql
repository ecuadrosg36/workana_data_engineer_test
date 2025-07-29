-- Ajustado a los meses reales que se verificaron en la tabla transactions

DROP TABLE IF EXISTS transactions_2025_01;
CREATE TABLE transactions_2025_01 AS
SELECT *
FROM transactions
WHERE strftime('%Y_%m', ts) = '2025_01';

DROP TABLE IF EXISTS transactions_2025_02;
CREATE TABLE transactions_2025_02 AS
SELECT *
FROM transactions
WHERE strftime('%Y_%m', ts) = '2025_02';

DROP TABLE IF EXISTS transactions_2025_03;
CREATE TABLE transactions_2025_03 AS
SELECT *
FROM transactions
WHERE strftime('%Y_%m', ts) = '2025_03';
DROP TABLE IF EXISTS transactions_2025_04;
CREATE TABLE transactions_2025_04 AS
SELECT *
FROM transactions
WHERE strftime('%Y_%m', ts) = '2025_04';

DROP TABLE IF EXISTS transactions_2025_05;
CREATE TABLE transactions_2025_05 AS
SELECT *
FROM transactions
WHERE strftime('%Y_%m', ts) = '2025_05';

DROP TABLE IF EXISTS transactions_2025_06;
CREATE TABLE transactions_2025_06 AS
SELECT *
FROM transactions
WHERE strftime('%Y_%m', ts) = '2025_06';

