# SQL exercise

A small orders dataset in DuckDB and a terminal SQL IDE to query it. Nothing to install beyond [uv](https://docs.astral.sh/uv/).

## Setup

One short script per platform installs uv if needed, then DuckDB and Harlequin. Run it from the repository root:

```bash
bash scripts/mac.sh
bash scripts/linux.sh
powershell -ExecutionPolicy Bypass -File scripts\win.ps1
```

No uv possible on your machine? Any Python 3.9 or newer works too:

```bash
python3 -m venv .venv && .venv/bin/pip install duckdb harlequin
.venv/bin/harlequin                      # instead of uv run ide
.venv/bin/python sql_shell.py task1      # instead of uv run sql task1
.venv/bin/python reveal.py task1         # instead of uv run reveal task1
```

Then:

```bash
uv run ide # opens the database in Harlequin
```

Harlequin: schema tree on the left, editor in the middle, results below.

| Key | Action |
|---|---|
| Ctrl+Enter | run the query, or the selected text |
| Ctrl+O | open a file, for example `queries/task1.sql` |
| Ctrl+S | save the file |
| F1 | all key bindings |
| Ctrl+Q | quit |

Prefer your own editor? Write SQL in a file and run it from the terminal:

```bash
uv run sql task1            # runs every statement in queries/task1.sql, prints each result
uv run sql --watch task1    # same, re-runs on every save
uv run sql                  # plain interactive shell
```

## Data

Four tables, described in [`queries/schema.md`](queries/schema.md): `customers`, `orders`, `order_items`, `promotions`. Timestamps are UTC. For the tasks, today is **2026-11-01**.

The dialect is DuckDB, which is PostgreSQL-flavoured and accepts most BigQuery functions (`DATE_DIFF`, `COUNTIF`, `DATE_SUB`). If a function you know is missing, say so and we will find the equivalent.

## AI assistants

You may use one. It follows the rules in [`AGENTS.md`](AGENTS.md): it types the SQL you describe and adds nothing of its own. Claude Code and Codex pick the file up automatically. If you use a chat window instead, paste the file in first.

## Tasks

Start with `queries/explore.sql` to look around. Then:

- [Task 1: recent order activity per customer](task1.md), written in `queries/task1.sql`
- [Task 2: late deliveries per customer](task2.md), written in `queries/task2.sql`
- [Task 3: late deliveries, as of a past date](task3.md), written in `queries/task3.sql`

When the interviewer says so, fetch the reference solution next to yours:

```bash
uv run reveal task1
```

It writes `queries/task1_reference.sql` and leaves your own file untouched. Open both in Harlequin and compare.
