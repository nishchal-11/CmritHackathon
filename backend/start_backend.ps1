# Start Operation Gridlock Backend Server
Write-Host "🚀 Starting Operation Gridlock Backend..." -ForegroundColor Green
Write-Host ""

# Change to backend directory
Set-Location $PSScriptRoot

# Start the server
Write-Host "Starting FastAPI server on http://127.0.0.1:8000" -ForegroundColor Yellow
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

