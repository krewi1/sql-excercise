# Task 3: late deliveries, as of a past date

The model from task 2 has to be trained on history. The data scientist needs the same feature as it would have looked on **2026-01-15**, so that each training row only knows what was known on that day.

## Goal

For every customer, compute the share of their delivered orders that had arrived after the promised date, as of the end of 2026-01-15.

The `orders` table holds today's values. Nothing in it is dated 2026-01-15.

## Output

The same columns as task 2:

| Column | Meaning |
|---|---|
| customer_id | the customer |
| delivered_orders | orders delivered by 2026-01-15 |
| late_orders | of those, orders that arrived after the promised date |
| late_share | late_orders divided by delivered_orders |

## Where

Write the query in `queries/task3.sql`. Start from your task 2 query.

If something in the task or the data is ambiguous, decide, and say what you assumed.

## When you are done

Pick a customer whose numbers differ from task 2. Explain the difference order by order: what did 2026-01-15 know about each one?
