# Dual-Panel Activity & Protocol Visualizer Launcher (PowerShell)
Write-Host "==================================================================" -ForegroundColor Cyan
Write-Host "  Starting Dual-Panel Activity & Protocol Visualizer..." -ForegroundColor Green
Write-Host "  Opening http://127.0.0.1:5000 in your browser..." -ForegroundColor Yellow
Write-Host "==================================================================" -ForegroundColor Cyan

Start-Process "http://127.0.0.1:5000"
python app.py
