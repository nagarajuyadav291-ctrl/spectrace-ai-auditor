# SpecTrace - Clean Setup Script
# Run this after fresh clone

Write-Host ""
Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  SpecTrace - Automated Setup              " -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists
if (Test-Path "backend\.env") {
    Write-Host ".env file already exists!" -ForegroundColor Green
} else {
    Write-Host "Creating .env file..." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Please enter your Groq API key:" -ForegroundColor Cyan
    Write-Host "(Get it from: https://console.groq.com)" -ForegroundColor Gray
    $apiKey = Read-Host "API Key"
    
    $envContent = @"
DATABASE_URL=sqlite:///./spectrace.db
GROQ_API_KEY=$apiKey
"@
    
    Set-Content -Path "backend\.env" -Value $envContent
    Write-Host ".env file created!" -ForegroundColor Green
}

Write-Host ""

# Setup backend
Write-Host "Setting up backend..." -ForegroundColor Yellow
cd backend

if (-not (Test-Path "venv")) {
    python -m venv venv
}

.\venv\Scripts\Activate.ps1
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt

Write-Host "Backend setup complete!" -ForegroundColor Green
Write-Host ""

cd ..

# Start servers
Write-Host "============================================" -ForegroundColor Green
Write-Host "  Starting Servers                         " -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""

Write-Host "Starting backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000"

Start-Sleep -Seconds 3

Write-Host "Starting frontend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend-v2'; python -m http.server 3000"

Start-Sleep -Seconds 3

Write-Host "Opening browser..." -ForegroundColor Cyan
Start-Process "http://localhost:3000"

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  All Done!                                " -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend: http://localhost:3000" -ForegroundColor Cyan
Write-Host "Backend:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Look for purple gradient UI!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
