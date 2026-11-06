#!/usr/bin/env bash
# Linux setup: install uv, then the exercise. Run from the repository root:
#
#     bash scripts/linux.sh

set -e

if ! command -v uv > /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    export PATH="$HOME/.local/bin:$PATH"
fi

uv sync
uv run sql explore > /dev/null
echo "ready: uv run harlequin"
