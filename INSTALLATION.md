# 🚀 STEP-BY-STEP INSTALLATION GUIDE

This guide will walk you through setting up SpecTrace on your local machine.

## Prerequisites

Before starting, ensure you have:
- **Python 3.9+** installed
- **Node.js 18+** installed
- **Docker & Docker Compose** installed
- **Git** installed
- **OpenAI API Key** (required)
- **Anthropic API Key** (optional)

## Step 1: Clone the Repository

```bash
git clone https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor.git
cd spectrace-ai-auditor
```

## Step 2: Start Database Services

Start PostgreSQL and Redis using Docker:

```bash
docker-compose up -d
```

Verify services are running:
```bash
docker-compose ps
```

You should see both `spectrace-postgres` and `spectrace-redis` running.

## Step 3: Setup Backend

### 3.1 Create Virtual Environment

```bash
cd backend
python3 -m venv venv
```

### 3.2 Activate Virtual Environment

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

### 3.3 Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

This will install all required Python packages including FastAPI, PyTorch, Transformers, etc.

### 3.4 Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` file and add your API keys:
```bash
nano .env  # or use any text editor
```

Update these values:
```env
DATABASE_URL=postgresql://spectrace:spectrace123@localhost:5432/spectrace
OPENAI_API_KEY=sk-your-actual-openai-key-here
ANTHROPIC_API_KEY=sk-ant-your-actual-anthropic-key-here
REDIS_URL=redis://localhost:6379
```

**Important:** Replace `sk-your-actual-openai-key-here` with your real OpenAI API key!

### 3.5 Initialize Database

```bash
python -c "from app.database import init_db; init_db()"
```

You should see: `✅ Database initialized successfully!`

### 3.6 Start Backend Server

```bash
python -m app.main
```

The backend will start on `http://localhost:8000`

You should see:
```
🚀 SpecTrace API started successfully!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Keep this terminal open!**

## Step 4: Setup Frontend

Open a **NEW terminal** window.

### 4.1 Navigate to Frontend Directory

```bash
cd spectrace-ai-auditor/frontend
```

### 4.2 Install Dependencies

```bash
npm install
```

This will install Angular and all required packages.

### 4.3 Install Angular CLI (if not already installed)

```bash
npm install -g @angular/cli
```

### 4.4 Start Frontend Server

```bash
ng serve
```

The frontend will start on `http://localhost:4200`

You should see:
```
✔ Browser application bundle generation complete.
** Angular Live Development Server is listening on localhost:4200 **
```

**Keep this terminal open too!**

## Step 5: Access the Application

Open your web browser and go to:
```
http://localhost:4200
```

You should see the SpecTrace dashboard! 🎉

## Step 6: Test the Application

### 6.1 Execute Your First Task

1. In the "Execute Agent Task" panel, enter a task:
   ```
   Research the latest developments in AI safety and summarize key findings
   ```

2. Select agent type: **GPT-4**

3. Set max steps: **10**

4. Click **"🚀 Execute & Audit"**

5. Wait for execution to complete (may take 30-60 seconds)

6. You'll see a success message with risk score!

### 6.2 View Results

- Check the **Execution History** table
- Click **"View"** button to see detailed analysis
- Review the **Behavioral Drift Analysis** panel

## Troubleshooting

### Backend won't start

**Error: `ModuleNotFoundError`**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

**Error: `Database connection failed`**
```bash
# Check if PostgreSQL is running
docker-compose ps

# Restart services
docker-compose restart postgres
```

### Frontend won't start

**Error: `ng: command not found`**
```bash
# Install Angular CLI globally
npm install -g @angular/cli
```

**Error: `Port 4200 already in use`**
```bash
# Use a different port
ng serve --port 4300
```

### API Key Issues

**Error: `401 Unauthorized` or `Invalid API key`**
- Double-check your API key in `backend/.env`
- Ensure no extra spaces or quotes
- Verify key is active on OpenAI dashboard

### Database Issues

**Error: `relation "agent_executions" does not exist`**
```bash
# Reinitialize database
cd backend
source venv/bin/activate
python -c "from app.database import init_db; init_db()"
```

## Stopping the Application

### Stop Frontend
Press `Ctrl+C` in the frontend terminal

### Stop Backend
Press `Ctrl+C` in the backend terminal

### Stop Docker Services
```bash
docker-compose down
```

## Restarting the Application

### Start Everything
```bash
# Terminal 1: Start Docker services
docker-compose up -d

# Terminal 2: Start backend
cd backend
source venv/bin/activate
python -m app.main

# Terminal 3: Start frontend
cd frontend
ng serve
```

## Quick Start Script

For convenience, you can use the automated setup script:

```bash
chmod +x setup.sh
./setup.sh
```

This will:
- Check prerequisites
- Setup backend virtual environment
- Install all dependencies
- Start Docker services
- Initialize database

## Verifying Installation

### Check Backend Health
```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status":"healthy","timestamp":"2024-..."}
```

### Check Frontend
Open `http://localhost:4200` - you should see the SpecTrace dashboard

### Check Database
```bash
docker exec -it spectrace-postgres psql -U spectrace -d spectrace -c "\dt"
```

Should show tables: `agent_executions`, `behavioral_patterns`, `spec_rules`

## Next Steps

1. **Customize Spec Rules**: Edit `backend/app/analysis/spec_compliance.py`
2. **Add Custom Agents**: Extend `backend/app/agents/executor.py`
3. **Explore API**: Visit `http://localhost:8000/docs` for API documentation
4. **Run Tests**: Execute test suite (when available)

## Getting Help

- **Issues**: https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor/issues
- **Email**: nagarajuyadav291@gmail.com
- **Documentation**: See main README.md

## System Requirements

- **RAM**: Minimum 4GB, Recommended 8GB+
- **Disk**: 2GB free space
- **OS**: macOS, Linux, or Windows 10/11
- **Internet**: Required for API calls

---

**Congratulations! You've successfully set up SpecTrace!** 🎉
