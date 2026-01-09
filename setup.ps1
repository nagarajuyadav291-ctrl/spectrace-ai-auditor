# SpecTrace - Quick Setup Script
# Run this to fix everything!

Write-Host "🚀 SpecTrace Setup Starting..." -ForegroundColor Green
Write-Host ""

# Step 1: Fix .env file
Write-Host "📝 Step 1: Fixing .env file..." -ForegroundColor Yellow
$envPath = "backend\.env"

$envContent = @"
# Database (SQLite - no PostgreSQL needed!)
DATABASE_URL=sqlite:///./spectrace.db

# FREE APIs (Get keys from links below)
GROQ_API_KEY=your_groq_key_here
GOOGLE_API_KEY=your_google_key_here
COHERE_API_KEY=your_cohere_key_here
PERSPECTIVE_API_KEY=your_perspective_key_here

# Optional: Paid APIs
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here
"@

Set-Content -Path $envPath -Value $envContent
Write-Host "✅ .env file created!" -ForegroundColor Green
Write-Host ""

# Step 2: Install packages
Write-Host "📦 Step 2: Installing Python packages..." -ForegroundColor Yellow
cd backend
.\venv\Scripts\Activate.ps1

pip install --quiet google-generativeai cohere anthropic httpx

Write-Host "✅ Packages installed!" -ForegroundColor Green
Write-Host ""

# Step 3: Show API key links
Write-Host "🔑 Step 3: Get FREE API Keys:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Groq (Fastest, FREE):" -ForegroundColor Cyan
Write-Host "   https://console.groq.com" -ForegroundColor White
Write-Host ""
Write-Host "2. Google Gemini (FREE):" -ForegroundColor Cyan
Write-Host "   https://aistudio.google.com/app/apikey" -ForegroundColor White
Write-Host ""
Write-Host "3. Cohere (FREE):" -ForegroundColor Cyan
Write-Host "   https://dashboard.cohere.com/api-keys" -ForegroundColor White
Write-Host ""
Write-Host "4. Perspective API (FREE):" -ForegroundColor Cyan
Write-Host "   https://developers.perspectiveapi.com/s/docs-get-started" -ForegroundColor White
Write-Host ""

# Step 4: Instructions
Write-Host "📋 Step 4: Next Steps:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Get API keys from links above" -ForegroundColor White
Write-Host "2. Edit backend\.env and paste your keys" -ForegroundColor White
Write-Host "3. Run: uvicorn app.main:app --reload --port 8000" -ForegroundColor White
Write-Host "4. Open new terminal, run: cd frontend-v2 && python -m http.server 3000" -ForegroundColor White
Write-Host "5. Open browser: http://localhost:3000" -ForegroundColor White
Write-Host ""

Write-Host "🎉 Setup Complete! Follow steps above to start." -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
