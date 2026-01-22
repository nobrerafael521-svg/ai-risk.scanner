# Run backend in dev mode (Windows PowerShell)

Set-Location (Join-Path $PSScriptRoot "..\..\backend")

if (!(Test-Path ".venv")) {
    python -m venv .venv
}

.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

$env:APP_ENV="development"
$env:APP_HOST="127.0.0.1"
$env:APP_PORT="8000"

.\.venv\Scripts\python.exe -m uvicorn app.main:app --host $env:APP_HOST --port $env:APP_PORT --reload
