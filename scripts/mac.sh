#!/usr/bin/env bash
# Mac setup: install uv, then the exercise. Run from the repository root:
#
#     bash scripts/mac.sh

set -e

if ! command -v uv > /dev/null; then
    if command -v brew > /dev/null; then
        brew install uv
    else
        curl -LsSf https://astral.sh/uv/install.sh | sh
        export PATH="$HOME/.local/bin:$PATH"
    fi
fi

uv sync
uv run sql explore > /dev/null
echo "ready: uv run ide"
