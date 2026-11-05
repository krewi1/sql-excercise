# Schema

Four tables, loaded from CSV into DuckDB. Timestamps are UTC. Today is 2026-11-01.

## customers

One row per customer. Primary key: customer_id.

| Column | Type | Nullable | Description |
|---|---|---|---|
| customer_id | BIGINT | No | Unique ID of the customer. |
| segment | VARCHAR | No | Customer segment: enterprise, smb, consumer. Holds the current value only. |

## orders

One row per order. Primary key: order_id.

| Column | Type | Nullable | Description |
|---|---|---|---|
| order_id | BIGINT | No | Unique ID of the order. |
| customer_id | BIGINT | No | Customer who placed the order. |
| promo_id | BIGINT | Yes | Promotion used on the order. NULL when no promotion was used. |
| order_total | DECIMAL(12,2) | No | Total amount of the whole order, in USD. |
| created_at | TIMESTAMP | No | When the order was placed, in UTC. |
| promised_date | DATE | Yes | Delivery date promised to the customer. |
| delivered_at | TIMESTAMP | Yes | When the order was delivered, in UTC. NULL until delivered. |
| status | VARCHAR | No | placed, cancelled or delivered. |

## order_items

One row per item in an order. Primary key: order_item_id. An order has one or more items.

| Column | Type | Nullable | Description |
|---|---|---|---|
| order_item_id | BIGINT | No | Unique ID of the item row. |
| order_id | BIGINT | No | Order the item belongs to. |
| sku | VARCHAR | No | Product SKU. |
| quantity | BIGINT | No | Number of units of this SKU in the order. |

## promotions

One row per promotion. Primary key: promo_id.

| Column | Type | Nullable | Description |
|---|---|---|---|
| promo_id | BIGINT | No | Unique ID of the promotion. |
| promo_code | VARCHAR | No | Code the customer enters at checkout. |
| is_active | BOOLEAN | No | TRUE if the promotion is active today. |
