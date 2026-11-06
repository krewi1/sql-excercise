-- Reference solution, Task 1. Compare it with yours: the differences are the conversation.
WITH clean_orders AS (
    SELECT DISTINCT order_id, customer_id, created_at, promised_date, delivered_at, status
    FROM orders
    WHERE status <> 'cancelled'
)

SELECT
    c.customer_id,
    COUNT(o.order_id) FILTER (WHERE o.created_at >= TIMESTAMP '2026-11-01' - INTERVAL 90 DAY) AS orders_last_90_days,
    DATE '2026-11-01' - MAX(o.created_at)::DATE AS days_since_last_order
FROM customers c
LEFT JOIN clean_orders o ON o.customer_id = c.customer_id
GROUP BY c.customer_id
ORDER BY c.customer_id
