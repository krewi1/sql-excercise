"""Run SQL against the interview dataset, backed by DuckDB.

    uv run sql queries/task1.sql           # run every statement in the file, print each result
    uv run sql --watch queries/task1.sql   # same, re-run on every save
    uv run sql a.sql b.sql                 # several files, in order, same connection
    uv run sql                             # interactive shell, statements end with ';'

Shell commands:  \\tables   \\d <table>   \\quit
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import duckdb

DATA_DIRECTORY = Path(__file__).parent / "data"
TABLES = ["customers", "promotions", "orders", "order_items"]


def connect() -> duckdb.DuckDBPyConnection:
    """In-memory DuckDB with the four CSVs loaded as tables, with their declared types."""
    connection = duckdb.connect(database=":memory:")
    load_tables_from_csv(connection)
    return connection


def load_tables_from_csv(connection: duckdb.DuckDBPyConnection) -> None:
    connection.execute("SET TimeZone = 'UTC'")
    connection.execute(f"""
        CREATE TABLE customers AS
        SELECT customer_id::BIGINT AS customer_id, segment::VARCHAR AS segment
        FROM read_csv('{DATA_DIRECTORY / "customers.csv"}', header = true)
    """)
    connection.execute(f"""
        CREATE TABLE promotions AS
        SELECT promo_id::BIGINT AS promo_id, promo_code::VARCHAR AS promo_code, is_active::BOOLEAN AS is_active
        FROM read_csv('{DATA_DIRECTORY / "promotions.csv"}', header = true)
    """)
    connection.execute(f"""
        CREATE TABLE orders AS
        SELECT
            order_id::BIGINT AS order_id,
            customer_id::BIGINT AS customer_id,
            promo_id::BIGINT AS promo_id,
            order_total::DECIMAL(12, 2) AS order_total,
            created_at::TIMESTAMP AS created_at,
            promised_date::DATE AS promised_date,
            delivered_at::TIMESTAMP AS delivered_at,
            status::VARCHAR AS status
        FROM read_csv('{DATA_DIRECTORY / "orders.csv"}', header = true, nullstr = '')
    """)
    connection.execute(f"""
        CREATE TABLE order_items AS
        SELECT order_item_id::BIGINT AS order_item_id, order_id::BIGINT AS order_id, sku::VARCHAR AS sku, quantity::BIGINT AS quantity
        FROM read_csv('{DATA_DIRECTORY / "order_items.csv"}', header = true)
    """)


def run_statement(connection: duckdb.DuckDBPyConnection, statement: str) -> None:
    try:
        relation = connection.sql(statement)
        if relation is None:
            print("ok")
        else:
            relation.show(max_rows=200, max_width=200)
    except duckdb.Error as error:
        print(f"error: {error}")


def split_statements(sql_text: str) -> list[str]:
    """Split on ';' outside of string literals and comments. Comments are kept with their statement."""
    statements: list[str] = []
    current: list[str] = []
    in_string = False
    in_line_comment = False
    for index, character in enumerate(sql_text):
        if in_line_comment:
            current.append(character)
            if character == "\n":
                in_line_comment = False
        elif in_string:
            current.append(character)
            if character == "'":
                in_string = False
        elif character == "'":
            in_string = True
            current.append(character)
        elif character == "-" and sql_text[index + 1 : index + 2] == "-":
            in_line_comment = True
            current.append(character)
        elif character == ";":
            statements.append("".join(current))
            current = []
        else:
            current.append(character)
    statements.append("".join(current))
    return [statement.strip() for statement in statements if statement.strip() and not is_only_comments(statement)]


def is_only_comments(statement: str) -> bool:
    return all(line.strip() == "" or line.strip().startswith("--") for line in statement.splitlines())


def run_file(connection: duckdb.DuckDBPyConnection, path: Path) -> None:
    print(f"== {path}")
    for statement in split_statements(path.read_text()):
        print()
        print(statement)
        run_statement(connection, statement)


def run_shell_command(connection: duckdb.DuckDBPyConnection, command: str) -> bool:
    """Returns False when the shell should exit."""
    name, _, argument = command.strip().partition(" ")
    if name in ("\\quit", "\\q"):
        return False
    if name == "\\tables":
        for table in TABLES:
            row_count = connection.sql(f"SELECT COUNT(*) FROM {table}").fetchall()[0][0]
            print(f"{table:12} {row_count:>6} rows")
    elif name == "\\d" and argument in TABLES:
        connection.sql(f"DESCRIBE {argument}").show()
    else:
        print("commands: \\tables   \\d <table>   \\quit")
    return True


def repl(connection: duckdb.DuckDBPyConnection) -> None:
    print("Interview dataset loaded. Statements end with ';'. \\tables lists tables, \\quit exits.")
    buffer: list[str] = []
    while True:
        try:
            line = input("sql> " if not buffer else "...> ")
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not buffer and line.startswith("\\"):
            if not run_shell_command(connection, line):
                break
            continue
        buffer.append(line)
        if line.rstrip().endswith(";"):
            run_statement(connection, "\n".join(buffer))
            buffer = []


def ui() -> None:
    """Open the DuckDB browser UI on data/exercise.duckdb and keep it alive until Ctrl+C.

    The UI has a notebook editor with table and column completion. It runs on
    localhost; the front-end assets come from duckdb.org, the data never leaves
    the machine. Tables created in the UI land in exercise.duckdb, not in the
    CSVs, so `uv run sql` does not see them.
    """
    import time

    argparse.ArgumentParser(description=ui.__doc__, formatter_class=argparse.RawDescriptionHelpFormatter).parse_args()
    database_path = DATA_DIRECTORY / "exercise.duckdb"
    if not database_path.exists():
        print(f"{database_path} is missing; run `uv run generate-dataset` first")
        sys.exit(1)
    connection = duckdb.connect(str(database_path))
    connection.execute("INSTALL ui")
    connection.execute("LOAD ui")
    connection.execute("CALL start_ui()")
    print("DuckDB UI is at http://localhost:4213 (the browser should have opened). Ctrl+C to stop.")
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        print()
    finally:
        connection.close()


def run_files(paths: list[Path]) -> None:
    """One fresh connection per run, so a CREATE TABLE in a file does not fail on the next run."""
    connection = connect()
    for path in paths:
        run_file(connection, path)
    connection.close()
    sys.stdout.flush()


def watch_files(paths: list[Path]) -> None:
    """Re-run the files whenever one of them is saved. Ctrl+C stops."""
    import time

    def modification_times() -> list[float]:
        return [path.stat().st_mtime if path.exists() else 0.0 for path in paths]

    last_seen = modification_times()
    print("\033[2J\033[H", end="")
    run_files(paths)
    print(f"\nwatching {', '.join(str(path) for path in paths)}; save a file to re-run, Ctrl+C to stop")
    try:
        while True:
            time.sleep(0.5)
            current = modification_times()
            if current != last_seen:
                last_seen = current
                print("\033[2J\033[H", end="")
                run_files(paths)
                print(f"\nwatching; last run {time.strftime('%H:%M:%S')}")
    except KeyboardInterrupt:
        print()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="*", type=Path, help="SQL files to run; none opens the interactive shell")
    parser.add_argument("--watch", action="store_true", help="re-run the files every time one of them is saved")
    arguments = parser.parse_args()

    if arguments.watch and not arguments.files:
        parser.error("--watch needs at least one file")
    if arguments.watch:
        watch_files(arguments.files)
    elif arguments.files:
        run_files(arguments.files)
    else:
        repl(connect())
    sys.exit(0)


if __name__ == "__main__":
    main()
