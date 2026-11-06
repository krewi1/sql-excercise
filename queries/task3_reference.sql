-- Reference solution, Task 3, as of 2026-01-15. Compare it with yours: the differences are the conversation.
WITH clean_orders AS (
    SELECT DISTINCT order_id, customer_id, created_at, promised_date, delivered_at, status
    FROM orders
    WHERE status <> 'cancelled'
)
,
orders_as_of AS (
    SELECT
        customer_id,
        promised_date,
        CASE WHEN delivered_at < TIMESTAMP '2026-01-15' + INTERVAL 1 DAY THEN delivered_at END AS delivered_at
    FROM clean_orders
    WHERE created_at < TIMESTAMP '2026-01-15' + INTERVAL 1 DAY
)
SELECT
    customer_id,
    COUNT(*) AS delivered_orders,
    COUNT(*) FILTER (WHERE delivered_at::DATE > promised_date) AS late_orders,
    ROUND(COUNT(*) FILTER (WHERE delivered_at::DATE > promised_date) * 1.0 / COUNT(*), 3) AS late_share
FROM orders_as_of
WHERE delivered_at IS NOT NULL AND promised_date IS NOT NULL
GROUP BY customer_id
ORDER BY customer_id
