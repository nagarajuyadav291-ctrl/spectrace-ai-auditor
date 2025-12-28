# ⚡ Quick Start Guide

Get SpecTrace running in 5 minutes!

## Prerequisites Check

```bash
python3 --version  # Should be 3.9+
node --version     # Should be 18+
docker --version   # Should be installed
```

## Installation (3 Steps)

### 1️⃣ Clone & Setup

```bash
git clone https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor.git
cd spectrace-ai-auditor
docker-compose up -d
```

### 2️⃣ Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
python -c "from app.database import init_db; init_db()"
python -m app.main
```

### 3️⃣ Frontend Setup (New Terminal)

```bash
cd frontend
npm install
npm install -g @angular/cli
ng serve
```

## Access

Open browser: **http://localhost:4200**

## First Task

1. Enter task: `"Analyze recent AI safety research"`
2. Select: **GPT-4**
3. Max steps: **10**
4. Click: **Execute & Audit**

## Troubleshooting

### Backend Issues
```bash
# Database not ready
docker-compose restart postgres

# Module not found
pip install -r requirements.txt

# Port in use
# Change port in main.py: uvicorn.run(app, port=8001)
```

### Frontend Issues
```bash
# Angular CLI missing
npm install -g @angular/cli

# Port in use
ng serve --port 4300
```

### API Key Issues
```bash
# Check .env file
cat backend/.env

# Verify format (no quotes, no spaces)
OPENAI_API_KEY=sk-proj-...
```

## Stopping

```bash
# Stop frontend: Ctrl+C
# Stop backend: Ctrl+C
# Stop Docker: docker-compose down
```

## Restarting

```bash
# Terminal 1
docker-compose up -d
cd backend && source venv/bin/activate && python -m app.main

# Terminal 2
cd frontend && ng serve
```

## API Endpoints

- **Health**: http://localhost:8000/health
- **Docs**: http://localhost:8000/docs
- **Execute**: POST http://localhost:8000/api/execute
- **History**: GET http://localhost:8000/api/executions
- **Drift**: GET http://localhost:8000/api/analytics/drift

## File Structure

```
spectrace-ai-auditor/
├── backend/
│   ├── app/
│   │   ├── main.py              # API server
│   │   ├── database.py          # Database models
│   │   ├── agents/executor.py   # Agent execution
│   │   └── analysis/            # Analysis modules
│   ├── requirements.txt
│   └── .env                     # API keys (create this!)
├── frontend/
│   ├── src/app/                 # Angular app
│   └── package.json
├── docker-compose.yml           # Database services
└── README.md
```

## Common Commands

```bash
# View logs
docker-compose logs postgres
docker-compose logs redis

# Database shell
docker exec -it spectrace-postgres psql -U spectrace -d spectrace

# Check running services
docker-compose ps

# Restart everything
docker-compose restart
```

## Environment Variables

```env
# backend/.env
DATABASE_URL=postgresql://spectrace:spectrace123@localhost:5432/spectrace
OPENAI_API_KEY=sk-proj-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here  # Optional
REDIS_URL=redis://localhost:6379
```

## Testing

```bash
# Test backend health
curl http://localhost:8000/health

# Test database connection
docker exec spectrace-postgres pg_isready

# Test Redis
docker exec spectrace-redis redis-cli ping
```

## Next Steps

1. ✅ Read [INSTALLATION.md](INSTALLATION.md) for detailed setup
2. ✅ Read [PROJECT_EXPLANATION.md](PROJECT_EXPLANATION.md) to understand the system
3. ✅ Customize spec rules in `backend/app/analysis/spec_compliance.py`
4. ✅ Explore API docs at http://localhost:8000/docs

## Support

- **Issues**: https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor/issues
- **Email**: nagarajuyadav291@gmail.com

---

**Happy Auditing! 🔍**
