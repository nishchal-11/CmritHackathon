# PowerShell script to run the FastAPI backend

Write-Host "🚀 Starting Operation Gridlock Backend..." -ForegroundColor Cyan

# Activate virtual environment
& "..\.venv\Scripts\Activate.ps1"

# Run uvicorn
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
