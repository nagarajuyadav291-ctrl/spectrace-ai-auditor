# SpecTrace Windows Quick Fix Script
# Run this in PowerShell to fix all issues

Write-Host "🔧 SpecTrace Quick Fix Script" -ForegroundColor Cyan
Write-Host "=============================" -ForegroundColor Cyan
Write-Host ""

# Check if in correct directory
if (-not (Test-Path "backend") -or -not (Test-Path "frontend")) {
    Write-Host "❌ Error: Please run this script from the spectrace-ai-auditor directory" -ForegroundColor Red
    exit 1
}

# Pull latest changes
Write-Host "📥 Pulling latest changes..." -ForegroundColor Yellow
git pull origin main

# Backend setup
Write-Host ""
Write-Host "🐍 Setting up backend..." -ForegroundColor Yellow
cd backend

# Check if venv exists
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Green
    python -m venv venv
}

# Activate venv and install
Write-Host "Installing dependencies..." -ForegroundColor Green
& .\venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt

# Check for .env
if (-not (Test-Path ".env")) {
    Write-Host "Creating .env file..." -ForegroundColor Green
    Copy-Item .env.example .env
    Write-Host "⚠️  IMPORTANT: Edit backend\.env and add your OPENAI_API_KEY" -ForegroundColor Yellow
}

# Initialize database
Write-Host "Initializing database..." -ForegroundColor Green
python -c "from app.database import init_db; init_db()"

cd ..

# Frontend setup
Write-Host ""
Write-Host "🎨 Setting up frontend..." -ForegroundColor Yellow
cd frontend

Write-Host "Installing dependencies..." -ForegroundColor Green
npm install

cd ..

Write-Host ""
Write-Host "✅ Setup complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📝 Next steps:" -ForegroundColor Cyan
Write-Host "1. Edit backend\.env and add your OPENAI_API_KEY"
Write-Host "2. Start backend: cd backend && .\venv\Scripts\Activate.ps1 && python -m app.main"
Write-Host "3. Start frontend (new terminal): cd frontend && ng serve"
Write-Host "4. Open http://localhost:4200"
Write-Host ""
Write-Host "📚 Documentation: See WINDOWS_SETUP.md for detailed instructions"
