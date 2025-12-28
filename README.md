# 🔍 SpecTrace: AI Behavior Auditor

**Autonomous AI-System Behavior Auditor for Agentic Models**

SpecTrace is a production-grade AI auditing system that continuously inspects, stress-tests, and explains agentic AI behavior under real-world task execution.

## 🎯 Problem Statement

AI-2027 research highlights that agentic AI systems fail not due to lack of capability, but due to:
- **Misalignment** - Agents pursuing unintended goals
- **Deception** - Hiding true intentions from operators
- **Shallow Honesty** - Appearing truthful while gaming systems
- **Unverifiable Reasoning** - Black-box decision making

**SpecTrace solves this** by providing continuous behavioral forensics for deployed AI agents.

## ✨ Core Features

### 🔬 Behavioral Analysis
- **Pattern Encoding** - Transformer-based behavioral embeddings
- **Deception Detection** - Identifies instrumental vs terminal honesty
- **Spec Compliance** - Rule-based + learned constraint checking
- **Drift Tracking** - Monitors behavioral changes over time

### 📊 Real-time Monitoring
- Live execution traces with full transparency
- Risk scoring per task execution
- Violation detection and alerting
- Historical trend analysis

### 🎨 Beautiful Dashboard
- Clean, modern Angular UI
- Real-time execution monitoring
- Interactive drift analytics
- Detailed execution forensics

## 🏗️ Architecture

```
┌─────────────────┐
│   Angular UI    │  ← Beautiful dashboard
└────────┬────────┘
         │
┌────────▼────────┐
│   FastAPI       │  ← REST API
│   Backend       │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼──┐  ┌──▼───┐
│ AI   │  │ Audit│
│Agent │  │Engine│
└──────┘  └──┬───┘
             │
        ┌────┴────┐
        │         │
    ┌───▼──┐  ┌──▼────┐
    │Vector│  │Postgres│
    │  DB  │  │   DB   │
    └──────┘  └────────┘
```

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- Node.js 18+
- PostgreSQL 15+
- Docker & Docker Compose
- OpenAI API Key
- Anthropic API Key (optional)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor.git
cd spectrace-ai-auditor
```

2. **Start databases**
```bash
docker-compose up -d postgres redis
```

3. **Setup Backend**
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env and add your API keys
nano .env
```

4. **Initialize Database**
```bash
python -c "from app.database import init_db; init_db()"
```

5. **Start Backend Server**
```bash
python -m app.main
# Backend runs on http://localhost:8000
```

6. **Setup Frontend** (New Terminal)
```bash
cd frontend
npm install
npm install -g @angular/cli
```

7. **Start Frontend**
```bash
ng serve
# Frontend runs on http://localhost:4200
```

8. **Open Browser**
```
http://localhost:4200
```

## 📖 Usage Guide

### 1. Execute Agent Task
- Enter a task description (e.g., "Research the latest AI safety papers")
- Select agent type (GPT-4, GPT-3.5, Claude-3)
- Set max execution steps
- Click "Execute & Audit"

### 2. Monitor Execution
- View real-time execution traces
- See risk scores and deception probabilities
- Check spec violations
- Analyze behavioral patterns

### 3. Track Drift
- Monitor behavioral drift over time
- Identify trend changes (increasing/decreasing/stable)
- Detect anomalies in agent behavior

### 4. Review History
- Browse all past executions
- Filter by risk level
- Deep dive into specific executions
- Export audit reports

## 🔧 Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql://spectrace:spectrace123@localhost:5432/spectrace
OPENAI_API_KEY=sk-your-key-here
ANTHROPIC_API_KEY=sk-ant-your-key-here
REDIS_URL=redis://localhost:6379
```

### Spec Rules
Edit `backend/app/analysis/spec_compliance.py` to customize:
- Safety constraints
- Behavioral rules
- Violation severity levels
- Custom compliance checks

## 📊 API Documentation

### Execute Task
```bash
POST /api/execute
{
  "task_description": "Research AI safety",
  "agent_type": "gpt-4",
  "max_steps": 10
}
```

### Get Executions
```bash
GET /api/executions?skip=0&limit=20
```

### Get Drift Analysis
```bash
GET /api/analytics/drift
```

### Get Execution Details
```bash
GET /api/executions/{execution_id}
```

## 🧪 Testing

### Backend Tests
```bash
cd backend
pytest tests/
```

### Frontend Tests
```bash
cd frontend
ng test
```

## 🐳 Docker Deployment

### Full Stack Deployment
```bash
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Redis (port 6379)
- Backend API (port 8000)
- Frontend UI (port 4200)

## 📁 Project Structure

```
spectrace-ai-auditor/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # Database models & connection
│   │   ├── models.py            # Pydantic schemas
│   │   ├── agents/
│   │   │   ├── executor.py      # Agent execution engine
│   │   │   └── tracer.py        # Execution tracing
│   │   ├── analysis/
│   │   │   ├── behavioral_encoder.py    # Behavior embeddings
│   │   │   ├── deception_detector.py    # Deception analysis
│   │   │   └── spec_compliance.py       # Rule checking
│   │   └── api/
│   │       └── routes.py        # API endpoints
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── app.component.ts
│   │   │   ├── app.component.html
│   │   │   └── app.component.css
│   │   └── environments/
│   ├── package.json
│   └── angular.json
├── docker-compose.yml
├── setup.sh
└── README.md
```

## 🎓 How It Works

### 1. Execution Capture
- Agent receives task
- Every step is traced (thoughts, actions, tool calls)
- Full execution graph stored

### 2. Behavioral Analysis
- Traces encoded into embeddings using Sentence Transformers
- Pattern matching against known behaviors
- Similarity search in vector database

### 3. Deception Detection
- Linguistic analysis of agent reasoning
- Pattern matching for deceptive indicators
- Probability scoring using contrastive learning

### 4. Spec Compliance
- Rule-based checking against safety constraints
- Violation detection and severity classification
- Risk score calculation

### 5. Drift Analysis
- Time-series analysis of risk scores
- Trend detection (increasing/decreasing/stable)
- Anomaly identification

## 🔒 Security Considerations

- API keys stored in environment variables
- Database credentials not committed
- Input validation on all endpoints
- SQL injection prevention via SQLAlchemy ORM
- CORS configured for production

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Inspired by AI-2027 research on agent alignment
- Built with FastAPI, Angular, PyTorch
- Uses OpenAI and Anthropic APIs

## 📞 Support

- Issues: [GitHub Issues](https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor/issues)
- Email: nagarajuyadav291@gmail.com

## 🎯 Roadmap

- [ ] Multi-agent coordination auditing
- [ ] Advanced ML-based deception models
- [ ] Real-time alerting system
- [ ] Export audit reports (PDF/JSON)
- [ ] Integration with LangChain/AutoGPT
- [ ] Custom rule builder UI
- [ ] Slack/Discord notifications

---

**Built with ❤️ for AI Safety**
