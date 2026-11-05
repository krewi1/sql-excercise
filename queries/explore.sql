-- Look around before writing anything. Today is 2026-11-01.
SELECT * FROM customers LIMIT 5;
SELECT * FROM orders ORDER BY created_at DESC LIMIT 10;
SELECT status, COUNT(*) AS rows FROM orders GROUP BY status;
