$ErrorActionPreference = "Stop"

Write-Host "=============================================" -ForegroundColor Cyan
Write-Host " STREAMLIT SUPABASE AGENT OOP" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan

if (Test-Path ".\.venv\Scripts\Activate.ps1") {
    . ".\.venv\Scripts\Activate.ps1"
} else {
    python -m venv .venv
    . ".\.venv\Scripts\Activate.ps1"
    pip install -r requirements.txt
}

streamlit run app.py
