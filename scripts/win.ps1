# Windows setup: install uv, then the exercise. Run from the repository root:
#
#     powershell -ExecutionPolicy Bypass -File scripts\win.ps1

$ErrorActionPreference = "Stop"

if (-not (Get-Command uv -ErrorAction SilentlyContinue)) {
    powershell -ExecutionPolicy Bypass -Command "irm https://astral.sh/uv/install.ps1 | iex"
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
}

uv sync
uv run sql explore | Out-Null
Write-Host "ready: uv run harlequin"
