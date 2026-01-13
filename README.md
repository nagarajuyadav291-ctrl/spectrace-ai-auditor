# 🛡️ SpecTrace - AI Safety Monitor

**Ultra-modern AI chat interface with real-time safety monitoring**

![Status](https://img.shields.io/badge/Status-Active-success)
![License](https://img.shields.io/badge/License-MIT-blue)
![Python](https://img.shields.io/badge/Python-3.8+-blue)

---

## ✨ Features

- 🎨 **Ultra-Modern UI** - Tailwind CSS with purple gradients
- 🤖 **15+ AI Models** - Groq, Google Gemini, Cohere, OpenAI, Claude
- 🛡️ **Real-Time Safety** - Multi-engine risk analysis
- 🆓 **100% Free Tier** - No credit card required
- ⚡ **Lightning Fast** - Groq models respond instantly

---

## 🚀 Quick Start

```powershell
# 1. Clone
git clone https://github.com/nagarajuyadav291-ctrl/spectrace-ai-auditor.git
cd spectrace-ai-auditor

# 2. Create backend/.env
# Add: GROQ_API_KEY=your_key_here

# 3. Setup backend
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# 4. Run backend (Terminal 1)
uvicorn app.main:app --reload --port 8000

# 5. Run frontend (Terminal 2)
cd frontend-v2
python -m http.server 3000

# 6. Open: http://localhost:3000
```

**See [QUICKSTART.md](QUICKSTART.md) for detailed steps**

---

## 📁 Project Structure

```
spectrace-ai-auditor/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── main.py      # API endpoints
│   │   ├── models.py    # Database models
│   │   ├── agents/      # AI agent logic
│   │   ├── analysis/    # Risk analysis
│   │   └── realtime/    # Real-time monitoring
│   ├── .env             # API keys (create this)
│   └── requirements.txt # Python packages
│
├── frontend-v2/         # Modern UI
│   ├── index.html       # Main UI
│   └── app.js           # JavaScript logic
│
├── README.md            # This file
├── QUICKSTART.md        # Setup guide
└── FREE_API_KEYS.md     # API key guide
```

---

## 🎨 UI Preview

### **Welcome Screen**
- Purple gradient logo with shield icon
- Sidebar with chat history
- 3 example cards (Examples, Science, Safety)
- Modern input with gradient border

### **Chat Interface**
- User messages (blue gradient avatar)
- AI messages (purple gradient avatar)
- Real-time risk badges (green/yellow/red)
- Copy/Regenerate/Safety buttons

### **Safety Panel**
- Overall risk score
- Deception probability
- Content safety metrics
- Violation alerts

---

## 🔑 Supported AI Models

### **Free Models**
- 🦙 Llama 3.1 70B (Groq) - Fastest
- 🦙 Llama 3.1 8B (Groq) - Ultra-fast
- 🌀 Mixtral 8x7B (Groq)
- 💎 Gemini 1.5 Flash (Google)
- 💎 Gemini 1.5 Pro (Google)
- 🔮 Command R (Cohere)

### **Premium Models**
- 🤖 GPT-4o (OpenAI)
- 🧠 Claude 3.5 Sonnet (Anthropic)

---

## 🛡️ Safety Features

- **Multi-Engine Analysis** - Combines multiple AI safety models
- **Risk Scoring** - 0-100% risk score for every response
- **Deception Detection** - Identifies misleading information
- **Content Safety** - Toxicity, hate speech, violence detection
- **Compliance Checking** - Regulatory compliance validation
- **Real-Time Monitoring** - Instant safety analysis

---

## 📖 Documentation

- [QUICKSTART.md](QUICKSTART.md) - Quick setup guide
- [FREE_API_KEYS.md](FREE_API_KEYS.md) - Get free API keys
- [LICENSE](LICENSE) - MIT License

---

## 🐛 Troubleshooting

**Module not found?**
```powershell
cd backend
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

**Port in use?**
```powershell
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force
```

**Old UI showing?**
- Use `http://localhost:3000` (NOT 8000)
- Hard refresh: `Ctrl + Shift + R`

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## 📄 License

MIT License - see [LICENSE](LICENSE) file

---

## 🌟 Star This Repo!

If you find SpecTrace useful, please star this repository! ⭐

---

**Built with ❤️ for AI Safety**
