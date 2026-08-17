[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$engineRoot = Join-Path $projectRoot "codexsaver-engine"
$engineCli = Join-Path $engineRoot "cli.py"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python Launcher (py) was not found. Install Python 3.10 or newer first."
}
if (-not (Test-Path -LiteralPath $engineCli)) {
    throw "CodexSaver engine was not found: $engineCli"
}

Write-Host "[1/3] Installing the CodexSaver Python package..."
& py -3 -m pip install -e $engineRoot
if ($LASTEXITCODE -ne 0) { throw "CodexSaver Python package installation failed." }

Write-Host "[2/3] Registering the global Codex MCP server..."
& py -3 $engineCli install --global --workspace $engineRoot
if ($LASTEXITCODE -ne 0) { throw "CodexSaver MCP registration failed." }

Write-Host "[3/3] Checking the installation..."
& py -3 $engineCli doctor --workspace $engineRoot
if ($LASTEXITCODE -ne 0) { throw "CodexSaver installation check failed." }

Write-Host ""
Write-Host "Installation complete. Restart Codex, then run .\start.ps1."
Write-Host "Enter the DeepSeek API Key in the dashboard. It is never stored in Git."
