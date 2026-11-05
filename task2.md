# Task 2: late deliveries per customer

The same model needs a feature describing delivery experience: how often a customer's orders arrive later than promised.

## Goal

For every customer, compute the share of their delivered orders that arrived after the promised date.

Today is **2026-11-01**.

## Output

One row per customer:

| Column | Meaning |
|---|---|
| customer_id | the customer |
| delivered_orders | orders that have been delivered |
| late_orders | delivered orders that arrived after the promised date |
| late_share | late_orders divided by delivered_orders |

## Where

Write the query in `queries/task2.sql`. The schema is in `queries/schema.md`.

If something in the task or the data is ambiguous, decide, and say what you assumed.

## When you are done

How would you convince yourself the numbers are right?
