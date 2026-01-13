# SpecTrace - Clean Setup & Run Script
# This script cleans old files and runs everything fresh!

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║         🧹 SPECTRACE CLEAN SETUP & RUN 🧹                  ║" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Stop any running servers
Write-Host "🛑 Step 1: Stopping any running servers..." -ForegroundColor Yellow
Write-Host ""

# Kill processes on ports 3000 and 8000
$ports = @(3000, 8000)
foreach ($port in $ports) {
    $process = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique
    if ($process) {
        Stop-Process -Id $process -Force -ErrorAction SilentlyContinue
        Write-Host "✅ Stopped process on port $port" -ForegroundColor Green
    }
}

Write-Host ""

# Step 2: Clean old/unnecessary files
Write-Host "🧹 Step 2: Cleaning old files..." -ForegroundColor Yellow
Write-Host ""

# Remove old frontend (Angular - not needed)
if (Test-Path "frontend") {
    Remove-Item -Path "frontend" -Recurse -Force
    Write-Host "✅ Removed old Angular frontend" -ForegroundColor Green
}

# Remove unnecessary documentation files
$docsToRemove = @(
    "IMPLEMENTATION_GUIDE.md",
    "INSTALLATION.md",
    "PROJECT_EXPLANATION.md",
    "QUICKSTART.md",
    "REVOLUTIONARY_FEATURES.md",
    "SETUP_SUMMARY.md",
    "UPGRADE_GUIDE.md",
    "VISUAL_GUIDE.md",
    "WINDOWS_SETUP.md",
    "setup.sh",
    "windows-setup.ps1"
)

foreach ($doc in $docsToRemove) {
    if (Test-Path $doc) {
        Remove-Item -Path $doc -Force
        Write-Host "✅ Removed $doc" -ForegroundColor Green
    }
}

# Remove Docker files (not needed for local dev)
if (Test-Path "docker-compose.yml") {
    Remove-Item -Path "docker-compose.yml" -Force
    Write-Host "✅ Removed docker-compose.yml" -ForegroundColor Green
}

Write-Host ""
Write-Host "✅ Cleanup complete!" -ForegroundColor Green
Write-Host ""

# Step 3: Setup .env file
Write-Host "📝 Step 3: Setting up .env file..." -ForegroundColor Yellow
Write-Host ""

$envPath = "backend\.env"

$envContent = @"
# SpecTrace Configuration
# Get FREE API keys from: FREE_API_KEYS.md

# Database (SQLite - no setup needed!)
DATABASE_URL=sqlite:///./spectrace.db

# ===== FREE APIs (No Credit Card Required!) =====

# GROQ (Fastest, FREE forever!)
# Get from: https://console.groq.com
GROQ_API_KEY=your_groq_key_here

# GOOGLE GEMINI (FREE tier)
# Get from: https://aistudio.google.com/app/apikey
GOOGLE_API_KEY=your_google_key_here

# COHERE (FREE trial)
# Get from: https://dashboard.cohere.com/api-keys
COHERE_API_KEY=your_cohere_key_here

# PERSPECTIVE API (FREE - for safety scoring)
# Get from: https://developers.perspectiveapi.com/s/docs-get-started
PERSPECTIVE_API_KEY=your_perspective_key_here

# ===== Optional: PAID APIs =====

# OPENAI (GPT-4, GPT-3.5)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_key_here

# ANTHROPIC (Claude)
# Get from: https://console.anthropic.com
ANTHROPIC_API_KEY=your_anthropic_key_here
"@

Set-Content -Path $envPath -Value $envContent
Write-Host "✅ .env file created!" -ForegroundColor Green
Write-Host ""

# Step 4: Install Python packages
Write-Host "📦 Step 4: Installing Python packages..." -ForegroundColor Yellow
Write-Host ""

cd backend

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "⚠️  Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment created!" -ForegroundColor Green
}

Write-Host ""
Write-Host "Installing packages..." -ForegroundColor Cyan

# Install all required packages
pip install --quiet --upgrade pip
pip install --quiet fastapi uvicorn sqlalchemy python-dotenv
pip install --quiet google-generativeai cohere anthropic openai
pip install --quiet httpx requests

Write-Host "✅ All packages installed!" -ForegroundColor Green
Write-Host ""

cd ..

# Step 5: Show API key instructions
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "║              🔑 GET YOUR FREE API KEYS 🔑                  ║" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

Write-Host "Get at least GROQ (fastest, completely FREE):" -ForegroundColor White
Write-Host ""

Write-Host "1️⃣  GROQ (Recommended - Fastest!)" -ForegroundColor Cyan
Write-Host "   → https://console.groq.com" -ForegroundColor White
Write-Host "   → Sign up → API Keys → Create → Copy key" -ForegroundColor Gray
Write-Host ""

Write-Host "2️⃣  GOOGLE GEMINI (Optional)" -ForegroundColor Cyan
Write-Host "   → https://aistudio.google.com/app/apikey" -ForegroundColor White
Write-Host ""

Write-Host "3️⃣  COHERE (Optional)" -ForegroundColor Cyan
Write-Host "   → https://dashboard.cohere.com/api-keys" -ForegroundColor White
Write-Host ""

Write-Host "📖 Full guide: FREE_API_KEYS.md" -ForegroundColor Yellow
Write-Host ""

# Step 6: Ask if user has API keys
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
Write-Host "║                                                            ║" -ForegroundColor Yellow
Write-Host "║              ⚠️  IMPORTANT: API KEYS NEEDED ⚠️              ║" -ForegroundColor Yellow
Write-Host "║                                                            ║" -ForegroundColor Yellow
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
Write-Host ""

$hasKeys = Read-Host "Do you have API keys ready? (y/n)"

if ($hasKeys -eq "y" -or $hasKeys -eq "Y") {
    Write-Host ""
    Write-Host "Great! Opening .env file for you to paste keys..." -ForegroundColor Green
    Start-Sleep -Seconds 2
    notepad backend\.env
    
    Write-Host ""
    Write-Host "Press any key after you've added your API keys..." -ForegroundColor Yellow
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    
    # Step 7: Start servers
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                            ║" -ForegroundColor Green
    Write-Host "║                  🚀 STARTING SERVERS 🚀                    ║" -ForegroundColor Green
    Write-Host "║                                                            ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    
    # Start backend in new window
    Write-Host "🔧 Starting backend server..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\backend'; .\venv\Scripts\Activate.ps1; uvicorn app.main:app --reload --port 8000"
    
    Start-Sleep -Seconds 3
    
    # Start frontend in new window
    Write-Host "🎨 Starting frontend server..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd '$PWD\frontend-v2'; python -m http.server 3000"
    
    Start-Sleep -Seconds 2
    
    # Open browser
    Write-Host "🌐 Opening browser..." -ForegroundColor Cyan
    Start-Sleep -Seconds 3
    Start-Process "http://localhost:3000"
    
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║                                                            ║" -ForegroundColor Green
    Write-Host "║                  ✅ ALL DONE! ✅                            ║" -ForegroundColor Green
    Write-Host "║                                                            ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    
    Write-Host "🎉 SpecTrace is now running!" -ForegroundColor Green
    Write-Host ""
    Write-Host "📍 Frontend: http://localhost:3000" -ForegroundColor Cyan
    Write-Host "📍 Backend:  http://localhost:8000" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "💡 Look for the purple gradient UI with sidebar!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To stop servers: Close the PowerShell windows" -ForegroundColor Gray
    Write-Host ""
    
} else {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Yellow
    Write-Host "║                                                            ║" -ForegroundColor Yellow
    Write-Host "║              📋 NEXT STEPS 📋                              ║" -ForegroundColor Yellow
    Write-Host "║                                                            ║" -ForegroundColor Yellow
    Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "1. Get FREE API keys (10 minutes):" -ForegroundColor White
    Write-Host "   → https://console.groq.com" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "2. Add keys to .env file:" -ForegroundColor White
    Write-Host "   notepad backend\.env" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "3. Run this script again:" -ForegroundColor White
    Write-Host "   .\clean-setup.ps1" -ForegroundColor Cyan
    Write-Host ""
}

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
