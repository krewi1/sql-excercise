"""Fetch the reference solution for a task and put it next to your own query.

    uv run reveal task1

Runs `git fetch origin task1` and checks out queries/task1_reference.sql from
that branch. Your queries/task1.sql is not touched. The interviewer publishes
the branch when build time is up; before that the command says so and stops.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("task", help="task1, task2 or task3")
    parser.add_argument("--remote", default="origin", help=argparse.SUPPRESS)
    arguments = parser.parse_args()
    task = arguments.task.removesuffix(".sql")
    reference_file = f"queries/{task}_reference.sql"

    fetch = subprocess.run(["git", "fetch", "--quiet", arguments.remote, task], cwd=ROOT, capture_output=True, text=True)
    if fetch.returncode != 0:
        sys.exit(f"the reference for {task} is not published yet; ask the interviewer")
    # `git show` to a file, not `git checkout`: a checkout would stage the file and it
    # would ride along with the candidate's next commit.
    show = subprocess.run(["git", "show", f"FETCH_HEAD:{reference_file}"], cwd=ROOT, check=True, capture_output=True, text=True)
    (ROOT / reference_file).write_text(show.stdout)
    print(f"reference written to {reference_file}; open it next to queries/{task}.sql")


if __name__ == "__main__":
    main()
