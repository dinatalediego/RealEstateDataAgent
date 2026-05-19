$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host " DECIDECASA AGENTOS - STREAMLIT + SUPABASE" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    Write-Host "Activando .venv existente..." -ForegroundColor Green
    . ".\.venv\Scripts\Activate.ps1"
}
else {
    Write-Host "Creando entorno virtual .venv..." -ForegroundColor Yellow
    python -m venv .venv
    . ".\.venv\Scripts\Activate.ps1"
}

Write-Host "Instalando dependencias..." -ForegroundColor Yellow
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Levantando Streamlit..." -ForegroundColor Green
streamlit run app.py
