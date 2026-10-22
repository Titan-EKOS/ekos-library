# One-time setup on EKOS. Run from any folder:
#   powershell -ExecutionPolicy Bypass -File D:\EKOS\Library\09_Server\setup.ps1
$ErrorActionPreference = "Stop"
$Server = $PSScriptRoot
$Root = Split-Path $Server -Parent
if (-not (Test-Path "$Server\.venv\Scripts\python.exe")) {
    py -3.12 -m venv "$Server\.venv"
}
& "$Server\.venv\Scripts\python.exe" -m pip install -q --upgrade pip
& "$Server\.venv\Scripts\python.exe" -m pip install -q -r "$Server\requirements.txt"
git -C $Root config core.hooksPath .githooks
git -C $Root config core.autocrlf false
Write-Host "Setup done. Test with: $Server\.venv\Scripts\python.exe -m pytest -q $Server\tests"
