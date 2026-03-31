# PTS backend: Python 3.11.x (project validated on 3.11.9). See repo README.md and .python-version.
param(
    [string]$ProjectRoot = ".",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$backendPath = Join-Path $ProjectRoot "backend"
if (!(Test-Path $backendPath)) {
    throw "Backend folder not found at $backendPath"
}
$backendPath = (Resolve-Path $backendPath).Path

Set-Location $backendPath

if (!(Test-Path ".venv")) {
    python -m venv .venv
}

& ".\.venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\.venv\Scripts\python.exe" -m pip install -r requirements.txt

if (!(Test-Path ".env")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Created backend/.env from .env.example. Update credentials before production use."
}

$uvicornArgs = "app.main:app --host 0.0.0.0 --port $Port"
Start-Process -FilePath ".\.venv\Scripts\python.exe" -ArgumentList "-m uvicorn $uvicornArgs" -WorkingDirectory $backendPath

Write-Host "Backend started on port $Port."
Write-Host "Health check: http://localhost:$Port/health"
