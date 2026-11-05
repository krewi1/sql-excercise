# Task 1: recent order activity per customer

A data scientist is building a model that scores every customer once a day. The first two features they need describe how recently and how often a customer orders.

## Goal

For every customer, compute:

- how many orders they placed in the last 90 days
- how many days have passed since their last order

Today is **2026-11-01**.

## Output

One row per customer:

| Column | Meaning |
|---|---|
| customer_id | the customer |
| orders_last_90_days | orders placed in the 90 days up to today |
| days_since_last_order | days between the last order and today |

## Where

Write the query in `queries/task1.sql`. The schema is in `queries/schema.md`.

If something in the task or the data is ambiguous, decide, and say what you assumed.

## When you are done

How would you convince yourself the numbers are right?
