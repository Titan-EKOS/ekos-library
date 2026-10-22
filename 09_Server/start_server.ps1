# Start the EKOS Library MCP server by hand (MCP clients normally start it themselves over stdio).
#   .\start_server.ps1          stdio
#   .\start_server.ps1 -Http    streamable HTTP on http://127.0.0.1:8765/mcp (local only)
param([switch]$Http, [int]$Port = 8765)
$Server = $PSScriptRoot
$Py = "$Server\.venv\Scripts\python.exe"
if (-not (Test-Path $Py)) { Write-Error "Run setup.ps1 first."; exit 1 }
if ($Http) { & $Py "$Server\run_server.py" --http --port $Port }
else       { & $Py "$Server\run_server.py" }
