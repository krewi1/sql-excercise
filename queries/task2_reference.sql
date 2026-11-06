-- Reference solution, Task 2. Compare it with yours: the differences are the conversation.
WITH clean_orders AS (
    SELECT DISTINCT order_id, customer_id, created_at, promised_date, delivered_at, status
    FROM orders
    WHERE status <> 'cancelled'
)

SELECT
    customer_id,
    COUNT(*) AS delivered_orders,
    COUNT(*) FILTER (WHERE delivered_at::DATE > promised_date) AS late_orders,
    ROUND(COUNT(*) FILTER (WHERE delivered_at::DATE > promised_date) * 1.0 / COUNT(*), 3) AS late_share
FROM clean_orders
WHERE status = 'delivered' AND promised_date IS NOT NULL
GROUP BY customer_id
ORDER BY customer_id
