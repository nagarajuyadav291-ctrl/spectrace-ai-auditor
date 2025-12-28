#!/bin/bash

echo "🚀 SpecTrace Setup Script"
echo "=========================="
echo ""

# Check prerequisites
echo "📋 Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.9 or higher."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18 or higher."
    exit 1
fi

if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker."
    exit 1
fi

echo "✅ All prerequisites found!"
echo ""

# Backend setup
echo "📦 Setting up backend..."
cd backend

# Create virtual environment
python3 -m venv venv
echo "✅ Virtual environment created"

# Activate virtual environment
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
echo "📥 Installing Python dependencies..."
pip install -r requirements.txt
echo "✅ Backend dependencies installed"

# Create .env file
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  IMPORTANT: Edit backend/.env and add your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - ANTHROPIC_API_KEY (optional)"
else
    echo "ℹ️  .env file already exists"
fi

cd ..

# Frontend setup
echo ""
echo "🎨 Setting up frontend..."
cd frontend

# Install dependencies
echo "📥 Installing Node.js dependencies..."
npm install
echo "✅ Frontend dependencies installed"

# Install Angular CLI globally
echo "📥 Installing Angular CLI..."
npm install -g @angular/cli
echo "✅ Angular CLI installed"

cd ..

# Docker setup
echo ""
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis
echo "✅ PostgreSQL and Redis started"

# Wait for PostgreSQL to be ready
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 5

# Initialize database
echo "🗄️  Initializing database..."
cd backend
source venv/bin/activate
python -c "from app.database import init_db; init_db()"
echo "✅ Database initialized"
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Edit backend/.env and add your API keys"
echo "2. Start backend: cd backend && source venv/bin/activate && python -m app.main"
echo "3. Start frontend (new terminal): cd frontend && ng serve"
echo "4. Open http://localhost:4200 in your browser"
echo ""
echo "📚 Documentation: See README.md for detailed usage instructions"
