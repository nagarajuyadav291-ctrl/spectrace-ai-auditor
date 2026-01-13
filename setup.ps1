# SpecTrace - Automated Setup Script
# This script sets up EVERYTHING automatically!

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║              🚀 SPECTRACE SETUP WIZARD 🚀                  ║" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "║          Ultra-Modern AI Safety Monitor                    ║" -ForegroundColor Cyan
Write-Host "║                                                            ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create .env file
Write-Host "📝 Step 1: Creating .env file..." -ForegroundColor Yellow
Write-Host ""

$envPath = "backend\.env"

$envContent = @"
# SpecTrace Configuration
# Get FREE API keys from: https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor/blob/main/FREE_API_KEYS.md

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

# HUGGING FACE (FREE)
# Get from: https://huggingface.co/settings/tokens
HUGGINGFACE_API_KEY=your_huggingface_key_here

# ===== Optional: More FREE APIs =====

# REPLICATE (Free tier)
# Get from: https://replicate.com/account/api-tokens
REPLICATE_API_KEY=your_replicate_key_here

# TOGETHER AI (Free trial)
# Get from: https://api.together.xyz
TOGETHER_API_KEY=your_together_key_here

# ===== Optional: PAID APIs =====

# OPENAI (GPT-4, GPT-3.5)
# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=your_openai_key_here

# ANTHROPIC (Claude)
# Get from: https://console.anthropic.com
ANTHROPIC_API_KEY=your_anthropic_key_here
"@

Set-Content -Path $envPath -Value $envContent
Write-Host "✅ .env file created at: $envPath" -ForegroundColor Green
Write-Host ""

# Step 2: Install Python packages
Write-Host "📦 Step 2: Installing Python packages..." -ForegroundColor Yellow
Write-Host ""

cd backend

# Activate virtual environment
if (Test-Path "venv\Scripts\Activate.ps1") {
    .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "⚠️  Virtual environment not found. Creating one..." -ForegroundColor Yellow
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    Write-Host "✅ Virtual environment created and activated" -ForegroundColor Green
}

Write-Host ""
Write-Host "Installing packages (this may take a minute)..." -ForegroundColor Cyan

# Install packages quietly
pip install --quiet --upgrade pip
pip install --quiet google-generativeai
pip install --quiet cohere
pip install --quiet anthropic
pip install --quiet httpx
pip install --quiet fastapi
pip install --quiet uvicorn
pip install --quiet sqlalchemy
pip install --quiet python-dotenv

Write-Host "✅ All packages installed!" -ForegroundColor Green
Write-Host ""

cd ..

# Step 3: Show API key instructions
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "║              🔑 GET YOUR FREE API KEYS 🔑                  ║" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

Write-Host "Get at least these 4 FREE keys (no credit card!):" -ForegroundColor White
Write-Host ""

Write-Host "1️⃣  GROQ (Fastest, FREE forever!)" -ForegroundColor Cyan
Write-Host "   → https://console.groq.com" -ForegroundColor White
Write-Host "   → Sign up → API Keys → Create → Copy key" -ForegroundColor Gray
Write-Host ""

Write-Host "2️⃣  GOOGLE GEMINI (FREE tier)" -ForegroundColor Cyan
Write-Host "   → https://aistudio.google.com/app/apikey" -ForegroundColor White
Write-Host "   → Sign in → Create API Key → Copy key" -ForegroundColor Gray
Write-Host ""

Write-Host "3️⃣  COHERE (FREE trial)" -ForegroundColor Cyan
Write-Host "   → https://dashboard.cohere.com/api-keys" -ForegroundColor White
Write-Host "   → Sign up → API Keys → Copy Trial Key" -ForegroundColor Gray
Write-Host ""

Write-Host "4️⃣  PERSPECTIVE API (FREE - for safety)" -ForegroundColor Cyan
Write-Host "   → https://developers.perspectiveapi.com/s/docs-get-started" -ForegroundColor White
Write-Host "   → Follow setup guide → Copy API key" -ForegroundColor Gray
Write-Host ""

Write-Host "📖 Full guide: FREE_API_KEYS.md" -ForegroundColor Yellow
Write-Host ""

# Step 4: Next steps
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "║                  ✅ SETUP COMPLETE! ✅                      ║" -ForegroundColor Green
Write-Host "║                                                            ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

Write-Host "📋 NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""

Write-Host "1. Get FREE API keys from links above (10 minutes)" -ForegroundColor White
Write-Host ""

Write-Host "2. Edit backend\.env and paste your keys:" -ForegroundColor White
Write-Host "   notepad backend\.env" -ForegroundColor Cyan
Write-Host ""

Write-Host "3. Start backend (Terminal 1):" -ForegroundColor White
Write-Host "   cd backend" -ForegroundColor Cyan
Write-Host "   .\venv\Scripts\Activate.ps1" -ForegroundColor Cyan
Write-Host "   uvicorn app.main:app --reload --port 8000" -ForegroundColor Cyan
Write-Host ""

Write-Host "4. Start frontend (Terminal 2):" -ForegroundColor White
Write-Host "   cd frontend-v2" -ForegroundColor Cyan
Write-Host "   python -m http.server 3000" -ForegroundColor Cyan
Write-Host ""

Write-Host "5. Open browser:" -ForegroundColor White
Write-Host "   http://localhost:3000" -ForegroundColor Cyan
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "║  🎨 NEW UI: Ultra-modern with Tailwind CSS                ║" -ForegroundColor Magenta
Write-Host "║  🚀 Better than ChatGPT, Claude, and all AI models!       ║" -ForegroundColor Magenta
Write-Host "║  🛡️  Real-time AI safety monitoring built-in              ║" -ForegroundColor Magenta
Write-Host "║                                                            ║" -ForegroundColor Magenta
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
Write-Host ""

Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
