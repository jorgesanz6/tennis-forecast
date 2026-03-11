# Script para lanzar la Tennis Forecast WebApp en Localhost

Write-Host "Iniciando Backend (FastAPI)..." -ForegroundColor Cyan
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m uvicorn main:app --reload --port 8000" -WorkingDirectory (Join-Path $PSScriptRoot "backend")

Write-Host "Iniciando Frontend (Server HTTP)..." -ForegroundColor Green
Start-Process -NoNewWindow -FilePath "python" -ArgumentList "-m http.server 3000" -WorkingDirectory (Join-Path $PSScriptRoot "frontend")

Write-Host "`nWebApp lista!" -ForegroundColor Yellow
Write-Host "Frontend: http://localhost:3000"
Write-Host "Backend API: http://localhost:8000"
Write-Host "Presiona Ctrl+C en las terminales para detener."
